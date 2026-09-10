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


class MockManager(object):
    """
    Mock plugin manager, used to provide the minimum
    amount of interface required by the template engine
    for the loading of the system wide variables.
    """

    def get_system_information_map(self):
        return dict(name="mock", version="1.0.0")


class MockPlugin(object):
    """
    Mock plugin to be used as the owner of the template
    engine system object under testing.
    """

    def __init__(self):
        self.manager = MockManager()

    def debug(self, message, *args, **kwargs):
        pass

    def info(self, message, *args, **kwargs):
        pass


class MockEntity(object):
    """
    Simple object based entity to be used in the testing
    of the attribute (object) based resolution of values.
    """

    def __init__(self, name="name", value=1, child=None):
        self.name = name
        self.value = value
        self.child = child

    def get_name(self):
        return self.name

    def upper_name(self, suffix="", prefix=""):
        return prefix + self.name.upper() + suffix
