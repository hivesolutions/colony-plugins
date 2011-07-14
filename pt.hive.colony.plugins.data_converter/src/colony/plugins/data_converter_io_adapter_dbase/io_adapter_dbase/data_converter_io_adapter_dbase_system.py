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

import os
import dbi
import odbc
import types
import datetime

import dbfpy.dbf

import data_converter_io_adapter_dbase_exceptions

INPUT_ATTRIBUTE_HANDLERS_VALUE = "input_attribute_handlers"
""" The input attribute handlers value """

INPUT_DIRECTORY_PATH_VALUE = "input_directory_path"
""" The input directory path value """

INPUT_ENTITY_HANDLERS_VALUE = "input_entity_handlers"
""" The input entity handlers value """

LOAD_ENTITIES_VALUE = "load_entities"
""" The load entities value """

LOAD_OPTIONS_VALUE = "load_options"
""" The load options value """

DBASE_TABLE_FILE_EXTENSION = ".dbf"
""" Extension of dbase table files """

ODBC_CONNECTION_STRING_TEMPLATE = "Driver={Microsoft Visual FoxPro Driver};SourceType=DBF;SourceDB=%s;Exclusive=No;Collate=Machine;NULL=YES;DELETED=YES;BACKGROUNDFETCH=NO;"
""" Odbc dbase connection string template """

SQL_TABLE_DUMP_QUERY_TEMPLATE = "select * from %s;"
""" Template for an sql table dump query """

