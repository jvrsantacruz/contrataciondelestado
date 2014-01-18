# -*- coding: utf-8 -*-

from expects import expect
from mamba import describe, context, before

from contratacion.parser import Parser, Codice1Parser, Codice2Parser

from spec.fixtures import (DOCUMENT, NO_VERSION_DOCUMENT, CODICE_2_DOCUMENT,
                           CODICE_21_DOCUMENT, NON_AWARDED_CODICE_2_DOCUMENT)


def _make_parser(doc):
    return Parser(doc)


with describe(Parser) as _:
    with context('type attribute'):
        def it_should_be_the_root_element_name():
            expect(_.parser).to.have.property('type', 'ContractAwardNotice')

    with context('version attribute'):
        def it_should_be_none_if_codice1():
            parser = _make_parser(NO_VERSION_DOCUMENT)

            expect(parser).to.have.property('version', None)

        def it_should_be_codice21_when_it_is():
            parser = _make_parser(CODICE_21_DOCUMENT)

            expect(parser).to.have.property('version', 'CODICE 2.01')

    with context('prepare_namespaces function'):
        def it_should_obtain_document_namespaces():
            class Document(object):
                nsmap = {'foo': 'bar'}

            namespaces = _.parser.prepare_namespaces(Document())

            expect(namespaces).to.have('foo')

        def it_should_rename_unnamed_namespaces_to_cac():
            class Document(object):
                nsmap = {None: 'bar'}

            namespaces = _.parser.prepare_namespaces(Document())

            expect(namespaces).to.have('can')

    @before.all
    def fixture():
        _.parser = _make_parser(DOCUMENT)


with describe(Codice1Parser) as _:
    with context('parse method'):
        def it_should_obtain_uuid():
            expect(_.result['uuid']).to.be.equal('2008-002958')

        def it_should_obtain_file():
            expect(_.result['file']).to.be.equal('006/08')

        def it_should_obtain_title():
            expect(_.result['title']).to.be.equal(_.title)

        def it_should_obtain_amount():
            expect(_.result['amount']).to.be.equal(5000000)

        def it_should_obtain_issued_at():
            expect(_.result['issued_at']).to.be.equal('2008-08-04T13:09:17+02:00')

        def it_should_obtain_awarded_at():
            expect(_.result['awarded_at']).to.be.equal('2008-08-01T00:00:00+02:00')

        def it_should_obtain_contractor_party():
            expect(_.result['contractor']).to.be.a(dict)

        def it_should_obtain_contractor_party_nif():
            expect(_.result['contractor']['nif']).to.be.equal(u'Q2829010D')

        def it_should_obtain_contractor_party_name():
            expect(_.result['contractor']['name']).to.be.equal(_.contractor_party_name)

        def it_should_obtain_contracted_party():
            expect(_.result['contracted']).to.be.a(dict)

        def it_should_obtain_contracted_party_nif():
            expect(_.result['contracted']['nif']).to.be.equal(u'A78688918')

        def it_should_obtain_contracted_party_name():
            expect(_.result['contracted']['name']).to.be.equal(u'ICEBERG MEDIA, S.A.')

    @before.all
    def fixture_():
        _.main_parser = _make_parser(NO_VERSION_DOCUMENT)
        _.parser = Codice1Parser(_.main_parser.query)
        _.result = _.parser.parse()
        _.title = ('PLANIFICACI\xd3N E INSERCI\xd3N EN EL MEDIO TELEVISI\xd3N '
                   'DE LAS CAMPA\xd1AS PUBLICITARIAS DEL FROM DURANTE EL A\xd1O'
                   ' 2008'.decode('latin-1'))
        _.contractor_party_name = ('Fondo de Regulaci\xf3n y Organizaci\xf3n'
                                   ' del Mercado de los Productos de la Pesca'
                                   ' y Cultivos Marinos (FROM)'.decode('latin-1'))


with describe('Codice2Parser with CODICE 2 document') as _:
    with context('parse method'):
        def it_should_obtain_uuid_():
            expect(_.result['uuid']).to.be.equal('2013-475971')

        def it_should_obtain_file_():
            expect(_.result['file']).to.be.equal('4630013001500')

        def it_should_obtain_title_():
            expect(_.result['title']).to.be.equal(_.title)

        def it_should_obtain_amount_():
            expect(_.result['amount']).to.be.equal(17000.0)

        def it_should_obtain_issued_at_():
            expect(_.result['issued_at']).to.be.equal('2013-06-07T12:23:30+02:00')

        def it_should_obtain_awarded_at_():
            expect(_.result['awarded_at']).to.be.equal('2013-05-28T00:00:00+01:00')

        def it_should_obtain_contractor_party_():
            expect(_.result['contractor']).to.be.a(dict)

        def it_should_obtain_contractor_party_nif_():
            expect(_.result['contractor']['nif']).to.be.equal('S3030051A')

        def it_should_obtain_contractor_party_name_():
            expect(_.result['contractor']['name']).to.be.equal(_.contractor_party_name)

        def it_should_obtain_contracted_party_():
            expect(_.result['contracted']).to.be.a(dict)

        def it_should_obtain_contracted_party_nif_():
            expect(_.result['contracted']['nif']).to.be.equal(u'A30033385')

        def it_should_obtain_contracted_party_name_():
            expect(_.result['contracted']['name']).to.be.equal(u'ELECTRICIDAD FERYSAN, S.A.')

    @before.all
    def fixture__():
        _.main_parser = _make_parser(CODICE_2_DOCUMENT)
        _.parser = Codice2Parser(_.main_parser.query)
        _.result = _.parser.parse()
        _.title = ('Servicio de Conservaci\xf3n y Mantenimiento de Las '
                   'Instalaciones T\xe9rmicas de la Base A\xe9rea de '
                   'Alcantarilla'.decode('latin-1'))
        _.contractor_party_name = ('Jefatura de la Secci\xf3n Econ\xf3mico-'
                                   'Administrativa 63 - Base A\xe9rea de '
                                   'Alcantarilla'.decode('latin-1'))

