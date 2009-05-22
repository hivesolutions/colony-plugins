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
import os.path
import dbfpy.dbf
import dbfpy.fields

import io_adapter_dbase_exceptions

DBASE_EXTENSION = ".dbf"

class IoAdapterDbase:
    """
    Input output adapter used to serialize data converter intermediate structures to dbase format.
    """

    def __init__(self, io_adapter_dbase_plugin):
        """
        Class constructor.

        @type io_adapter_dbase_plugin: IoAdapterDbasePlugin
        @param io_adapter_dbase_plugin: Input output adapter dbase plugin.
        """

        self.io_adapter_dbase_plugin = io_adapter_dbase_plugin

        # adds support for memo and general datatypes to dbfpy
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
                        table_file_path = os.path.join(root_path, file_name)
                        table_name_path_map[table_name] = table_file_path

        # for each table open a connection to it and dump the table's contents to the intermediate structure
        table_names = table_name_path_map.keys()

        self.io_adapter_dbase_plugin.logger.info("[%s] Loading %d tables with dbase io adapter" % (self.io_adapter_dbase_plugin.id, len(table_names)))

        # copies every table to the intermediate structure
        for table_index in range(len(table_names)):
            table_name = table_names[table_index]

            self.io_adapter_dbase_plugin.logger.info("[%s] Loading table '%s' (%d/%d) with dbase io adapter" % (self.io_adapter_dbase_plugin.id, table_name, table_index, len(table_names)))

            # retrieves the file path where the table is located
            table_file_path = table_name_path_map[table_name]

            # retrieves the tables records
            records = dbfpy.dbf.Dbf(table_file_path)

            # creates an entity for each record and adds it to the intermediate structure
            for record_index in range(len(records)):
                record = records[record_index]
                record_map = record.asDict()
                for column_name in record_map:
                    field_value = record_map[column_name]
                    entity = intermediate_structure.create_entity(column_name)
                    entity.set_attribute(column_name, field_value)

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
    defaultValue = " " * 10
    length = 10

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
    # "yyyymmdd" gives us 8 characters
    length = 8

    def decodeValue(self, value):
        return ""

    def encodeValue(self, value):
        return ""
