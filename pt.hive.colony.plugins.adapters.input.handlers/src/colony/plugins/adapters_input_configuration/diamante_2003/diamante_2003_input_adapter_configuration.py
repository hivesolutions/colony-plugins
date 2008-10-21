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

__revision__ = "$LastChangedRevision: 2099 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 13:18:44 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import string
import datetime
import os
import stat

class Diamante_2003_InputAdapterConfiguration:
    """
    Provides a the necessary configuration parameters and functions to convert
    data from the Diamante 2003 version to the intermediate internal structure
    """

    parent_plugin = None
    """ Reference to the plugin that owns this code """

    #@todo: move this to xml file
    work_unit_table_list_map = {"customer" : ["clientes", "paises", "profissa", "observa", "zonas", "password", "forneced"]} 
    """ Dictionary relating work unit name with a list of the database table names that need to be processed for the work unit to be complete """

    def __init__(self, parent_plugin):
        self.parent_plugin = parent_plugin

    def get_work_unit_list(self):
        """
        Gets a list of the work units provided by this configuration plugin
        
        @return: List of strings with the names of the available work units
        """

        return self.work_unit_table_list_map.keys()

    def get_table_list(self, work_unit_name):
        """
        Gets a list with the names of the tables a certain work unit is meant to process
        
        @param work_unit_name: Name of the work unit one wants to get the respective list of tables from
        @return: List of strings with the tables that belong to the provided work unit
        """

        return self.work_unit_table_list_map[work_unit_name] 

    def get_configuration_file_paths(self):
        """
        Returns the path to the configuration file provided by this plugin
        
        @return: String with the full path to the input configuration file
        """

        file_paths = []
        path = os.path.dirname(__file__) + "/xml/"
        dir_list = os.listdir(path)
        for fname in dir_list:
            full_path = path + fname
            mode = os.stat(full_path)[stat.ST_MODE]
            if not stat.S_ISDIR(mode):
                file_paths.append(full_path)
        return file_paths

    def has_handler(self, handler_name):
        """
        Indicates this configuration plugin has a certain handler function
        
        @param handler_name: Name of the handler function
        @return: Boolean indicating if the requested handler function exists
        """

        if self.get_handler(handler_name) == None:
            return False
        return True

    def get_handler(self, handler_name):
        """
        Returns the requested handler function
        
        @param handler_name: Name of the handler function
        @return: Reference to the requested handler function in case it exists
        """

        return getattr(self, handler_name)

    def column_handler_timestamp_to_datetime(self, arguments):
        """
        Converts a timestamp to a datetime object
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """

        value = arguments[0]
        
        if value:
            value = datetime.datetime.fromtimestamp(int(value))
        return value

    def column_handler_string_to_lowercase(self, arguments):
        """
        Converts a string to lowercase
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """

        value = arguments[0]
        
        if value:
            value = string.lower(value)
        return value
    
    def column_handler_diamante_encryption_to_plaintext(self, arguments):
        """
        Decrypts a Diamante 2003 encoded string
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """

        value = arguments[0]

        if value:
            newstr = ""
            for char in value:
                ascii_value = ord(char)
                decoded_ascii_value = 255 - ascii_value
                decoded_char = chr(decoded_ascii_value)
                newstr += decoded_char
            value = newstr
        return value

    #@todo: this function should be on the output adapter instead
    def column_handler_diamante_gender_id_to_hive_gender_id(self, arguments):
        """
        Converts a Diamante 2003 gender enumeration to a Hive gender enumeration
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """

        value = arguments[0]

        DIAMANTE_GENDER_MALE = "1"
        DIAMANTE_GENDER_FEMALE = "2"
        DIAMANTE_GENDER_NEUTRAL = "3"
        HIVE_GENDER_MALE = "0"
        HIVE_GENDER_FEMALE = "1"
        HIVE_GENDER_NEUTRAL = "2"

        if value == DIAMANTE_GENDER_MALE:
            return HIVE_GENDER_MALE
        elif value == DIAMANTE_GENDER_FEMALE:
            return HIVE_GENDER_FEMALE
        elif value == DIAMANTE_GENDER_NEUTRAL:
            return HIVE_GENDER_NEUTRAL
