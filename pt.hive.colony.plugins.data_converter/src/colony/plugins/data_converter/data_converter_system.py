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

import data_converter_exceptions

class DataConverter:
    """
    Converts data from one medium and schema to another.
    """

    data_converter_plugin = None
    """ Data converter plugin """

    index_entity_map = None
    """ Dictionary associating an index with an entity """

    def __init__(self, data_converter_plugin):
        """
        Class constructor.

        @type data_converter_plugin: DataConverterPlugin
        @param data_converter_plugin: Data converter plugin.
        """

        self.data_converter_plugin = data_converter_plugin
        self.index_entity_map = {}

    def convert_data(self, input_options, output_options, conversion_options):
        """
        Converts data from one intermediate structure to another transforming its schema along the way.

        @type input_options: Dictionary
        @param input_options: Options used to determine how the input intermediate structure should retrieve its data.
        @type output_options: Dictionary
        @param output_options: Options used to determine how the output intermediate structure should save its data.
        @type conversion_options: Dictionary
        @param conversion_options: Options used to determine how to perform the conversion process.
        """

        self.data_converter_plugin.logger.info("[%s] Data conversion process started" % self.data_converter_plugin.id)

        # clears the index used in the last conversion
        self.index_entity_map = {}

        # raises an exception in case one of the mandatory options is not provided
        mandatory_input_output_options = ["io_adapter_plugin_id"]
        for mandatory_input_output_option in mandatory_input_output_options:
            if not mandatory_input_output_option in input_options or not mandatory_input_output_option in output_options:
                raise data_converter_exceptions.DataConverterOptionMissing("DataConverter.convert_data - Mandatory option not supplied (option_name = %s)" % mandatory_input_output_option)

        # extracts the mandatory options
        input_adapter_plugin_id = input_options["io_adapter_plugin_id"]
        output_adapter_plugin_id = output_options["io_adapter_plugin_id"]

        # creates the input and output intermediate structures
        input_intermediate_structure = self.data_converter_plugin.intermediate_structure_plugin.create_intermediate_structure()
        output_intermediate_structure = self.data_converter_plugin.intermediate_structure_plugin.create_intermediate_structure()

        # loads the source data into the input intermediate structure
        self.data_converter_plugin.intermediate_structure_plugin.load(input_intermediate_structure, input_adapter_plugin_id, input_options)

        # migrate the input intermediate structure's entity attributes to the output intermediate structure
        self.convert_attributes(input_intermediate_structure, output_intermediate_structure, conversion_options)

        # migrate the output intermediate structure's entity relations to the output intermediate structure
        self.convert_relations(input_intermediate_structure, output_intermediate_structure, conversion_options)

        # saves the output intermediate structure with the results of the conversion
        self.data_converter_plugin.intermediate_structure_plugin.save(output_intermediate_structure, output_adapter_plugin_id, output_options)

        self.data_converter_plugin.logger.info("[%s] Data conversion process ended" % self.data_converter_plugin.id)

    def convert_attributes(self, input_intermediate_structure, output_intermediate_structure, options):
        """
        Converts the entities in the input intermediate structure and their respective attributes into entities in the output intermediate structure.

        @type input_intermediate_structure: IntermediateStructure
        @param input_intermediate_structure: The intermediate structure where entities are going to be converted from.
        @type output_intermediate_structure: IntermediateStructure
        @param output_intermediate_structure: The intermediate structure where entities are going to be converted to.
        @type options: Dictionary
        @param options: Map with the options that specify how the conversion should be performed.
        """

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["attribute_mapping"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise data_converter_exceptions.DataConverterOptionMissing("DataConverter.convert_attributes - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        attribute_mapping = options["attribute_mapping"]

        # converts each input intermediate entity with the name specified in the mapping
        intermediate_entities_mapping = attribute_mapping["intermediate_entities"]
        for intermediate_entity_mapping in intermediate_entities_mapping:
            self.convert_attributes_intermediate_entity_mapping(input_intermediate_structure, output_intermediate_structure, options, intermediate_entity_mapping)

    def convert_attributes_intermediate_entity_mapping(self, input_intermediate_structure, output_intermediate_structure, options, intermediate_entity_mapping):
        intermediate_entity_name = intermediate_entity_mapping["name"]

        # converts each input intermediate entity into a number of output intermediate entities
        remote_entities_mapping = intermediate_entity_mapping["remote_entities"]
        for remote_entity_mapping in remote_entities_mapping:
            self.convert_attributes_intermediate_entity_remote_entity_mapping(input_intermediate_structure, output_intermediate_structure, options, remote_entity_mapping, intermediate_entity_name)

    def convert_attributes_intermediate_entity_remote_entity_mapping(self, input_intermediate_structure, output_intermediate_structure, options, remote_entity_mapping, intermediate_entity_name):
        remote_entity_name = remote_entity_mapping["name"]

        # retrieves all input intermediate entities with the name specified in the mapping and converts them
        input_entities = input_intermediate_structure.get_entities(intermediate_entity_name)
        for input_entity in input_entities:

            # runs the validators to confirm if this mapping should be executed for this instance
            valid = True
            if "validators" in remote_entity_mapping:
                validators = remote_entity_mapping["validators"]
                for validator in validators:
                    valid = validator(input_entity)
                    if not valid:
                        break

            # converts the input intermediate entity into output entities in case all validators passed
            if valid:

                # creates an entity in the output intermediate structure to convert the input entity into
                output_entity = output_intermediate_structure.create_entity(remote_entity_name)

                # converts the input entities' attributes into a number of output intermediate entity attributes
                remote_attributes_mapping = remote_entity_mapping["remote_attributes"]
                for remote_attribute_mapping in remote_attributes_mapping:
                    self.convert_attributes_intermediate_entity_remote_entity_attribute_mapping(input_intermediate_structure, output_intermediate_structure, options, remote_attribute_mapping, input_entity, output_entity)

                # pipes the output entity through the configured handlers, if any
                if "handlers" in remote_entity_mapping:
                    handlers = remote_entity_mapping["handlers"]
                    for handler in handlers:
                        output_entity = handler(output_entity)

                # indexes the output entity by the an index in case one was specified
                if "index" in remote_entity_mapping:
                    index_elements = remote_entity_mapping["index"]
                    index = self.convert_index_elements_to_index(index_elements, input_entity, output_entity)
                    self.index_entity(index, output_entity)

    def convert_attributes_intermediate_entity_remote_entity_attribute_mapping(self, input_intermediate_structure, output_intermediate_structure, options, remote_attribute_mapping, input_entity, output_entity):
        remote_attribute_name = remote_attribute_mapping["name"]
        attribute_name = remote_attribute_mapping["attribute_name"]

        self.data_converter_plugin.logger.info("[%s] Converting input entity attribute '%s.%s' to output entity attribute '%s.%s'" % (self.data_converter_plugin.id, input_entity.get_name(), attribute_name, output_entity.get_name(), remote_attribute_name))

        # retrieves the input intermediate entity's attribute value
        input_attribute_value = input_entity.get_attribute(attribute_name)

        # runs the validators to confirm if this mapping should be executed for this instance
        valid = True
        if "validators" in remote_attribute_mapping:
            validators = remote_attribute_mapping["validators"]
            for validator in validators:
                valid = validator(input_attribute_value)
                if not valid:
                    break

        # converts the input intermediate entity attributes into output intermediate entity attributes in case
        # all validators passed
        if valid:
            output_attribute_value = input_attribute_value

            # pipes the input attribute value throughout the configured handlers, if any
            if "handlers" in remote_attribute_mapping:
                handlers = remote_attribute_mapping["handlers"]
                for handler in handlers:
                    output_attribute_value = handler(output_attribute_value)

            # sets the post-processed input attribute value in the output entity
            output_entity.set_attribute(remote_attribute_name, output_attribute_value)

    def convert_relations(self, input_intermediate_structure, output_intermediate_structure, options):
        """
        Creates relations in the output intermediate structure.

        @type input_intermediate_structure: IntermediateStructure
        @param input_intermediate_structure: The intermediate structure where to extract data to infer which relations should be created.
        @type output_intermediate_structure: IntermediateStructure
        @param output_intermediate_structure: The intermediate structure where relations are going to be created.
        @type options: Dictionary
        @param options: Map with the options that specify how the conversion should be performed.
        """

        pass

    def convert_index_elements_to_index(self, index_elements, input_entity, output_entity):
        """
        Converts the index specified in the conversion options into the real index value.

        @type index_elements: List
        @param index_elements: The index specified in the conversion options.
        @type input_entity: Entity
        @param input_entity: The input entity that originated the output entity one wants to index.
        @type output_entity: Entity
        @param output_entity: The output entity one wants to index.
        @rtype: List
        @return: The real index value.
        """

        index = []

        # converts each index element into its real index value
        for index_element in index_elements:
            type, value = index_element

            if type == "constant":
                pass
            elif type == "input_attribute":
                attribute_name = value
                value = input_entity.get_attribute(attribute_name)
            elif type == "output_attribute":
                attribute_name = value
                value = output_entity.get_attribute(attribute_name)
            elif type == "function":
                function = value
                value = function(input_entity, output_entity)
            else:
                raise data_converter_exceptions.DataConverterIndexElementTypeUnknown("DataConverter.convert_index_elements_to_index - The specified index element is of an unknown type (index_element = %s)" % value)

            index.append(value)

        # turns the index list into a tuple because it is the expected format
        index = tuple(index)

        return index

    def index_entity(self, index, entity):
        """
        Indexes an entity by the specified index.

        @param index: The index to index the entity by.
        @type entity: Entity
        @param entity: The entity one wants to index.
        """

        # raises an exception in case the specified index already exists
        if index in self.index_entity_map:
            raise data_converter_exceptions.DataConverterDuplicateIndex("DataConverter.index_entity - The specified index already exists (index = %s)" % str(index))

        # indexes the entity by the specified index
        self.index_entity_map[index] = entity

    def get_entity(self, index):
        """
        Retrieves the entity that is indexed by the specified index.

        @param index: The index the desired entity is indexed by.
        @rtype: Entity
        @return: The entity that was indexed with the specified index.
        """

        # raises an exception in case the specified index does not exist
        if not index in self.index_entity_map:
            raise data_converter_exceptions.DataConverterEntityNotFound("DataConverter.get_entity - The specified index does not exist (index = %s)" % str(index))

        # retrieves the entity that is indexed by the specified index
        entity = self.index_entity_map[index]

        return entity
