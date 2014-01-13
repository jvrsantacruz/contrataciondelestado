# -*- coding: utf-8 -*-

from flask import Blueprint, g
from flask.ext import restful

import models
import mappers


api_blueprint = Blueprint('api', 'contratacion')
api = restful.Api(api_blueprint)


class Resource(restful.Resource):
    @property
    def mapper(self):
        return mappers.Mapper.get_mapper(self.model, g.db)

    def get(self, id=None):
        return self.mapper.all() if id is None else self.mapper.get_or_404(id)


class Licitations(Resource):
    model = models.Licitation


class Contractors(Resource):
    model = models.Party

    @property
    def mapper(self):
        return mappers.ViewMapper(self.model.contractors(g.db))


class Contracteds(Resource):
    model = models.Party

    @property
    def mapper(self):
        return mappers.ViewMapper(self.model.contracted(g.db))


class Parties(Resource):
    model = models.Party


api.add_resource(Licitations, '/licitations', '/licitations/<int:id>')
api.add_resource(Contractors, '/contractors', '/contractors/<int:id>')
api.add_resource(Contracteds, '/contracted', '/contracted/<int:id>')
api.add_resource(Parties, '/parties', '/parties/<int:id>')
