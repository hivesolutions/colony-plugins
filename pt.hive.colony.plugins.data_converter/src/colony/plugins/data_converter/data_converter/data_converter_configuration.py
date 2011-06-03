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

ARGUMENTS_VALUE = "arguments"
""" The arguments value """

ATTRIBUTES_VALUE = "attributes"
""" The attributes value """

ATTRIBUTE_MAPPING_VALUE = "attribute_mapping"
""" The attribute mapping value """

CONNECTORS_VALUE = "connectors"
""" The connectors value """

ENTITY_MAPPING_VALUE = "entity_mapping"
""" The entity mapping value """

ENTITY_NAMES_VALUE = "entity_names"
""" The entity names value """

ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE = "entity_relation_attribute_names"
""" The entity relation attribute names value """

FUNCTION_VALUE = "function"
""" The function value """

HANDLERS_VALUE = "handlers"
""" The handlers value """

INPUT_DEPENDENCIES_VALUE = "input_dependencies"
""" The input dependencies value """

INPUT_ENTITIES_VALUE = "input_entities"
""" The input entities value """

INPUT_ENTITY_MAPPING_VALUE = "InputEntityMapping"
""" The input entity mapping value """

INPUT_NAME_VALUE = "input_name"
""" The input name value """

INPUT_OUTPUT_ENTITY_MAPPING_VALUE = "InputOutputEntityMapping"
""" The input output entity mapping value """

INPUT_VALUE_VALUE = "input_value"
""" The input value """

LIST_TYPE_VALUE = "list_type"
""" The list type value """

NAME_VALUE = "name"
""" The name value """

OUTPUT_ATTRIBUTE_MAPPING_VALUE = "OutputAttributeMapping"
""" The output attribute mapping value """

OUTPUT_ENTITY_MAPPING_VALUE = "OutputEntityMapping"
""" The output entity mapping value """

OUTPUT_DEPENDENCIES_VALUE = "output_dependencies"
""" The output dependencies value """

OUTPUT_NAME_VALUE = "output_name"
""" The output name value """

RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE = "related_entity_relation_attribute_names"
""" The related entity relation attribute names value """

RELATION_MAPPING_VALUE = "RelationMapping"
""" The relation mapping value """

RELATIONS_VALUE = "relations"
""" The relations value """

TYPES_VALUE = "types"
""" The types value """

VALIDATORS_VALUE = "validators"
""" The validators value """

OUTPUT_ENTITY_MAPPING_DESCRIPTION_TEMPLATE = "name = %s"
""" The output entity mapping description template """

INPUT_ENTITY_MAPPING_DESCRIPTION_TEMPLATE = "name = %s"
""" The input entity mapping description template """

OUTPUT_ATTRIBUTE_MAPPING_DESCRIPTION_TEMPLATE = "name = %s"
""" The output attribute mapping description template """

RELATION_MAPPING_DESCRIPTION_TEMPLATE = "relation_attribute_names = %s; related_entity_relation_attribute_names = %s"
""" The relation mapping description template """

