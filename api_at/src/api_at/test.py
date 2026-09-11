#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from . import system
from . import exceptions
from . import mocks


class APIATTest(colony.Test):
    """
    The API AT infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (APIATBaseTestCase,)

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class APIATBaseTestCase(colony.ColonyTestCase):

    @staticmethod
    def get_description():
        return "API AT Base test case"

    def test_validate_credentials(self):
        """
        Tests that `validate_credentials` always returns `True` (API compatibility mock).
        """

        client = system.ATClient(plugin=None, certificate_info=None)
        result = client.validate_credentials()
        self.assertEqual(result, True)

    def test_get_certificate_not_before_utc_time(self):
        """
        Tests parsing of `UTCTime` format (`YYMMDDhhmmssZ`) for `not_before`.

        `UTCTime` uses 2-digit year for dates 1950-2049.
        """

        # creates an `ATClient` with mock `certificate_info` using `UTCTime` format
        client = system.ATClient(
            plugin=None,
            certificate_info={"not_before": "250415073858Z"},
        )

        # retrieves the timestamp and verifies it matches expected value
        # 2025-04-15 07:38:58 UTC = 1744702738
        not_before = client.get_certificate_not_before()
        self.assertEqual(not_before, 1744702738)

    def test_get_certificate_not_before_generalized_time(self):
        """
        Tests parsing of `GeneralizedTime` format (`YYYYMMDDhhmmssZ`) for `not_before`.

        `GeneralizedTime` uses 4-digit year for dates outside 1950-2049.
        """

        # creates an `ATClient` with mock `certificate_info` using `GeneralizedTime` format
        client = system.ATClient(
            plugin=None,
            certificate_info={"not_before": "20500415073858Z"},
        )

        # retrieves the timestamp and verifies it matches expected value
        # 2050-04-15 07:38:58 UTC = 2533621138
        not_before = client.get_certificate_not_before()
        self.assertEqual(not_before, 2533621138)

    def test_get_certificate_not_before_none(self):
        """
        Tests that `get_certificate_not_before` returns `None` when `certificate_info` is `None`.
        """

        client = system.ATClient(plugin=None, certificate_info=None)
        not_before = client.get_certificate_not_before()
        self.assertEqual(not_before, None)

    def test_get_certificate_not_before_missing_field(self):
        """
        Tests that `get_certificate_not_before` returns `None` when `not_before` field is missing.
        """

        client = system.ATClient(plugin=None, certificate_info={})
        not_before = client.get_certificate_not_before()
        self.assertEqual(not_before, None)

    def test_get_certificate_not_after_utc_time(self):
        """
        Tests parsing of `UTCTime` format (`YYMMDDhhmmssZ`) for `not_after`.

        `UTCTime` uses 2-digit year for dates 1950-2049.
        """

        # creates an `ATClient` with mock `certificate_info` using `UTCTime` format
        client = system.ATClient(
            plugin=None,
            certificate_info={"not_after": "270415074858Z"},
        )

        # retrieves the timestamp and verifies it matches expected value
        # 2027-04-15 07:48:58 UTC = 1807775338
        not_after = client.get_certificate_not_after()
        self.assertEqual(not_after, 1807775338)

    def test_get_certificate_not_after_generalized_time(self):
        """
        Tests parsing of `GeneralizedTime` format (`YYYYMMDDhhmmssZ`) for `not_after`.

        `GeneralizedTime` uses 4-digit year for dates outside 1950-2049.
        """

        # creates an `ATClient` with mock `certificate_info` using `GeneralizedTime` format
        client = system.ATClient(
            plugin=None,
            certificate_info={"not_after": "20510415074858Z"},
        )

        # retrieves the timestamp and verifies it matches expected value
        # 2051-04-15 07:48:58 UTC = 2565157738
        not_after = client.get_certificate_not_after()
        self.assertEqual(not_after, 2565157738)

    def test_get_certificate_not_after_none(self):
        """
        Tests that `get_certificate_not_after` returns `None` when `certificate_info` is `None`.
        """

        client = system.ATClient(plugin=None, certificate_info=None)
        not_after = client.get_certificate_not_after()
        self.assertEqual(not_after, None)

    def test_get_certificate_not_after_missing_field(self):
        """
        Tests that `get_certificate_not_after` returns `None` when `not_after` field is missing.
        """

        client = system.ATClient(plugin=None, certificate_info={})
        not_after = client.get_certificate_not_after()
        self.assertEqual(not_after, None)

    def test_get_certificate_common_name(self):
        """
        Tests that `get_certificate_common_name` correctly extracts the CN from subject.

        The subject is a list of RDNs where each RDN has the structure:
        `SET { SEQUENCE { OID, value } }`
        The Common Name OID is `2.5.4.3`.
        """

        # creates a mock subject structure matching the format from `load_certificate_der`
        subject = [
            {"value": [{"value": [{"value": (2, 5, 4, 6)}, {"value": "PT"}]}]},
            {
                "value": [
                    {"value": [{"value": (2, 5, 4, 3)}, {"value": "Test Common Name"}]}
                ]
            },
        ]

        client = system.ATClient(plugin=None, certificate_info={"subject": subject})
        common_name = client.get_certificate_common_name()
        self.assertEqual(common_name, "Test Common Name")

    def test_get_certificate_common_name_none(self):
        """
        Tests that `get_certificate_common_name` returns `None` when `certificate_info` is `None`.
        """

        client = system.ATClient(plugin=None, certificate_info=None)
        common_name = client.get_certificate_common_name()
        self.assertEqual(common_name, None)

    def test_get_certificate_common_name_missing_subject(self):
        """
        Tests that `get_certificate_common_name` returns `None` when `subject` field is missing.
        """

        client = system.ATClient(plugin=None, certificate_info={})
        common_name = client.get_certificate_common_name()
        self.assertEqual(common_name, None)

    def test_get_certificate_common_name_not_found(self):
        """
        Tests that `get_certificate_common_name` returns `None` when CN OID is not in subject.
        """

        # creates a mock subject without Common Name (OID `2.5.4.3`)
        subject = [
            {"value": [{"value": [{"value": (2, 5, 4, 6)}, {"value": "PT"}]}]},
            {"value": [{"value": [{"value": (2, 5, 4, 10)}, {"value": "Some Org"}]}]},
        ]

        client = system.ATClient(plugin=None, certificate_info={"subject": subject})
        common_name = client.get_certificate_common_name()
        self.assertEqual(common_name, None)

    def test_get_server_name_test_mode(self):
        """
        Tests that `get_server_name` returns `"test"` when `test_mode` is `True`.
        """

        client = system.ATClient(plugin=None, certificate_info=None, test_mode=True)
        server_name = client.get_server_name()
        self.assertEqual(server_name, "test")

    def test_get_server_name_production_mode(self):
        """
        Tests that `get_server_name` returns `"production"` when `test_mode` is `False`.
        """

        client = system.ATClient(plugin=None, certificate_info=None, test_mode=False)
        server_name = client.get_server_name()
        self.assertEqual(server_name, "production")

    def test_submit_document_logging(self):
        """
        Tests that `_submit_document` logs the target URL of the submission
        and the response received from the AT.
        """

        # creates the XML response of a successful submission, the one that
        # carries neither a fault nor a return message
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body />
        </S:Envelope>"""

        plugin = mocks.MockPlugin()
        http_client = mocks.MockHTTPClient(received_message=xml_response)
        client = system.ATClient(
            plugin=plugin,
            ssl_plugin=mocks.MockSSLPlugin(),
            client_http_plugin=mocks.MockClientHTTPPlugin(http_client=http_client),
            test_mode=True,
        )

        data = client._submit_document("https://at.example.com/ws", "<payload />")
        self.assertEqual(data, xml_response)
        self.assertEqual(
            plugin.messages[0],
            "Submitting AT document to 'https://at.example.com/ws' "
            "using the version 1 of the specification",
        )
        self.assertEqual(
            plugin.messages[-1],
            "Received AT response with the status code 200 and the data: %s"
            % xml_response,
        )

    def test_submit_document_logging_error_response(self):
        """
        Tests that `_submit_document` logs the response of a rejected
        submission before the error is raised.
        """

        # creates the XML response of a submission rejected by the AT with
        # an authentication error, the case that must remain diagnosable
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <RegisterInvoiceResponse>
                    <codResultOper>40001</codResultOper>
                    <msgResultOper>Credenciais invalidas</msgResultOper>
                </RegisterInvoiceResponse>
            </S:Body>
        </S:Envelope>"""

        plugin = mocks.MockPlugin()
        http_client = mocks.MockHTTPClient(received_message=xml_response)
        client = system.ATClient(
            plugin=plugin,
            ssl_plugin=mocks.MockSSLPlugin(),
            client_http_plugin=mocks.MockClientHTTPPlugin(http_client=http_client),
            test_mode=True,
        )

        raised = False
        try:
            client._submit_document(
                "https://at.example.com/ws", "<payload />", version=2
            )
        except exceptions.ATAPIError as e:
            raised = True
            self.assertEqual(e.error_code, 40001)
        self.assertEqual(raised, True)
        self.assertEqual(
            plugin.messages[-1],
            "Received AT response with the status code 200 and the data: %s"
            % xml_response,
        )

    def test_submit_document_invalid_version(self):
        """
        Tests that `_submit_document` raises `ATVersionError` for an
        unsupported version of the specification.
        """

        plugin = mocks.MockPlugin()
        client = system.ATClient(
            plugin=plugin,
            ssl_plugin=mocks.MockSSLPlugin(),
            client_http_plugin=mocks.MockClientHTTPPlugin(),
            test_mode=True,
        )

        raised = False
        try:
            client._submit_document(
                "https://at.example.com/ws", "<payload />", version=3
            )
        except exceptions.ATVersionError:
            raised = True
        self.assertEqual(raised, True)

        # no message should have been logged as the failure happens before
        # the submission is performed
        self.assertEqual(plugin.messages, [])

    def test_submit_document_invalid_http_code(self):
        """
        Tests that `_submit_document` raises `ATAPIError` when the HTTP
        status code of the response is not a successful one.
        """

        # creates an XML response free of AT errors, so that the failure
        # comes exclusively from the HTTP status code
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body />
        </S:Envelope>"""

        plugin = mocks.MockPlugin()
        http_client = mocks.MockHTTPClient(
            received_message=xml_response, status_code=500
        )
        client = system.ATClient(
            plugin=plugin,
            ssl_plugin=mocks.MockSSLPlugin(),
            client_http_plugin=mocks.MockClientHTTPPlugin(http_client=http_client),
            test_mode=True,
        )

        raised = False
        try:
            client._submit_document("https://at.example.com/ws", "<payload />")
        except exceptions.ATAPIError as e:
            raised = True
            self.assertEqual(e.error_code, 500)
        self.assertEqual(raised, True)
        self.assertEqual(
            plugin.messages[-1],
            "Received AT response with the status code 500 and the data: %s"
            % xml_response,
        )

    def test_submit_document_check_errors(self):
        """
        Tests that `_submit_document` uses the provided `check_errors`
        callable instead of the default one of the version.
        """

        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body />
        </S:Envelope>"""

        plugin = mocks.MockPlugin()
        http_client = mocks.MockHTTPClient(received_message=xml_response)
        client = system.ATClient(
            plugin=plugin,
            ssl_plugin=mocks.MockSSLPlugin(),
            client_http_plugin=mocks.MockClientHTTPPlugin(http_client=http_client),
            test_mode=True,
        )

        checked = []
        client._submit_document(
            "https://at.example.com/ws",
            "<payload />",
            check_errors=lambda data: checked.append(data),
        )
        self.assertEqual(checked, [xml_response])

    def test_submit_document_invalid_http_code_non_xml(self):
        """
        Tests that `_submit_document` falls back to the raw data as the
        details of the error when the response is not valid XML.
        """

        # creates a response that cannot be parsed as XML, the shape of a
        # plain text error returned by an intermediate gateway that fails
        # before the request reaches the AT
        data_response = "504 Gateway Time-out"

        plugin = mocks.MockPlugin()
        http_client = mocks.MockHTTPClient(
            received_message=data_response, status_code=504
        )
        client = system.ATClient(
            plugin=plugin,
            ssl_plugin=mocks.MockSSLPlugin(),
            client_http_plugin=mocks.MockClientHTTPPlugin(http_client=http_client),
            test_mode=True,
        )

        raised = False
        try:
            client._submit_document(
                "https://at.example.com/ws",
                "<payload />",
                check_errors=lambda data: None,
            )
        except exceptions.ATAPIError as e:
            raised = True
            self.assertEqual(e.error_code, 504)
            self.assertEqual(e.details, data_response)
        self.assertEqual(raised, True)

    def test_submit_document_reuses_http_client(self):
        """
        Tests that `_submit_document` reuses the HTTP client across
        submissions instead of creating one per operation.
        """

        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body />
        </S:Envelope>"""

        plugin = mocks.MockPlugin()
        http_client = mocks.MockHTTPClient(received_message=xml_response)
        client = system.ATClient(
            plugin=plugin,
            ssl_plugin=mocks.MockSSLPlugin(),
            client_http_plugin=mocks.MockClientHTTPPlugin(http_client=http_client),
            test_mode=True,
        )

        client._submit_document("https://at.example.com/ws", "<payload />")
        client._submit_document("https://at.example.com/ws", "<payload />")

        # both submissions must have been performed, while the parameters
        # of the client creation are only logged once (a single client)
        self.assertEqual(len(http_client.requests), 2)
        created = [
            m for m in plugin.messages if m.startswith("Submitting AT information")
        ]
        self.assertEqual(len(created), 1)

    def test_get_at_document_id(self):
        """
        Tests that `get_at_document_id` correctly extracts `ATDocCodeID` from XML response.
        """

        # creates a sample XML response with a document ID
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <RegisterInvoiceResponse>
                    <ATDocCodeID>AT123456789</ATDocCodeID>
                    <ReturnCode>0</ReturnCode>
                    <ReturnMessage>Success</ReturnMessage>
                </RegisterInvoiceResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        doc_id = client.get_at_document_id(xml_response)
        self.assertEqual(doc_id, "AT123456789")

    def test_get_at_document_id_not_found(self):
        """
        Tests that `get_at_document_id` returns `None` when `ATDocCodeID` is not present.
        """

        # creates a sample XML response without `ATDocCodeID`
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <RegisterInvoiceResponse>
                    <ReturnCode>0</ReturnCode>
                    <ReturnMessage>Success</ReturnMessage>
                </RegisterInvoiceResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        doc_id = client.get_at_document_id(xml_response)
        self.assertEqual(doc_id, None)

    def test_get_at_invoices(self):
        """
        Tests that `get_at_invoices` correctly parses a SOAP response with invoice data.
        """

        # creates a sample XML response matching the AT invoice query format
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <InvoicesResponse>
                    <InvoicesList>
                        <Invoice>
                            <InvoiceNo>FT 2026/1</InvoiceNo>
                            <ATCUD>AAAA-1234</ATCUD>
                            <GrossTotal>100.00</GrossTotal>
                        </Invoice>
                    </InvoicesList>
                    <estadoExecucao>
                        <codResultOper>20000</codResultOper>
                        <msgResultOper>Sucesso</msgResultOper>
                    </estadoExecucao>
                </InvoicesResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        invoices = client.get_at_invoices(xml_response)
        self.assertNotEqual(invoices, None)

    def test_get_at_invoices_empty_response(self):
        """
        Tests that `get_at_invoices` returns `None` when `InvoicesList` is not present.
        """

        # creates a sample XML response without `InvoicesList`
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <InvoicesResponse>
                    <estadoExecucao>
                        <codResultOper>20000</codResultOper>
                        <msgResultOper>Sucesso</msgResultOper>
                    </estadoExecucao>
                </InvoicesResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        invoices = client.get_at_invoices(xml_response)
        self.assertEqual(invoices, None)

    def test_get_at_invoices_custom_tag(self):
        """
        Tests that `get_at_invoices` correctly uses a custom `tag_name` for extraction.
        """

        # creates a sample XML response with a custom tag name
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <InvoicesResponse>
                    <CustomInvoiceList>
                        <Invoice>
                            <InvoiceNo>FT 2026/2</InvoiceNo>
                            <ATCUD>BBBB-5678</ATCUD>
                        </Invoice>
                    </CustomInvoiceList>
                </InvoicesResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        invoices = client.get_at_invoices(xml_response, tag_name="CustomInvoiceList")
        self.assertNotEqual(invoices, None)

    def test_get_at_invoices_multiple_invoices(self):
        """
        Tests that `get_at_invoices` correctly parses multiple invoices.
        """

        # creates a sample XML response with multiple invoices
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <InvoicesResponse>
                    <InvoicesList>
                        <Invoice>
                            <InvoiceNo>FT 2026/1</InvoiceNo>
                            <ATCUD>AAAA-0001</ATCUD>
                            <GrossTotal>100.00</GrossTotal>
                        </Invoice>
                        <Invoice>
                            <InvoiceNo>FT 2026/2</InvoiceNo>
                            <ATCUD>AAAA-0002</ATCUD>
                            <GrossTotal>200.00</GrossTotal>
                        </Invoice>
                        <Invoice>
                            <InvoiceNo>FT 2026/3</InvoiceNo>
                            <ATCUD>AAAA-0003</ATCUD>
                            <GrossTotal>300.00</GrossTotal>
                        </Invoice>
                    </InvoicesList>
                </InvoicesResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        invoices = client.get_at_invoices(xml_response)
        self.assertNotEqual(invoices, None)

    def test_get_at_series(self):
        """
        Tests that `get_at_series` correctly parses series response from XML.
        """

        # creates a sample XML response with series data
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <registarSerieResp>
                    <codValidacaoSerie>ABCD1234</codValidacaoSerie>
                    <serie>FT</serie>
                    <tipoSerie>N</tipoSerie>
                    <dataInicioPrevUtiliz>2026-01-01</dataInicioPrevUtiliz>
                </registarSerieResp>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        series = client.get_at_series(xml_response)
        self.assertNotEqual(series, None)

    def test_get_at_series_not_found(self):
        """
        Tests that `get_at_series` returns `None` when the series tag is not present.
        """

        # creates a sample XML response without the series tag
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <SomeOtherResponse>
                    <data>value</data>
                </SomeOtherResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        series = client.get_at_series(xml_response)
        self.assertEqual(series, None)

    def test_get_at_series_custom_tag(self):
        """
        Tests that `get_at_series` correctly uses a custom `tag_name` for extraction.
        """

        # creates a sample XML response with a custom series tag
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <consultarSeriesResp>
                    <serie>NC</serie>
                    <tipoSerie>N</tipoSerie>
                </consultarSeriesResp>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        series = client.get_at_series(xml_response, tag_name="consultarSeriesResp")
        self.assertNotEqual(series, None)

    def test_check_at_errors_v1_success(self):
        """
        Tests that `_check_at_errors_v1` does not raise for success response (code `0`).
        """

        # creates a sample XML response with success code
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <RegisterInvoiceResponse>
                    <ReturnCode>0</ReturnCode>
                    <ReturnMessage>Sucesso</ReturnMessage>
                </RegisterInvoiceResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        # should not raise any exception
        client._check_at_errors_v1(xml_response)

    def test_check_at_errors_v1_error(self):
        """
        Tests that `_check_at_errors_v1` raises `ATAPIError` for error response.
        """

        # creates a sample XML response with error code
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <RegisterInvoiceResponse>
                    <ReturnCode>1001</ReturnCode>
                    <ReturnMessage>Documento invalido</ReturnMessage>
                </RegisterInvoiceResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        raised = False
        try:
            client._check_at_errors_v1(xml_response)
        except exceptions.ATAPIError as e:
            raised = True
            self.assertEqual(e.error_code, 1001)
        self.assertEqual(raised, True)

    def test_check_at_errors_v1_fault(self):
        """
        Tests that `_check_at_errors_v1` raises `ATAPIError` for SOAP fault response.
        """

        # creates a sample XML response with SOAP fault
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <S:Fault>
                    <faultcode>S:Server</faultcode>
                    <faultstring>Internal Server Error</faultstring>
                </S:Fault>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        raised = False
        try:
            client._check_at_errors_v1(xml_response)
        except exceptions.ATAPIError:
            raised = True
        self.assertEqual(raised, True)

    def test_check_at_errors_v1_no_error(self):
        """
        Tests that `_check_at_errors_v1` does not raise when no error elements present.
        """

        # creates a sample XML response without error elements
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <RegisterInvoiceResponse>
                    <ATDocCodeID>AT123456</ATDocCodeID>
                </RegisterInvoiceResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        # should not raise any exception
        client._check_at_errors_v1(xml_response)

    def test_check_at_errors_v1_custom_tags(self):
        """
        Tests that `_check_at_errors_v1` works with custom tag names (V2 style tags).
        """

        # creates a sample XML response with custom tags and success code
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <SubmitInvoiceResponse>
                    <CodigoResposta>0</CodigoResposta>
                    <Mensagem>Operacao efectuada com sucesso</Mensagem>
                </SubmitInvoiceResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        # should not raise any exception
        client._check_at_errors_v1(
            xml_response, code_tag="CodigoResposta", message_tag="Mensagem"
        )

    def test_check_at_errors_v2_success(self):
        """
        Tests that `_check_at_errors_v2` does not raise for success response (`2xxxx` codes).
        """

        # creates a sample XML response with success code (`20000`)
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <QueryInvoicesResponse>
                    <estadoExecucao>
                        <codResultOper>20000</codResultOper>
                        <msgResultOper>Sucesso</msgResultOper>
                    </estadoExecucao>
                </QueryInvoicesResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        # should not raise any exception
        client._check_at_errors_v2(xml_response)

    def test_check_at_errors_v2_error(self):
        """
        Tests that `_check_at_errors_v2` raises `ATAPIError` for error response (non-`2xxxx`).
        """

        # creates a sample XML response with error code (`3xxxx` = validation error)
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <QueryInvoicesResponse>
                    <estadoExecucao>
                        <codResultOper>30001</codResultOper>
                        <msgResultOper>Parametros de pesquisa invalidos</msgResultOper>
                    </estadoExecucao>
                </QueryInvoicesResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        raised = False
        try:
            client._check_at_errors_v2(xml_response)
        except exceptions.ATAPIError as e:
            raised = True
            self.assertEqual(e.error_code, 30001)
        self.assertEqual(raised, True)

    def test_check_at_errors_v2_auth_error(self):
        """
        Tests that `_check_at_errors_v2` raises `ATAPIError` for auth error (`4xxxx` codes).
        """

        # creates a sample XML response with authentication error code
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <QueryInvoicesResponse>
                    <estadoExecucao>
                        <codResultOper>40001</codResultOper>
                        <msgResultOper>Credenciais invalidas</msgResultOper>
                    </estadoExecucao>
                </QueryInvoicesResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        raised = False
        try:
            client._check_at_errors_v2(xml_response)
        except exceptions.ATAPIError as e:
            raised = True
            self.assertEqual(e.error_code, 40001)
        self.assertEqual(raised, True)

    def test_check_at_errors_v2_system_error(self):
        """
        Tests that `_check_at_errors_v2` raises `ATAPIError` for system error (`5xxxx` codes).
        """

        # creates a sample XML response with system error code
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <QueryInvoicesResponse>
                    <estadoExecucao>
                        <codResultOper>50001</codResultOper>
                        <msgResultOper>Erro interno do sistema</msgResultOper>
                    </estadoExecucao>
                </QueryInvoicesResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        raised = False
        try:
            client._check_at_errors_v2(xml_response)
        except exceptions.ATAPIError as e:
            raised = True
            self.assertEqual(e.error_code, 50001)
        self.assertEqual(raised, True)

    def test_check_at_errors_v2_fault(self):
        """
        Tests that `_check_at_errors_v2` raises `ATAPIError` for a SOAP
        fault whose code is a qualified name instead of a number.
        """

        # creates a sample SOAP fault, the shape used by the AT to report
        # a failure of the WS-Security authentication
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <S:Fault>
                    <faultcode>S:Client</faultcode>
                    <faultstring>Invalid authentication credentials</faultstring>
                </S:Fault>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        raised = False
        try:
            client._check_at_errors_v2(xml_response)
        except exceptions.ATAPIError as e:
            raised = True
            self.assertEqual(e.error_code, "S:Client")
            self.assertEqual(e.message, "Invalid authentication credentials")
        self.assertEqual(raised, True)

    def test_check_at_errors_v2_fault_numeric(self):
        """
        Tests that `_check_at_errors_v2` raises `ATAPIError` for a SOAP
        fault whose code is a number, keeping it as an integer.
        """

        # creates a sample SOAP fault carrying a numeric code, the case
        # that must keep its original integer based handling
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <S:Fault>
                    <faultcode>40001</faultcode>
                    <faultstring>Credenciais invalidas</faultstring>
                </S:Fault>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        raised = False
        try:
            client._check_at_errors_v2(xml_response)
        except exceptions.ATAPIError as e:
            raised = True
            self.assertEqual(e.error_code, 40001)
        self.assertEqual(raised, True)

    def test_check_at_errors_v2_fault_numeric_success(self):
        """
        Tests that `_check_at_errors_v2` does not raise for a fault code
        that falls in the successful (`2xxxx`) range.
        """

        # creates a sample response whose fault code is a success one, the
        # boundary that the numeric handling must keep honouring
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <S:Fault>
                    <faultcode>20001</faultcode>
                    <faultstring>Operacao concluida</faultstring>
                </S:Fault>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        # should not raise any exception
        client._check_at_errors_v2(xml_response)

    def test_check_at_errors_v2_no_code(self):
        """
        Tests that `_check_at_errors_v2` does not raise when no result code present.
        """

        # creates a sample XML response without result code elements
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <SomeResponse>
                    <data>value</data>
                </SomeResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        # should not raise any exception
        client._check_at_errors_v2(xml_response)

    def test_check_at_errors_v2_custom_tags(self):
        """
        Tests that `_check_at_errors_v2` works with custom tag names.
        """

        # creates a sample XML response with custom tags and success code
        xml_response = """<?xml version="1.0" encoding="utf-8"?>
        <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
            <S:Body>
                <CustomResponse>
                    <customCode>21000</customCode>
                    <customMessage>Custom success</customMessage>
                </CustomResponse>
            </S:Body>
        </S:Envelope>"""

        client = system.ATClient(plugin=None, certificate_info=None)
        # should not raise any exception (`21000` starts with `2`, so it's success)
        client._check_at_errors_v2(
            xml_response, code_tag="customCode", message_tag="customMessage"
        )

    def test_check_at_errors_v2_multiple_success_codes(self):
        """
        Tests that `_check_at_errors_v2` recognizes various `2xxxx` codes as success.
        """

        # test various success codes in the `2xxxx` range
        success_codes = [20000, 20001, 21000, 22500, 29999]

        client = system.ATClient(plugin=None, certificate_info=None)

        for code in success_codes:
            xml_response = """<?xml version="1.0" encoding="utf-8"?>
            <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
                <S:Body>
                    <Response>
                        <codResultOper>%d</codResultOper>
                        <msgResultOper>Success</msgResultOper>
                    </Response>
                </S:Body>
            </S:Envelope>""" % code

            # should not raise any exception for success codes
            client._check_at_errors_v2(xml_response)
