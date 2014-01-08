# -*- coding: utf-8 -*-

import urllib

from mock import Mock, MagicMock
from expects import expect
from mamba import describe, context, before

from pyquery import PyQuery

from contratacion.fetcher import Fetcher

from spec.fixtures import (MAIN_PAGE, FIRST_PAGE_URL, FIRST_PAGE, DETAIL_URLS,
                           FIRST_PAGE_ACTION, FIRST_PAGE_FORM_DATA,
                           DETAIL_PAGE, DATA_PAGE_URL, DATA_PAGE, DOCUMENT_URL,
                           CODICE_21_DOCUMENT, LAST_PAGE, LAST_DETAIL_URLS)


with describe(Fetcher) as _:
    def it_should_have_a_start_page_property_default_to_1():
        expect(_get_fetcher()).to.have.property('start_page', 1)

    with context('should_get_page_details'):
        def it_should_say_no_if_for_pages_previous_to_start_page():
            fetcher = _get_fetcher(page=5)

            expect(fetcher.should_get_page_details(1)).to.be.false

        def it_should_say_yes_if_for_start_page():
            fetcher = _get_fetcher(page=5)

            expect(fetcher.should_get_page_details(5)).to.be.true

        def it_should_say_yes_for_pages_posterior_to_start_page():
            fetcher = _get_fetcher(page=5)

            expect(fetcher.should_get_page_details(6)).to.be.true

    with context('get_link_to_first_page'):
        def it_should_return_a_url_from_given_document():
            document = _.documents['main_page']

            url = _.fetcher.get_link_to_first_page(document)

            expect(url).to.be.equal(FIRST_PAGE_URL)

    with context('get_requests_to_detail_page'):
        def it_should_return_list_of_prepared_requests_for_given_urls():
            urls = ['http://foo.com/', 'http://bar.com/']

            requests = _.fetcher.get_requests_to_detail_page(urls)

            expect([r.url for r in requests]).to.be.equal(urls)

    with context('get_links_to_detail_page'):
        def it_should_return_a_list_of_urls_from_given_document():
            document = _.documents['first_page']

            urls = _.fetcher.get_links_to_detail_page(document)

            expect(urls).to.be.equal(DETAIL_URLS)

        def it_should_return_a_list_of_urls_for_last_page_document():
            document = _.documents['last_page']

            urls = _.fetcher.get_links_to_detail_page(document)

            expect(urls).to.be.equal(LAST_DETAIL_URLS)

    with context('get_page_number'):
        def it_should_return_current_page_number():
            document = _.documents['first_page']

            page = _.fetcher.get_page_number(document)

            expect(page).to.be.equal(1)

    with context('get_request_to_next_list_page'):
        def it_should_return_request_for_the_next_page():
            document = _.documents['first_page']

            request = _.fetcher.get_request_to_next_list_page(document)

            expect(request).to.have.property('path_url', FIRST_PAGE_ACTION)
            expect(request).to.have.property('body', urllib.urlencode(FIRST_PAGE_FORM_DATA))

        def it_should_return_none_at_the_last_page():
            document = _.documents['last_page']

            request = _.fetcher.get_request_to_next_list_page(document)

            expect(request).to.be.none

    with context('get_most_recent_xml_link_from_detail_page'):
        def it_should_return_a_url_from_the_given_document_():
            document = _.documents['detail_page']

            url = _.fetcher.get_most_recent_xml_link_from_detail_page(document)

            expect(url).to.be.equal(DATA_PAGE_URL)

    with context('get_html_meta_redirection'):
        def it_should_return_a_url_from_the_given_document__():
            document = _.documents['data_page']

            url = _.fetcher.get_html_meta_redirection_url(document)

            expect(url).to.be.equal(DOCUMENT_URL)

    with context('fetch_list_page'):
        def it_should_return_current_page_next_request_and_all_detail_requests():
            request = None
            fetcher = _get_fetcher()
            fetcher.fetch = Mock(return_value=_.documents['first_page'])

            requests, page, next = fetcher.fetch_list_page(request)

            expect(page).to.be.equal(1)
            expect(next.path_url).to.be.equal(FIRST_PAGE_ACTION)
            expect([r.path_url for r in requests]).to.be.equal(DETAIL_URLS)

        def it_should_return_current_page_none_for_next_request_and_all_detail_requests():
            request = None
            fetcher = _get_fetcher()
            fetcher.fetch = Mock(return_value=_.documents['last_page'])

            requests, page, next = fetcher.fetch_list_page(request)

            expect(next).to.be.none
            expect(page).to.be.equal(2726)
            expect([r.path_url for r in requests]).to.be.equal(LAST_DETAIL_URLS)

    with context('fetch_data'):
        def _requests_for_fetch_data(fetcher):
            document_url = fetcher.uri(DOCUMENT_URL)
            request = fetcher.request(document_url)
            response = _Response(url=document_url + '/', text=CODICE_21_DOCUMENT)
            return document_url, request, response

        def it_should_do_nothing_if_the_document_has_been_downloaded_before():
            fetcher = _get_fetcher()
            document_url, request, response = _requests_for_fetch_data(fetcher)
            fetcher.store.__contains__.return_value = True
            fetcher.send = Mock()

            fetcher.fetch_data(request)

            expect(fetcher.send.called).to.be.false
            expect(fetcher.store.__contains__.call_args[0]).to.have(request.url)

        def it_should_download_new_data_documents():
            fetcher = _get_fetcher()
            document_url, request, response = _requests_for_fetch_data(fetcher)
            fetcher.store.__contains__.return_value = False
            fetcher.send = Mock(return_value=response)

            fetcher.fetch_data(request)

            expect(fetcher.send.call_args[0]).to.have(request)

        def it_should_store_downloaded_data_documents_by_url():
            fetcher = _get_fetcher()
            document_url, request, response = _requests_for_fetch_data(fetcher)
            fetcher.store.__contains__.return_value = False
            fetcher.send = Mock(return_value=response)
            fetcher.store.put = Mock()

            fetcher.fetch_data(request)

            expect(fetcher.store.put.call_args[0]).to.have(response.url, response.text)

    with context('fetch_data_page'):
        def it_should_fetch_the_data_page():
            request, fetcher = None, _get_fetcher()
            fetcher.fetch = Mock()
            fetcher.get_html_meta_redirection_url = Mock(return_value=DOCUMENT_URL)

            fetcher.fetch_data_page(request)

            expect(fetcher.fetch.call_args[0]).to.have(request)

        def it_should_resolve_the_meta_redirection():
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_html_meta_redirection_url = Mock(return_value=DOCUMENT_URL)

            fetcher.fetch_data_page(request)

            expect(fetcher.get_html_meta_redirection_url.call_args[0]).to.have(document)

        def it_should_return_a_prepared_request_for_document_url():
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_html_meta_redirection_url = Mock(return_value=DOCUMENT_URL)

            request = fetcher.fetch_data_page(request)

            expect(request.path_url).to.be.equal(DOCUMENT_URL)

    with context('fetch_detail_page'):
        def it_should_fetch_the_detail_request():
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_most_recent_xml_link_from_detail_page = Mock(return_value=None)

            fetcher.fetch_detail_page(request)

            expect(fetcher.fetch.call_args[0]).to.have(request)

        def it_should_get_the_data_page_link():
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_most_recent_xml_link_from_detail_page = Mock(return_value=None)

            fetcher.fetch_detail_page(request)

            expect(fetcher.get_most_recent_xml_link_from_detail_page.call_args[0]).to.have(document)

        def it_should_return_a_prepared_request_for_document_url():
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_most_recent_xml_link_from_detail_page = Mock(return_value=DATA_PAGE_URL)

            next_request = fetcher.fetch_detail_page(request)

            expect(next_request.url).to.be.equal(DATA_PAGE_URL)

        def it_should_return_none_if_there_is_no_data_document_links():
            request, fetcher, document = None, _get_fetcher(), 'document'
            fetcher.fetch = Mock(return_value=document)
            fetcher.get_most_recent_xml_link_from_detail_page = Mock(return_value=None)

            next_request = fetcher.fetch_detail_page(request)

            expect(next_request).to.be.none

    with context('fetch_data_document'):
        def it_should_fetch_a_data_document_from_a_detail_page_request():
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

    def _get_store():
        return MagicMock()

    def _get_fetcher(**kwargs):
        return Fetcher(store=_get_store(), **kwargs)

    def _get_document(source):
        return PyQuery(source)

    @before.all
    def fixture():
        _.fetcher = _get_fetcher()
        _.documents = {
            'main_page': _get_document(MAIN_PAGE),
            'first_page': _get_document(FIRST_PAGE),
            'detail_page': _get_document(DETAIL_PAGE),
            'data_page': _get_document(DATA_PAGE),
            'last_page': _get_document(LAST_PAGE)
        }

    class _Response(object):
        def __init__(self, url, text):
            self.url = url
            self.text = text

    class _Request(object):
        def __init__(self, url):
            self.url = url
