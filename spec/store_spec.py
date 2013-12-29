# -*- coding: utf-8 -*-

import os
import zlib
from functools import partial

from expects import expect
from mamba import describe, context, before, after

from contratacion.store import Store


with describe(Store) as _:
    with context('clean method'):
        def it_should_return_a_cleaned_url():
            url = _.store.clean('http://host')

            expect(url).to.be.equal('httphost')

    with context('compress method'):
        def it_should_return_compressed_value():
            compressed = zlib.compress(_.data.encode('utf-8'))

            expect(_.store.compress(_.data)).to.be.equal(compressed)

    with context('decompress method'):
        def it_should_return_decompressed_value():
            compressed = zlib.compress(_.data.encode('utf-8'))

            expect(_.store.decompress(compressed)).to.be.equal(_.data)

    with context('put method'):
        def it_should_store_given_data():
            _.store.put(_.url, _.data)

            expect(_.store.get(_.url)).to.be.equal(_.data)

        def it_should_return_the_cleaned_key():
            key = _.store.put(_.url, _.data)

            expect(key).to.be.equal(_.clean_url)

    with context('get method'):
        def it_should_get_already_stored_data():
            _.store.put(_.url, _.data)

            expect(_.store.get(_.url)).to.be.equal(_.data)

    with context('delete method'):
        def it_should_remove_already_stored_data():
            _.store.put(_.url, _.data)
            _.store.delete(_.url)

            expect(partial(_.store.get, _.url)).to.raise_error(KeyError)

    with context('iteritems method'):
        def it_should_be_a_key_value_iterable():
            _.store.put(_.url, _.data)

            items = list(_.store.iteritems())

            expect(items).to.have((_.clean_url, _.data))

    with context('len operator'):
        def it_should_return_number_of_stored_values():
            number_of_elements = len(_.store.keys())

            expect(len(_.store)).to.be.equal(number_of_elements)

    with context('iteration'):
        def it_should_give_all_available_keys():
            expect(list(_.store)).to.be.equal(_.store.keys())

    with context('contains operator'):
        def it_should_return_True_for_present_keys():
            _.store.put(_.url, _.data)

            expect(_.url in _.store).to.be.true

        def it_should_return_True_for_no_present__keys():
            expect('fake' in _.store).to.be.false

    def _get_store(path):
        return Store(path)

    @before.all
    def fixture():
        _.data = u'ñ'
        _.url = 'http://host'
        _.clean_url = 'httphost'
        _.tmp_file = '/tmp/test_store.sqlite'
        _.store = _get_store(_.tmp_file)

    @after.all
    def clean_fixture():
        try:
            os.unlink(_.tmp_file)
        except OSError:
            pass