class DataConverterConfiguration:
    """
    Stores a data converter configuration.
    """

    configuration_plugin_id = None
    """ Unique identifier for the configuration plugin this configuration was created from """

    configuration_id = None
    """ Configuration unique identifier assigned to this configuration """

    intermediate_structure_schema = None
    """ The output intermediate structure's schema """

    input_io_adapters_options = []
    """ Lists with maps with the options to provide the input io adapter """

    output_entity_name_output_entity_mapping_map = {}
    """ Dictionary relating the name of an output entity with its mapping configuration """

    global_input_entity_indexers = []
    """ List of input indexers to apply to every entity """

    input_entity_name_indexers_map = {}
    """ Dictionary relating the name of an input entity with the indexers to run on it """

    global_output_entity_indexers = []
    """ List of output indexers to apply to every entity """

    output_entity_name_indexers_map = {}
    """ Dictionary relating the name of an output entity with the indexers to run on it """

    post_attribute_mapping_handlers = []
    """ List of handlers to be executed at the end of the attribute mapping conversion step """

    post_conversion_handlers = []
    """ List of handlers to be executed at the end of the conversion """

    output_io_adapters_options = {}
    """ Lists with maps with the options to provide the output io adapter """

    next_configuration_item_id = 0
    """ Unique identifier for the next data converter configuration item """

    configuration_item_type_configuration_item_ids_map = {}
    """ Dictionary relating a configuration item type a list of unique identifiers of its instances """

    configuration_item_id_configuration_item_type_map = {}
    """ Dictionary relating the unique identifier of a configuration item with its type """

    configuration_item_id_configuration_item_map = {}
    """ Dictionary relating the unique identifier of a configuration item with its unique identifier """

    configuration_item_id_dependent_configuration_item_ids_map = {}
    """ Dictionary relating the unique identifier of a configuration item with the unique identifiers of the ones that depend on it """

    configuration_item_id_enabled_map = {}
    """ Dictionary relating the unique identifier of a configuration item with a boolean indicating if its enabled or not """

    option_name_value_map = {}
    """ Dictionary associating an option's name with it's value """

    def __init__(self, configuration_plugin_id, configuration_id):
        self.configuration_plugin_id = configuration_plugin_id
        self.configuration_id = configuration_id
        self.intermediate_structure_schema = None
        self.input_io_adapters_options = []
        self.output_entity_name_enabled_map = {}
        self.output_entity_name_output_entity_mapping_map = {}
        self.global_input_entity_indexers = []
        self.input_entity_name_indexers_map = {}
        self.global_output_entity_indexers = []
        self.output_entity_name_indexers_map = {}
        self.post_attribute_mapping_handlers = []
        self.post_conversion_handlers = []
        self.output_io_adapters_options = []
        self.next_configuration_item_id = 0
        self.configuration_item_id_configuration_item_type_map = {}
        self.configuration_item_id_configuration_item_map = {}
        self.configuration_item_id_dependent_configuration_item_ids_map = {}
        self.configuration_item_id_enabled_map = {}
        self.configuration_item_type_configuration_item_ids_map = {}
        self.configuration_item_type_configuration_item_ids_map[OUTPUT_ENTITY_MAPPING_VALUE] = []
        self.configuration_item_type_configuration_item_ids_map[INPUT_ENTITY_MAPPING_VALUE] = []
        self.configuration_item_type_configuration_item_ids_map[INPUT_OUTPUT_ENTITY_MAPPING_VALUE] = []
        self.configuration_item_type_configuration_item_ids_map[OUTPUT_ATTRIBUTE_MAPPING_VALUE] = []
        self.configuration_item_type_configuration_item_ids_map[RELATION_MAPPING_VALUE] = []
        self.option_name_value_map = {}

    def __str__(self):
        return self.configuration_plugin_id

    def get_configuration_id(self):
        return self.configuration_id

    def get_configuration_item_ids(self):
        # retrieves the unique identifiers for the currently defined configuration items
        configuration_item_ids = self.configuration_item_id_configuration_item_map.keys()

        return configuration_item_ids

    def get_configuration_item_ids_by_type(self, configuration_item_type):
        # raises an exception in case no configuration item of the specified type is defined
        if not configuration_item_type in self.configuration_item_type_configuration_item_ids_map:
            raise data_converter_exceptions.DataConverterConfigurationConfigurationItemTypeNotDefined(str(configuration_item_type))

        # retrieves the unique identifiers for the defined configuration items with the specified type
        configuration_item_ids = self.configuration_item_type_configuration_item_ids_map[configuration_item_type]

        return configuration_item_ids

    def get_enabled_configuration_item_ids_by_type(self, configuration_item_type):
        # retrieves the unique identifiers for the enabled configuration items that are of the specified type
        configuration_item_ids = self.get_configuration_item_ids_by_type(configuration_item_type)
        configuration_item_ids = [configuration_item_id for configuration_item_id in configuration_item_ids if self.configuration_item_id_enabled_map[configuration_item_id]]

        return configuration_item_ids

    def get_next_configuration_item_id(self):
        # retrieves the next configuration item id
        self.next_configuration_item_id += 1

        return self.next_configuration_item_id

    def get_configuration_item(self, configuration_item_id):
        # raises an exception in case the configuration item with the specified unique identifier doesn't exist
        if not configuration_item_id in self.configuration_item_id_configuration_item_map:
            raise data_converter_exceptions.DataConverterConfigurationConfigurationItemNotDefined(str(configuration_item_id))

        # retrieves the specified configuration item
        configuration_item = self.configuration_item_id_configuration_item_map[configuration_item_id]

        return configuration_item

    def is_configuration_item_enabled(self, configuration_item_id):
        # raises an exception in case the configuration item with the specified unique identifier doesn't exist
        if not configuration_item_id in self.configuration_item_id_configuration_item_map:
            raise data_converter_exceptions.DataConverterConfigurationConfigurationItemNotDefined(str(configuration_item_id))

        # retrieves the specified configuration item's enabled status
        enabled = self.configuration_item_id_enabled_map[configuration_item_id]

        return enabled

    def enable_configuration_item(self, configuration_item_id):
        # raises an exception in case the configuration item with the specified unique identifier doesn't exist
        if not configuration_item_id in self.configuration_item_id_configuration_item_map:
            raise data_converter_exceptions.DataConverterConfigurationConfigurationItemNotDefined(str(configuration_item_id))

        # raises an exception in case the specified configuration item is already enabled
        if self.configuration_item_id_enabled_map[configuration_item_id]:
            raise data_converter_exceptions.DataConverterConfigurationConfigurationItemAlreadyEnabled(str(configuration_item_id))

        # enables the specified configuration item
        configuration_item = self.get_configuration_item(configuration_item_id)
        configuration_item.enable()
        self.configuration_item_id_enabled_map[configuration_item_id] = True

        # enables the configuration items that depend on the specified configuration item
        dependent_configuration_item_ids = self.get_all_dependent_configuration_item_ids(configuration_item_id)
        for dependent_configuration_item_id in dependent_configuration_item_ids:
            configuration_item = self.get_configuration_item(dependent_configuration_item_id)
            configuration_item.enable()
            self.configuration_item_id_enabled_map[dependent_configuration_item_id] = True

    def disable_configuration_item(self, configuration_item_id):
        # raises an exception in case the configuration item with the specified unique identifier doesn't exist
        if not configuration_item_id in self.configuration_item_id_configuration_item_map:
            raise data_converter_exceptions.DataConverterConfigurationConfigurationItemNotDefined(str(configuration_item_id))

        # raises an exception in case the specified configuration item is already disabled
        if not self.configuration_item_id_enabled_map[configuration_item_id]:
            raise data_converter_exceptions.DataConverterConfigurationConfigurationItemAlreadyDisabled(str(configuration_item_id))

        # disables the specified configuration item
        configuration_item = self.get_configuration_item(configuration_item_id)
        configuration_item.disable()
        self.configuration_item_id_enabled_map[configuration_item_id] = False

        # disables the configuration items that depend on the specified configuration item
        dependent_configuration_item_ids = self.get_all_dependent_configuration_item_ids(configuration_item_id)
        for dependent_configuration_item_id in dependent_configuration_item_ids:
            configuration_item = self.get_configuration_item(dependent_configuration_item_id)
            configuration_item.disable()
            self.configuration_item_id_enabled_map[dependent_configuration_item_id] = False

    def create_configuration_item(self, parent_configuration_item, configuration_item_type, configuration):
        configuration_item_class = None

        # retrieves the class for the specified configuration item type
        if configuration_item_type == OUTPUT_ENTITY_MAPPING_VALUE:
            configuration_item_class = OutputEntityMapping
        elif configuration_item_type == INPUT_ENTITY_MAPPING_VALUE:
            configuration_item_class = InputEntityMapping
        elif configuration_item_type == INPUT_OUTPUT_ENTITY_MAPPING_VALUE:
            configuration_item_class = InputOutputEntityMapping
        elif configuration_item_type == OUTPUT_ATTRIBUTE_MAPPING_VALUE:
            configuration_item_class = OutputAttributeMapping
        elif configuration_item_type == RELATION_MAPPING_VALUE:
            configuration_item_class = RelationMapping
        else:
            # raises an exception in case the specified configuration item type doesn't exist
            raise data_converter_exceptions.DataConverterConfigurationConfigurationItemTypeNotRecognized(str(configuration_item_type))

        # creates a configuration item of the specified type
        configuration_item_id = self.get_next_configuration_item_id()
        self.configuration_item_id_enabled_map[configuration_item_id] = True
        self.configuration_item_id_dependent_configuration_item_ids_map[configuration_item_id] = []
        self.configuration_item_type_configuration_item_ids_map[configuration_item_type].append(configuration_item_id)
        self.configuration_item_id_configuration_item_type_map[configuration_item_id] = configuration_item_type
        configuration_item = configuration_item_class(self, parent_configuration_item, configuration_item_id)
        self.configuration_item_id_configuration_item_map[configuration_item_id] = configuration_item

        # adds the provided initial configuration to the configuration item
        configuration_item.add_configuration(configuration)

        return configuration_item

    def add_configuration_item_dependency(self, configuration_item_id, dependent_configuration_item_id):
        # raises an exception in case the configuration item with the specified unique identifier doesn't exist
        if not configuration_item_id in self.configuration_item_id_configuration_item_map:
            raise data_converter_exceptions.DataConverterConfigurationConfigurationItemNotDefined(str(configuration_item_id))

        # raises an exception in case the dependent configuration item with the specified unique identifier doesn't exist
        if not dependent_configuration_item_id in self.configuration_item_id_configuration_item_map:
            raise data_converter_exceptions.DataConverterConfigurationConfigurationItemNotDefined(str(dependent_configuration_item_id))

        # stores the dependency relationship between the two configuration items
        self.configuration_item_id_dependent_configuration_item_ids_map[configuration_item_id].append(dependent_configuration_item_id)

    def get_dependent_configuration_item_ids(self, configuration_item_id):
        # raises an exception in case the configuration item with the specified unique identifier doesn't exist
        if not configuration_item_id in self.configuration_item_id_configuration_item_map:
            raise data_converter_exceptions.DataConverterConfigurationConfigurationItemNotDefined(str(configuration_item_id))

        # retrieves the unique identifiers for the configuration items that depend on the specified configuration item
        dependent_configuration_item_ids = self.configuration_item_id_dependent_configuration_item_ids_map[configuration_item_id]

        return dependent_configuration_item_ids

    def get_dependent_configuration_item_ids_by_type(self, configuration_item_id, configuration_item_type):
        # retrieves the unique identifiers for the configuration items that depend on the specified configuration item and are of the specified type
        dependent_configuration_item_ids = self.get_dependent_configuration_item_ids(configuration_item_id)
        dependent_configuration_item_ids = [dependent_configuration_item_id for dependent_configuration_item_id in dependent_configuration_item_ids if self.configuration_item_id_configuration_item_type_map[dependent_configuration_item_id] == configuration_item_type]

        return dependent_configuration_item_ids

    def get_enabled_dependent_configuration_item_ids_by_type(self, configuration_item_id, configuration_item_type):
        # retrieves the unique identifiers for the enabled configuration items that depend on the specified configuration item and are of the specified type
        dependent_configuration_item_ids = self.get_dependent_configuration_item_ids_by_type(configuration_item_id, configuration_item_type)
        dependent_configuration_item_ids = [dependent_configuration_item_id for dependent_configuration_item_id in dependent_configuration_item_ids if self.configuration_item_id_enabled_map[dependent_configuration_item_id]]

        return dependent_configuration_item_ids

    def get_all_dependent_configuration_item_ids(self, configuration_item_id):
        # retrieves the unique identifiers for the configuration items that depend on the specified configuration item
        dependent_configuration_item_ids = self.get_dependent_configuration_item_ids(configuration_item_id)
        processed_dependent_configuration_item_ids = []
        pending_dependent_configuration_item_ids = []

        # collects the unique identifiers for all configuration items that directly or indirectly depend on the specified configuration item
        while dependent_configuration_item_ids:

            # retrieves the unique identifiers for the configuration items that depend on each configuration item
            for dependent_configuration_item_id in dependent_configuration_item_ids:
                if not dependent_configuration_item_id in processed_dependent_configuration_item_ids:
                    processed_dependent_configuration_item_ids.append(dependent_configuration_item_id)
                    pending_dependent_configuration_item_ids.extend(self.get_dependent_configuration_item_ids(dependent_configuration_item_id))

            # adds the configuration item ids whose dependent item ids still need to be collected to the list for use in the next iteration
            dependent_configuration_item_ids = pending_dependent_configuration_item_ids
            pending_dependent_configuration_item_ids = []

        return processed_dependent_configuration_item_ids

    def get_all_enabled_dependent_configuration_item_ids_by_type(self, configuration_item_id, configuration_item_type):
        # retrieves unique identifiers for all configuration item ids that directly or indirectly depend on the specified configuration item
        dependent_configuration_item_ids = self.get_all_dependent_configuration_item_ids(configuration_item_id)

        # filters the dependent configuration item ids list to leave only the ones that are enabled
        dependent_configuration_item_ids = [dependent_configuration_item_id for dependent_configuration_item_id in dependent_configuration_item_ids if self.get_configuration_item(dependent_configuration_item_id).is_enabled()]

        # filters the dependent configuration item ids list to leave only the ones that are of the specified type
        dependent_configuration_item_ids = [dependent_configuration_item_id for dependent_configuration_item_id in dependent_configuration_item_ids if self.get_configuration_item(dependent_configuration_item_id).__class__.__name__ == configuration_item_type]

        return dependent_configuration_item_ids

    def add_attribute_mapping_output_entities(self, attribute_mapping_output_entities):
        # adds the specified entity mappings to this configuration
        for attribute_mapping_output_entity in attribute_mapping_output_entities:
            output_entity_name = attribute_mapping_output_entity[OUTPUT_NAME_VALUE]

            # creates an output entity mapping configuration item in case one doesn't exist for entities with the current name
            if not output_entity_name in self.output_entity_name_output_entity_mapping_map:
                configuration_item = self.create_configuration_item(self, OUTPUT_ENTITY_MAPPING_VALUE, attribute_mapping_output_entity)
                self.output_entity_name_output_entity_mapping_map[output_entity_name] = configuration_item
            else:
                # otherwise adds the configuration to the output entity mapping configuration
                configuration_item = self.output_entity_name_output_entity_mapping_map[output_entity_name]
                configuration_item.add_configuration(attribute_mapping_output_entity)

    def add_relation_mapping_entities(self, relation_mapping_entities):
        # adds the specified relation mappings to this configuration
        for relation_mapping_entity in relation_mapping_entities:
            output_entity_name = relation_mapping_entity[OUTPUT_NAME_VALUE]

            # raises an exception if no output entity mapping is defined for output entities with the current name
            if not output_entity_name in self.output_entity_name_output_entity_mapping_map:
                raise data_converter_exceptions.DataConverterConfigurationOutputEntityNotDefined(output_entity_name)

            # adds the relation mapping to the output entity mapping
            self.output_entity_name_output_entity_mapping_map[output_entity_name].add_configuration(relation_mapping_entity)

    def get_post_attribute_mapping_handlers(self):
        return self.post_attribute_mapping_handlers

    def add_post_attribute_mapping_handlers(self, post_attribute_mapping_handlers):
        self.post_attribute_mapping_handlers.extend([Function(post_attribute_mapping_handler) for post_attribute_mapping_handler in post_attribute_mapping_handlers])

    def get_post_conversion_handlers(self):
        return self.post_conversion_handlers

    def add_post_conversion_handlers(self, post_conversion_handlers):
        self.post_conversion_handlers.extend([Function(post_conversion_handler) for post_conversion_handler in post_conversion_handlers])

    def get_global_input_entity_indexers(self):
        return self.global_input_entity_indexers

    def get_input_entity_indexers(self, input_entity_name):
        input_entity_indexers = self.input_entity_name_indexers_map.get(input_entity_name, [])

        return input_entity_indexers

    def add_input_entity_indexers(self, input_entity_indexers):
        # adds each input indexer to the configuration
        for input_indexer in input_entity_indexers:

            # retrieves the input entity names the indexer applies to
            entity_names = input_indexer.get(ENTITY_NAMES_VALUE, None)

            input_indexer_function = Function(input_indexer)

            # associates the indexer with each entity name in case
            # such an association was specified
            if entity_names:
                for entity_name in entity_names:

                    # allocates a location for the indexers of the input entity with the current name
                    # if it was not allocated before
                    if not entity_name in self.input_entity_name_indexers_map:
                        self.input_entity_name_indexers_map[entity_name] = []

                    # associates the indexer with the entity name
                    if not input_indexer_function in self.input_entity_name_indexers_map[entity_name]:
                        self.input_entity_name_indexers_map[entity_name].append(input_indexer_function)
            elif not input_indexer_function in self.global_input_entity_indexers:
                # otherwise adds the indexer to the list of global input indexers
                self.global_input_entity_indexers.append(input_indexer_function)

    def get_global_output_entity_indexers(self):
        return self.global_output_entity_indexers

    def get_output_entity_indexers(self, output_entity_name):
        output_entity_indexers = self.output_entity_name_indexers_map.get(output_entity_name, [])

        return output_entity_indexers

    def add_output_entity_indexers(self, output_entity_indexers):
        # adds each output indexer to the configuration
        for output_indexer in output_entity_indexers:

            # retrieves the output entity names the indexer applies to
            entity_names = output_indexer.get(ENTITY_NAMES_VALUE, None)

            output_indexer_function = Function(output_indexer)

            # associates the indexer with each entity name in case
            # such an association was specified
            if entity_names:
                for entity_name in entity_names:

                    # allocates a location for the indexers of the output entity with the current name
                    # if it was not allocated before
                    if not entity_name in self.output_entity_name_indexers_map:
                        self.output_entity_name_indexers_map[entity_name] = []

                    # associates the indexer with the entity name
                    if not output_indexer_function in self.output_entity_name_indexers_map[entity_name]:
                        self.output_entity_name_indexers_map[entity_name].append(output_indexer_function)
            elif not output_indexer_function in self.global_output_entity_indexers:
                # otherwise adds the indexer to the list of global output indexers
                self.global_output_entity_indexers.append(output_indexer_function)

    def get_output_entity_names(self):
        # retrieves the names of the output entities defined in this configuration
        output_entity_names = self.output_entity_name_enabled_map.keys()

        return output_entity_names

    def get_output_entity_mapping(self, output_entity_name):
        # raises an exception in case the specified output entity is not defined
        if not output_entity_name in self.output_entity_name_output_entity_mapping_map:
            raise data_converter_exceptions.DataConverterConfigurationOutputEntityNotDefined(str(output_entity_name))

        # retrieves the output entity mapping for output entities with the specified name
        output_entity_mapping = self.output_entity_name_output_entity_mapping_map[output_entity_name]

        return output_entity_mapping

    def get_input_io_adapters_options(self):
        return self.input_io_adapters_options

    def add_input_io_adapters_options(self, input_io_adapter_options):
        self.input_io_adapters_options.extend(input_io_adapter_options)

    def get_output_io_adapters_options(self):
        return self.output_io_adapters_options

    def add_output_io_adapters_options(self, output_io_adapter_options):
        self.output_io_adapters_options.extend(output_io_adapter_options)

    def get_input_dependencies(self):
        # retrieves the input dependencies of this configuration's input entity mappings
        output_entity_mapping_dependencies_maps = [output_entity_mapping.get_input_dependencies() for output_entity_mapping in self.configuration_item_type_configuration_item_ids_map[OUTPUT_ENTITY_MAPPING_VALUE]]

        # retrieves the input dependencies of this configuration's post conversion handlers
        post_conversion_handler_dependencies_maps = [post_conversion_handler.get_input_dependencies() for post_conversion_handler in self.post_conversion_handlers]

        # retrieves the input dependencies of this configuration's global input entity indexers
        input_indexers_dependencies_maps = [input_entity_indexer.get_input_dependencies() for input_entity_indexer in self.global_input_entity_indexers]
        for input_entity_indexers in self.input_entity_name_indexers_map.values():
            input_indexers_dependencies_maps.extend([input_entity_indexer.get_input_dependencies() for input_entity_indexer in input_entity_indexers])

        # merges the input dependencies of this configuration
        dependencies_maps = []
        dependencies_maps.extend(output_entity_mapping_dependencies_maps)
        dependencies_maps.extend(post_conversion_handler_dependencies_maps)
        dependencies_maps.extend(input_indexers_dependencies_maps)
        input_dependencies_map = merge_dependency_maps(dependencies_maps)

        return input_dependencies_map

    def get_enabled_input_dependencies(self):
        # retrieves the input dependencies of this configuration's input entity mappings
        output_entity_mapping_dependencies_maps = [self.get_configuration_item(output_entity_mapping_id).get_input_dependencies() for output_entity_mapping_id in self.configuration_item_type_configuration_item_ids_map[OUTPUT_ENTITY_MAPPING_VALUE] if self.get_configuration_item(output_entity_mapping_id).is_enabled()]

        # retrieves the input dependencies of this configuration's post conversion handlers
        post_conversion_handler_dependencies_maps = [post_conversion_handler.get_input_dependencies() for post_conversion_handler in self.post_conversion_handlers]

        # retrieves the input dependencies of this configuration's global input entity indexers
        input_indexers_dependencies_maps = [input_entity_indexer.get_input_dependencies() for input_entity_indexer in self.global_input_entity_indexers]
        for input_entity_indexers in self.input_entity_name_indexers_map.values():
            input_indexers_dependencies_maps.extend([input_entity_indexer.get_input_dependencies() for input_entity_indexer in input_entity_indexers])

        # merges the input dependencies of this configuration
        dependencies_maps = []
        dependencies_maps.extend(output_entity_mapping_dependencies_maps)
        dependencies_maps.extend(post_conversion_handler_dependencies_maps)
        dependencies_maps.extend(input_indexers_dependencies_maps)
        input_dependencies_map = merge_dependency_maps(dependencies_maps)

        return input_dependencies_map

    def get_output_dependencies(self):
        # retrieves the output dependencies of this configuration's output entity mappings
        output_entity_mapping_dependencies_maps = [output_entity_mapping.get_output_dependencies() for output_entity_mapping in self.configuration_item_type_configuration_item_ids_map[OUTPUT_ENTITY_MAPPING_VALUE]]

        # retrieves the output dependencies of this configuration's post conversion handlers
        post_conversion_handler_dependencies_maps = [post_conversion_handler.get_output_dependencies() for post_conversion_handler in self.post_conversion_handlers]

        # retrieves the output dependencies of this configuration's global output entity indexers
        output_indexers_dependencies_maps = [output_entity_indexer.get_output_dependencies() for output_entity_indexer in self.global_output_entity_indexers]
        for output_entity_indexers in self.output_entity_name_indexers_map.values():
            output_indexers_dependencies_maps.extend([output_entity_indexer.get_output_dependencies() for output_entity_indexer in output_entity_indexers])

        # merges the output dependencies of this configuration
        dependencies_maps = []
        dependencies_maps.extend(output_entity_mapping_dependencies_maps)
        dependencies_maps.extend(post_conversion_handler_dependencies_maps)
        dependencies_maps.extend(output_indexers_dependencies_maps)
        output_dependencies_map = merge_dependency_maps(dependencies_maps)

        return output_dependencies_map

    def get_enabled_output_dependencies(self):
        # retrieves the output dependencies of this configuration's output entity mappings
        output_entity_mapping_dependencies_maps = [output_entity_mapping.get_output_dependencies() for output_entity_mapping in self.configuration_item_type_configuration_item_ids_map[OUTPUT_ENTITY_MAPPING_VALUE] if output_entity_mapping.is_enabled()]

        # retrieves the output dependencies of this configuration's post conversion handlers
        post_conversion_handler_dependencies_maps = [post_conversion_handler.get_output_dependencies() for post_conversion_handler in self.post_conversion_handlers]

        # retrieves the output dependencies of this configuration's global output entity indexers
        output_indexers_dependencies_maps = [output_entity_indexer.get_output_dependencies() for output_entity_indexer in self.global_output_entity_indexers]
        for output_entity_indexers in self.output_entity_name_indexers_map.values():
            output_indexers_dependencies_maps.extend([output_entity_indexer.get_output_dependencies() for output_entity_indexer in output_entity_indexers])

        # merges the output dependencies of this configuration
        dependencies_maps = []
        dependencies_maps.extend(output_entity_mapping_dependencies_maps)
        dependencies_maps.extend(post_conversion_handler_dependencies_maps)
        dependencies_maps.extend(output_indexers_dependencies_maps)
        output_dependencies_map = merge_dependency_maps(dependencies_maps)

        return output_dependencies_map

    def get_intermediate_structure_schema(self):
        return self.intermediate_structure_schema

    def add_intermediate_entity_schemas(self, intermediate_entity_schemas):
        # initializes the intermediate structure schema in case it isn't yet
        if not self.intermediate_structure_schema:
            self.intermediate_structure_schema = {}

        # merges each provided intermediates structure schema part into the current intermediate
        # structure schema
        for intermediate_entity_schema in intermediate_entity_schemas:

            # retrieves the intermediate structure schema's mandatory options
            entity_name = intermediate_entity_schema[NAME_VALUE]
            entity_schema = intermediate_entity_schema[ATTRIBUTES_VALUE]

            # merges the current entity schema with the provided entity schema and
            # stores it in the configuration's intermediates structure schema
            current_entity_schema = self.intermediate_structure_schema.get(entity_name, {})
            current_entity_schema = self.merge_entity_schemas(current_entity_schema, entity_schema)
            self.intermediate_structure_schema[entity_name] = current_entity_schema

    def merge_entity_schemas(self, original_entity_schema, new_entity_schema):
        merged_entity_schema = {}

        # merges the original entity schema with the new entity schema
        for attribute_name, new_attribute_schema in new_entity_schema.items():

            # copies the new attribute schema to the merged one in case it doesn't
            # exist in the orginal
            if not attribute_name in original_entity_schema:
                merged_entity_schema[attribute_name] = new_attribute_schema
            else:
                # otherwise merges the two attribute schemas
                merged_attribute_schema = {}
                original_attribute_schema = original_entity_schema[attribute_name]

                # retrieves each attribute schema's mandatory parameters
                original_attribute_schema_types = original_attribute_schema[TYPES_VALUE]
                new_attribute_schema_types = new_attribute_schema[TYPES_VALUE]

                # merges the allowed types
                merged_attribute_schema[TYPES_VALUE] = []
                merged_attribute_schema[TYPES_VALUE].extend(original_attribute_schema_types)
                merged_attribute_schema[TYPES_VALUE].extend(new_attribute_schema_types)
                merged_attribute_schema[TYPES_VALUE] = list(set(merged_attribute_schema[TYPES_VALUE]))

                # retrieves each attribute schema's non-mandatory parameters
                original_attribute_schema_list_type = original_attribute_schema.get(LIST_TYPE_VALUE, None)
                new_attribute_schema_list_type = new_attribute_schema.get(LIST_TYPE_VALUE, None)

                # copies the list type parameter in case it is not defined yet
                if new_attribute_schema_list_type and not original_attribute_schema_list_type:
                    merged_attribute_schema[LIST_TYPE_VALUE] = new_attribute_schema_list_type

        return merged_entity_schema

    def has_option(self, option_name):
        return option_name in self.option_name_value_map

    def get_option(self, option_name):
        # raises an exception in case the specified option
        # doesn't exist
        if not option_name in self.option_name_value_map:
            raise data_converter_exceptions.DataConverterConfigurationOptionNotFound(option_name)

        # retrieves the value of the specified option
        option_value = self.option_name_value_map[option_name]

        return option_value

    def set_option(self, option_name, option_value):
        # stores the specified option
        self.option_name_value_map[option_name] = option_value

    def set_options(self, option_name_value_map):
        # stores the provided options
        self.option_name_value_map = option_name_value_map

