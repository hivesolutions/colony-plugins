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

import types

EMPTY_SEARCH_OPTIONS_MAP = {}
""" The empty search options map """

IDENTIFIER_SPLITTER = ":"
""" The symbol to split identifier and parameters """

ARGUMENTS_SPLITTER = ","
""" The symbol to split identifier and arguments """

INDEX_IDENTIFIER_PREFIX = "web_mvc_"
""" The index identifier prefix to be used by all the indexes created """

CREATION_OPTIONS_VALUE = "creation_options"
""" The creation options value """

SEARCH_OPTIONS_VALUE = "search_options"
""" The search options value """

ARGUMENTS_VALUE = "arguments"
""" The arguments value """

SEARCH_CRAWLER_TYPE_VALUE = "search_crawler_type"
""" The key to retrieve the search crawler type from the index configuration map """

SEARCH_CRAWLER_OPTIONS_VALUE = "search_crawler_options"
""" The options value for the search crawler """

SEARCH_PROCESSOR_TYPE_VALUE = "search_processor_type"
""" The key to retrieve the search processor type from the index configuration map """

SEARCH_PROCESSOR_OPTIONS_VALUE = "search_processor_options"
""" The options value for the search processor """

ENTITY_MANAGER_TYPE = "entity_manager"
""" The entity manager type """

TARGET_CLASS_NAMES_VALUE = "target_class_names"
""" The entity manager target class names value """

TARGET_CLASSES_VALUE = "target_classes"
""" The entity manager target classes value """

QUERY_OPTIONS_VALUE = "query_options"
""" The entity manager query options """

ENTITY_MANAGER_ARGUMENTS_VALUE = "entity_manager_arguments"
""" The entity manager arguments value """

FILE_PATH_VALUE = "file_path"
""" The file path value """

CONNECTION_PARAMETERS_VALUE = "connection_parameters"
""" The connection parameters value """

class WebMvcSearch:
    """
    The entity manager search class.
    """

    web_mvc_search_plugin = None
    """ The search plugin """

    def __init__(self, web_mvc_search_plugin):
        """
        Constructor of the class.

        @type web_mvc_search_plugin: WebMvcSearchPlugin
        @param web_mvc_search_plugin: The search plugin.
        """

        self.web_mvc_search_plugin = web_mvc_search_plugin

    def update_index(self, index_identifier, index_configuration_map):
        # retrieves the search manager plugin
        search_manager_plugin = self.web_mvc_search_plugin.search_manager_plugin

        # retrieves the index creation options
        index_creation_options = index_configuration_map[CREATION_OPTIONS_VALUE]

        # retrieves the prefixed index identifier
        prefixed_index_identifier = self._get_prefixed_index_identifier(index_identifier)

        # creates the index for the provided identifier
        search_manager_plugin.create_index_with_identifier(prefixed_index_identifier, index_creation_options)

    def replace_arguments(self, configuration_map, arguments_map):
        # initializes the index configuration
        index_configuration = {}

        for configuration_key in configuration_map:
            configuration_value = configuration_map[configuration_key]
            configuration_value_type = type(configuration_value)

            # in case the value is a map
            if configuration_value_type == types.DictType:
                # recursively replaces the arguments in the value
                index_configuration[configuration_key] = self.replace_arguments(configuration_value, arguments_map)
            # in case it is a list
            elif configuration_value_type in [types.ListType, types.TupleType]:
                # initializes the value list
                value_list = []

                # recursively replaces the arguments for all the values in the list
                for value_element in configuration_value:
                    if type(value_element) == dict:
                        value_list.append(self.replace_arguments(value_element, arguments_map))
                    else:
                        value_list.append(value_element)

                # sets the list in the index configuration
                index_configuration[configuration_key] = value_list
            # in case it is a leaf node of string type
            elif configuration_value_type in types.StringTypes:
                # initializes the formatted value
                formatted_value = configuration_value

                # for all the arguments
                for argument_name in arguments_map:
                    argument_value = arguments_map[argument_name]
                    formatted_value = formatted_value.replace("${" + argument_name + "}", argument_value)

                # finds any of the argument names in the value
                index_configuration[configuration_key] = formatted_value
            # in case it is a leaf node of other kind
            else:
                index_configuration[configuration_key] = configuration_value

        # returns the replaces index configuration
        return index_configuration

    def search_index(self, index_identifier, query_string):
        return self.search_index_options(index_identifier, query_string, EMPTY_SEARCH_OPTIONS_MAP)

    def search_index_options(self, index_identifier, query_string, options):
        # retrieves the search manager plugin
        search_manager_plugin = self.web_mvc_search_plugin.search_manager_plugin

        # retrieves the prefixed index identifier
        prefixed_index_identifier = self._get_prefixed_index_identifier(index_identifier)

        # performs the search
        return search_manager_plugin.search_index_by_identifier(prefixed_index_identifier, query_string, options)

    def create_search_index_controller(self, search_index_identifier, search_index_configuration_map, entity_models_modules):
        # creates a new search index controller object
        search_index_controller = SearchIndexController(self, search_index_identifier)

        # loads the generic index configuration map for the current index
        search_index_controller._load_index_configuration_map(search_index_configuration_map, entity_models_modules)

        # returns the created search index controller
        return search_index_controller

    def has_index(self, search_index_identifier):
        # retrieves the search manager plugin
        search_manager_plugin = self.web_mvc_search_plugin.search_manager_plugin

        # retrieves the prefixed index identifier
        prefixed_index_identifier = self._get_prefixed_index_identifier(search_index_identifier)

        return search_manager_plugin.has_index(prefixed_index_identifier)

    def _get_prefixed_index_identifier(self, index_identifier):
        return INDEX_IDENTIFIER_PREFIX + index_identifier