class IoAdapterDbase:
    """
    Input output adapter used to load and save data converter intermediate structures
    to and from dbase format.
    """

    io_adapter_dbase_plugin = None
    """ Io adapter dbase plugin """

    def __init__(self, io_adapter_dbase_plugin):
        """
        Constructor of the class.

        @type io_adapter_dbase_plugin: IoAdapterDbasePlugin
        @param io_adapter_dbase_plugin: Input output adapter dbase plugin.
        """

        self.io_adapter_dbase_plugin = io_adapter_dbase_plugin

    def load_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the
        dbase source specified in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load
        the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        """

        # extracts the mandatory options
        directory_path = configuration.get_option(INPUT_DIRECTORY_PATH_VALUE)

        # raises an exception in case the specified directory does not exist
        if not os.path.exists(directory_path):
            raise data_converter_io_adapter_dbase_exceptions.IoAdapterDbaseDirectoryNotFound(directory_path)

        # indexes the dbase table names to their location
        table_name_path_map = self.index_dbase_tables(directory_path)

        # copies every table to the intermediate structure
        self.load_intermediate_structure_tables(intermediate_structure, options, table_name_path_map)

    def load_intermediate_structure_tables(self, intermediate_structure, options, table_name_path_map):
        """
        Populates the intermediate structure with data retrieved from the
        dbase source specified in the options for the specified tables.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load
        the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        @type table_name_path_map: Dictionary
        @param table_name_path_map: Map associating the names of the discovered dbase tables with the
        paths of the directories they are contained in.
        """

        table_names = table_name_path_map.keys()

        # extracts the non-mandatory_options
        load_options = options.get(LOAD_OPTIONS_VALUE, {})
        load_entity_name_attribute_names_map = load_options.get(LOAD_ENTITIES_VALUE, None)

        # extracts only the specified entity names in case they were provided
        if load_entity_name_attribute_names_map:
            table_names = load_entity_name_attribute_names_map.keys()

        # creates an entity in the intermediate structure for each table row
        for table_name_index in range(len(table_names)):
            table_name = table_names[table_name_index]

            self.io_adapter_dbase_plugin.info("Loading table '%s' (%d/%d)" % (table_name, table_name_index + 1, len(table_names)))

            # ignores this iteration in case the table doesn't exist
            if not table_name in table_name_path_map:
                self.io_adapter_dbase_plugin.warning("Skipping table '%s' because it doesn't exist" % (table_name))
                continue

            # prepares the intermediate structure to store entities with the specified name
            intermediate_structure.allocate_entity_name(table_name)

            # retrieves the file path where the table is located
            table_path = table_name_path_map[table_name]

            # opens the table file with dbfpy to retrieve the table's column names
            table_file_path = os.path.join(table_path, table_name + DBASE_TABLE_FILE_EXTENSION)
            records = dbfpy.dbf.Dbf(table_file_path)
            column_names = records.fieldNames
            load_column_names = column_names

            # extracts only the specified attribute names in case they were provided
            if load_entity_name_attribute_names_map and load_entity_name_attribute_names_map[table_name]:
                load_column_names = load_entity_name_attribute_names_map[table_name]

            try:
                # creates an odbc database connection to the database to retrieve its data
                odbc_connection_string = ODBC_CONNECTION_STRING_TEMPLATE % (table_path)
                odbc_connection = odbc.odbc(odbc_connection_string)
                cursor = odbc_connection.cursor()
                sql_table_dump_query = SQL_TABLE_DUMP_QUERY_TEMPLATE % (table_name)

                # performs an sql query on the table to retrieve its data
                cursor.execute(sql_table_dump_query)
                rows = cursor.fetchall()

                # creates an entity for each record and adds it to the intermediate structure
                self.load_intermediate_structure_table_rows(intermediate_structure, options, table_name, column_names, load_column_names, rows)
            finally:
                # closes the odbc database connection
                odbc_connection.close()

    def load_intermediate_structure_table_rows(self, intermediate_structure, options, table_name, column_names, load_column_names, rows):
        """
        Populates the intermediate structure with data retrieved from the
        dbase source specified in the options for the specified tables.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load
        the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        @type table_name: String
        @param table_name: Name of the table to which the provided rows belong.
        @type column_names: List
        @param column_names: List with the names of the provided rows' columns.
        @type load_column_names: List
        @param load_column_names: List with the names of the columns whose fields
        one wants to load.
        @type rows: List
        @param rows: List of table rows where to create entities from.
        """

        # extracts the non-mandatory options
        input_entity_handlers = options.get(INPUT_ENTITY_HANDLERS_VALUE, [])
        input_attribute_handlers = options.get(INPUT_ATTRIBUTE_HANDLERS_VALUE, [])

        # extends the input attribute handlers with the default ones
        default_input_attribute_handlers = [self.input_attribute_handler_convert_dbi_date, self.input_attribute_handler_convert_dbi_raw, self.input_attribute_handler_convert_string]
        input_attribute_handlers.extend(default_input_attribute_handlers)

        # creates an entity in the intermediate structure for each row
        for row in rows:

            # ignores the row in case it is completely empty
            non_null_field_values = [row[column_name_index] for column_name_index in range(len(column_names)) if not row[column_name_index] == None]
            if non_null_field_values:
                entity = intermediate_structure.create_entity(table_name)

                # sets each field as an entity attribute
                for load_column_name in load_column_names:
                    column_name_index = column_names.index(load_column_name)

                    # retrieves the field value and passes it through the
                    # configured field handlers
                    field_value = row[column_name_index]
                    for input_attribute_handler in input_attribute_handlers:
                        field_value = input_attribute_handler(intermediate_structure, entity, field_value)

                    # sets the post-processed field value in the entity attribute
                    column_name = column_names[column_name_index]
                    entity.set_attribute(column_name, field_value)

                # passes the entity through all input entity handlers
                for input_entity_handler in input_entity_handlers:
                    entity = input_entity_handler(intermediate_structure, entity)

    def save_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in dbase format at the location
        and with characteristics defined in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure
        into dbase format.
        """

        raise data_converter_io_adapter_dbase_exceptions.IoAdapterDbaseMethodNotImplemented()

    def index_dbase_tables(self, directory_path):
        """
        Crawls the provided directories searching for dbase tables and indexing
        their names to their directory path.

        @type directory_path: String
        @param directory_path: Directory paths where to search for tables.
        @rtype: Dictionary
        @return: Map associating the names of the discovered dbase tables with the
        paths of the directories they are contained in.
        """

        table_name_path_map = {}

        # indexes the paths to the tables discovered in the provided paths
        for walk_tuple in os.walk(directory_path, topdown = True):
            root_path = walk_tuple[0]
            files = walk_tuple[2]

            # indexes the path in case the file has a dbase table extension
            for file_name in files:
                extension_name = file_name[len(file_name) - 4:]
                if extension_name == DBASE_TABLE_FILE_EXTENSION:
                    table_name = file_name[:-4]
                    table_name_path_map[table_name] = root_path

        return table_name_path_map

    def input_attribute_handler_convert_dbi_raw(self, intermediate_structure, entity, attribute_value):
        """
        Converts the DbiRaw value to a string.

        @type value: DbiRaw
        @param value: The value one wants to convert.
        @rtype: String
        @return: The converted value.
        """

        # converts the dbi raw object to a string
        if type(attribute_value) == type(dbi.dbiRaw(0)):
            attribute_value = str(attribute_value)

        return attribute_value

    def input_attribute_handler_convert_dbi_date(self, intermediate_structure, entity, attribute_value):
        """
        Converts the DbiDate value to a Date object.

        @type value: DbiDate
        @param value: The value one wants to convert.
        @rtype: Date
        @return: The converted value.
        """

        # converts the dbi date to a datetime object
        if type(attribute_value) == type(dbi.dbiDate(0)):
            if int(attribute_value) == -1:
                attribute_value = None
            else:
                attribute_value = datetime.datetime.fromtimestamp(int(dbi.dbiDate(attribute_value)))

        return attribute_value

    def input_attribute_handler_convert_string(self, intermediate_structure, entity, attribute_value):
        """
        Converts the string to a stripped string or to a null value to
        circunvent dbase's string representation problems.

        @type value: String
        @param value: The value one wants to convert.
        @rtype: String
        @return: The stripped string, or None in case it is an empty string.
        """

        # strips the string and converts it to null in case it is empty
        if type(attribute_value) in types.StringTypes:
            attribute_value = attribute_value.strip()

            # returns None in case its an empty string
            if not attribute_value:
                return None

        return attribute_value
