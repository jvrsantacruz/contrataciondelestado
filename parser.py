#!/usr/bin/env python
#-*- coding: utf-8 -*-

from itertools import chain

from lxml import etree
import y_serial_v060 as y_serial

from models import get_session, Licitation, Contractor, Contracted


def prefixed_tag_names(namespaces):

    root_components = ['ContractAwardNotice']

    basic_components = [
        'ActivityCode', 'AddressFormatCode', 'AwardDate', 'AwardTime', 'CityName',
        'ContractFolderID', 'ContractFileID', 'ContractingPartyTypeCode', 'CustomizationID',
        'Description', 'ElectronicMail', 'ExpenseCode', 'ID', 'IdentificationCode', 'IssueDate', 'IssueTime',
        'GovernmentProcurementAgreementConstraintIndicator',
        'ItemClassificationCode', 'JobTitle', 'Line', 'Name', 'PayableAmount',
        'PostalZone', 'ProcedureCode', 'ProfileID', 'ResultCode',
        'SubmissionMethodCode', 'SubTypeCode', 'TaxExclusiveAmount', 'Telefax',
        'Telephone', 'TotalAmount', 'TypeCode', 'UrgencyCode', 'UUID',
    ]

    aggregate_components = [
        'Address', 'AddressLine', 'AwardedTenderedProject', 'BudgetAmount',
        'BuyerProfileURIID', 'Contact', 'ContractingParty',
        'ContractingAuthorityParty', 'Country', 'DocumentAvailabilityPeriod',
        'LegalMonetaryTotal', 'OccurrenceLocation', 'OpenTenderEvent', 'Party',
        'PartyIdentification', 'PartyName', 'Person', 'PostalAddress',
        'ProcurementProject', 'RequiredCommodityClassification',
        'TenderingProcess', 'TenderResult', 'TenderSubmissionDeadlinePeriod',
        'WinningParty', 'MinutesDocumentReference', 'TenderingTerms'
    ]

    def prefix(ns, tag):
        return "{" + namespaces[ns] + "}" + tag

    components = chain(
        ((name, prefix('can', name)) for name in root_components),
        ((name, prefix('cbc', name)) for name in basic_components),
        ((name, prefix('cac', name)) for name in aggregate_components))

    return dict(components)


class Parser(object):
    def __init__(self, content):
        content = self.prepare_content(content)
        self.document = self.prepare_document(content)
        self.namespaces = self.prepare_namespaces(self.document)

    def prepare_document(self, content):
        return etree.fromstring(content)

    def prepare_content(self, content):
        return content.encode('utf-8')

    def prepare_namespaces(self, document):
        return dict((prefix or 'can', url)
                    for prefix, url in document.nsmap.items())

    def xpath(self, query):
        return self.document.xpath(query, namespaces=self.namespaces)

    def element(self, query):
        return first(self.xpath(query))

    def parse(self):
        data = self.parse_codice()
        data['contractor'] = self.parse_contractor()
        data['contracted'] = self.parse_contracted()

        return data

    def parse_codice(self):
        return {
            'uuid': self.element('/can:ContractAwardNotice/cbc:UUID/text()'),
            'file': self.element('/can:ContractAwardNotice/cbc:ContractFileID/text()'),
            'title': self.element('//cac:ProcurementProject/cbc:Name/text()'),
            'type': self.element('//cac:ProcurementProject/cbc:TypeCode/@name'),
            'subtype': self.element('//cac:ProcurementProject/cbc:SubTypeCode/@name'),
            'issued_at': "{date}T{time}".format(
                date=self.element('/can:ContractAwardNotice/cbc:IssueDate/text()')[:10],
                time=self.element('/can:ContractAwardNotice/cbc:IssueTime/text()')
            ),
            'awarded_at': "{date}T{time}".format(
                date=self.element('//cac:TenderResult/cbc:AwardDate/text()')[:10],
                time=self.element('//cac:TenderResult/cbc:AwardTime/text()')
            ),
            'amount': to_int(self.element('//cac:AwardedTenderedProject//cbc:TaxExclusiveAmount/text()')),
            'payable_amount': to_int(self.element('//cac:AwardedTenderedProject//cbc:PayableAmount/text()')),
        }

    def parse_contractor(self):
        return {
            'nif': self.element('//cac:ContractingParty//cbc:ID[@schemeName="CIF" or @schemeName="NIF"]/text()'),
            'name': self.element('//cac:ContractingParty//cac:PartyName/cbc:Name/text()'),
            'uri': self.element('//cac:ContractingParty/cbc:BuyerProfileURIID/text()'),
        }

    def parse_contracted(self):
        return {
            'nif': self.element('//cac:WinningParty//cbc:ID[@schemeName="CIF" or @schemeName="NIF"]/text()'),
            'name': self.element('//cac:WinningParty//cac:PartyName/cbc:Name/text()'),
        }


def first(elements):
    for element in elements:
        return element


def to_int(number):
    try:
        return int(number)
    except (TypeError, ValueError):
        return None


def get_store():
    return y_serial.Main('tmp.slite')


def main():
    store = get_store()
    session = get_session()

    print store.select(table='raw')
    print Parser(store.select(table='raw')).parse()

if __name__ == "__main__":
    main()
