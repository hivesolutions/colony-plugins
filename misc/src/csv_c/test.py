#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from . import mocks

class CSVTest(colony.Test):
    """
    The CSV serializer class, responsible for the
    management of the associated test cases.
    """

    def get_bundle(self):
        return (
            CSVBaseTestCase,
        )

class CSVBaseTestCase(colony.ColonyTestCase):

    @staticmethod
    def get_description():
        return "CSV Base test case"

    def test_dumps(self):
        result = self.system.dumps(mocks.SIMPLE_OBJECT, encoding = None)
        self.assertEqual(result, mocks.SIMPLE_CSV)

        result = self.system.dumps(mocks.SIMPLE_RAW, encoding = None)
        self.assertEqual(result, mocks.SIMPLE_CSV)

        result = self.system.dumps(mocks.COMPLEX_OBJECT, encoding = None)
        self.assertEqual(result, mocks.COMPLEX_CSV)

        result = self.system.dumps(mocks.COMPLEX_RAW, encoding = None)
        self.assertEqual(result, mocks.COMPLEX_CSV)

    def test_loads(self):
        result = self.system.loads(mocks.SIMPLE_CSV)
        self.assertEqual(result, mocks.SIMPLE_RAW)

        result = self.system.loads(mocks.COMPLEX_CSV)
        self.assertEqual(result, mocks.COMPLEX_RAW)
