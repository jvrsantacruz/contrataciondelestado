#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
from contextlib import contextmanager

from lxml import etree

from .store import Store
from .validators import validate
from .models import get_session, Licitation
from .helpers import first, to_float, compose_iso_date


logger = logging.getLogger('parser')


class Query(object):
    """Builds and execute xpath in easy steps

    Based on context managers that keeps state, a query can be composed by
    steps, allowing to perform multiple queries with the same prefix.

    >>> document = etree.fromstring('''
    ... <root>
    ...    <element>
    ...        <child>foo</child>
    ...        <sibling>bar</sibling>
    ...    </element>
    ... </root>
    ... ''')
    >>> namespaces = {}
    >>> query = Query(document, namespaces)
    >>> with query('/root') as q:
    ...     with query('/element'):
    ...         print(q['/child/text()'])
    'foo'
    """
    def __init__(self, document, namespaces):
        """Create a query manager object

        :param document: :class:`etree.ElementTree` object
        :param namespaces: a `prefix: uri` dictionary for xml namespaces.
        """
        self.prefix = ''
        self.document = document
        self.namespaces = namespaces

    def xpath(self, query):
        """Compile a xpath query"""
        return self.document.xpath(query, namespaces=self.namespaces)

    def element(self, query_text):
        """Perform the xpath query and get the result"""
        return first(self.xpath(self.query(query_text)))

    def query(self, query_text):
        """Add the current context to the given query"""
        return self.prefix + query_text

    @contextmanager
    def within(self, prefix):
        """Append the given piece of query to the context"""
        old_prefix = self.prefix

        self.prefix += prefix
        yield self
        self.prefix = old_prefix

    @contextmanager
    def __call__(self, prefix):
        with self.within(prefix) as query:
            yield query

    def __getitem__(self, query_text):
        """Perform the xpath query and get the result"""
        return self.element(query_text)


class ParserImplementation(object):
    def __init__(self, query):
        self.query = query


class Codice1Parser(ParserImplementation):
    def parse(self):
        data = self.parse_codice()
        data['contractor'] = self.parse_contractor()
        data['contracted'] = self.parse_contracted()
        return data

    def parse_codice(self):
        with self.query('/can:ContractAwardNotice') as q:
            data = {
                'uuid': q['/cbc:UUID/text()'],
                'file': q['/cbc:ContractFileID/text()'],
                'issued_at': compose_iso_date(
                    date=q['/cbc:IssueDate/text()'],
                    time=q['/cbc:IssueTime/text()']
                ),
            }
            with q('/cac:TenderResult'):
                data.update({
                    'result_code': q['/cbc:ResultCode/text()'],
                    'awarded_at': compose_iso_date(
                        date=q['/cbc:AwardDate/text()'],
                        time=q['/cbc:AwardTime/text()']
                    ),
                    'amount': to_float(q['/cbc:AwardPriceAmount/text()']),
                    'payable_amount': to_float(q['/cbc:TotalAwardPriceAmount/text()']),
                })
                with q('/cac:ProcuringProject'):
                    data.update({
                        'title': q['/cbc:ContractName/text()'],
                        'type': q['/cbc:TypeCode/@name'],
                        'subtype': q['/cbc:SubTypeCode/@name'],
                        'budget_amount': to_float(q['/cbc:NetBudgetAmount/text()']),
                        'budget_payable_amount': to_float(q['/cbc:TotalBudgetAmount/text()']),
                    })
        return data

    def parse_contracted(self):
        with self.query('/can:ContractAwardNotice/cac:TenderResult/cac:WinnerParty') as q:
            return {
                'name': q['/cac:PartyName/cbc:Name/text()'],
                'nif': q['/cac:PartyIdentification/cbc:ID/text()']
            }

    def parse_contractor(self):
        with self.query('/can:ContractAwardNotice/cac:ContractingAuthorityParty') as q:
            data = {'uri': q['/cbc:BuyerProfileURIID/text()']}

            with q('/cac:Party'):
                data.update({
                    'name': q['/cac:PartyName/cbc:Name/text()'],
                    'nif': q['/cac:PartyIdentification/cbc:ID[@schemeName="CIF" or @schemeName="NIF"]/text()'],
                })
        return data


