# -*- coding: utf-8 -*-

from flask import Blueprint, g
from flask.ext import restful

import models


api_blueprint = Blueprint('api', 'contratacion')
api = restful.Api(api_blueprint)


class Licitations(restful.Resource):
    def get(self):
        query = g.db.query(models.Licitation)[:20]
        licitations = [l.to_dict() for l in query]
        return dict(licitations=licitations)


class Licitation(restful.Resource):
    def get(self, id):
        licitation = g.db.query(models.Licitation).get(id)
        if licitation is None:
            restful.abort(404)
        return dict(licitation=licitation.to_dict())


class Contractors(restful.Resource):
    def get(self):
        query = models.Party.contractors(g.db)[:20]
        contractors = [l.to_dict() for l in query]
        return dict(contractors=contractors)


class Contractor(restful.Resource):
    def get(self, id):
        contractor = models.Party.contractors(g.db).filter_by(id=id).first()
        if contractor is None:
            restful.abort(404)
        return dict(contractor=contractor.to_dict())


class Contracteds(restful.Resource):
    def get(self):
        query = models.Party.contracted(g.db)[:20]
        contracted = [c.to_dict() for c in query]
        return dict(contracted=contracted)


class Contracted(restful.Resource):
    def get(self, id):
        contracted = models.Party.contracted(g.db).filter_by(id=id).first()
        if contracted is None:
            restful.abort(404)
        return dict(contracted=contracted.to_dict())


class Parties(restful.Resource):
    def get(self):
        query = g.db.query(models.Party)[:20]
        parties = [p.to_dict() for p in query]
        return dict(parties=parties)


class Party(restful.Resource):
    def get(self, id):
        party = models.Party.get_by_id(g.db, id)
        if party is None:
            restful.abort(404)
        return dict(party=party.to_dict())


api.add_resource(Licitations, '/licitations')
api.add_resource(Licitation, '/licitations/<int:id>')
api.add_resource(Contractors, '/contractors')
api.add_resource(Contractor, '/contractors/<int:id>')
api.add_resource(Contracteds, '/contracted')
api.add_resource(Contracted, '/contracted/<int:id>')
api.add_resource(Parties, '/parties')
api.add_resource(Party, '/parties/<int:id>')
