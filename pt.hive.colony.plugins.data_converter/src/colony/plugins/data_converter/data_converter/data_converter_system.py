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

import time
import types

import data_converter_exceptions
import data_converter_configuration
import intermediate_structure
import generic_entity_validators
import generic_entity_handlers
import generic_attribute_validators
import generic_attribute_handlers
import generic_connectors
import generic_input_entity_indexers
import generic_output_entity_indexers
import generic_post_attribute_mapping_handlers
import generic_post_conversion_handlers

IO_ADAPTER_PLUGIN_ID_VALUE = "io_adapter_plugin_id"
""" The io adapter plugin id value """

LOAD_OPTIONS_VALUE = "load_options"
""" The load options value """

LOAD_ENTITIES_VALUE = "load_entities"
""" The load entities value """

OUTPUT_ENTITY_MAPPING_VALUE = "OutputEntityMapping"
""" The output entity mapping value """

RELATION_MAPPING_VALUE = "RelationMapping"
""" The relation mapping value """

INPUT_ENTITY_MAPPING_VALUE = "InputEntityMapping"
""" The input entity mapping value """

INPUT_OUTPUT_ENTITY_MAPPING_VALUE = "InputOutputEntityMapping"
""" The input output entity mapping value """

OUTPUT_ATTRIBUTE_MAPPING_VALUE = "OutputAttributeMapping"
""" The output attribute mapping value """

