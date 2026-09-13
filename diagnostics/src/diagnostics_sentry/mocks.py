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


class MockPlugin(object):
    def __init__(self, client=None):
        self.manager = MockPluginManager()
        self.api_sentry_plugin = MockAPISentryPlugin(client=client)


class MockPluginManager(object):
    def __init__(self, version="1.4.49", environment="cpython"):
        self._version = version
        self._environment = environment

    def get_version(self):
        return self._version

    def get_environment(self):
        return self._environment

    def get_plugin_paths(self):
        return ["/colony/plugins"]

    def get_system_information_map(self):
        return dict(
            layout_mode="default",
            run_mode="production",
            timestamp=1789261658.0,
            version=self._version,
            release="100",
            build="final",
            release_date_time="13 Sep 2026 01:07:38",
            environment=self._environment,
        )

    def generate_event(self, event_name, event_args):
        pass


class MockUnstartedPluginManager(MockPluginManager):
    def get_system_information_map(self):
        return None


class MockAPISentryPlugin(object):
    def __init__(self, client=None):
        self.client = client or MockSentryClient()
        self.attributes = None

    def create_client(self, api_attributes):
        self.attributes = api_attributes
        return self.client


class MockSentryClient(object):
    def __init__(self, accepted=True):
        self.accepted = accepted
        self.events = []
        self.closed = False

    def build_stacktrace(self, traceback_list):
        return dict(frames=["frame"])

    def build_event(self, **kwargs):
        return dict(kwargs)

    def submit_event(self, event):
        self.events.append(event)
        return self.accepted

    def close(self):
        self.closed = True


class MockRaisingSentryClient(MockSentryClient):
    def build_event(self, **kwargs):
        raise RuntimeError("no event")


class MockRequest(object):
    def __init__(
        self,
        method="GET",
        path="omni/sales",
        attributes_map=None,
        address="192.168.1.100",
        session=None,
        status_code=500,
        headers=None,
        connection_address=None,
        secure=False,
        server_software=None,
        request=None,
        content_type=None,
        encoder_name=None,
    ):
        self._method = method
        self._path = path
        self._attributes_map = attributes_map or {}
        self._address = address
        self._session = session
        self._status_code = status_code
        self._headers = headers or {}
        self._connection_address = connection_address or (None, None)
        self._secure = secure
        self._server_software = server_software
        self._request = request
        self._content_type = content_type
        self._encoder_name = encoder_name

    def is_get(self):
        return self._method == "GET"

    def is_secure(self):
        return self._secure

    def get_header(self, header_name):
        for name, value in self._headers.items():
            if name.lower() == header_name.lower():
                return value
        return None

    def get_headers(self):
        return self._headers

    def get_attributes_list(self):
        return list(self._attributes_map.keys())

    def get_attribute(self, attribute_name, default=None):
        return self._attributes_map.get(attribute_name, default)

    def get_server_software(self):
        return self._server_software

    def get_request(self):
        return self._request

    def get_session(self):
        return self._session

    def get_method(self):
        return self._method

    def get_path(self):
        return self._path

    def get_content_type(self):
        return self._content_type

    def get_encoder_name(self):
        return self._encoder_name

    def get_status_code(self):
        return self._status_code

    def get_connection_address(self, resolve=True, cleanup=True):
        return self._connection_address

    def get_address(self):
        return self._address


class MockRaisingRequest(MockRequest):
    def is_secure(self):
        raise RuntimeError("no scheme")

    def get_header(self, header_name):
        raise RuntimeError("no header")

    def get_headers(self):
        raise RuntimeError("no headers")

    def get_server_software(self):
        raise RuntimeError("no server software")

    def get_request(self):
        raise RuntimeError("no request")

    def get_session(self):
        raise RuntimeError("no session")

    def get_content_type(self):
        raise RuntimeError("no content type")

    def get_status_code(self):
        raise RuntimeError("no status code")

    def get_connection_address(self, resolve=True, cleanup=True):
        raise RuntimeError("no connection address")

    def get_address(self):
        raise RuntimeError("no address")


class MockCaseSensitiveRequest(MockRequest):
    def get_header(self, header_name):
        return self._headers.get(header_name, None)


class MockServiceRequest(object):
    def __init__(self, environ=None, query_string=None, protocol_version=None):
        self.environ = environ
        self.query_string = query_string
        self.protocol_version = protocol_version


class MockSession(object):
    def __init__(
        self,
        attributes_map=None,
        session_id="c2f1b9e7d4a6",
        name="RedisSession",
        creation_time=1789261658.0,
        expire_time=1789265258.0,
    ):
        self.attributes_map = attributes_map or {}
        self.session_id = session_id
        self.creation_time = creation_time
        self.expire_time = expire_time
        self._name = name

    def get_name(self):
        return self._name

    def get_session_id(self):
        return self.session_id

    def get_expire_time(self):
        return self.expire_time

    def get_attribute(self, attribute_name, default=None):
        return self.attributes_map.get(attribute_name, default)


class MockEntity(object):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __getattr__(self, name):
        raise RuntimeError("lazy loading of '%s' from the data source" % name)


class MockTemplateFile(object):
    def __init__(self, file_path="index.html.tpl"):
        self.file_path = file_path
