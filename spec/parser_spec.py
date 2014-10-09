# -*- coding: utf-8 -*-

from expects import *

from contratacion.parser import Parser, Codice1Parser, Codice2Parser

from spec.fixtures import (DOCUMENT, NO_VERSION_DOCUMENT, CODICE_2_DOCUMENT,
                           CODICE_21_DOCUMENT, NON_AWARDED_CODICE_2_DOCUMENT)


def _make_parser(doc):
    return Parser(doc)


with description(Parser):
    with context('type attribute'):
        with it('should be the root element name'):
            expect(self.parser).to.have.property('type', 'ContractAwardNotice')

    with context('version attribute'):
        with it('should be none if codice1'):
            parser = _make_parser(NO_VERSION_DOCUMENT)

            expect(parser).to.have.property('version', None)

        with it('should be codice21 when it is'):
            parser = _make_parser(CODICE_21_DOCUMENT)

            expect(parser).to.have.property('version', 'CODICE 2.01')

    with context('prepare_namespaces function'):
        with it('should obtain document namespaces'):
            class Document(object):
                nsmap = {'foo': 'bar'}

            namespaces = self.parser.prepare_namespaces(Document())

            expect(namespaces).to.have('foo')

        with it('should rename unnamed namespaces to cac'):
            class Document(object):
                nsmap = {None: 'bar'}

            namespaces = self.parser.prepare_namespaces(Document())

            expect(namespaces).to.have('can')

    with before.all:
        self.parser = _make_parser(DOCUMENT)


with description(Codice1Parser):
    with context('parse method'):
        with it('should obtain uuid'):
            expect(self.result['uuid']).to.be.equal('2008-002958')

        with it('should obtain file'):
            expect(self.result['file']).to.be.equal('006/08')

        with it('should obtain title'):
            expect(self.result['title']).to.be.equal(self.title)

        with it('should obtain amount'):
            expect(self.result['amount']).to.be.equal(5000000)

        with it('should obtain issued at'):
            expect(self.result['issued_at']).to.be.equal('2008-08-04T13:09:17+02:00')

        with it('should obtain awarded at'):
            expect(self.result['awarded_at']).to.be.equal('2008-08-01T00:00:00+02:00')

        with it('should obtain contractor party'):
            expect(self.result['contractor']).to.be.a(dict)

        with it('should obtain contractor party nif'):
            expect(self.result['contractor']['nif']).to.be.equal(u'Q2829010D')

        with it('should obtain contractor party name'):
            expect(self.result['contractor']['name']).to.be.equal(self.contractor_party_name)

        with it('should obtain contracted party'):
            expect(self.result['contracted']).to.be.a(dict)

        with it('should obtain contracted party nif'):
            expect(self.result['contracted']['nif']).to.be.equal(u'A78688918')

        with it('should obtain contracted party name'):
            expect(self.result['contracted']['name']).to.be.equal(u'ICEBERG MEDIA, S.A.')

    with before.all:
        self.main_parser = _make_parser(NO_VERSION_DOCUMENT)
        self.parser = Codice1Parser(self.main_parser.query)
        self.result = self.parser.parse()
        self.title = ('PLANIFICACI\xd3N E INSERCI\xd3N EN EL MEDIO TELEVISI\xd3N '
                   'DE LAS CAMPA\xd1AS PUBLICITARIAS DEL FROM DURANTE EL A\xd1O'
                   ' 2008'.decode('latin-1'))
        self.contractor_party_name = ('Fondo de Regulaci\xf3n y Organizaci\xf3n'
                                   ' del Mercado de los Productos de la Pesca'
                                   ' y Cultivos Marinos (FROM)'.decode('latin-1'))


with describe('Codice2Parser with CODICE 2 document') as _:
    with context('parse method'):
        with it('should obtain uuid '):
            expect(self.result['uuid']).to.be.equal('2013-475971')

        with it('should obtain file '):
            expect(self.result['file']).to.be.equal('4630013001500')

        with it('should obtain title '):
            expect(self.result['title']).to.be.equal(self.title)

        with it('should obtain amount '):
            expect(self.result['amount']).to.be.equal(17000.0)

        with it('should obtain issued at '):
            expect(self.result['issued_at']).to.be.equal('2013-06-07T12:23:30+02:00')

        with it('should obtain awarded at '):
            expect(self.result['awarded_at']).to.be.equal('2013-05-28T00:00:00+01:00')

        with it('should obtain contractor party '):
            expect(self.result['contractor']).to.be.a(dict)

        with it('should obtain contractor party nif '):
            expect(self.result['contractor']['nif']).to.be.equal('S3030051A')

        with it('should obtain contractor party name '):
            expect(self.result['contractor']['name']).to.be.equal(self.contractor_party_name)

        with it('should obtain contracted party '):
            expect(self.result['contracted']).to.be.a(dict)

        with it('should obtain contracted party nif '):
            expect(self.result['contracted']['nif']).to.be.equal(u'A30033385')

        with it('should obtain contracted party name '):
            expect(self.result['contracted']['name']).to.be.equal(u'ELECTRICIDAD FERYSAN, S.A.')

    with before.all:
        self.main_parser = _make_parser(CODICE_2_DOCUMENT)
        self.parser = Codice2Parser(self.main_parser.query)
        self.result = self.parser.parse()
        self.title = ('Servicio de Conservaci\xf3n y Mantenimiento de Las '
                   'Instalaciones T\xe9rmicas de la Base A\xe9rea de '
                   'Alcantarilla'.decode('latin-1'))
        self.contractor_party_name = ('Jefatura de la Secci\xf3n Econ\xf3mico-'
                                   'Administrativa 63 - Base A\xe9rea de '
                                   'Alcantarilla'.decode('latin-1'))

