# -*- coding: utf-8 -*-

import urllib

from expects import *
from mock import Mock, MagicMock

from pyquery import PyQuery

from contratacion.fetcher import Fetcher

from spec.fixtures import (MAIN_PAGE, FIRST_PAGE_URL, FIRST_PAGE, DETAIL_URLS,
                           FIRST_PAGE_ACTION, FIRST_PAGE_FORM_DATA,
                           DETAIL_PAGE, DATA_PAGE_URL, DATA_PAGE, DOCUMENT_URL,
                           CODICE_21_DOCUMENT, LAST_PAGE, LAST_DETAIL_URLS)


with description(Fetcher):
    with it('should have a start page property default to 1'):
        expect(_get_fetcher()).to.have.property('start_page', 1)

    with context('should_get_page_details'):
        with it('should say no for pages previous to start page'):
            fetcher = _get_fetcher(page=5)

            expect(fetcher.should_get_page_details(1)).to.be.false

        with it('should say yes for start page'):
            fetcher = _get_fetcher(page=5)

            expect(fetcher.should_get_page_details(5)).to.be.true

        with it('should say yes for pages posterior to start page'):
            fetcher = _get_fetcher(page=5)

            expect(fetcher.should_get_page_details(6)).to.be.true

    with context('get_link_to_first_page'):
        with it('should return a url from given document'):
            document = self.documents['main_page']

            url = self.fetcher.get_link_to_first_page(document)

            expect(url).to.be.equal(FIRST_PAGE_URL)

    with context('get_requests_to_detail_page'):
        with it('should return list of prepared requests for given urls'):
            urls = ['http://foo.com/', 'http://bar.com/']

            requests = self.fetcher.get_requests_to_detail_page(urls)

            expect([r.url for r in requests]).to.be.equal(urls)

    with context('get_links_to_detail_page'):
        with it('should return a list of urls from given document'):
            document = self.documents['first_page']

            urls = self.fetcher.get_links_to_detail_page(document)

            expect(urls).to.be.equal(DETAIL_URLS)

        with it('should return a list of urls for last page document'):
            document = self.documents['last_page']

            urls = self.fetcher.get_links_to_detail_page(document)

            expect(urls).to.be.equal(LAST_DETAIL_URLS)

    with context('get_page_number'):
        with it('should return current page number'):
            document = self.documents['first_page']

            page = self.fetcher.get_page_number(document)

            expect(page).to.be.equal(1)

    with context('get_request_to_next_list_page'):
        with it('should return request for the next page'):
            document = self.documents['first_page']

            request = self.fetcher.get_request_to_next_list_page(document)

            expect(request).to.have.property('path_url', FIRST_PAGE_ACTION)
            expect(request).to.have.property('body', urllib.urlencode(FIRST_PAGE_FORM_DATA))

        with it('should return none at the last page'):
            document = self.documents['last_page']

            request = self.fetcher.get_request_to_next_list_page(document)

            expect(request).to.be.none

    with context('get_most_recent_xml_link_from_detail_page'):
        with it('should return a url from the given document '):
            document = self.documents['detail_page']

            url = self.fetcher.get_most_recent_xml_link_from_detail_page(document)

            expect(url).to.be.equal(DATA_PAGE_URL)

    with context('get_html_meta_redirection'):
        with it('should return a url from the given document  '):
            document = self.documents['data_page']

            url = self.fetcher.get_html_meta_redirection_url(document)

            expect(url).to.be.equal(DOCUMENT_URL)

    with context('fetch_list_page'):
        with it('should return current page next request and all detail requests'):
            request = None
            fetcher = _get_fetcher()
            fetcher.fetch = Mock(return_value=self.documents['first_page'])

            requests, page, next = fetcher.fetch_list_page(request)

            expect(page).to.be.equal(1)
            expect(next.path_url).to.be.equal(FIRST_PAGE_ACTION)
            expect([r.path_url for r in requests]).to.be.equal(DETAIL_URLS)

        with it('should return current page none for next request and all detail requests'):
            request = None
            fetcher = _get_fetcher()
            fetcher.fetch = Mock(return_value=self.documents['last_page'])

            requests, page, next = fetcher.fetch_list_page(request)

            expect(next).to.be.none
            expect(page).to.be.equal(2726)
            expect([r.path_url for r in requests]).to.be.equal(LAST_DETAIL_URLS)

    with context('fetch_data'):
        with it('should do nothing if the document has been downloaded before'):
            fetcher = _get_fetcher()
            document_url, request, response = _requests_for_fetch_data(fetcher)
            fetcher.store.__contains__.return_value = True
            fetcher.send = Mock()

            fetcher.fetch_data(request)

            expect(fetcher.send.called).to.be.false
            expect(fetcher.store.__contains__.call_args[0]).to.have(request.url)

        with it('should download new data documents'):
            fetcher = _get_fetcher()
            document_url, request, response = _requests_for_fetch_data(fetcher)
            fetcher.store.__contains__.return_value = False
            fetcher.send = Mock(return_value=response)

            fetcher.fetch_data(request)

            expect(fetcher.send.call_args[0]).to.have(request)

        with it('should store downloaded data documents by url'):
            fetcher = _get_fetcher()
            document_url, request, response = _requests_for_fetch_data(fetcher)
            fetcher.store.__contains__.return_value = False
            fetcher.send = Mock(return_value=response)
            fetcher.store.put = Mock()

            fetcher.fetch_data(request)

            expect(fetcher.store.put.call_args[0]).to.have(response.url, response.text)

    with context('fetch_data_page'):
        with it('should fetch the data page'):
            request, fetcher = None, _get_fetcher()
            fetcher.fetch = Mock()
            fetcher.get_html_meta_redirection_url = Mock(return_value=DOCUMENT_URL)

            fetcher.fetch_data_page(request)

            expect(fetcher.fetch.call_args[0]).to.have(request)

        with it('should resolve the meta redirection'):
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_html_meta_redirection_url = Mock(return_value=DOCUMENT_URL)

            fetcher.fetch_data_page(request)

            expect(fetcher.get_html_meta_redirection_url.call_args[0]).to.have(document)

        with it('should return a prepared request for document url'):
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_html_meta_redirection_url = Mock(return_value=DOCUMENT_URL)

            request = fetcher.fetch_data_page(request)

            expect(request.path_url).to.be.equal(DOCUMENT_URL)

    with context('fetch_detail_page'):
        with it('should fetch the detail request'):
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_most_recent_xml_link_from_detail_page = Mock(return_value=None)

            fetcher.fetch_detail_page(request)

            expect(fetcher.fetch.call_args[0]).to.have(request)

        with it('should get the data page link'):
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_most_recent_xml_link_from_detail_page = Mock(return_value=None)

            fetcher.fetch_detail_page(request)

            expect(fetcher.get_most_recent_xml_link_from_detail_page.call_args[0]).to.have(document)

        with it('should return a prepared request for document url '):
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_most_recent_xml_link_from_detail_page = Mock(return_value=DATA_PAGE_URL)

            next_request = fetcher.fetch_detail_page(request)

            expect(next_request.url).to.be.equal(DATA_PAGE_URL)

        with it('should return none if there is no data document links'):
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_most_recent_xml_link_from_detail_page = Mock(return_value=None)

            next_request = fetcher.fetch_detail_page(request)

            expect(next_request).to.be.none

    with context('fetch_data_document'):
        with it('should fetch a data document from a detail page request'):
            detail_page_request, data_page_request, data_document_request =\
                _Request(1), _Request(2), _Request(3)
            fetcher = _get_fetcher(max_retries=0)
            fetcher.fetch_detail_page = Mock(return_value=data_page_request)
            fetcher.fetch_data_page = Mock(return_value=data_document_request)
            fetcher.fetch_data = Mock(return_value=None)

            fetcher.fetch_data_document(detail_page_request)

            fetcher.fetch_detail_page.assert_called_with(detail_page_request)
            fetcher.fetch_data_page.assert_called_with(data_page_request)
            fetcher.fetch_data.assert_called_with(data_document_request)

    with before.all:
        self.fetcher = _get_fetcher()
        self.documents = {
            'main_page': _get_document(MAIN_PAGE),
            'first_page': _get_document(FIRST_PAGE),
            'detail_page': _get_document(DETAIL_PAGE),
            'data_page': _get_document(DATA_PAGE),
            'last_page': _get_document(LAST_PAGE)
        }


def _get_store():
    return MagicMock()


def _get_fetcher(**kwargs):
    return Fetcher(store=_get_store(), **kwargs)


def _get_document(source):
    return PyQuery(source)


class _Response(object):
    def __init__(self, url, text):
        self.url = url
        self.text = text


class _Request(object):
    def __init__(self, url):
        self.url = url


def _requests_for_fetch_data(fetcher):
    document_url = fetcher.uri(DOCUMENT_URL)
    request = fetcher.request(document_url)
    response = _Response(url=document_url + '/', text=CODICE_21_DOCUMENT)
    return document_url, request, response
