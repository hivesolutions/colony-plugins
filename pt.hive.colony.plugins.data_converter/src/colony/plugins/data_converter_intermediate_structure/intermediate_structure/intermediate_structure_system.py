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

import sys
import os.path

import intermediate_structure_exceptions

class IntermediateStructure:
    """
    Intermediate structure used to hold the results of each conversion step.
    """

    intermediate_structure_plugin = None
    """ The data converter intermediate structure plugin """

    next_object_id = 1
    """ The next unique identifier that will be assigned to a new entity """

    entities = []
    """ List used to store the entities in the order they were created """

    store_map = {}
    """ Dictionary used to store the intermediate structure sorted by entity name """

    index_map = {}
    """ Dictionary used to store the intermediate structure index """

    def __init__(self, intermediate_structure_plugin):
        """
        Class constructor.

        @type intermediate_structure_plugin: IntermediateStructurePlugin
        @param intermediate_structure_plugin: Intermediate structure plugin.
        """

        self.intermediate_structure_plugin = intermediate_structure_plugin
        self.next_object_id = 1
        self.entities = []
        self.store_map = {}
        self.index_map = {}

    def configure(self):
        """
        Configures the intermediate structure to adhere to the specified schema.
        """

        self.next_object_id = 1
        self.entities = []
        self.index_map = {}

        # resets the store map without destroying the configured schema
        for entity_name in self.store_map:
            self.store_map[entity_name] = []

    def load(self, io_adapter_plugin_id, options):
        """
        Populates the intermediate structure with data retrieved from the csv source specified in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the provided intermediate structure.
        """

        # retrieves the specified input output adapter plugin
        input_adapter_plugin = None
        for io_adapter_plugin in self.intermediate_structure_plugin.io_adapter_plugins:
            if io_adapter_plugin_id == io_adapter_plugin.id:
                input_adapter_plugin = io_adapter_plugin

        # raises an exception in case the specified io adapter plugin was not found
        if not input_adapter_plugin:
            raise intermediate_structure_exceptions.IntermediateStructurePluginMissing("IntermediateStructure.load - Specified input output adapter plugin was not found (io_adapter_plugin = %s)" % io_adapter_plugin_id)

        # resets the intermediate structure's state
        self.configure()

        # redirects the load request to the specified input output adapter
        input_adapter_plugin.load(self, options)

    def save(self, io_adapter_plugin_id, options):
        """
        Saves the intermediate structure to a file in csv format at the location and with characteristics defined in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure into csv format.
        """

        # retrieves the specified input output adapter plugin
        output_adapter_plugin = None
        for io_adapter_plugin in self.intermediate_structure_plugin.io_adapter_plugins:
            if io_adapter_plugin_id == io_adapter_plugin.id:
                output_adapter_plugin = io_adapter_plugin

        # raises an exception in case the specified io adapter plugin was not found
        if not output_adapter_plugin:
            raise intermediate_structure_exceptions.IntermediateStructurePluginMissing("IntermediateStructure.save - Specified input output adapter plugin was not found (io_adapter_plugin = %s)" % io_adapter_plugin_id)

        # redirects the save request to the specified input output adapter
        output_adapter_plugin.save(self, options)

    def has_entities(self, entity_name):
        """
        Indicates if the intermediate structure is configured to store entities with the specified name.

        @rtype: bool
        @return: Boolean indicating if the intermediate structure is configured to store entities with the specified name.
        """

        return entity_name in self.store_map

    def get_entities(self, entity_name = None):
        """
        Retrieves all entities, or all entities with the specified name.

        @type: str
        @param entity_name: Optional string specifying the name the retrieved entities must have.
        @rtype: List
        @return: List with the intermediate structure's entities.
        """

        # @todo: re-enable exception when intermediate structure supports configuration
        # raises an exception in case the specified entity is not found in the store
        # if entity_name and not entity_name in self.store_map:
        #    raise intermediate_structure_exceptions.IntermediateStructureEntityNotAllowed("IntermediateStructure.get_entities - Intermediate structure was not configured to support entities with the specified name (entity_name = %s)" % entity_name)

        # retrieves the specified entity instances that exist in the intermediate structure
        if entity_name:
            entities = self.store_map[entity_name]
        else:
            entities = self.entities

        return entities

    def has_entity(self, index):
        """
        Indicates if the specified entity exists in the intermediate structure.

        @type: str
        @param index: Index that the entity is indexed by in the intermediate structure.
        @rtype: bool
        @return: Boolean indicating if the entity exists in the intermediate structure.
        """

        return index in self.index_map

    def get_entity(self, index):
        """
        Returns the specified entity from the intermediate structure.

        @type: str
        @param index: Index that the entity is indexed by in the intermediate structure.
        @rtype: Entity
        @return: The specified intermediate structure entity.
        """

        # raises and exception in case the specified entity is not found in the index
        if not index in self.index_map:
            raise intermediate_structure_exceptions.IntermediateStructureEntityNotFound("IntermediateStructure.get_entity - Intermediate structure index doesn't have the specified entity (index = %s)" % index)

        # retrieves the specified entity from the intermediate structure's index
        entity = self.index_map[index]

        return entity

    def create_entity(self, entity_name):
        """
        Creates an entity with the specified name in the intermediate structure.

        @type: str
        @param entity_name: Name of the entity one wants to create.
        @rtype: Entity
        @return: The specified intermediate structure entity.
        """

        # creates an entity with the specified name and adds it to the
        # intermediate structure
        entity = Entity(self.next_object_id, entity_name)
        self.add_entity(entity)

        # increments the next object id so the next created entity
        # receives an object id different from this one
        self.next_object_id += 1

        return entity

    def add_entity(self, entity):
        """
        Adds the provided entity to the intermediate structure.

        @type: Entity
        @param entity: Entity to add to the intermediate structure.
        """

        entity_name = entity.get_name()

        # @todo: re-enable exception when intermediate structure supports configuration
        # raises an exception in case the intermediate structure was not configured to support entities with the specified name
        # if not self.has_entities(entity_name):
        #    raise intermediate_structure_exceptions.IntermediateStructureEntityNotAllowed("IntermediateStructure.add_entity - Intermediate structure was not configured to support entities with the specified name (entity_name = %s)" % entity_name)
        if not entity_name in self.store_map:
            self.store_map[entity_name] = []

        # adds the entity to the store
        entities = self.store_map[entity_name]
        entities.append(entity)
        self.store_map[entity_name] = entities

        # adds the entity to the ordered list
        self.entities.append(entity)

    def index_entity(self, entity, index):
        """
        Indexes an intermediate structure entity with the specified index.

        @type: Entity
        @param entity: Entity to index.
        @type: str
        @param index: Index with which to index the entity by.
        """

        # raises an exception in case an entity is already occupying the specified index position
        if index in self.index_map:
            raise intermediate_structure_exceptions.IntermediateStructureIndexOcuppied("IntermediateStructure.index_entity - An entity is already indexed with the specified key (index = %s)" % index)

        # indexes the entity by the specified key
        self.index_map[index] = entity
        entity.indexes.append(index)

    def remove_entity(self, entity):
        """
        Removes the specified entity from the intermediate structure.

        @type: Entity
        @param entity: Entity one wants to remove from the intermediate structure.
        """

        # raises an exception in case the entity isn't found
        if not entity in self.entities:
            raise intermediate_structure_exceptions.IntermediateStructureEntityNotFound("IntermediateStructure.remove_entity - Intermediate structure doesn't have the specified entity")

        # removes the entity from the ordered list
        self.entities.remove(entity)

        # removes the entity from the store
        entity_name = entity.get_name()
        entities = self.store_map[entity_name]
        entities.remove(entity)
        self.store_map[entity_name] = entities

        # removes the entity from the index
        for index in entity.indexes:
            del self.index_map[index]

