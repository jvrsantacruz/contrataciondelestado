#!/usr/bin/env python
#-*- coding: utf-8 -*-

from gevent import monkey

monkey.patch_all()

import re
import time
import logging
from itertools import chain
from urlparse import urljoin
from argparse import ArgumentParser

import requests
from pyquery import PyQuery
from gevent.pool import Pool

from .store import Store

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

    def __init__(self):
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
        return PyQuery(response.text)

    def send(self, request):
        """Send the request and get the response

        :param request: Prepared request ready to send.
        :rtype: :class:`requests.Response` object.
        """
        logger.debug("%s %s", request.method, request.url)
        response = self.session.send(request, verify=False)
        self.profiler.request_sent()
        return response


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

    def __init__(self, store, page=None):
        self.store = store
        self.pool = Pool(10)
        self.sender = Sender()
        self.start_page = page if page is not None else 1

    def run(self):
        next = self.fetch_main_page()

        while next:
            next = self.fetch_page(next)

    def fetch_main_page(self):
        """Load main url, obtain session cookie and url for 1 page

        :returns: Prepared request for page 1
        """
        d = self.fetch(self.request(self.main_url))

        url = d('#tabla_liciResueltas + div a').attr('href')

        return self.request(self.uri(url))

    def fetch_page(self, request):
        """Load all data in a result page

        :param request: Prepared request for the nth page of results.
        :returns: Prepared request for page n + 1 if any
        """
        details, page, next = self.fetch_list_page(request)

        if page >= self.start_page:
            if details:
                self.pool.map(self.fetch_data_document, details)

        logger.info("Page {}".format(page))
        return next

    def fetch_list_page(self, request):
        """Load and parse the list of links in a result page

        :param request: Prepared request for page of results.
        :returns: `(details, page, next)` where `details` is the list of
         results (links) in the page, `page` is the number of the current page,
         and next is a prepared request for that page.
        """
        d = self.fetch(request)

        details = [self.request(self.uri(a.get('href')))
                   for a in d('.tdidExpedienteWidth a')
                   if a is not None]

        page = int(d('[id*="textNumPag"]').text())

        action, data = submit(d('input[id*="siguienteLink"]'))
        next = self.request(self.uri(action), data) if data else None

        return details, page, next

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
        detail = self.fetch_detail_page(request)
        if detail:
            data = self.fetch_data_page(detail)
            if data:
                self.fetch_data(data)

    def fetch_detail_page(self, request):
        """Fetch detail page and link for data document

        :param request: Prepared request for detail page.
        :returns: Prepared request for redirect page if any.
        """
        d = self.fetch(request)

        url = d('.documentosPub:last a:contains("Xml")').attr('href')

        if url is not None:
            return self.request(url)

    def fetch_data_page(self, request, parser=re.compile(".*;url='([^']+)'")):
        """Fetch redirect page which leds to a document.

        :param request: Prepared request for data page.
        :param parser: Regular expression for an html meta tag.
        :returns: Prepared request for the data document file.
        """
        d = self.fetch(request)

        meta = d('meta[http-equiv="refresh"]')
        content = parser.match(meta.attr('content'))
        url = self.uri(content.group(1))

        return self.request(url)

    def fetch_data(self, request):
        """Fetch a document file and store it if is new.

        :param request: Prepared request for the data document.
        """
        if request.url in self.store:
            logger.warning('Already stored ' + request.url)
            return

        response = self.send(request)
        self.store.put(response.url, response.text)
        logger.info('Stored ' + response.url)

    def request(self, url, data=None):
        return self.sender.request(url, data)

    def fetch(self, request):
        return self.sender.fetch(request)

    def uri(self, url):
        return urljoin(self.host, url)

    def send(self, request):
        return self.sender.send(request)


def fetch_documents(store_path, page):
    store = Store(store_path)
    fetcher = Fetcher(store=store, page=page)
    fetcher.run()
