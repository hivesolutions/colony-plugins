#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.test_util

class DummyUnitTest:
    """
    The dummy unit test class
    """

    dummy_unit_test_plugin = None
    """ The dummy unit test plugin """

    def __init__(self, dummy_unit_test_plugin):
        """
        Constructor of the class

        @type dummy_unit_test_plugin: DummyUnitTestPlugin
        @param dummy_unit_test_plugin: The dummy unit test plugin
        """

        self.dummy_unit_test_plugin = dummy_unit_test_plugin

    def get_test_case_bundle(self):
        return [DummyTest1, DummyTest2]

class DummyTest1(colony.libs.test_util.ColonyTestCase):

    def setUp(self):
        # prints a debug message
        self.plugin.info("Setting up dummy test 1...")

    def test_dummy_method1(self):
        self.assertEqual(True, True)

    def test_dummy_method2(self):
        self.assertEqual(False, False)

class DummyTest2(colony.libs.test_util.ColonyTestCase):

    def setUp(self):
        # prints a debug message
        self.plugin.info("Setting up dummy test 2...")

    def test_dummy_method1(self):
        self.assertEqual(1, 1)

    def test_dummy_method2(self):
        self.assertEqual(2, 2)
