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

import types

import data_converter_io_adapter_xml_exceptions

BEAUTIFY_VALUE = "beautify"
""" The beautify value """

ENTITY_META_ATTRIBUTES_VALUE = "entity_meta_attributes"
""" The entity meta attributes value """

ENTITY_TAG_ORDER_VALUE = "entity_tag_order"
""" The entity tag order value """

MANDATORY_TAGS_VALUE = "mandatory_tags"
""" The mandatory tags value """

OUTPUT_FILE_PATH_VALUE = "output_file_path"
""" The output file path value """

ROOT_ENTITY_NAME_VALUE = "root_entity_name"
""" The root entity name value """

XML_START_TAG = "<?xml version=\"%s\" encoding=\"%s\"?>"
""" The xml start tag """

XML_NODE_TAG_FORMAT = "<%s>%s</%s>"
""" The xml node tag format """

XML_NODE_EMPTY_TAG_FORMAT = "<%s/>"
""" The xml empty tag format """

XML_NODE_START_TAG_FORMAT = "<%s%s>"
""" The xml node start tag format """

XML_NODE_END_TAG_FORMAT = "</%s>"
""" The xml node end tag format """

XML_VERSION_VALUE = "xml_version"
""" The xml version value """

XML_ENCODING_VALUE = "xml_encoding"
""" The xml encoding value """

FIRST_INDENTATION_LEVEL = 0
""" The number indentations that are applied to the first entry level """

INDENTATION_TOKEN = " "
""" The token that will be used to apply an indentation """

DEFAULT_BEAUTIFY_SETTING = False
""" Boolean indicating if the output xml file should be beautified """

DEFAULT_XML_VERSION = "1.0"
""" The default xml version that will be used in the output file """

DEFAULT_XML_ENCODING = "utf-8"
""" The default xml encoding that will be used in the output file """

