#!/usr/bin/env python
#-*- coding: utf-8 -*-

from gevent import monkey

monkey.patch_all()

import re
import logging
from itertools import chain
from urlparse import urljoin

import requests
from pyquery import PyQuery
from gevent.pool import Pool
import y_serial_v060 as y_serial

_LOGGING_FMT_ = '%(asctime)s %(levelname)-8s %(message)s'


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


class Fetcher(object):

    host = "https://contrataciondelestado.es"
    main_url = urljoin(host, "/wps/portal/plataforma")
    list_url = urljoin(host, '/wps/portal/!ut/p/b1/hc7LDoIwFATQLyIdKLR0SUppS1SIIkg3hoUxJDw2xu8XiS7Fu5vkTOYSR1rP5z7jVMSUkgtxU_fs792jn6dueGfHrhoslFZQIFUCtqjyo6w4ijRaQLsA_LgEaz9UhZSZCQC1pwgM17GiEii__Q3wZ78hbiURlWGd1yU7WQ1Yk6W7sx9BB-wDNl48mHm8kdENmbBe8gJ_U3kE/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=javax.servlet.include.path_info=QCPjspQCPLicitacionesResueltasView.jsp/231949228532/-/')

    def __init__(self, page=None):
        self.pool = Pool(10)
        self.session = requests.Session()
        self.store = y_serial.Main('tmp.slite')
        self.start_page = page if page is not None else 1

    def run(self):
        next = self.fetch_main_page()

        while next:
            next = self.fetch_page(next)

        self.pool.join()

    def fetch_main_page(self):
        d = self.fetch(self.request(self.main_url))

        url = d('#tabla_liciResueltas + div a').attr('href')

        return self.request(self.uri(url))

    def fetch_page(self, request):
        details, page, next = self.fetch_list_page(request)

        if details and page >= self.start_page:

        logging.info(next.url)
        return next

    def fetch_list_page(self, request):
        d = self.fetch(request)

        details = [self.request(self.uri(a.get('href')))
                   for a in d('.tdidExpedienteWidth a')
                   if a is not None]

        page = int(d('[id*="textNumPag"]').text())

        action, data = submit(d('input[id*="siguienteLink"]'))
        next = self.request(self.uri(action), data)

        return details, page, next

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

        if self.stored(url):
            logging.warning('Already stored ' + url)
            return

        response = self.send(self.request(url))

        self.save(url, response.text)
        #document = etree.iterparse(StringIO(response.text.encode('utf-8')))
        #for event, element in document:

    def stored(self, name):
        return self.store.select(name, 'raw')

    def save(self, name, data):
        self.store.insert(data, name, 'raw')
        logging.info('Stored ' + name)

    def request(self, url, data=None):
        method = 'GET' if data is None else 'POST'
        return requests.Request(
            method, url, data=data, cookies=self.session.cookies
        ).prepare()

    def fetch(self, request):
        logging.info("Sending " + str(request))
        response = self.send(request)
        return PyQuery(response.text)

    def uri(self, url):
        return urljoin(self.host, url)

    def send(self, request):
        response = self.session.send(request, verify=False)
        return response


def main():
    logging.basicConfig(level=logging.INFO, format=_LOGGING_FMT_)

    Fetcher().run()


if __name__ == "__main__":
    main()
