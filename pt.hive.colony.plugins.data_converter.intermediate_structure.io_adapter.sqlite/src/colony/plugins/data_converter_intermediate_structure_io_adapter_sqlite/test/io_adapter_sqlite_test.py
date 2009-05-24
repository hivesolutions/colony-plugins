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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import unittest
import os.path

class IoAdapterSqliteTest:
    """
    The input output sqlite test plugin unit test class.
    """

    io_adapter_sqlite_test_plugin = None
    """ The input output sqlite test plugin """

    def __init__(self, io_adapter_sqlite_test_plugin):
        """
        Constructor of the class.

        @type io_adapter_sqlite_test_plugin: IoAdapterSqliteTestPlugin
        @param io_adapter_sqlite_test_plugin: The input output sqlite test plugin.
        """

        self.io_adapter_sqlite_test_plugin = io_adapter_sqlite_test_plugin

    def get_plugin_test_case_bundle(self):
        return [IoAdapterSqliteTestPluginTestCase]

class IoAdapterSqliteTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin.info("Setting up Io Adapter Sqlite Test Case...")

        # retrieves the resource manager plugin
        resource_manager_plugin = self.plugin.resource_manager_plugin

        # retrieves the user home path resource
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")

        # retrieves the user home path value
        user_home_path = user_home_path_resource.data

        # creates the path where to store the serialized intermediate structures used in the test
        self.test_intermediate_structure_file_path = os.path.join(user_home_path, "test_intermediate_structure.sqlite")

        # retrieves the intermediate structure plugin
        self.intermediate_structure_plugin = self.plugin.intermediate_structure_plugin

    def tearDown(self):
        self.plugin.info("Tearing down Io Adapter Sqlite Test Case...")

        # removes the files created in the test
        if os.path.exists(self.test_intermediate_structure_file_path):
            os.remove(self.test_intermediate_structure_file_path)

class IoAdapterSqliteTestPluginTestCase:

    @staticmethod
    def get_related_class():
        return pt.hive.colony.plugins.DataConverterIoAdapterSqlitePlugin

    @staticmethod
    def get_test_case():
        return IoAdapterSqliteTestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "Io Adapter Sqlite Test Plugin test case covering the data converter input output sqlite testing"
s