with describe('Codice2Parser with CODICE 2.1 document') as _:
    with context('parse method'):
        with it('should obtain uuid  '):
            expect(self.result['uuid']).to.be.equal('2013-476016')

        with it('should obtain file  '):
            expect(self.result['file']).to.be.equal('500083004400')

        with it('should obtain title  '):
            expect(self.result['title']).to.be.equal('Gases Industriales')

        with it('should obtain amount  '):
            expect(self.result['amount']).to.be.equal(124700)

        with it('should obtain issued at  '):
            expect(self.result['issued_at']).to.be.equal('2013-06-07T13:03:50+02:00')

        with it('should obtain awarded at  '):
            expect(self.result['awarded_at']).to.be.equal('2013-06-05T00:00:00+02:00')

        with it('should obtain contractor party  '):
            expect(self.result['contractor']).to.be.a(dict)

        with it('should obtain contractor party nif  '):
            expect(self.result['contractor']['nif']).to.be.equal('Q2822003F')

        with it('should obtain contractor party name  '):
            expect(self.result['contractor']['name']).to.be.equal(
                'Direcci\xf3n General del INTA'.decode('latin-1'))

        with it('should obtain contracted party  '):
            expect(self.result['contracted']).to.be.a(dict)

        with it('should obtain contracted party nif  '):
            expect(self.result['contracted']['nif']).to.be.equal('B28062339')

        with it('should obtain contracted party name  '):
            expect(self.result['contracted']['name']).to.be.equal(
                'PRAXAIR ESPA\xd1A, SLU'.decode('latin-1'))

    with before.all:
        self.main_parser = _make_parser(CODICE_21_DOCUMENT)
        self.parser = Codice2Parser(self.main_parser.query)
        self.result = self.parser.parse()
        self.title = ('Servicio de Conservaci\xf3n y Mantenimiento de Las '
                   'Instalaciones T\xe9rmicas de la Base A\xe9rea de '
                   'Alcantarilla'.decode('latin-1'))
        self.contractor_party_name = ('Jefatura de la Secci\xf3n Econ\xf3mico-'
                                   'Administrativa 63 - Base A\xe9rea de '
                                   'Alcantarilla'.decode('latin-1'))

with describe('Codice2Parser with a non awarded CODICE 2 document') as _:
    with context('parse method'):
        with it('should obtain uuid   '):
            expect(self.result['uuid']).to.be.equal(u'2013-540567')

        with it('should obtain file   '):
            expect(self.result['file']).to.be.equal(u'PA 01/2013')

        with it('should obtain title   '):
            expect(self.result['title']).to.be.equal(self.title.decode('latin-1'))

        with it('should obtain amount   '):
            expect(self.result['amount']).to.be.equal(None)

        with it('should obtain issued at   '):
            expect(self.result['issued_at']).to.be.equal('2013-12-16T12:03:01+01:00')

        with it('should obtain awarded at   '):
            expect(self.result['awarded_at']).to.be.equal('2013-12-12T00:00:00+01:00')

        with it('should obtain contractor party   '):
            expect(self.result['contractor']).to.be.a(dict)

        with it('should obtain contractor party nif   '):
            expect(self.result['contractor']['nif']).to.be.equal('S2800464F')

        with it('should obtain contractor party name   '):
            expect(self.result['contractor']['name']).to.be.equal(
                self.contractor_party_name.decode('latin-1'))

        with it('should obtain contracted party   '):
            expect(self.result['contracted']).to.be.none

    with before.all:
        self.main_parser = _make_parser(NON_AWARDED_CODICE_2_DOCUMENT)
        self.parser = Codice2Parser(self.main_parser.query)
        self.result = self.parser.parse()
        self.title = 'Suministro para la adquisici\xf3n actualizaci\xf3n y soporte t\xe9cnico de producto Microsoft con destino a la Subsecretaria del Ministerio de Hacienda y Administraciones P\xfablicas'
        self.contractor_party_name = 'Subsecretar\xeda de Hacienda y Administraciones P\xfablicas (Oficial\xeda Mayor)'
