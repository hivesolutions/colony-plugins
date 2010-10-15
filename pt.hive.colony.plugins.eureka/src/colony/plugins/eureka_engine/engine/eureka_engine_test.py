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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2087 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-20 22:25:42 +0100 (Mon, 20 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import unittest

class EurekaEngineTest:
    """
    The Eureka Engine plugin unit test class.
    """

    eureka_engine_plugin = None
    """ The eureka engine plugin """

    def __init__(self, eureka_engine_plugin):
        """
        Constructor of the class

        @type eureka_engine_plugin: EurekaEnginePlugin
        @param eureka_engine_plugin: The eureka engine plugin.
        """

        self.eureka_engine_plugin = eureka_engine_plugin

    def get_plugin_test_case_bundle(self):
        return [EurekaEnginePluginTestCase]

class EurekaEngineTestCase(unittest.TestCase):
    """
    This test case targets the Eureka Engine core.
    The plugin's facade is exercised below using Mock objects to stand-in for
     - Item Extension plugins
     - Eureka Items of entity, operation, procedure and text parameter types
     - Eureka Item Processer plugins (filter, mapper, sorter and a context aware filter)
    """

    def setUp(self):
        self.plugin.logger.info("Setting up Eureka Engine Test Case...")

    def test_method_get_all_items_with_mock_item_extension(self):
        """
        This method targets the get_all_items of the EurekaEnginePlugin's facade
        """

        # @todo: specify test environment (use the MockItemExtensionPlugin)

        # testing with valid keyword
        test_items = self.plugin.get_all_items("mock")
        self.assertEqual(len(test_items), 4)

        # testing with non-present keyword
        test_items = self.plugin.get_all_items("badkeyword")
        # as all items are being fetched, it should return 4 items
        self.assertEqual(len(test_items), 4)

        # testing with specific keyword
        test_items = self.plugin.get_all_items("entity")
        self.assertEqual(len(test_items), 4)

    def test_method_get_items_with_mocks(self):
        """
        This method targets the get_items_xxx methods of the EurekaEnginePlugin's facade:
         - get_items_for_string
         - get_items_for_string_with_context
        The main cenarios exercised are:
         - valid keyword, returning several items
         - keyword which is not present in any item, returing 0 items
         - specific keywords, returning only some items
         - using an Eureka Item Mapper plugin to test the scoring approach
         - different similarity scores (partial and full matches) of the provided keywords against the specific item's keywords
         - using an Eureka Item Sorter, to get ordered item lists (after being scored)
         - using Eureka Item Filters both with and without context
        """

        # testing with valid keyword
        test_items = self.plugin.get_items_for_string("mock", max_items = None)
        self.assertEqual(len(test_items), 4)

        # testing with non-present keyword
        test_items = self.plugin.get_items_for_string("badkeyword", max_items = None)
        self.assertEqual(len(test_items), 0)

        # testing with specific keyword
        test_items = self.plugin.get_items_for_string("entity", max_items = None)
        self.assertEqual(len(test_items), 1)

        # testing mapper plugins
        test_items = self.plugin.get_items_for_string("entity action", max_items = None)
        self.assertEqual(test_items[0].score, 0.6)

        # testing mapper plugins full hit
        test_items = self.plugin.get_items_for_string("mock entity", max_items = None)
        self.assertEqual(test_items[0].score, 1)

        # testing sorter plugin
        test_items = self.plugin.get_items_for_string("mock text", max_items = None)
        self.assertEqual(test_items[0].key, "mock_text_parameter")

        # testing sorter with hit ratio
        test_items = self.plugin.get_items_for_string("text parameter", max_items = None)
        self.assertEqual(test_items[0].key, "mock_text_parameter")

        # testing context awareness
        import eureka_mock_item_extension.mock_item_extension.mock_operation_item
        operation_item = eureka_mock_item_extension.mock_item_extension.mock_operation_item.MockOperationItem()
        context = [operation_item]
        test_items = self.plugin.get_items_for_string_with_context("mock", context, max_items = None)
        self.assertEqual(test_items[0].key, "mock_entity")
        # due to context should only find one item
        self.assertEqual(len(test_items), 1)

        # testing context awareness filter without context
        test_items = self.plugin.get_items_for_string_with_context("mock", context = None, max_items = None)
        self.assertEqual(test_items[0].key, "mock_entity")

class EurekaEnginePluginTestCase:

    @staticmethod
    def get_test_case():
        return EurekaEngineTestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "Eureka Engine Plugin test case covering the server side plugin's facade"
