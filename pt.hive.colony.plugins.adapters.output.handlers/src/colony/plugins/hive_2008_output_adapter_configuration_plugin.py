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

import colony.plugins.plugin_system

class Hive_2008_OutputAdapterConfigurationPlugin(colony.plugins.plugin_system.Plugin):
    """
    Provides a the necessary configuration parameters and functions to convert
    data from the internal structure to the Hive ERP 2008 version
    """

    id = "pt.hive.colony.plugins.adapters.output.configuration.hive_2008"
    name = "Hive 2008 Output Adapter Configuration Plugin"
    short_name = "Hive 2008 Output Adapter Configuration"
    description = "Provides a the necessary configuration parameters and functions to convert data from the internal structure to the Hive ERP 2008 version"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["adapter.output.configuration"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.countrycode_mapper", "1.0.0")]
    events_handled = []
    events_registrable = []
    valid = True

    codebase = None
    """ Base code supplied by this plugin, meant to be accessible only with the methods supplied by the plugin class"""
    
    countrycode_mapper_plugin = None
    
    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global adapters_output_configuration
        import adapters_output_configuration.hive_2008.hive_2008_output_adapter_configuration
        self.codebase = adapters_output_configuration.hive_2008.hive_2008_output_adapter_configuration.Hive_2008_OutputAdapterConfiguration(self)
        
    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.codebase = None
        self.countrycode_mapper_plugin = None

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)
        if colony.plugins.plugin_system.is_capability_or_sub_capability_in_list("country_code_mapper.iso", plugin.capabilities):
            self.countrycode_mapper_plugin = plugin

    def get_configuration_file_paths(self):
        """
        Returns the path to the configuration file provided by this plugin
        
        @return: List of strings with the full paths to the input configuration files
        """
        return self.codebase.get_configuration_file_paths()

    def has_handler(self, handler_name):
        """
        Indicates this configuration plugin has a certain handler function
        
        @param handler_name: Name of the handler function
        @return: Boolean indicating if the requested handler function exists
        """
        return self.codebase.has_handler(handler_name)

    def get_handler(self, handler_name):
        """
        Returns the requested handler function
        
        @param handler_name: Name of the handler function
        @return: Reference to the requested handler function in case it exists
        """
        return self.codebase.get_handler(handler_name)

    def get_work_unit_list(self):
        """
        Gets a list of the work units provided by this configuration plugin
        
        @return: List of strings with the names of the available work units
        """
        return self.codebase.get_work_unit_list()

    def get_entity_name_list(self, work_unit_name):
        """
        Gets a list with the names of the internal entities a certain work unit is meant to process
        
        @param work_unit_name: Name of the work unit one wants to get the respective list of internal entities from
        @return: List of strings with the internal entities that belong to the provided work unit
        """
        return self.codebase.get_entity_name_list(work_unit_name)
