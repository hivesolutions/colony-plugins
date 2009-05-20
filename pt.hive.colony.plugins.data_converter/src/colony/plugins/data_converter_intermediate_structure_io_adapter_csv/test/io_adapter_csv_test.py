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

class IoAdapterCsvTest:
    """
    The input output csv test plugin unit test class.
    """

    io_adapter_csv_test_plugin = None
    """ The input output csv test plugin """

    def __init__(self, io_adapter_csv_test_plugin):
        """
        Constructor of the class.

        @type io_adapter_csv_test_plugin: IoAdapterCsvTestPlugin
        @param io_adapter_csv_test_plugin: The input output csv test plugin.
        """

        self.io_adapter_csv_test_plugin = io_adapter_csv_test_plugin

    def get_plugin_test_case_bundle(self):
        return [IoAdapterCsvTestPluginTestCase]

class IoAdapterCsvTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin.info("Setting up Io Adapter Csv Test Case...")

        # retrieves the resource manager plugin
        resource_manager_plugin = self.plugin.resource_manager_plugin

        # retrieves the user home path resource
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")

        # retrieves the user home path value
        user_home_path = user_home_path_resource.data

        # creates the path where to store the serialized intermediate structures used in the test
        self.test_intermediate_structure_file_path = os.path.join(user_home_path, "test_intermediate_structure")

        # retrieves the intermediate structure plugin
        self.intermediate_structure_plugin = self.plugin.intermediate_structure_plugin

    def test_intermediate_structure_csv(self):
        # defines the csv schema
        entity_names = ["dummy_entity", "dummy_entity"]
        entity_name_attribute_names_map = {"dummy_entity" : ["normal_attribute"],
                                           "dummy_entity" : ["normal_attribute"]}

        # creates test csv data
        file_data = ""
        for entity_index in range(3):
            for attribute_index in range(2):
                file_data += "%s;" % (entity_index + 1)
        file_data = file_data[:-1]

        # writes the test csv data to the test csv file
        file = open(self.test_intermediate_structure_file_path, "w")
        file.write(file_data)
        file.close()

        # creates an intermediate structure instance
        intermediate_structure = self.intermediate_structure_plugin.create_intermediate_structure()
        self.assertNotEquals(intermediate_structure, None)

        # defines the options that will be provided to the load and save operations
        io_adapter_plugin_id = "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.csv"
        load_save_options = {"file_path" : self.test_intermediate_structure_file_path,
                             "entity_names" : entity_names,
                             "entity_name_attribute_names" : entity_name_attribute_names_map,
                             "csv_token_separator" : ";"}

        first_entity_index = str(("dummy_entity", "1"))
        second_entity_index = str(("dummy_entity", "2"))

        # creates two entities and indexes them
        first_entity = intermediate_structure.create_entity("dummy_entity")
        second_entity = intermediate_structure.create_entity("dummy_entity")
        intermediate_structure.index_entity(first_entity, first_entity_index)
        intermediate_structure.index_entity(second_entity, second_entity_index)

        # retrieves the previously created entities
        first_entity = intermediate_structure.get_entity(first_entity_index)
        second_entity = intermediate_structure.get_entity(second_entity_index)

        # sets the first entity's attributes
        self.assertEquals(first_entity.get_object_id(), 1)
        self.assertEquals(first_entity.get_name(), "dummy_entity")
        first_entity.set_attribute("normal_attribute", "1")
        self.assertEquals(first_entity.has_attribute("normal_attribute"), True)
        self.assertEquals(first_entity.get_attribute("normal_attribute"), "1")

        # sets the second entity's attributes
        self.assertEquals(second_entity.get_object_id(), 2)
        self.assertEquals(second_entity.get_name(), "dummy_entity")
        second_entity.set_attribute("normal_attribute", "2")
        self.assertEquals(second_entity.has_attribute("normal_attribute"), True)
        self.assertEquals(second_entity.get_attribute("normal_attribute"), "2")

        # closes the intermediate structure thereby persisting it
        intermediate_structure.save(io_adapter_plugin_id, load_save_options)

        # re-opens the intermediate structure
        intermediate_structure.load(io_adapter_plugin_id, load_save_options)

        # tests the intermediate structure
        entities = intermediate_structure.get_entities("dummy_entity")
        self.assertEquals(len(entities), 2)
        entities = intermediate_structure.get_entities()
        self.assertEquals(len(entities), 2)

        # retrieves the previously saved entities
        first_entity = entities[0]
        second_entity = entities[1]

        # tests the first entity
        self.assertNotEquals(first_entity, None)
        self.assertEquals(first_entity.get_name(), "dummy_entity")
        self.assertEquals(first_entity.get_attribute("normal_attribute"), "1")

        # tests the second entity
        self.assertNotEquals(second_entity, None)
        self.assertEquals(second_entity.get_name(), "dummy_entity")
        self.assertEquals(second_entity.get_attribute("normal_attribute"), "2")

        # clears the internal structure and tests that it has been cleared correctly
        intermediate_structure.remove_entity(first_entity)
        intermediate_structure.remove_entity(second_entity)
        self.assertEquals(len(intermediate_structure.get_entities("dummy_entity")), 0)
        self.assertEquals(intermediate_structure.has_entity(first_entity_index), False)
        self.assertEquals(intermediate_structure.has_entity(second_entity_index), False)
        self.assertEquals(len(intermediate_structure.entities), 0)
        self.assertEquals(len(intermediate_structure.store_map.keys()), 1)
        self.assertEquals(len(intermediate_structure.index_map.keys()), 0)

        # closes the intermediate structure thereby persisting it
        intermediate_structure.save(io_adapter_plugin_id, load_save_options)

        # re-opens the intermediate structure
        intermediate_structure.load(io_adapter_plugin_id, load_save_options)

        # tests that the intermediate structure is still cleared
        self.assertEquals(len(intermediate_structure.get_entities("dummy_entity")), 0)
        self.assertEquals(intermediate_structure.has_entity(first_entity_index), False)
        self.assertEquals(intermediate_structure.has_entity(second_entity_index), False)
        self.assertEquals(len(intermediate_structure.entities), 0)
        self.assertEquals(len(intermediate_structure.store_map.keys()), 1)
        self.assertEquals(len(intermediate_structure.index_map.keys()), 0)

        # closes the intermediate structure
        intermediate_structure.save(io_adapter_plugin_id, load_save_options)

    def tearDown(self):
        self.plugin.info("Tearing down Io Adapter Csv Test Case...")

        # removes the files created in the test
        if os.path.exists(self.test_intermediate_structure_file_path):
            os.remove(self.test_intermediate_structure_file_path)

class IoAdapterCsvTestPluginTestCase:

    @staticmethod
    def get_related_class():
        return pt.hive.colony.plugins.DataConverterIoAdapterCsvPlugin

    @staticmethod
    def get_test_case():
        return IoAdapterCsvTestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "Io Adapter Csv Test Plugin test case covering the data converter input output csv testing"