class OutputEntityMapping:

    data_converter_configuration = None
    """ The data converter configuration this output entity mapping belongs to """

    configuration_item_id = None
    """ Unique identifier for this configuration item in the data converter configuration """

    output_entity_name = None
    """ Name of the output entity """

    input_entity_name_input_entity_mapping_map = {}
    """ Dictionary relating the name of an input entity with its mappings """

    relation_mappings = []
    """ List of relation mappings defined for this output entity """

    enabled = True
    """ Boolean indicating if this configuration item is enabled """

    def __init__(self, data_converter_configuration, parent_configuration_item, configuration_item_id):
        self.data_converter_configuration = data_converter_configuration
        self.configuration_item_id = configuration_item_id
        self.output_entity_name = None
        self.input_entity_name_input_entity_mapping_map = {}
        self.relation_mappings = []
        self.enabled = True

    def __str__(self):
        return OUTPUT_ENTITY_MAPPING_DESCRIPTION_TEMPLATE % (self.output_entity_name)

    def get_configuration_item_id(self):
        return self.configuration_item_id

    def add_configuration(self, configuration):
        # retrieves the mandatory configuration attributes
        self.output_entity_name = configuration[OUTPUT_NAME_VALUE]

        # retrieves the non-mandatory configuration attributes
        input_entity_mappings = configuration.get(INPUT_ENTITIES_VALUE, [])
        relation_mappings = configuration.get(RELATIONS_VALUE, [])

        # adds the input entity mappings to the output entity mapping
        for input_entity_mapping in input_entity_mappings:
            input_entity_name = input_entity_mapping[INPUT_NAME_VALUE]

            # creates a new input entity mapping in case one was not defined before for input entities of the specified name
            if not input_entity_name in self.input_entity_name_input_entity_mapping_map:
                configuration_item = self.data_converter_configuration.create_configuration_item(self, INPUT_ENTITY_MAPPING_VALUE, input_entity_mapping)
                configuration_item_id = configuration_item.get_configuration_item_id()
                self.input_entity_name_input_entity_mapping_map[input_entity_name] = configuration_item
                self.data_converter_configuration.add_configuration_item_dependency(self.configuration_item_id, configuration_item_id)
            else:
                # otherwise adds the new configuration to the existing input entity mapping
                configuration_item = self.input_entity_name_input_entity_mapping_map[input_entity_name]
                configuration_item.add_configuration(input_entity_mapping)

        # adds the relation mappings to the output entity mapping
        for relation_mapping in relation_mappings:
            configuration_item = self.data_converter_configuration.create_configuration_item(self, RELATION_MAPPING_VALUE, relation_mapping)
            configuration_item_id = configuration_item.get_configuration_item_id()
            self.relation_mappings.append(configuration_item)
            self.data_converter_configuration.add_configuration_item_dependency(self.configuration_item_id, configuration_item_id)

    def is_enabled(self):
        return self.enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def get_output_entity_name(self):
        return self.output_entity_name

    def get_input_entity_mapping(self, input_entity_name):
        # raises an exception in case no input entity mapping is defined for input entities with the specified name
        if not input_entity_name in self.input_entity_name_input_entity_mapping_map:
            raise data_converter_exceptions.DataConverterConfigurationInputEntityNotDefined(str(input_entity_name))

        input_entity_mapping = self.input_entity_name_input_entity_mapping_map[input_entity_name]

        return input_entity_mapping

    def get_input_dependencies(self):
        # retrieves the input dependencies of this output entity mapping's input entity mappings
        input_entity_mapping_dependencies_maps = [input_entity_mapping.get_input_dependencies() for input_entity_mapping in self.input_entity_name_input_entity_mapping_map.values()]

        # retrieves the input dependencies of this output entity mapping's relation mappings
        relation_dependencies_maps = [relation_mapping.get_input_dependencies() for relation_mapping in self.relation_mappings]

        # merges the input dependencies of this output entity mapping
        dependencies_maps = []
        dependencies_maps.extend(input_entity_mapping_dependencies_maps)
        dependencies_maps.extend(relation_dependencies_maps)
        input_dependencies_map = merge_dependency_maps(dependencies_maps)

        return input_dependencies_map

    def get_enabled_input_dependencies(self):
        # retrieves the input dependencies of this output entity mapping's input entity mappings
        input_entity_mapping_dependencies_maps = [input_entity_mapping.get_input_dependencies() for input_entity_mapping in self.input_entity_name_input_entity_mapping_map.values() if input_entity_mapping.is_enabled()]

        # retrieves the input dependencies of this output entity mapping's relation mappings
        relation_dependencies_maps = [relation_mapping.get_input_dependencies() for relation_mapping in self.relation_mappings if relation_mapping.is_enabled()]

        # merges the input dependencies of this output entity mapping
        dependencies_maps = []
        dependencies_maps.extend(input_entity_mapping_dependencies_maps)
        dependencies_maps.extend(relation_dependencies_maps)
        input_dependencies_map = merge_dependency_maps(dependencies_maps)

        return input_dependencies_map

    def get_output_dependencies(self):
        # retrieves the output dependencies of this output entity mapping's input entity mappings
        input_entity_mapping_dependencies_maps = [input_entity_mapping.get_output_dependencies() for input_entity_mapping in self.input_entity_name_input_entity_mapping_map.values()]

        # retrieves the output dependencies of this output entity mapping's relation mappings
        relation_dependencies_maps = [relation_mapping.get_output_dependencies() for relation_mapping in self.relation_mappings]

        # merges the output dependencies of this output entity mapping
        dependencies_maps = []
        dependencies_maps.extend(input_entity_mapping_dependencies_maps)
        dependencies_maps.extend(relation_dependencies_maps)
        output_dependencies_map = merge_dependency_maps(dependencies_maps)

        return output_dependencies_map

    def get_enabled_output_dependencies(self):
        # retrieves the output dependencies of this output entity mapping's input entity mappings
        input_entity_mapping_dependencies_maps = [input_entity_mapping.get_output_dependencies() for input_entity_mapping in self.input_entity_name_input_entity_mapping_map.values() if input_entity_mapping.is_enabled()]

        # retrieves the output dependencies of this output entity mapping's relation mappings
        relation_dependencies_maps = [relation_mapping.get_output_dependencies() for relation_mapping in self.relation_mappings if relation_mapping.is_enabled()]

        # merges the output dependencies of this output entity mapping
        dependencies_maps = []
        dependencies_maps.extend(input_entity_mapping_dependencies_maps)
        dependencies_maps.extend(relation_dependencies_maps)
        output_dependencies_map = merge_dependency_maps(dependencies_maps)

        return output_dependencies_map

