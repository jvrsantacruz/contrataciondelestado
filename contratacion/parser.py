#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
from contextlib import contextmanager

from lxml import etree

from .store import Store
from .validators import validate
from .models import get_session, Licitation


logger = logging.getLogger('parser')


class ParserImplementation(object):
    def __init__(self, document, namespaces):
        self._prefix = ''
        self.document = document
        self.namespaces = namespaces

    def xpath(self, query):
        return self.document.xpath(query, namespaces=self.namespaces)

    def element(self, query_text):
        return first(self.xpath(self.query(query_text)))

    def query(self, query_text):
        return self._prefix + query_text

    @contextmanager
    def within(self, prefix):
        old_prefix = self._prefix

        self._prefix += prefix
        yield self._prefix

        self._prefix = old_prefix

    def parse_iso_datetime(self, date, time):
        if date:
            zone = date[10:]
            nozone_date = date[:10]
            nozone_time = (time and time[:8]) or "00:00:00"
            return "{date}T{time}{zone}".format(date=nozone_date, time=nozone_time, zone=zone)


class Codice1Parser(ParserImplementation):
    def parse(self):
        data = self.parse_codice()
        data['contractor'] = self.parse_contractor()
        data['contracted'] = self.parse_contracted()
        return data

    def parse_codice(self):
        with self.within('/can:ContractAwardNotice'):
            data = {
                'uuid': self.element('/cbc:UUID/text()'),
                'file': self.element('/cbc:ContractFileID/text()'),
                'issued_at': self.parse_iso_datetime(
                    date=self.element('/cbc:IssueDate/text()'),
                    time=self.element('/cbc:IssueTime/text()')
                ),
            }
            with self.within('/cac:TenderResult'):
                data.update({
                    'result_code': self.element('/cbc:ResultCode/text()'),
                    'awarded_at': self.parse_iso_datetime(
                        date=self.element('/cbc:AwardDate/text()'),
                        time=self.element('/cbc:AwardTime/text()')
                    ),
                })
            with self.within('/cac:TenderResult'):
                data.update({
                    'amount': to_float(self.element('/cbc:AwardPriceAmount/text()')),
                    'payable_amount': to_float(self.element('/cbc:TotalAwardPriceAmount/text()')),
                })
                with self.within('/cac:ProcuringProject'):
                    data.update({
                        'title': self.element('/cbc:ContractName/text()'),
                        'type': self.element('/cbc:TypeCode/@name'),
                        'subtype': self.element('/cbc:SubTypeCode/@name'),
                        'budget_amount': to_float(self.element('/cbc:NetBudgetAmount/text()')),
                        'budget_payable_amount': to_float(self.element('/cbc:TotalBudgetAmount/text()')),
                    })
        return data

    def parse_contracted(self):
        with self.within('/can:ContractAwardNotice/cac:TenderResult/cac:WinnerParty'):
            return {
                'name': self.element('/cac:PartyName/cbc:Name/text()'),
                'nif': self.element('/cac:PartyIdentification/cbc:ID/text()')
            }

    def parse_contractor(self):
        with self.within('/can:ContractAwardNotice/cac:ContractingAuthorityParty'):
            data = {'uri': self.element('/cbc:BuyerProfileURIID/text()')}

            with self.within('/cac:Party'):
                data.update({
                    'name': self.element('/cac:PartyName/cbc:Name/text()'),
                    'nif': self.element('/cac:PartyIdentification/cbc:ID[@schemeName="CIF" or @schemeName="NIF"]/text()'),
                })
        return data