class DataConverter:
    """
    Converts data from one medium and schema to another.
    """

    data_converter_plugin = None
    """ Data converter plugin """

    last_loaded_configuration_id = 0
    """ Last identifier assigned to a loaded configuration """

    loaded_configuration_id_configuration_map = {}
    """ Dictionary relating the id assigned to a loaded configuration with the configuration itself """

    entity_validator_name_validator_map = {}
    """ Dictionary associating the name of an entity validator function with the function itself """

    entity_handler_name_handler_map = {}
    """ Dictionary associating the name of an entity handler with the handler itself """

    attribute_validator_name_validator_map = {}
    """ Dictionary associating the name of an attribute validator with the validator itself """

    attribute_handler_name_handler_map = {}
    """ Dictionary associating the name of an attribute handler with the handler itself """

    connector_name_connector_map = {}
    """ Dictionary associating the name of a connector with the connector itself """

    post_attribute_mapping_handler_name_handler_map = {}
    """ Dictionary associating the name of a post attribute mapping handler with the handler itself """

    post_conversion_handler_name_handler_map = {}
    """ Dictionary associating the name of a post conversion handler with the handler itself """

    input_indexer_name_input_indexer_map = {}
    """ Dictionary associating the name of an input indexer function with the function itself """

    output_indexer_name_output_indexer_map = {}
    """ Dictionary associating the name of an output indexer function with the function itself """

    io_adapter_plugin_id_plugin_map = {}
    """ Dictionary associating an io adapter's plugin id with the plugin itself """

    configuration_plugin_id_plugin_map = {}
    """ Dictionary associating a configuration's plugin id with the plugin that provides it """

    def __init__(self, data_converter_plugin):
        """
        Constructor of the class.

        @type data_converter_plugin: DataConverterPlugin
        @param data_converter_plugin: Data converter plugin.
        """

        self.data_converter_plugin = data_converter_plugin
        self.last_loaded_configuration_id = 0
        self.loaded_configuration_id_configuration_map = {}
        self.entity_validator_name_validator_map = {}
        self.entity_handler_name_handler_map = {}
        self.attribute_validator_name_validator_map = {}
        self.attribute_handler_name_handler_map = {}
        self.connector_name_connector_map = {}
        self.post_attribute_mapping_handler_name_handler_map = {}
        self.post_conversion_handler_name_handler_map = {}
        self.input_indexer_name_input_indexer_map = {}
        self.output_indexer_name_output_indexer_map = {}
        self.io_adapter_plugin_id_plugin_map = {}
        self.configuration_plugin_id_plugin_map = {}

    def load_data_converter(self):
        """
        Loads the data converter's resources.
        """

        # adds the generic entity validators to the list of entity validators
        entity_validator_names = [entity_validator_name for entity_validator_name in dir(generic_entity_validators) if type(getattr(generic_entity_validators, entity_validator_name)) == types.FunctionType]
        for entity_validator_name in entity_validator_names:
            entity_validator = getattr(generic_entity_validators, entity_validator_name)
            self.entity_validator_name_validator_map[entity_validator_name] = entity_validator

        # adds the generic entity handlers to the list of entity handlers
        entity_handler_names = [entity_handler_name for entity_handler_name in dir(generic_entity_handlers) if type(getattr(generic_entity_handlers, entity_handler_name)) == types.FunctionType]
        for entity_handler_name in entity_handler_names:
            entity_handler = getattr(generic_entity_handlers, entity_handler_name)
            self.entity_handler_name_handler_map[entity_handler_name] = entity_handler

        # adds the generic attribute handlers to the list of attribute handlers
        attribute_handler_names = [attribute_handler_name for attribute_handler_name in dir(generic_attribute_handlers) if type(getattr(generic_attribute_handlers, attribute_handler_name)) == types.FunctionType]
        for attribute_handler_name in attribute_handler_names:
            attribute_handler = getattr(generic_attribute_handlers, attribute_handler_name)
            self.attribute_handler_name_handler_map[attribute_handler_name] = attribute_handler

        # adds the generic attribute validators to the list of attribute validators
        attribute_validator_names = [attribute_validator_name for attribute_validator_name in dir(generic_attribute_validators) if type(getattr(generic_attribute_validators, attribute_validator_name)) == types.FunctionType]
        for attribute_validator_name in attribute_validator_names:
            attribute_validator = getattr(generic_attribute_validators, attribute_validator_name)
            self.attribute_validator_name_attribute_validator_map[attribute_validator_name] = attribute_validator

        # adds the generic connectors to the list of connectors
        connector_names = [connector_name for connector_name in dir(generic_connectors) if type(getattr(generic_connectors, connector_name)) == types.FunctionType]
        for connector_name in connector_names:
            connector = getattr(generic_connectors, connector_name)
            self.connector_name_connector_map[connector_name] = connector

        # adds the generic input indexers to the list of input indexers
        input_indexer_names = [input_indexer_name for input_indexer_name in dir(generic_input_entity_indexers) if type(getattr(generic_input_entity_indexers, input_indexer_name)) == types.FunctionType]
        for input_indexer_name in input_indexer_names:
            input_indexer = getattr(generic_input_entity_indexers, input_indexer_name)
            self.input_indexer_name_input_indexer_map[input_indexer_name] = input_indexer

        # adds the generic output indexers to the list of output indexers
        output_indexer_names = [output_indexer_name for output_indexer_name in dir(generic_output_entity_indexers) if type(getattr(generic_output_entity_indexers, output_indexer_name)) == types.FunctionType]
        for output_indexer_name in output_indexer_names:
            output_indexer = getattr(generic_output_entity_indexers, output_indexer_name)
            self.output_indexer_name_output_indexer_map[output_indexer_name] = output_indexer

        # adds the generic post attribute mapping handlers to the list of post attribute mapping handlers
        post_attribute_mapping_handler_names = [post_attribute_mapping_handler_name for post_attribute_mapping_handler_name in dir(generic_post_attribute_mapping_handlers) if type(getattr(generic_post_attribute_mapping_handlers, post_attribute_mapping_handler_name)) == types.FunctionType]
        for post_attribute_mapping_handler_name in post_attribute_mapping_handler_names:
            post_attribute_mapping_handler = getattr(generic_post_attribute_mapping_handlers, post_attribute_mapping_handler_name)
            self.post_attribute_mapping_handler_name_handler_map[post_attribute_mapping_handler_name] = post_attribute_mapping_handler

        # adds the generic post conversion handlers to the list of post conversion handlers
        post_conversion_handler_names = [post_conversion_handler_name for post_conversion_handler_name in dir(generic_post_conversion_handlers) if type(getattr(generic_post_conversion_handlers, post_conversion_handler_name)) == types.FunctionType]
        for post_conversion_handler_name in post_conversion_handler_names:
            post_conversion_handler = getattr(generic_post_conversion_handlers, post_conversion_handler_name)
            self.post_conversion_handler_name_handler_map[post_conversion_handler_name] = post_conversion_handler

    def get_next_loaded_configuration_id(self):
        # generates the next loaded configuration id
        self.last_loaded_configuration_id += 1

        return self.last_loaded_configuration_id

    def get_loaded_configuration_ids(self):
        """
        Retrieves the unique identifiers for the currently loaded configurations.

        @rtype: List
        @return: List with the unique identifiers for the loaded configurations.
        """

        # retrieves the unique identifiers for the currently loaded configurations
        loaded_configuration_ids = self.loaded_configuration_id_configuration_map.keys()

        return loaded_configuration_ids

    def get_loaded_configuration(self, configuration_id):
        """
        Retrieves the currently loaded data converter configuration.

        @type configuration_id: int
        @param configuration_id: Unique identifier for the data converter configuration
        one wants to retrieve.
        @rtype: DataConverterConfiguration
        @return: Data converter configuration one wants to retrieve.
        """

        # raises an exception in case the specified configuration is not found
        if not configuration_id in self.loaded_configuration_id_configuration_map:
            raise data_converter_exceptions.DataConverterConfigurationNotFound(str(configuration_id))

        # retrieves the loaded configuration with the specified id
        data_converter_configuration = self.loaded_configuration_id_configuration_map[configuration_id]

        return data_converter_configuration

    def load_configuration(self, configuration_plugin_id, option_name_value_map):
        """
        Unique identifier for the data converter configuration one wants to load.

        @type configuration_plugin_id: String
        @param configuration_plugin_id: Unique identifier for the
        data converter plugin one wants to load the configuration from.
        @type option_name_value_map: Dictionary
        @param option_name_value_map: Dictionary with the conversion options.

        @rtype: DataConverterConfiguration
        @return: The loaded data converter configuration.
        """

        # raises an exception in case the specified configuration plugin is not found
        if not configuration_plugin_id in self.configuration_plugin_id_plugin_map:
            raise data_converter_exceptions.DataConverterConfigurationPluginNotFound(str(configuration_plugin_id))

        # retrieves the configuration plugin and the configurations it provides
        configuration_plugin = self.configuration_plugin_id_plugin_map[configuration_plugin_id]
        intermediate_entity_schemas = configuration_plugin.get_intermediate_entity_schemas()
        input_io_adapters_options = configuration_plugin.get_input_io_adapters_options()
        attribute_mapping_output_entities = configuration_plugin.get_attribute_mapping_output_entities()
        relation_mapping_entities = configuration_plugin.get_relation_mapping_entities()
        input_entity_indexers = configuration_plugin.get_input_entity_indexers()
        output_entity_indexers = configuration_plugin.get_output_entity_indexers()
        post_attribute_mapping_handlers = configuration_plugin.get_post_attribute_mapping_handlers()
        post_conversion_handlers = configuration_plugin.get_post_conversion_handlers()
        output_io_adapters_options = configuration_plugin.get_output_io_adapters_options()

        # creates a new configuration with and adds the configurations provided by the plugin into it
        loaded_configuration_id = self.get_next_loaded_configuration_id()
        loaded_configuration = data_converter_configuration.DataConverterConfiguration(configuration_plugin_id, loaded_configuration_id)
        loaded_configuration.add_intermediate_entity_schemas(intermediate_entity_schemas)
        loaded_configuration.add_input_io_adapters_options(input_io_adapters_options)
        loaded_configuration.add_attribute_mapping_output_entities(attribute_mapping_output_entities)
        loaded_configuration.add_relation_mapping_entities(relation_mapping_entities)
        loaded_configuration.add_input_entity_indexers(input_entity_indexers)
        loaded_configuration.add_output_entity_indexers(output_entity_indexers)
        loaded_configuration.add_post_attribute_mapping_handlers(post_attribute_mapping_handlers)
        loaded_configuration.add_post_conversion_handlers(post_conversion_handlers)
        loaded_configuration.add_output_io_adapters_options(output_io_adapters_options)

        # configures the loaded configuration with the provided options
        loaded_configuration.set_options(option_name_value_map)

        # indexes the loaded configuration and its plugin by the generated id
        self.loaded_configuration_id_configuration_map[loaded_configuration_id] = loaded_configuration

        return loaded_configuration

    def unload_configuration(self, configuration_id):
        """
        Unique identifier for the data converter configuration one wants to unload.

        @type configuration_id: int
        @param configuration_id: Unique identifier for the data converter configuration
        one wants to unload.
        """

        # raises an exception in case the specified configuration is not found
        if not configuration_id in self.loaded_configuration_id_configuration_map:
            raise data_converter_exceptions.DataConverterConfigurationNotFound(str(configuration_id))

        # removes the references to the specified configuration
        del self.loaded_configuration_id_configuration_map[configuration_id]

    def set_configuration_option(self, configuration_id, option_name, option_value):
        # raises an exception in case the specified configuration is not found
        if not configuration_id in self.loaded_configuration_id_configuration_map:
            raise data_converter_exceptions.DataConverterConfigurationNotFound(str(configuration_id))

        # retrieves the specified configuration
        loaded_configuration = self.loaded_configuration_id_configuration_map[configuration_id]

        # sets the specified option in the configuration
        loaded_configuration.set_option(option_name, option_value)

    def create_intermediate_structure(self, configuration_map):
        """
        Creates an intermediate structure instance.

        @type configuration_map: Dictionary
        @param configuration_map: Map defining the intermediate structure's schema, or non
        in case one doesn't one to configure the intermediate structure.
        @rtype: IntermediateStructure
        @return: The created intermediate structure.
        """

        intermediate_structure_instance = intermediate_structure.IntermediateStructure()

        # configures the intermediate structure's schema in case one is provided
        if configuration_map:
            intermediate_structure_instance.configure_schema(configuration_map)

        return intermediate_structure_instance

    def load_intermediate_structure(self, configuration, intermediate_structure, io_adapter_plugin_id, options):
        """
        Populates the intermediate structure with data retrieved from the source
        specified in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type io_adapter_plugin_id: String
        @param io_adapter_plugin_id: Unique identifier for the input output adapter plugin
        one wants to use to load the intermediate structure.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the provided
        intermediate structure.
        @rtype: IntermediateStructure
        @return: The loaded intermediate structure.
        """

        self.data_converter_plugin.info("Loading intermediate structure with %s" % io_adapter_plugin_id)

        start_time = time.time()

        # retrieves the specified input output adapter plugin
        input_adapter_plugin = self.io_adapter_plugin_id_plugin_map.get(io_adapter_plugin_id, None)

        # raises an exception in case the specified io adapter plugin was not found
        if not input_adapter_plugin:
            raise data_converter_exceptions.DataConverterIoAdapterPluginNotFound(str(io_adapter_plugin_id))

        # redirects the load request to the specified input output adapter
        input_adapter_plugin.load_intermediate_structure(configuration, intermediate_structure, options)

        end_time = time.time()
        time_elapsed = end_time - start_time

        self.data_converter_plugin.info("Finished loading intermediate structure with %s in %ds" % (io_adapter_plugin_id, time_elapsed))

        return intermediate_structure

    def save_intermediate_structure(self, configuration, intermediate_structure, io_adapter_plugin_id, options):
        """
        Saves the intermediate structure to a file at the location and with characteristics
        defined in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type io_adapter_plugin_id: String
        @param io_adapter_plugin_id: Unique identifier for the input output adapter plugin
        one wants to use to save intermediate structure.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure.
        """

        self.data_converter_plugin.info("Saving intermediate structure with %s" % io_adapter_plugin_id)

        start_time = time.time()

        # retrieves the specified input output adapter plugin
        output_adapter_plugin = self.io_adapter_plugin_id_plugin_map.get(io_adapter_plugin_id, None)

        # raises an exception in case the specified io adapter plugin was not found
        if not output_adapter_plugin:
            raise data_converter_exceptions.DataConverterIoAdapterPluginNotFound(str(io_adapter_plugin_id))

        # redirects the save request to the specified input output adapter
        output_adapter_plugin.save_intermediate_structure(configuration, intermediate_structure, options)

        end_time = time.time()
        time_elapsed = end_time - start_time

        self.data_converter_plugin.info("Finished saving intermediate structure with %s in %ds" % (io_adapter_plugin_id, time_elapsed))

        return intermediate_structure

    def convert_data(self, configuration_id):
        """
        Converts data from one intermediate structure to another transforming
        its schema along the way.

        @type configuration_id: int
        @param configuration_id: Unique identifier for the data converter configuration
        one wants to retrieve.
        @rtype: IntermediateStructure
        @return: Output intermediate structure.
        """

        # raises an exception in case the specified configuration is not found
        if not configuration_id in self.loaded_configuration_id_configuration_map:
            raise data_converter_exceptions.DataConverterConfigurationNotFound(str(configuration_id))

        self.data_converter_plugin.info("Data conversion started")

        start_time = time.time()

        # retrieves the specified loaded configuration
        loaded_configuration = self.loaded_configuration_id_configuration_map[configuration_id]

        # extracts the mandatory options
        intermediate_structure_schema = loaded_configuration.get_intermediate_structure_schema()
        input_io_adapters_options = loaded_configuration.get_input_io_adapters_options()
        output_io_adapters_options = loaded_configuration.get_output_io_adapters_options()

        # creates an input intermediate structure
        input_intermediate_structure = self.create_intermediate_structure(None)

        # loads the intermediate structure with the specified io adapters
        for input_io_adapter_options in input_io_adapters_options:
            input_io_adapter_plugin_id = input_io_adapter_options[IO_ADAPTER_PLUGIN_ID_VALUE]

            # infers the entities that must be loaded by the input adapter from the configuration
            input_io_adapter_options[LOAD_OPTIONS_VALUE] = {}
            input_io_adapter_options[LOAD_OPTIONS_VALUE][LOAD_ENTITIES_VALUE] = loaded_configuration.get_enabled_input_dependencies()

            # loads the data to the input intermediate structure with the current io adapter
            self.data_converter_plugin.load_intermediate_structure(loaded_configuration, input_intermediate_structure, input_io_adapter_plugin_id, input_io_adapter_options)

        # runs the input indexers on the loaded input intermediate structure
        self.index_input_intermediate_structure(loaded_configuration, input_intermediate_structure)

        # creates an output intermediate structure
        output_intermediate_structure = self.create_intermediate_structure(intermediate_structure_schema)

        # migrates the input intermediate structure's entity attributes to the output intermediate structure
        self.convert_entities(loaded_configuration, input_intermediate_structure, output_intermediate_structure)

        # executes the post attribute mapping handlers to finish any work that was not supported by the data converter itself
        self.execute_post_attribute_mapping_handlers(loaded_configuration, input_intermediate_structure, output_intermediate_structure)

        # migrates the output intermediate structure's entity relations to the output intermediate structure
        self.convert_relations(loaded_configuration, input_intermediate_structure, output_intermediate_structure)

        # executes the post conversion handlers to finish any work that was not supported by the data converter itself
        self.execute_post_conversion_handlers(loaded_configuration, input_intermediate_structure, output_intermediate_structure)

        # saves the output intermediate structure with the the specified output io adapters
        for output_io_adapter_options in output_io_adapters_options:
            output_io_adapter_plugin_id = output_io_adapter_options[IO_ADAPTER_PLUGIN_ID_VALUE]

            # saves data from the output intermediates structure with the current io adapter
            self.data_converter_plugin.save_intermediate_structure(loaded_configuration, output_intermediate_structure, output_io_adapter_plugin_id, output_io_adapter_options)

        end_time = time.time()
        time_elapsed = end_time - start_time

        self.data_converter_plugin.info("Data conversion completed in %ds" % time_elapsed)

        return output_intermediate_structure

    def index_input_intermediate_structure(self, configuration, input_intermediate_structure):
        # retrieves the input indexers that apply to all entities
        global_input_entity_indexers = configuration.get_global_input_entity_indexers()

        # indexes all input entities that have associated input indexers
        input_entity_names = input_intermediate_structure.get_entity_names()
        for input_entity_name in input_entity_names:

            # retrieves all input indexers that apply to entities with this name
            input_entity_indexers = configuration.get_input_entity_indexers(input_entity_name)
            all_input_entity_indexers = []
            all_input_entity_indexers.extend(global_input_entity_indexers)
            all_input_entity_indexers.extend(input_entity_indexers)

            # runs the input indexers on the input entities
            for input_indexer in all_input_entity_indexers:
                input_indexer_function = input_indexer.get_function()
                input_indexer_arguments = input_indexer.get_arguments()

                # fetches the input indexer from the generic input indexers in case a string was provided
                if input_indexer.is_function_name():
                    input_indexer_function = self.input_indexer_name_input_indexer_map[input_indexer_function]

                # runs the input indexers on each input entity
                input_entities = input_intermediate_structure.get_entities_by_name(input_entity_name)
                for input_entity in input_entities:

                    # runs the input indexer on the input entity
                    input_indexer_function(self, configuration, input_intermediate_structure, input_entity, input_indexer_arguments)

    def convert_entities(self, configuration, input_intermediate_structure, output_intermediate_structure):
        """
        Converts the entities in the input intermediate structure and their respective attributes
        into entities in the output intermediate structure.

        @type input_intermediate_structure: IntermediateStructure
        @param input_intermediate_structure: The intermediate structure where entities are going to
        be converted from.
        @type output_intermediate_structure: IntermediateStructure
        @param output_intermediate_structure: The intermediate structure where entities are going
        to be converted to.
        """

        self.data_converter_plugin.info("Data conversion entity conversion started")

        start_time = time.time()

        # converts the entities that are currently enabled in the configuration
        output_entity_mapping_configuration_item_ids = configuration.get_enabled_configuration_item_ids_by_type(OUTPUT_ENTITY_MAPPING_VALUE)
        for output_entity_mapping_configuration_item_id in output_entity_mapping_configuration_item_ids:
            output_entity_mapping = configuration.get_configuration_item(output_entity_mapping_configuration_item_id)

            # extracts the output entities from the enabled input entity sources
            input_entity_mapping_configuration_item_ids = configuration.get_enabled_dependent_configuration_item_ids_by_type(output_entity_mapping_configuration_item_id, INPUT_ENTITY_MAPPING_VALUE)
            for input_entity_mapping_configuration_item_id in input_entity_mapping_configuration_item_ids:
                input_entity_mapping = configuration.get_configuration_item(input_entity_mapping_configuration_item_id)

                # extracts output entities from the current input entity source in the way specified by the input output entity mapping
                input_output_entity_mapping_configuration_item_ids = configuration.get_enabled_dependent_configuration_item_ids_by_type(input_entity_mapping_configuration_item_id, INPUT_OUTPUT_ENTITY_MAPPING_VALUE)
                for input_output_entity_mapping_configuration_item_id in input_output_entity_mapping_configuration_item_ids:
                    input_output_entity_mapping = configuration.get_configuration_item(input_output_entity_mapping_configuration_item_id)
                    self.convert_entities_input_output_entity(configuration, input_intermediate_structure, output_intermediate_structure, output_entity_mapping, input_entity_mapping, input_output_entity_mapping)

        end_time = time.time()
        time_elapsed = end_time - start_time

        self.data_converter_plugin.info("Data conversion entity conversion completed in %ds" % time_elapsed)

    def convert_entities_input_output_entity(self, configuration, input_intermediate_structure, output_intermediate_structure, output_entity_mapping, input_entity_mapping, input_output_entity_mapping):
        # retrieves the mapping attributes
        output_entity_name = output_entity_mapping.get_output_entity_name()
        input_entity_name = input_entity_mapping.get_input_entity_name()
        validators = input_output_entity_mapping.get_validators()
        handlers = input_output_entity_mapping.get_handlers()

        # converts each input entity to an output entity
        input_entities = input_intermediate_structure.get_entities_by_name(input_entity_name)
        for input_entity in input_entities:

            # skips to the next input entity in case one of the specified validators fails
            valid = self.is_input_entity_valid(configuration, input_intermediate_structure, input_entity, validators)
            if not valid:
                continue

            # creates an entity in the output intermediate structure to convert the input entity into
            output_entity = output_intermediate_structure.create_entity(output_entity_name)

            # converts the input entity attributes to the output entity
            input_output_entity_mapping_configuration_item_id = input_output_entity_mapping.get_configuration_item_id()
            output_attribute_mapping_configuration_item_ids = configuration.get_enabled_dependent_configuration_item_ids_by_type(input_output_entity_mapping_configuration_item_id, OUTPUT_ATTRIBUTE_MAPPING_VALUE)
            for output_attribute_mapping_configuration_item_id in output_attribute_mapping_configuration_item_ids:
                output_attribute_mapping = configuration.get_configuration_item(output_attribute_mapping_configuration_item_id)
                self.convert_entities_output_attribute(configuration, input_intermediate_structure, output_intermediate_structure, output_attribute_mapping, input_entity_mapping, input_output_entity_mapping, output_attribute_mapping, input_entity, output_entity)

            # pipes the output entity through the configured handlers
            for handler in handlers:
                handler_function = handler.get_function()
                handler_arguments = handler.get_arguments()

                # retrieves the handler in case a string with its name was provided
                if handler.is_function_name():
                    handler_function = self.entity_handler_name_handler_map[handler_function]

                # runs the entity handler on the output entity
                output_entity = handler_function(self, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, handler_arguments)

            # runs the output indexers associated with the output entity
            self.index_output_entity(configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity)

    def index_output_entity(self, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity):
        # retrieves the output indexers that apply to all entities
        global_output_entity_indexers = configuration.get_global_output_entity_indexers()

        # indexes all output entities that have associated output indexers
        output_entity_name = output_entity.get_name()

        # retrieves all output indexers that apply to entities with this name
        output_entity_indexers = configuration.get_output_entity_indexers(output_entity_name)
        all_output_entity_indexers = []
        all_output_entity_indexers.extend(global_output_entity_indexers)
        all_output_entity_indexers.extend(output_entity_indexers)

        # runs the output indexers on the input entities
        for output_indexer in all_output_entity_indexers:
            output_indexer_function = output_indexer.get_function()
            output_indexer_arguments = output_indexer.get_arguments()

            # fetches the output indexer from the generic output indexers in case a string was provided
            if output_indexer.is_function_name():
                output_indexer_function = self.output_indexer_name_output_indexer_map[output_indexer_function]

            # runs the output indexer on the input entity
            output_indexer_function(self, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_indexer_arguments)

    # @todo: comment this
    def convert_entities_output_attribute(self, configuration, input_intermediate_structure, output_intermediate_structure, output_entity_mapping, input_entity_mapping, input_output_entity_mapping, output_attribute_mapping, input_entity, output_entity):
        # retrieves the output attribute mapping's attributes
        output_attribute_name = output_attribute_mapping.get_output_attribute_name()
        input_attribute_name =  output_attribute_mapping.get_input_attribute_name()
        default_value = output_attribute_mapping.get_default_value()
        validators = output_attribute_mapping.get_validators()
        handlers = output_attribute_mapping.get_handlers()

        # raises an exception in case neither an attribute value source nor a default value were provided
        if not input_attribute_name and not handlers and default_value == None:
            raise data_converter_exceptions.DataConverterMandatoryOptionNotFound("input attribute name or default value or handlers")

        # retrieves the input entity's attribute value in case an input attribute was specified
        input_attribute_value = None
        if input_attribute_name:
            input_attribute_value = input_entity.get_attribute(input_attribute_name)

        # replaces the input attribute value with the default value in case it is none
        if input_attribute_value == None and not default_value == None:
            input_attribute_value = default_value

        # returns in case one of the specified validators fails
        valid = self.is_input_attribute_value_valid(configuration, input_intermediate_structure, input_entity, input_attribute_value, validators)
        if not valid:
            return

        # converts the input entity attributes into output entity attributes in case
        # all validators passed
        output_attribute_value = input_attribute_value

        # pipes the input attribute value throughout the configured handlers
        for handler in handlers:
            handler_function = handler.get_function()
            handler_arguments = handler.get_arguments()

            # retrieves the handler in case a string with its name was provided
            if handler.is_function_name():
                handler_function = self.attribute_handler_name_handler_map[handler_function]

            # replaces the output attribute value with the attribute handler's result
            output_attribute_value = handler_function(self, configuration, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, handler_arguments)

        # sets the post-processed input attribute value in the output entity
        output_entity.set_attribute(output_attribute_name, output_attribute_value)

    # @todo: comment this
    def convert_relations(self, configuration, input_intermediate_structure, output_intermediate_structure):
        self.data_converter_plugin.info("Data conversion relation conversion started")

        start_time = time.time()

        # creates relations for every created output entity
        output_entity_mapping_configuration_item_ids = configuration.get_enabled_configuration_item_ids_by_type(OUTPUT_ENTITY_MAPPING_VALUE)
        for output_entity_mapping_configuration_item_id in output_entity_mapping_configuration_item_ids:
            output_entity_mapping = configuration.get_configuration_item(output_entity_mapping_configuration_item_id)

            # creates relations for the every output entity created with the current output entity mapping
            relation_mapping_configuration_item_ids = configuration.get_enabled_dependent_configuration_item_ids_by_type(output_entity_mapping_configuration_item_id, RELATION_MAPPING_VALUE)
            for relation_mapping_configuration_item_id in relation_mapping_configuration_item_ids:
                relation_mapping = configuration.get_configuration_item(relation_mapping_configuration_item_id)
                self.convert_relations_relation_mapping(configuration, input_intermediate_structure, output_intermediate_structure, output_entity_mapping, relation_mapping)

        end_time = time.time()
        time_elapsed = end_time - start_time

        self.data_converter_plugin.info("Data conversion relation conversion completed in %ds" % time_elapsed)

    def convert_relations_relation_mapping(self, configuration, input_intermediate_structure, output_intermediate_structure, output_entity_mapping, relation_mapping):
        output_entity_name = output_entity_mapping.get_output_entity_name()
        connectors = relation_mapping.get_connectors()
        entity_relation_attribute_names = relation_mapping.get_entity_relation_attribute_names()
        related_entity_relation_attribute_names = relation_mapping.get_related_entity_relation_attribute_names()

        # executes the connectors specified in the relation mapping
        output_entities = output_intermediate_structure.get_entities_by_name(output_entity_name)
        for output_entity in output_entities:

            # executes the specified connectors
            for connector in connectors:
                connector_function = connector.get_function()
                connector_arguments = connector.get_arguments()

                # retrieves the related entity indexes handler in case its name was provided
                if connector.is_function_name():
                    connector_function = self.connector_name_connector_map[connector_function]

                # retrieves the entities specified by each index and associates them with the output entity
                related_entities = connector_function(self, configuration, input_intermediate_structure, output_intermediate_structure, output_entity, connector_arguments)
                for related_entity in related_entities:

                    # adds the related entity to every specified relation attribute in the entity
                    for entity_relation_attribute_name in entity_relation_attribute_names:
                        self.connect_entities(output_entity, entity_relation_attribute_name, related_entity)

                    # adds the entity to every specified relation attribute in the related entity
                    for related_entity_relation_attribute_name in related_entity_relation_attribute_names:
                        self.connect_entities(related_entity, related_entity_relation_attribute_name, output_entity)

    def connect_entities(self, entity, entity_relation_attribute_name, related_entity):
        """
        Connects an entity to another.

        @type entity: Entity
        @param entity: Entity where one wants to add a related entity to its relation attribute.
        @type entity_relation_attribute_name: String
        @param entity_relation_attribute_name: Name of the entity's relation attribute.
        @type related_entity: Entity
        @param related_entity: Entity one wants to add to the relation attribute.
        """

        # retrieves the entity's relation attribute value
        entity_relation_attribute_value = entity.get_attribute(entity_relation_attribute_name)

        # adds the related entity to the relation attribute value in case it is a "to many" relation
        if type(entity_relation_attribute_value) == types.ListType:
            entity_relation_attribute_value.append(related_entity)
        elif entity_relation_attribute_value:
            entity_relation_attribute_value = [entity_relation_attribute_value]
            entity_relation_attribute_value.append(related_entity)
        else:
            # sets the related entity directly in case it is a "to one" relation
            entity_relation_attribute_value = related_entity

        # updates the entity's relation attribute
        entity.set_attribute(entity_relation_attribute_name, entity_relation_attribute_value)

    def disconnect_entities(self, entity, entity_relation_attribute_name, related_entity):
        """
        Disconnects an entity from another.

        @type entity: Entity
        @param entity: Entity where one wants to remove a related entity from its relation attribute.
        @type entity_relation_attribute_name: String
        @param entity_relation_attribute_name: Name of the entity's relation attribute.
        @type related_entity: Entity
        @param related_entity: Entity one wants to remove from the relation attribute.
        """

        # retrieves the entity's relation attribute value
        entity_relation_attribute_value = entity.get_attribute(entity_relation_attribute_name)

        # removes the related entity to the relation attribute value in case it is a "to many" relation
        if type(entity_relation_attribute_value) == types.ListType:
            # removes the related entity
            entity_relation_attribute_value.remove(related_entity)

            # updates the entity's relation attribute
            entity.set_attribute(entity_relation_attribute_name, entity_relation_attribute_value)
        elif entity_relation_attribute_value == related_entity:
            # sets the relation attribute as none
            entity.set_attribute(entity_relation_attribute_name, None)
        else:
            # otherwise raises an exception
            raise data_converter_exceptions.DataConverterEntityNotFound("related entity not found")

    def execute_post_attribute_mapping_handlers(self, configuration, input_intermediate_structure, output_intermediate_structure):
        self.data_converter_plugin.info("Data conversion attribute mapping post-processing started")

        start_time = time.time()

        # executes the post attribute mapping handlers
        post_attribute_mapping_handlers = configuration.get_post_attribute_mapping_handlers()
        for post_attribute_mapping_handler in post_attribute_mapping_handlers:
            post_attribute_mapping_handler_function = post_attribute_mapping_handler.get_function()
            post_attribute_mapping_handler_function_arguments = post_attribute_mapping_handler.get_arguments()

            # retrieves the post attribute mapping handler in case a string with its name was provided
            if post_attribute_mapping_handler.is_function_name():
                post_attribute_mapping_handler_function = self.post_attribute_mapping_handler_name_handler_map[post_attribute_mapping_handler_function]

            # executes the post attribute mapping handler
            output_intermediate_structure = post_attribute_mapping_handler_function(self, configuration, input_intermediate_structure, output_intermediate_structure, post_attribute_mapping_handler_function_arguments)

        end_time = time.time()
        time_elapsed = end_time - start_time

        self.data_converter_plugin.info("Data attribute mapping post-processing ended in %ds" % time_elapsed)

    def execute_post_conversion_handlers(self, configuration, input_intermediate_structure, output_intermediate_structure):
        self.data_converter_plugin.info("Data conversion post-processing started")

        start_time = time.time()

        # executes the post conversion handlers
        post_conversion_handlers = configuration.get_post_conversion_handlers()
        for post_conversion_handler in post_conversion_handlers:
            post_conversion_handler_function = post_conversion_handler.get_function()
            post_conversion_handler_function_arguments = post_conversion_handler.get_arguments()

            # retrieves the post conversion handler in case a string with its name was provided
            if post_conversion_handler.is_function_name():
                post_conversion_handler_function = self.post_conversion_handler_name_handler_map[post_conversion_handler_function]

            # executes the post conversion handler
            output_intermediate_structure = post_conversion_handler_function(self, configuration, input_intermediate_structure, output_intermediate_structure, post_conversion_handler_function_arguments)

        end_time = time.time()
        time_elapsed = end_time - start_time

        self.data_converter_plugin.info("Data conversion post-processing ended in %ds" % time_elapsed)

    def is_input_entity_valid(self, configuration, input_intermediate_structure, input_entity, validators):
        # tests if all validators return true
        for validator in validators:
            validator_function = validator.get_function()
            validator_arguments = validator.get_arguments()

            # retrieves the validator in case a string with its name was provided
            if validator.is_function_name():
                validator_function = self.entity_validator_name_validator_map[validator_function]

            # returns false in case one of the validators fails
            valid = validator_function(self, configuration, input_intermediate_structure, input_entity, validator_arguments)
            if not valid:
                return False

        return True

    def is_input_attribute_value_valid(self, configuration, input_intermediate_structure, input_entity, input_attribute_value, validators):
        # tests the if all validators return true
        for validator in validators:
            validator_function = validator.get_function()
            validator_arguments = validator.get_arguments()

            # retrieves the validator in case a string with its name was provided
            if validator.is_function_name():
                validator_function = self.attribute_validator_name_validator_map[validator_function]

            # returns false in case one of the validators fails
            valid = validator_function(self, configuration, input_intermediate_structure, input_entity, input_attribute_value, validator_arguments)
            if not valid:
                return False

        return True

    def add_io_adapter_plugin(self, io_adapter_plugin):
        """
        Adds an input output adapter to load and save the intermediate structure with.

        @type io_adapter_plugin: Plugin
        @param io_adapter_plugin: Input output adapter plugin one wants to add.
        """

        self.io_adapter_plugin_id_plugin_map[io_adapter_plugin.id] = io_adapter_plugin

    def remove_io_adapter_plugin(self, io_adapter_plugin):
        """
        Removes an input output adapter.

        @type io_adapter_plugin: Plugin
        @param io_adapter_plugin: Input output adapter plugin one wants to remove.
        """

        del self.io_adapter_plugin_id_plugin_map[io_adapter_plugin.id]

    def add_configuration_plugin(self, configuration_plugin):
        """
        Adds a data converter configuration plugin.

        @type configuration_plugin: Plugin
        @param configuration_plugin: Data converter configuration plugin one wants to add.
        """

        self.configuration_plugin_id_plugin_map[configuration_plugin.id] = configuration_plugin

    def remove_configuration_plugin(self, configuration_plugin):
        """
        Removes a data converter configuration plugin.

        @type data_converter_configuration_plugin: Plugin
        @param data_converter_configuration_plugin: Data converter configuration plugin one wants to remove.
        """

        del self.configuration_plugin_id_plugin_map[configuration_plugin.id]