class IoAdapterXml:
    """
    Input output adapter used to load and save data converter intermediate
    structures to and from xml format.
    """

    io_adapter_xml_plugin = None
    """ Io adapter xml plugin """

    def __init__(self, io_adapter_xml_plugin):
        """
        Constructor of the class.

        @type io_adapter_xml_plugin: IoAdapterXmlPlugin
        @param io_adapter_xml_plugin: Input output adapter xml plugin.
        """

        self.io_adapter_xml_plugin = io_adapter_xml_plugin

    def load_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the
        xml source specified in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to
        load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        """

        raise data_converter_io_adapter_xml_exceptions.IoAdapterXmlMethodNotImplemented()

    def save_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in xml format at the location
        and with characteristics defined in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate
        structure into xml format.
        """

        # extracts the mandatory options
        root_entity_name = options[ROOT_ENTITY_NAME_VALUE]
        file_path = configuration.get_option(OUTPUT_FILE_PATH_VALUE)

        # extracts the non-mandatory options
        xml_version = options.get(XML_VERSION_VALUE, DEFAULT_XML_VERSION)
        xml_encoding = options.get(XML_ENCODING_VALUE, DEFAULT_XML_ENCODING)
        beautify = options.get(BEAUTIFY_VALUE, DEFAULT_BEAUTIFY_SETTING)

        # opens the target xml file
        output_file = open(file_path, "wb")

        # retrieves the root entity
        entities = intermediate_structure.get_entities_by_name(root_entity_name)

        # throws an exception in case more than one
        # root entity was retrieved
        if len(entities) > 1:
            raise data_converter_io_adapter_xml_exceptions.IoAdapterXmlUnexpectedNumberRootEntities()

        # retrieves the root entity from the list
        # of retrieved entities
        root_entity = entities[0]

        # creates the xml file's start tag, indenting and breaking the line in case beautification is enabled
        xml_start_tag = XML_START_TAG % (xml_version, xml_encoding)
        if beautify:
            xml_start_tag = xml_start_tag + "\n"

        # writes the xml file's start tag to the output file
        self.write_to_file(output_file, xml_start_tag, xml_encoding)

        # saves the root entity
        self.save_entity(intermediate_structure, options, output_file, root_entity, FIRST_INDENTATION_LEVEL)

        # closes the xml file
        output_file.close()

    def save_entity(self, intermediate_structure, options, output_file, entity, indentation_level):
        # extracts the non-mandatory options
        entity_meta_attributes_map = options.get(ENTITY_META_ATTRIBUTES_VALUE, {})
        beautify = options.get(BEAUTIFY_VALUE, DEFAULT_BEAUTIFY_SETTING)
        entity_tag_order_map = options.get(ENTITY_TAG_ORDER_VALUE, {})
        xml_encoding = options.get(XML_ENCODING_VALUE, DEFAULT_XML_ENCODING)

        # retrieves the entity's name
        entity_name = entity.get_name()

        # creates the meta attributes string for this entity
        entity_meta_attributes = ""
        if entity_name in entity_meta_attributes_map:
            meta_attributes_map = entity_meta_attributes_map[entity_name]
            for meta_attribute_name, meta_attribute_value in meta_attributes_map.items():
                entity_meta_attributes += " " + meta_attribute_name + "=\"" +  meta_attribute_value + "\""

        # creates the entity's start tag, indenting and breaking the line in case beautification is enabled
        entity_start_tag = XML_NODE_START_TAG_FORMAT % (entity_name, entity_meta_attributes)
        if beautify:
            entity_start_tag = INDENTATION_TOKEN * indentation_level + entity_start_tag + "\n"

        # writes the entity start tag to the output file
        self.write_to_file(output_file, entity_start_tag, xml_encoding)

        # retrieves the entity's attributes
        attribute_name_value_map = entity.get_attributes()
        attribute_name_values = attribute_name_value_map.items()

        # sorts the entity's attributes in case their order was specified
        if entity_name in entity_tag_order_map:
            sorted_entity_attribute_names = entity_tag_order_map[entity_name]
            attribute_name_values.sort(lambda x, y: sorted_entity_attribute_names.index(x[0]) - sorted_entity_attribute_names.index(y[0]))

        # writes the entity's attribute to the xml file
        for attribute_name, attribute_value in attribute_name_values:
            if type(attribute_value) == types.ListType:
                for attribute_value_entity in attribute_value:
                    self.save_entity_attribute(intermediate_structure, options, output_file, entity, attribute_name, attribute_value_entity, indentation_level + 1)
            else:
                self.save_entity_attribute(intermediate_structure, options, output_file, entity, attribute_name, attribute_value, indentation_level + 1)

        # creates the entity's end tag, indenting and breaking the line in case beautification is enabled
        entity_end_tag = XML_NODE_END_TAG_FORMAT % entity_name
        if beautify:
            entity_end_tag = INDENTATION_TOKEN * indentation_level + entity_end_tag + "\n"

        # writes the entity's end tag to the output file
        self.write_to_file(output_file, entity_end_tag, xml_encoding)

    def save_entity_attribute(self, intermediate_structure, options, output_file, entity, attribute_name, attribute_value, indentation_level):
        # extracts the non-mandatory options
        beautify = options.get(BEAUTIFY_VALUE, DEFAULT_BEAUTIFY_SETTING)
        mandatory_tags = options.get(MANDATORY_TAGS_VALUE, [])
        xml_encoding = options.get(XML_ENCODING_VALUE, DEFAULT_XML_ENCODING)

        # calls the save entity function again in case the attribute is an entity
        if type(attribute_value) == types.InstanceType:
            self.save_entity(intermediate_structure, options, output_file, attribute_value, indentation_level)
        else:
            attribute_tag = None

            # creates the entity's attribute tag
            if not attribute_value == None:
                attribute_tag = XML_NODE_TAG_FORMAT % (attribute_name, attribute_value, attribute_name)
            elif attribute_name in mandatory_tags:
                # creates and empty tag if the tag is mandatory
                attribute_tag = XML_NODE_EMPTY_TAG_FORMAT % (attribute_name)

            # indents and breaks the line in case beautification is enabled
            if attribute_tag and beautify:
                attribute_tag = INDENTATION_TOKEN * indentation_level + attribute_tag + "\n"

            # writes the attribute tag to the output file
            if attribute_tag:
                self.write_to_file(output_file, attribute_tag, xml_encoding)

    def write_to_file(self, output_file, value, encoding):
        # encodes the value to the specified xml encoding and writes it to the file
        encoded_value = value.encode(encoding)
        output_file.write(encoded_value)
