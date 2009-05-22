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

class DataConverter:
    """
    Converts data from one medium and schema to another.
    """

    data_converter_plugin = None
    """ Data converter plugin """

    index_entity_map = {}
    """ Dictionary associating an index with an entity """

    def __init__(self, data_converter_plugin):
        """
        Class constructor.

        @type data_converter_plugin: DataConverterPlugin
        @param data_converter_plugin: Data converter plugin.
        """

        self.data_converter_plugin = data_converter_plugin
        self.index_entity_map = {}

    def check_mandatory_options(self, mandatory_attributes, options, function_name):
        # raises an exception in case one of the mandatory conversion options is not provided
        for mandatory_attribute_name in mandatory_attributes:
            if not mandatory_attribute_name in options:
                raise data_converter_exceptions.DataConverterOptionMissing("%s - Mandatory option not supplied (option_name = %s)" % (function_name, mandatory_attribute_name))

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

        # extracts the mandatory options
        input_adapter_plugin_id = input_options["io_adapter_plugin_id"]
        output_adapter_plugin_id = output_options["io_adapter_plugin_id"]

        # creates the input and output intermediate structures
        input_intermediate_structure = self.data_converter_plugin.intermediate_structure_plugin.create_intermediate_structure()
        output_intermediate_structure = self.data_converter_plugin.intermediate_structure_plugin.create_intermediate_structure()

        # loads the source data into the input intermediate structure
        self.data_converter_plugin.intermediate_structure_plugin.load(input_intermediate_structure, input_adapter_plugin_id, input_options)

        # migrate the input intermediate structure's entity attributes to the output intermediate structure
        if "attribute_mapping" in conversion_options:
            attribute_mapping = conversion_options["attribute_mapping"]
            self.convert_attributes(input_intermediate_structure, output_intermediate_structure, attribute_mapping)

        # migrate the output intermediate structure's entity relations to the output intermediate structure
        if "relation_mapping" in conversion_options:
            relation_mapping = conversion_options["relation_mapping"]
            self.convert_relations(input_intermediate_structure, output_intermediate_structure, relation_mapping)

        # saves the output intermediate structure with the results of the conversion
        self.data_converter_plugin.intermediate_structure_plugin.save(output_intermediate_structure, output_adapter_plugin_id, output_options)

        self.data_converter_plugin.logger.info("[%s] Data conversion process ended" % self.data_converter_plugin.id)

    def convert_attributes(self, input_intermediate_structure, output_intermediate_structure, attribute_mapping):
        """
        Converts the entities in the input intermediate structure and their respective attributes into entities in the output intermediate structure.

        @type input_intermediate_structure: IntermediateStructure
        @param input_intermediate_structure: The intermediate structure where entities are going to be converted from.
        @type output_intermediate_structure: IntermediateStructure
        @param output_intermediate_structure: The intermediate structure where entities are going to be converted to.
        @type attribute_mapping: Dictionary
        @param attribute_mapping: Map with the options that specify how the attribute conversion should be performed.
        """

        # converts each input intermediate entity with the name specified in the mapping
        input_entities_mapping = attribute_mapping["input_entities"]
        for input_entity_mapping in input_entities_mapping:
            self.convert_attributes_input_entity_mapping(input_intermediate_structure, output_intermediate_structure, input_entity_mapping)

    def convert_attributes_input_entity_mapping(self, input_intermediate_structure, output_intermediate_structure, input_entity_mapping):
        # raises an exception in case one of the mandatory options is not provided
        self.check_mandatory_options(["name"], input_entity_mapping, "DataConverter.convert_attributes_input_entity_mapping")

        # extracts the mandatory options
        input_entity_name = input_entity_mapping["name"]

        # converts each input entity into a number of output entities
        output_entities_mapping = input_entity_mapping["output_entities"]
        for output_entity_mapping in output_entities_mapping:
            self.convert_attributes_input_entity_output_entity_mapping(input_intermediate_structure, output_intermediate_structure, output_entity_mapping, input_entity_name)

    def convert_attributes_input_entity_output_entity_mapping(self, input_intermediate_structure, output_intermediate_structure, output_entity_mapping, input_entity_name):
        # raises an exception in case one of the mandatory options is not provided
        self.check_mandatory_options(["name"], output_entity_mapping, "DataConverter.convert_attributes_input_entity_output_entity_mapping")

        # extracts the mandatory options
        output_entity_name = output_entity_mapping["name"]

        # retrieves all input entities with the name specified in the mapping and converts them
        input_entities = input_intermediate_structure.get_entities(input_entity_name)
        for input_entity in input_entities:

            # runs the validators to confirm if this mapping should be executed for this instance
            valid = True
            if "validators" in output_entity_mapping:
                validators = output_entity_mapping["validators"]
                for validator in validators:
                    valid = validator(input_entity)
                    if not valid:
                        break

            # converts the input entity into output entities in case all validators passed
            if valid:

                # creates an entity in the output intermediate structure to convert the input entity into
                output_entity = output_intermediate_structure.create_entity(output_entity_name)

                # converts the input entities' attributes into a number of output entity attributes
                output_attributes_mapping = output_entity_mapping["output_attributes"]
                for output_attribute_mapping in output_attributes_mapping:
                    self.convert_attributes_input_entity_output_entity_attribute_mapping(input_intermediate_structure, output_intermediate_structure, output_attribute_mapping, input_entity, output_entity)

                # pipes the output entity through the configured handlers, if any
                if "handlers" in output_entity_mapping:
                    handlers = output_entity_mapping["handlers"]
                    for handler in handlers:
                        output_entity = handler(output_entity)

                # indexes the output entity by the an index in case one was specified
                if "index" in output_entity_mapping:
                    index_elements = output_entity_mapping["index"]
                    index = self.convert_index_elements_to_index(index_elements, input_entity, output_entity)
                    self.index_entity(index, output_entity)

                # index the created output entity so that its origins can be traced back afterwards
                self.index_entity(("input_entity_object_id", input_entity.get_name(), "=", input_entity.get_object_id(), "created", "output_entity_name", "=", output_entity.get_name()), output_entity)

    def convert_attributes_input_entity_output_entity_attribute_mapping(self, input_intermediate_structure, output_intermediate_structure, output_attribute_mapping, input_entity, output_entity):
        # raises an exception in case one of the mandatory options is not provided
        self.check_mandatory_options(["name", "attribute_name"], output_attribute_mapping, "DataConverter.convert_attributes_input_entity_output_entity_attribute_mapping")

        # extracts the mandatory options
        output_attribute_name = output_attribute_mapping["name"]
        attribute_name = output_attribute_mapping["attribute_name"]

        self.data_converter_plugin.logger.info("[%s] Converting input entity attribute '%s.%s' (object_id = %d) to output entity attribute '%s.%s' (object_id = %d)" % (self.data_converter_plugin.id, input_entity.get_name(), attribute_name, input_entity.get_object_id(), output_entity.get_name(), output_attribute_name, output_entity.get_object_id()))

        # retrieves the input entity's attribute value
        input_attribute_value = input_entity.get_attribute(attribute_name)

        # runs the validators to confirm if this mapping should be executed for this instance
        valid = True
        if "validators" in output_attribute_mapping:
            validators = output_attribute_mapping["validators"]
            for validator in validators:
                valid = validator(input_attribute_value)
                if not valid:
                    break

        # converts the input entity attributes into output entity attributes in case
        # all validators passed
        if valid:
            output_attribute_value = input_attribute_value

            # pipes the input attribute value throughout the configured handlers, if any
            if "handlers" in output_attribute_mapping:
                handlers = output_attribute_mapping["handlers"]
                for handler in handlers:
                    output_attribute_value = handler(output_attribute_value)

            # sets the post-processed input attribute value in the output entity
            output_entity.set_attribute(output_attribute_name, output_attribute_value)

    def convert_relations(self, input_intermediate_structure, output_intermediate_structure, relation_mapping):
        """
        Creates relations in the output intermediate structure.

        @type input_intermediate_structure: IntermediateStructure
        @param input_intermediate_structure: The intermediate structure where to extract data to infer which relations should be created.
        @type output_intermediate_structure: IntermediateStructure
        @param output_intermediate_structure: The intermediate structure where relations are going to be created.
        @type relation_mapping: Dictionary
        @param relation_mapping: Map with the options that specify how the relation conversion should be performed.
        """

        # raises an exception in case one of the mandatory options is not provided
        self.check_mandatory_options(["entities"], relation_mapping, "DataConverter.convert_relations")

        # extracts the mandatory options
        entities_mapping = relation_mapping["entities"]

        # creates relations for every instance of the mapped entities
        for entity_mapping in entities_mapping:
            self.convert_relations_entity_mapping(input_intermediate_structure, output_intermediate_structure, entity_mapping)

    def convert_relations_entity_mapping(self, input_intermediate_structure, output_intermediate_structure, entity_mapping):
        # raises an exception in case one of the mandatory options is not provided
        self.check_mandatory_options(["name"], entity_mapping, "DataConverter.convert_relations_entity_mapping")

        # extracts the mandatory options
        entity_name = entity_mapping["name"]

        # creates the mapped relations for every entity instance
        relations_mapping = entity_mapping["relations"]
        for relation_mapping in relations_mapping:
            self.convert_relations_entity_relation_mapping(input_intermediate_structure, output_intermediate_structure, relation_mapping, entity_name)

    def convert_relations_entity_relation_mapping(self, input_intermediate_structure, output_intermediate_structure, relation_mapping, entity_name):
        # raises an exception in case one of the mandatory options is not provided
        self.check_mandatory_options(["index", "entity_relation_attribute_names", "related_entity_relation_attribute_names"], relation_mapping, "DataConverter.convert_relations_entity_relation_mapping")

        # extracts the mandatory options
        index_elements = relation_mapping["index"]
        entity_relation_attribute_names = relation_mapping["entity_relation_attribute_names"]
        related_entity_relation_attribute_names = relation_mapping["related_entity_relation_attribute_names"]

        # creates relations for each entity in the output intermediate structure
        entities = output_intermediate_structure.get_entities(entity_name)
        for entity in entities:
            index = self.convert_index_elements_to_index(index_elements, entity, None)

            # creates a relation with every entity at the specified index
            related_entities = self.get_entities(index)
            for related_entity in related_entities:

                # adds the related entity to every specified relation attribute in the entity
                for entity_relation_attribute_name in entity_relation_attribute_names:
                    self.connect_entities(entity, entity_relation_attribute_name, related_entity)

                # adds the entity to every specified relation attribute in the related entity
                for related_entity_relation_attribute_name in related_entity_relation_attribute_names:
                    self.connect_entities(related_entity, related_entity_relation_attribute_name, entity)

    def connect_entities(self, entity, entity_relation_attribute_name, related_entity):
        """
        Connects an entity to another.

        @type entity: Entity
        @param entity: Entity where one wants to add a related entity to its relation attribute.
        @type entity_relation_attribute_name: str
        @param entity_relation_attribute_name: Name of the entity's relation attribute.
        @type related_entity: Entity
        @param related_entity: Entity one wants to add to the relation attribute.
        """

        self.data_converter_plugin.logger.info("[%s] Adding entity '%s' (object_id = %d) to entity relation '%s.%s' (object_id = %d)" % (self.data_converter_plugin.id, related_entity.get_name(), related_entity.get_object_id(), entity.get_name(), entity_relation_attribute_name, entity.get_object_id()))

        # retrieves the entity's relation attribute value
        entity_relation_attribute_value = None
        if entity.has_attribute(entity_relation_attribute_name):
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

            # doesn't interpret the value in case it is a constant
            if type == "constant":
                pass
            elif type == "input_attribute":
                # retrieves the attribute in the input entity with the name specified in the value
                attribute_name = value
                value = input_entity.get_attribute(attribute_name)
            elif type == "output_attribute":
                # retrieves the attribute in the output entity with the name specified in the value
                attribute_name = value
                value = output_entity.get_attribute(attribute_name)
            elif type == "function":
                # uses the return of the function passed in the value
                function = value
                value = function(input_entity, output_entity)
            else:
                # raises an exception in case the index element type is not one of the previous ones
                raise data_converter_exceptions.DataConverterIndexElementTypeUnknown("DataConverter.convert_index_elements_to_index - The specified index element is of an unknown type (index_element = %s)" % value)

            # adds the real index value to the index
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

        # creates an index in case the specified one doesn't exist yet
        if not index in self.index_entity_map:
            self.index_entity_map[index] = []

        # indexes the entity by the specified index
        self.index_entity_map[index].append(entity)

    def get_entities(self, index):
        """
        Retrieves the entity that is indexed by the specified index.

        @param index: The index the desired entity is indexed by.
        @rtype: Entity
        @return: The entity that was indexed with the specified index.
        """

        # raises an exception in case the specified index does not exist
        if not index in self.index_entity_map:
            raise data_converter_exceptions.DataConverterEntityNotFound("DataConverter.get_entities - The specified index does not exist (index = %s)" % str(index))

        # retrieves the entity that is indexed by the specified index
        entity = self.index_entity_map[index]

        return entity
