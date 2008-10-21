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

import string
import os
import stat
import md5

class Hive_2008_OutputAdapterConfiguration:
    """
    Provides a the necessary configuration parameters and functions to convert
    data from the internal structure to the Hive ERP 2008 version
    """
    
    #@todo: move to xml
    workUnitName_domainEntityNameList_map = {"customer" : ["Customer", "Address", "ContactInformation", "User", "Supplier"]}
    """ Dictionary relating work unit name with the a list of names of the domain entities that must be processed for the work unit to be complete """
    
    parent_plugin = None
    """ Reference to the plugin that owns this code """
    
    def __init__(self, parent_plugin):
        """
        Class constructor
        
        @param parent_plugin: Reference to the plugin that owns this code
        """
        self.parent_plugin = parent_plugin
    
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
    
    def get_work_unit_list(self):
        """
        Gets a list of the work units provided by this configuration plugin
        
        @return: List of strings with the names of the available work units
        """
        return self.workUnitName_domainEntityNameList_map.keys()
    
    def get_entity_name_list(self, work_unit_name):
        """
        Gets a list with the names of the internal entities a certain work unit is meant to process
        
        @param work_unit_name: Name of the work unit one wants to get the respective list of internal entities from
        @return: List of strings with the internal entities that belong to the provided work unit
        """
        return self.workUnitName_domainEntityNameList_map[work_unit_name]
    
    ###### DOMAIN ENTITY HANDLERS ######
        
    ###### ATTRIBUTE HANDLERS ######
    
    def domain_attribute_handler_value_to_md5(self, arguments):
        """
        Returns the MD5 hash of a certain value
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """
        value = arguments[0]
        
        if value:
            value = md5.new(value).digest()
        
        return value

    def domain_attribute_handler_name(self, arguments):
        """
        Concatenates the name and surname fields
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """
        value = arguments[0]
        
        internal_entity_instance = arguments[1]
        if internal_entity_instance.has_field("surname"): 
            value += " " + internal_entity_instance.surname
        return value
    
    def domain_attribute_handler_observations(self, arguments):
        """
        Concatenates the observation field
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """
        value = arguments[0]
        
        internal_entity_instance = arguments[1]
        if internal_entity_instance.has_field("observation"): 
            value += " " + internal_entity_instance.observation.observation
        return value
    
    def domain_attribute_handler_profession(self, arguments):
        """
        Retrieves the profession name from its reference
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """
        value = arguments[0]
        
        if value:
            value = value.professionName
        return value

    def domain_attribute_handler_string_to_lowercase(self, arguments):
        """
        Converts a string to lowercase
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """
        value = arguments[0]
        
        if value:
            value = string.lower(value)
        return value

    def domain_attribute_handler_country(self, arguments):
        """
        Converts a country name to it's country code
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """
        countrycode_mapper_plugin = self.parent_plugin.countrycode_mapper_plugin
        
        value = arguments[0]
        
        if value:
            value = countrycode_mapper_plugin.get_country_code(value.countryName)
        return value
