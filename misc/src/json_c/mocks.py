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

import decimal
import datetime
import itertools

import colony


def mock_function():
    """
    Simple function to be used in the validation of the
    serialization of the function type.
    """

    pass


class MockObject(object):
    """
    Simple object to be used in the validation of the
    attribute based serialization of instances.
    """

    def __init__(self):
        self.age = 24
        self.name = colony.legacy.u("João")

    def method(self):
        pass


class MockJSONValue(object):
    """
    Object that provides a JSON value method, that should
    take precedence over the "normal" serialization.
    """

    def json_v(self):
        return dict(kind="resolved")


class MockJSONValueNative(object):
    """
    Object whose JSON value method returns a value that is
    already supported by the embedded encoder.
    """

    def json_v(self):
        return [1, 2]


class MockOpaque(object):
    """
    Object that hides every attribute, including the class
    one, making it impossible to serialize.
    """

    def __getattribute__(self, name):
        raise AttributeError(name)


SIMPLE_OBJECT = dict(name=colony.legacy.u("João"))

SIMPLE_JSON = colony.legacy.u('{"name":"João"}')

SIMPLE_PRETTY_JSON = colony.legacy.u('{\n    "name" : "João"\n}')

COMPLEX_OBJECT = [1, 2.5, True, False, None, [], dict(tuple=(1, 2))]

COMPLEX_JSON = '[1,2.5,true,false,null,[],{"tuple":[1,2]}]'

ESCAPE_OBJECT = ["/var/log", 'say "hi"', "a\nb\tc\x00"]

ESCAPE_JSON = '["\\/var\\/log","say \\"hi\\"","a\\nb\\tc\\u0000"]'

EQUIVALENT_VALUES = (
    None,
    True,
    False,
    0,
    -12,
    2**70,
    3.0,
    "",
    "plain",
    "a/b",
    "a\\b",
    colony.legacy.u("olá 中文"),
    [],
    {},
    (),
    [1, "two", None],
    dict(a=[1, dict(b=(2, 3))], c="d/e"),
    {1: "a", 2.5: "b"},
    datetime.datetime(2026, 1, 2, 3, 4, 5),
    datetime.datetime(1970, 1, 1),
    datetime.date(2026, 1, 2),
    colony.Decimal("12.50"),
    decimal.Decimal("0.5"),
    MockObject(),
    MockJSONValue(),
    MockJSONValueNative(),
    colony.FormatTuple("%s", "a"),
    dict(value=MockObject()),
)
""" The sequence of values for which both the "normal" and the
embedded approaches must generate exactly the same result """

FALLBACK_VALUES = (
    float("inf"),
    float("-inf"),
    decimal.Decimal("12.50"),
    decimal.Decimal("1E+2"),
    {True: 1},
    {None: 1},
    {(1, 2): "tuple key"},
    dict(ratio=float("inf")),
)
""" The sequence of values that the embedded approach is not able
to serialize in an equivalent way, and that must be routed into
the "normal" approach instead """
