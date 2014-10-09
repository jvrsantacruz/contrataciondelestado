# -*- coding: utf-8 -*-

import json

from expects import *

from contratacion.application import create_app
from contratacion.models import Licitation, Party, get_session


with description('Application'):
    with before.all:
        self.per_page = 10
        self.db = get_session(_app().config['DATABASE'])

    with context('licitation resource'):
        with context('when GET /licitation'):
            with it('should return ok with the first 10 licitations'):
                licitations = [l.to_dict() for l in _licitations(self).limit(self.per_page)]

                response = _client().get('/licitations')

                _expect_ok_response(response)
                expect(licitations).to.have.length(self.per_page)
                expect(_json_data(response)).to.be.equal(licitations)

        with context('when GET /licitations/400'):
            with it('should return ok with the licitation n 400'):
                licitation = _liciatation(self, 400).to_dict()

                response = _client().get('/licitations/400')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(licitation)

        with context('when GET /licitations/999999'):
            with it('should return not found with an error message'):
                response = _client().get('/licitations/999999')

                _expect_not_found_resposne(response)

        with context('when GET /licitations?per_page=1'):
            with it('should return a page with the first item'):
                licitations = [l.to_dict() for l in _licitations(self)[:1]]

                response = _client().get('/licitations?per_page=1')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(licitations)

        with context('when GET /licitations?page=2'):
            with it('should return per page items of page 2'):
                licitations = [l.to_dict() for l in
                    _licitations(self).offset(self.per_page).limit(self.per_page)]

                response = _client().get('/licitations?page=2')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(licitations)

        with context('when GET /licitations?per_page=1&page=2'):
            with it('should return a page with the second item'):
                licitations = [l.to_dict() for l in _licitations(self)[1:2]]

                response = _client().get('/licitations?per_page=1&page=2')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(licitations)

    with context('contractor resource'):
        with context('when GET /contractors'):
            with it('should return ok with the first 10 contractors'):
                contractors = [c.to_dict() for c in _contractors(self, ).limit(self.per_page)]

                response = _client().get('/contractors')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contractors)

        with context('when GET /contractors/400'):
            with it('should return ok with the contractor n 400'):
                contractor = _contractor(self, 400).to_dict()

                response = _client().get('/contractors/400')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contractor)

        with context('when GET /contractors/999999'):
            with it('should return not found with an error message '):
                response = _client().get('/contractors/999999')

                _expect_not_found_resposne(response)

        with context('when GET /contractors?per_page=1'):
            with it('should return a page with the first item'):
                contractors = [l.to_dict() for l in _contractors(self, )[:1]]

                response = _client().get('/contractors?per_page=1')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contractors)

        with context('when GET /contractors?page=2'):
            with it('should return per page items of page 2'):
                contractors = [l.to_dict() for l in
                    _contractors(self, ).offset(self.per_page).limit(self.per_page)]

                response = _client().get('/contractors?page=2')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contractors)

        with context('when GET /contractors?per_page=1&page=2'):
            with it('should return a page with the second item'):
                contractors = [l.to_dict() for l in _contractors(self, )[1:2]]

                response = _client().get('/contractors?per_page=1&page=2')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contractors)

    with context('contracted resource'):
        with context('when GET /contracted'):
            with it('should return ok with the first 10 contracted'):
                contracted = [c.to_dict() for c in _contracted(self, ).limit(self.per_page)]

                response = _client().get('/contracted')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contracted)

        with context('when GET /contracted/400'):
            with it('should return ok with the contracted n 400'):
                contracted = _contracted(self, 400).to_dict()

                response = _client().get('/contracted/400')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contracted)

        with context('when GET /contracted/999999'):
            with it('should return not found with an error message  '):
                response = _client().get('/contracted/999999')

                _expect_not_found_resposne(response)

        with context('when GET /contracted?per_page=1'):
            with it('should return a page with the first item    '):
                contracted = [l.to_dict() for l in _contracted(self, )[:1]]

                response = _client().get('/contracted?per_page=1')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contracted)

        with context('when GET /contracted?page=2'):
            with it('should return per page items of page 2   '):
                contracted = [l.to_dict() for l in
                    _contracted(self, ).offset(self.per_page).limit(self.per_page)]

                response = _client().get('/contracted?page=2')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contracted)

        with context('when GET /contracted?per_page=1&page=2'):
            with it('should return a page with the second item    '):
                contracted = [l.to_dict() for l in _contracted(self, )[1:2]]

                response = _client().get('/contracted?per_page=1&page=2')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contracted)

    with context('party resource'):
        with context('when GET /parties'):
            with it('should return ok with the first 10 parties'):
                parties = [p.to_dict() for p in _parties(self, ).limit(self.per_page)]

                response = _client().get('/parties')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(parties)

        with context('when GET /parties/100'):
            with it('should return ok with the party n 100'):
                party = _party(self, 100).to_dict()

                response = _client().get('/parties/100')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(party)

        with context('when GET /parties/999999'):
            with it('should return not found with an error message   '):
                response = _client().get('/parties/999999')

                _expect_not_found_resposne(response)

        with context('when GET /parties?per_page=1'):
            with it('should return a page with the first item   '):
                parties = [l.to_dict() for l in _parties(self, )[:1]]

                response = _client().get('/parties?per_page=1')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(parties)

        with context('when GET /parties?page=2'):
            with it('should return per page items of page 2   '):
                parties = [l.to_dict() for l in
                    _parties(self, ).offset(self.per_page).limit(self.per_page)]

                response = _client().get('/parties?page=2')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(parties)

        with context('when GET /parties?per_page=1&page=2'):
            with it('should return a page with the second item    '):
                parties = [l.to_dict() for l in _parties(self, )[1:2]]

                response = _client().get('/parties?per_page=1&page=2')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(parties)


def _app():
    app = create_app(configuration={'DATABASE': 'test-db.sqlite'})
    app.testing = True
    return app


def _client():
    return _app().test_client()


def _licitations(self):
    return self.db.query(Licitation)


def _liciatation(self, id):
    return self.db.query(Licitation).get(id)


def _party(self, id):
    return self.db.query(Party).get(id)


def _parties(self, ):
    return self.db.query(Party)


def _contractors(self, ):
    return Party.contractors(self.db)


def _contractor(self, id):
    return Party.contractors(self.db).filter_by(id=id).first()


def _contracted(self, id=None):
    if id is None:
        return Party.contracted(self.db)
    else:
        return Party.contracted(self.db).filter_by(id=id).first()


def _expect_ok_response(response):
    _expect_json_response(response, code=200)


def _expect_not_found_resposne(response):
    _expect_json_response(response, code=404)


def _expect_json_response(response, code):
    expect(response.status_code).to.be.equal(code)
    expect(response.content_type).to.be.equal('application/json')


def _json_data(response):
    return json.loads(response.data)
