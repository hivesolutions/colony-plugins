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

class IntermediateStructureTest:
    """
    The intermediate structure test plugin unit test class.
    """

    data_converter_intermediate_structure_test_plugin = None
    """ The intermediate structure test plugin """

    def __init__(self, data_converter_intermediate_structure_test_plugin):
        """
        Constructor of the class.

        @type data_converter_intermediate_structure_test_plugin: DataConverterIntermediateStructurePlugin
        @param data_converter_intermediate_structure_test_plugin: The intermediate structure test plugin.
        """

        self.data_converter_intermediate_structure_test_plugin = data_converter_intermediate_structure_test_plugin

    def get_plugin_test_case_bundle(self):
        return [IntermediateStructureTestPluginTestCase]

class IntermediateStructureTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin.info("Setting up Intermediate Structure Test Case...")

        # retrieves the resource manager plugin
        resource_manager_plugin = self.plugin.resource_manager_plugin

        # retrieves the user home path resource
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")

        # retrieves the user home path value
        user_home_path = user_home_path_resource.data

        # retrieves the intermediate structure plugin
        self.intermediate_structure_plugin = self.plugin.intermediate_structure_plugin

    def test_intermediate_structure(self):
        # creates an intermediate structure instance
        configuration_map = {"dummy_entity" : {"normal_attribute" : {"default_value" : -1,
                                                                     "type" : "integer"},
                                               "relation_attribute" : {"default_value" : None,
                                                                       "type" : "instance"}}}
        intermediate_structure = self.intermediate_structure_plugin.create_intermediate_structure(configuration_map)
        self.assertNotEquals(intermediate_structure, None)

        first_entity_index = str(("dummy_entity", 1))
        second_entity_index = str(("dummy_entity", 2))

        # creates two entities and indexes them
        first_entity = intermediate_structure.create_entity("dummy_entity")
        self.assertEquals(first_entity.get_attribute("normal_attribute"), -1)
        second_entity = intermediate_structure.create_entity("dummy_entity")
        self.assertEquals(second_entity.get_attribute("relation_attribute"), None)
        intermediate_structure.index_entity(first_entity, first_entity_index)
        intermediate_structure.index_entity(second_entity, second_entity_index)

        # retrieves the previously created entities
        first_entity = intermediate_structure.get_entity(first_entity_index)
        second_entity = intermediate_structure.get_entity(second_entity_index)

        # sets the first entity's attributes
        self.assertEquals(first_entity.get_object_id(), 1)
        self.assertEquals(first_entity.get_name(), "dummy_entity")
        first_entity.set_attribute("normal_attribute", 1)
        self.assertEquals(first_entity.has_attribute("normal_attribute"), True)
        self.assertEquals(first_entity.get_attribute("normal_attribute"), 1)
        first_entity.set_attribute("relation_attribute", second_entity)
        self.assertEquals(first_entity.has_attribute("relation_attribute"), True)
        self.assertEquals(first_entity.get_attribute("relation_attribute"), second_entity)
        self.assertTrue("normal_attribute" in first_entity.get_attributes())
        self.assertEquals(first_entity.get_attributes()["normal_attribute"], 1)
        self.assertTrue("relation_attribute" in first_entity.get_attributes())
        self.assertEquals(first_entity.get_attributes()["relation_attribute"], second_entity)

        # sets the second entity's attributes
        self.assertEquals(second_entity.get_object_id(), 2)
        self.assertEquals(second_entity.get_name(), "dummy_entity")
        second_entity.set_attribute("normal_attribute", 2)
        self.assertEquals(second_entity.has_attribute("normal_attribute"), True)
        self.assertEquals(second_entity.get_attribute("normal_attribute"), 2)
        second_entity.set_attribute("relation_attribute", first_entity)
        self.assertEquals(second_entity.has_attribute("relation_attribute"), True)
        self.assertEquals(second_entity.get_attribute("relation_attribute"), first_entity)
        self.assertTrue("normal_attribute" in second_entity.get_attributes())
        self.assertEquals(second_entity.get_attributes()["normal_attribute"], 2)
        self.assertTrue("relation_attribute" in second_entity.get_attributes())
        self.assertEquals(second_entity.get_attributes()["relation_attribute"], first_entity)

        # clears the internal structure and tests that it has been cleared correctly
        intermediate_structure.remove_entity(first_entity)
        intermediate_structure.remove_entity(second_entity)
        self.assertEquals(len(intermediate_structure.get_entities("dummy_entity")), 0)
        self.assertEquals(intermediate_structure.has_entity(first_entity_index), False)
        self.assertEquals(intermediate_structure.has_entity(second_entity_index), False)
        self.assertEquals(len(intermediate_structure.entities), 0)
        self.assertEquals(len(intermediate_structure.entity_name_entities_map.keys()), 1)
        self.assertEquals(len(intermediate_structure.index_entity_map.keys()), 0)

    def tearDown(self):
        self.plugin.info("Tearing down Intermediate Structure Test Case...")

class IntermediateStructureTestPluginTestCase:

    @staticmethod
    def get_related_class():
        return pt.hive.colony.plugins.DataConverterIntermediateStructurePlugin

    @staticmethod
    def get_test_case():
        return IntermediateStructureTestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "Data Converter Intermediate Structure Plugin test case covering the data converter intermediate structure testing"