class Entity:

    object_id = None
    """ The entity's unique identifier in the intermediate structure """

    name = None
    """ The name of the entity """

    indexes = []
    """ The indexes this entity is indexed by in the intermediate structure """

    attribute_name_value_map = {}
    """ Dictionary associating the name of an attribute with its value """

    def __init__(self, object_id, name):
        """
        Class constructor.

        @type object_id: int
        @param object_id: Unique identifier for the entity in the intermediate structure.
        @type name: str
        @param name: Name of the entity.
        """

        self.object_id = object_id
        self.name = name
        self.indexes = []
        self.attribute_name_value_map = {}

    def get_object_id(self):
        """
        Returns the unique identifier for this entity in the intermediate structure.

        @rtype: int
        @return: Unique identifier for this entity in the intermediate structure.
        """

        return self.object_id

    def get_name(self):
        """
        Returns the name for this entity in the intermediate structure.

        @rtype: str
        @return: Name of the entity in the intermediate structure.
        """

        return self.name

    def has_attribute(self, attribute_name):
        """
        Indicates if the entity is configured to have the specified attribute.

        @type: str
        @param attribute_name: Name of the attribute one wants to know if its exists in the entity.
        @rtype: bool
        @return: Boolean indicating if the attribute exists in the entity.
        """

        return attribute_name in self.attribute_name_value_map

    def get_attribute(self, attribute_name):
        """
        Retrieves the value of the specified entity attribute.

        @type: str
        @param attribute_name: Name of the attribute whose value one wants to retrieve from the entity.
        @return: Retrieves the value of the specified attribute.
        """

        # @todo: re-enable exception when intermediate structure supports configuration
        # raises an exception if the specified attribute does not exist
        #if not attribute_name in self.attribute_name_value_map:
        #    raise intermediate_structure_exceptions.IntermediateStructureEntityAttributeNotAllowed("IntermediateStructure.get_attribute - Intermediate structure entity was not configured to support attributes with the specified name (entity_name = %s, attribute_name = %s)" % (self.name, attribute_name))

        # retrieves the attribute value
        attribute_value = self.attribute_name_value_map[attribute_name]

        return attribute_value

    def set_attribute(self, attribute_name, attribute_value):
        """
        Sets the value for an entity's attribute.

        @type: str
        @param attribute_name: Name of the attribute whose value one wants to set in the entity.
        @param attribute_value: Attribute value one wants to set.
        """

        # @todo: re-enable exception when intermediate structure supports configuration
        # raises an exception if the specified attribute does not exist
        #if not attribute_name in self.attribute_name_value_map:
        #    raise intermediate_structure_exceptions.IntermediateStructureEntityAttributeNotAllowed("IntermediateStructure.set_attribute - Intermediate structure entity was not configured to support attributes with the specified name (entity_name = %s, attribute_name = %s)" % (self.name, attribute_name))

        self.attribute_name_value_map[attribute_name] = attribute_value
