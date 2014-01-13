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
