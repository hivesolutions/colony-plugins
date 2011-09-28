#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import os
import types

import data_converter_io_adapter_entity_manager_exceptions

AUTOCOMMIT_VALUE = "autocommit"
""" The autocommit value """

EAGER_LOADING_RELATIONS_VALUE = "eager_loading_relations"
""" The eager loading relations value """

ENTITY_MANAGER_ENGINE_VALUE = "entity_manager_engine"
""" The entity manager engine value """

ENTITY_MANAGER_VALUE = "entity_manager"
""" The entity manager value """

EQUALS_VALUE = "="
""" The equals value """

FIELDS_VALUE = "fields"
""" The fields value """

FILE_PATH_VALUE = "file_path"
""" The file path value """

INPUT_FILE_PATH_VALUE = "input_file_path"
""" The input file path value """

OBJECT_ID_VALUE = "object_id"
""" The object id value """

OUTPUT_FILE_PATH_VALUE = "output_file_path"
""" The output file path value """

LOAD_OPTIONS_VALUE = "load_options"
""" The load options value """

LOAD_ENTITIES_VALUE = "load_entities"
""" The load entities value """

INPUT_ATTRIBUTE_HANDLERS_VALUE = "input_attribute_handlers"
""" The input attribute handlers value """

class IoAdapterEntityManager:
    """
    Provides a means to load and save the intermediate structure by using the
    colony entity manager.
    """

    io_adapter_entity_manager_plugin = None
    """ Io adapter entity manager plugin """

    def __init__(self, io_adapter_entity_manager_plugin):
        """
        Constructor of the class.

        @type io_adapter_entity_manager_plugin: IoAdapterEntityManager
        @param io_adapter_entity_manager_plugin: Input output adapter entity_manager plugin.
        """

        self.io_adapter_entity_manager_plugin = io_adapter_entity_manager_plugin

    def load_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the
        entity manager with the specified options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to
        load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into
        the provided intermediate structure.
        """

        # creates an entity manager instance in case an entity manager wasn't provided
        entity_manager_provided = configuration.has_option(ENTITY_MANAGER_VALUE)
        if not entity_manager_provided:
            # retrieves the mandatory options
            entity_manager_engine = options[ENTITY_MANAGER_ENGINE_VALUE]
            file_path = configuration.get_option(INPUT_FILE_PATH_VALUE)

            # raises and exception in case the specified file does not exist
            if not os.path.exists(file_path):
                raise data_converter_io_adapter_entity_manager_exceptions.IoAdapterEntityManagerFileNotFound(file_path)

            # retrieves the entity manager plugin
            entity_manager_plugin = self.io_adapter_entity_manager_plugin.entity_manager_plugin

            # defines the connection parameters
            connection_parameters = {
                FILE_PATH_VALUE : file_path,
                AUTOCOMMIT_VALUE : False
            }

            # initializes the entity manager
            entity_manager = entity_manager_plugin.load_entity_manager(entity_manager_engine)
            entity_manager.set_connection_parameters(connection_parameters)

            # loads the entity manager
            entity_manager.load_entity_manager()
        else:
            # otherwise retrieves the provided entity manager
            entity_manager = configuration.get_option(ENTITY_MANAGER_VALUE)

        try:
            # loads the intermediate structure entities' attributes
            entity_object_id_entity_map, entity_object_id_intermediate_entity_object_id_map = self.load_attributes(intermediate_structure, entity_manager, options)

            # loads the intermediate structure entities' relations
            self.load_relations(intermediate_structure, entity_manager, options, entity_object_id_entity_map, entity_object_id_intermediate_entity_object_id_map)
        finally:
            # closes the database connection in case it was
            # created by the io adapter
            if not entity_manager_provided:
                entity_manager.close_connection()

    def load_attributes(self, intermediate_structure, entity_manager, options):
        """
        Loads the intermediate structure's entities' attributes with the entity manager.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to load.
        @type entity_manager: EntityManager
        @param entity_manager: Entity manager used to load the intermediate structure
        entities' attributes.
        @type options: Dictionary
        @param options: Options used to determine how to load data into
        the provided intermediate structure.
        @rtype: List
        @return: List with a map associating the created entity object ids with the
        entities themselves
        and a map associating the object ids of the entities with the ones of the
        created intermediate entities.
        """

        # dictionary used to index the entities retrieved in the load attributes step by their object id
        entity_object_id_entity_map = {}

        # dictionary used to associate the created intermediate entity object ids with entity object ids
        entity_object_id_intermediate_entity_object_id_map = {}

        # extracts the non-mandatory options
        load_options = options.get(LOAD_OPTIONS_VALUE, {})
        load_entity_name_attribute_names_map = load_options.get(LOAD_ENTITIES_VALUE, None)
        input_attribute_handlers = options.get(INPUT_ATTRIBUTE_HANDLERS_VALUE, [])

        # retrieves a list of available entity classes
        entity_classes = entity_manager.entity_classes_list

        # filters the entity classes to the specified entity names
        if load_entity_name_attribute_names_map:
            entity_class_names = load_entity_name_attribute_names_map.keys()
            entity_classes = [entity_class for entity_class in entity_classes if entity_class.__name__ in entity_class_names]

        # retrieves all entities and stores their contents in the intermediate structure
        for entity_class in entity_classes:

            # retrieves the attributes names one wishes to retrieve for this entity
            entity_class_name = entity_class.__name__

            # retrieves all objects of the specified class
            find_options = {FIELDS_VALUE : ["object_id"]}
            entities = entity_manager.find_a(entity_class, find_options)

            # retrieves the names of the attributes that must be loaded
            attribute_names = []
            if entity_class_name in load_entity_name_attribute_names_map:
                attribute_names = load_entity_name_attribute_names_map[entity_class_name]

            # initializes the find options
            find_options = {}

            # figures out which non relation attribute names must be loaded
            non_relation_attribute_names = entity_manager.get_entity_class_non_relation_attribute_names(entity_class)
            if attribute_names:
                non_relation_attribute_names = [non_relation_attribute_name for non_relation_attribute_name in non_relation_attribute_names if non_relation_attribute_name in attribute_names]

            # sets the attributes that must be loaded in the find options
            # in case they were specified
            if attribute_names:
                find_options[FIELDS_VALUE] = ["object_id"] + attribute_names

            # figures out which relation attribute names must be loaded
            relation_attribute_names = entity_manager.get_entity_class_relation_attribute_names(entity_class)
            if attribute_names:
                relation_attribute_names = [relation_attribute_name for relation_attribute_name in relation_attribute_names if relation_attribute_name in attribute_names]

            # injects the relation attribute names that must be loaded
            # in the find options, if there are any
            if relation_attribute_names:
                find_options[EAGER_LOADING_RELATIONS_VALUE] = {}
                for relation_attribute_name in relation_attribute_names:
                    find_options[EAGER_LOADING_RELATIONS_VALUE][relation_attribute_name] = {}

            # creates an intermediate entity for each entity and populates it with the entity's attributes
            for entity in entities:

                # creates the intermediate entity and indexes it to the intermediate entity for use in the load relations step
                intermediate_entity = intermediate_structure.create_entity(entity_class_name)
                intermediate_entity_object_id = intermediate_entity.get_object_id()
                entity_object_id_intermediate_entity_object_id_map[entity.object_id] = intermediate_entity_object_id

                # retrieves the entity again but now fully loaded and indexes it by its object id for use in the load relations step
                entity = entity_manager.get(entity_class, entity.object_id, find_options)
                entity_object_id_entity_map[entity.object_id] = entity

                # injects the entity class in the entity
                # for later reference
                setattr(entity, "entity_class", entity_class)

                # copies the entity's attributes to the intermediate entity
                for attribute_name in non_relation_attribute_names:
                    attribute_value = getattr(entity, attribute_name)

                    # passes the attribute value through the configured input attribute handlers
                    for input_attribute_handler in input_attribute_handlers:
                        attribute_value = input_attribute_handler(intermediate_structure, entity, attribute_value)

                    intermediate_entity.set_attribute(attribute_name, attribute_value)

        return (
            entity_object_id_entity_map,
            entity_object_id_intermediate_entity_object_id_map
        )

    def load_relations(self, intermediate_structure, entity_manager, options, entity_object_id_entity_map, entity_object_id_intermediate_entity_object_id_map):
        """
        Loads the intermediate structure's entities' relations with the entity manager.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to load.
        @type entity_manager: EntityManager
        @param entity_manager: Entity manager used to load the intermediate structure
        entities' attributes.
        @type options: Dictionary
        @param options: Options used to determine how to load data into
        the provided intermediate structure.
        @type entity_object_id_entity_map: Dictionary
        @param entity_object_id_entity_map: Map associating the object ids of the
        entities created in the load attributes step with the entities themselves.
        @type entity_object_id_intermediate_entity_object_id_map: Dictionary
        @param entity_object_id_intermediate_entity_object_id_map: Map associating
        the entity object ids with the object ids of the correspondent intermediate
        entities created in the load attributes step.
        """

        # extracts the non-mandatory options
        load_options = options.get(LOAD_OPTIONS_VALUE, {})
        load_entity_name_attribute_names_map = load_options.get(LOAD_ENTITIES_VALUE, None)

        # retrieves the entity for each intermediate entity
        entities = entity_object_id_entity_map.values()
        for entity in entities:
            entity_class = getattr(entity, "entity_class")
            entity_class_name = entity_class.__name__

            # retrieves the correspondent intermediate entity created in the load attributes step
            intermediate_entity_object_id = entity_object_id_intermediate_entity_object_id_map[entity.object_id]
            intermediate_entity_index = self.get_intermediate_entity_index(intermediate_entity_object_id)
            intermediate_entities = intermediate_structure.get_entities_by_index(intermediate_entity_index)

            # raises an exception in case more than one entity was
            # found at the specified index
            if len(intermediate_entities) > 1:
                raise data_converter_io_adapter_entity_manager_exceptions.IoAdapterEntityManagerUnexpectedNumberIntermediateEntities()

            # retrieves the associated intermediate entity
            intermediate_entity = intermediate_entities[0]

            # retrieves the names of the attributes that must be loaded
            attribute_names = []
            if entity_class_name in load_entity_name_attribute_names_map:
                attribute_names = load_entity_name_attribute_names_map[entity_class_name]

            # figures out which relation attribute names must be loaded
            relation_attribute_names = entity_manager.get_entity_class_relation_attribute_names(entity_class)
            if attribute_names:
                relation_attribute_names = [relation_attribute_name for relation_attribute_name in relation_attribute_names if relation_attribute_name in attribute_names]

            # iterates through the intermediate entity's relation attributes and creates
            # a connection between the respective entity and the respective related entity
            for attribute_name in relation_attribute_names:

                # retrieves the intermediate entity's relation value
                intermediate_entity_attribute_value = None
                if intermediate_entity.has_attribute(attribute_name):
                    intermediate_entity_attribute_value = intermediate_entity.get_attribute(attribute_name)

                # retrieves the entities that are in the entity relation attribute
                related_entity_or_entities = getattr(entity, attribute_name)

                # if entity relation is a "to many" relation
                if type(related_entity_or_entities) == types.ListType:
                    related_entities = related_entity_or_entities

                    # converts the intermediate structure value to a "to many" relation in case it's not currently
                    if not type(intermediate_entity_attribute_value) == types.ListType:
                        if not intermediate_entity_attribute_value:
                            intermediate_entity_attribute_value = []
                        else:
                            intermediate_entity_attribute_value = [
                                intermediate_entity_attribute_value
                            ]

                    # retrieves the intermediate entity associated with each related entity and adds it to the intermediate entity's relation attribute
                    for related_entity in related_entities:
                        related_intermediate_entity_object_id = entity_object_id_intermediate_entity_object_id_map[related_entity.object_id]
                        related_intermediate_entity_index = self.get_intermediate_entity_index(related_intermediate_entity_object_id)
                        related_intermediate_entities = intermediate_structure.get_entities_by_index(related_intermediate_entity_index)
                        related_intermediate_entity = related_intermediate_entities[0]
                        intermediate_entity_attribute_value.append(related_intermediate_entity)

                    # updates the intermediate entity's relation attribute with the retrieved related intermediate entities
                    intermediate_entity.set_attribute(attribute_name, intermediate_entity_attribute_value)

                elif related_entity_or_entities:
                    # if the entity relation is a "to one" relation
                    related_entity = related_entity_or_entities
                    related_intermediate_entity = None

                    # retrieves the intermediate entity that corresponds to the related entity
                    if related_entity:
                        related_intermediate_entity_object_id = entity_object_id_intermediate_entity_object_id_map[related_entity.object_id]
                        related_intermediate_entity_index = self.get_intermediate_entity_index(related_intermediate_entity_object_id)
                        related_intermediate_entities = intermediate_structure.get_entities_by_index(related_intermediate_entity_index)
                        related_intermediate_entity = related_intermediate_entities[0]

                    # updates the intermediate entity's relation attribute with the retrieved related intermediate entity
                    intermediate_entity.set_attribute(attribute_name, related_intermediate_entity)

    def save_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Saves the intermediate structure with the entity manager at the location and with characteristics
        defined in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure with the entity manager.
        """

        # creates an entity manager instance in case an entity manager wasn't provided
        entity_manager_provided = configuration.has_option(ENTITY_MANAGER_VALUE)
        if not entity_manager_provided:
            # retrieves the mandatory options
            entity_manager_engine = options[ENTITY_MANAGER_ENGINE_VALUE]
            file_path = configuration.get_option(OUTPUT_FILE_PATH_VALUE)

            # retrieves the entity manager plugin
            entity_manager_plugin = self.io_adapter_entity_manager_plugin.entity_manager_plugin

            # defines the connection parameters
            connection_parameters = {
                FILE_PATH_VALUE : file_path,
                AUTOCOMMIT_VALUE : False
            }

            # initializes the entity manager
            entity_manager = entity_manager_plugin.load_entity_manager(entity_manager_engine)
            entity_manager.set_connection_parameters(connection_parameters)

            # loads the entity manager
            entity_manager.load_entity_manager()
        else:
            # otherwise retrieves the provided entity manager
            entity_manager = configuration.get_option(ENTITY_MANAGER_VALUE)

        try:
            # saves the intermediate structure entities' attributes
            entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map = self.save_attributes(intermediate_structure, entity_manager)

            # saves the intermediate structure entities' relations
            self.save_relations(intermediate_structure, entity_manager, entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map)
        finally:
            # closes the database connection in
            # case it was created by the io adapter
            if not entity_manager_provided:
                entity_manager.close_connection()

    def save_attributes(self, intermediate_structure, entity_manager):
        """
        Saves the intermediate structure's entities' attributes with the entity manager.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type entity_manager: EntityManager
        @param entity_manager: Entity manager used to save the intermediate structure
        entities' attributes.
        @rtype: List
        @return: List with a map associating the created entity object ids with the
        entities themselves and a map
        associating the object ids of the intermediate entities with the ones of the
        created entities.
        """

        # dictionary used to index the entities created in the save attributes step by their object id
        entity_object_id_entity_map = {}

        # dictionary used to associate intermediate entity object ids with entity object ids
        intermediate_entity_object_id_entity_object_id_map = {}

        # creates a transaction for the save attributes operation
        entity_manager.create_transaction("io_adapter_entity_manager_save_attributes_transaction")

        # creates an entity for each intermediate entity in the internal structure and populates it with its attributes
        intermediate_entities = intermediate_structure.get_entities()
        self.save_attributes_intermediate_entities(intermediate_structure, entity_manager, entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map, intermediate_entities)

        # commits the save attributes operation's transaction
        entity_manager.commit_transaction("io_adapter_entity_manager_save_attributes_transaction")

        return (entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map)

    def save_attributes_intermediate_entities(self, intermediate_structure, entity_manager, entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map, intermediate_entities):
        """
        Saves the intermediate structure's entities' attributes with the entity manager.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type entity_manager: EntityManager
        @param entity_manager: Entity manager used to save the intermediate structure
        entities' attributes.
        @type entity_object_id_entity_map: Dictionary
        @param entity_object_id_entity_map: Map associating the object ids of the
        entities created in the load attributes step with the entities themselves.
        @type intermediate_entity_object_id_entity_object_id_map: Dictionary
        @param intermediate_entity_object_id_entity_object_id_map: Map associating
        intermediate entity object ids with the object ids of the correspondent entities.
        @type intermediate_entities: List
        @param intermediate_entities: List of intermediate entities where to extract
        the entity attributes from.
        @rtype: List
        @return: List with a map associating the created entity object ids with the
        entities themselves and a map associating the object ids of the intermediate
        entities with the ones of the created entities.
        """

        # creates an entity for each intermediate entity and populates it with the entity's attributes
        for intermediate_entity in intermediate_entities:

            # retrieves the entity class related with the intermediate entity
            intermediate_entity_name = intermediate_entity.get_name()
            entity_class = entity_manager.get_entity_class(intermediate_entity_name)

            # skips this entity in case its correspondent class was not found in the entity manager
            if not entity_class:
                self.io_adapter_entity_manager_plugin.error("Failed to save entity named '%s' because it doesn't exist in the entity manager" % intermediate_entity_name)
                continue

            # creates an entity
            entity = entity_class()

            # populates the entity with the intermediate entity's attributes
            non_relation_attribute_names = self.get_non_relation_attribute_names(intermediate_entity)
            for non_relation_attribute_name in non_relation_attribute_names:
                intermediate_entity_attribute_value = intermediate_entity.get_attribute(non_relation_attribute_name)
                setattr(entity, non_relation_attribute_name, intermediate_entity_attribute_value)

            # saves the entity
            entity_manager._save(entity)

            # index the entity for later usage in the save relations step
            entity_object_id_entity_map[entity.object_id] = entity
            intermediate_entity_object_id_entity_object_id_map[intermediate_entity.object_id] = entity.object_id

    def save_relations(self, intermediate_structure, entity_manager, entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map):
        """
        Saves the intermediate structure's entities' relations with the entity manager.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type entity_manager: EntityManager
        @param entity_manager: Entity manager used to save the intermediate structure
        entities' attributes.
        @type entity_object_id_entity_map: Dictionary
        @param entity_object_id_entity_map: Map associating the object ids of the entities
        created in the save attributes step with the entities themselves.
        @type intermediate_entity_object_id_entity_object_id_map: Dictionary
        @param intermediate_entity_object_id_entity_object_id_map: Map associating the
        intermediate entity object ids with the object ids of the correspondent entities created
        in the save attributes step.
        """

        # creates a transaction for the save relations operation
        entity_manager.create_transaction("io_adapter_entity_manager_save_relations_transaction")

        # creates an entity for each intermediate entity in the internal structure and populates it with its attributes
        intermediate_entities = intermediate_structure.get_entities()
        self.save_relations_intermediate_entities(intermediate_structure, entity_manager, entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map, intermediate_entities)

        # commits the save relations operation's transaction
        entity_manager.commit_transaction("io_adapter_entity_manager_save_relations_transaction")

    def save_relations_intermediate_entities(self, intermediate_structure, entity_manager, entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map, intermediate_entities):
        """
        Saves the provided intermediate entities's relations with the entity manager.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type entity_manager: EntityManager
        @param entity_manager: Entity manager used to save the intermediate structure
        entities' attributes.
        @type entity_object_id_entity_map: Dictionary
        @param entity_object_id_entity_map: Map associating the object ids of the entities
        created in the save attributes step with the entities themselves.
        @type intermediate_entity_object_id_entity_object_id_map: Dictionary
        @param intermediate_entity_object_id_entity_object_id_map: Map associating the
        intermediate entity object ids with the object ids of the correspondent entities
        created in the save attributes step.
        @type intermediate_entities: List
        @param intermediate_entities: List of intermediate entities where to extract the relations from.
        """

        # copies each intermediate entity's relations to the respective entity
        for intermediate_entity in intermediate_entities:

            # retrieves the respective entity which was created in the save attributes step
            intermediate_entity_object_id = intermediate_entity.get_object_id()
            entity_object_id = intermediate_entity_object_id_entity_object_id_map[intermediate_entity_object_id]
            entity = entity_object_id_entity_map[entity_object_id]

            # iterates through the intermediate entity's relation attributes replicating the associations in the respective entity
            relation_attribute_names = self.get_relation_attribute_names(intermediate_entity)

            # populates the entity with its related entities
            for relation_attribute_name in relation_attribute_names:
                intermediate_related_entity_or_entities = intermediate_entity.get_attribute(relation_attribute_name)

                # encapsulates the relation attribute's value in a list in case its a "to one" relation in order to reuse the following code
                if type(intermediate_related_entity_or_entities) == types.ListType:
                    intermediate_related_entities = intermediate_related_entity_or_entities
                elif intermediate_related_entity_or_entities:
                    intermediate_related_entities = [
                        intermediate_related_entity_or_entities
                    ]
                else:
                    intermediate_related_entities = []

                # iterates through each intermediate related entity in the intermediate entity's relation attributes replicating the association in the respective entity
                self.save_relations_intermediate_entity_intermediate_related_entities(intermediate_structure, entity_manager, entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map, intermediate_related_entities, entity, relation_attribute_name)

            # @todo: skipping updates on the mapped by side because of orm limitation
            try:
                # updates the entity
                entity_manager._update(entity)
            except:
                pass

    def save_relations_intermediate_entity_intermediate_related_entities(self, intermediate_structure, entity_manager, entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map, intermediate_related_entities, entity, relation_attribute_name):
        """
        Saves the entities that correspond to the provided intermediate entities in the specified entity
        and relation attribute.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type entity_manager: EntityManager
        @param entity_manager: Entity manager used to save the intermediate structure entities' attributes.
        @type entity_object_id_entity_map: Dictionary
        @param entity_object_id_entity_map: Map associating the object ids of the entities created in the
        save attributes step with the entities themselves.
        @type entity_object_id_entity_map: Dictionary
        @param entity_object_id_entity_map: Map associating the object ids of the entities
        created in the save attributes step with the entities themselves.
        @type intermediate_entity_object_id_entity_object_id_map: Dictionary
        @param intermediate_entity_object_id_entity_object_id_map: Map associating the intermediate entity
        object ids with the object ids of the correspondent entities created in the save attributes step.
        @type intermediate_related_entities: List
        @param intermediate_related_entities: List of intermediate entities that were in the intermediate
        entity's relations.
        @type relation_attribute_name: String
        @param relation_attribute_name: Name of the relation attribute where the the retrieved related
        entities will be stored.
        @type entity: Entity
        @param entity: Entity where to store the entities that correspond to the provided intermediate
        related entities.
        """

        # logs an error and returns in case the specified relation attribute was not found
        if not hasattr(entity, relation_attribute_name):
            self.io_adapter_entity_manager_plugin.error("Entity '%s' has no relation attribute named '%s:" % (entity.__class__.__name__, relation_attribute_name))
            return

        entity_attribute_value = getattr(entity, relation_attribute_name)

        # retrieves entity that corresponds to the intermediate entity that is in the relation attribute adds it to the entity's relation attribute
        for intermediate_related_entity in intermediate_related_entities:
            intermediate_related_entity_object_id = intermediate_related_entity.get_object_id()
            related_entity_object_id = intermediate_entity_object_id_entity_object_id_map[intermediate_related_entity_object_id]
            related_entity = entity_object_id_entity_map[related_entity_object_id]

            # sets the intermediate entity's attribute value in the entity
            if type(entity_attribute_value) == types.ListType:
                entity_attribute_value.append(related_entity)
            elif entity_attribute_value:
                entity_attribute_value = [
                    entity_attribute_value
                ]

                entity_attribute_value.append(related_entity)
            else:
                entity_attribute_value = related_entity
            setattr(entity, relation_attribute_name, entity_attribute_value)

    def get_intermediate_entity_index(self, intermediate_entity_object_id):
        """
        Retrieves the index used to retrieve an entity from the
        intermediate structure.

        @type intermediate_entity_object_id: int
        @param intermediate_entity_object_id: Intermediate structure object id
        for the entity one wants to retrieve.
        @rtype: String
        @return: String with the index that can be used to retrieve the specified
        entity from the intermediate structure.
        """

        intermediate_entity_index = (
            OBJECT_ID_VALUE, EQUALS_VALUE, intermediate_entity_object_id
        )

        return intermediate_entity_index

    def get_non_relation_attribute_names(self, intermediate_entity):
        """
        Retrieves the names of the provided intermediate structure entity's non
        relation attributes.

        @type intermediate_entity: Entity
        @param intermediate_entity: The entity whose non relation attribute names one wants
        to retrieve.
        @rtype: List
        @return: List with the names of the entity's non relation attributes.
        """

        intermediate_entity_attributes_map = intermediate_entity.get_attributes()
        intermediate_entity_attribute_names = intermediate_entity_attributes_map.keys()
        non_relation_attribute_names = [attribute_name for attribute_name in intermediate_entity_attribute_names if type(intermediate_entity.get_attribute(attribute_name)) not in (types.ListType, types.InstanceType)]

        return non_relation_attribute_names

    def get_relation_attribute_names(self, intermediate_entity):
        """
        Retrieves the names of the provided intermediate structure entity's
        relation attributes.

        @type intermediate_entity: Entity
        @param intermediate_entity: The entity whose relation attribute names one wants
        to retrieve.
        @rtype: List
        @return: List with the names of the entity's relation attributes.
        """

        intermediate_entity_attributes_map = intermediate_entity.get_attributes()
        intermediate_entity_attribute_names = intermediate_entity_attributes_map.keys()
        relation_attribute_names = [attribute_name for attribute_name in intermediate_entity_attribute_names if type(intermediate_entity.get_attribute(attribute_name)) in (types.ListType, types.InstanceType)]

        return relation_attribute_names