class Codice2Parser(ParserImplementation):
    def parse(self):
        data = self.parse_codice()
        data['contractor'] = self.parse_contractor()
        data['contracted'] = self.parse_contracted()
        return data

    def parse_codice(self):
        with self.query('/can:ContractAwardNotice') as q:
            data = {
                'uuid': q['/cbc:UUID/text()'],
                'file': q['/cbc:ContractFolderID/text()'],
                'issued_at': compose_iso_date(
                    date=q['/cbc:IssueDate/text()'],
                    time=q['/cbc:IssueTime/text()']
                ),
            }
            with q('/cac:TenderResult'):
                data.update({
                    'result_code': q['/cbc:ResultCode/text()'],
                    'awarded_at': compose_iso_date(
                        date=q['/cbc:AwardDate/text()'],
                        time=q['/cbc:AwardTime/text()']
                    ),
                })

            with q('/cac:ProcurementProject'):
                data.update({
                    'title': q['/cbc:Name/text()'],
                    'type': q['/cbc:TypeCode/@name'],
                    'subtype': q['/cbc:SubTypeCode/@name'],
                    'budget_amount': to_float(q['/cbc:BudgetAmount/cbc:TaxExclusiveAmount/text()']),
                    'budget_payable_amount': to_float(q['/cbc:BudgetAmount/cbc:PayableAmount/text()']),
                })

            with q('/cac:TenderResult'):
                with q('/cac:AwardedTenderedProject'):
                    with q('/cac:LegalMonetaryTotal'):
                        data.update({
                            'amount': to_float(q['/cbc:TaxExclusiveAmount/text()']),
                            'payable_amount': to_float(q['/cbc:PayableAmount/text()']),
                        })
        return data

    def parse_contracted(self):
        with self.query('/can:ContractAwardNotice') as q:
            with q('/cac:TenderResult'):
                with q('/cac:WinningParty'):
                    return {
                        'nif': (q['/cac:PartyIdentification/cbc:ID[@schemeName="CIF" or @schemeName="NIF" or @schemeName="NIE" or @schemeName="OTROS" or @schemeName="ID_UTE_TEMP_PLATAFORMA"]/text()']
                                or q['/cac:PartyIdentification/cbc:ID/text()']),
                        'name': q['/cac:PartyName/cbc:Name/text()'],
                    }

    def parse_contractor(self):
        with self.query('/can:ContractAwardNotice') as q:
            with q('/cac:ContractingParty'):
                with q('/cac:Party'):
                    return {
                        'nif': q['/cac:PartyIdentification/cbc:ID[@schemeName="CIF" or @schemeName="NIF"]/text()'],
                        'name': q['/cac:PartyName/cbc:Name/text()'],
                        'uri': q['/cbc:WebsiteURI/text()'],
                    }


class Parser(object):
    def __init__(self, content):
        content = self.prepare_content(content)
        self.document = self.prepare_document(content)
        self.version = self.get_version(self.document)
        self.type = self.get_document_type(self.document)
        self.namespaces = self.prepare_namespaces(self.document)

        self.impl = self.prepare_impl()

    @property
    def query(self):
        return Query(self.document, self.namespaces)

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

    def prepare_impl(self):
        Parser = {
            None: Codice1Parser,
            'CODICE 2.0': Codice2Parser,
            'CODICE 2.01': Codice2Parser
        }.get(self.version)
        return Parser(self.query)

    def get_version(self, document):
        return first(document.xpath('*[local-name() = "CustomizationID"]/text()'))

    def get_document_type(self, document):
        return document.tag.split('}')[-1]

    def parse(self):
        return self.impl.parse()


def get_store(database):
    return Store(database)


def iteritems(store):
    for key in store.keys():
        yield key, store.get(key)


def is_valid_document(parser):
    return parser.type == 'ContractAwardNotice'


def parse(store):
    for key, content in iteritems(store):
        try:
            document = Parser(content)
            if is_valid_document(document):
                yield validate(document.parse())
        except etree.XMLSyntaxError:
            pass


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

        if progress % 100 == 0:
            _log_parsing_progress(inserted, ignored, rejected, progress, total)

    _log_parsing_progress(inserted, ignored, rejected, progress, total)
    logger.info('finished')
