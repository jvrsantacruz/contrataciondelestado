# -*- coding: utf-8 -*-
"""Operations with data models

Wraps models to offer a common iterface for creating/updating/deleting.
"""

from flask.ext.restful import abort


class Mapper(object):
    def __init__(self, query):
        self.query = query

    @classmethod
    def get_mapper(cls, model, session):
        return  cls(session.query(model))

    def all(self):
        return map(self.serialize, self.query[:10])

    def all_paginated(self, page=None, per_page=None):
        collection, meta = paginate(self.query, page=page, per_page=per_page)
        return map(self.serialize, collection), meta

    def get(self, id):
        return self.serialize(self.query.get(id))

    def get_or_404(self, id):
        return self.get(id) or abort(404)

    def serialize(self, obj):
        if obj is not None:
            return obj.to_dict()


class ViewMapper(Mapper):
    def get(self, id):
        return self.serialize(self.query.filter_by(id=id).first())


def paginate(collection, page=None, per_page=None):
    """Slice a page of the given collection

    Pagination starts at `1`.

    `metadata` consist in a dictionary that contains
    the `last` page number, and may also have the values for
    `next` and `prev` pages if apply.

    :param collection: list-like object
    :param page: number of the page (default: 10)
    :param per_page: number of results per page (default: 10)
    :returns: (elementos, metadata)
    """
    page = 1 if page is None else page
    per_page = 10 if per_page is None else per_page

    # query data
    limit = max(per_page, 1)
    offset = (max(page, 1) - 1) * limit

    # slice the query
    paginated = collection[offset:offset + limit]

    # real data
    total = length(collection)
    total_query = length(paginated)     # number of items in response

    metadata = pagination_metadata(offset, total_query, total)

    return paginated, metadata


def pagination_metadata(offset, limit, total):
    """Return a metadata dict from the query counters

    :param offset: offset to the last element in the page
    :param limit: number of elements in the page
    :param total: total elements in the collection
    :returns: `dict` with optional `last`, `next` and `prev` values.
    """
    total_pages = nth_page(limit, total)
    current_page = nth_page(limit, offset + limit)

    meta = {'last': total_pages}

    if current_page < total_pages:
        meta['next'] = current_page + 1

    if current_page > 1:
        meta['prev'] = current_page - 1

    return meta


def nth_page(per_page, offset):
    """Returns the page number of the nth item"""
    return offset / per_page + int(offset % per_page > 0) if per_page else 1


def length(query_or_collection):
    try:
        return len(query_or_collection)
    except TypeError:
        return query_or_collection.count()
