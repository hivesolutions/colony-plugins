#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

from csv_c import test_mocks

class CsvTest(colony.Test):
    """
    The csv serializer class, responsible for the
    management of the associated test cases.
    """

    def get_bundle(self):
        return (
            CsvBaseTestCase,
        )

class CsvBaseTestCase(colony.ColonyTestCase):

    @staticmethod
    def get_description():
        return "Csv Plugin test case"

    def test_dumps(self):
        result = self.system.dumps(test_mocks.SIMPLE_OBJECT, encoding = None)
        self.assertEqual(result, test_mocks.SIMPLE_CSV)

        result = self.system.dumps(test_mocks.SIMPLE_RAW, encoding = None)
        self.assertEqual(result, test_mocks.SIMPLE_CSV)

    def test_loads(self):
        result = self.system.loads(test_mocks.SIMPLE_CSV)
        self.assertEqual(result, test_mocks.SIMPLE_RAW)
