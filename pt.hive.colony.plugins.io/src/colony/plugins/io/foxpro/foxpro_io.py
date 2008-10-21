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

__revision__ = "$LastChangedRevision: 2112 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 15:23:46 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import dbi, odbc, os, stat, string

DBF_EXTENSION = ".dbf"
SLASH = "/"

class FoxProInputOutput:

    table_path_map = {}
    """ Dictionary that relates table names with the path they are stored in """

    connection_string = 'Driver={Microsoft Visual FoxPro Driver};SourceType=DBF;SourceDB=%s;Exclusive=No;Collate=Machine;NULL=NO;DELETED=NO;BACKGROUNDFETCH=NO;'
    """ Default connection string for FoxPro. Expects the path to the database files as a parameter. """

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

    def connect_database(self, database_path):
        """
        Connects to a database in the given path, by discovering all the database files in it and in all it's subdirectories,
        in order to then provide a transparent access to them
        
        @param database_path: Path to the directory where all the database files are stored (they may be there or under any subdirectory)
        """
        self.table_path_map = {}
        path_list = self.get_subdirectories(database_path, [database_path])
        for path in path_list:
            dir_list = os.listdir(path)
            table_list = []
            for fname in dir_list:
                full_path = path + SLASH + fname
                mode = os.stat(full_path)[stat.ST_MODE]
                if not stat.S_ISDIR(mode) and fname[-4:] == DBF_EXTENSION:
                    table_list.append(fname[:-4])
                    self.table_path_map[fname[:-4]] = path + SLASH

    def connect_table(self, table_name):
        """
        Returns a connection to the specified table
        
        @param table_name: Name of the table to which you want to connect to
        """
        return odbc.odbc(self.connection_string % (self.table_path_map[table_name])).cursor()

    def flush(self):
        """
        Flushes all the previous operations down the stream of the I/O plugin
        """
        return

    def delete(self, object):
        """
        Deletes an object from the datastore
        
        @param object: Entity instance to delete from the datastore
        """
        return

    def save(self, object):
        """
        Saves an object to the datastore
		
        @param object: Entity instance to save to the datastore
        """
        return None

    def query(self, table_name, column_list):
        """
        Returns a set of results from the datastore
        
        @param table_name: Name of the table where one wants to get data from
        @param column_list: List of columns where one wants to get data from
        @return: Results of the database query in a dictionary indexed by column name
        """
        cursor = self.connect_table(table_name)
        column_list_string = ""
        for column in column_list[:-1]:
            column_list_string += column + ","
        column_list_string += column_list[-1]
        cursor.execute("SELECT " + column_list_string + " FROM " + table_name)
        results = cursor.fetchall()
        returned_results = []
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

    def initialize(self, database_path):
        """
        Sets information and runs required methods for this I/O plugin to be operational
        
        @param database_path: Root path of the foxpro database
        """
        self.connect_database(database_path)
