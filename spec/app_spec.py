# -*- coding: utf-8 -*-

import json

from expects import expect
from mamba import describe, context, before, pending

from contratacion.application import create_app
from contratacion.models import Licitation, Party, get_session


with describe('Application') as _:

    with context('licitation resource'):
        with context('when GET /licitation'):
            def it_should_return_ok_with_the_first_10_licitations():
                licitations = [l.to_dict() for l in _licitations().limit(_.per_page)]

                with _app().test_client() as client:
                    response = client.get('/licitations')

                _expect_ok_response(response)
                expect(licitations).to.have.length(_.per_page)
                expect(_json_data(response)).to.be.equal(licitations)

        with context('when GET /licitations/400'):
            def it_should_return_ok_with_the_licitation_n_400():
                licitation = _licitation(400).to_dict()

                with _app().test_client() as client:
                    response = client.get('/licitations/400')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(licitation)

        with context('when GET /licitations/999999'):
            def it_should_return_not_found_with_an_error_message():
                with _app().test_client() as client:
                    response = client.get('/licitations/999999')

                _expect_not_found_resposne(response)

        with context('when GET /licitations?page=2'):
            def it_should_return_per_page_items_of_page_2():
                licitations = [l.to_dict() for l in
                    _licitations().offset(_.per_page).limit(_.per_page)]

                with _app().test_client() as client:
                    response = client.get('/licitations?page=2')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(licitations)

    with context('contractor resource'):
        with context('when GET /contractors'):
            def it_should_return_ok_with_the_first_10_contractors():
                contractors = [c.to_dict() for c in _contractors().limit(_.per_page)]

                with _app().test_client() as client:
                    response = client.get('/contractors')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contractors)

        with context('when GET /contractors/400'):
            def it_should_return_ok_with_the_contractor_n_400():
                contractor = _contractor(400).to_dict()

                with _app().test_client() as client:
                    response = client.get('/contractors/400')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contractor)

        with context('when GET /contractors/999999'):
            def it_should_return_not_found_with_an_error_message_():
                with _app().test_client() as client:
                    response = client.get('/contractors/999999')

                _expect_not_found_resposne(response)

    with context('contracted resource'):
        with context('when GET /contracted'):
            def it_should_return_ok_with_the_first_10_contracted():
                contracted = [c.to_dict() for c in _contracted().limit(_.per_page)]

                with _app().test_client() as client:
                    response = client.get('/contracted')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contracted)

        with context('when GET /contracted/400'):
            def it_should_return_ok_with_the_contracted_n_400():
                contracted = _contracted(400).to_dict()

                with _app().test_client() as client:
                    response = client.get('/contracted/400')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(contracted)

        with context('when GET /contracted/999999'):
            def it_should_return_not_found_with_an_error_message__():
                with _app().test_client() as client:
                    response = client.get('/contracted/999999')

                _expect_not_found_resposne(response)

    with context('party resource'):
        with context('when GET /parties'):
            def it_should_return_ok_with_the_first_10_parties():
                parties = [p.to_dict() for p in _parties().limit(_.per_page)]

                with _app().test_client() as client:
                    response = client.get('/parties')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(parties)

        with context('when GET /parties/100'):
            def it_should_return_ok_with_the_party_n_100():
                party = _party(100).to_dict()

                with _app().test_client() as client:
                    response = client.get('/parties/100')

                _expect_ok_response(response)
                expect(_json_data(response)).to.be.equal(party)

        with context('when GET /parties/999999'):
            def it_should_return_not_found_with_an_error_message___():
                with _app().test_client() as client:
                    response = client.get('/parties/999999')

                _expect_not_found_resposne(response)

    @before.all
    def setup():
        _.per_page = 10
        _.db = get_session(_app().config['DATABASE'])

    def _app():
        app = create_app(configuration={'DATABASE': 'test-db.sqlite'})
        app.testing = True
        return app

    def _licitations():
        return _.db.query(Licitation)

    def _licitation(id):
        return _.db.query(Licitation).get(id)

    def _party(id):
        return _.db.query(Party).get(id)

    def _parties():
        return _.db.query(Party)

    def _contractors():
        return Party.contractors(_.db)

    def _contractor(id):
        return Party.contractors(_.db).filter_by(id=id).first()

    def _contracted(id=None):
        if id is None:
            return Party.contracted(_.db)
        else:
            return Party.contracted(_.db).filter_by(id=id).first()

    def _expect_ok_response(response):
        _expect_json_response(response, code=200)

    def _expect_not_found_resposne(response):
        _expect_json_response(response, code=404)

    def _expect_json_response(response, code):
        expect(response.status_code).to.be.equal(code)
        expect(response.content_type).to.be.equal('application/json')

    def _json_data(response):
        return json.loads(response.data)