class InputEntityMapping:

    data_converter_configuration = None
    """ The data converter configuration this mapping belongs to """

    configuration_item_id = None
    """ Unique identifier for this configuration item in the data converter configuration """

    output_entity_mapping = None
    """ The output entity mapping this input entity mapping belongs to """

    input_entity_name = None
    """ Name of the input entity """

    input_output_entity_mappings = []
    """ List of input output entity mappings defined for this input entity mapping """

    enabled = True
    """ Boolean indicating if this configuration item is enabled """

    def __init__(self, data_converter_configuration, output_entity_mapping, configuration_item_id):
        self.data_converter_configuration = data_converter_configuration
        self.output_entity_mapping = output_entity_mapping
        self.configuration_item_id = configuration_item_id
        self.input_entity_name = None
        self.input_output_entity_mappings = []
        self.enabled = True

    def __str__(self):
        return INPUT_ENTITY_MAPPING_DESCRIPTION_TEMPLATE % (self.input_entity_name)

    def is_enabled(self):
        return self.enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def get_configuration_item_id(self):
        return self.configuration_item_id

    def add_configuration(self, configuration):
        # retrieves the mandatory configuration attributes
        input_entity_name = configuration[INPUT_NAME_VALUE]
        input_output_entity_mappings = configuration[ENTITY_MAPPING_VALUE]

        self.input_entity_name = input_entity_name

        # adds the input output entity mappings to this input entity mapping
        for input_output_entity_mapping in input_output_entity_mappings:
            configuration_item = self.data_converter_configuration.create_configuration_item(self, INPUT_OUTPUT_ENTITY_MAPPING_VALUE, input_output_entity_mapping)
            configuration_item_id = configuration_item.get_configuration_item_id()
            self.input_output_entity_mappings.append(configuration_item)
            self.data_converter_configuration.add_configuration_item_dependency(self.configuration_item_id, configuration_item_id)

    def get_input_entity_name(self):
        return self.input_entity_name

    def get_input_output_entity_mappings(self):
        return self.input_output_entity_mappings

    def get_input_dependencies(self):
        # retrieves the input dependencies of this input entity mapping's input output entity mappings
        input_output_entity_mapping_dependencies_maps = [input_output_entity_mapping.get_input_dependencies() for input_output_entity_mapping in self.input_output_entity_mappings]

        # merges the input dependencies of this input entity mapping
        input_dependencies_map = merge_dependency_maps(input_output_entity_mapping_dependencies_maps)

        return input_dependencies_map

    def get_enabled_input_dependencies(self):
        # retrieves the input dependencies of this input entity mapping's input output entity mappings
        input_output_entity_mapping_dependencies_maps = [input_output_entity_mapping.get_input_dependencies() for input_output_entity_mapping in self.input_output_entity_mappings if input_output_entity_mapping.is_enabled()]

        # merges the input dependencies of this input entity mapping
        input_dependencies_map = merge_dependency_maps(input_output_entity_mapping_dependencies_maps)

        return input_dependencies_map

    def get_output_dependencies(self):
        # retrieves the output dependencies of this input entity mapping's input output entity mappings
        input_output_entity_mapping_dependencies_maps = [input_output_entity_mapping.get_output_dependencies() for input_output_entity_mapping in self.input_output_entity_mappings]

        # merges the output dependencies of this input entity mapping
        output_dependencies_map = merge_dependency_maps(input_output_entity_mapping_dependencies_maps)

        return output_dependencies_map

    def get_enabled_output_dependencies(self):
        # retrieves the output dependencies of this input entity mapping's input output entity mappings
        input_output_entity_mapping_dependencies_maps = [input_output_entity_mapping.get_output_dependencies() for input_output_entity_mapping in self.input_output_entity_mappings if input_output_entity_mapping.is_enabled()]

        # merges the output dependencies of this input entity mapping
        output_dependencies_map = merge_dependency_maps(input_output_entity_mapping_dependencies_maps)

        return output_dependencies_map

