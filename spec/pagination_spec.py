# -*- coding: utf-8 -*-

from expects import expect
from mamba import describe, context, before

from contratacion.mappers import paginate, pagination_metadata


with describe('pagination_metadata') as _:
    with context('when given a negative page number'):
        def it_should_default_to_1():
            result, meta = paginate(_.collection, page=-1, per_page=_.per_page)

            expect(result).to.be.equal(_.collection)
            expect(meta).to.be.equal(dict(last=1))

    with context('when given page 2 of 1'):
        def it_should_return_an_empty_result():
            result, meta = paginate(_.collection, page=2, per_page=_.per_page)

            expect(result).to.be.empty
            expect(meta).to.be.equal(dict(last=1))

    with context('when given page 1 of 2'):
        def it_should_return_the_first_page():
            result, meta = paginate(_.collection, page=1, per_page=_.length/2)

            expect(result).to.be.equal(range(_.length/2))
            expect(meta).to.be.equal(dict(last=2, next=2))

    with context('when given page 2 of 2'):
        def it_should_return_the_second_page():
            result, meta = paginate(_.collection, page=2, per_page=_.length/2)

            expect(result).to.be.equal(range(_.length/2, _.length))
            expect(meta).to.be.equal(dict(last=2, prev=1))

    @before.all
    def setup():
        _.length = 10
        _.per_page= 10
        _.collection = range(_.length)


with describe('pagination_metadata') as _:
    with context('when given an empty collection'):
        def it_should_return_last_is_1():
            meta = pagination_metadata(**_.counters_0_of_0)

            expect(meta).to.be.equal(dict(last=1))

    with context('when given page 1 of 1'):
        def it_should_return_last_is_1_():
            meta = pagination_metadata(**_.counters_1_of_1)

            expect(meta).to.be.equal(dict(last=1))

    with context('when given page 1 of 2'):
        def it_should_return_last_is_2_and_next_is_2():
            meta = pagination_metadata(**_.counters_1_of_2)

            expect(meta).to.be.equal(dict(last=2, next=2))

    with context('when given page 2 of 2'):
        def it_should_return_last_is_2_and_prev_is_1():
            meta = pagination_metadata(**_.counters_2_of_2)

            expect(meta).to.be.equal(dict(last=2, prev=1))

    with context('when given page 2 of 3'):
        def it_should_return_last_is_3_and_prev_is_1_and_next_is_3():
            meta = pagination_metadata(**_.counters_2_of_3)

            expect(meta).to.be.equal(dict(prev=1, next=3, last=3))

    with context('when given page 5 of 10'):
        def it_should_return_last_is_10_and_prev_is_4_and_next_is_6():
            meta = pagination_metadata(**_.counters_5_of_10)

            expect(meta).to.be.equal(dict(prev=4, next=6, last=10))

    with context('when given page 5 of 10 at 1 per page'):
        def it_should_return_last_is_50_and_prev_is_4_and_next_is_6():
            meta = pagination_metadata(**_.counters_5_of_10_at_1)

            expect(meta).to.be.equal(dict(prev=4, next=6, last=50))

    @before.all
    def setup_():
        _.counters_0_of_0 = dict(offset=0, limit=0, total=0)
        _.counters_1_of_1 = dict(offset=0, limit=5, total=5)
        _.counters_1_of_2 = dict(offset=0, limit=5, total=10)
        _.counters_2_of_2 = dict(offset=5, limit=5, total=10)
        _.counters_2_of_3 = dict(offset=5, limit=5, total=15)
        _.counters_5_of_10 = dict(offset=20, limit=5, total=50)
        _.counters_5_of_10_at_1 = dict(offset=4, limit=1, total=50)
