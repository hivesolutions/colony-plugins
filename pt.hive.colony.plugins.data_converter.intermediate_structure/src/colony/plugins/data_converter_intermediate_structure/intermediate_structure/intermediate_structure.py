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
import types
import os.path

import intermediate_structure_exceptions

class IntermediateStructure:
    """
    Intermediate structure used to hold the results of each conversion step.
    """

    next_object_id = 1
    """ The next unique identifier that will be assigned to a new entity """

    entities = []
    """ List used to store the entities in the order they were created """

    entity_name_entities_map = {}
    """ Dictionary used to store the intermediate structure sorted by entity name """

    index_entity_map = {}
    """ Dictionary used to store the intermediate structure index """

    configuration_map = None
    """ Map used to configure the intermediate structure to obey to a certain schema """

    def __init__(self, configuration_map = None):
        """
        Class constructor.

        @type configuration_map: Dictionary
        @param configuration_map: Optional map defining the intermediate structure's schema.
        """

        self.next_object_id = 1
        self.entities = []
        self.entity_name_entities_map = {}
        self.index_entity_map = {}
        self.configuration_map = configuration_map

        # creates storage in the store for each configured entity name
        if self.configuration_map:
            for entity_name in configuration_map:
                self.entity_name_entities_map[entity_name] = []

    def reset(self):
        """
        Resets the intermediate structure.
        """

        self.next_object_id = 1
        self.entities = []
        self.index_entity_map = {}

        # resets the lists for the entities specified in the configuration in case it exists
        if self.configuration_map:
            for entity_name in self.configuration_map:
                self.entity_name_entities_map[entity_name] = []
        else:
            # otherwise resets the whole store
            self.entity_name_entities_map = {}

    def has_entities(self, entity_name):
        """
        Indicates if the intermediate structure has entities with the specified name.

        @rtype: bool
        @return: Boolean indicating if the intermediate structure has entities with the specified name.
        """

        # raises an exception in case the intermediate structure is configured and doesn't accept entities with this name
        if self.configuration_map and not entity_name in self.configuration_map:
            raise intermediate_structure_exceptions.IntermediateStructureOperationNotAllowed("IntermediateStructure.has_entities - The intermediate structure is not configured to allow this entity name (entity_name = %s)" % entity_name)

        return entity_name in self.entity_name_entities_map

    def get_entities(self, entity_name = None):
        """
        Retrieves all entities, or all entities with the specified name.

        @type: str
        @param entity_name: Optional string specifying the name the retrieved entities must have.
        @rtype: List
        @return: List with the intermediate structure's entities.
        """

        # retrieves the specified entity instances that exist in the intermediate structure
        if entity_name:

            # raises an exception in case the intermediate structure is configured and doesn't accept entities with this name
            if self.configuration_map and not entity_name in self.configuration_map:
                raise intermediate_structure_exceptions.IntermediateStructureOperationNotAllowed("IntermediateStructure.get_entities - The intermediate structure is not configured to allow this entity name (entity_name = %s)" % entity_name)

            entities = self.entity_name_entities_map[entity_name]
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

        # raises an exception if the provided index is not a string
        if not type(index) == types.StringType:
            raise intermediate_structure_exceptions.IntermediateStructureOptionInvalid("IntermediateStructure.index_entity - The index must be a string")

        return index in self.index_entity_map

    def get_entity(self, index):
        """
        Returns the specified entity from the intermediate structure.

        @type: str
        @param index: Index that the entity is indexed by in the intermediate structure.
        @rtype: Entity
        @return: The specified intermediate structure entity.
        """

        # raises an exception if the provided index is not a string
        if not type(index) == types.StringType:
            raise intermediate_structure_exceptions.IntermediateStructureOptionInvalid("IntermediateStructure.get_entity - The index must be a string")

        # raises and exception in case the specified entity is not found in the index
        if not index in self.index_entity_map:
            raise intermediate_structure_exceptions.IntermediateStructureEntityNotFound("IntermediateStructure.get_entity - Intermediate structure index doesn't have the specified entity (index = %s)" % index)

        # retrieves the specified entity from the intermediate structure's index
        entity = self.index_entity_map[index]

        return entity

    def create_entity(self, entity_name):
        """
        Creates an entity with the specified name in the intermediate structure.

        @type: str
        @param entity_name: Name of the entity one wants to create.
        @rtype: Entity
        @return: The specified intermediate structure entity.
        """

        # raises an exception in case the intermediate structure is configured and doesn't accept entities with this name
        if self.configuration_map and not entity_name in self.configuration_map:
            raise intermediate_structure_exceptions.IntermediateStructureOperationNotAllowed("IntermediateStructure.create_entity - The intermediate structure is not configured to allow this entity name (entity_name = %s)" % entity_name)

        # retrieves the configuration map for the entity in case the intermediate structure was configured
        entity_configuration_map = None
        if self.configuration_map:
             entity_configuration_map = self.configuration_map[entity_name]

        # creates an entity with the specified name and adds it to the intermediate structure
        entity = Entity(self, self.next_object_id, entity_name, entity_configuration_map)
        self.add_entity(entity)

        # increments the next object id so the next created entity receives an object id different from this one
        self.next_object_id += 1

        return entity

    def add_entity(self, entity):
        """
        Adds the provided entity to the intermediate structure.

        @type: Entity
        @param entity: Entity to add to the intermediate structure.
        """

        # raises an exception in case the intermediate structure is configured and doesn't accept entities with this name
        entity_name = entity.get_name()
        if self.configuration_map and not entity_name in self.configuration_map:
            raise intermediate_structure_exceptions.IntermediateStructureOperationNotAllowed("IntermediateStructure.add_entity - The intermediate structure is not configured to allow this entity name (entity_name = %s)" % entity_name)

        # creates a list for the entity type in the store in case it doesn't exist
        if not entity_name in self.entity_name_entities_map:
            self.entity_name_entities_map[entity_name] = []

        # adds the entity to the store
        entities = self.entity_name_entities_map[entity_name]
        entities.append(entity)
        self.entity_name_entities_map[entity_name] = entities

        # adds the entity to the ordered list
        self.entities.append(entity)

        # indexes the entity by its object id
        entity_object_id = entity.get_object_id()
        index = str((entity_name, "object_id", entity_object_id))
        self.index_entity(entity, index)

    def index_entity(self, entity, index):
        """
        Indexes an intermediate structure entity with the specified index.

        @type: Entity
        @param entity: Entity to index.
        @type: str
        @param index: Index with which to index the entity by.
        """

        # raises an exception if the provided index is not a string
        if not type(index) == types.StringType:
            raise intermediate_structure_exceptions.IntermediateStructureOperationNotAllowed("IntermediateStructure.index_entity - The index must be a string")

        # raises an exception in case the intermediate structure is configured and doesn't accept entities with this name
        entity_name = entity.get_name()
        if self.configuration_map and not entity_name in self.configuration_map:
            raise intermediate_structure_exceptions.IntermediateStructureOperationNotAllowed("IntermediateStructure.index_entity - The intermediate structure is not configured to allow this entity name (entity_name = %s)" % entity_name)

        # raises an exception in case an entity is already occupying the specified index position
        if index in self.index_entity_map:
            raise intermediate_structure_exceptions.IntermediateStructureIndexOcuppied("IntermediateStructure.index_entity - An entity is already indexed with the specified key (index = %s)" % index)

        # indexes the entity by the specified key
        self.index_entity_map[index] = entity
        entity.indexes.append(index)

    def remove_entity(self, entity):
        """
        Removes the specified entity from the intermediate structure.

        @type: Entity
        @param entity: Entity one wants to remove from the intermediate structure.
        """

        # raises an exception in case the intermediate structure is configured and doesn't accept entities with this name
        entity_name = entity.get_name()
        if self.configuration_map and not entity_name in self.configuration_map:
            raise intermediate_structure_exceptions.IntermediateStructureOperationNotAllowed("IntermediateStructure.remove_entity - The intermediate structure is not configured to allow this entity name (entity_name = %s)" % entity_name)

        # raises an exception in case the entity isn't found
        if not entity in self.entities:
            raise intermediate_structure_exceptions.IntermediateStructureEntityNotFound("IntermediateStructure.remove_entity - Intermediate structure doesn't have the specified entity")

        # removes the entity from the ordered list
        self.entities.remove(entity)

        # removes the entity from the store
        entity_name = entity.get_name()
        entities = self.entity_name_entities_map[entity_name]
        entities.remove(entity)
        self.entity_name_entities_map[entity_name] = entities

        # removes the entity entry in the store in case the intermediate structure is not configured and
        # removing this entity resulted in the list becoming empty
        if not self.configuration_map and not entities:
            del self.entity_name_entities_map[entity_name]

        # removes the entity from the index
        for index in entity.indexes:
            del self.index_entity_map[index]

