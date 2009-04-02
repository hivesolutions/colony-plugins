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

import dbi, odbc, os, stat, string

DBF_EXTENSION = ".dbf"
SLASH = "/"
CONNECTION_STRING = 'Driver={Microsoft Visual FoxPro Driver};SourceType=DBF;SourceDB=%s;Exclusive=No;Collate=Machine;NULL=NO;DELETED=NO;BACKGROUNDFETCH=NO;'

class FoxProInputOutput:

    def __init__(self, foxpro_io_plugin):
        self.foxpro_io_plugin = foxpro_io_plugin

    def get_subdirectories(self, path, returned_path_list):
        """
        Returns a list with paths of directories that are deeper than the one provided

        @param path: The root path from which all subdirectories will be retrieved
        @param returned_path_list: The list where all the paths will be stored. Useful for recursive calls.
        @return: A list with all the subdirectories of the provided path (to deepest node)
        """
        dir_list = os.listdir(path)
        for fname in dir_list:
            full_path = path + SLASH + fname
            mode = os.stat(full_path)[stat.ST_MODE]
            if stat.S_ISDIR(mode):
                returned_path_list.append(full_path)
                self.get_subdirectories(full_path, returned_path_list)
        return returned_path_list

    def connect(self, options):
        """
        Connects to a database in the given path, by discovering all the database files in it and in all it's subdirectories,
        in order to then provide a transparent access to them

        @param options: Map with the connection options
        """
        database_path = options["database_path"]
        table_path_map = {}
        path_list = self.get_subdirectories(database_path, [database_path])
        for path in path_list:
            dir_list = os.listdir(path)
            table_list = []
            for fname in dir_list:
                full_path = path + SLASH + fname
                mode = os.stat(full_path)[stat.ST_MODE]
                if not stat.S_ISDIR(mode) and fname[-4:] == DBF_EXTENSION:
                    table_list.append(fname[:-4])
                    table_path_map[fname[:-4]] = path + SLASH

        return FoxProInputOutputConnection(table_path_map)

# @todo: comment this
class FoxProInputOutputConnection :

    def __init__(self, table_path_map):
        # dictionary that relates table names with the path they are stored in
        self.table_path_map = table_path_map

    def query(self, table_name, column_list = []):
        """
        Returns a set of results from the database.

        @param table_name: Name of the table where one wants to get data from.
        @param column_list: List of columns where one wants to get data from.
        @return: Results of the database query in a dictionary indexed by column name.
        """
        returned_results = []

        if len(column_list):
            table_path = self.table_path_map[table_name]
            connection_string = CONNECTION_STRING % (table_path)
            odbc_connection = odbc.odbc(connection_string)
            cursor = odbc_connection.cursor()

            column_list_string = ""
            for column in column_list[:-1]:
                column_list_string += column + ","
            column_list_string += column_list[-1]
            cursor.execute("SELECT " + column_list_string + " FROM " + table_name)
            results = cursor.fetchall()

            for result in results:
                result_map = {}
                for x in range(len(result)):
                    # fix for null dbiDates
                    if type(result[x]) == type(dbi.dbiDate(0)) and int(result[x]) == -1:
                        result_map[column_list[x]] = None
                    elif type(result[x]) == str:
                        if string.strip(result[x]) == "":
                            result_map[column_list[x]] = None
                        else:
                            result_map[column_list[x]] = string.strip(result[x])
                    else:
                        result_map[column_list[x]] = result[x]
                returned_results.append(result_map)

        return returned_results

    def close(self):
        """
        Closes the connection
        """
        pass
