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

import datetime
import dbi
import odbc
import stat
import string
import os.path
import dbfpy.dbf
import dbfpy.fields

import io_adapter_dbase_exceptions

DBASE_EXTENSION = ".dbf"
CONNECTION_STRING = "Driver={Microsoft Visual FoxPro Driver};SourceType=DBF;SourceDB=%s;Exclusive=No;Collate=Machine;NULL=NO;DELETED=NO;BACKGROUNDFETCH=NO;"
SQL_TABLE_DUMP_QUERY = "SELECT * FROM %s;"

class IoAdapterDbase:
    """
    Input output adapter used to serialize data converter intermediate structures to dbase format.
    """

    input_field_handlers = []
    """ List of handlers every field value is passed through before being input """

    output_field_handlers = []
    """ List of handlers every field value is passed through before being output """

    def __init__(self, io_adapter_dbase_plugin):
        """
        Class constructor.

        @type io_adapter_dbase_plugin: IoAdapterDbasePlugin
        @param io_adapter_dbase_plugin: Input output adapter dbase plugin.
        """

        self.io_adapter_dbase_plugin = io_adapter_dbase_plugin

        # sets the default input field handlers to process dates, strings and raw value
        self.input_field_handlers = [self.process_dbi_date, self.process_dbi_raw, self.process_string]

        # sets the default output field handlers
        self.output_field_handlers = []

        # overrides the dbfpy handler for general, memo and date field types
        # so it doesn't crash when the column names are retrieved through it
        dbfpy.fields.registerField(DbfGeneralFieldDef)
        dbfpy.fields.registerField(DbfMemoFieldDef)
        dbfpy.fields.registerField(DbfDateFieldDef)

    def load(self, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the dbase source specified in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the provided intermediate structure.
        """

        self.io_adapter_dbase_plugin.logger.info("[%s] Loading intermediate structure with dbase io adapter" % self.io_adapter_dbase_plugin.id)

        # raises an exception in case one of the mandatory options is not provided
        mandatory_options = ["directory_paths"]
        for mandatory_option in mandatory_options:
            if not mandatory_option in options:
                raise io_adapter_dbase_exceptions.IoAdapterDbaseOptionNotFound("IoAdapterDbase.load - Mandatory option not supplied (option_name = %s)" % mandatory_option)

        # extracts the mandatory options
        directory_paths = options["directory_paths"]

        # adds the provided input field handlers to the default field handlers
        if "input_field_handlers" in options:
            input_field_handlers = options["input_field_handlers"]
            self.input_field_handlers.extend(input_field_handlers)

        # adds the provided output field handlers to the default field handlers
        if "output_field_handlers" in options:
            output_field_handlers = options["output_field_handlers"]
            self.output_field_handlers.extend(output_field_handlers)

        # raises an exception in case the specified directory does not exist
        for directory_path in directory_paths:
            if not os.path.exists(directory_path):
                raise io_adapter_dbase_exceptions.IoAdapterDbaseOptionValid("IoAdapterDbase.load - Specified directory to load intermediate structure from does not exist (directory_path = %s)" % directory_path)

        # indexes the dbase table names to their location
        table_name_path_map = {}
        for directory_path in directory_paths:
            for root_path, directories, files in os.walk(directory_path, topdown=True):
                for file_name in files:
                    extension_name = file_name[len(file_name) - 4:]
                    if extension_name == DBASE_EXTENSION:
                        table_name = file_name[:-4]
                        table_name_path_map[table_name] = root_path

        # for each table open a connection to it and dump the table's contents to the intermediate structure
        table_names = table_name_path_map.keys()

        self.io_adapter_dbase_plugin.logger.info("[%s] Loading %d tables with dbase io adapter" % (self.io_adapter_dbase_plugin.id, len(table_names)))

        # copies every table to the intermediate structure
        for table_index in range(len(table_names)):
            table_name = table_names[table_index]

            self.io_adapter_dbase_plugin.logger.info("[%s] Loading table '%s' (%d/%d) with dbase io adapter" % (self.io_adapter_dbase_plugin.id, table_name, table_index, len(table_names)))

            # retrieves the file path where the table is located
            table_path = table_name_path_map[table_name]

            # sets ups the means to interact with the table
            table_file_path = os.path.join(table_path, table_name + ".dbf")
            records = dbfpy.dbf.Dbf(table_file_path)
            column_names_query = [table_name + "." + field_name + ", " for field_name in records.fieldNames][:-2]
            odbc_connection_string = CONNECTION_STRING % (table_path)
            odbc_connection = odbc.odbc(odbc_connection_string)
            cursor = odbc_connection.cursor()
            sql_table_dump_query = SQL_TABLE_DUMP_QUERY % (table_name)

            try:
                # performs an sql query on the table to retrieve its data
                cursor.execute(sql_table_dump_query)
                results = cursor.fetchall()

                # creates an entity for each record and adds it to the intermediate structure
                for result in results:
                    entity = intermediate_structure.create_entity(table_name)

                    # sets each field as an entity attribute
                    for column_name_index in range(len(records.fieldNames)):

                        # retrieves the field value and passes it through the
                        # configured field handlers
                        field_value = result[column_name_index]
                        for input_field_handler in self.input_field_handlers:
                            field_value = input_field_handler(field_value)

                        # sets the post-processed field value in the entity attribute
                        column_name = records.fieldNames[column_name_index]
                        entity.set_attribute(column_name, field_value)
            except:
                self.io_adapter_dbase_plugin.logger.error("[%s] Error executing query (query = %s)" % (self.io_adapter_dbase_plugin.id, sql_table_dump_query))

    def process_dbi_raw(self, value):
        """
        Converts the DbiRaw value to a string.

        @type value: DbiRaw
        @param value: The value one wants to convert.
        @rtype: str
        @return: The converted value.
        """

        if type(value) == type(dbi.dbiRaw(0)):
            value = str(value)

        return value

    def process_dbi_date(self, value):
        """
        Converts the DbiDate value to a Date object.

        @type value: DbiDate
        @param value: The value one wants to convert.
        @rtype: Date
        @return: The converted value.
        """

        if type(value) == type(dbi.dbiDate(0)):
            if int(value) == -1:
                value = None
            else:
                value = datetime.datetime.fromtimestamp(int(dbi.dbiDate(value)))

        return value

    def process_string(self, value):
        """
        Converts the string to a stripped string or to a null value to
        circunvent dbase's string representation problems.

        @type value: str
        @param value: The value one wants to convert.
        @rtype: str
        @return: The stripped string, or None in case it is an empty string.
        """

        if type(value) == str:
            if string.strip(value) == "":
                value = None
            else:
                value = string.strip(value)

        return value

    def save(self, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in dbase format at the location and with characteristics defined in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure into dbase format.
        """

        self.io_adapter_dbase_plugin.logger.info("[%s] Saving intermediate structure with dbase io adapter" % (self.io_adapter_dbase_plugin.id))

        raise io_adapter_dbase_exceptions.IoAdapterDbaseOperationNotSupported("IoAdapterDbase.save - The intermediate structure dbase io adapter currently does not support the save operation")

class DbfGeneralFieldDef(dbfpy.fields.DbfFieldDef):
    """
    Extends dbfpy by providing support for encoding/decoding general fields.
    """

    typeCode = "G"
    defaultValue = ""

    def decodeValue(self, value):
        return ""

    def encodeValue(self, value):
        return ""

class DbfMemoFieldDef(dbfpy.fields.DbfFieldDef):
    """
    Extends dbfpy by providing support for encoding/decoding memo fields.
    """

    typeCode = "M"
    defaultValue = ""

    def decodeValue(self, value):
        return ""

    def encodeValue(self, value):
        return ""

class DbfDateFieldDef(dbfpy.fields.DbfFieldDef):
    """
    Extends dbfpy by providing support for encoding/decoding date fields.
    """

    typeCode = "D"
    defaultValue = ""

    def decodeValue(self, value):
        return ""

    def encodeValue(self, value):
        return ""
