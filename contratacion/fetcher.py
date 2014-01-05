#!/usr/bin/env python
#-*- coding: utf-8 -*-

from gevent import monkey

monkey.patch_all()

import re
import logging
from itertools import chain
from urlparse import urljoin
from argparse import ArgumentParser

import requests
from pyquery import PyQuery
from gevent.pool import Pool

from store import Store

_LOGGING_FMT_ = '%(asctime)s %(levelname)-8s %(message)s'

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


class Sender(object):
    """Manages request creation and sending"""

    def __init__(self):
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
        d = self.fetch(self.request(self.main_url))

        url = d('#tabla_liciResueltas + div a').attr('href')

        return self.request(self.uri(url))

    def fetch_page(self, request):
        details, page, next = self.fetch_list_page(request)

        if page >= self.start_page:
            if details:
                self.pool.map(self.fetch_data_document, details)

        logger.info("Page {}".format(page))
        return next

    def fetch_list_page(self, request):
        d = self.fetch(request)

        details = [self.request(self.uri(a.get('href')))
                   for a in d('.tdidExpedienteWidth a')
                   if a is not None]

        page = int(d('[id*="textNumPag"]').text())

        action, data = submit(d('input[id*="siguienteLink"]'))
        next = self.request(self.uri(action), data) if data else None

        return details, page, next

    def fetch_data_document(self, request):
        detail = self.fetch_detail_page(request)
        if detail:
            data = self.fetch_data_page(detail)
            if data:
                self.fetch_data(data)

    def fetch_detail_page(self, request):
        d = self.fetch(request)

        url = d('.documentosPub:last a:contains("Xml")').attr('href')

        if url is not None:
            return self.request(url)

    def fetch_data_page(self, request, parser=re.compile(".*;url='([^']+)'")):
        d = self.fetch(request)

        meta = d('meta[http-equiv="refresh"]')
        content = parser.match(meta.attr('content'))
        url = self.uri(content.group(1))

        return self.request(url)

    def fetch_data(self, request):
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
