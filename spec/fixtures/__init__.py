# -*- coding: utf-8 -*-

import codecs


def open(path):
    return codecs.open(path, encoding='utf-8')


with open('spec/fixtures/codice_1.xml') as stream:
    NO_VERSION_DOCUMENT = stream.read()


with open('spec/fixtures/codice_2.xml') as stream:
    CODICE_2_DOCUMENT = stream.read()


with open('spec/fixtures/codice_21.xml') as stream:
    CODICE_21_DOCUMENT = stream.read()


DOCUMENT = CODICE_2_DOCUMENT


with open('spec/fixtures/non_awarded_codice_2.xml') as stream:
    NON_AWARDED_CODICE_2_DOCUMENT = stream.read()


with open('spec/fixtures/main_page.html') as stream:
    MAIN_PAGE = stream.read()

FIRST_PAGE_URL = '/wps/portal/!ut/p/b0/fc5NDoIwFATgs3iCDrQFWZJSCgjyo1TohrAwBiPgwnh-gbjVt5vkm8wjhjTETP17uPWvYZ76x5qN0yk4TMQeBQLpIc7PSSXOLvKAL6BdAH6cj63PZC5EGNmAzCjsyFV7SQVQcHIhZiOcCqYTXTinWAFxFAZpbXEo2_mCPxPHaB6vpF0Y7XwtS399VemDgO3WWVjQylKpRZ5jgzsrdx-R_UUj/'

with open('spec/fixtures/first_page.html') as stream:
    FIRST_PAGE = stream.read()

FIRST_PAGE_ACTION = '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=javax.servlet.include.path_info=QCPjspQCPLicitacionesResueltasView.jsp/250214691671/-/'

FIRST_PAGE_FORM_DATA = {
    'javax.faces.ViewState': 'j_id1:j_id2',
    'viewns_Z7_G064CI9300DE90IOTJRCT70OT7_:form1': 'viewns_Z7_G064CI9300DE90IOTJRCT70OT7_:form1',
    'viewns_Z7_G064CI9300DE90IOTJRCT70OT7_:form1:siguienteLink': 'Siguiente >>'
}

DETAIL_URLS = [
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=26674922/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=26675139/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=26674878/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=26624933/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=24518928/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=26398997/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=26669318/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=24027557/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=22369032/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=24071272/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=23512511/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=23512158/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=26570321/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=24571933/250214691670/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=26362814/250214691671/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=24941484/250214691671/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=26268273/250214691671/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=25279843/250214691671/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=24697805/250214691671/-/',
    '/wps/portal/!ut/p/b1/hc7LDoIwFATQLzId2lLskpTSlqgQRZBuDAtjSHhsjN8vEl2KdzfJmcwlnjQB5QG4lIySC_Fj--zu7aObxrZ_Zy-uBoIrJxmQaAmXl9lRlRHyJJxBMwP8uBhLn-tcqdRSQO8ZqI3MVjMFFN_-CvizXxO_kJApXmVVIU7OAM6mye4chDBUfMDKiwc7DTcy-D6VbhO_ALcY_OU!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=25486965/250214691671/-/'
]

with open('spec/fixtures/detail_page.html') as stream:
    DETAIL_PAGE = stream.read()

DATA_PAGE_URL = "https://contrataciondelestado.es/wps/wcm/connect/PLACE_es/Site/area/docAccCmpnt?srv=cmpnt&cmpntname=GetDocumentsById&source=library&DocumentIdParam=8ba0d726-6ca3-4271-9346-6f422f9c5115"

with open('spec/fixtures/data_page.html') as stream:
    DATA_PAGE = stream.read()

DOCUMENT_URL = '/wps/wcm/connect/ac73cb13-1b12-422d-9bf8-7942b99c0c7b/DOC_CAN_ADJ2014-545517.xml?MOD=AJPERES'

with open('spec/fixtures/last_page.html') as stream:
    LAST_PAGE = stream.read()

