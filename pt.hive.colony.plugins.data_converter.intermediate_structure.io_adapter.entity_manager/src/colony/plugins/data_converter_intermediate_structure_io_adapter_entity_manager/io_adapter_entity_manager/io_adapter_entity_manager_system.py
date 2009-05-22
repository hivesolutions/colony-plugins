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
import os.path

import io_adapter_entity_manager_exceptions

LAZY_LOADED = "%lazy-loaded%"
""" String used by the entity manager to indicate that an entity's relation is lazy loaded """

class IoAdapterEntityManager:
    """
    Provides a means to load and save the intermediate structure by using the colony business entity manager.
    """

    def __init__(self, io_adapter_entity_manager_plugin):
        """
        Class constructor.

        @type io_adapter_entity_manager_plugin: IoAdapterEntityManager
        @param io_adapter_entity_manager_plugin: Input output adapter entity_manager plugin.
        """

        self.io_adapter_entity_manager_plugin = io_adapter_entity_manager_plugin

    def load(self, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the entity manager with the specified options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the provided intermediate structure.
        """

        self.io_adapter_entity_manager_plugin.logger.info("[%s] Loading intermediate structure with entity manager io adapter" % self.io_adapter_entity_manager_plugin.id)

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["file_path", "entity_manager_engine"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise io_adapter_entity_manager_exceptions.IoAdapterEntityManagerOptionNotFound("IoAdapterEntityManager.load - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        file_path = options["file_path"]
        entity_manager_engine = options["entity_manager_engine"]

        # raises and exception in case the specified file does not exist
        if not os.path.exists(file_path):
            raise io_adapter_entity_manager_exceptions.IoAdapterEntityManagerOptionInvalid("IoAdapterEntityManager.load - Specified file to load intermediate structure from does not exist (file_path = %s)" % file_path)

        # retrieves the entity manager plugin
        entity_manager_plugin = self.io_adapter_entity_manager_plugin.entity_manager_plugin

        # initializes the entity manager
        entity_manager = entity_manager_plugin.load_entity_manager(entity_manager_engine)
        entity_manager.set_connection_parameters({"file_path" : file_path, "autocommit" : False})

        # loads the entity manager
        entity_manager.load_entity_manager()

        # loads the intermediate structure entities' attributes
        entity_object_id_entity_map, entity_object_id_intermediate_entity_object_id_map = self.load_attributes(intermediate_structure, entity_manager)

        # loads the intermediate structure entities' relations
        self.load_relations(intermediate_structure, entity_manager, entity_object_id_entity_map, entity_object_id_intermediate_entity_object_id_map)

    def load_attributes(self, intermediate_structure, entity_manager):
        """
        Loads the intermediate structure's entities' attributes with the entity manager.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to load.
        @type entity_manager: EntityManager
        @param entity_manager: Entity manager used to load the intermediate structure entities' attributes.
        @rtype: List
        @return: List with a map associating the created entity object ids with the entities themselves and a map associating the object ids of the entities with the ones of the created intermediate entities.
        """

        self.io_adapter_entity_manager_plugin.logger.info("[%s] Loading intermediate structure entities' attributes with entity manager io adapter" % self.io_adapter_entity_manager_plugin.id)

        # dictionary used to index the entities retrieved in the load attributes step by their object id
        entity_object_id_entity_map = {}

        # dictionary used to associate the created intermediate entity object ids with entity object ids
        entity_object_id_intermediate_entity_object_id_map = {}

        # retrieves all entities and stores their contents in the intermediate structure
        for entity_class in entity_manager.entity_classes_list:
            entity_name = entity_class.__name__

            # retrieves all entities of this type
            entities = entity_manager._find_all(entity_class)

            # creates an intermediate entity for each entity and populates it with the entity's attributes
            for entity in entities:

                # creates the intermediate entity and indexes it to the intermediate entity for use in the load relations step
                intermediate_entity = intermediate_structure.create_entity(entity_name)
                intermediate_entity_object_id = intermediate_entity.get_object_id()
                entity_object_id_intermediate_entity_object_id_map[entity.object_id] = intermediate_entity_object_id

                # discovers which fields are lazy loaded relations and creates find options to retrieve the entity fully loaded
                find_options = {"eager_loading_relations" : {}}
                relation_attribute_names = entity_manager.get_entity_class_relation_attribute_names(entity_class)
                for attribute_name in relation_attribute_names:
                    find_options["eager_loading_relations"][attribute_name] = {}

                # retrieves the entity again but now fully loaded and indexes it by its object id for use in the load relations step
                entity = entity_manager.find_options(entity_class, entity.object_id, find_options)
                entity_object_id_entity_map[entity.object_id] = entity

                # copies the entity's attributes to the intermediate entity
                non_relation_attribute_names = entity_manager.get_entity_class_non_relation_attribute_names(entity_class)
                for attribute_name in non_relation_attribute_names:
                    attribute_value = getattr(entity, attribute_name)
                    intermediate_entity.set_attribute(attribute_name, attribute_value)

        return (entity_object_id_entity_map, entity_object_id_intermediate_entity_object_id_map)

    def load_relations(self, intermediate_structure, entity_manager, entity_object_id_entity_map, entity_object_id_intermediate_entity_object_id_map):
        """
        Loads the intermediate structure's entities' relations with the entity manager.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to load.
        @type entity_manager: EntityManager
        @param entity_manager: Entity manager used to load the intermediate structure entities' attributes.
        @type entity_object_id_entity_map: Dictionary
        @param entity_object_id_entity_map: Map associating the object ids of the entities created in the load attributes step with the entities themselves.
        @type entity_object_id_intermediate_entity_object_id_map: Dictionary
        @param entity_object_id_intermediate_entity_object_id_map: Map associating the entity object ids with the object ids of the correspondent intermediate entities created in the load attributes step.
        """

        self.io_adapter_entity_manager_plugin.logger.info("[%s] Loading intermediate structure entities' relations with entity manager io adapter" % self.io_adapter_entity_manager_plugin.id)

        # creates a map where to store the computation of intermediate entity non-relation attribute names
        entity_name_relation_attribute_names_map = {}

        # retrieves the entity for each intermediate entity
        entities = entity_object_id_entity_map.values()
        for entity in entities:
            entity_name = entity.__class__.__name__

            # retrieves the correspondent intermediate entity
            intermediate_entity_object_id = entity_object_id_intermediate_entity_object_id_map[entity.object_id]
            intermediate_entity_index = str((entity_name, "object_id", intermediate_entity_object_id))
            intermediate_entity = intermediate_structure.get_entity(intermediate_entity_index)

            # computes which intermediate entity attributes are relation attributes and stores the results so that they don't have to be calculated again
            if entity_name in entity_name_relation_attribute_names_map:
                relation_attribute_names = entity_name_relation_attribute_names_map[entity_name]
            else:
                relation_attribute_names = entity_manager.get_entity_class_relation_attribute_names(entity.__class__)
                entity_name_relation_attribute_names_map[entity_name] = relation_attribute_names

            # retrieves the associated entities and stores them in the intermediate entity they are related with
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
                            intermediate_entity_attribute_value = [intermediate_entity_attribute_value]

                    # retrieves the intermediate entity associated with each related entity and adds it to the intermediate entity's relation attribute
                    for related_entity in related_entities:
                        related_entity_name = related_entity.__class__.__name__
                        related_intermediate_entity_object_id = entity_object_id_intermediate_entity_object_id_map[related_entity.object_id]
                        related_intermediate_entity_index = str((related_entity_name, "object_id", related_intermediate_entity_object_id))
                        related_intermediate_entity = intermediate_structure.get_entity(related_intermediate_entity_index)
                        intermediate_entity_attribute_value.append(related_intermediate_entity)

                    # updates the intermediate entity's relation attribute with the retrieved related intermediate entities
                    intermediate_entity.set_attribute(attribute_name, intermediate_entity_attribute_value)
                elif related_entity_or_entities:
                    # if the entity relation is a "to one" relation
                    related_entity = related_entity_or_entities
                    related_entity_name = related_entity.__class__.__name__
                    related_intermediate_entity = None

                    # retrieves the intermediate entity that corresponds to the related entity
                    if related_entity:
                        related_intermediate_entity_object_id = entity_object_id_intermediate_entity_object_id_map[related_entity.object_id]
                        related_intermediate_entity_index = str((related_entity_name, "object_id", related_intermediate_entity_object_id))
                        related_intermediate_entity = intermediate_structure.get_entity(related_intermediate_entity_index)

                    # updates the intermediate entity's relation attribute with the retrieved related intermediate entity
                    intermediate_entity.set_attribute(attribute_name, related_intermediate_entity)

    def save(self, intermediate_structure, options):
        """
        Saves the intermediate structure with the entity manager at the location and with characteristics defined in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure with the entity manager.
        """

        self.io_adapter_entity_manager_plugin.info("Saving intermediate structure with entity manager io adapter")

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["file_path", "entity_manager_engine"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise io_adapter_entity_manager_exceptions.IoAdapterEntityManagerOptionNotFound("IoAdapterEntityManager.save - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        file_path = options["file_path"]
        entity_manager_engine = options["entity_manager_engine"]

        # retrieves the entity manager plugin
        entity_manager_plugin = self.io_adapter_entity_manager_plugin.entity_manager_plugin

        # initializes the entity manager
        entity_manager = entity_manager_plugin.load_entity_manager(entity_manager_engine)
        entity_manager.set_connection_parameters({"file_path" : file_path, "autocommit" : False})

        # loads the entity manager
        entity_manager.load_entity_manager()

        # saves the intermediate structure entities' attributes
        entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map = self.save_attributes(intermediate_structure, entity_manager)

        # saves the intermediate structure entities' relations
        self.save_relations(intermediate_structure, entity_manager, entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map)

    def save_attributes(self, intermediate_structure, entity_manager):
        """
        Saves the intermediate structure's entities' attributes with the entity manager.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type entity_manager: EntityManager
        @param entity_manager: Entity manager used to save the intermediate structure entities' attributes.
        @rtype: List
        @return: List with a map associating the created entity object ids with the entities themselves and a map associating the object ids of the intermediate entities with the ones of the created entities.
        """

        self.io_adapter_entity_manager_plugin.logger.info("[%s] Saving intermediate structure entities' attributes with entity manager io adapter" % self.io_adapter_entity_manager_plugin.id)

        # dictionary used to index the entities created in the save attributes step by their object id
        entity_object_id_entity_map = {}

        # dictionary used to associate intermediate entity object ids with entity object ids
        intermediate_entity_object_id_entity_object_id_map = {}

        # creates a transaction for the save attributes operation
        entity_manager.create_transaction("io_adapter_entity_manager_save_attributes_transaction")

        # creates a map where to store the computation of intermediate entity non-relation attribute names
        intermediate_entity_name_non_relation_attribute_names_map = {}

        # creates an entity for each intermediate entity in the internal structure and populates it with its attributes
        intermediate_entities = intermediate_structure.get_entities()
        for intermediate_entity in intermediate_entities:

            # retrieves the entity class related with the intermediate entity
            intermediate_entity_name = intermediate_entity.get_name()
            entity_class = entity_manager.get_entity_class(intermediate_entity_name)

            # raises an exception in case the respective entity class is not found
            if not entity_class:
                raise io_adapter_entity_manager_exceptions.IoAdapterEntityManagerEntityClassNotFound("IoAdapterEntityManager.save - Entity class not found (entity_class_name = %s)" % intermediate_entity_name)

            # creates an entity
            entity = entity_class()

            # computes which intermediate entity attributes are not relation attributes and stores the results so that they don't have to be calculated again
            if intermediate_entity_name in intermediate_entity_name_non_relation_attribute_names_map:
                non_relation_attribute_names = intermediate_entity_name_non_relation_attribute_names_map[intermediate_entity_name]
            else:
                non_relation_attribute_names = [attribute_name for attribute_name in intermediate_entity.get_attributes().keys() if type(intermediate_entity.get_attribute(attribute_name)) not in (types.ListType, types.InstanceType)]
                intermediate_entity_name_non_relation_attribute_names_map[intermediate_entity_name] = non_relation_attribute_names

            # populates the entity with the intermediate entity's attributes
            for attribute_name in non_relation_attribute_names:
                intermediate_entity_attribute_value = intermediate_entity.get_attribute(attribute_name)
                setattr(entity, attribute_name, intermediate_entity_attribute_value)

            # saves the entity
            entity_manager.save(entity)

            # index the entity for later usage in the save relations step
            entity_object_id_entity_map[entity.object_id] = entity
            intermediate_entity_object_id_entity_object_id_map[intermediate_entity.object_id] = entity.object_id

        # commits the save attributes operation's transaction
        entity_manager.commit_transaction("io_adapter_entity_manager_save_attributes_transaction")

        return (entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map)

    def save_relations(self, intermediate_structure, entity_manager, entity_object_id_entity_map, intermediate_entity_object_id_entity_object_id_map):
        """
        Saves the intermediate structure's entities' attributes with the entity manager.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type entity_manager: EntityManager
        @param entity_manager: Entity manager used to save the intermediate structure entities' attributes.
        @type entity_object_id_entity_map: Dictionary
        @param entity_object_id_entity_map: Map associating the object ids of the entities created in the save attributes step with the entities themselves.
        @type intermediate_entity_object_id_entity_object_id_map: Dictionary
        @param intermediate_entity_object_id_entity_object_id_map: Map associating the intermediate entity object ids with the object ids of the correspondent entities created in the save attributes step.
        """

        self.io_adapter_entity_manager_plugin.logger.info("[%s] Saving intermediate structure entities' relations with entity manager io adapter" % self.io_adapter_entity_manager_plugin.id)

        # creates a transaction for the save relations operation
        entity_manager.create_transaction("io_adapter_entity_manager_save_relations_transaction")

        # creates a map where to store the computation of intermediate entity non-relation attribute names
        intermediate_entity_name_relation_attribute_names_map = {}

        # creates an entity for each intermediate entity in the internal structure and populates it with its attributes
        intermediate_entities = intermediate_structure.get_entities()
        for intermediate_entity in intermediate_entities:

            # retrieves the respective entity which was created in the save attributes step
            intermediate_entity_name = intermediate_entity.get_name()
            intermediate_entity_object_id = intermediate_entity.get_object_id()
            entity_object_id = intermediate_entity_object_id_entity_object_id_map[intermediate_entity_object_id]
            entity = entity_object_id_entity_map[entity_object_id]

            # computes which intermediate entity attributes are relation attributes and stores the results so that they don't have to be calculated again
            if intermediate_entity_name in intermediate_entity_name_relation_attribute_names_map:
                relation_attribute_names = intermediate_entity_name_relation_attribute_names_map[intermediate_entity_name]
            else:
                relation_attribute_names = [attribute_name for attribute_name in intermediate_entity.get_attributes().keys() if type(intermediate_entity.get_attribute(attribute_name)) in (types.ListType, types.InstanceType)]
                intermediate_entity_name_relation_attribute_names_map[intermediate_entity_name] = relation_attribute_names

            # populates the entity with its related entities
            for attribute_name in relation_attribute_names:
                entity_attribute_value = getattr(entity, attribute_name)
                intermediate_related_entity_or_entities = intermediate_entity.get_attribute(attribute_name)

                # encapsulates the relation attribute's value in a list in case its a "to one" relation in order to reuse the following code
                if type(intermediate_related_entity_or_entities) == types.ListType:
                    intermediate_related_entities = intermediate_related_entity_or_entities
                elif intermediate_related_entity_or_entities:
                    intermediate_related_entities = [intermediate_related_entity_or_entities]
                else:
                    intermediate_related_entities = []

                # retrieves entity that corresponds to the intermediate entity that is in the relation attribute adds it to the entity's relation attribute
                for intermediate_related_entity in intermediate_related_entities:
                    intermediate_related_entity_object_id = intermediate_related_entity.get_object_id()
                    related_entity_object_id = intermediate_entity_object_id_entity_object_id_map[intermediate_related_entity_object_id]
                    related_entity = entity_object_id_entity_map[related_entity_object_id]

                    # raises an exception in case the related entity is not found
                    if not related_entity:
                        intermediate_related_entity_name = intermediate_related_entity.get_name()
                        raise io_adapter_entity_manager_exceptions.IoAdapterEntityManagerEntityClassNotFound("IoAdapterEntityManager.save - Entity class not found (entity_class_name = %s)" % entity_name)

                    # sets the intermediate entity's attribute value in the entity
                    if type(entity_attribute_value) == types.ListType:
                        entity_attribute_value.append(related_entity)
                    elif entity_attribute_value:
                        entity_attribute_value = [entity_attribute_value]
                        entity_attribute_value.append(related_entity)
                    else:
                        entity_attribute_value = related_entity
                    setattr(entity, attribute_name, entity_attribute_value)

            # @todo: skipping updates on the mapped by side because of orm limitation
            try:
                # updates the entity
                entity_manager.update(entity)
            except:
                pass

        # commits the save relations operation's transaction
        entity_manager.commit_transaction("io_adapter_entity_manager_save_relations_transaction")
