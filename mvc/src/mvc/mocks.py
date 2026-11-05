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
        self.manager = MockManager()


class MockManager(object):
    def __init__(self):
        self.run_mode = "development"

    def is_development(self):
        return self.run_mode == "development"


class MockMVCServicePlugin(object):
    def __init__(self):
        self.short_name = "mock"
        self.controller = MockController(self)

    def get_patterns(self):
        return ((r"mvc/test", self.controller.handle_test),)


class MockController(object):
    def __init__(self, plugin):
        self.plugin = plugin

    def handle_test(self, request):
        pass


class MockRESTRequest(object):
    def __init__(self):
        self.path_list = ["mvc", "other"]
        self.calls = []

    def get_path_list(self):
        return self.path_list

    def clear_sessions(self):
        self.calls.append("clear_sessions")
