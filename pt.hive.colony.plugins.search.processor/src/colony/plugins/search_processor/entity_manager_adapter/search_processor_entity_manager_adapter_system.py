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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
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

import search_processor_entity_manager_adapter_exceptions

SEARCH_PROCESSOR_ADAPTER_TYPE = "entity_manager"
""" The current search processor adapter type """

ENTITY_MANAGER_ARGUMENTS_VALUE = "entity_manager_arguments"
""" The entity manager arguments value """

TARGET_CLASSES_VALUE = "target_classes"
""" The entity manager target classes value """

QUERY_OPTIONS_VALUE = "query_options"
""" The entity manager query options value """

ENGINE_VALUE = "engine"
""" The engine value """

CONNECTION_PARAMETERS_VALUE = "connection_parameters"
""" The connection parameters value """

ENTITY_CLASSES_LIST_VALUE = "entity_classes_list"
""" The entity classes list value """

ENTITY_CLASSES_MAP_VALUE = "entity_classes_map"
""" The entity classes map value """

DEFAULT_ENGINE = "sqlite"
""" The default engine """

DEFAULT_CONNECTION_PARAMETERS = {
    "autocommit" : False
}
""" The default connection parameters """

class SearchProcessorEntityManagerAdapter:
    """
    The search processor file system adapter class.
    """

    search_processor_entity_manager_adapter_plugin = None
    """ The search processor file system adapter plugin """

    def __init__(self, search_processor_entity_manager_adapter_plugin):
        """
        Constructor of the class.

        @type search_processor_entity_manager_adapter_plugin: SearchProcessorEntityManagerAdapterPlugin
        @param search_processor_entity_manager_adapter_plugin: The search processor file system adapter plugin.
        """

        self.search_processor_entity_manager_adapter_plugin = search_processor_entity_manager_adapter_plugin

    def get_type(self):
        return SEARCH_PROCESSOR_ADAPTER_TYPE

    def process_results(self, search_results, properties):
        # initializes the entity list
        entities = []

        if not ENTITY_MANAGER_ARGUMENTS_VALUE in properties:
            raise search_processor_entity_manager_adapter_exceptions.MissingProperty(ENTITY_MANAGER_ARGUMENTS_VALUE)

        # retrieves the entity manager plugin
        entity_manager_plugin = self.search_processor_entity_manager_adapter_plugin.entity_manager_plugin

        # retrieves the business helper plugin
        business_helper_plugin = self.search_processor_entity_manager_adapter_plugin.business_helper_plugin

        # retrieves the entity manager arguments
        entity_manager_arguments = properties[ENTITY_MANAGER_ARGUMENTS_VALUE]

        # tries to retrieve the list of entity classes from the properties
        if TARGET_CLASSES_VALUE in properties:
            entity_classes_list = properties[TARGET_CLASSES_VALUE]
        # in case no entity specification is provided
        else:
            raise search_processor_entity_manager_adapter_exceptions.MissingProperty(TARGET_CLASSES_VALUE)

        # generates the entity models map from the base entity models list
        # creating the map associating the class names with the classes
        entity_classes_map = business_helper_plugin.generate_bundle_map(entity_classes_list)

        # retrieves the engine from the entity manager arguments or uses
        # the default engine
        engine = entity_manager_arguments.get(ENGINE_VALUE, DEFAULT_ENGINE)

        # retrieves the connection parameters from the entity manager arguments or uses
        # the default connection parameters
        connection_parameters = entity_manager_arguments.get(CONNECTION_PARAMETERS_VALUE, DEFAULT_CONNECTION_PARAMETERS)

        # creates the entity manager properties
        entity_manager_properties = {
            ENTITY_CLASSES_LIST_VALUE : entity_classes_list,
            ENTITY_CLASSES_MAP_VALUE : entity_classes_map
        }

        # creates a new entity manager with the given properties
        entity_manager = entity_manager_plugin.load_entity_manager_properties(engine, entity_manager_properties)

        # sets the connection parameters for the entity manager
        entity_manager.set_connection_parameters(connection_parameters)

        # loads the entity manager
        entity_manager.load_entity_manager()

        # tries to retrieve query options from the processor options
        find_options = properties.get(QUERY_OPTIONS_VALUE, {})

        # retrieves the list of entities, from the search results
        for search_result in search_results:
            # retrieves the document id of the search result
            entity_object_id = search_result["document_id"]

            # retrieves additional document metadata
            document_information_map = search_result["document_information_map"]

            # retrieves the entity class name
            entity_class_name = document_information_map["entity_class_name"]

            # retrieves the corresponding entity class
            entity_class = entity_manager.get_entity_class(entity_class_name)

            # retrieves the entity using the provided document id
            entity = entity_manager.find_options(entity_class, entity_object_id, find_options)

            # appends the retrieved entity to the entity list
            entities.append(entity)

        return entities
