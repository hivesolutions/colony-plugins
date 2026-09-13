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

import os
import sys
import hashlib
import logging
import threading

import colony

from . import mocks
from . import system

DSN = "https://public@o4507.ingest.us.sentry.io/4509"
""" The DSN used in the complete set of tests, considered
to be the canonical representation of a Sentry DSN """

CONFIG_NAMES = (
    "SENTRY_DSN",
    "SENTRY_ENVIRONMENT",
    "SENTRY_RELEASE",
    "SENTRY_SERVER_NAME",
    "SENTRY_LEVEL",
    "SENTRY_SAMPLE_RATE",
    "SENTRY_SEND_REQUEST",
    "SENTRY_SEND_QUERY",
    "SENTRY_SEND_USER",
    "SENTRY_BREADCRUMBS",
    "SENTRY_MAX_BREADCRUMBS",
    "SENTRY_IGNORED",
    "SENTRY_SESSION_ATTRIBUTES",
)
""" The complete set of configuration names used by the plugin,
unset at the end of each one of the test cases """


class DiagnosticsSentryTest(colony.Test):
    """
    The diagnostics Sentry infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            DiagnosticsSentryLifecycleTestCase,
            DiagnosticsSentryObserverTestCase,
            DiagnosticsSentryCaptureTestCase,
            DiagnosticsSentryContextTestCase,
            SentryHandlerTestCase,
            DiagnosticsSentryPluginTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class DiagnosticsSentryBaseTestCase(colony.ColonyTestCase):
    """
    The base test case for the diagnostics Sentry tests, responsible
    for the isolation of the configuration and of the global logger
    from the remaining test cases.
    """

    def setUp(self):
        colony.ColonyTestCase.setUp(self)
        self._systems = []

    def tearDown(self):
        for _system in self._systems:
            _system.stop()
        for name in CONFIG_NAMES:
            colony.conf_r(name)

    def _build_system(self, client=None, dsn=DSN, **config):
        if dsn:
            colony.conf_s("SENTRY_DSN", dsn)
        for name, value in colony.legacy.items(config):
            colony.conf_s("SENTRY_" + name.upper(), value)
        plugin = mocks.MockPlugin(client=client)
        _system = system.DiagnosticsSentry(plugin)
        self._systems.append(_system)
        return _system

    def _build_started(self, client=None, **config):
        client = client or mocks.MockSentryClient()
        _system = self._build_system(client=client, **config)
        _system.start()
        return _system


class DiagnosticsSentryLifecycleTestCase(DiagnosticsSentryBaseTestCase):
    @staticmethod
    def get_description():
        return "Diagnostics Sentry lifecycle test case"

    def test_configuration_defaults(self):
        _system = self._build_system()

        self.assertEqual(_system.dsn, DSN)
        self.assertEqual(_system.level, system.DEFAULT_LEVEL)
        self.assertEqual(_system.sample_rate, system.DEFAULT_SAMPLE_RATE)
        self.assertEqual(_system.send_request, False)
        self.assertEqual(_system.send_query, False)
        self.assertEqual(_system.send_user, True)
        self.assertEqual(_system.breadcrumbs, True)
        self.assertEqual(_system.max_breadcrumbs, system.DEFAULT_MAX_BREADCRUMBS)
        self.assertEqual(_system.ignored, system.DEFAULT_IGNORED)
        self.assertEqual(_system.session_attributes, system.DEFAULT_SESSION_ATTRIBUTES)

    def test_configuration_override(self):
        _system = self._build_system(
            level="WARNING",
            sample_rate=0.5,
            send_request=True,
            send_user=False,
            max_breadcrumbs=10,
            session_attributes="system_company;employee",
        )

        self.assertEqual(_system.level, "WARNING")
        self.assertEqual(_system.sample_rate, 0.5)
        self.assertEqual(_system.send_request, True)
        self.assertEqual(_system.send_user, False)
        self.assertEqual(_system.max_breadcrumbs, 10)
        self.assertEqual(_system.session_attributes, ["system_company", "employee"])

    def test_start(self):
        logger = logging.getLogger(system.DEFAULT_LOGGER)
        handlers = len(logger.handlers)

        _system = self._build_started()

        self.assertNotEqual(_system.client, None)
        self.assertEqual(len(logger.handlers), handlers + 1)
        self.assertEqual(_system.handler.level, logging.ERROR)

    def test_start_no_dsn(self):
        logger = logging.getLogger(system.DEFAULT_LOGGER)
        handlers = len(logger.handlers)

        _system = self._build_system(dsn=None)
        _system.start()

        self.assertEqual(_system.client, None)
        self.assertEqual(_system.handler, None)
        self.assertEqual(len(logger.handlers), handlers)

    def test_start_level(self):
        _system = self._build_started(level="warning")

        self.assertEqual(_system.handler.level, logging.WARNING)

    def test_stop(self):
        logger = logging.getLogger(system.DEFAULT_LOGGER)
        handlers = len(logger.handlers)
        client = mocks.MockSentryClient()

        _system = self._build_started(client=client)
        _system.stop()

        self.assertEqual(_system.client, None)
        self.assertEqual(_system.handler, None)
        self.assertEqual(client.closed, True)
        self.assertEqual(len(logger.handlers), handlers)

    def test_stop_not_started(self):
        _system = self._build_system(dsn=None)

        _system.stop()

        self.assertEqual(_system.client, None)

    def test_stop_unregisters_observers(self):
        _system = self._build_started()
        _system.stop()

        # notifies the events that the system was registered for, in case
        # the observers were not properly unregistered the notification
        # would reach an handler bound to an already stopped system
        colony.notify_g("request.begin", mocks.MockRequest())
        colony.notify_g("sql.executed", "SELECT 1", "sqlite", 1)

        self.assertEqual(_system.client, None)

    def test_create_client(self):
        client = mocks.MockSentryClient()
        _system = self._build_system(client=client)

        result = _system.create_client()

        attributes = _system.plugin.api_sentry_plugin.attributes
        self.assertEqual(result, client)
        self.assertEqual(attributes["dsn"], DSN)
        self.assertEqual(attributes["release"], "1.4.49")
        self.assertEqual(attributes["environment"], "cpython")
        self.assertEqual(attributes["in_app_paths"], ["/colony/plugins"])

    def test_create_client_explicit(self):
        _system = self._build_system(
            environment="production", release="1.49.2", server_name="omni-ldj"
        )

        _system.create_client()

        attributes = _system.plugin.api_sentry_plugin.attributes
        self.assertEqual(attributes["environment"], "production")
        self.assertEqual(attributes["release"], "1.49.2")
        self.assertEqual(attributes["server_name"], "omni-ldj")


class DiagnosticsSentryObserverTestCase(DiagnosticsSentryBaseTestCase):
    @staticmethod
    def get_description():
        return "Diagnostics Sentry observer test case"

    def test_request_begin(self):
        _system = self._build_started()
        request = mocks.MockRequest()

        _system.request_begin(request)

        context = _system._context()
        self.assertEqual(context.request, request)
        self.assertEqual(len(context.breadcrumbs), 0)
        self.assertNotEqual(context.begin, None)

    def test_request_begin_bounded_breadcrumbs(self):
        _system = self._build_started(max_breadcrumbs=2)
        _system.request_begin(mocks.MockRequest())

        _system.add_breadcrumb("query", "first")
        _system.add_breadcrumb("query", "second")
        _system.add_breadcrumb("query", "third")

        breadcrumbs = _system._context().breadcrumbs
        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs[0]["message"], "second")
        self.assertEqual(breadcrumbs[1]["message"], "third")

    def test_request_end(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        request = mocks.MockRequest()
        _system.request_begin(request)

        _system.request_end(request)

        self.assertEqual(len(client.events), 0)
        self.assertEqual(_system._context().request, None)
        self.assertEqual(_system._context().breadcrumbs, None)
        self.assertEqual(_system._context().begin, None)

    def test_request_end_exception(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        request = mocks.MockRequest()
        _system.request_begin(request)

        _system.request_end(request, RuntimeError("problem"))

        self.assertEqual(len(client.events), 1)
        self.assertEqual(_system._context().request, None)

    def test_request_end_exception_stacktrace(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        request = mocks.MockRequest()
        _system.request_begin(request)

        # the observers are notified while the handling of the exception is
        # still in progress, so the traceback must reach the event instead of
        # the failing location being lost for the main MVC path
        try:
            raise RuntimeError("problem")
        except RuntimeError as exception:
            _system.request_end(request, exception)

        self.assertEqual(client.events[0]["stacktrace"], dict(frames=["frame"]))

    def test_request_end_swallows_error(self):
        client = mocks.MockRaisingSentryClient()
        _system = self._build_started(client=client)
        request = mocks.MockRequest()
        _system.request_begin(request)

        _system.request_end(request, RuntimeError("problem"))

        self.assertEqual(_system._context().request, None)

    def test_request_exception(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        request = mocks.MockRequest()

        _system.request_exception(request, ValueError("invalid"), dict())

        self.assertEqual(len(client.events), 1)
        self.assertEqual(client.events[0]["exception"].args[0], "invalid")

    def test_request_exception_stacktrace(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)

        try:
            raise ValueError("invalid")
        except ValueError as exception:
            _system.request_exception(mocks.MockRequest(), exception, dict())

        self.assertEqual(client.events[0]["stacktrace"], dict(frames=["frame"]))

    def test_request_exception_swallows_error(self):
        client = mocks.MockRaisingSentryClient()
        _system = self._build_started(client=client)

        _system.request_exception(mocks.MockRequest(), ValueError("invalid"))

        self.assertEqual(len(client.events), 0)

    def test_resolve_traceback(self):
        _system = self._build_started()

        try:
            raise ValueError("invalid")
        except ValueError as exception:
            traceback_list = _system.resolve_traceback(exception)

        self.assertNotEqual(traceback_list, None)

    def test_resolve_traceback_execution_information(self):
        _system = self._build_started()

        # exercises the fallback to the execution information of the current
        # thread, used under Python 2 where the exceptions do not carry a
        # traceback of their own, note that the value held by the execution
        # information after the traceback of the exception has been cleared
        # is itself dependent on the version of the interpreter, so it's the
        # source of the fallback that is verified and not a fixed value
        try:
            raise ValueError("invalid")
        except ValueError as exception:
            exception.__traceback__ = None
            traceback_list = _system.resolve_traceback(exception)
            expected = sys.exc_info()[2]

        self.assertEqual(traceback_list, expected)

    def test_resolve_traceback_no_handling(self):
        _system = self._build_started()

        self.assertEqual(_system.resolve_traceback(ValueError("invalid")), None)

    def test_resolve_traceback_unrelated_exception(self):
        _system = self._build_started()

        # the execution information of the current thread is only usable in
        # case it refers the very same exception, as otherwise the traceback
        # of an unrelated failure would be reported
        try:
            raise ValueError("invalid")
        except ValueError:
            traceback_list = _system.resolve_traceback(RuntimeError("other"))

        self.assertEqual(traceback_list, None)

    def test_template_end(self):
        _system = self._build_started()
        _system.request_begin(mocks.MockRequest())

        _system.template_end(1, mocks.MockTemplateFile("index.html.tpl"))

        breadcrumb = _system._context().breadcrumbs[0]
        self.assertEqual(breadcrumb["category"], "template")
        self.assertEqual(breadcrumb["data"]["file_path"], "index.html.tpl")

    def test_template_end_no_file(self):
        _system = self._build_started()
        _system.request_begin(mocks.MockRequest())

        _system.template_end(1)

        breadcrumb = _system._context().breadcrumbs[0]
        self.assertEqual(breadcrumb["data"]["file_path"], None)

    def test_orm_begin(self):
        _system = self._build_started()
        _system.request_begin(mocks.MockRequest())

        _system.orm_begin(1, "find", dict())

        breadcrumb = _system._context().breadcrumbs[0]
        self.assertEqual(breadcrumb["category"], "orm")
        self.assertEqual(breadcrumb["message"], "find")

    def test_sql_executed(self):
        _system = self._build_started()
        _system.request_begin(mocks.MockRequest())

        # the engines embed the values of the entities in the query, so only
        # the operation of it may be recorded unless the text has been
        # explicitly requested by the operator
        _system.sql_executed("INSERT INTO omni_person VALUES ('secret')", "sqlite", 12)

        breadcrumb = _system._context().breadcrumbs[0]
        self.assertEqual(breadcrumb["category"], "query")
        self.assertEqual(breadcrumb["message"], "INSERT")
        self.assertEqual(breadcrumb["data"], dict(engine="sqlite", time=12))

    def test_sql_executed_send_query(self):
        _system = self._build_started(send_query=True)
        _system.request_begin(mocks.MockRequest())

        _system.sql_executed("SELECT 1", "sqlite", 12)

        self.assertEqual(_system._context().breadcrumbs[0]["message"], "SELECT 1")

    def test_sql_executed_bytes(self):
        _system = self._build_started(send_query=True)
        _system.request_begin(mocks.MockRequest())

        _system.sql_executed(b"SELECT 1", "sqlite", 12)

        self.assertEqual(_system._context().breadcrumbs[0]["message"], "SELECT 1")

    def test_sql_executed_undecodable_bytes(self):
        _system = self._build_started(send_query=True)
        _system.request_begin(mocks.MockRequest())

        # the engines provide the query encoded using the charset of the data
        # source, so an undecodable byte must never break the operation that
        # has just been performed, as the notification is a synchronous one
        _system.sql_executed(b"SELECT '\xe1\xe9'", "mysql", 12)

        message = _system._context().breadcrumbs[0]["message"]
        self.assertEqual(message.startswith("SELECT"), True)

    def test_sql_executed_truncated(self):
        _system = self._build_started(send_query=True)
        _system.request_begin(mocks.MockRequest())

        _system.sql_executed("A" * (system.MAX_QUERY_LENGTH + 100), "sqlite", 12)

        message = _system._context().breadcrumbs[0]["message"]
        self.assertEqual(len(message), system.MAX_QUERY_LENGTH)

    def test_query_operation(self):
        _system = self._build_started()

        self.assertEqual(_system.query_operation("select * from omni"), "SELECT")
        self.assertEqual(_system.query_operation("  UPDATE omni SET a = 1"), "UPDATE")
        self.assertEqual(_system.query_operation("DELETE"), "DELETE")

    def test_query_operation_empty(self):
        _system = self._build_started()

        self.assertEqual(_system.query_operation("   "), system.UNKNOWN_OPERATION)

    def test_add_breadcrumb_no_request(self):
        _system = self._build_started()

        _system.add_breadcrumb("query", "SELECT 1")

        self.assertEqual(_system._context().breadcrumbs, None)

    def test_add_breadcrumb_disabled(self):
        _system = self._build_started(breadcrumbs=False)
        _system.request_begin(mocks.MockRequest())

        _system.add_breadcrumb("query", "SELECT 1")

        self.assertEqual(len(_system._context().breadcrumbs), 0)


class DiagnosticsSentryCaptureTestCase(DiagnosticsSentryBaseTestCase):
    @staticmethod
    def get_description():
        return "Diagnostics Sentry capture test case"

    def test_capture_record(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        record = self._build_record("problem %s", ("here",))

        result = _system.capture_record(record)

        event = client.events[0]
        self.assertEqual(result, True)
        self.assertEqual(event["message"], "problem here")
        self.assertEqual(event["level"], "error")
        self.assertEqual(event["logger"], "colony")
        self.assertEqual(event["exception"], None)
        self.assertEqual(event["stacktrace"], None)

    def test_capture_record_exception(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)

        try:
            raise ValueError("invalid value")
        except ValueError:
            record = self._build_record("problem", exc_info=sys.exc_info())

        _system.capture_record(record)

        event = client.events[0]
        self.assertEqual(event["exception"].args[0], "invalid value")
        self.assertEqual(event["stacktrace"], dict(frames=["frame"]))

    def test_capture_record_level(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        record = self._build_record("problem", level=logging.CRITICAL)

        _system.capture_record(record)

        self.assertEqual(client.events[0]["level"], "fatal")

    def test_capture_record_unknown_level(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        record = self._build_record("problem")
        record.levelname = "VERBOSE"

        _system.capture_record(record)

        self.assertEqual(client.events[0]["level"], system.DEFAULT_EVENT_LEVEL)

    def test_capture_record_location(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        record = self._build_record("problem")
        record.funcName = "create"

        _system.capture_record(record)

        # the location of the logging call is the only reference to the code
        # that originated the record, as no stack trace is available for it
        extra = client.events[0]["extra"]
        self.assertEqual(extra, dict(path=__file__, lineno=1, function="create"))

    def test_capture_no_client(self):
        _system = self._build_system(dsn=None)

        result = _system.capture(exception=ValueError("invalid"))

        self.assertEqual(result, False)

    def test_capture_ignored(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client, ignored="ValueError")

        result = _system.capture(exception=ValueError("invalid"))

        self.assertEqual(result, False)
        self.assertEqual(len(client.events), 0)

    def test_capture_not_sampled(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client, sample_rate=0.0)

        result = _system.capture(exception=ValueError("invalid"))

        self.assertEqual(result, False)
        self.assertEqual(len(client.events), 0)

    def test_capture_not_accepted(self):
        client = mocks.MockSentryClient(accepted=False)
        _system = self._build_started(client=client)

        result = _system.capture(exception=ValueError("invalid"))

        self.assertEqual(result, False)
        self.assertEqual(len(client.events), 1)

    def test_capture_breadcrumbs(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        _system.request_begin(mocks.MockRequest())
        _system.sql_executed("SELECT 1", "sqlite", 12)

        _system.capture(exception=ValueError("invalid"))

        breadcrumbs = client.events[0]["breadcrumbs"]
        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs[0]["message"], "SELECT")

    def test_capture_context_request(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        request = mocks.MockRequest(path="omni/sales/1")
        _system.request_begin(request)

        _system.capture(exception=ValueError("invalid"))

        self.assertEqual(client.events[0]["request"]["url"], "omni/sales/1")
        self.assertEqual(client.events[0]["transaction"], "GET omni/sales/{id}")

    def test_capture_contexts(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)

        _system.capture(exception=ValueError("invalid"))

        event = client.events[0]
        self.assertEqual(event["contexts"]["colony"]["version"], "1.4.49")
        self.assertEqual(event["contexts"]["process"]["pid"], os.getpid())
        self.assertEqual("session" in event["contexts"], False)
        self.assertEqual(event["extra"], None)

    def test_capture_request_contexts(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        session = mocks.MockSession(dict(username="joamag"))
        _system.request_begin(mocks.MockRequest(session=session))

        _system.capture(exception=ValueError("invalid"))

        event = client.events[0]
        self.assertEqual(event["user"]["username"], "joamag")
        self.assertEqual(event["contexts"]["session"]["storage"], "redis")
        self.assertEqual(event["contexts"]["response"]["status_code"], 500)
        self.assertEqual(event["transaction"], "GET omni/sales")

    def test_capture_recursion_guard(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        context = _system._context()
        context.capturing = True

        result = _system.capture(exception=ValueError("invalid"))

        self.assertEqual(result, False)
        self.assertEqual(len(client.events), 0)

    def test_capture_releases_recursion_guard(self):
        client = mocks.MockRaisingSentryClient()
        _system = self._build_started(client=client)

        self.assertRaises(RuntimeError, _system.capture, ValueError("invalid"))
        self.assertEqual(_system._context().capturing, False)

    def test_capture_safe(self):
        client = mocks.MockRaisingSentryClient()
        _system = self._build_started(client=client)

        result = _system.capture_safe(exception=ValueError("invalid"))

        self.assertEqual(result, False)

    def _build_record(self, message, args=None, level=logging.ERROR, exc_info=None):
        return logging.LogRecord("colony", level, __file__, 1, message, args, exc_info)


class DiagnosticsSentryContextTestCase(DiagnosticsSentryBaseTestCase):
    @staticmethod
    def get_description():
        return "Diagnostics Sentry context test case"

    def test_build_request(self):
        _system = self._build_started()
        request = mocks.MockRequest(method="POST", path="omni/sales")

        data = _system.build_request(request)

        self.assertEqual(data, dict(method="POST", url="omni/sales"))

    def test_build_request_complete(self):
        _system = self._build_started()
        request = mocks.MockRequest(
            path="/adm/stores/1",
            headers={
                "Host": "omni.example.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Cookie": "sid=c2f1b9e7d4a6",
            },
            connection_address=("172.17.0.80", 52314),
            request=mocks.MockServiceRequest(
                environ=dict(SERVER_PROTOCOL="HTTP/1.1"), query_string="page=2"
            ),
        )

        data = _system.build_request(request)

        self.assertEqual(data["url"], "http://omni.example.com/adm/stores/1")
        self.assertEqual(data["headers"]["Cookie"], system.SCRUBBED_VALUE)
        self.assertEqual(data["env"]["REMOTE_ADDR"], "172.17.0.80")
        self.assertEqual(data["env"]["SERVER_PROTOCOL"], "HTTP/1.1")
        self.assertEqual("query_string" in data, False)
        self.assertEqual("data" in data, False)

    def test_build_request_none(self):
        _system = self._build_started()

        self.assertEqual(_system.build_request(None), None)

    def test_build_request_contents(self):
        _system = self._build_started(send_request=True)
        request = mocks.MockRequest(
            method="POST",
            attributes_map=dict(name="product", password="secret"),
            request=mocks.MockServiceRequest(query_string="page=2&token=secret"),
        )

        data = _system.build_request(request)

        self.assertEqual(data["data"]["name"], "product")
        self.assertEqual(data["data"]["password"], system.SCRUBBED_VALUE)
        self.assertEqual(
            data["query_string"], [["page", "2"], ["token", system.SCRUBBED_VALUE]]
        )

    def test_build_request_contents_get(self):
        _system = self._build_started(send_request=True)
        request = mocks.MockRequest(
            attributes_map=dict(page="2"),
            request=mocks.MockServiceRequest(query_string="page=2"),
        )

        # the attributes of a request using the get method are the values of its
        # query string, so they are reported as such and never as its contents
        data = _system.build_request(request)

        self.assertEqual(data["query_string"], [["page", "2"]])
        self.assertEqual("data" in data, False)

    def test_build_request_raising_request(self):
        _system = self._build_started(send_request=True)

        data = _system.build_request(mocks.MockRaisingRequest())

        self.assertEqual(data, dict(method="GET", url="omni/sales"))

    def test_resolve_url(self):
        _system = self._build_started()
        headers = {"Host": "omni.example.com"}
        request = mocks.MockRequest(path="/adm/stores/1", headers=headers)
        secure_request = mocks.MockRequest(
            path="/adm/stores/1", headers=headers, secure=True
        )

        self.assertEqual(
            _system.resolve_url(request), "http://omni.example.com/adm/stores/1"
        )
        self.assertEqual(
            _system.resolve_url(secure_request), "https://omni.example.com/adm/stores/1"
        )

    def test_resolve_url_forwarded(self):
        _system = self._build_started()
        request = mocks.MockRequest(
            path="/adm/stores/1",
            headers={
                "Host": "omni:8080",
                "X-Forwarded-Host": "omni.example.com, proxy.example.com",
                "X-Forwarded-Proto": "https, http",
            },
        )

        # a chain of proxies sets one value for each one of them, the first value
        # being the one of the request as received by the first of the proxies
        self.assertEqual(
            _system.resolve_url(request), "https://omni.example.com/adm/stores/1"
        )

    def test_resolve_url_case_insensitive(self):
        _system = self._build_started()
        request = mocks.MockCaseSensitiveRequest(
            path="/adm/stores/1",
            headers={
                "host": "omni:8080",
                "x-forwarded-host": "omni.example.com",
                "x-forwarded-proto": "https",
            },
        )

        # the requests of the HTTP service keep the names of the headers as they
        # have been received (eg: lower cased by a proxy), so the headers must be
        # resolved regardless of the case of their names
        self.assertEqual(
            _system.resolve_url(request), "https://omni.example.com/adm/stores/1"
        )

    def test_resolve_url_no_host(self):
        _system = self._build_started()
        request = mocks.MockRequest(path="/adm/stores/1")

        self.assertEqual(_system.resolve_url(request), "/adm/stores/1")

    def test_resolve_url_raising_request(self):
        _system = self._build_started()

        self.assertEqual(_system.resolve_url(mocks.MockRaisingRequest()), "omni/sales")

    def test_build_headers(self):
        _system = self._build_started()
        request = mocks.MockRequest(
            headers={
                "User-Agent": "Mozilla/5.0",
                "Authorization": "Basic dXNlcjpwYXNz",
                "Cookie": "sid=c2f1b9e7d4a6",
                "X-Forwarded-For": "203.0.113.7",
                "Referer": "https://omni.example.com/reset?token=secret",
            }
        )

        headers = _system.build_headers(request)

        self.assertEqual(headers["User-Agent"], "Mozilla/5.0")
        self.assertEqual(headers["Authorization"], system.SCRUBBED_VALUE)
        self.assertEqual(headers["Cookie"], system.SCRUBBED_VALUE)
        self.assertEqual(headers["X-Forwarded-For"], "203.0.113.7")
        self.assertEqual(headers["Referer"], "https://omni.example.com/reset")

    def test_build_headers_no_user(self):
        _system = self._build_started(send_user=False)
        request = mocks.MockRequest(
            headers={
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/json",
                "referer": "https://omni.example.com/reset?token=secret",
                "X-Forwarded-For": "203.0.113.7",
                "CF-Connecting-IP": "203.0.113.7",
                "True-Client-IP": "203.0.113.7",
                "X-Forwarded-Email": "joamag@example.com",
            }
        )

        # any header may carry the address or the identity of the client (eg: the
        # ones set by a proxy), so only the headers that identify neither the
        # client nor the user are sent in case the user is not to be sent
        headers = _system.build_headers(request)

        self.assertEqual(
            headers,
            {
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/json",
                "referer": "https://omni.example.com/reset",
            },
        )

    def test_build_headers_empty(self):
        _system = self._build_started()

        self.assertEqual(_system.build_headers(mocks.MockRequest()), None)

    def test_build_headers_raising_request(self):
        _system = self._build_started()

        self.assertEqual(_system.build_headers(mocks.MockRaisingRequest()), None)

    def test_build_env(self):
        _system = self._build_started()
        environ = dict(
            SERVER_NAME="omni", SERVER_PORT="8080", SERVER_PROTOCOL="HTTP/1.1"
        )
        request = mocks.MockRequest(
            connection_address=("172.17.0.80", 52314),
            server_software="netius/1.63.1",
            request=mocks.MockServiceRequest(environ=environ),
        )

        env = _system.build_env(request)

        self.assertEqual(
            env,
            dict(
                REMOTE_ADDR="172.17.0.80",
                REMOTE_PORT=52314,
                SERVER_SOFTWARE="netius/1.63.1",
                SERVER_NAME="omni",
                SERVER_PORT="8080",
                SERVER_PROTOCOL="HTTP/1.1",
            ),
        )

    def test_build_env_protocol_version(self):
        _system = self._build_started()
        request = mocks.MockRequest(
            request=mocks.MockServiceRequest(protocol_version="HTTP/1.0")
        )

        # the requests of the HTTP service have no WSGI environment, providing
        # the version of the protocol through the lower level request instead
        env = _system.build_env(request)

        self.assertEqual(env, dict(SERVER_PROTOCOL="HTTP/1.0"))

    def test_build_env_no_user(self):
        _system = self._build_started(send_user=False)
        request = mocks.MockRequest(connection_address=("203.0.113.7", 52314))

        # without a proxy the address of the connection is the one of the client
        # which is not to be sent in case the user is not to be sent
        self.assertEqual(_system.build_env(request), dict())

    def test_build_env_raising_request(self):
        _system = self._build_started()

        self.assertEqual(_system.build_env(mocks.MockRaisingRequest()), dict())

    def test_build_query_string(self):
        _system = self._build_started()
        request = mocks.MockRequest(
            request=mocks.MockServiceRequest(
                query_string="page=2&sort=&token=secret&page=3"
            )
        )

        pairs = _system.build_query_string(request)

        self.assertEqual(
            pairs,
            [
                ["page", "2"],
                ["page", "3"],
                ["sort", ""],
                ["token", system.SCRUBBED_VALUE],
            ],
        )

    def test_build_query_string_empty(self):
        _system = self._build_started()

        self.assertEqual(_system.build_query_string(mocks.MockRequest()), None)

    def test_build_query_string_raising_request(self):
        _system = self._build_started()
        request = mocks.MockRaisingRequest()

        self.assertEqual(_system.build_query_string(request), None)

    def test_build_user(self):
        _system = self._build_started()
        session = mocks.MockSession(dict(username="joamag"))
        request = mocks.MockRequest(address="192.168.1.100", session=session)

        user = _system.build_user(request)

        self.assertEqual(user, dict(ip_address="192.168.1.100", username="joamag"))

    def test_build_user_object(self):
        _system = self._build_started()
        user = mocks.MockEntity(
            object_id=5, username="joamag", email="joamag@example.com"
        )
        session = mocks.MockSession(dict(user=user, user_id=1))
        request = mocks.MockRequest(address="192.168.1.100", session=session)

        user = _system.build_user(request)

        self.assertEqual(
            user,
            dict(
                ip_address="192.168.1.100",
                id=1,
                username="joamag",
                email="joamag@example.com",
            ),
        )

    def test_build_user_lazy(self):
        _system = self._build_started()
        session = mocks.MockSession(dict(user=mocks.MockEntity(username="joamag")))
        request = mocks.MockRequest(address=None, session=session)

        # the values of the user object that are not loaded must not be retrieved,
        # as their loading would access the data source while the error is being
        # reported (eg: the email of a lazy loaded entity)
        user = _system.build_user(request)

        self.assertEqual(user, dict(username="joamag"))

    def test_build_user_disabled(self):
        _system = self._build_started(send_user=False)

        self.assertEqual(_system.build_user(mocks.MockRequest()), None)

    def test_build_user_none(self):
        _system = self._build_started()

        self.assertEqual(_system.build_user(None), None)

    def test_build_user_no_session(self):
        _system = self._build_started()
        request = mocks.MockRequest(session=None)

        user = _system.build_user(request)

        self.assertEqual(user, dict(ip_address="192.168.1.100"))

    def test_build_user_empty(self):
        _system = self._build_started()
        request = mocks.MockRequest(address=None, session=None)

        self.assertEqual(_system.build_user(request), None)

    def test_build_user_raising_request(self):
        _system = self._build_started()

        self.assertEqual(_system.build_user(mocks.MockRaisingRequest()), None)

    def test_resolve_user(self):
        _system = self._build_started()
        user = mocks.MockEntity(
            object_id=5, username="object", email="object@example.com"
        )
        session = mocks.MockSession(dict(username="session", account=user))

        # the values stored directly in the session take precedence over the ones
        # of the user object, which may be stored under any of the common names
        values = _system.resolve_user(session)

        self.assertEqual(
            values, dict(id=5, username="session", email="object@example.com")
        )

    def test_resolve_user_invalid(self):
        _system = self._build_started()
        user = mocks.MockEntity(email=["joamag@example.com"])
        session = mocks.MockSession(dict(username="", login=dict(), user=user))

        # neither the empty values nor the values that are not scalars identify
        # the user, as they would be meaningless in its description
        self.assertEqual(_system.resolve_user(session), dict())

    def test_build_tags(self):
        _system = self._build_started()
        request = mocks.MockRequest(method="POST", status_code=500)

        tags = _system.build_tags(request)

        self.assertEqual(tags, dict(method="POST", status_code="500"))

    def test_build_tags_device_type(self):
        _system = self._build_started()
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile"
        request = mocks.MockRequest(headers={"User-Agent": user_agent})

        tags = _system.build_tags(request)

        self.assertEqual(tags["device_type"], "mobile")

    def test_build_tags_none(self):
        _system = self._build_started()

        self.assertEqual(_system.build_tags(None), None)

    def test_build_tags_raising_request(self):
        _system = self._build_started()

        tags = _system.build_tags(mocks.MockRaisingRequest())

        self.assertEqual(tags, dict(method="GET"))

    def test_build_tags_exception(self):
        _system = self._build_started()
        request = mocks.MockRequest(status_code=200)

        # the observers are notified before the upper layers assign the status
        # code of the error response, so the one still set in the request must
        # not be the one reported for a request that failed
        tags = _system.build_tags(request, exception=RuntimeError("problem"))

        self.assertEqual(tags["status_code"], "500")

    def test_resolve_device_type(self):
        _system = self._build_started()
        user_agents = (
            ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://google.com/bot)", "bot"),
            ("Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) Mobile/15E148", "tablet"),
            ("Mozilla/5.0 (Linux; Android 14; SM-X710) Safari/537.36", "tablet"),
            ("Mozilla/5.0 (Linux; Android 14; Pixel 8) Mobile Safari/537.36", "mobile"),
            ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0", "desktop"),
        )

        # the bots and the tablets are verified before the remaining types, as
        # their user agents may also include the keywords of the mobile devices
        for user_agent, device_type in user_agents:
            request = mocks.MockRequest(headers={"User-Agent": user_agent})
            self.assertEqual(_system.resolve_device_type(request), device_type)

    def test_resolve_device_type_case_insensitive(self):
        _system = self._build_started()
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile"
        request = mocks.MockCaseSensitiveRequest(headers={"user-agent": user_agent})

        self.assertEqual(_system.resolve_device_type(request), "mobile")

    def test_resolve_device_type_none(self):
        _system = self._build_started()

        self.assertEqual(_system.resolve_device_type(mocks.MockRequest()), None)

    def test_resolve_device_type_raising_request(self):
        _system = self._build_started()
        request = mocks.MockRaisingRequest()

        self.assertEqual(_system.resolve_device_type(request), None)

    def test_resolve_status_code(self):
        _system = self._build_started()
        request = mocks.MockRequest(status_code=404)

        self.assertEqual(_system.resolve_status_code(request), 404)

    def test_resolve_status_code_exception(self):
        _system = self._build_started()
        request = mocks.MockRequest(status_code=200)

        exception = ValueError("not found")
        exception.status_code = 404

        self.assertEqual(_system.resolve_status_code(request, exception), 404)

    def test_resolve_status_code_exception_default(self):
        _system = self._build_started()
        request = mocks.MockRequest(status_code=200)

        self.assertEqual(
            _system.resolve_status_code(request, RuntimeError("problem")),
            system.ERROR_STATUS_CODE,
        )

    def test_resolve_status_code_exception_invalid(self):
        _system = self._build_started()
        request = mocks.MockRequest(status_code=200)

        exception = ValueError("broken")
        exception.status_code = "not a number"

        self.assertEqual(
            _system.resolve_status_code(request, exception), system.ERROR_STATUS_CODE
        )

    def test_resolve_status_code_raising_request(self):
        _system = self._build_started()

        self.assertEqual(_system.resolve_status_code(mocks.MockRaisingRequest()), None)

    def test_resolve_transaction(self):
        _system = self._build_started()
        request = mocks.MockRequest(path="/adm/stores/5857409334")
        json_request = mocks.MockRequest(method="POST", path="/sam/sales/6475.json")
        named_request = mocks.MockRequest(path="/adm/users/2fa/v2")

        self.assertEqual(_system.resolve_transaction(request), "GET /adm/stores/{id}")
        self.assertEqual(
            _system.resolve_transaction(json_request), "POST /sam/sales/{id}.json"
        )

        # only the segments that are complete numbers (optionally followed by an
        # extension) are identifiers, the ones merely starting with a number are
        # part of the name of the endpoint and must be kept as they are
        self.assertEqual(
            _system.resolve_transaction(named_request), "GET /adm/users/2fa/v2"
        )

    def test_resolve_transaction_none(self):
        _system = self._build_started()

        self.assertEqual(_system.resolve_transaction(None), None)

    def test_build_contexts(self):
        _system = self._build_system()

        contexts = _system.build_contexts()

        colony_context = contexts["colony"]
        self.assertEqual(colony_context["layout_mode"], "default")
        self.assertEqual(colony_context["run_mode"], "production")
        self.assertEqual(colony_context["start_timestamp"], 1789261658.0)
        self.assertEqual(colony_context["version"], "1.4.49")
        self.assertEqual(colony_context["release"], "100")
        self.assertEqual(colony_context["build"], "final")
        self.assertEqual(colony_context["release_date_time"], "13 Sep 2026 01:07:38")
        self.assertEqual(colony_context["environment"], "cpython")

        thread = threading.current_thread()
        process_context = contexts["process"]
        self.assertEqual(process_context["pid"], os.getpid())
        self.assertEqual(process_context["tid"], thread.ident)
        self.assertEqual(process_context["thread"], thread.name)

    def test_build_contexts_no_system_information(self):
        _system = self._build_system()
        _system.plugin.manager = mocks.MockUnstartedPluginManager()

        # an event may be originated before the plugin manager completes its
        # start, in which case the information about it is not yet available
        # and only the process is described in the contexts of the event
        contexts = _system.build_contexts()

        self.assertEqual(contexts["colony"]["version"], None)
        self.assertEqual(contexts["colony"]["run_mode"], None)
        self.assertEqual(contexts["process"]["pid"], os.getpid())

    def test_build_contexts_request(self):
        _system = self._build_system()
        request = mocks.MockRequest(session=mocks.MockSession(), status_code=404)

        contexts = _system.build_contexts(request)

        self.assertEqual(contexts["session"]["storage"], "redis")
        self.assertEqual(contexts["response"]["status_code"], 404)

    def test_build_session(self):
        _system = self._build_system()
        session = mocks.MockSession(dict(_locale="pt_pt", user_id=1, user_acl=dict()))
        request = mocks.MockRequest(session=session)

        context = _system.build_session(request)

        session_hash = hashlib.sha256(b"c2f1b9e7d4a6").hexdigest()
        self.assertEqual(context["storage"], "redis")
        self.assertEqual(context["id_hash"], session_hash[: system.SESSION_HASH_LENGTH])
        self.assertEqual(context["creation_time"], 1789261658.0)
        self.assertEqual(context["expire_time"], 1789265258.0)
        self.assertEqual(context["locale"], "pt_pt")
        self.assertEqual(context["attributes"], ["_locale", "user_acl", "user_id"])
        self.assertEqual("values" in context, False)

        # the identifier of the session is a credential that grants access to
        # it, so it must never be part of the description of the session, and
        # the type name is reserved by Sentry for the kind of the context
        self.assertEqual("c2f1b9e7d4a6" in str(context), False)
        self.assertEqual("type" in context, False)

    def test_build_session_values(self):
        _system = self._build_system(
            session_attributes="system_company;employee;store;secret_key"
        )
        company = mocks.MockEntity(object_id=1, name="Company", tax_number="PT123")
        session = mocks.MockSession(
            dict(system_company=company, employee="joamag", secret_key="abc")
        )
        request = mocks.MockRequest(session=session)

        # only the attributes that identify an object are reported for it, as the
        # remaining ones may hold personal or tax information, and the attributes
        # not defined in the session are not reported at all
        values = _system.build_session(request)["values"]

        self.assertEqual(values["system_company"], dict(object_id="1", name="Company"))
        self.assertEqual(values["employee"], "joamag")
        self.assertEqual(values["secret_key"], system.SCRUBBED_VALUE)
        self.assertEqual("store" in values, False)

    def test_build_session_values_empty(self):
        _system = self._build_system(session_attributes="employee;functional_unit")
        functional_unit = mocks.MockEntity(tax_number="PT123")
        session = mocks.MockSession(dict(employee="", functional_unit=functional_unit))
        request = mocks.MockRequest(session=session)

        # the values whose description is empty describe nothing, as it's the case
        # of an empty string or of an object with no identifying attribute loaded
        context = _system.build_session(request)

        self.assertEqual("values" in context, False)

    def test_build_session_values_no_user(self):
        _system = self._build_system(session_attributes="employee", send_user=False)
        session = mocks.MockSession(dict(employee="joamag"))
        request = mocks.MockRequest(session=session)

        self.assertEqual("values" in _system.build_session(request), False)

    def test_build_session_previous(self):
        _system = self._build_system()
        session = mocks.MockSession(name="CustomSession", session_id=None)
        del session.creation_time

        # the sessions of the previous versions have no creation time and the type
        # of an unknown class of session is described by the name of the class
        context = _system.build_session(mocks.MockRequest(session=session))

        self.assertEqual(context["storage"], "CustomSession")
        self.assertEqual(context["creation_time"], None)
        self.assertEqual("id_hash" in context, False)

    def test_build_session_none(self):
        _system = self._build_system()

        self.assertEqual(_system.build_session(None), None)
        self.assertEqual(_system.build_session(mocks.MockRequest()), None)

    def test_build_session_raising_request(self):
        _system = self._build_system()

        self.assertEqual(_system.build_session(mocks.MockRaisingRequest()), None)

    def test_build_response(self):
        _system = self._build_started()
        request = mocks.MockRequest(
            content_type="application/json", encoder_name="json"
        )
        _system.request_begin(request)

        exception = ValueError("not found")
        exception.status_code = 404
        response = _system.build_response(request, exception=exception)

        self.assertEqual(response["status_code"], 404)
        self.assertEqual(response["content_type"], "application/json")
        self.assertEqual(response["encoder"], "json")
        self.assertEqual(response["elapsed"] >= 0.0, True)

    def test_build_response_other_request(self):
        _system = self._build_started()
        _system.request_begin(mocks.MockRequest())

        # the beginning of the handling is only known for the request that is
        # being handled by the current thread and not for any other request
        response = _system.build_response(mocks.MockRequest(status_code=200))

        self.assertEqual(response, dict(status_code=200))

    def test_build_response_none(self):
        _system = self._build_started()

        self.assertEqual(_system.build_response(None), None)

    def test_build_response_raising_request(self):
        _system = self._build_started()

        self.assertEqual(_system.build_response(mocks.MockRaisingRequest()), None)

    def test_describe_value(self):
        _system = self._build_started()
        store = dict(object_id=1, name="Store", address="Porto")

        self.assertEqual(_system.describe_value(1), "1")
        self.assertEqual(_system.describe_value("pt_pt"), "pt_pt")
        self.assertEqual(
            _system.describe_value(store), dict(object_id="1", name="Store")
        )

    def test_describe_value_truncated(self):
        _system = self._build_started()
        name = "x" * (system.MAX_VALUE_LENGTH + 1)

        # the identifying attributes of an object are truncated as any other value,
        # so that a large one never leads to the rejection of the complete event
        description = _system.describe_value(mocks.MockEntity(name=name))

        self.assertEqual(
            description, dict(name=name[: system.MAX_VALUE_LENGTH] + "...")
        )

    def test_describe_value_lazy(self):
        _system = self._build_started()
        store = mocks.MockEntity(name="Store")

        # the attributes that are not loaded in the object are not described, as
        # describing them would access the data source (lazy loading)
        self.assertEqual(_system.describe_value(store), dict(name="Store"))

    def test_scrub_map(self):
        _system = self._build_started()

        scrubbed = _system.scrub_map(dict(name="product", api_key="abc", quantity=12))

        self.assertEqual(scrubbed["name"], "product")
        self.assertEqual(scrubbed["api_key"], system.SCRUBBED_VALUE)
        self.assertEqual(scrubbed["quantity"], "12")

    def test_scrub_map_nested(self):
        _system = self._build_started()

        # the MVC layer stores the parsed payload of a request as a nested
        # map, so a sensitive field under a name that is not itself sensitive
        # must still be scrubbed
        scrubbed = _system.scrub_map(
            dict(_json_data=dict(name="product", password="secret"))
        )

        self.assertEqual(scrubbed["_json_data"]["name"], "product")
        self.assertEqual(scrubbed["_json_data"]["password"], system.SCRUBBED_VALUE)

    def test_scrub_map_empty(self):
        _system = self._build_started()

        self.assertEqual(_system.scrub_map(None), {})
        self.assertEqual(_system.scrub_map({}), {})

    def test_scrub_value_sequence(self):
        _system = self._build_started()

        scrubbed = _system.scrub_value([dict(token="abc"), "plain", 12])

        self.assertEqual(scrubbed[0]["token"], system.SCRUBBED_VALUE)
        self.assertEqual(scrubbed[1], "plain")
        self.assertEqual(scrubbed[2], "12")

    def test_scrub_value_tuple(self):
        _system = self._build_started()

        scrubbed = _system.scrub_value((dict(secret="abc"),))

        self.assertEqual(scrubbed[0]["secret"], system.SCRUBBED_VALUE)

    def test_scrub_value_scalar(self):
        _system = self._build_started()

        self.assertEqual(_system.scrub_value(12), "12")
        self.assertEqual(_system.scrub_value("plain"), "plain")

    def test_scrub_value_truncated(self):
        _system = self._build_started()
        limit = "x" * system.MAX_VALUE_LENGTH

        # a large value (eg: an uploaded file) would lead to the rejection of the
        # complete event, so the values exceeding the limit are truncated
        value = _system.scrub_value(limit + "x")

        self.assertEqual(_system.scrub_value(limit), limit)
        self.assertEqual(value, limit + "...")

    def test_is_sensitive(self):
        _system = self._build_started()

        self.assertEqual(_system.is_sensitive("password"), True)
        self.assertEqual(_system.is_sensitive("Authorization"), True)
        self.assertEqual(_system.is_sensitive("card_number"), True)
        self.assertEqual(_system.is_sensitive("session_id"), True)
        self.assertEqual(_system.is_sensitive("quantity"), False)

    def test_is_ignored(self):
        _system = self._build_started(ignored="ValueError;KeyError")

        self.assertEqual(_system.is_ignored(ValueError("invalid")), True)
        self.assertEqual(_system.is_ignored(KeyError("missing")), True)
        self.assertEqual(_system.is_ignored(RuntimeError("problem")), False)
        self.assertEqual(_system.is_ignored(None), False)

    def test_is_sampled(self):
        _system = self._build_started()

        self.assertEqual(_system.is_sampled(), True)

    def test_is_sampled_never(self):
        _system = self._build_started(sample_rate=0.0)

        self.assertEqual(_system.is_sampled(), False)

    def test_level(self):
        _system = self._build_started(level="warning")

        self.assertEqual(_system._level(), logging.WARNING)

    def test_is_scalar(self):
        _system = self._build_started()

        # the zero is a valid value (eg: the identifier of a user) while an empty
        # string identifies nothing, and the containers are never scalars
        self.assertEqual(_system._is_scalar("joamag"), True)
        self.assertEqual(_system._is_scalar(0), True)
        self.assertEqual(_system._is_scalar(""), False)
        self.assertEqual(_system._is_scalar(None), False)
        self.assertEqual(_system._is_scalar(dict()), False)

    def test_header(self):
        _system = self._build_started()
        headers = {"Host": "omni.example.com", "user-agent": "Mozilla/5.0"}
        request = mocks.MockCaseSensitiveRequest(headers=headers)

        self.assertEqual(_system._header(request, "Host"), "omni.example.com")
        self.assertEqual(_system._header(request, "User-Agent"), "Mozilla/5.0")
        self.assertEqual(_system._header(request, "Referer"), None)


class SentryHandlerTestCase(DiagnosticsSentryBaseTestCase):
    @staticmethod
    def get_description():
        return "Sentry Handler test case"

    def test_emit(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        record = self._build_record("problem")

        _system.handler.emit(record)

        self.assertEqual(len(client.events), 1)

    def test_emit_stack_record(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        record = self._build_record("  File ...")
        record.stack = True

        _system.handler.emit(record)

        self.assertEqual(len(client.events), 0)

    def test_emit_swallows_error(self):
        client = mocks.MockRaisingSentryClient()
        _system = self._build_started(client=client)
        record = self._build_record("problem")

        # silences the error handling of the logging infra-structure while the
        # emission is performed, as the failure is the expected outcome of the
        # test and the complete traceback of it would otherwise be printed to
        # the standard error stream
        raise_exceptions = logging.raiseExceptions
        logging.raiseExceptions = False
        try:
            _system.handler.emit(record)
        finally:
            logging.raiseExceptions = raise_exceptions

        self.assertEqual(len(client.events), 0)

    def test_emit_through_logger(self):
        client = mocks.MockSentryClient()
        self._build_started(client=client)

        logging.getLogger(system.DEFAULT_LOGGER).error("scheduler task failed")

        self.assertEqual(len(client.events), 1)
        self.assertEqual(client.events[0]["message"], "scheduler task failed")

    def test_emit_below_level(self):
        client = mocks.MockSentryClient()
        self._build_started(client=client)

        logging.getLogger(system.DEFAULT_LOGGER).info("just information")

        self.assertEqual(len(client.events), 0)

    def _build_record(self, message, level=logging.ERROR):
        return logging.LogRecord("colony", level, __file__, 1, message, None, None)


class DiagnosticsSentryPluginTestCase(DiagnosticsSentryBaseTestCase):
    @staticmethod
    def get_description():
        return "Diagnostics Sentry Plugin test case"

    def test_capabilities(self):
        # the reporter is not a dependency of any other plugin, meaning that
        # the plugin manager only loads it in case it's flagged as a startup
        # plugin, without such flag it would be installed but never loaded
        # and no error would ever be reported
        self.assertEqual("startup" in self.plugin.capabilities, True)
        self.assertEqual("error_reporter" in self.plugin.capabilities, True)

    def test_load_plugin(self):
        # the dependencies are only injected by the plugin manager after the
        # loading of the plugin, so the Sentry API plugin is not available at
        # this stage and starting the reporting would fail the loading of the
        # complete plugin system whenever a DSN is defined
        plugin = self._build_loaded()

        self.assertEqual(hasattr(plugin, "api_sentry_plugin"), False)
        self.assertEqual(plugin.system.client, None)
        self.assertEqual(plugin.system.handler, None)

    def test_end_load_plugin(self):
        logger = logging.getLogger(system.DEFAULT_LOGGER)
        handlers = len(logger.handlers)
        client = mocks.MockSentryClient()

        # injects the Sentry API plugin the same way the plugin manager does
        # for the dependencies, right before the end of the loading
        plugin = self._build_loaded()
        plugin.api_sentry_plugin = mocks.MockAPISentryPlugin(client=client)
        plugin.end_load_plugin()

        self.assertEqual(plugin.system.client, client)
        self.assertEqual(len(logger.handlers), handlers + 1)

    def test_unload_plugin(self):
        logger = logging.getLogger(system.DEFAULT_LOGGER)
        handlers = len(logger.handlers)
        client = mocks.MockSentryClient()

        plugin = self._build_loaded()
        plugin.api_sentry_plugin = mocks.MockAPISentryPlugin(client=client)
        plugin.end_load_plugin()
        plugin.unload_plugin()

        self.assertEqual(plugin.system.client, None)
        self.assertEqual(plugin.system.handler, None)
        self.assertEqual(client.closed, True)
        self.assertEqual(len(logger.handlers), handlers)

    def test_unload_plugin_not_started(self):
        # the loading of the plugin may be interrupted before its end (eg: a
        # dependency that fails to be injected), in which case the plugin is
        # still unloaded with the plugin system without its reporting having
        # ever been started
        plugin = self._build_loaded()
        plugin.unload_plugin()

        self.assertEqual(plugin.system.client, None)
        self.assertEqual(plugin.system.handler, None)

    def _build_loaded(self):
        colony.conf_s("SENTRY_DSN", DSN)

        # creates the plugin outside of the plugin manager so that none of its
        # dependencies is injected, which is the state of the plugin while its
        # loading is still in progress
        plugin = self.plugin.__class__(mocks.MockPluginManager())
        plugin.load_plugin()
        self._systems.append(plugin.system)
        return plugin
