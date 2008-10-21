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

import xml.dom.minidom

import input_configuration

#@todo: review and comment this file
class Parser:

    def __init__(self):
        pass

    def parse(self):
        pass

    def get_value(self):
        pass

class InputConfigurationParser(Parser):

    file_path = None
    input_configuration = None

    def __init__(self, file_path = None):
        Parser.__init__(self)
        self.file_path = file_path
        self.input_configuration = input_configuration.InputConfiguration()

    def parse(self):
        self.load_config_file(self.file_path)
        return self.input_configuration

    def load_config_file(self, file_path):
        # creates the xml document DOM object
        xml_document = xml.dom.minidom.parse(file_path)
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_input_configuration(child_node)

    def parse_input_configuration(self, input_configuration_element):
        child_nodes = input_configuration_element.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_input_configuration_element(child_node, self.input_configuration)

    def parse_input_configuration_element(self, input_configuration_element, input_configuration):
        node_name = input_configuration_element.nodeName

        if node_name == "tables":
            self.parse_tables(input_configuration_element, input_configuration)

    def parse_tables(self, tables, input_configuration):
        child_nodes = tables.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                input_configuration.add_table(self.parse_table(child_node))

    def parse_table(self, table):
        table_structure = input_configuration.Table()
        child_nodes = table.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_table_element(child_node, table_structure)

        return table_structure

    def parse_table_element(self, table_element, table):
        node_name = table_element.nodeName

        if node_name == "name":
            table.name = table_element.firstChild.data.strip()
        elif node_name == "internal_entity":
            table.internal_entity = table_element.firstChild.data.strip()
        elif node_name == "handlers":
            self.parse_table_handlers(table_element, table)
        elif node_name == "columns":
            self.parse_table_columns(table_element, table)

    def parse_table_handlers(self, handlers, table):
        child_nodes = handlers.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                handler = self.parse_table_handler(child_node)
                table.add_handler(handler)

    def parse_table_handler(self, handler):
        handler_structure = input_configuration.Handler()
        child_nodes = handler.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_table_handler_element(child_node, handler_structure)

        return handler_structure

    def parse_table_handler_element(self, handler_element, handler):
        node_name = handler_element.nodeName

        if node_name == "name":
            handler.name = handler_element.firstChild.data.strip()

    def parse_table_columns(self, columns, table):
        child_nodes = columns.childNodes
        
        for child_node in child_nodes:
            if valid_node(child_node):
                column = self.parse_table_column(child_node)
                table.add_column(column)

    def parse_table_column(self, column):
        column_structure = input_configuration.Column()
        child_nodes = column.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_table_column_element(child_node, column_structure)

        return column_structure

    def parse_table_column_element(self, column_element, column):
        node_name = column_element.nodeName

        if node_name == "name":
            column.name = column_element.firstChild.data.strip()
        elif node_name == "internal_entity":
            self.parse_table_column_internal_entity(column_element, column)
        elif node_name == "internal_attribute":
            column.internal_attribute = column_element.firstChild.data.strip()
        elif node_name == "primary_key":
            primary_key = column_element.firstChild.data.strip()
            if primary_key == "true":
                column.primary_key = True
            elif primary_key == "false":
                column.primary_key = False
        elif node_name == "referenced_table":
            column.referenced_table = column_element.firstChild.data.strip()
        elif node_name == "handlers":
            self.parse_table_column_handlers(column_element, column)

    def parse_table_column_internal_entity(self, internal_entity, column):
        child_nodes = internal_entity.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_table_column_internal_entity_element(child_node, column)

    def parse_table_column_internal_entity_element(self, internal_entity, column):
        node_name = internal_entity.nodeName

        if node_name == "name":
            column.internal_entity = internal_entity.firstChild.data.strip()
        elif node_name == "id":
            column.internal_entity_id = internal_entity.firstChild.data.strip()

    def parse_table_column_handlers(self, handlers, column):
        child_nodes = handlers.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                handler = self.parse_table_column_handler(child_node)
                column.add_handler(handler)

    def parse_table_column_handler(self, handler):
        handler_structure = input_configuration.Handler()
        child_nodes = handler.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_table_column_handler_element(child_node, handler_structure)

        return handler_structure

    def parse_table_column_handler_element(self, handler_element, handler):
        node_name = handler_element.nodeName

        if node_name == "name":
            handler.name = handler_element.firstChild.data.strip()

def valid_node(node):
    """
    Gets if a node is valid or not for parsing
    """

    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        return True
    return False