class InputOutputEntityMapping:

    data_converter_configuration = None
    """ The data converter configuration this mapping belongs to """

    configuration_item_id = None
    """ Unique identifier for this configuration item in the data converter configuration """

    input_entity_mapping = None
    """ The input entity mapping this input-output entity mapping belongs to """

    validators = []
    """ The validators that must pass for the input entity to be converted to an output entity """

    handlers = []
    """ The handlers that will be executed after the input entity is converted to an output entity """

    output_attribute_name_enabled_map = {}
    """ Dictionary relating the name of an output attribute and a flag indicating if its currently enabled """

    output_attribute_name_output_attribute_mapping_map = {}
    """ Dictionary relating the name of an output attribute with its output attribute mapping """

    enabled = True
    """ Boolean indicating if this configuration item is enabled """

    def __init__(self, data_converter_configuration, input_entity_mapping, configuration_item_id):
        self.data_converter_configuration = data_converter_configuration
        self.input_entity_mapping = input_entity_mapping
        self.configuration_item_id = configuration_item_id
        self.validators = []
        self.handlers = []
        self.output_attribute_name_enabled_map = {}
        self.output_attribute_name_output_attribute_mapping_map = {}
        self.enabled = True

    def __str__(self):
        return ""

    def is_enabled(self):
        return self.enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def get_configuration_item_id(self):
        return self.configuration_item_id

    def add_configuration(self, configuration):
        # retrieves the mandatory configuration attributes
        output_attribute_mappings = configuration[ATTRIBUTE_MAPPING_VALUE]

        # retrieves the non-mandatory configuration attributes
        validators = configuration.get(VALIDATORS_VALUE, [])
        handlers = configuration.get(HANDLERS_VALUE, [])

        # adds the output attribute mappings to this input output entity mapping
        for output_attribute_mapping in output_attribute_mappings:
            output_attribute_name = output_attribute_mapping[OUTPUT_NAME_VALUE]

            # creates a new output attribute mapping in case one was not defined before for output attributes with the specified name
            if not output_attribute_name in self.output_attribute_name_output_attribute_mapping_map:
                configuration_item = self.data_converter_configuration.create_configuration_item(self, OUTPUT_ATTRIBUTE_MAPPING_VALUE, output_attribute_mapping)
                configuration_item_id = configuration_item.get_configuration_item_id()
                self.output_attribute_name_output_attribute_mapping_map[output_attribute_name] = configuration_item
                self.data_converter_configuration.add_configuration_item_dependency(self.configuration_item_id, configuration_item_id)
            else:
                # otherwise adds the configuration to the existing output attribute mapping
                configuration_item = self.output_attribute_name_output_attribute_mapping_map[output_attribute_name]
                configuration_item.add_configuration(output_attribute_mapping)

        # adds provided validators, handlers to the input output entity mapping
        self.validators.extend([Function(validator) for validator in validators])
        self.handlers.extend([Function(handler) for handler in handlers])

    def get_validators(self):
        return self.validators

    def get_handlers(self):
        return self.handlers

    def get_output_attribute_mapping(self, output_attribute_name):
        # raises an exception in case no attribute mapping is defined for output attributes with the specified name
        if not output_attribute_name in self.output_attribute_name_output_attribute_mapping:
            raise data_converter_exceptions.DataConverterConfigurationOutputAttributeNotDefined(str(output_attribute_name))

        # returns the output attribute mapping for output attributes with the specified name
        output_attribute_mapping = self.output_attribute_name_output_attribute_mapping[output_attribute_name]

        return output_attribute_mapping

    def get_input_dependencies(self):
        # retrieves the input dependencies of this input output entity mapping's output attribute mappings
        output_attribute_mapping_dependencies_maps = [output_attribute_mapping.get_input_dependencies() for output_attribute_mapping in self.output_attribute_name_output_attribute_mapping_map.values()]

        # retrieves the input dependencies of this input output entity mapping's handlers
        handler_dependencies_maps = [handler.get_input_dependencies() for handler in self.handlers]

        # retrieves the input dependencies of this input output entity mapping's validators
        validator_dependencies_maps = [validator.get_input_dependencies() for validator in self.validators]

        # retrieves the input dependencies for this input output entity mapping's output attribute mappings for their input attributes (these dependencies can only be extracted at this level)
        input_entity_name = self.input_entity_mapping.get_input_entity_name()
        output_attribute_mapping_input_attribute_names = [output_attribute_mapping.get_input_attribute_name() for output_attribute_mapping in self.output_attribute_name_output_attribute_mapping_map.values() if output_attribute_mapping.get_input_attribute_name()]
        output_attribute_mapping_dependencies_map = {}
        output_attribute_mapping_dependencies_map[input_entity_name] = output_attribute_mapping_input_attribute_names

        # merges the input dependencies of this input output entity mapping
        dependencies_maps = [output_attribute_mapping_dependencies_map]
        dependencies_maps.extend(output_attribute_mapping_dependencies_maps)
        dependencies_maps.extend(handler_dependencies_maps)
        dependencies_maps.extend(validator_dependencies_maps)
        input_dependencies_map = merge_dependency_maps(dependencies_maps)

        return input_dependencies_map

    def get_enabled_input_dependencies(self):
        # retrieves the input dependencies of this input output entity mapping's output attribute mappings
        output_attribute_mapping_dependencies_maps = [output_attribute_mapping.get_input_dependencies() for output_attribute_mapping in self.output_attribute_name_output_attribute_mapping_map.values() if output_attribute_mapping.is_enabled()]

        # retrieves the input dependencies of this input output entity mapping's handlers
        handler_dependencies_maps = [handler.get_input_dependencies() for handler in self.handlers]

        # retrieves the input dependencies of this input output entity mapping's validators
        validator_dependencies_maps = [validator.get_input_dependencies() for validator in self.validators]

        # retrieves the input dependencies for this input output entity mapping's output attribute mappings for their input attributes (these dependencies can only be extracted at this level)
        input_entity_name = self.input_entity_mapping.get_input_entity_name()
        output_attribute_mapping_input_attribute_names = [output_attribute_mapping.get_input_attribute_name() for output_attribute_mapping in self.output_attribute_name_output_attribute_mapping_map.values() if output_attribute_mapping.is_enabled() and output_attribute_mapping.get_input_attribute_name()]
        output_attribute_mapping_dependencies_map = {}
        output_attribute_mapping_dependencies_map[input_entity_name] = output_attribute_mapping_input_attribute_names

        # merges the input dependencies of this input output entity mapping
        dependencies_maps = [output_attribute_mapping_dependencies_map]
        dependencies_maps.extend(output_attribute_mapping_dependencies_maps)
        dependencies_maps.extend(handler_dependencies_maps)
        dependencies_maps.extend(validator_dependencies_maps)
        input_dependencies_map = merge_dependency_maps(dependencies_maps)

        return input_dependencies_map

    def get_output_dependencies(self):
        # retrieves the output dependencies of this input output entity mapping's output attribute mappings
        output_attribute_mapping_dependencies_maps = [output_attribute_mapping.get_output_dependencies() for output_attribute_mapping in self.output_attribute_name_output_attribute_mapping_map.values()]

        # retrieves the output dependencies of this input output entity mapping's handlers
        handler_dependencies_maps = [handler.get_output_dependencies() for handler in self.handlers]

        # retrieves the output dependencies of this input output entity mapping's validators
        validator_dependencies_maps = [validator.get_output_dependencies() for validator in self.validators]

        # merges the output dependencies of this input output entity mapping
        dependencies_maps = []
        dependencies_maps.extend(output_attribute_mapping_dependencies_maps)
        dependencies_maps.extend(handler_dependencies_maps)
        dependencies_maps.extend(validator_dependencies_maps)
        output_dependencies_map = merge_dependency_maps(dependencies_maps)

        return output_dependencies_map

    def get_enabled_output_dependencies(self):
        # retrieves the output dependencies of this input output entity mapping's output attribute mappings
        output_attribute_mapping_dependencies_maps = [output_attribute_mapping.get_output_dependencies() for output_attribute_mapping in self.output_attribute_name_output_attribute_mapping_map.values() if output_attribute_mapping.is_enabled()]

        # retrieves the output dependencies of this input output entity mapping's handlers
        handler_dependencies_maps = [handler.get_output_dependencies() for handler in self.handlers]

        # retrieves the output dependencies of this input output entity mapping's validators
        validator_dependencies_maps = [validator.get_output_dependencies() for validator in self.validators]

        # merges the output dependencies of this input output entity mapping
        dependencies_maps = []
        dependencies_maps.extend(output_attribute_mapping_dependencies_maps)
        dependencies_maps.extend(handler_dependencies_maps)
        dependencies_maps.extend(validator_dependencies_maps)
        output_dependencies_map = merge_dependency_maps(dependencies_maps)

        return output_dependencies_map

