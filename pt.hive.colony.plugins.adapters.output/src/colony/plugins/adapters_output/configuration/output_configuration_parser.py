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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import xml.dom.minidom

import output_configuration

#@todo: review and comment this file
class Parser:
    
    def __init__(self):
        pass
    
    def parse(self):
        pass
    
    def get_value(self):
        pass

class OutputConfigurationParser(Parser):
    
    file_path = None

    output_configuration = None
    
    def __init__(self, file_path = None):
        Parser.__init__(self)
        self.file_path = file_path
        self.output_configuration = output_configuration.OutputConfiguration()
       
    def parse(self):
        self.load_config_file(self.file_path)
        return self.output_configuration

    def load_config_file(self, file_path):
        # creates the xml document DOM object
        xml_document = xml.dom.minidom.parse(file_path)
        child_nodes = xml_document.childNodes
        
        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_output_configuration(child_node)
                
    def parse_output_configuration(self, output_configuration_element):
        child_nodes = output_configuration_element.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_output_configuration_element(child_node, self.output_configuration)
    
    def parse_output_configuration_element(self, output_configuration_element, output_configuration):
        node_name = output_configuration_element.nodeName

        if node_name == "domain_entities":
            self.parse_domain_entities(output_configuration_element, output_configuration)
                
    def parse_domain_entities(self, domain_entities, output_configuration):
        child_nodes = domain_entities.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                output_configuration.add_domain_entity(self.parse_domain_entity(child_node))

    def parse_domain_entity(self, domain_entity):
        domain_entity_structure = output_configuration.DomainEntity()
        child_nodes = domain_entity.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_domain_entity_element(child_node, domain_entity_structure)

        return domain_entity_structure

    def parse_domain_entity_element(self, domain_entity_element, domain_entity):
        node_name = domain_entity_element.nodeName

        if node_name == "name":
            domain_entity.name = domain_entity_element.firstChild.data.strip()
        elif node_name == "table":
            domain_entity.table = domain_entity_element.firstChild.data.strip()
        elif node_name == "internal_entity":
            domain_entity.internal_entity = domain_entity_element.firstChild.data.strip()
        elif node_name == "parent":
            domain_entity.parent = domain_entity_element.firstChild.data.strip()
        elif node_name == "handlers":
            self.parse_domain_entity_handlers(domain_entity_element, domain_entity)
        elif node_name == "attributes":
            self.parse_domain_entity_attributes(domain_entity_element, domain_entity)

    def parse_domain_entity_handlers(self, handlers, attribute):
        child_nodes = handlers.childNodes
        
        for child_node in child_nodes:
            if valid_node(child_node):
                handler = self.parse_domain_entity_handler(child_node)
                attribute.add_domain_entity_handler(handler)
                
    def parse_domain_entity_handler(self, handler):
        handler_structure = output_configuration.Handler()
        child_nodes = handler.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_domain_entity_handler_element(child_node, handler_structure)
        
        return handler_structure
    
    def parse_domain_entity_handler_element(self, handler_element, handler):
        node_name = handler_element.nodeName

        if node_name == "name":
            handler.name = handler_element.firstChild.data.strip()
        elif node_name == "module":
            handler.module = handler_element.firstChild.data.strip()
            
    def parse_domain_entity_attributes(self, attributes, domain_entity):
        child_nodes = attributes.childNodes
        
        for child_node in child_nodes:
            if valid_node(child_node):
                attribute = self.parse_domain_entity_attribute(child_node)
                domain_entity.add_domain_attribute(attribute)

    def parse_domain_entity_attribute(self, attribute):
        attribute_structure = output_configuration.DomainEntityAttribute()
        child_nodes = attribute.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_domain_entity_attribute_element(child_node, attribute_structure)

        return attribute_structure
    
    def parse_domain_entity_attribute_element(self, attribute_element, attribute):
        node_name = attribute_element.nodeName
                
        if node_name == "name":
            attribute.name = attribute_element.firstChild.data.strip()
        elif node_name == "type":
            attribute.type = attribute_element.firstChild.data.strip()
        elif node_name == "primary_key":
            primary_key = attribute_element.firstChild.data.strip()
            if primary_key == "true":
                attribute.primary_key = True
            elif primary_key == "false":
                attribute.primary_key = False
        elif node_name == "internal_attribute":
            attribute.internal_attribute = attribute_element.firstChild.data.strip()
        elif node_name == "handlers":
            self.parse_domain_entity_attribute_handlers(attribute_element, attribute)
        elif node_name == "referenced_domain_entity":
            attribute.referenced_domain_entity = self.parse_domain_entity_attribute_referenced_domain_entity(attribute_element)
    
    def parse_domain_entity_attribute_handlers(self, handlers, attribute):
        child_nodes = handlers.childNodes
        
        for child_node in child_nodes:
            if valid_node(child_node):
                handler = self.parse_domain_entity_attribute_handler(child_node)
                attribute.add_handler(handler)
                
    def parse_domain_entity_attribute_handler(self, handler):
        handler_structure = output_configuration.Handler()
        child_nodes = handler.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_domain_entity_attribute_handler_element(child_node, handler_structure)
        
        return handler_structure
    
    def parse_domain_entity_attribute_handler_element(self, handler_element, handler):
        node_name = handler_element.nodeName

        if node_name == "name":
            handler.name = handler_element.firstChild.data.strip()
        elif node_name == "module":
            handler.module = handler_element.firstChild.data.strip()
            
    def parse_domain_entity_attribute_referenced_domain_entity(self, referenced_domain_entity):
        referenced_domain_entity_structure = output_configuration.ReferencedDomainEntity()
        child_nodes = referenced_domain_entity.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_domain_entity_attribute_referenced_domain_entity_element(child_node, referenced_domain_entity_structure)

        return referenced_domain_entity_structure
    
    def parse_domain_entity_attribute_referenced_domain_entity_element(self, referenced_domain_entity_element, referenced_domain_entity):
        node_name = referenced_domain_entity_element.nodeName                
        if node_name == "name":
            referenced_domain_entity.name = referenced_domain_entity_element.firstChild.data.strip()
        elif node_name == "multiplicity":
            referenced_domain_entity.multiplicity = referenced_domain_entity_element.firstChild.data.strip()

def valid_node(node):
    """
    Gets if a node is valid or not for parsing
    """

    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        return True
    else:
        return False