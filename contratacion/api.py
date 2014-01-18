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

    def get(self, id):
        return self.mapper.get_or_404(id)


class ListResource(Resource):
    def get(self):
        return self.mapper.all()


class Licitation(Resource):
    model = models.Licitation


class LicitationList(ListResource):
    model = models.Licitation


class Contractor(Resource):
    model = models.Party

    @property
    def mapper(self):
        return mappers.ViewMapper(self.model.contractors(g.db))


class ContractorList(ListResource):
    model = models.Party

    @property
    def mapper(self):
        return mappers.ViewMapper(self.model.contractors(g.db))


class Contracted(Resource):
    model = models.Party

    @property
    def mapper(self):
        return mappers.ViewMapper(self.model.contracted(g.db))


class ContractedList(ListResource):
    model = models.Party

    @property
    def mapper(self):
        return mappers.ViewMapper(self.model.contracted(g.db))


class Party(Resource):
    model = models.Party


class Parties(ListResource):
    model = models.Party


api.add_resource(LicitationList, '/licitations')
api.add_resource(Licitation, '/licitations/<int:id>')

api.add_resource(ContractorList, '/contractors')
api.add_resource(Contractor, '/contractors/<int:id>')

api.add_resource(ContractedList, '/contracted')
api.add_resource(Contracted, '/contracted/<int:id>')

api.add_resource(Parties, '/parties')
api.add_resource(Party, '/parties/<int:id>')