class OutputAttributeMapping:

    data_converter_configuration = None
    """ The data converter configuration this mapping belongs to """

    configuration_item_id = None
    """ Unique identifier for this configuration item in the data converter configuration """

    input_output_entity_mapping = None
    """ The input output entity mapping this output attribute mapping is related to """

    output_attribute_name = None
    """ Name of the output attribute """

    input_attribute_name = None
    """ Name of the input attribute that's going to be converted to the output attribute """

    default_value = None
    """ Default value to apply to the output attribute """

    validators = []
    """ Validators that must pass for the input attribute to be converted to an output attribute """

    handlers = []
    """ Handlers that will be executed after the input attribute is converted to an output attribute """

    enabled = True
    """ Boolean indicating if this configuration item is enabled """

    def __init__(self, data_converter_configuration, input_output_entity_mapping, configuration_item_id):
        self.data_converter_configuration = data_converter_configuration
        self.input_output_entity_mapping = input_output_entity_mapping
        self.configuration_item_id = configuration_item_id
        self.output_attribute_name = None
        self.input_attribute_name = None
        self.default_value = None
        self.validators = []
        self.handlers = []
        self.enabled = True

    def __str__(self):
        return OUTPUT_ATTRIBUTE_MAPPING_DESCRIPTION_TEMPLATE % (self.output_attribute_name)

    def is_enabled(self):
        return self.enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def get_configuration_item_id(self):
        return self.configuration_item_id

    def add_configuration(self, configuration):
        # retrieves the non-mandatory options
        name = configuration.get(OUTPUT_NAME_VALUE, None)
        validators = configuration.get(VALIDATORS_VALUE, [])
        attribute_name = configuration.get(INPUT_NAME_VALUE, None)
        handlers = configuration.get(HANDLERS_VALUE, [])
        default_value = configuration.get(INPUT_VALUE_VALUE, None)

        # raises an exception in case the output attribute name is being redefined
        if name and self.output_attribute_name:
            raise data_converter_exceptions.DataConverterConfigurationOutputAttributeNameAlreadyDefined(str(name))
        else:
            # otherwise sets the output attribute name
            self.output_attribute_name = name

        # raises an exception in case the input attribute name is being redefined
        if attribute_name and self.input_attribute_name:
            raise data_converter_exceptions.DataConverterConfigurationInputAttributeNameAlreadyDefined(str(attribute_name))
        else:
            # otherwise sets the input attribute name
            self.input_attribute_name = attribute_name

        # raises an exception in case the default value is being redefined
        if default_value and self.default_value:
            raise data_converter_exceptions.DataConverterConfigurationDefaultValueAlreadyDefined(str(default_value))
        else:
            # otherwise sets the default value
            self.default_value = default_value

        # adds the provided validators and handlers
        self.validators.extend([Function(validator) for validator in validators])
        self.handlers.extend([Function(handler) for handler in handlers])

    def get_output_attribute_name(self):
        return self.output_attribute_name

    def get_input_attribute_name(self):
        return self.input_attribute_name

    def get_default_value(self):
        return self.default_value

    def get_validators(self):
        return self.validators

    def get_handlers(self):
        return self.handlers

    def get_input_dependencies(self):
        # retrieves the input dependencies for this output attribute mapping's handlers
        handler_dependencies_maps = [handler.get_input_dependencies() for handler in self.handlers]

        # retrieves the input dependencies for this output attribute mapping's validators
        validator_dependencies_maps = [validator.get_input_dependencies() for validator in self.validators]

        # merges the input dependencies of this relation mapping
        dependencies_maps = []
        dependencies_maps.extend(handler_dependencies_maps)
        dependencies_maps.extend(validator_dependencies_maps)
        input_dependencies_map = merge_dependency_maps(dependencies_maps)

        return input_dependencies_map

    def get_output_dependencies(self):
        # retrieves the output dependencies for this output attribute mapping's handlers
        handler_dependencies_maps = [handler.get_output_dependencies() for handler in self.handlers]

        # retrieves the output dependencies for this output attribute mapping's validators
        validator_dependencies_maps = [validator.get_output_dependencies() for validator in self.validators]

        # merges the output dependencies of this relation mapping
        dependencies_maps = []
        dependencies_maps.extend(handler_dependencies_maps)
        dependencies_maps.extend(validator_dependencies_maps)
        output_dependencies_map = merge_dependency_maps(dependencies_maps)

        return output_dependencies_map