LAST_DETAIL_URLS = [
    '/wps/portal/!ut/p/b1/hc5BDoIwFATQs3AA84cWWliSUtoaFaMVpRvDwhgThY3x_CLRpfp3k7zJfArUxgyxZBAZpwOFvntczt39MvTd9ZWDOBqIRLmcA6XO4Wo_3ygvUZfpCNoR4MsVmPqJrpWqLAP0koNZaTLNFbD-9H-AP_t7ChNJuUqaebMWW2cAZ6tysYtTGCbe4MeLKzvcTtSOTH6d8pI8tbZ0im7hWuVuZs5FFD0B6ZsPCA!!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=109688/250463671592/-/',
    '/wps/portal/!ut/p/b1/hc5BDoIwFATQs3AA84cWWliSUtoaFaMVpRvDwhgThY3x_CLRpfp3k7zJfArUxgyxZBAZpwOFvntczt39MvTd9ZWDOBqIRLmcA6XO4Wo_3ygvUZfpCNoR4MsVmPqJrpWqLAP0koNZaTLNFbD-9H-AP_t7ChNJuUqaebMWW2cAZ6tysYtTGCbe4MeLKzvcTtSOTH6d8pI8tbZ0im7hWuVuZs5FFD0B6ZsPCA!!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=63442/250463671592/-/',
    '/wps/portal/!ut/p/b1/hc5BDoIwFATQs3AA84cWWliSUtoaFaMVpRvDwhgThY3x_CLRpfp3k7zJfArUxgyxZBAZpwOFvntczt39MvTd9ZWDOBqIRLmcA6XO4Wo_3ygvUZfpCNoR4MsVmPqJrpWqLAP0koNZaTLNFbD-9H-AP_t7ChNJuUqaebMWW2cAZ6tysYtTGCbe4MeLKzvcTtSOTH6d8pI8tbZ0im7hWuVuZs5FFD0B6ZsPCA!!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=118590/250463671592/-/',
    '/wps/portal/!ut/p/b1/hc5BDoIwFATQs3AA84cWWliSUtoaFaMVpRvDwhgThY3x_CLRpfp3k7zJfArUxgyxZBAZpwOFvntczt39MvTd9ZWDOBqIRLmcA6XO4Wo_3ygvUZfpCNoR4MsVmPqJrpWqLAP0koNZaTLNFbD-9H-AP_t7ChNJuUqaebMWW2cAZ6tysYtTGCbe4MeLKzvcTtSOTH6d8pI8tbZ0im7hWuVuZs5FFD0B6ZsPCA!!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=110004/250463671592/-/',
    '/wps/portal/!ut/p/b1/hc5BDoIwFATQs3AA84cWWliSUtoaFaMVpRvDwhgThY3x_CLRpfp3k7zJfArUxgyxZBAZpwOFvntczt39MvTd9ZWDOBqIRLmcA6XO4Wo_3ygvUZfpCNoR4MsVmPqJrpWqLAP0koNZaTLNFbD-9H-AP_t7ChNJuUqaebMWW2cAZ6tysYtTGCbe4MeLKzvcTtSOTH6d8pI8tbZ0im7hWuVuZs5FFD0B6ZsPCA!!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=51249/250463671592/-/',
    '/wps/portal/!ut/p/b1/hc5BDoIwFATQs3AA84cWWliSUtoaFaMVpRvDwhgThY3x_CLRpfp3k7zJfArUxgyxZBAZpwOFvntczt39MvTd9ZWDOBqIRLmcA6XO4Wo_3ygvUZfpCNoR4MsVmPqJrpWqLAP0koNZaTLNFbD-9H-AP_t7ChNJuUqaebMWW2cAZ6tysYtTGCbe4MeLKzvcTtSOTH6d8pI8tbZ0im7hWuVuZs5FFD0B6ZsPCA!!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=72129/250463671593/-/',
    '/wps/portal/!ut/p/b1/hc5BDoIwFATQs3AA84cWWliSUtoaFaMVpRvDwhgThY3x_CLRpfp3k7zJfArUxgyxZBAZpwOFvntczt39MvTd9ZWDOBqIRLmcA6XO4Wo_3ygvUZfpCNoR4MsVmPqJrpWqLAP0koNZaTLNFbD-9H-AP_t7ChNJuUqaebMWW2cAZ6tysYtTGCbe4MeLKzvcTtSOTH6d8pI8tbZ0im7hWuVuZs5FFD0B6ZsPCA!!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=42476/250463671593/-/',
    '/wps/portal/!ut/p/b1/hc5BDoIwFATQs3AA84cWWliSUtoaFaMVpRvDwhgThY3x_CLRpfp3k7zJfArUxgyxZBAZpwOFvntczt39MvTd9ZWDOBqIRLmcA6XO4Wo_3ygvUZfpCNoR4MsVmPqJrpWqLAP0koNZaTLNFbD-9H-AP_t7ChNJuUqaebMWW2cAZ6tysYtTGCbe4MeLKzvcTtSOTH6d8pI8tbZ0im7hWuVuZs5FFD0B6ZsPCA!!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=52070/250463671593/-/',
    '/wps/portal/!ut/p/b1/hc5BDoIwFATQs3AA84cWWliSUtoaFaMVpRvDwhgThY3x_CLRpfp3k7zJfArUxgyxZBAZpwOFvntczt39MvTd9ZWDOBqIRLmcA6XO4Wo_3ygvUZfpCNoR4MsVmPqJrpWqLAP0koNZaTLNFbD-9H-AP_t7ChNJuUqaebMWW2cAZ6tysYtTGCbe4MeLKzvcTtSOTH6d8pI8tbZ0im7hWuVuZs5FFD0B6ZsPCA!!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_G064CI9300DE90IOTJRCT70OT7/act/id=0/p=ACTION_NAME_PARAM=SourceAction/p=idLicitacion=90791/250463671593/-/'
]
