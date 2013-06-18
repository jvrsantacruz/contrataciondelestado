#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from contextlib import contextmanager

from lxml import etree
import y_serial_v060 as y_serial

from models import get_session, Licitation, Contractor, Contracted


class Extractor(object):
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

    def parse(self):
        data = self.parse_codice()
        data.update(self.parse_extra())
        data['contractor'] = self.parse_contractor()
        data['contracted'] = self.parse_contracted()

        return data

    def parse_codice(self):
        with self.within('/can:ContractAwardNotice'):
            data = {
                'uuid': self.element('/cbc:UUID/text()'),
                'file': (self.element('/cbc:ContractFileID/text()') or self.element('/cbc:ContractFolderID/text()')),
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

        return data

    def parse_iso_datetime(self, date, time):
        if date:
            zone = date[10:]
            nozone_date = date[:10]
            nozone_time = (time and time[:10]) or "00:00:00"
            return "{date}T{time}{zone}".format(date=nozone_date, time=nozone_time, zone=zone)


class Codice1Extractor(Extractor):
    def parse_extra(self):
        with self.within('/can:ContractAwardNotice'):
            with self.within('/cac:TenderResult'):
                data = {
                    'amount': to_float(self.element('/cbc:AwardPriceAmount/text()')),
                    'payable_amount': to_float(self.element('/cbc:TotalAwardPriceAmount/text()')),
                }

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


class Codice2Extractor(Extractor):
    def parse_extra(self):
        data = {}

        with self.within('/can:ContractAwardNotice'):
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


class Validator(object):
    accepted_result_codes = {
        'Adjudicado': '8',
        'Formalizado': '9',
        'Adjudicado Definitivamente': '2',
    }

    def validate(self, data):
        assert data['result_code'] in self.accepted_result_codes.values(), 'Not Successful'

        assert any(map(lambda e: e is not None, [
            data['amount'], data['payable_amount'],
            data['budget_amount'], data['budget_payable_amount']
        ])), "All payment and budget amounts are None"

        assert data['uuid'], "UUID is empty"
        assert data['file'], "File is empty"
        assert data['issued_at'], "issued_at is empty"
        assert data['awarded_at'], "awarded_at is empty"

        assert data['contractor'], "Contractor is empty"
        assert data['contractor']['nif'], "Contractor's nif is empty"
        assert data['contractor']['name'], "Contractor's name is empty"

        assert data['contracted'], "Contracted is empty"
        assert data['contracted']['nif'], "Contracted's nif is empty"
        assert data['contracted']['name'], "Contracted's name is empty"

        return data


class Parser(object):

    def __init__(self, content):
        content = self.prepare_content(content)
        document = self.prepare_document(content)

        if self.document_type(document) != 'ContractAwardNotice':
            raise ValueError("Unkown document type")

        namespaces = self.prepare_namespaces(document)
        self.extractor = self.prepare_extractor(document, namespaces)

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

    def prepare_extractor(self, document, namespaces):
        version = self.version(document)

        Extractor = {
            None: Codice1Extractor,
            'CODICE 2.0': Codice2Extractor,
            'CODICE 2.01': Codice2Extractor
        }[version]

        return Extractor(document, namespaces)

    def version(self, document):
        return first(document.xpath('*[local-name() = "CustomizationID"]/text()'))

    def document_type(self, document):
        return document.tag.split('}')[-1]

    def parse(self):
        return self.extractor.parse()


def first(elements):
    for element in elements:
        return element


def to_float(number):
    try:
        return float(number)
    except (TypeError, ValueError):
        return None


def get_store():
    return y_serial.Main('tmp.sqlite')


def parse(store, validator):
    errors, discarted, parsed = 0, 0, 0
    for n, (timestamp, key, value) in store.iterselectdic('.*', table='raw'):
        try:
            yield validator.validate(Parser(value).parse())
        except (ValueError, AssertionError) as error:
            if str(error) in ("Not Successful", "Unkown document type"):
                discarted += 1
            else:
                print('ignoring', key)
                print error
                errors += 1
        else:
            parsed += 1

        if n % 50 == 0:
            sys.stdout.write("\r\bParsed: {} Errors: {} Discarted: {} Total: {}"
                             .format(parsed, errors, discarted, discarted + errors + parsed))
            sys.stdout.flush()


def main():
    store = get_store()
    session = get_session()
    validator = Validator()

    total = 0
    for data in parse(store, validator):
        total += data['amount'] or data['budget_amount']

    print('Total: ' + str(total))

if __name__ == "__main__":
    main()
