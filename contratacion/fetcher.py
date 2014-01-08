#!/usr/bin/env python
#-*- coding: utf-8 -*-

from gevent import monkey

monkey.patch_all()

import re
import time
import random
import logging
from itertools import chain
from urlparse import urljoin

import gevent
import requests
import lxml
import lxml.etree
from pyquery import PyQuery
from gevent.pool import Pool

from .store import Store
from .helpers import ignore

logger = logging.getLogger('fetcher')


def serialize(element):
    element = PyQuery(element)

    if element.is_('select'):
        val = serialize_select(element)
    else:
        val = element.val()

    return element.attr('name'), val


def serialize_select(select):
    return (select('option[selected="selected"]:first')
            or select('option:first')).val()


def serializeArray(form):
    return map(serialize, form(
        'select[name]:not(:disabled),'
        'input[name][type!="submit"]:not(:disabled)'
    ))


def submit(input):
    input = PyQuery(input)

    form = input.closest('form')
    action = form.attr('action')

    return action, dict(chain(serializeArray(form), [serialize(input)]))


class Profiler(object):
    def __init__(self):
        self.n = 0
        self._start_time = None  # set on first access

    @property
    def start_time(self):
        if self._start_time is None:
            self._start_time = time.time()
        return self._start_time

    @property
    def elapsed_time(self):
        return time.time() - self.start_time

    @property
    def average(self):
        return self.n / self.elapsed_time

    def request_sent(self):
        self.n += 1
        logger.debug('Requests per second: %f (%d requests)', self.average, self.n)


class Sender(object):
    """Manages request creation and sending"""

    def __init__(self, max_retries):
        self.retries = 0
        self.max_retries = max_retries
        self.profiler = Profiler()
        self.session = requests.Session()

    def request(self, url, data=None):
        """Create a prepared request ready to pass to fetch/send methods

        The default method is GET but It will create a
        POST request instead if data is set.

        :param url: Request's url
        :param data: Optional data dictionary
        :rtype: :class:`requests.Request` object.
        """
        method = 'GET' if data is None else 'POST'
        return requests.Request(
            method, url, data=data, cookies=self.session.cookies
        ).prepare()

    def fetch(self, request):
        """Send a prepared request and get the response parsed by PyQuery

        :param request: Prepared request ready to send.
        :rtype: :class:`PyQuery` object.
        """
        response = self.send(request)
        try:
            return PyQuery(response.text)
        except lxml.etree.XMLSyntaxError as error:
            logger.error('Bad response %s:\n%s', response.url, response.text)

    def send(self, request):
        """Send the request and get the response

        :param request: Prepared request ready to send.
        :rtype: :class:`requests.Response` object.
        """
        logger.debug("%s %s", request.method, request.url)
        response = self.session.send(request, verify=False)
        self.profiler.request_sent()
        return response

    def execute(self, function, request):
        times = 0
        result = function(request)

        while self.should_keep_trying(result, times):
            times += 1
            self.wait_for_next_try(times)

            logger.warning('Retrying "%s"', request.url)
            result = function(request)

        if times == self.max_retries:
            logger.warning('Out of reintents (%d) for %s',
                           self.max_retries, request.url)

        return result

    def should_keep_trying(self, result, times):
        return result is None and times < self.max_retries

    def wait_for_next_try(self, times):
        self.retries += 1
        logger.warning('Total retries "%d"', self.retries)
        self.wait_time(times)

    def wait_time(self, step):
        """Binary exponential backoff

        The server keeps session and renews it after a fixed amount of
        requests. This invalidates the previous requests, which may have been
        sent already, are thus refused by the server and must be retried.
        When there is a bunch of requests being retried, a random waiting time
        is used to avoid being sent at the same time again.
        """
        seconds = ((2. ** step) - 1.) / 2.
        gevent.sleep(seconds + random.random())


