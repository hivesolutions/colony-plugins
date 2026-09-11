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
import json
import time

import colony

from . import mocks
from . import system
from . import exceptions

DSN = "https://public@o4507.ingest.us.sentry.io/4509"
""" The DSN used in the complete set of tests, considered
to be the canonical representation of a Sentry DSN """


class APISentryTest(colony.Test):
    """
    The API Sentry infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            APISentryTestCase,
            SentryClientDsnTestCase,
            SentryClientFrameTestCase,
            SentryClientEventTestCase,
            SentryClientSubmissionTestCase,
            ExceptionsTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class APISentryTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "API Sentry test case"

    def test_create_client(self):
        plugin = mocks.MockPlugin()
        api_sentry = system.APISentry(plugin)

        client = api_sentry.create_client(dict(dsn=DSN))

        self.assert_type(client, system.SentryClient)
        self.assertEqual(client.dsn, DSN)
        self.assertEqual(client.dsn_structure["project_id"], "4509")
        self.assertEqual(client.timeout, system.DEFAULT_TIMEOUT)
        self.assertEqual(client.max_length, system.DEFAULT_MAX_LENGTH)

    def test_create_client_attributes(self):
        plugin = mocks.MockPlugin()
        api_sentry = system.APISentry(plugin)

        client = api_sentry.create_client(
            dict(
                dsn=DSN,
                environment="production",
                release="1.49.2",
                server_name="omni-ldj",
                timeout=10.0,
                max_length=16,
                in_app_paths=["/omni"],
            )
        )

        self.assertEqual(client.environment, "production")
        self.assertEqual(client.release, "1.49.2")
        self.assertEqual(client.server_name, "omni-ldj")
        self.assertEqual(client.timeout, 10.0)
        self.assertEqual(client.max_length, 16)
        self.assertEqual(client.in_app_paths, ["/omni"])

    def test_create_client_no_dsn(self):
        plugin = mocks.MockPlugin()
        api_sentry = system.APISentry(plugin)

        client = api_sentry.create_client(dict())

        self.assertEqual(client.dsn_structure, None)
        self.assertEqual(client.is_enabled(), False)


class SentryClientDsnTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Sentry Client DSN test case"

    def test_close(self):
        http_client = mocks.MockHTTPClient()
        client = self._build_client(http_client=http_client)
        client.submit_event(client.build_event(message="message"))

        client.close()

        self.assertEqual(http_client.closed, True)
        self.assertEqual(client.http_client, None)

    def test_close_no_client(self):
        client = self._build_client()

        client.close()

        self.assertEqual(client.http_client, None)

    def test_close_flushes_pending(self):
        http_client = mocks.MockHTTPClient()
        client = self._build_client(http_client=http_client, max_length=16)
        client.submit_event(client.build_event(message="message"))

        self.assertEqual(len(http_client.requests), 0)

        client.close()

        self.assertEqual(len(http_client.requests), 1)

    def test_close_tolerates_transport_error(self):
        http_client = mocks.MockRaisingHTTPClient()
        client = self._build_client(http_client=http_client, max_length=16)
        client.submit_event(client.build_event(message="message"))

        client.close()

        self.assertEqual(http_client.closed, True)

    def test_parse_dsn(self):
        client = self._build_client()

        structure = client.parse_dsn(DSN)

        self.assertEqual(structure["public_key"], "public")
        self.assertEqual(structure["project_id"], "4509")
        self.assertEqual(
            structure["envelope_url"],
            "https://o4507.ingest.us.sentry.io/api/4509/envelope/",
        )

    def test_parse_dsn_port(self):
        client = self._build_client()

        structure = client.parse_dsn("http://public@sentry.example.com:9000/42")

        self.assertEqual(
            structure["envelope_url"],
            "http://sentry.example.com:9000/api/42/envelope/",
        )

    def test_parse_dsn_path_prefix(self):
        client = self._build_client()

        structure = client.parse_dsn("https://public@sentry.example.com/prefix/42")

        self.assertEqual(
            structure["envelope_url"],
            "https://sentry.example.com/prefix/api/42/envelope/",
        )

    def test_parse_dsn_no_scheme(self):
        client = self._build_client()

        self.assertRaises(
            exceptions.InvalidDsn, client.parse_dsn, "public@sentry.io/42"
        )

    def test_parse_dsn_no_public_key(self):
        client = self._build_client()

        self.assertRaises(
            exceptions.InvalidDsn, client.parse_dsn, "https://sentry.io/42"
        )

    def test_parse_dsn_no_project_id(self):
        client = self._build_client()

        self.assertRaises(
            exceptions.InvalidDsn, client.parse_dsn, "https://public@sentry.io/"
        )

    def test_is_enabled(self):
        client = self._build_client()

        self.assertEqual(client.is_enabled(), True)

    def test_is_enabled_no_dsn(self):
        client = self._build_client(dsn=None)

        self.assertEqual(client.is_enabled(), False)

    def test_is_enabled_rate_limited(self):
        client = self._build_client()
        client._retry_after = time.time() + 60.0

        self.assertEqual(client.is_enabled(), False)

    def test_is_enabled_rate_limit_elapsed(self):
        client = self._build_client()
        client._retry_after = time.time() - 1.0

        self.assertEqual(client.is_enabled(), True)

    def _build_client(self, dsn=DSN, http_client=None, **kwargs):
        plugin = mocks.MockPlugin(
            client_http_plugin=mocks.MockClientHTTPPlugin(http_client=http_client)
        )
        return system.SentryClient(
            plugin.json_plugin, plugin.client_http_plugin, dsn, **kwargs
        )


class SentryClientFrameTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Sentry Client frame test case"

    def test_build_frame(self):
        client = self._build_client()

        frame = client.build_frame(__file__, 1, "module")

        self.assertEqual(frame["filename"], "test.py")
        self.assertEqual(frame["abs_path"], __file__)
        self.assertEqual(frame["function"], "module")
        self.assertEqual(frame["lineno"], 1)
        self.assertEqual(frame["in_app"], False)
        self.assertEqual(frame["context_line"], "#!/usr/bin/python")
        self.assertEqual(frame["pre_context"], [])
        self.assertEqual(len(frame["post_context"]), system.CONTEXT_LINES)

    def test_build_frame_context_window(self):
        client = self._build_client()

        frame = client.build_frame(__file__, 20, "module")

        self.assertEqual(len(frame["pre_context"]), system.CONTEXT_LINES)
        self.assertEqual(len(frame["post_context"]), system.CONTEXT_LINES)
        self.assertEqual(frame["context_line"].endswith("\n"), False)

    def test_build_frame_missing_file(self):
        client = self._build_client()

        frame = client.build_frame("/not/a/real/file.py", 10, "function")

        self.assertEqual(frame["lineno"], 10)
        self.assertEqual("context_line" in frame, False)
        self.assertEqual("pre_context" in frame, False)

    def test_build_frame_lineno_overflow(self):
        client = self._build_client()

        frame = client.build_frame(__file__, 1000000, "function")

        self.assertEqual("context_line" in frame, False)

    def test_build_frame_lineno_zero(self):
        client = self._build_client()

        frame = client.build_frame(__file__, 0, "function")

        self.assertEqual("context_line" in frame, False)

    def test_build_stacktrace(self):
        client = self._build_client()

        try:
            self._raise_nested()
        except RuntimeError:
            _type, _value, traceback_list = sys.exc_info()
            stacktrace = client.build_stacktrace(traceback_list)

        frames = stacktrace["frames"]
        self.assertEqual(len(frames), 3)
        self.assertEqual(frames[0]["function"], "test_build_stacktrace")
        self.assertEqual(frames[1]["function"], "_raise_nested")
        self.assertEqual(frames[2]["function"], "_raise")

    def test_build_stacktrace_empty(self):
        client = self._build_client()

        stacktrace = client.build_stacktrace(None)

        self.assertEqual(stacktrace["frames"], [])

    def test_is_in_app(self):
        client = self._build_client(in_app_paths=["/omni", "/colony"])

        self.assertEqual(client.is_in_app("/omni/sales/src/system.py"), True)
        self.assertEqual(client.is_in_app("/usr/lib/python/json.py"), False)

    def test_is_in_app_no_paths(self):
        client = self._build_client()

        self.assertEqual(client.is_in_app("/omni/sales/src/system.py"), False)

    def _raise_nested(self):
        self._raise()

    def _raise(self):
        raise RuntimeError("nested problem")

    def _build_client(self, **kwargs):
        plugin = mocks.MockPlugin()
        return system.SentryClient(
            plugin.json_plugin, plugin.client_http_plugin, DSN, **kwargs
        )


class SentryClientEventTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Sentry Client event test case"

    def test_build_event(self):
        client = self._build_client()

        event = client.build_event()

        self.assertEqual(len(event["event_id"]), 32)
        self.assertEqual(event["platform"], system.DEFAULT_PLATFORM)
        self.assertEqual(event["level"], system.DEFAULT_LEVEL)
        self.assertEqual(event["server_name"], "omni-ldj")
        self.assertEqual(event["timestamp"].endswith("Z"), True)
        self.assertEqual(event["contexts"]["runtime"]["name"], "python")
        self.assertEqual("exception" in event, False)
        self.assertEqual("environment" in event, False)

    def test_build_event_unique_identifier(self):
        client = self._build_client()

        first = client.build_event()
        second = client.build_event()

        self.assertNotEqual(first["event_id"], second["event_id"])

    def test_build_event_environment_release(self):
        client = self._build_client(environment="production", release="1.49.2")

        event = client.build_event(logger="colony", message="problem")

        self.assertEqual(event["environment"], "production")
        self.assertEqual(event["release"], "1.49.2")
        self.assertEqual(event["logger"], "colony")
        self.assertEqual(event["message"], dict(formatted="problem"))

    def test_build_event_exception(self):
        client = self._build_client()

        event = client.build_event(exception=ValueError("invalid value"))

        values = event["exception"]["values"]
        self.assertEqual(len(values), 1)
        self.assertEqual(values[0]["type"], "ValueError")
        self.assertEqual(values[0]["value"], "invalid value")
        self.assertEqual("stacktrace" in values[0], False)

    def test_build_event_exception_stacktrace(self):
        client = self._build_client()
        stacktrace = dict(frames=[])

        event = client.build_event(
            exception=ValueError("invalid value"), stacktrace=stacktrace
        )

        self.assertEqual(event["exception"]["values"][0]["stacktrace"], stacktrace)
        self.assertEqual("stacktrace" in event, False)

    def test_build_event_stacktrace_only(self):
        client = self._build_client()
        stacktrace = dict(frames=[])

        event = client.build_event(stacktrace=stacktrace)

        self.assertEqual(event["stacktrace"], stacktrace)
        self.assertEqual("exception" in event, False)

    def test_build_event_optional(self):
        client = self._build_client()

        event = client.build_event(
            level="warning",
            request=dict(method="GET"),
            user=dict(id="1"),
            tags=dict(route="omni/sales"),
            extra=dict(status=500),
            breadcrumbs=[dict(message="query")],
        )

        self.assertEqual(event["level"], "warning")
        self.assertEqual(event["request"], dict(method="GET"))
        self.assertEqual(event["user"], dict(id="1"))
        self.assertEqual(event["tags"], dict(route="omni/sales"))
        self.assertEqual(event["extra"], dict(status=500))
        self.assertEqual(event["breadcrumbs"], dict(values=[dict(message="query")]))

    def test_build_envelope(self):
        client = self._build_client()
        event = client.build_event(message="problem")

        envelope = client.build_envelope(event)

        lines = envelope.split("\n")
        self.assertEqual(len(lines), 3)

        header = json.loads(lines[0])
        self.assertEqual(header["event_id"], event["event_id"])
        self.assertEqual(header["dsn"], DSN)

        item_header = json.loads(lines[1])
        self.assertEqual(item_header["type"], "event")
        self.assertEqual(item_header["length"], len(lines[2].encode("utf-8")))

    def test_build_envelope_unicode_length(self):
        client = self._build_client()
        event = client.build_event(message="problema com acentuação")

        envelope = client.build_envelope(event)

        lines = envelope.split("\n")
        item_header = json.loads(lines[1])
        self.assertEqual(item_header["length"], len(lines[2].encode("utf-8")))

    def _build_client(self, **kwargs):
        plugin = mocks.MockPlugin()
        kwargs.setdefault("server_name", "omni-ldj")
        return system.SentryClient(
            plugin.json_plugin, plugin.client_http_plugin, DSN, **kwargs
        )


class SentryClientSubmissionTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Sentry Client submission test case"

    def test_submit_event(self):
        http_client = mocks.MockHTTPClient()
        client = self._build_client(http_client=http_client)

        result = client.submit_event(client.build_event(message="problem"))

        self.assertEqual(result, True)
        self.assertEqual(len(http_client.requests), 1)
        self.assertEqual(
            http_client.requests[0]["url"],
            "https://o4507.ingest.us.sentry.io/api/4509/envelope/",
        )
        self.assertEqual(http_client.requests[0]["method"], system.POST_METHOD_VALUE)

    def test_submit_event_disabled(self):
        http_client = mocks.MockHTTPClient()
        client = self._build_client(dsn=None, http_client=http_client)

        result = client.submit_event(dict(event_id="0" * 32))

        self.assertEqual(result, False)
        self.assertEqual(len(http_client.requests), 0)

    def test_submit_event_buffers(self):
        http_client = mocks.MockHTTPClient()
        client = self._build_client(http_client=http_client, max_length=3)

        client.submit_event(client.build_event(message="first"))
        client.submit_event(client.build_event(message="second"))

        self.assertEqual(len(http_client.requests), 0)
        self.assertEqual(len(client.events), 2)

        client.submit_event(client.build_event(message="third"))

        self.assertEqual(len(http_client.requests), 3)
        self.assertEqual(len(client.events), 0)

    def test_submit_event_timeout_overflow(self):
        http_client = mocks.MockHTTPClient()
        client = self._build_client(http_client=http_client, max_length=16, timeout=0.0)
        client._last_flush = time.time() - 1.0

        client.submit_event(client.build_event(message="problem"))

        self.assertEqual(len(http_client.requests), 1)

    def test_submit_event_swallows_error(self):
        http_client = mocks.MockRaisingHTTPClient()
        client = self._build_client(http_client=http_client)

        result = client.submit_event(client.build_event(message="problem"))

        self.assertEqual(result, True)
        self.assertEqual(len(client.events), 0)

    def test_submit_event_raises_error(self):
        http_client = mocks.MockRaisingHTTPClient()
        client = self._build_client(http_client=http_client)

        self.assertRaises(
            RuntimeError,
            client.submit_event,
            client.build_event(message="problem"),
            True,
        )

    def test_flush_empty(self):
        http_client = mocks.MockHTTPClient()
        client = self._build_client(http_client=http_client)

        client.flush()

        self.assertEqual(len(http_client.requests), 0)

    def test_flush_clears_before_submission(self):
        http_client = mocks.MockRaisingHTTPClient()
        client = self._build_client(http_client=http_client, max_length=16)
        client.submit_event(client.build_event(message="problem"))

        client.flush()

        self.assertEqual(len(client.events), 0)
        self.assertEqual(len(http_client.requests), 1)

    def test_submit_envelope_auth_header(self):
        http_client = mocks.MockHTTPClient()
        client = self._build_client(http_client=http_client)

        client.submit_envelope(client.build_event(message="problem"))

        headers = http_client.requests[0]["headers"]
        self.assertEqual(
            headers["X-Sentry-Auth"],
            "Sentry sentry_version=%s, sentry_client=%s/%s, sentry_key=public"
            % (system.SENTRY_VERSION, system.CLIENT_NAME, system.CLIENT_VERSION),
        )
        self.assertEqual(
            http_client.requests[0]["content_type"], system.CONTENT_TYPE_VALUE
        )

    def test_submit_envelope_rate_limited(self):
        response = mocks.MockHTTPResponse(
            status_code=system.RATE_LIMIT_CODE, headers_map={"Retry-After": "120"}
        )
        http_client = mocks.MockHTTPClient(responses=[response])
        client = self._build_client(http_client=http_client)

        result = client.submit_envelope(client.build_event(message="problem"))

        self.assertEqual(result, False)
        self.assertEqual(client.is_enabled(), False)
        self.assertEqual(client._retry_after > time.time() + 100.0, True)

    def test_retry_delay(self):
        client = self._build_client()

        response = mocks.MockHTTPResponse(headers_map={"Retry-After": "45"})
        self.assertEqual(client._retry_delay(response), 45.0)

    def test_retry_delay_no_header(self):
        client = self._build_client()

        response = mocks.MockHTTPResponse()
        self.assertEqual(client._retry_delay(response), system.DEFAULT_RETRY_AFTER)

    def test_retry_delay_invalid_header(self):
        client = self._build_client()

        response = mocks.MockHTTPResponse(headers_map={"Retry-After": "soon"})
        self.assertEqual(client._retry_delay(response), system.DEFAULT_RETRY_AFTER)

    def test_get_http_client(self):
        http_client = mocks.MockHTTPClient()
        client = self._build_client(http_client=http_client)

        first = client._get_http_client()
        second = client._get_http_client()

        self.assertEqual(first, http_client)
        self.assertEqual(second, http_client)
        self.assertEqual(http_client.opened, True)

    def _build_client(self, dsn=DSN, http_client=None, **kwargs):
        plugin = mocks.MockPlugin(
            client_http_plugin=mocks.MockClientHTTPPlugin(http_client=http_client)
        )
        client = system.SentryClient(
            plugin.json_plugin, plugin.client_http_plugin, dsn, **kwargs
        )
        client.open()
        return client


class ExceptionsTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "API Sentry exceptions test case"

    def test_api_sentry_exception(self):
        exception = exceptions.APISentryException()

        self.assertTrue(isinstance(exception, colony.ColonyException))
        self.assertEqual(exception.message, None)

    def test_invalid_dsn(self):
        exception = exceptions.InvalidDsn("https://sentry.io/42")

        self.assertTrue(isinstance(exception, exceptions.APISentryException))
        self.assertEqual(exception.message, "https://sentry.io/42")
        self.assertEqual(str(exception), "Invalid DSN - https://sentry.io/42")
