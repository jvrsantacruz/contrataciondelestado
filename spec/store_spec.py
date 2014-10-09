# -*- coding: utf-8 -*-

import os
import zlib
from functools import partial

from expects import *

from contratacion.store import Store


with description(Store):
    with context('clean method'):
        with it('should return a clean url'):
            url = self.store.clean('http://host')

            expect(url).to.be.equal('httphost')

    with context('compress method'):
        with it('should return compressed value'):
            compressed = zlib.compress(self.data.encode('utf-8'))

            expect(self.store.compress(self.data)).to.be.equal(compressed)

    with context('decompress method'):
        with it('should return decompressed value'):
            compressed = zlib.compress(self.data.encode('utf-8'))

            expect(self.store.decompress(compressed)).to.be.equal(self.data)

    with context('put method'):
        with it('should store given data'):
            self.store.put(self.url, self.data)

            expect(self.store.get(self.url)).to.be.equal(self.data)

        with it('should return the cleaned key'):
            key = self.store.put(self.url, self.data)

            expect(key).to.be.equal(self.clean_url)

    with context('get method'):
        with it('should get already stored data'):
            self.store.put(self.url, self.data)

            expect(self.store.get(self.url)).to.be.equal(self.data)

    with context('delete method'):
        with it('should remove already stored data'):
            self.store.put(self.url, self.data)
            self.store.delete(self.url)

            expect(partial(self.store.get, self.url)).to.raise_error(KeyError)

    with context('iteritems method'):
        with it('should be a key value iterable'):
            self.store.put(self.url, self.data)

            items = list(self.store.iteritems())

            expect(items).to.have((self.clean_url, self.data))

    with context('len operator'):
        with it('should return number of stored values'):
            number_of_elements = len(self.store.keys())

            expect(len(self.store)).to.be.equal(number_of_elements)

    with context('iteration'):
        with it('should give all available keys'):
            expect(list(self.store)).to.be.equal(self.store.keys())

    with context('contains operator'):
        with it('should return True for present keys'):
            self.store.put(self.url, self.data)

            expect(self.url in self.store).to.be.true

        with it('should return False for no present  keys'):
            expect('fake' in self.store).to.be.false

    with before.all:
        self.data = u'ñ'
        self.url = 'http://host'
        self.clean_url = 'httphost'
        self.tmp_file = '/tmp/test_store.sqlite'
        self.store = _get_store(self.tmp_file)

    with after.all:
        try:
            os.unlink(self.tmp_file)
        except OSError:
            pass


def _get_store(path):
    return Store(path)
