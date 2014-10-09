# -*- coding: utf-8 -*-

from expects import *

from contratacion.mappers import paginate, pagination_metadata


with description('pagination_metadata'):
    with context('when given a negative page number'):
        with it('should default to 1'):
            result, meta = paginate(self.collection, page=-1, per_page=self.per_page)

            expect(result).to.be.equal(self.collection)
            expect(meta).to.be.equal(dict(last=1))

    with context('when given page 2 of 1'):
        with it('should return an empty result'):
            result, meta = paginate(self.collection, page=2, per_page=self.per_page)

            expect(result).to.be.empty
            expect(meta).to.be.equal(dict(last=1))

    with context('when given page 1 of 2'):
        with it('should return the first page'):
            result, meta = paginate(self.collection, page=1, per_page=self.length / 2)

            expect(result).to.be.equal(range(self.length / 2))
            expect(meta).to.be.equal(dict(last=2, next=2))

    with context('when given page 2 of 2'):
        with it('should return the second page'):
            result, meta = paginate(self.collection, page=2, per_page=self.length / 2)

            expect(result).to.be.equal(range(self.length / 2, self.length))
            expect(meta).to.be.equal(dict(last=2, prev=1))

    with before.all:
        self.length = 10
        self.per_page = 10
        self.collection = range(self.length)


with description('pagination_metadata'):
    with context('when given an empty collection'):
        with it('should return last is 1'):
            meta = pagination_metadata(**self.counters_0_of_0)

            expect(meta).to.be.equal(dict(last=1))

    with context('when given page 1 of 1'):
        with it('should return last is 1 '):
            meta = pagination_metadata(**self.counters_1_of_1)

            expect(meta).to.be.equal(dict(last=1))

    with context('when given page 1 of 2'):
        with it('should return last is 2 and next is 2'):
            meta = pagination_metadata(**self.counters_1_of_2)

            expect(meta).to.be.equal(dict(last=2, next=2))

    with context('when given page 2 of 2'):
        with it('should return last is 2 and prev is 1'):
            meta = pagination_metadata(**self.counters_2_of_2)

            expect(meta).to.be.equal(dict(last=2, prev=1))

    with context('when given page 2 of 3'):
        with it('should return last is 3 and prev is 1 and next is 3'):
            meta = pagination_metadata(**self.counters_2_of_3)

            expect(meta).to.be.equal(dict(prev=1, next=3, last=3))

    with context('when given page 5 of 10'):
        with it('should return last is 10 and prev is 4 and next is 6'):
            meta = pagination_metadata(**self.counters_5_of_10)

            expect(meta).to.be.equal(dict(prev=4, next=6, last=10))

    with context('when given page 5 of 10 at 1 per page'):
        with it('should return last is 50 and prev is 4 and next is 6'):
            meta = pagination_metadata(**self.counters_5_of_10_at_1)

            expect(meta).to.be.equal(dict(prev=4, next=6, last=50))

    with before.all:
        self.counters_0_of_0 = dict(offset=0, limit=0, total=0)
        self.counters_1_of_1 = dict(offset=0, limit=5, total=5)
        self.counters_1_of_2 = dict(offset=0, limit=5, total=10)
        self.counters_2_of_2 = dict(offset=5, limit=5, total=10)
        self.counters_2_of_3 = dict(offset=5, limit=5, total=15)
        self.counters_5_of_10 = dict(offset=20, limit=5, total=50)
        self.counters_5_of_10_at_1 = dict(offset=4, limit=1, total=50)
