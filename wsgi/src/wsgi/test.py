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

import datetime
import time

import colony

from . import exceptions
from . import mocks
from . import system


class WSGITest(colony.Test):
    """
    The WSGI test class, responsible for returning
    the associated test cases.
    """

    def get_bundle(self):
        return (
            WSGISystemTestCase,
            WSGIRequestTestCase,
            WSGIRequestParsingTestCase,
            WSGIRequestHeadersTestCase,
            WSGIRequestCacheTestCase,
            WSGIPathResolutionTestCase,
            ExceptionsTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class WSGISystemTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "WSGI System test case"

    def test_initialization(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        self.assertEqual(wsgi.plugin, mock_plugin)

    def test_handle_success(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        environ = mocks.create_environ(method="GET", path="/test")
        start_response = mocks.MockStartResponse()

        wsgi.handle(environ, start_response)

        self.assertNotEqual(start_response.status, None)
        self.assertTrue(start_response.status.startswith("200"))
        self.assertNotEqual(start_response.response_headers, None)

    def test_handle_exception(self):
        mock_plugin = mocks.MockPlugin()
        mock_plugin.rest_plugin.raise_exception = True
        mock_plugin.rest_plugin.exception = Exception("Test error")
        wsgi = system.WSGI(mock_plugin)

        environ = mocks.create_environ(method="GET", path="/test")
        start_response = mocks.MockStartResponse()

        content = wsgi.handle(environ, start_response)

        self.assertTrue(start_response.status.startswith("500"))
        self.assertTrue(len(content) > 0)

    def test_handle_exception_with_status_code(self):
        mock_plugin = mocks.MockPlugin()

        class CustomException(Exception):
            status_code = 404

        mock_plugin.rest_plugin.raise_exception = True
        mock_plugin.rest_plugin.exception = CustomException("Not found")
        wsgi = system.WSGI(mock_plugin)

        environ = mocks.create_environ(method="GET", path="/test")
        start_response = mocks.MockStartResponse()

        wsgi.handle(environ, start_response)

        self.assertTrue(start_response.status.startswith("404"))

    def test_handle_with_prefix(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        environ = mocks.create_environ(method="GET", path="/test")
        start_response = mocks.MockStartResponse()

        wsgi.handle(environ, start_response, prefix="/api")

        self.assertEqual(len(mock_plugin.rest_plugin.handled_requests), 1)
        request = mock_plugin.rest_plugin.handled_requests[0]
        self.assertTrue(request.uri.startswith("/dynamic/rest/api"))

    def test_handle_response_headers(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        environ = mocks.create_environ(method="GET", path="/test")
        start_response = mocks.MockStartResponse()

        wsgi.handle(environ, start_response)

        header_names = [h[0] for h in start_response.response_headers]
        self.assertIn("Content-Type", header_names)
        self.assertIn("X-Powered-By", header_names)

    def test_handle_security_headers(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        environ = mocks.create_environ(method="GET", path="/test")
        start_response = mocks.MockStartResponse()

        wsgi.handle(environ, start_response)

        header_names = [h[0] for h in start_response.response_headers]
        self.assertIn("Access-Control-Allow-Origin", header_names)
        self.assertIn("Access-Control-Allow-Headers", header_names)
        self.assertIn("Access-Control-Allow-Methods", header_names)
        self.assertIn("Content-Security-Policy", header_names)
        self.assertIn("X-Frame-Options", header_names)
        self.assertIn("X-XSS-Protection", header_names)
        self.assertIn("X-Content-Type-Options", header_names)

    def test_error_message(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        error = Exception("Test error message")
        message = wsgi.error_message(error, code=500)

        self.assertIn("500", message)
        self.assertIn("Test error message", message)
        self.assertIn("Colony Framework", message)

    def test_error_message_development_mode(self):
        mock_plugin = mocks.MockPlugin()
        mock_plugin.manager._development = True
        wsgi = system.WSGI(mock_plugin)

        try:
            raise Exception("Test traceback")
        except Exception as e:
            message = wsgi.error_message(e, code=500)

        self.assertIn("Traceback", message)

    def test_error_message_production_mode(self):
        mock_plugin = mocks.MockPlugin()
        mock_plugin.manager._development = False
        wsgi = system.WSGI(mock_plugin)

        error = Exception("Test error")
        message = wsgi.error_message(error, code=500)

        self.assertNotIn("Traceback", message)

    def test_stacktrace_message(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        try:
            raise Exception("Test exception")
        except Exception:
            lines = list(wsgi.stacktrace_message())

        self.assertTrue(len(lines) > 0)
        self.assertTrue(any("Exception" in line for line in lines))


class WSGIRequestTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "WSGI Request test case"

    def test_initialization(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.service, wsgi)
        self.assertEqual(request.operation_type, "GET")
        self.assertEqual(request.status_code, 200)
        self.assertNotEqual(request.attributes_map, None)
        self.assertNotEqual(request.headers_out, None)
        self.assertNotEqual(request.message_buffer, None)

    def test_path_construction(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test/path")

        request = system.WSGIRequest(wsgi, environ)

        self.assertTrue(request.uri.endswith("/test/path"))
        self.assertTrue(request.path.endswith("/test/path"))
        self.assertEqual(request.original_path, "/test/path")

    def test_path_with_query_string(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(
            method="GET", path="/test", query_string="key=value"
        )

        request = system.WSGIRequest(wsgi, environ)

        self.assertIn("?", request.path)
        self.assertIn("key=value", request.path)
        self.assertIn("?", request.original_path)

    def test_path_with_script_name(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test", script_name="/app")

        request = system.WSGIRequest(wsgi, environ)

        self.assertTrue(request.original_path.startswith("/app"))

    def test_path_with_prefix(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ, prefix="/api")

        self.assertIn("/api", request.uri)

    def test_operation_type(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        for method in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
            environ = mocks.create_environ(method=method, path="/test")
            request = system.WSGIRequest(wsgi, environ)
            self.assertEqual(request.get_operation_type(), method)
            self.assertEqual(request.get_method(), method)

    def test_set_operation_type(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.set_operation_type("POST")

        self.assertEqual(request.get_operation_type(), "POST")

    def test_read(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        body = b"test body content"
        environ = mocks.create_environ(
            method="POST",
            path="/test",
            body=body,
            content_length=len(body),
        )

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.read(), body)

    def test_write(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.write(b"Hello ")
        request.write(b"World")

        self.assertEqual(len(request.message_buffer), 2)
        self.assertEqual(request.message_buffer[0], b"Hello ")
        self.assertEqual(request.message_buffer[1], b"World")

    def test_write_unicode(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.write("Hello World")

        self.assertEqual(len(request.message_buffer), 1)
        self.assertEqual(request.message_buffer[0], b"Hello World")

    def test_flush(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.flush()

    def test_finish(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.finish()

        self.assertIn("Cache-Control", request.headers_out)
        self.assertEqual(
            request.headers_out["Cache-Control"], "no-cache, must-revalidate"
        )

    def test_finish_preserves_cache_control(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.headers_out["Cache-Control"] = "max-age=3600"
        request.finish()

        self.assertEqual(request.headers_out["Cache-Control"], "max-age=3600")

    def test_is_secure_http(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test", url_scheme="http")

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.is_secure(), False)

    def test_is_secure_https(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test", url_scheme="https")

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.is_secure(), True)

    def test_allow_deny_cookies(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)

        # default should be True
        self.assertEqual(request.cookies_allowed, True)

        request.deny_cookies()
        self.assertEqual(request.cookies_allowed, False)

        request.allow_cookies()
        self.assertEqual(request.cookies_allowed, True)

    def test_is_mediated(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.is_mediated(), False)

        request.mediated = True
        self.assertEqual(request.is_mediated(), True)

    def test_is_chunked_encoded(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)

        # default should be False
        self.assertEqual(request.is_chunked_encoded(), False)

        request.chunked_encoding = True
        self.assertEqual(request.is_chunked_encoded(), True)

    def test_get_status_message(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)

        request.status_code = 200
        self.assertEqual(request.get_status_message(), "OK")

        request.status_code = 404
        self.assertEqual(request.get_status_message(), "Not Found")

        request.status_code = 500
        self.assertEqual(request.get_status_message(), "Internal Server Error")

    def test_get_status_message_custom(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.status_message = "Custom Message"

        self.assertEqual(request.get_status_message(), "Custom Message")

    def test_get_status_message_invalid(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.status_code = 999

        self.assertEqual(request.get_status_message(), "Invalid")

    def test_execute_background(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)

        executed = []

        def background_task():
            executed.append(True)

        request.execute_background(background_task)
        time.sleep(0.1)

        self.assertEqual(len(executed), 1)

    def test_mediate(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.mediated = True
        request.mediated_handler = mocks.MockMediatedHandler(b"Hello World")

        chunks = list(request.mediate())

        self.assertEqual(b"".join(chunks), b"Hello World")


class WSGIRequestParsingTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "WSGI Request Parsing test case"

    def test_parse_get_arguments(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(
            method="GET", path="/test", query_string="name=John&age=30"
        )

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.get_attribute("name"), "John")
        self.assertEqual(request.get_attribute("age"), "30")

    def test_parse_get_arguments_url_encoded(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(
            method="GET", path="/test", query_string="name=John%20Doe&city=New%20York"
        )

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.get_attribute("name"), "John Doe")
        self.assertEqual(request.get_attribute("city"), "New York")

    def test_parse_get_arguments_empty_value(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test", query_string="flag")

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.get_attribute("flag"), None)

    def test_parse_get_arguments_duplicate(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(
            method="GET", path="/test", query_string="item=a&item=b&item=c"
        )

        request = system.WSGIRequest(wsgi, environ)

        items = request.get_attribute("item")
        self.assertEqual(items, ["a", "b", "c"])

    def test_parse_post_urlencoded(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        body = b"username=admin&password=secret"
        environ = mocks.create_environ(
            method="POST",
            path="/test",
            content_type="application/x-www-form-urlencoded",
            content_length=len(body),
            body=body,
        )

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.get_attribute("username"), "admin")
        self.assertEqual(request.get_attribute("password"), "secret")

    def test_parse_multipart(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        fields = [
            ("name", "John"),
            ("email", "john@example.com"),
        ]
        body, content_type = mocks.create_multipart_body(fields)

        environ = mocks.create_environ(
            method="POST",
            path="/test",
            content_type=content_type,
            content_length=len(body),
            body=body,
        )

        request = system.WSGIRequest(wsgi, environ)

        name_attr = request.get_attribute("name")
        self.assertNotEqual(name_attr, None)
        self.assertEqual(name_attr["contents"], b"John")

        email_attr = request.get_attribute("email")
        self.assertNotEqual(email_attr, None)
        self.assertEqual(email_attr["contents"], b"john@example.com")

    def test_parse_multipart_file(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        fields = [
            ("document", "test.txt", "Hello World", "text/plain"),
        ]
        body, content_type = mocks.create_multipart_body(fields)

        environ = mocks.create_environ(
            method="POST",
            path="/test",
            content_type=content_type,
            content_length=len(body),
            body=body,
        )

        request = system.WSGIRequest(wsgi, environ)

        doc_attr = request.get_attribute("document")
        self.assertNotEqual(doc_attr, None)
        self.assertEqual(doc_attr["filename"], "test.txt")
        self.assertEqual(doc_attr["contents"], b"Hello World")

    def test_get_attributes_list(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(
            method="GET", path="/test", query_string="a=1&b=2&c=3"
        )

        request = system.WSGIRequest(wsgi, environ)
        attrs = request.get_attributes_list()

        self.assertIn("a", attrs)
        self.assertIn("b", attrs)
        self.assertIn("c", attrs)

    def test_set_attribute(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.set_attribute("custom", "value")

        self.assertEqual(request.get_attribute("custom"), "value")

    def test_get_attribute_default(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.get_attribute("missing"), None)
        self.assertEqual(request.get_attribute("missing", "default"), "default")


class WSGIRequestHeadersTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "WSGI Request Headers test case"

    def test_get_header(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(
            method="GET",
            path="/test",
            headers={"X-Custom-Header": "custom-value"},
        )

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.get_header("X-Custom-Header"), "custom-value")

    def test_get_header_content_type(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(
            method="POST",
            path="/test",
            content_type="application/json",
        )

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.get_header("Content-Type"), "application/json")

    def test_get_header_missing(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)

        self.assertEqual(request.get_header("Missing-Header"), None)

    def test_set_header(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.set_header("X-Custom", "value")

        self.assertEqual(request.headers_out["X-Custom"], "value")

    def test_set_header_unicode(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.set_header("X-Unicode", "café")

        self.assertIn("X-Unicode", request.headers_out)

    def test_append_header(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.set_header("Set-Cookie", "session=abc")
        request.append_header("Set-Cookie", "; path=/")

        self.assertEqual(request.headers_out["Set-Cookie"], "session=abc; path=/")

    def test_append_header_new(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.append_header("X-New-Header", "value")

        self.assertEqual(request.headers_out["X-New-Header"], "value")


class WSGIRequestCacheTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "WSGI Request Cache Control test case"

    def test_max_age(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.set_max_age(3600)

        self.assertEqual(request.get_max_age(), 3600)
        self.assertEqual(request.headers_out["Cache-Control"], "max-age=3600")

    def test_etag(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        request.set_etag('"abc123"')

        self.assertEqual(request.get_etag(), '"abc123"')
        self.assertEqual(request.headers_out["ETag"], '"abc123"')

    def test_expiration_timestamp(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        timestamp = time.time() + 3600
        request.set_expiration_timestamp(timestamp)

        self.assertEqual(request.get_expiration_timestamp(), timestamp)

    def test_last_modified_timestamp(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)
        timestamp = time.time()
        request.set_last_modified_timestamp(timestamp)

        self.assertEqual(request.get_last_modified_timestamp(), timestamp)
        self.assertIn("Last-Modified", request.headers_out)

    def test_verify_resource_modification_not_modified(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        modified_time = datetime.datetime(2023, 1, 1, 12, 0, 0)
        if_modified = modified_time.strftime("%a, %d %b %Y %H:%M:%S GMT")

        environ = mocks.create_environ(
            method="GET",
            path="/test",
            headers={"If-Modified-Since": if_modified},
        )

        request = system.WSGIRequest(wsgi, environ)
        old_timestamp = datetime.datetime(2022, 1, 1, 12, 0, 0).timestamp()

        result = request.verify_resource_modification(modified_timestamp=old_timestamp)
        self.assertEqual(result, False)

    def test_verify_resource_modification_modified(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        modified_time = datetime.datetime(2023, 1, 1, 12, 0, 0)
        if_modified = modified_time.strftime("%a, %d %b %Y %H:%M:%S GMT")

        environ = mocks.create_environ(
            method="GET",
            path="/test",
            headers={"If-Modified-Since": if_modified},
        )

        request = system.WSGIRequest(wsgi, environ)
        new_timestamp = datetime.datetime(2024, 1, 1, 12, 0, 0).timestamp()

        result = request.verify_resource_modification(modified_timestamp=new_timestamp)
        self.assertEqual(result, True)

    def test_verify_resource_modification_etag_match(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        environ = mocks.create_environ(
            method="GET",
            path="/test",
            headers={"If-None-Match": '"abc123"'},
        )

        request = system.WSGIRequest(wsgi, environ)

        result = request.verify_resource_modification(etag_value='"abc123"')
        self.assertEqual(result, False)

    def test_verify_resource_modification_etag_no_match(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)

        environ = mocks.create_environ(
            method="GET",
            path="/test",
            headers={"If-None-Match": '"abc123"'},
        )

        request = system.WSGIRequest(wsgi, environ)

        result = request.verify_resource_modification(etag_value='"xyz789"')
        self.assertEqual(result, True)

    def test_verify_resource_modification_no_headers(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test")

        request = system.WSGIRequest(wsgi, environ)

        result = request.verify_resource_modification(
            modified_timestamp=time.time(), etag_value='"abc123"'
        )
        self.assertEqual(result, True)


class WSGIPathResolutionTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "WSGI Path Resolution test case"

    def test_resolve_path_no_alias(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test/path")

        request = system.WSGIRequest(wsgi, environ, alias=None)

        self.assertTrue(request.uri.endswith("/test/path"))

    def test_resolve_path_with_alias(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/old/path")

        alias = [("/old", "/new")]
        request = system.WSGIRequest(wsgi, environ, alias=alias)

        self.assertTrue(request.uri.endswith("/new/path"))

    def test_resolve_path_alias_no_match(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test/path")

        alias = [("/other", "/replaced")]
        request = system.WSGIRequest(wsgi, environ, alias=alias)

        self.assertTrue(request.uri.endswith("/test/path"))

    def test_shorten_path_no_rewrite(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test/path")

        request = system.WSGIRequest(wsgi, environ, rewrite=None)

        self.assertEqual(request.original_path, "/test/path")

    def test_shorten_path_with_rewrite(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/app/test/path")

        rewrite = [("/app", "")]
        request = system.WSGIRequest(wsgi, environ, rewrite=rewrite)

        self.assertEqual(request.original_path, "/test/path")

    def test_shorten_path_rewrite_no_match(self):
        mock_plugin = mocks.MockPlugin()
        wsgi = system.WSGI(mock_plugin)
        environ = mocks.create_environ(method="GET", path="/test/path")

        rewrite = [("/other", "")]
        request = system.WSGIRequest(wsgi, environ, rewrite=rewrite)

        self.assertEqual(request.original_path, "/test/path")


class ExceptionsTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "WSGI Exceptions test case"

    def test_wsgi_exception(self):
        exception = exceptions.WSGIException()
        self.assertEqual(exception.message, None)
        self.assertTrue(isinstance(exception, colony.ColonyException))

    def test_wsgi_runtime_exception(self):
        exception = exceptions.WSGIRuntimeException("test error message")
        self.assertEqual(exception.message, "test error message")
        self.assertEqual(str(exception), "WSGI runtime exception - test error message")

    def test_wsgi_runtime_exception_inheritance(self):
        exception = exceptions.WSGIRuntimeException("test")
        self.assertTrue(isinstance(exception, exceptions.WSGIException))
        self.assertTrue(isinstance(exception, colony.ColonyException))