class Fetcher(object):
    """Fetching of xml documents from contrataciondelestado.es

    1. Fetch main page, set session cookie and scrap list page link
    2. Fetch list page and scrap details, page number and next page link
        0. Skip page if previous to start_page
        1. Fetch detail page and scrap the xml link
        2. Fetch xml link page and resolve the <meta http-equiv="refresh">
        3. Fetch xml link to the actual data and store it
    """

    host = "https://contrataciondelestado.es"
    main_url = urljoin(host, "/wps/portal/plataforma")

    def __init__(self, store, page=None, workers=None,
                 async=None, max_retries=None):
        self.store = store
        self.async = async
        self.sender = Sender(3 if max_retries is None else max_retries)
        self.start_page = page if page is not None else 1
        workers = workers if workers is not None else 5
        self.pool = self.get_pool_of_workers(workers)

    def get_pool_of_workers(self, workers):
        logger.info('Starting %d workers', workers)
        return Pool(workers)

    def run(self):
        next = self.fetch_main_page()

        while next:
            next = self.fetch_page(next)

    def fetch_main_page(self):
        """Load main url, obtain session cookie and url for 1 page

        :returns: Prepared request for page 1
        """
        d = self.fetch(self.request(self.main_url))

        url = self.get_link_to_first_page(d)

        return self.request(self.uri(url))

    def get_link_to_first_page(self, document):
        return document('#tabla_liciResueltas + div a').attr('href')

    def fetch_page(self, request):
        """Load all data in a result page

        :param request: Prepared request for the nth page of results.
        :returns: Prepared request for page n + 1 if any
        """
        details, page, next = self.fetch_list_page(request)
        logger.info("Page {}".format(page))

        if details and self.should_get_page_details(page):
            self.fetch_all_data_documents_from_details(details)

        return next

    def should_get_page_details(self, page):
        return page >= self.start_page

    def fetch_all_data_documents_from_details(self, details):
        pool_map = self.pool.map_async if self.async else self.pool.map
        pool_map(self.fetch_data_document, details)

    def fetch_list_page(self, request):
        """Load and parse the list of links in a result page

        :param request: Prepared request for page of results.
        :returns: `(details, page, next)` where `details` is the list of
         results (links) in the page, `page` is the number of the current page,
         and `next` is a prepared request for that page.
        """
        d = self.fetch(request)
        page = self.get_page_number(d)
        next = self.get_request_to_next_list_page(d)
        urls = self.get_links_to_detail_page(d)
        details = self.get_requests_to_detail_page(urls)
        logger.debug('Page %d contains %d details: %s', page, len(urls), urls)
        return details, page, next

    def get_requests_to_detail_page(self, urls):
        return [self.request(self.uri(url)) for url in urls]

    def get_links_to_detail_page(self, document):
        links = document('.tdidExpedienteWidth a')
        return [link.get('href') for link in links if link is not None]

    def get_page_number(self, document):
        return int(document('[id*="textNumPag"]').text())

    def get_request_to_next_list_page(self, document):
        with ignore(Exception):
            action, data = submit(document('input[id*="siguienteLink"]'))
            return self.request(self.uri(action), data) if action else None

    def fetch_data_document(self, request):
        """Fetch an specific document

        # Link in results page
        # goes to detail page
        # Link in detail page
        # goes to data page page which
        # is a redirection page which
        # goes to data document which
        # is finally stored

        :param request: Prepared request for detail page.
        :returns: Prepared request from the result list page.
        """
        with ignore(Exception):
            detail = self.execute(self.fetch_detail_page, request)
            if detail is not None:
                data = self.execute(self.fetch_data_page, detail)
                if data is not None:
                    self.execute(self.fetch_data, data)
                else:
                    logger.error('Could not fetch data page: %s', detail.url)
            else:
                logger.error('Could not fetch detail page: %s', request.url)

    def fetch_detail_page(self, request):
        """Fetch detail page and link for data document

        :param request: Prepared request for detail page.
        :returns: Prepared request for redirect page if any.
        """
        d = self.fetch(request)

        url = self.get_most_recent_xml_link_from_detail_page(d)

        if url is not None:
            return self.request(url)

    def get_most_recent_xml_link_from_detail_page(self, document):
        """Get the most recent xml document from the detail

        Xml documents in detail page are sorted by date.
        """
        return document('.documentosPub:last a:contains("Xml")').attr('href')

    def fetch_data_page(self, request):
        """Fetch redirect page which leds to a document.

        :param request: Prepared request for data page.
        :returns: Prepared request for the data document file.
        """
        d = self.fetch(request)

        url = self.get_html_meta_redirection_url(d)

        return self.request(self.uri(url))

    html_meta_parser = re.compile(".*;url='([^']+)'")
    """Parses url in `<meta http-equiv="refresh" content="0;url='/wps/..'">`"""

    def get_html_meta_redirection_url(self, document):
        meta = document('meta[http-equiv="refresh"]')
        content = self.html_meta_parser.match(meta.attr('content'))
        url = content.group(1)
        return url

    def fetch_data(self, request):
        """Fetch a document file and store it if is new.

        :param request: Prepared request for the data document.
        :returns: True if stored, False if already there.
        """
        if request.url in self.store:
            logger.warning('Already stored ' + request.url)
            return False

        response = self.send(request)
        self.store.put(response.url, response.text)
        logger.info('Stored ' + response.url)
        return True

    def request(self, url, data=None):
        return self.sender.request(url, data)

    def fetch(self, request):
        return self.sender.fetch(request)

    def uri(self, url):
        return urljoin(self.host, url)

    def send(self, request):
        return self.sender.send(request)

    def execute(self, function, request):
        return self.sender.execute(function, request)


def fetch_documents(store_path, page, workers, async, max_retries):
    store = Store(store_path)
    fetcher = Fetcher(store=store, page=page, workers=workers,
                      async=async, max_retries=max_retries)
    fetcher.run()
