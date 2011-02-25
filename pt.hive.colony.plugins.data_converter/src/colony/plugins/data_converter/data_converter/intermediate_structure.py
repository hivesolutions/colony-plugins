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

import types

import data_converter_exceptions

TYPES_VALUE = "types"

OBJECT_ID_VALUE = "object_id"

EQUALS_VALUE = "="

DEFAULT_VALUE_VALUE = "default_value"

LIST_TYPE_VALUE = "list_type"

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

    def __init__(self):
        """
        Constructor of the class.
        """

        self.next_object_id = 1
        self.entities = []
        self.entity_name_entities_map = {}
        self.index_entity_map = {}

    def configure_schema(self, configuration_map):
        """
        Configures the intermediate structure to obey to the specified schema.

        @type configuration_map: Dictionary
        @param configuration_map: Map defining the intermediate structure's schema.
        """

        self.next_object_id = 1
        self.entities = []
        self.index_entity_map = {}
        self.entity_name_entities_map = {}
        self.configuration_map = configuration_map

        # resets the lists for the entities specified in the configuration
        for entity_name in configuration_map:
            self.entity_name_entities_map[entity_name] = []

    def get_entity_names(self):
        """
        Returns the names of the entities that are in the intermediate structure.

        @rtype: List
        @return: List with the names of the entities in the intermediate structure.
        """

        entity_names = self.entity_name_entities_map.keys()

        return entity_names

    def get_entities(self):
        """
        Retrieves all entities in the intermediate structure by order of insertion.

        @rtype: List
        @return: List with the intermediate structure's entities.
        """

        return self.entities

    def get_entities_by_name(self, entity_name):
        """
        Retrieves all entities with the specified name.

        @type entity_name: String
        @param entity_name: String specifying the name the retrieved entities must have.
        @rtype: List
        @return: List with the intermediate structure's entities.
        """

        # raises an exception in case the intermediate structure is configured and doesn't accept entities with this name
        if self.configuration_map and not entity_name in self.configuration_map:
            raise data_converter_exceptions.IntermediateStructureEntityNotAllowed(str(entity_name))

        entities = self.entity_name_entities_map.get(entity_name, [])

        return entities

    def get_entities_by_index(self, index):
        """
        Returns the specified entity from the intermediate structure.

        @type index: String
        @param index: Index that the entity is indexed by in the intermediate structure.
        @rtype: List
        @return: The entities that are in the specified index.
        """

        # raises an exception if the provided index is not a tuple
        if not type(index) == types.TupleType:
            raise data_converter_exceptions.IntermediateStructureIndexNotTuple(str(index))

        # retrieves the specified entity from the intermediate structure's index
        entities = self.index_entity_map.get(index, [])

        return entities

    def create_entity(self, entity_name):
        """
        Creates an entity with the specified name in the intermediate structure.

        @type entity_name: String
        @param entity_name: Name of the entity one wants to create.
        @rtype: Entity
        @return: The specified intermediate structure entity.
        """

        # raises an exception in case the intermediate structure is configured and doesn't accept entities with this name
        if self.configuration_map and not entity_name in self.configuration_map:
            raise data_converter_exceptions.IntermediateStructureEntityNotAllowed(str(entity_name))

        # creates an entity with the specified name and adds it to the intermediate structure
        entity = Entity(self, self.next_object_id, entity_name)
        self.add_entity(entity)

        # configures the entity in case the intermediate structure was configured
        entity_configuration_map = None
        if self.configuration_map:
            entity_configuration_map = self.configuration_map[entity_name]
            entity.configure_schema(entity_configuration_map)

        # increments the next object id so the next created entity receives an object id different from this one
        self.next_object_id += 1

        return entity

    def add_entity(self, entity):
        """
        Adds the provided entity to the intermediate structure.

        @type entity: Entity
        @param entity: Entity to add to the intermediate structure.
        """

        # raises an exception in case the intermediate structure is configured and doesn't accept entities with this name
        entity_name = entity.get_name()
        if self.configuration_map and not entity_name in self.configuration_map:
            raise data_converter_exceptions.IntermediateStructureEntityNotAllowed(str(entity_name))

        # creates a list for the entity type in the store in case it doesn't exist
        if not entity_name in self.entity_name_entities_map:
            self.allocate_entity_name(entity_name)

        # adds the entity to the store
        entities = self.entity_name_entities_map[entity_name]
        entities.append(entity)
        self.entity_name_entities_map[entity_name] = entities

        # adds the entity to the ordered list
        self.entities.append(entity)

        # indexes the entity by its object id
        entity_object_id = entity.get_object_id()
        index = (OBJECT_ID_VALUE, EQUALS_VALUE, entity_object_id)
        self.index_entity(entity, index)

    def index_entity(self, entity, index):
        """
        Indexes an intermediate structure entity with the specified index.

        @type entity: Entity
        @param entity: Entity to index.
        @type index: String
        @param index: Index with which to index the entity by.
        """

        # raises an exception if the provided index is not a tuple
        if not type(index) == types.TupleType:
            raise data_converter_exceptions.IntermediateStructureIndexNotTuple(str(index))

        # raises an exception in case the intermediate structure is configured and doesn't accept entities with this name
        entity_name = entity.get_name()
        if self.configuration_map and not entity_name in self.configuration_map:
            raise data_converter_exceptions.IntermediateStructureEntityNotAllowed(str(entity_name))

        # indexes the entity by the specified key
        if not index in self.index_entity_map:
            self.index_entity_map[index] = [entity]
        else:
            # adds the entity to the index location
            self.index_entity_map[index].append(entity)

        # adds the index to the entity
        entity.indexes.append(index)

    def remove_entity(self, entity):
        """
        Removes the specified entity from the intermediate structure.

        @type entity: Entity
        @param entity: Entity one wants to remove from the intermediate structure.
        """

        entity_name = entity.get_name()
        entity_object_id = entity.get_object_id()

        # raises an exception in case the intermediate structure is configured and doesn't accept entities with this name
        if self.configuration_map and not entity_name in self.configuration_map:
            raise data_converter_exceptions.IntermediateStructureEntityNotAllowed(str(entity_name))

        # raises an exception in case the entity isn't found
        if not entity in self.entities:
            raise data_converter_exceptions.IntermediateStructureEntityNotFound("%s.%s = %d" % (entity_name, OBJECT_ID_VALUE, entity_object_id))

        # removes the entity from the ordered list
        self.entities.remove(entity)

        # removes the entity from the store
        entities = self.entity_name_entities_map[entity_name]
        entities.remove(entity)
        self.entity_name_entities_map[entity_name] = entities

        # removes the entity entry in the store in case the intermediate structure is not configured and
        # removing this entity resulted in the list becoming empty
        if not self.configuration_map and not entities:
            del self.entity_name_entities_map[entity_name]

        # removes the entity from the index
        for index in entity.indexes:
            entities = self.index_entity_map[index]
            entities.remove(entity)

            # removes the index entry in case it is left empty
            if not entities:
                del self.index_entity_map[index]

    def allocate_entity_name(self, entity_name):
        """
        Allocates a position where to store entities with
        the specified name.

        @type entity_name: String
        @param entity_name: Name of the entities for which
        one wants to allocate storage in the intermediate
        structure.
        """

        if entity_name in self.entity_name_entities_map:
            raise data_converter_exceptions.IntermediateStructureEntityNameAlreadyAllocated(str(entity_name))

        self.entity_name_entities_map[entity_name] = []

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

    def __init__(self, intermediate_structure, object_id, name):
        """
        Constructor of the class.

        @type intermediate_structure: DataConverter
        @param intermediate_structure: The intermediate structure the entity belongs to.
        @type object_id: int
        @param object_id: Unique identifier for the entity in the intermediate structure.
        @type name: String
        @param name: Name of the entity.

        """

        self.intermediate_structure = intermediate_structure
        self.object_id = object_id
        self.name = name
        self.indexes = []
        self.attribute_name_value_map = {}
        self.configuration_map = None

    def configure_schema(self, configuration_map):
        """
        Configures the entity to obey to the specified schema.

        @type configuration_map: Dictionary
        @param configuration_map: Map defining the intermediate structure's schema.
        """

        self.attribute_name_value_map = {}
        self.configuration_map = configuration_map

        # initializes the entity's attributes with the default values
        for attribute_name, configuration_map in configuration_map.items():

            # retrieves the configuration's attributes
            list_type = configuration_map.get(LIST_TYPE_VALUE, False)
            default_value = configuration_map.get(DEFAULT_VALUE_VALUE, None)

            # initializes the attribute with the configured type and value
            if not default_value and list_type:
                self.attribute_name_value_map[attribute_name] = []
            else:
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

        @rtype: String
        @return: Name of the entity in the intermediate structure.
        """

        return self.name

    def has_attribute(self, attribute_name):
        """
        Indicates if the entity has the specified attribute.

        @type attribute_name: String
        @param attribute_name: Name of the attribute one wants to know if
        its exists in the entity.
        @rtype: bool
        @return: Boolean indicating if the attribute exists in the entity.
        """

        # raises an exception in case the entity is configured and doesn't accept attributes with this name
        if self.configuration_map and not attribute_name in self.configuration_map:
            raise data_converter_exceptions.IntermediateStructureEntityAttributeNotAllowed("%s.%s" % (self.name, attribute_name))

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

        @type attribute_name: String
        @param attribute_name: Name of the attribute whose value one wants to
        retrieve from the entity.
        @return: Retrieves the value of the specified attribute.
        """

        # raises an exception in case the entity is configured and doesn't accept attributes with this name
        if self.configuration_map and not attribute_name in self.configuration_map:
            raise data_converter_exceptions.IntermediateStructureEntityAttributeNotAllowed("%s.%s" % (self.name, attribute_name))

        # raises an exception in case the specified attribute name was not found in the entity
        if not attribute_name in self.attribute_name_value_map:
            raise data_converter_exceptions.IntermediateStructureEntityAttributeNotFound("%s.%s" % (self.name, attribute_name))

        # retrieves the attribute value
        attribute_value = self.attribute_name_value_map[attribute_name]

        return attribute_value

    def set_attribute(self, attribute_name, attribute_value):
        """
        Sets the value for an entity's attribute.

        @type attribute_name: String
        @param attribute_name: Name of the attribute whose value one wants
        to set in the entity.
        @type attribute_value: Object
        @param attribute_value: Attribute value one wants to set.
        """

        # raises an exception in case the entity is configured and doesn't accept attributes with this name
        if self.configuration_map and not attribute_name in self.configuration_map:
            raise data_converter_exceptions.IntermediateStructureEntityAttributeNotAllowed("%s.%s" % (self.name, attribute_name))

        # checks if the value is compatible with the configuration applied to this attribute in case there is one
        if self.configuration_map and attribute_name in self.configuration_map:
            attribute_configuration_map = self.configuration_map[attribute_name]

            # tests if the provided attribute value is of the same type as the configuration specified for this attribute
            attribute_types = attribute_configuration_map.get(TYPES_VALUE, [])
            list_type = attribute_configuration_map.get(LIST_TYPE_VALUE, False)

            # raises an exception in case a type was configured for this attribute and the specified attribute value does not match it
            if list_type and not type(attribute_value) == types.ListType or not self.is_valid_attribute(attribute_value, attribute_types):
                raise data_converter_exceptions.IntermediateStructureEntityAttributeDataTypeNotAllowed("%s.%s (%s)" % (self.name, attribute_name, type(attribute_value)))

        # sets the attribute value in the entity's attribute
        self.attribute_name_value_map[attribute_name] = attribute_value

    def remove_attribute(self, attribute_name):
        """
        Removes the specified attribute from the entity.

        @type attribute_name: String
        @param attribute_name: Name of the attribute whose value one wants
        to remove from the entity.
        """

        # raises an exception in case the entity is configured and with attributes with this name
        if self.configuration_map and attribute_name in self.configuration_map:
            raise data_converter_exceptions.IntermediateStructureEntityAttributeNotAllowed("%s.%s" % (self.name, attribute_name))

        # raises an exception in case the specified attribute doesn't exist
        if not attribute_name in self.attribute_name_value_map:
            raise data_converter_exceptions.IntermediateStructureEntityAttributeNotFound(attribute_name)

        # removes the specified attribute
        del self.attribute_name_value_map[attribute_name]

    def is_valid_attribute(self, attribute_value, attribute_types):
        # converts the attribute value into a list in case it is not
        # in order to reuse the same code
        if not type(attribute_value) == types.ListType:
            attribute_value = [attribute_value]

        # splits the attribute types into python types and entity types
        plain_attribute_types = [attribute_type for attribute_type in attribute_types if not type(attribute_type) in types.StringTypes]
        plain_attribute_types.append(types.NoneType)
        entity_attribute_types = [attribute_type for attribute_type in attribute_types if type(attribute_type) in types.StringTypes]

        # tests if the attribute is invalid
        for attribute_value_item in attribute_value:

            # returns false in case the attribute is an entity that is not allowed
            if type(attribute_value_item) == types.InstanceType and entity_attribute_types and not attribute_value_item.get_name() in entity_attribute_types:
                return False

            # returns false in the attribute is a plain type that is not allowed
            if not type(attribute_value_item) == types.InstanceType and plain_attribute_types and not type(attribute_value_item) in plain_attribute_types:
                return False

        return True