class Entity:

    intermediate_structure = None
    """ The intermediate structure the entity belongs to """

    object_id = None
    """ The entity's unique identifier in the intermediate structure """

    name = None
    """ The name of the entity """

    indexes = []
    """ The indexes this entity is indexed by in the intermediate structure """

    attribute_name_value_map = {}
    """ Dictionary associating the name of an attribute with its value """

    configuration_map = None
    """ Map used to configure the intermediate structure to obey to a certain schema """

    def __init__(self, intermediate_structure, object_id, name, configuration_map = None):
        """
        Class constructor.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: The intermediate structure the entity belongs to.
        @type object_id: int
        @param object_id: Unique identifier for the entity in the intermediate structure.
        @type name: str
        @param name: Name of the entity.
        @type configuration_map: Dictionary
        @param configuration_map: Optional map defining the intermediate structure's schema.
        """

        self.intermediate_struture = intermediate_structure
        self.object_id = object_id
        self.name = name
        self.indexes = []
        self.attribute_name_value_map = {}
        self.configuration_map = configuration_map

        # initializes the entity's attributes with the default values in case a configuration was specified
        if self.configuration_map:
            for attribute_name in configuration_map:
                attribute_configuration_map = configuration_map[attribute_name]
                self.attribute_name_value_map[attribute_name] = None

                # applies the default value to the attribute if one is specified
                if "default_value" in attribute_configuration_map:
                    default_value = attribute_configuration_map["default_value"]
                    self.attribute_name_value_map[attribute_name] = default_value

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
        Indicates if the entity has the specified attribute.

        @type: str
        @param attribute_name: Name of the attribute one wants to know if its exists in the entity.
        @rtype: bool
        @return: Boolean indicating if the attribute exists in the entity.
        """

        # raises an exception in case the entity is configured and doesn't accept attributes with this name
        if self.configuration_map and not attribute_name in self.configuration_map:
           raise intermediate_structure_exceptions.IntermediateStructureOperationNotAllowed("Entity.has_attribute - The entity is not configured to allow this attribute name (attribute_name = %s)" % attribute_name)

        return attribute_name in self.attribute_name_value_map

    def get_attributes(self):
        """
        Retrieves a map with the entity's attributes.

        @rtype: Dictionary
        @return: Map with the entity's attributes indexed by their name.
        """

        return self.attribute_name_value_map

    def get_attribute(self, attribute_name):
        """
        Retrieves the value of the specified entity attribute.

        @type: str
        @param attribute_name: Name of the attribute whose value one wants to retrieve from the entity.
        @return: Retrieves the value of the specified attribute.
        """

        # raises an exception in case the entity is configured and doesn't accept attributes with this name
        if self.configuration_map and not attribute_name in self.configuration_map:
           raise intermediate_structure_exceptions.IntermediateStructureOperationNotAllowed("Entity.get_attribute - The entity is not configured to allow this attribute name (attribute_name = %s)" % attribute_name)

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

        # raises an exception in case the entity is configured and doesn't accept attributes with this name
        if self.configuration_map and not attribute_name in self.configuration_map:
           raise intermediate_structure_exceptions.IntermediateStructureOperationNotAllowed("Entity.set_attribute - The entity is not configured to allow this attribute name (attribute_name = %s)" % attribute_name)

        # checks if the value is compatible with the configuration applied to this attribute in case there is one
        if self.configuration_map and attribute_name in self.configuration_map:
            attribute_configuration_map = self.configuration_map[attribute_name]

            # tests if the provided attribute value is of the same type as the configuration specified for this attribute
            if "type" in attribute_configuration_map:
                attribute_type = attribute_configuration_map["type"]

                # raises an exception in case a type was configured for this attribute and the specified attribute value does not match it
                allowed_types = [("instance", types.InstanceType), ("float", types.FloatType), ("integer", types.IntType), ("string", types.StringType), ("list", types.ListType)]
                if not (attribute_type, type(attribute_value)) in allowed_types:
                    raise intermediate_structure_exceptions.IntermediateStructureOperationNotAllowed("Entity.set_attribute - The specified attribute type is not allowed for this attribute (attribute_name = %s)" % attribute_name)

        # sets the attribute value in the entity's attribute
        self.attribute_name_value_map[attribute_name] = attribute_value
