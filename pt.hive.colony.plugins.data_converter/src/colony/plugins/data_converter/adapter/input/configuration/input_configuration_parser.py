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

import input_configuration

class Parser:

    def __init__(self):
        pass

    def parse(self):
        pass

    def get_value(self):
        pass

class InputConfigurationParser(Parser):
    """
    XML parser for the data converter input configuration.
    """

    file_path = None
    """ File path where the xml configuration file is located """

    input_configuration = None
    """ Input configuration extracted from the specified xml file """

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

        if node_name == "primary_key":
            self.parse_table_primary_key_columns(table_element, table)
        elif node_name == "foreign_keys":
            self.parse_table_foreign_keys(table_element, table)
        elif node_name == "name":
            table.name = table_element.firstChild.data.strip()
        elif node_name == "internal_entity":
            table.internal_entity = table_element.firstChild.data.strip()
        elif node_name == "handlers":
            self.parse_table_handlers(table_element, table)
        elif node_name == "columns":
            self.parse_table_columns(table_element, table)

    def parse_table_primary_key_columns(self, primary_key, table):
        child_nodes = primary_key.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                table.primary_key_columns.append(child_node.firstChild.data.strip())

    def parse_table_handlers(self, handlers, table):
        child_nodes = handlers.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                handler = self.parse_table_handler(child_node)
                table.handlers.append(handler)

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

    def parse_table_foreign_keys(self, foreign_keys, table):
        child_nodes = foreign_keys.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                foreign_key = self.parse_table_foreign_key(child_node)
                table.foreign_keys.append(foreign_key)

    def parse_table_foreign_key(self, foreign_key):
        foreign_key_structure = input_configuration.ForeignKey()
        child_nodes = foreign_key.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_table_foreign_key_element(child_node, foreign_key_structure)

        return foreign_key_structure

    def parse_table_foreign_key_element(self, foreign_key_element, foreign_key):
        node_name = foreign_key_element.nodeName

        if node_name == "foreign_key_columns":
            self.parse_table_foreign_key_columns(foreign_key_element, foreign_key)
        elif node_name == "foreign_table":
            foreign_key.foreign_table = foreign_key_element.firstChild.data.strip()

    def parse_table_foreign_key_columns(self, foreign_key_columns, foreign_key):
        child_nodes = foreign_key_columns.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                foreign_key.columns.append(child_node.firstChild.data.strip())

    def parse_table_columns(self, columns, table):
        child_nodes = columns.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                column = self.parse_table_column(child_node)
                table.add_column(column)

                # replace previously parse primary key and foreign key column names 
                # with their respective column instances
                if column.name in table.primary_key_columns:
                    table.primary_key_columns.remove(column.name)
                    table.primary_key_columns.append(column)
                for foreign_key in table.foreign_keys:
                    if column.name in foreign_key.columns:
                        foreign_key.columns.remove(column.name)
                        foreign_key.columns.append(column)

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
                column.handlers.append(handler)

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
    Gets if a node is valid or not for parsing.
    """

    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        return True
    return False
