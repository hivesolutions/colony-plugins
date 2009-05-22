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

__revision__ = "$LastChangedRevision: 1026 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-01-19 23:05:23 +0000 (seg, 19 Jan 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import unittest
import os.path

class DataConverterTest:
    """
    The data converter plugin unit test class.
    """

    data_converter_test_plugin = None
    """ The base data test plugin """

    def __init__(self, data_converter_test_plugin):
        """
        Constructor of the class.

        @type data_converter_test_plugin: DataConverterTestPlugin
        @param data_converter_test_plugin: The data converter test plugin.
        """

        self.data_converter_test_plugin = data_converter_test_plugin

    def get_plugin_test_case_bundle(self):
        return [DataConverterTestPluginTestCase]

class DataConverterTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin.info("Setting up Data Converter Test Case...")

        # retrieves the resource manager plugin
        resource_manager_plugin = self.plugin.resource_manager_plugin

        # retrieves the user home path resource
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")

        # retrieves the user home path value
        user_home_path = user_home_path_resource.data

        # retrieves the data converter plugin
        self.data_converter_plugin = self.plugin.data_converter_plugin

        # retrieves the intermediate structure plugin
        self.intermediate_structure_plugin = self.plugin.intermediate_structure_plugin

        # creates the path where to store the serialized input intermediate structures used in the test
        self.test_input_intermediate_structure_file_path = os.path.join(user_home_path, "test_input_intermediate_structure")

        # creates the path where to store the serialized input intermediate structures used in the test
        self.test_output_intermediate_structure_file_path = os.path.join(user_home_path, "test_output_intermediate_structure")

    def test_convert_data_csv_to_pickle(self):
        # defines the csv schema
        entity_names = ["dummy_entity", "dummy_entity"]
        entity_name_attribute_names_map = {"dummy_entity" : ["normal_attribute"],
                                           "dummy_entity" : ["normal_attribute"]}

        # creates test csv data
        file_data = ""
        for entity_index in range(len(entity_names)):
            entity_name = entity_names[entity_index]
            attribute_names = entity_name_attribute_names_map[entity_name]
            for attribute_index in range(len(attribute_names)):
                file_data += "%s;" % (entity_index + 1)
        file_data = file_data[:-1]

        # writes the test csv data to the test csv file
        file = open(self.test_input_intermediate_structure_file_path, "w")
        file.write(file_data)
        file.close()

        # defines the input options
        input_options = {"io_adapter_plugin_id" : "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.csv",
                         "file_path" : self.test_input_intermediate_structure_file_path,
                         "entity_names" : entity_names,
                         "entity_name_attribute_names" : entity_name_attribute_names_map,
                         "csv_token_separator" : ";"}

        # defines the output options
        output_options = {"io_adapter_plugin_id" : "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.pickle",
                          "file_path" : self.test_output_intermediate_structure_file_path}

        # defines the conversion options
        conversion_options = {}

        # converts the data
        self.data_converter_plugin.convert_data(input_options, output_options, conversion_options)

        # creates an intermediate structure instance
        intermediate_structure = self.intermediate_structure_plugin.create_intermediate_structure()
        self.assertNotEquals(intermediate_structure, None)

        # loads the results of the data conversion operation
        self.intermediate_structure_plugin.load(intermediate_structure, "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.pickle", output_options)

        # retrieves the previously created entities
        entities = intermediate_structure.get_entities()
        self.assertEquals(len(entities), 2)
        first_entity = entities[0]
        second_entity = entities[1]

        # sets the first entity's attributes
        self.assertEquals(first_entity.get_object_id(), 1)
        self.assertEquals(first_entity.get_name(), "dummy_entity")
        first_entity.set_attribute("normal_attribute", 1)
        self.assertEquals(first_entity.has_attribute("normal_attribute"), True)
        self.assertEquals(first_entity.get_attribute("normal_attribute"), 1)

        # sets the second entity's attributes
        self.assertEquals(second_entity.get_object_id(), 2)
        self.assertEquals(second_entity.get_name(), "dummy_entity")
        second_entity.set_attribute("normal_attribute", 2)
        self.assertEquals(second_entity.has_attribute("normal_attribute"), True)
        self.assertEquals(second_entity.get_attribute("normal_attribute"), 2)

    def tearDown(self):
        self.plugin.info("Tearing down Data Converter Test Case...")

        # removes the test input file
        if os.path.exists(self.test_input_intermediate_structure_file_path):
            os.remove(self.test_input_intermediate_structure_file_path)

        # removes the test output file
        if os.path.exists(self.test_output_intermediate_structure_file_path):
            os.remove(self.test_output_intermediate_structure_file_path)

class DataConverterTestPluginTestCase:

    @staticmethod
    def get_related_class():
        return pt.hive.colony.plugins.DataConverterPlugin

    @staticmethod
    def get_test_case():
        return DataConverterTestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "Data Converter Test Plugin test case covering the data converter testing"
