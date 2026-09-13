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

    def generate_event(self, event_name, event_args):
        pass


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
    ):
        self._method = method
        self._path = path
        self._attributes_map = attributes_map or {}
        self._address = address
        self._session = session
        self._status_code = status_code

    def get_method(self):
        return self._method

    def get_path(self):
        return self._path

    def get_attributes_map(self):
        return self._attributes_map

    def get_address(self):
        return self._address

    def get_session(self):
        return self._session

    def get_status_code(self):
        return self._status_code


class MockRaisingRequest(MockRequest):
    def get_address(self):
        raise RuntimeError("no address")

    def get_session(self):
        raise RuntimeError("no session")

    def get_status_code(self):
        raise RuntimeError("no status code")


class MockSession(object):
    def __init__(self, attributes_map=None):
        self._attributes_map = attributes_map or {}

    def get_attribute(self, attribute_name, default=None):
        return self._attributes_map.get(attribute_name, default)


class MockTemplateFile(object):
    def __init__(self, file_path="index.html.tpl"):
        self.file_path = file_path
