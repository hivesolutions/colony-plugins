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


class MockFileEnginePlugin(object):
    """
    Mock file engine plugin, keeping the files in memory as a map
    that associates the name of each file with its data and its
    modification timestamp, the access to a file that does not exist
    fails with a key error, the error "native" to the engine.
    """

    def __init__(self, files=None):
        self.files = files or dict()

    def get_engine_name(self):
        return "mock"

    def get_internal_version(self):
        return None

    def create_connection(self, connection_parameters):
        return MockFileConnection(connection_parameters)

    def close_connection(self, connection):
        pass

    def get(self, connection, file_name):
        data, _mtime = self.files[file_name]
        return data

    def delete(self, connection, file_name):
        del self.files[file_name]

    def size(self, connection, file_name):
        data, _mtime = self.files[file_name]
        return len(data)

    def mtime(self, connection, file_name):
        _data, mtime = self.files[file_name]
        return mtime

    def exists(self, connection, file_name):
        return file_name in self.files


class MockFileConnection(object):
    """
    Mock file connection, holding the connection parameters
    used in its creation.
    """

    def __init__(self, connection_parameters):
        self.connection_parameters = connection_parameters
