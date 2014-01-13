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


class Licitations(Resource):
    model = models.Licitation

    def get(self):
        return dict(licitations=self.mapper.all())


class Licitation(Resource):
    model = models.Licitation

    def get(self, id):
        return dict(licitation=self.mapper.get_or_404(id))


class Contractors(Resource):
    model = models.Party

    @property
    def mapper(self):
        return mappers.ViewMapper(self.model.contractors(g.db))

    def get(self):
        return dict(contractors=self.mapper.all())


class Contractor(Resource):
    model = models.Party

    @property
    def mapper(self):
        return mappers.ViewMapper(self.model.contractors(g.db))

    def get(self, id):
        return dict(contractor=self.mapper.get_or_404(id))


class Contracteds(Resource):
    model = models.Party

    @property
    def mapper(self):
        return mappers.ViewMapper(self.model.contracted(g.db))

    def get(self):
        return dict(contracted=self.mapper.all())


class Contracted(Resource):
    model = models.Party

    @property
    def mapper(self):
        return mappers.ViewMapper(self.model.contracted(g.db))

    def get(self, id):
        return dict(contracted=self.mapper.get_or_404(id))


class Parties(Resource):
    model = models.Party

    def get(self):
        return dict(parties=self.mapper.all())


class Party(Resource):
    model = models.Party

    def get(self, id):
        return dict(party=self.mapper.get_or_404(id))


api.add_resource(Licitations, '/licitations')
api.add_resource(Licitation, '/licitations/<int:id>')
api.add_resource(Contractors, '/contractors')
api.add_resource(Contractor, '/contractors/<int:id>')
api.add_resource(Contracteds, '/contracted')
api.add_resource(Contracted, '/contracted/<int:id>')
api.add_resource(Parties, '/parties')
api.add_resource(Party, '/parties/<int:id>')
