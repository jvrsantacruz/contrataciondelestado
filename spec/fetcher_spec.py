# -*- coding: utf-8 -*-

import urllib

from expects import expect
from mamba import describe, context, before

from pyquery import PyQuery

from contratacion.fetcher import Fetcher, Sender

from spec.fixtures import (MAIN_PAGE, FIRST_PAGE_URL, FIRST_PAGE, DETAIL_URLS,
                           FIRST_PAGE_ACTION, FIRST_PAGE_FORM_DATA,
                           DETAIL_PAGE, DATA_PAGE_URL, DATA_PAGE, DOCUMENT_URL)


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

    def _get_fetcher(**kwargs):
        return Fetcher(store=None, **kwargs)

    def _get_document(source):
        return PyQuery(source)

    @before.all
    def fixture():
        _.fetcher = _get_fetcher()
        _.documents = {
            'main_page': _get_document(MAIN_PAGE),
            'first_page': _get_document(FIRST_PAGE),
            'detail_page': _get_document(DETAIL_PAGE),
            'data_page': _get_document(DATA_PAGE)
        }