class Codice2Parser(ParserImplementation):
    def parse(self):
        data = self.parse_codice()
        data['contractor'] = self.parse_contractor()
        data['contracted'] = self.parse_contracted()
        return data

    def parse_codice(self):
        with self.within('/can:ContractAwardNotice'):
            data = {
                'uuid': self.element('/cbc:UUID/text()'),
                'file': self.element('/cbc:ContractFolderID/text()'),
                'issued_at': self.parse_iso_datetime(
                    date=self.element('/cbc:IssueDate/text()'),
                    time=self.element('/cbc:IssueTime/text()')
                ),
            }
            with self.within('/cac:TenderResult'):
                data.update({
                    'result_code': self.element('/cbc:ResultCode/text()'),
                    'awarded_at': self.parse_iso_datetime(
                        date=self.element('/cbc:AwardDate/text()'),
                        time=self.element('/cbc:AwardTime/text()')
                    ),
                })

            with self.within('/cac:ProcurementProject'):
                data.update({
                    'title': self.element('/cbc:Name/text()'),
                    'type': self.element('/cbc:TypeCode/@name'),
                    'subtype': self.element('/cbc:SubTypeCode/@name'),
                    'budget_amount': to_float(self.element('/cbc:BudgetAmount/cbc:TaxExclusiveAmount/text()')),
                    'budget_payable_amount': to_float(self.element('/cbc:BudgetAmount/cbc:PayableAmount/text()')),
                })

            with self.within('/cac:TenderResult'):
                with self.within('/cac:AwardedTenderedProject'):
                    with self.within('/cac:LegalMonetaryTotal'):
                        data.update({
                            'amount': to_float(self.element('/cbc:TaxExclusiveAmount/text()')),
                            'payable_amount': to_float(self.element('/cbc:PayableAmount/text()')),
                        })
        return data

    def parse_contracted(self):
        with self.within('/can:ContractAwardNotice'):
            with self.within('/cac:TenderResult'):
                with self.within('/cac:WinningParty'):
                    return {
                        'nif': (self.element('/cac:PartyIdentification/cbc:ID[@schemeName="CIF" or @schemeName="NIF" or @schemeName="NIE" or @schemeName="OTROS" or @schemeName="ID_UTE_TEMP_PLATAFORMA"]/text()')
                                or self.element('/cac:PartyIdentification/cbc:ID/text()')),
                        'name': self.element('/cac:PartyName/cbc:Name/text()'),
                    }

    def parse_contractor(self):
        with self.within('/can:ContractAwardNotice'):
            with self.within('/cac:ContractingParty'):
                with self.within('/cac:Party'):
                    return {
                        'nif': self.element('/cac:PartyIdentification/cbc:ID[@schemeName="CIF" or @schemeName="NIF"]/text()'),
                        'name': self.element('/cac:PartyName/cbc:Name/text()'),
                        'uri': self.element('/cbc:WebsiteURI/text()'),
                    }


class Parser(object):
    def __init__(self, content):
        content = self.prepare_content(content)
        self.document = self.prepare_document(content)
        self.version = self.get_version(self.document)
        self.type = self.get_document_type(self.document)
        self.namespaces = self.prepare_namespaces(self.document)
        self.impl = self.prepare_impl(self.document, self.namespaces)

    def prepare_document(self, content):
        return etree.fromstring(content)

    def prepare_content(self, content):
        return content.encode('utf-8')

    def prepare_namespaces(self, document):
        namespaces = {
            'can': 'urn:dgpe:names:draft:codice:schema:xsd:ContractAwardNotice-1',
            'cbc': 'urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-1',
            'cac': 'urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-1'
        }

        namespaces.update({
            prefix or 'can': url for prefix, url in document.nsmap.items()
        })

        return namespaces

    def prepare_impl(self, document, namespaces):
        Parser = {
            None: Codice1Parser,
            'CODICE 2.0': Codice2Parser,
            'CODICE 2.01': Codice2Parser
        }.get(self.version)
        return Parser(document, namespaces)

    def get_version(self, document):
        return first(document.xpath('*[local-name() = "CustomizationID"]/text()'))

    def get_document_type(self, document):
        return document.tag.split('}')[-1]

    def parse(self):
        return self.impl.parse()


def first(elements):
    for element in elements:
        return element


def to_float(number):
    try:
        return float(number)
    except (TypeError, ValueError):
        return None


def get_store(database):
    return Store(database)


def iteritems(store):
    for key in store.keys():
        yield key, store.get(key)


def is_valid_document(parser):
    return parser.type == 'ContractAwardNotice'


def parse(store):
    for key, content in iteritems(store):
        document = Parser(content)
        if is_valid_document(document):
            yield validate(document.parse())


def _log_parsing_progress(*counters):
    logger.info(
        'Inserted: %d Ignored: %d Rejected: %d Total: %d of %d', *counters)


def parse_documents(store_path, database_path):
    store = get_store(store_path)
    database = get_session(database_path)

    total = len(store)
    inserted, ignored, rejected, progress = 0, 0, 0, 0
    for data in parse(store):
        progress += 1

        if data is None:
            rejected += 1
        elif Licitation.create(database, data):
            inserted += 1
        else:
            ignored += 1

        if total % 100:
            _log_parsing_progress(inserted, ignored, rejected, progress, total)

    _log_parsing_progress(inserted, ignored, rejected, progress, total)
    logger.info('finished')
