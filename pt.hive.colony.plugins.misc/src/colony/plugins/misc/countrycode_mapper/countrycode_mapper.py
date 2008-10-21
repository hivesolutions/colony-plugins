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

FILE_PATH = "resources/iso_country_codes.dat"

class CountryCodeMapper:
    
    code_country_map = {}
    country_code_map = {}
    
    def __init__(self):
        self.reset_state()
    
    def reset_state(self):
        """
        Resets the objects attributes to their original state
        """
        self.code_country_map = {}
        self.country_code_map  = {}
    
    #@todo: find better way to store country information
    def load_country_information(self):
        """
        Loads information about country names and their respective iso codes
        """
        countries_file = open(os.path.join(os.path.dirname(__file__), FILE_PATH), "r")
        lines = countries_file.readlines()
        for line in lines:
            tokens = line.split(",")
            code = tokens[0]
            country_list = []
            for token in tokens[1:]:
                if token[-1] == "\n":
                    token = token[0:-1]
                self.country_code_map[token] = code
                country_list.append(token)
            self.code_country_map[code] = country_list
        countries_file.close()
    
    def get_country_name(self, country_code):
        """
        Returns the country name that corresponds to the given country code
        
        @param country_code: The country code of the country whose name one wants to retrieve
        @return: Country name that corresponds to the provided country code
        """
        return self.code_country_map[string.lower(string.strip(country_code))]
    
    def get_country_code(self, country_name):
        """
        Returns the country code that corresponds to the given country name
        
        @param country_name: The country name of the country whose code one wants to retrieve
        @return: Country code that corresponds to the provided country name
        """
        return self.country_code_map[string.lower(string.strip(country_name))]
