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
    def __init__(self):
        self.service_utils_plugin = None
        self.manager = None


class MockConfigurationProperty(object):
    def __init__(self, data):
        self._data = data

    def get_data(self):
        return self._data


class MockHandlerPlugin(object):
    def __init__(self, name):
        self._handler_name = name

    def get_handler_name(self):
        return self._handler_name


class MockEncodingPlugin(object):
    def __init__(self, name):
        self._encoding_name = name

    def get_encoding_name(self):
        return self._encoding_name


class MockAuthHandlerPlugin(object):
    def __init__(self, name):
        self._handler_name = name

    def get_handler_name(self):
        return self._handler_name


class MockErrorHandlerPlugin(object):
    def __init__(self, name):
        self._error_handler_name = name

    def get_error_handler_name(self):
        return self._error_handler_name