class RelationMapping:

    data_converter_configuration = None
    """ The data converter configuration this mapping belongs to """

    configuration_item_id = None
    """ Unique identifier for this configuration item in the data converter configuration """

    output_entity_mapping = None
    """ The output entity mapping this relation mapping belongs to """

    entity_relation_attribute_names = []
    """ Name of the entity's relation attributes where the related entities will be added to """

    related_entity_relation_attribute_names = []
    """ Name of the related entity's relation attribute where the source entity will be added to """

    connectors = []
    """ List of connector functions that define the indexes that point to the output entities to add to the relations """

    enabled = True
    """ Boolean indicating if this configuration item is enabled """

    def __init__(self, data_converter_configuration, output_entity_mapping, configuration_item_id):
        self.data_converter_configuration = data_converter_configuration
        self.output_entity_mapping = output_entity_mapping
        self.configuration_item_id = configuration_item_id
        self.entity_relation_attribute_names = []
        self.related_entity_relation_attribute_names = []
        self.connectors = []
        self.enabled = True

    def __str__(self):
        return RELATION_MAPPING_DESCRIPTION_TEMPLATE % (self.entity_relation_attribute_names, self.related_entity_relation_attribute_names)

    def is_enabled(self):
        return self.enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def get_configuration_item_id(self):
        return self.configuration_item_id

    def add_configuration(self, configuration):
        # retrieves the mandatory options
        entity_relation_attribute_names = configuration[ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE]
        related_entity_relation_attribute_names = configuration[RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE]
        connectors = configuration[CONNECTORS_VALUE]

        # adds the provided relation attribute names and connectors
        self.entity_relation_attribute_names.extend(entity_relation_attribute_names)
        self.related_entity_relation_attribute_names.extend(related_entity_relation_attribute_names)
        self.connectors.extend([Function(connector) for connector in connectors])

    def get_entity_relation_attribute_names(self):
        return self.entity_relation_attribute_names

    def get_related_entity_relation_attribute_names(self):
        return self.related_entity_relation_attribute_names

    def get_connectors(self):
        return self.connectors

    def get_input_dependencies(self):
        # retrieves the input dependencies of the relation mapping's connectors
        connector_input_dependency_maps = [connector.get_input_dependencies() for connector in self.connectors]

        # merges the input dependencies of this relation mapping
        input_dependencies_map = merge_dependency_maps(connector_input_dependency_maps)

        return input_dependencies_map

    def get_output_dependencies(self):
        # retrieves the output dependencies of the relation mapping's connectors
        connector_output_dependency_maps = [connector.get_output_dependencies() for connector in self.connectors]

        # merges the output dependencies of this relation mapping
        output_dependencies_map = merge_dependency_maps(connector_output_dependency_maps)

        return output_dependencies_map

