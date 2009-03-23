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

import xml.dom.minidom

import data_converter_adapter_configuration

class Parser:

    def __init__(self):
        pass

    def parse(self):
        pass

    def get_value(self):
        pass

class DataConverterAdapterConfigurationParser(Parser):
    """
    XML parser for the data converter input configuration.
    """

    file_path = None
    """ File path where the xml configuration file is located """

    adapter_configuration = None
    """ Input configuration extracted from the specified xml file """

    def __init__(self, file_path = None):
        Parser.__init__(self)
        self.file_path = file_path
        self.adapter_configuration = data_converter_adapter_configuration.DataConverterAdapterConfiguration()

    def parse(self):
        self.load_config_file(self.file_path)
        return self.adapter_configuration

    def load_config_file(self, file_path):
        # creates the xml document DOM object
        xml_document = xml.dom.minidom.parse(file_path)
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_adapter_configuration(child_node)

    def parse_adapter_configuration(self, adapter_configuration_element):
        child_nodes = adapter_configuration_element.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_adapter_configuration_element(child_node, self.adapter_configuration)

    def parse_adapter_configuration_element(self, adapter_configuration_element, adapter_configuration):
        node_name = adapter_configuration_element.nodeName

        if node_name == "tables":
            self.parse_domain_entities(adapter_configuration_element, adapter_configuration)

    def parse_domain_entities(self, domain_entities, adapter_configuration):
        child_nodes = domain_entities.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                adapter_configuration.add_domain_entity(self.parse_domain_entity(child_node))

    def parse_domain_entity(self, domain_entity):
        domain_entity_structure = data_converter_adapter_configuration.DomainEntity()
        child_nodes = domain_entity.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_domain_entity_element(child_node, domain_entity_structure)

        return domain_entity_structure

    def parse_domain_entity_element(self, domain_entity_element, domain_entity):
        node_name = domain_entity_element.nodeName

        if node_name == "primary_key":
            self.parse_domain_entity_primary_key_domain_attributes(domain_entity_element, domain_entity)
        elif node_name == "foreign_keys":
            self.parse_domain_entity_foreign_keys(domain_entity_element, domain_entity)
        elif node_name == "name":
            domain_entity.name = domain_entity_element.firstChild.data.strip()
        elif node_name == "internal_entity":
            domain_entity.internal_entity = domain_entity_element.firstChild.data.strip()
        elif node_name == "handlers":
            self.parse_domain_entity_handlers(domain_entity_element, domain_entity)
        elif node_name == "columns":
            self.parse_domain_attributes(domain_entity_element, domain_entity)

    def parse_domain_entity_primary_key_domain_attributes(self, primary_key, domain_entity):
        child_nodes = primary_key.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                domain_entity.primary_key_domain_attributes.append(child_node.firstChild.data.strip())

    def parse_domain_entity_handlers(self, handlers, domain_entity):
        child_nodes = handlers.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                handler = self.parse_domain_entity_handler(child_node)
                domain_entity.handlers.append(handler)

    def parse_domain_entity_handler(self, handler):
        handler_structure = data_converter_adapter_configuration.Handler()
        child_nodes = handler.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_domain_entity_handler_element(child_node, handler_structure)

        return handler_structure

    def parse_domain_entity_handler_element(self, handler_element, handler):
        node_name = handler_element.nodeName

        if node_name == "name":
            handler.name = handler_element.firstChild.data.strip()

    def parse_domain_entity_foreign_keys(self, foreign_keys, domain_entity):
        child_nodes = foreign_keys.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                foreign_key = self.parse_domain_entity_foreign_key(child_node)
                domain_entity.foreign_keys.append(foreign_key)

    def parse_domain_entity_foreign_key(self, foreign_key):
        foreign_key_structure = data_converter_adapter_configuration.ForeignKey()
        child_nodes = foreign_key.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_domain_entity_foreign_key_element(child_node, foreign_key_structure)

        return foreign_key_structure

    def parse_domain_entity_foreign_key_element(self, foreign_key_element, foreign_key):
        node_name = foreign_key_element.nodeName

        if node_name == "foreign_key_columns":
            self.parse_domain_entity_foreign_key_domain_attributes(foreign_key_element, foreign_key)
        elif node_name == "foreign_table":
            foreign_key.foreign_domain_entity = foreign_key_element.firstChild.data.strip()

    def parse_domain_entity_foreign_key_domain_attributes(self, foreign_key_domain_attributes, foreign_key):
        child_nodes = foreign_key_domain_attributes.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                foreign_key.domain_attributes.append(child_node.firstChild.data.strip())

    def parse_domain_attributes(self, domain_attributes, domain_entity):
        child_nodes = domain_attributes.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                domain_attribute = self.parse_domain_attribute(child_node)
                domain_entity.add_domain_attribute(domain_attribute)

                # replace previously parse primary key and foreign key domain attribute names 
                # with their respective domain attribute instances
                if domain_attribute.name in domain_entity.primary_key_domain_attributes:
                    domain_entity.primary_key_domain_attributes.remove(domain_attribute.name)
                    domain_entity.primary_key_domain_attributes.append(domain_attribute)
                for foreign_key in domain_entity.foreign_keys:
                    if domain_attribute.name in foreign_key.domain_attributes:
                        foreign_key.domain_attributes.remove(domain_attribute.name)
                        foreign_key.domain_attributes.append(domain_attribute)

    def parse_domain_attribute(self, domain_attribute):
        domain_attribute_structure = data_converter_adapter_configuration.DomainAttribute()
        child_nodes = domain_attribute.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_domain_attribute_element(child_node, domain_attribute_structure)

        return domain_attribute_structure

    def parse_domain_attribute_element(self, domain_attribute_element, domain_attribute):
        node_name = domain_attribute_element.nodeName

        if node_name == "name":
            domain_attribute.name = domain_attribute_element.firstChild.data.strip()
        elif node_name == "internal_entity":
            self.parse_domain_attribute_internal_entity(domain_attribute_element, domain_attribute)
        elif node_name == "internal_attribute":
            domain_attribute.internal_attribute = domain_attribute_element.firstChild.data.strip()
        elif node_name == "handlers":
            self.parse_domain_attribute_handlers(domain_attribute_element, domain_attribute)

    def parse_domain_attribute_internal_entity(self, internal_entity, domain_attribute):
        child_nodes = internal_entity.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_domain_attribute_internal_entity_element(child_node, domain_attribute)

    def parse_domain_attribute_internal_entity_element(self, internal_entity, domain_attribute):
        node_name = internal_entity.nodeName

        if node_name == "name":
            domain_attribute.internal_entity = internal_entity.firstChild.data.strip()
        elif node_name == "id":
            domain_attribute.internal_entity_id = internal_entity.firstChild.data.strip()

    def parse_domain_attribute_handlers(self, handlers, domain_attribute):
        child_nodes = handlers.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                handler = self.parse_domain_attribute_handler(child_node)
                domain_attribute.handlers.append(handler)

    def parse_domain_attribute_handler(self, handler):
        handler_structure = data_converter_adapter_configuration.Handler()
        child_nodes = handler.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_domain_attribute_handler_element(child_node, handler_structure)

        return handler_structure

    def parse_domain_attribute_handler_element(self, handler_element, handler):
        node_name = handler_element.nodeName

        if node_name == "name":
            handler.name = handler_element.firstChild.data.strip()

def valid_node(node):
    """
    Indicates if a node is valid or not for parsing.
    """

    return node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE
