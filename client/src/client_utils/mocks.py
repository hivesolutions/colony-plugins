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
        self.manager = None

    def debug(self, message):
        pass


class MockSocketProviderPlugin(object):
    def __init__(self, name):
        self._provider_name = name

    def get_provider_name(self):
        return self._provider_name

    def provide_socket_parameters(self, parameters):
        return MockSocket()


class MockSocketUpgraderPlugin(object):
    def __init__(self, name):
        self._upgrader_name = name

    def get_upgrader_name(self):
        return self._upgrader_name

    def upgrade_socket_parameters(self, socket, parameters):
        return socket


class MockSocket(object):
    def __init__(self, fd=-1):
        self._fd = fd
        self._closed = False
        self.blocking = True
        self._recv_data = [b""]
        self._sent_data = []

    def fileno(self):
        return self._fd

    def connect(self, address):
        pass

    def close(self):
        self._closed = True

    def setblocking(self, blocking):
        self.blocking = blocking

    def recv(self, size):
        if self._recv_data:
            return self._recv_data.pop(0)
        return b""

    def send(self, data):
        self._sent_data.append(data)
        return len(data)

    def sendto(self, data, address):
        self._sent_data.append(data)
        return len(data)
