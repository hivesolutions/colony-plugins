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
        self.test_intermediate_structure_file_path = os.path.join(user_home_path, "test_intermediate_structure.pickle")

    def test_convert_data(self):
        # creates the input intermediate structure where to start the conversion from
        intermediate_structure = self.intermediate_structure_plugin.create_intermediate_structure()
        dummy_entity = intermediate_structure.create_entity("dummy_entity")
        dummy_entity.set_attribute("attribute_1", "attribute_1_value")
        self.assertEquals(dummy_entity.get_attribute("attribute_1"), "attribute_1_value")
        dummy_entity.set_attribute("attribute_2", " attribute_2_value")
        self.assertEquals(dummy_entity.get_attribute("attribute_2"), " attribute_2_value")
        dummy_entity = intermediate_structure.create_entity("dummy_entity")
        dummy_entity.set_attribute("attribute_1", "attribute_1_value")
        self.assertEquals(dummy_entity.get_attribute("attribute_1"), "attribute_1_value")
        dummy_entity.set_attribute("attribute_2", " attribute_2_value")
        self.assertEquals(dummy_entity.get_attribute("attribute_2"), " attribute_2_value")

        # defines the output options
        input_output_options = {"io_adapter_plugin_id" : "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.pickle",
                                "file_path" : self.test_intermediate_structure_file_path}

        # saves the input intermediate structure
        self.intermediate_structure_plugin.save(intermediate_structure, "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.pickle", input_output_options)

        # defines the conversion options
        conversion_options = {"attribute_mapping" : {"intermediate_entities" : [{"name" : "dummy_entity",
                                                                                 "remote_entities" : [{"name" : "mock_entity",
                                                                                                       "validators" : [self.is_valid_entity],
                                                                                                       "handlers" : [self.entity_handler],
                                                                                                       "index" : [("constant", "object_id"), ("function", self.get_entity_object_id), ("input_attribute", "attribute_1"), ("output_attribute", "mock_attribute_1")],
                                                                                                       "remote_attributes" : [{"name" : "mock_attribute_1",
                                                                                                                               "attribute_name" : "attribute_1",
                                                                                                                               "validators" : [self.is_valid_attribute],
                                                                                                                               "handlers" : [self.attribute_handler]},
                                                                                                                              {"name" : "mock_attribute_2",
                                                                                                                               "attribute_name" : "attribute_2"}]},
                                                                                                      {"name" : "mock_entity",
                                                                                                       "validators" : [self.is_valid_entity],
                                                                                                       "handlers" : [self.entity_handler],
                                                                                                       "index" : [("constant", "object_id"), ("function", self.get_entity_object_id), ("input_attribute", "attribute_1"), ("output_attribute", "mock_attribute_1")],
                                                                                                       "remote_attributes" : [{"name" : "mock_attribute_1",
                                                                                                                               "attribute_name" : "attribute_1",
                                                                                                                               "validators" : [self.is_valid_attribute],
                                                                                                                               "handlers" : [self.attribute_handler]},
                                                                                                                              {"name" : "mock_attribute_2",
                                                                                                                               "attribute_name" : "attribute_2"}]}]}]}}

        # converts the data
        self.data_converter_plugin.convert_data(input_output_options, input_output_options, conversion_options)

        # loads the results of the data conversion operation
        self.intermediate_structure_plugin.load(intermediate_structure, "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.pickle", input_output_options)

        # retrieves the previously created entities
        entities = intermediate_structure.get_entities()
        self.assertEquals(len(entities), 4)
        dummy_entities = []
        mock_entities = []
        for entity in entities:
            entity_name = entity.get_name()
            if entity_name == "dummy_entity":
                dummy_entities.append(entity)
            elif entity_name == "mock_entity":
                mock_entities.append(entity)
        self.assertEquals(len(dummy_entities), 0)
        self.assertEquals(len(mock_entities), 4)

        # tests that all mock entities have two mock attributes with the same value as their object id
        for mock_entity in mock_entities:
            self.assertEquals(len(mock_entity.get_attributes().keys()), 2)
            self.assertEquals(mock_entity.has_attribute("mock_attribute_1"), True)
            self.assertEquals(mock_entity.get_attribute("mock_attribute_1"), "Attribute_1_value")
            self.assertEquals(mock_entity.has_attribute("mock_attribute_2"), True)
            self.assertEquals(mock_entity.get_attribute("mock_attribute_2"), "attribute_2_value")
            mock_entity_index = ("object_id", mock_entity.get_object_id(), "attribute_1_value", "Attribute_1_value")
            mock_entity = self.data_converter_plugin.data_converter.get_entity(mock_entity_index)
            self.assertEquals(len(mock_entity.get_attributes().keys()), 2)
            self.assertEquals(mock_entity.has_attribute("mock_attribute_1"), True)
            self.assertEquals(mock_entity.get_attribute("mock_attribute_1"), "Attribute_1_value")
            self.assertEquals(mock_entity.has_attribute("mock_attribute_2"), True)
            self.assertEquals(mock_entity.get_attribute("mock_attribute_2"), "attribute_2_value")

    def tearDown(self):
        self.plugin.info("Tearing down Data Converter Test Case...")

        # removes the test intermediate structure file
        if os.path.exists(self.test_intermediate_structure_file_path):
            os.remove(self.test_intermediate_structure_file_path)

    def is_valid_entity(self, entity):
        return True

    def entity_handler(self, entity):
        attribute_value = entity.get_attribute("mock_attribute_2")
        attribute_value = attribute_value.strip()
        entity.set_attribute("mock_attribute_2", attribute_value)

        return entity

    def is_valid_attribute(self, attribute_value):
        return True

    def attribute_handler(self, attribute_value):
        return attribute_value.capitalize()

    def get_entity_object_id(self, input_entity, output_entity):
        return output_entity.get_object_id()

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