class SearchIndexController:
    """
    The search index controller class.
    """

    web_mvc_search = None
    """ The web mvc search """

    search_index_configuration_map = {}
    """ The search index configuration map """

    search_index_identifier = "none"
    """ The search identifier for the controlled index """

    def __init__(self, web_mvc_search, search_index_identifier):
        """
        Constructor of the class.

        @type web_mvc_search: WebMvcSearch
        @param web_mvc_search: The web mvc search.
        """

        self.web_mvc_search = web_mvc_search
        self.search_index_identifier = search_index_identifier

    def _load_index_configuration_map(self, base_index_configuration_map, entity_models_modules):
        # splits the index identifier into base index identifier and arguments
        base_index_identifier_arguments_list = self.search_index_identifier.split(IDENTIFIER_SPLITTER, 1)

        # determines the length of the identifier plus arguments list
        base_index_identifier_arguments_list_length = len(base_index_identifier_arguments_list)

        if base_index_identifier_arguments_list_length == 2:
            # retrieves the arguments
            arguments_string = base_index_identifier_arguments_list[1]
        else:
            # retrieves the arguments
            arguments_string = ""

        # retrieves the index creation options
        index_creation_options = base_index_configuration_map.get(CREATION_OPTIONS_VALUE, {})

        # retrieves the configured argument names
        argument_names = index_creation_options.get(ARGUMENTS_VALUE, [])

        # splits the arguments
        argument_values = arguments_string.split(ARGUMENTS_SPLITTER)

        # creates the arguments map from the names and values
        arguments_map = types.DictType(zip(argument_names, argument_values))

        # replaces the arguments in the base index configuration
        index_configuration_map = self.web_mvc_search.replace_arguments(base_index_configuration_map, arguments_map)

        # retrieves the updated the index creation options
        index_creation_options = index_configuration_map.get(CREATION_OPTIONS_VALUE, {})

        # in case the index is of entity manager crawler type
        search_crawler_type = index_creation_options.get(SEARCH_CRAWLER_TYPE_VALUE)

        if not search_crawler_type == ENTITY_MANAGER_TYPE:
            # stores the concrete index configuration in the controller
            self.search_index_configuration_map = index_configuration_map

            # skips the processing for entity manager index types
            return

        # retrieves the search crawler options
        search_crawler_options = index_creation_options.get(SEARCH_CRAWLER_OPTIONS_VALUE, {})

        # retrieves the entity class names list
        entity_class_names = search_crawler_options.get(TARGET_CLASS_NAMES_VALUE, [])

        # determines the corresponding classes for the provided class names
        entity_classes = self.get_entity_classes(entity_class_names, entity_models_modules)

        # sets the entity classes in the index creation options
        search_crawler_options[TARGET_CLASSES_VALUE] = entity_classes

        # retrieves the search options
        search_options = index_configuration_map.get(SEARCH_OPTIONS_VALUE)

        # in case the search options map does not exist
        if not search_options:
            # creates a new search options map
            search_options = {}

            # sets the created search options in the configuration map
            index_configuration_map[SEARCH_OPTIONS_VALUE] = search_options

        # retrieve the search processor type
        search_processor_type = search_options.get(SEARCH_PROCESSOR_TYPE_VALUE)

        # in case the processor type is not of entity manager type:
        if not search_processor_type == ENTITY_MANAGER_TYPE:
            # stores the concrete index configuration in the controller
            self.search_index_configuration_map = index_configuration_map

            # skips the remaining processor options processing
            return

        # retrieves the search processor options
        search_processor_options = search_options.get(SEARCH_PROCESSOR_OPTIONS_VALUE)

        # in case the search processor options map does not exist
        if not search_processor_options:
            # creates a new search options map
            search_processor_options = {}

            # sets the created search processor options in the search options map
            search_options[SEARCH_PROCESSOR_OPTIONS_VALUE] = search_processor_options

        # in case the entity manager arguments are not defined in the processor options
        if not ENTITY_MANAGER_ARGUMENTS_VALUE in search_processor_options:
            # retrieves the entity manager arguments from the creation options
            entity_manager_arguments = search_crawler_options[ENTITY_MANAGER_ARGUMENTS_VALUE]

            # sets the entity manager arguments in the search options
            search_processor_options[ENTITY_MANAGER_ARGUMENTS_VALUE] = entity_manager_arguments

        # in case the classes for the entity manager processor have not been specified
        if not TARGET_CLASSES_VALUE in search_processor_options:
            # retrieves the entity classes from the index creation options
            entity_classes = search_crawler_options[TARGET_CLASSES_VALUE]

            # sets the entity classes in the search options
            search_processor_options[TARGET_CLASSES_VALUE] = entity_classes

        if not QUERY_OPTIONS_VALUE in search_options:
            # retrieves the entity manager crawl options from the index creation options
            crawl_options = search_crawler_options.get(QUERY_OPTIONS_VALUE, {})

            # stores the entity manager process options in the search options map
            search_processor_options[QUERY_OPTIONS_VALUE] = crawl_options

        # retrieves the entity manager arguments from the search processor options
        entity_manager_arguments = search_processor_options.get(ENTITY_MANAGER_ARGUMENTS_VALUE, {})

        # retrieve the connection parameters
        connection_parameters = entity_manager_arguments.get(CONNECTION_PARAMETERS_VALUE, {})

        # resolves the connection parameters
        self._resolve_connection_parameters(connection_parameters)

        # stores the concrete index configuration in the controller
        self.search_index_configuration_map = index_configuration_map

    def update(self):
        # updates the index
        self.web_mvc_search.update_index(self.search_index_identifier, self.search_index_configuration_map)

    def search(self, search_query):
        # the empty search options
        options = {}

        # uses the search options method
        return self.search_options(search_query, options)

    def search_options(self, search_query, options):
        # in case the index was not already created
        if not self.web_mvc_search.has_index(self.search_index_identifier):
            # updates the index, creating if necessary
            self.update()

        # retrieves the index search options from the configuration map
        configured_search_options = self.search_index_configuration_map.get(SEARCH_OPTIONS_VALUE, {})

        # merges the provided options map with the configured search options map
        options.update(configured_search_options)

        return self.web_mvc_search.search_index_options(self.search_index_identifier, search_query, options)

    def get_entity_classes(self, entity_class_names, entity_models_modules):
        # initializes the list of entity classes
        entity_classes = []

        # initializes the map of module names into modules
        modules_map = {}

        # indexes the modules by name
        for entity_models_module in entity_models_modules:
            modules_map[entity_models_module.__name__] = entity_models_module

        # retrieves all the classes
        for entity_class_name in entity_class_names:
            # splits the full class name into namespace tokens
            entity_class_tokens = entity_class_name.split(".")

            # retrieves the starting module name
            entity_module_name = entity_class_tokens[0]

            # retrieves the starting module
            entity_models_module = modules_map[entity_module_name]

            # for the remaining tokens
            for entity_class_token in entity_class_tokens[1:]:
                # retrieves the relevant root module
                module_attribute = getattr(entity_models_module, entity_class_token)

                # determines the module attribute type
                module_attribute_type = type(module_attribute)

                # in case the attribute is not a module, the class was found
                if not module_attribute_type == types.ModuleType:
                    entity_classes.append(module_attribute)

                    # stops processing
                    break

                # iterates for the next module, depth first
                entity_models_module = module_attribute

        # returns the entity classes
        return entity_classes

    def _resolve_connection_parameters(self, connection_parameters):
        """
        Resolves the given connection parameters map, substituting
        the values with the resolved ones.

        @type connection_parameters: Dictionary
        @param connection_parameters: The connection parameters to be resolved.
        """

        # retrieves the web mvc search plugin
        web_mvc_search_plugin = self.web_mvc_search.web_mvc_search_plugin

        # retrieves the plugin manager
        plugin_manager = web_mvc_search_plugin.manager

        # resolves the file path
        connection_parameters[FILE_PATH_VALUE] = plugin_manager.resolve_file_path(connection_parameters[FILE_PATH_VALUE], True, True)