with describe('Codice2Parser with CODICE 2.1 document') as _:
    with context('parse method'):
        def it_should_obtain_uuid__():
            expect(_.result['uuid']).to.be.equal('2013-476016')

        def it_should_obtain_file__():
            expect(_.result['file']).to.be.equal('500083004400')

        def it_should_obtain_title__():
            expect(_.result['title']).to.be.equal('Gases Industriales')

        def it_should_obtain_amount__():
            expect(_.result['amount']).to.be.equal(124700)

        def it_should_obtain_issued_at__():
            expect(_.result['issued_at']).to.be.equal('2013-06-07T13:03:50+02:00')

        def it_should_obtain_awarded_at__():
            expect(_.result['awarded_at']).to.be.equal('2013-06-05T00:00:00+02:00')

        def it_should_obtain_contractor_party__():
            expect(_.result['contractor']).to.be.a(dict)

        def it_should_obtain_contractor_party_nif__():
            expect(_.result['contractor']['nif']).to.be.equal('Q2822003F')

        def it_should_obtain_contractor_party_name__():
            expect(_.result['contractor']['name']).to.be.equal(
                'Direcci\xf3n General del INTA'.decode('latin-1'))

        def it_should_obtain_contracted_party__():
            expect(_.result['contracted']).to.be.a(dict)

        def it_should_obtain_contracted_party_nif__():
            expect(_.result['contracted']['nif']).to.be.equal('B28062339')

        def it_should_obtain_contracted_party_name__():
            expect(_.result['contracted']['name']).to.be.equal(
                'PRAXAIR ESPA\xd1A, SLU'.decode('latin-1'))

    @before.all
    def fixture___():
        _.main_parser = _make_parser(CODICE_21_DOCUMENT)
        _.parser = Codice2Parser(_.main_parser.query)
        _.result = _.parser.parse()
        _.title = ('Servicio de Conservaci\xf3n y Mantenimiento de Las '
                   'Instalaciones T\xe9rmicas de la Base A\xe9rea de '
                   'Alcantarilla'.decode('latin-1'))
        _.contractor_party_name = ('Jefatura de la Secci\xf3n Econ\xf3mico-'
                                   'Administrativa 63 - Base A\xe9rea de '
                                   'Alcantarilla'.decode('latin-1'))

with describe('Codice2Parser with a non awarded CODICE 2 document') as _:
    with context('parse method'):
        def it_should_obtain_uuid___():
            expect(_.result['uuid']).to.be.equal(u'2013-540567')

        def it_should_obtain_file___():
            expect(_.result['file']).to.be.equal(u'PA 01/2013')

        def it_should_obtain_title___():
            expect(_.result['title']).to.be.equal(_.title.decode('latin-1'))

        def it_should_obtain_amount___():
            expect(_.result['amount']).to.be.equal(None)

        def it_should_obtain_issued_at___():
            expect(_.result['issued_at']).to.be.equal('2013-12-16T12:03:01+01:00')

        def it_should_obtain_awarded_at___():
            expect(_.result['awarded_at']).to.be.equal('2013-12-12T00:00:00+01:00')

        def it_should_obtain_contractor_party___():
            expect(_.result['contractor']).to.be.a(dict)

        def it_should_obtain_contractor_party_nif___():
            expect(_.result['contractor']['nif']).to.be.equal('S2800464F')

        def it_should_obtain_contractor_party_name___():
            expect(_.result['contractor']['name']).to.be.equal(
                _.contractor_party_name.decode('latin-1'))

        def it_should_obtain_contracted_party___():
            expect(_.result['contracted']).to.be.none

    @before.all
    def fixture____():
        _.main_parser = _make_parser(NON_AWARDED_CODICE_2_DOCUMENT)
        _.parser = Codice2Parser(_.main_parser.query)
        _.result = _.parser.parse()
        _.title = 'Suministro para la adquisici\xf3n actualizaci\xf3n y soporte t\xe9cnico de producto Microsoft con destino a la Subsecretaria del Ministerio de Hacienda y Administraciones P\xfablicas'
        _.contractor_party_name = 'Subsecretar\xeda de Hacienda y Administraciones P\xfablicas (Oficial\xeda Mayor)'
