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

__revision__ = "$LastChangedRevision: 2096 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 13:02:08 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class CountryCodeMapperPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Country Code Mapper plugin
    """

    id = "pt.hive.colony.plugins.misc.countrycode_mapper"
    name = "Country Code Mapper Plugin"
    short_name = "Country Code Mapper"
    description = "Provides a mapping between country names and country codes, in both directions"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["country_code_mapper.iso"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []

    logic = None
    
    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.countrycode_mapper.countrycode_mapper
        self.logic = misc.countrycode_mapper.countrycode_mapper.CountryCodeMapper()
        self.logic.reset_state()
        self.logic.load_country_information()

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)    

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.logic.reset_state()
        self.logic = None

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_country_name(self, country_code):
        """
        Returns a country name by providing it's iso country code
        
        @param country_code: ISO country code (ex: Portugal's iso country code is pt)
        @return: Name of the country specified by the provided iso country code
        """
        return self.logic.get_country_name(country_code)
    
    def get_country_code(self, country_name):
        """
        Returns a country code by providing a country name
        
        @param country_name: Name of the country one wants to get the ISO country code for
        @return: ISO country code for the specified country name
        """
        return self.logic.get_country_code(country_name)
