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

class IoAdapterEntityManagerTest:
    """
    The input output entity manager test plugin unit test class.
    """

    io_adapter_entity_manager_test_plugin = None
    """ The input output entity manager test plugin """

    entity_bundle = []
    """ The bundle containing the entity classes """

    entity_bundle_map = {}
    """ The map associating the entity classes with their names """

    def __init__(self, io_adapter_entity_manager_test_plugin):
        """
        Constructor of the class.

        @type io_adapter_entity_manager_test_plugin: IoAdapterEntityManagerTestPlugin
        @param io_adapter_entity_manager_test_plugin: The input output entity manager test plugin.
        """

        self.io_adapter_entity_manager_test_plugin = io_adapter_entity_manager_test_plugin
        self.entity_bundle = []
        self.entity_bundle_map = {}

    def get_plugin_test_case_bundle(self):
        return [IoAdapterEntityManagerTestPluginTestCase]

    def generate_classes(self):
        # retrieves the business helper plugin
        business_helper_plugin = self.io_adapter_entity_manager_test_plugin.business_helper_plugin

        # creates the list of global values
        global_values = []

        # retrieves the base directory name
        base_directory_name = self.get_path_directory_name()

        # imports the classes module
        business_helper_plugin.import_class_module("io_adapter_entity_manager_test_data_classes", globals(), locals(), global_values, base_directory_name)

        # sets the entity bundle
        self.entity_bundle = [FirstEntity, SecondEntity]

        # creates the entity bundle map
        entity_bundle_map = {}

        # iterates over all the classes in the entity bundle
        for entity_class in self.entity_bundle:
            # retrieves the entity class name
            entity_class_name = entity_class.__name__

            # sets the class in the entity bundle map
            entity_bundle_map[entity_class_name] = entity_class

        # sets the entity bundle map
        self.entity_bundle_map = entity_bundle_map

    def get_entity_bundle(self):
        return self.entity_bundle

    def get_entity_bundle_map(self):
        return self.entity_bundle_map

    def get_path_directory_name(self):
        return os.path.dirname(__file__)

class IoAdapterEntityManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin.info("Setting up Io Adapter Entity Manager Test Case...")

        # retrieves the resource manager plugin
        resource_manager_plugin = self.plugin.resource_manager_plugin

        # retrieves the user home path resource
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")

        # retrieves the user home path value
        user_home_path = user_home_path_resource.data

        # creates the path where to store the serialized intermediate structures used in the test
        self.test_intermediate_structure_file_path = os.path.join(user_home_path, "test_intermediate_structure.db")

        # retrieves the intermediate structure plugin
        self.intermediate_structure_plugin = self.plugin.intermediate_structure_plugin

    def test_intermediate_structure_entity_manager(self):
        # creates an intermediate structure instance
        intermediate_structure = self.intermediate_structure_plugin.create_intermediate_structure()
        self.assertNotEquals(intermediate_structure, None)

        # defines the options that will be provided to the load and save operations
        io_adapter_plugin_id = "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.entity_manager"
        load_save_options = {"file_path" : self.test_intermediate_structure_file_path,
                             "entity_manager_engine" : "sqlite"}

        # creates two entities and indexes them
        first_entity = intermediate_structure.create_entity("FirstEntity")
        second_entity = intermediate_structure.create_entity("SecondEntity")
        first_entity_replica = intermediate_structure.create_entity("FirstEntity")
        second_entity_replica = intermediate_structure.create_entity("SecondEntity")

        # retrieves the previously created entities
        first_entity = intermediate_structure.get_entity(str((first_entity.get_name(), "object_id", first_entity.get_object_id())))
        second_entity = intermediate_structure.get_entity(str((second_entity.get_name(), "object_id", second_entity.get_object_id())))

        # sets the first entity's attributes
        self.assertEquals(first_entity.get_object_id(), 1)
        self.assertEquals(first_entity.get_name(), "FirstEntity")
        first_entity.set_attribute("attribute", 1)
        self.assertEquals(first_entity.has_attribute("attribute"), True)
        self.assertEquals(first_entity.get_attribute("attribute"), 1)
        first_entity.set_attribute("second_entity", second_entity)
        self.assertEquals(first_entity.has_attribute("second_entity"), True)
        self.assertEquals(first_entity.get_attribute("second_entity"), second_entity)
        first_entity.set_attribute("second_entities", [second_entity, second_entity_replica])
        self.assertEquals(first_entity.get_attribute("second_entities"), [second_entity, second_entity_replica])

        # sets the second entity's attributes
        self.assertEquals(second_entity.get_object_id(), 2)
        self.assertEquals(second_entity.get_name(), "SecondEntity")
        second_entity.set_attribute("attribute", 2)
        self.assertEquals(second_entity.has_attribute("attribute"), True)
        self.assertEquals(second_entity.get_attribute("attribute"), 2)
        second_entity.set_attribute("first_entity", first_entity)
        self.assertEquals(second_entity.has_attribute("first_entity"), True)
        self.assertEquals(second_entity.get_attribute("first_entity"), first_entity)
        second_entity.set_attribute("first_entities", [first_entity, first_entity_replica])
        self.assertEquals(second_entity.get_attribute("first_entities"), [first_entity, first_entity_replica])

        # sets the first entity replica's attributes
        self.assertEquals(first_entity_replica.get_object_id(), 3)
        self.assertEquals(first_entity_replica.get_name(), "FirstEntity")
        first_entity_replica.set_attribute("attribute", 3)
        self.assertEquals(first_entity_replica.has_attribute("attribute"), True)
        self.assertEquals(first_entity_replica.get_attribute("attribute"), 3)
        first_entity_replica.set_attribute("second_entity", None)
        self.assertEquals(first_entity_replica.has_attribute("second_entity"), True)
        self.assertEquals(first_entity_replica.get_attribute("second_entity"), None)
        first_entity_replica.set_attribute("second_entities", [second_entity])
        self.assertEquals(first_entity_replica.get_attribute("second_entities"), [second_entity])

        # sets the second entity replica's attributes
        self.assertEquals(second_entity_replica.get_object_id(), 4)
        self.assertEquals(second_entity_replica.get_name(), "SecondEntity")
        second_entity_replica.set_attribute("attribute", 4)
        self.assertEquals(second_entity_replica.has_attribute("attribute"), True)
        self.assertEquals(second_entity_replica.get_attribute("attribute"), 4)
        second_entity_replica.set_attribute("first_entity", None)
        self.assertEquals(second_entity_replica.has_attribute("first_entity"), True)
        self.assertEquals(second_entity_replica.get_attribute("first_entity"), None)
        second_entity_replica.set_attribute("first_entities", [first_entity])
        self.assertEquals(second_entity_replica.get_attribute("first_entities"), [first_entity])

        # closes the intermediate structure thereby persisting it
        self.intermediate_structure_plugin.save(intermediate_structure, io_adapter_plugin_id, load_save_options)

        # re-opens the intermediate structure
        self.intermediate_structure_plugin.load(intermediate_structure, io_adapter_plugin_id, load_save_options)

        # tests the intermediate structure
        entities = intermediate_structure.get_entities("FirstEntity")
        self.assertEquals(len(entities), 2)
        entities = intermediate_structure.get_entities("SecondEntity")
        self.assertEquals(len(entities), 2)
        entities = intermediate_structure.get_entities()
        self.assertEquals(len(entities), 4)

        # retrieves the previously saved entities
        first_entity = None
        second_entity = None
        first_entity_replica = None
        second_entity_replica = None
        for entity in entities:
            self.assertEquals(entity.has_attribute("attribute"), True)
            if entity.get_attribute("attribute") == 1:
                first_entity = entity
            elif entity.get_attribute("attribute") == 2:
                second_entity = entity
            elif entity.get_attribute("attribute") == 3:
                first_entity_replica = entity
            elif entity.get_attribute("attribute") == 4:
                second_entity_replica = entity

        # tests if all entities were retrieved
        self.assertNotEquals(first_entity, None)
        self.assertNotEquals(second_entity, None)
        self.assertNotEquals(first_entity_replica, None)
        self.assertNotEquals(second_entity_replica, None)

        # tests the first entity
        self.assertNotEquals(first_entity, None)
        self.assertEquals(first_entity.get_name(), "FirstEntity")
        self.assertEquals(first_entity.has_attribute("second_entity"), True)
        self.assertEquals(first_entity.get_attribute("second_entity"), second_entity)
        self.assertEquals(first_entity.has_attribute("second_entities"), True)
        self.assertEquals(first_entity.get_attribute("second_entities"), [second_entity, second_entity_replica])

        # tests the second entity
        self.assertNotEquals(second_entity, None)
        self.assertEquals(second_entity.get_name(), "SecondEntity")
        self.assertEquals(second_entity.has_attribute("first_entity"), True)
        self.assertEquals(second_entity.get_attribute("first_entity"), first_entity)
        self.assertEquals(second_entity.has_attribute("first_entities"), True)
        self.assertEquals(second_entity.get_attribute("first_entities"), [first_entity, first_entity_replica])

        # clears the internal structure and tests that it has been cleared correctly
        intermediate_structure.remove_entity(first_entity)
        intermediate_structure.remove_entity(second_entity)
        intermediate_structure.remove_entity(first_entity_replica)
        intermediate_structure.remove_entity(second_entity_replica)
        self.assertEquals(intermediate_structure.has_entities("FirstEntity"), False)
        self.assertEquals(intermediate_structure.has_entity(str((first_entity.get_name(), "object_id", first_entity.get_object_id()))), False)
        self.assertEquals(intermediate_structure.has_entity(str((first_entity_replica.get_name(), "object_id", first_entity_replica.get_object_id()))), False)
        self.assertEquals(intermediate_structure.has_entities("SecondEntity"), False)
        self.assertEquals(intermediate_structure.has_entity(str((second_entity.get_name(), "object_id", second_entity.get_object_id()))), False)
        self.assertEquals(intermediate_structure.has_entity(str((second_entity_replica.get_name(), "object_id", second_entity_replica.get_object_id()))), False)
        self.assertEquals(len(intermediate_structure.entities), 0)
        self.assertEquals(len(intermediate_structure.entity_name_entities_map.keys()), 0)
        self.assertEquals(len(intermediate_structure.index_entity_map.keys()), 0)

    def tearDown(self):
        self.plugin.info("Tearing down Io Adapter Entity Manager Test Case...")

        # removes the files created in the test
        if os.path.exists(self.test_intermediate_structure_file_path):
           os.remove(self.test_intermediate_structure_file_path)

class IoAdapterEntityManagerTestPluginTestCase:

    @staticmethod
    def get_related_class():
        return pt.hive.colony.plugins.DataConverterIoAdapterEntityManagerPlugin

    @staticmethod
    def get_test_case():
        return IoAdapterEntityManagerTestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "Io Adapter Entity Manager Test Plugin test case covering the data converter input output entity manager testing"
