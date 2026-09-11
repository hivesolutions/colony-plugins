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

import sys
import types
import decimal
import datetime
import itertools

import colony

from . import mocks
from . import serializer


class JSONTest(colony.Test):
    """
    The JSON serializer class, responsible for the
    management of the associated test cases.
    """

    def get_bundle(self):
        return (JSONBaseTestCase,)


class JSONBaseTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "JSON Base test case"

    def test_dumps_f(self):
        result = serializer.dumps_f(mocks.SIMPLE_OBJECT)
        self.assertEqual(result, mocks.SIMPLE_JSON)

        result = serializer.dumps_f(mocks.COMPLEX_OBJECT)
        self.assertEqual(result, mocks.COMPLEX_JSON)

        result = serializer.dumps_f(mocks.ESCAPE_OBJECT)
        self.assertEqual(result, mocks.ESCAPE_JSON)

        result = serializer.dumps_f(datetime.date(1970, 1, 2))
        self.assertEqual(result, "86400")

        # the to many relations of an entity are held in a list based
        # structure that used to be serialized as its own method map
        result = serializer.dumps_f(colony.JournaledList([1, 2]))
        self.assertEqual(result, "[1,2]")

        # the sub-classes of the native types used to be serialized as
        # the map of their own methods instead of their contents
        self.assertEqual(serializer.dumps_f(mocks.MockDict(a=1)), '{"a":1}')
        self.assertEqual(serializer.dumps_f(mocks.MockList([1, 2])), "[1,2]")
        self.assertEqual(serializer.dumps_f(mocks.MockString("a/b")), '"a\\/b"')

    def test_dumps_f_equivalent(self):
        for value in mocks.EQUIVALENT_VALUES:
            result = serializer.dumps_f(value)
            expected = serializer.dumps(value)
            self.assertEqual(result, expected)

        # the single pass sequences are consumed by the serialization
        # and so a new instance is built for each of the approaches
        result = serializer.dumps_f(item for item in [1, 2, 3])
        expected = serializer.dumps(item for item in [1, 2, 3])
        self.assertEqual(result, expected)
        self.assertEqual(result, "[1,2,3]")

        result = serializer.dumps_f(itertools.chain([1], [2]))
        expected = serializer.dumps(itertools.chain([1], [2]))
        self.assertEqual(result, expected)
        self.assertEqual(result, "[1,2]")

    def test_dumps_f_fallback(self):
        # the non finite float values are represented in a different
        # way by the embedded encoder and so the "normal" one is used
        self.assertEqual(serializer.dumps_f(float("inf")), "inf")
        self.assertEqual(serializer.dumps_f(float("-inf")), "-inf")
        self.assertEqual(serializer.dumps_f(dict(ratio=float("inf"))), '{"ratio":inf}')

        # the decimal values whose representation is not the same as
        # the float one must also be routed into the "normal" approach
        self.assertEqual(serializer.dumps_f(decimal.Decimal("12.50")), "12.50")
        self.assertEqual(serializer.dumps_f(decimal.Decimal("1E+2")), "1E+2")

        # the boolean and none keys are coerced by the embedded encoder
        # into their JSON counterparts instead of the string ones
        self.assertEqual(serializer.dumps_f({True: 1}), '{"True":1}')
        self.assertEqual(serializer.dumps_f({False: 1}), '{"False":1}')
        self.assertEqual(serializer.dumps_f({None: 1}), '{"None":1}')

        # the keys that are not supported by the embedded encoder are
        # converted into their string representation by the "normal" one
        self.assertEqual(serializer.dumps_f({(1, 2): "a"}), '{"(1, 2)":"a"}')

        # a string key that looks like a coerced one triggers the same
        # fallback, generating an equivalent (just slower) result
        self.assertEqual(serializer.dumps_f({"true": 1}), '{"true":1}')

        # the single pass sequences must not be consumed by the embedded
        # encoder, otherwise the fallback would lose their contents
        self.assertEqual(serializer.dumps_f(item for item in [float("inf")]), "[inf]")
        self.assertEqual(
            serializer.dumps_f(item for item in [decimal.Decimal("12.50")]), "[12.50]"
        )
        self.assertEqual(serializer.dumps_f(itertools.chain([float("inf")])), "[inf]")

        for value in mocks.FALLBACK_VALUES:
            result = serializer.dumps_f(value)
            expected = serializer.dumps(value)
            self.assertEqual(result, expected)

    def test_dumps_f_unencodable(self):
        self.assertRaises(
            colony.ColonyException, lambda: serializer.dumps_f(mocks.MockOpaque())
        )

    def test_dumps_f_no_embedded(self):
        # simulates the absence of the embedded JSON module, so that
        # the "normal" approach is used as the fallback strategy
        module = sys.modules.get("json", None)
        sys.modules["json"] = None
        try:
            result = serializer.dumps_f(mocks.SIMPLE_OBJECT)
        finally:
            if module == None:
                del sys.modules["json"]
            else:
                sys.modules["json"] = module
        self.assertEqual(result, mocks.SIMPLE_JSON)

    def test_dumps_f_version(self):
        version = serializer.FAST_VERSION

        # simulates an older interpreter, under which the embedded
        # encoder is not able to generate an equivalent result, note
        # that the control characters above the escape range are the
        # ones that the "normal" approach emits in their literal form
        serializer.FAST_VERSION = (99, 0)
        try:
            result = serializer.dumps_f("a\x1ab")
            self.assertEqual(result, serializer.dumps("a\x1ab"))
            self.assertEqual(result, '"a\x1ab"')
        finally:
            serializer.FAST_VERSION = version

        # simulates a recent enough interpreter, under which the same
        # control characters are escaped by the embedded encoder
        serializer.FAST_VERSION = (0, 0)
        try:
            self.assertEqual(serializer.dumps_f("a\x1ab"), '"a\\u001ab"')
        finally:
            serializer.FAST_VERSION = version

    def test_dumps_lazy_f(self):
        parts = list(serializer.dumps_lazy_f(mocks.COMPLEX_OBJECT))
        self.assertGreater(len(parts), 1)
        self.assertEqual("".join(parts), mocks.COMPLEX_JSON)

        parts = list(serializer.dumps_lazy_f([]))
        self.assertEqual("".join(parts), "[]")

        parts = list(serializer.dumps_lazy_f((1, 2)))
        self.assertEqual("".join(parts), "[1,2]")

        # the non sequence values are not able to generate a partial
        # result and so a single (complete) part is yielded
        parts = list(serializer.dumps_lazy_f(mocks.SIMPLE_OBJECT))
        self.assertEqual(len(parts), 1)
        self.assertEqual("".join(parts), mocks.SIMPLE_JSON)

        parts = list(serializer.dumps_lazy_f(float("inf")))
        self.assertEqual("".join(parts), "inf")

        # an item that requires the fallback must not affect the
        # remaining ones, that are still dumped by the embedded encoder
        parts = list(serializer.dumps_lazy_f([1, decimal.Decimal("12.50"), 2]))
        self.assertEqual("".join(parts), "[1,12.50,2]")
        self.assertEqual(
            "".join(parts), serializer.dumps([1, decimal.Decimal("12.50"), 2])
        )

    def test_default_f(self):
        self.assertEqual(
            serializer.default_f(mocks.MockJSONValue()), dict(kind="resolved")
        )
        self.assertEqual(serializer.default_f(mocks.MockJSONValueNative()), [1, 2])

        self.assertEqual(serializer.default_f(None), None)
        self.assertEqual(serializer.default_f(mocks.MockNone()), None)
        self.assertEqual(serializer.default_f("value"), "value")
        self.assertEqual(serializer.default_f(dict(a=1)), dict(a=1))

        self.assertEqual(serializer.default_f(mocks.mock_function), "function")
        self.assertEqual(serializer.default_f(types), "module")
        self.assertEqual(serializer.default_f(mocks.MockObject().method), "method")

        self.assertEqual(serializer.default_f(decimal.Decimal("0.5")), 0.5)

        value = datetime.datetime(1970, 1, 2)
        self.assertEqual(serializer.default_f(value), 86400)

        value = datetime.date(1970, 1, 2)
        self.assertEqual(serializer.default_f(value), 86400)

        value = serializer.default_f(mocks.MockObject())
        self.assertEqual(value, dict(age=24, name=colony.legacy.u("João")))

    def test_default_f_sequence(self):
        # the single pass sequences must not be consumed, as the
        # "normal" approach would not be able to iterate them again
        self.assertRaises(
            colony.ColonyException,
            lambda: serializer.default_f(item for item in [1, 2]),
        )
        self.assertRaises(
            colony.ColonyException,
            lambda: serializer.default_f(itertools.chain([1], [2])),
        )

        # the sequences are still dumped with their contents, through
        # the "normal" approach that is used as the fallback
        self.assertEqual(serializer.dumps_f(item for item in [1, 2]), "[1,2]")
        self.assertEqual(serializer.dumps_f(itertools.chain([1], [2])), "[1,2]")

    def test_default_f_invalid(self):
        self.assertRaises(
            colony.ColonyException,
            lambda: serializer.default_f(decimal.Decimal("12.50")),
        )
        self.assertRaises(
            colony.ColonyException, lambda: serializer.default_f(mocks.MockOpaque())
        )

    def test_dumps(self):
        result = self.system.dumps(mocks.SIMPLE_OBJECT)
        self.assertEqual(result, mocks.SIMPLE_JSON)

        result = self.system.dumps(mocks.SIMPLE_OBJECT, fast=False)
        self.assertEqual(result, mocks.SIMPLE_JSON)

        for value in mocks.EQUIVALENT_VALUES + mocks.FALLBACK_VALUES:
            self.assertEqual(
                self.system.dumps(value), self.system.dumps(value, fast=False)
            )

        # a date value used to send the serializer into an infinite
        # recursion, as it was handled as a generic instance
        value = datetime.date(1970, 1, 2)
        self.assertEqual(self.system.dumps(value), "86400")
        self.assertEqual(self.system.dumps(value, fast=False), "86400")

        # the to many relations of an entity are held in a list based
        # structure that used to be serialized as its own method map
        value = colony.JournaledList([1, 2])
        self.assertEqual(self.system.dumps(value), "[1,2]")
        self.assertEqual(self.system.dumps(value, fast=False), "[1,2]")

    def test_dumps_lazy(self):
        parts = list(self.system.dumps_lazy(mocks.COMPLEX_OBJECT))
        self.assertEqual("".join(parts), mocks.COMPLEX_JSON)

        parts = list(self.system.dumps_lazy(mocks.COMPLEX_OBJECT, fast=False))
        self.assertEqual("".join(parts), mocks.COMPLEX_JSON)

        # the "normal" approach generates a partial result while the
        # embedded one is only able to generate a complete one
        parts = list(self.system.dumps_lazy(mocks.COMPLEX_OBJECT, fast=False))
        self.assertGreater(len(parts), 1)

    def test_dumps_pretty(self):
        result = self.system.dumps_pretty(mocks.SIMPLE_OBJECT)
        self.assertEqual(result, mocks.SIMPLE_PRETTY_JSON)

        result = self.system.dumps_pretty(datetime.date(1970, 1, 2))
        self.assertEqual(result, "86400")

        result = self.system.dumps_pretty(mocks.MockList([1, 2]))
        self.assertEqual(result, "[1, 2]")

    def test_dumps_buffer(self):
        result = self.system.dumps_buffer(mocks.SIMPLE_OBJECT)
        self.assertEqual(result, mocks.SIMPLE_JSON)

        result = self.system.dumps_buffer(datetime.date(1970, 1, 2))
        self.assertEqual(result, "86400")

        result = self.system.dumps_buffer(mocks.MockList([1, 2]))
        self.assertEqual(result, "[1,2]")

    def test_loads(self):
        result = self.system.loads(mocks.SIMPLE_JSON)
        self.assertEqual(result, mocks.SIMPLE_OBJECT)

        result = self.system.loads(mocks.SIMPLE_JSON, fast=False)
        self.assertEqual(result, mocks.SIMPLE_OBJECT)

        result = self.system.loads(serializer.dumps_f(mocks.COMPLEX_OBJECT))
        self.assertEqual(result[:5], [1, 2.5, True, False, None])
