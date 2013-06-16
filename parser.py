#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
        data['contractor'] = self.parse_contractor()
        data['contracted'] = self.parse_contracted()

        return data

    def parse_codice(self):
        with self.within('/can:ContractAwardNotice'):
            base_data = {
                'uuid': self.element('/cbc:UUID/text()'),
                'file': (self.element('/cbc:ContractFileID/text()')
                         or self.element('/cbc:ContractFolderID/text()')),
            }

            with self.within('/cac:TenderResult'):
                base_data.update({'result_code': self.element('/cbc:ResultCode/@name')})

        base_data.update({
            'title': self.element('//cac:ProcurementProject/cbc:Name/text()'),
            'type': self.element('//cac:ProcurementProject/cbc:TypeCode/@name'),
            'subtype': self.element('//cac:ProcurementProject/cbc:SubTypeCode/@name'),
            'issued_at': self.parse_iso_datetime(
                date=self.element('/can:ContractAwardNotice/cbc:IssueDate/text()'),
                time=self.element('/can:ContractAwardNotice/cbc:IssueTime/text()')
            ),
            'awarded_at': self.parse_iso_datetime(
                date=self.element('//cac:TenderResult/cbc:AwardDate/text()'),
                time=self.element('//cac:TenderResult/cbc:AwardTime/text()')
            ),
            'amount': self.parse_amount(),
            'payable_amount': self.parse_payable_amount(),
            'budget_amount': self.parse_budget_amount(),
            'budget_payable_amount': self.parse_budget_payable_amount(),
        })

        return base_data

    def parse_iso_datetime(self, date, time):
        if date and time:
            return "{date}T{time}".format(date=date[:10], time=time)


class Codice1Extractor(Extractor):
    def parse_amount(self):
        return to_float(self.element('//cac:TenderResult/cbc:AwardPriceAmount/text()'))

    def parse_payable_amount(self):
        return to_float(self.element('//cac:TenderResult/cbc:TotalAwardPriceAmount/text()'))

    def parse_budget_amount(self):
        return to_float(self.element('//cac:ProcuringProject/cbc:NetBudgetAmount/text()'))

    def parse_budget_payable_amount(self):
        return to_float(self.element('//cac:ProcuringProject/cbc:TotalBudgetAmount/text()'))

    def parse_contracted(self):
        return {
            'nif': self.element('//cac:WinnerParty//cbc:ID[@schemeName="CIF" or @schemeName="NIF"]/text()'),
            'name': self.element('//cac:WinnerParty//cac:PartyName/cbc:Name/text()'),
        }

    def parse_contractor(self):
        return {
            'nif': self.element('//cac:ContractingAuthorityParty//cbc:ID[@schemeName="CIF" or @schemeName="NIF"]/text()'),
            'name': self.element('//cac:ContractingAuthorityParty//cac:PartyName/cbc:Name/text()'),
            'uri': self.element('//cac:ContractingAuthorityParty/cbc:BuyerProfileURIID/text()'),
        }


class Codice2Extractor(Extractor):
    def parse_amount(self):
        return to_float(self.element('//cac:AwardedTenderedProject//cbc:TaxExclusiveAmount/text()'))

    def parse_payable_amount(self):
        return to_float(self.element('//cac:AwardedTenderedProject//cbc:PayableAmount/text()'))

    def parse_budget_amount(self):
        return to_float(self.element('//cac:BudgetAmount/cbc:TaxExclusiveAmount/text()'))

    def parse_budget_payable_amount(self):
        return to_float(self.element('//cac:BudgetAmount/cbc:TotalAmount/text()'))

    def parse_contracted(self):
        return {
            'nif': self.element('//cac:WinningParty//cbc:ID[@schemeName="CIF" or @schemeName="NIF" or @schemeName="OTROS"]/text()'),
            'name': self.element('//cac:WinningParty//cac:PartyName/cbc:Name/text()'),
        }

    def parse_contractor(self):
        return {
            'nif': self.element('//cac:ContractingParty//cbc:ID[@schemeName="CIF" or @schemeName="NIF"]/text()'),
            'name': self.element('//cac:ContractingParty//cac:PartyName/cbc:Name/text()'),
            'uri': self.element('//cac:ContractingParty/cbc:BuyerProfileURIID/text()'),
        }


class Parser(object):

    def __init__(self, content):
        content = self.prepare_content(content)
        document = self.prepare_document(content)

        if self.document_type != 'ContractAwardNotice':
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
        return self.element.tag.split('}')[-1]

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


def main():
    store = get_store()
    session = get_session()

    print store.select(table='raw')
    print Parser(store.select(table='raw')).parse()

if __name__ == "__main__":
    main()