class Function:

    function = None
    """ Name of function or function reference """

    arguments = {}
    """ Arguments to call the function with """

    input_dependencies_map = {}
    """ The input entities and respective attributes this function depends on """

    output_dependencies_map = {}
    """ The output entities and respective attributes this function depends on """

    def __init__(self, function):
        self.function = function[FUNCTION_VALUE]
        self.arguments = function.get(ARGUMENTS_VALUE, {})
        self.input_dependencies_map = function.get(INPUT_DEPENDENCIES_VALUE, {})
        self.output_dependencies_map = function.get(OUTPUT_DEPENDENCIES_VALUE, {})

    def __eq__(self, function):
        if not self.function == function.get_function():
            return False

        if not self.arguments == function.get_arguments():
            return False

        if not self.input_dependencies_map == function.get_input_dependencies():
            return False

        if not self.output_dependencies_map == function.get_output_dependencies():
            return False

        return True

    def is_function_name(self):
        return type(self.function) in types.StringTypes

    def is_function_reference(self):
        return not type(self.function) in types.StringTypes

    def get_function(self):
        return self.function

    def get_arguments(self):
        return self.arguments

    def get_input_dependencies(self):
        return self.input_dependencies_map

    def get_output_dependencies(self):
        return self.output_dependencies_map

def merge_dependency_maps(dependency_maps):
    merged_dependency_map = {}

    # adds all dependency maps to the same one
    for dependency_map in dependency_maps:

        # adds each dependency map's contents to the merged dependency map
        for entity_name, attribute_names in dependency_map.iteritems():

            # creates an entry for the entity dependency in case it doesn't exist
            if not entity_name in merged_dependency_map:
                merged_dependency_map[entity_name] = []

            # adds all attribute dependencies
            merged_dependency_map[entity_name].extend(attribute_names)

    # removes attribute dependency duplicates from the map
    for entity_name, attribute_names in merged_dependency_map.iteritems():
        merged_dependency_map[entity_name] = list(set(attribute_names))

    return merged_dependency_map
