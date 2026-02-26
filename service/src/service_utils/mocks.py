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

    def info(self, message):
        pass

    def warning(self, message):
        pass


class MockSocket(object):
    def __init__(self, fd=10):
        self._fd = fd
        self._closed = False
        self.blocking = True

    def fileno(self):
        return self._fd

    def close(self):
        self._closed = True

    def setblocking(self, blocking):
        self.blocking = blocking

    def accept(self):
        return (MockSocket(self._fd + 1), ("127.0.0.1", 12345))

    def recv(self, size):
        return b""

    def send(self, data):
        return len(data)

    def setsockopt(self, level, option, value):
        pass

    def bind(self, address):
        pass

    def listen(self, backlog):
        pass
