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

import sys
import logging

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
    "SENTRY_SEND_USER",
    "SENTRY_BREADCRUMBS",
    "SENTRY_MAX_BREADCRUMBS",
    "SENTRY_IGNORED",
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
        self.assertEqual(_system.send_user, True)
        self.assertEqual(_system.breadcrumbs, True)
        self.assertEqual(_system.max_breadcrumbs, system.DEFAULT_MAX_BREADCRUMBS)
        self.assertEqual(_system.ignored, system.DEFAULT_IGNORED)

    def test_configuration_override(self):
        _system = self._build_system(
            level="WARNING",
            sample_rate=0.5,
            send_request=True,
            send_user=False,
            max_breadcrumbs=10,
        )

        self.assertEqual(_system.level, "WARNING")
        self.assertEqual(_system.sample_rate, 0.5)
        self.assertEqual(_system.send_request, True)
        self.assertEqual(_system.send_user, False)
        self.assertEqual(_system.max_breadcrumbs, 10)

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

    def test_request_end_exception(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        request = mocks.MockRequest()
        _system.request_begin(request)

        _system.request_end(request, RuntimeError("problem"))

        self.assertEqual(len(client.events), 1)
        self.assertEqual(_system._context().request, None)

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

    def test_request_exception_swallows_error(self):
        client = mocks.MockRaisingSentryClient()
        _system = self._build_started(client=client)

        _system.request_exception(mocks.MockRequest(), ValueError("invalid"))

        self.assertEqual(len(client.events), 0)

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

        _system.sql_executed("SELECT 1", "sqlite", 12)

        breadcrumb = _system._context().breadcrumbs[0]
        self.assertEqual(breadcrumb["category"], "query")
        self.assertEqual(breadcrumb["message"], "SELECT 1")
        self.assertEqual(breadcrumb["data"], dict(engine="sqlite", time=12))

    def test_sql_executed_bytes(self):
        _system = self._build_started()
        _system.request_begin(mocks.MockRequest())

        _system.sql_executed(b"SELECT 1", "sqlite", 12)

        self.assertEqual(_system._context().breadcrumbs[0]["message"], "SELECT 1")

    def test_sql_executed_truncated(self):
        _system = self._build_started()
        _system.request_begin(mocks.MockRequest())

        _system.sql_executed("A" * (system.MAX_QUERY_LENGTH + 100), "sqlite", 12)

        message = _system._context().breadcrumbs[0]["message"]
        self.assertEqual(len(message), system.MAX_QUERY_LENGTH)

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
        self.assertEqual(breadcrumbs[0]["message"], "SELECT 1")

    def test_capture_context_request(self):
        client = mocks.MockSentryClient()
        _system = self._build_started(client=client)
        request = mocks.MockRequest(path="omni/sales/1")
        _system.request_begin(request)

        _system.capture(exception=ValueError("invalid"))

        self.assertEqual(client.events[0]["request"]["url"], "omni/sales/1")

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

    def test_build_request_none(self):
        _system = self._build_started()

        self.assertEqual(_system.build_request(None), None)

    def test_build_request_contents(self):
        _system = self._build_started(send_request=True)
        request = mocks.MockRequest(
            attributes_map=dict(name="product", password="secret")
        )

        data = _system.build_request(request)

        self.assertEqual(data["data"]["name"], "product")
        self.assertEqual(data["data"]["password"], system.SCRUBBED_VALUE)

    def test_build_user(self):
        _system = self._build_started()
        session = mocks.MockSession(dict(username="joamag"))
        request = mocks.MockRequest(address="192.168.1.100", session=session)

        user = _system.build_user(request)

        self.assertEqual(user, dict(ip_address="192.168.1.100", username="joamag"))

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

    def test_build_tags(self):
        _system = self._build_started()
        request = mocks.MockRequest(method="POST", status_code=500)

        tags = _system.build_tags(request)

        self.assertEqual(tags, dict(method="POST", status_code="500"))

    def test_build_tags_none(self):
        _system = self._build_started()

        self.assertEqual(_system.build_tags(None), None)

    def test_build_tags_raising_request(self):
        _system = self._build_started()

        tags = _system.build_tags(mocks.MockRaisingRequest())

        self.assertEqual(tags, dict(method="GET"))

    def test_scrub_map(self):
        _system = self._build_started()

        scrubbed = _system.scrub_map(dict(name="product", api_key="abc", quantity=12))

        self.assertEqual(scrubbed["name"], "product")
        self.assertEqual(scrubbed["api_key"], system.SCRUBBED_VALUE)
        self.assertEqual(scrubbed["quantity"], "12")

    def test_scrub_map_empty(self):
        _system = self._build_started()

        self.assertEqual(_system.scrub_map(None), {})
        self.assertEqual(_system.scrub_map({}), {})

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

        _system.handler.emit(record)

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
