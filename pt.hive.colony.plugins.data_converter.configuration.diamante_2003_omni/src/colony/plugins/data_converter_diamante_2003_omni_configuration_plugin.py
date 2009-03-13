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

__revision__ = "$LastChangedRevision: 1805 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-03-10 08:56:01 +0000 (Tue, 10 Mar 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class DataConverterDiamante2003OmniConfigurationPlugin(colony.plugins.plugin_system.Plugin):
    """
    Provides access to and information on the loaded Diamante migration logic plugins
    """
    
    id = "pt.hive.colony.plugins.data_converter.configuration.diamante_2003_omni"
    name = "Data Converter Diamante2003-Omni Configuration Plugin"
    short_name = "Data Converter Diamante2003-Omni Configuration"
    description = "Provides configuration resources for the data converter to be able to convert data from a Diamante 2003 installation to the Omni ERP"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["data_converter_configuration"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global data_converter_diamante_2003_omni_configuration
        import data_converter_diamante_2003_omni_configuration.adapter.input.configuration.diamante_2003.dia_2003_input_adapter_configuration
        import data_converter_diamante_2003_omni_configuration.adapter.output.configuration.omni.omni_output_adapter_configuration
        self.data_converter_diamante_2003_input_adapter_configuration = data_converter_diamante_2003_omni_configuration.adapter.input.configuration.diamante_2003.dia_2003_input_adapter_configuration.Diamante2003InputAdapterConfiguration(self)
        self.data_converter_omni_output_adapter_configuration = data_converter_diamante_2003_omni_configuration.adapter.output.configuration.omni.omni_output_adapter_configuration.OmniOutputAdapterConfiguration(self)
        
    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)
            
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)
    
    def get_input_adapter_configuration(self):
        """
        Returns the configuration for the data converter's input adapter.
        
        @return: Data converter input adapter configuration object.
        """
        return self.data_converter_diamante_2003_input_adapter_configuration

    def get_output_adapter_configuration(self):
        """
        Returns the configuration for the data converter's output adapter.
        
        @return: Data converter output adapter configuration object.
        """
        return self.data_converter_omni_output_adapter_configuration
