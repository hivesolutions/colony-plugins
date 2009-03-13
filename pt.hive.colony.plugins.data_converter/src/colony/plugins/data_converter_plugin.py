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

class DataConverterPlugin(colony.plugins.plugin_system.Plugin):
    """
    Provides a means to convert data from one medium and schema to another
    """
    
    id = "pt.hive.colony.plugins.data_converter"
    name = "Data converter plugin"
    short_name = "Data converter"
    description = "Provides plugin to convert data from one medium and schema to another"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["console_command_extension"]
    capabilities_allowed = ["io", "data_converter_configuration", "data_converter_observer"]
    dependencies = [colony.plugins.plugin_system.PackageDependency(
                    "SQL Alchemy O/R mapper", "sqlalchemy", "0.4.x", "http://www.sqlalchemy.org"),
                    colony.plugins.plugin_system.PackageDependency(
                    "MySQL-Python", "MySQLdb", "1.2.x", "http://mysql-python.sourceforge.net"), 
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.tasks.task_manager", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.log", "1.0.0")]
    events_handled = []
    events_registrable = []

    io_plugins = []
    """ Input/output adapter plugins """
    
    logger_plugin = None
    """ Logger plugin """
    
    task_manager_plugin = None
    """ Task manager plugin """
    
    data_converter_configuration_plugins = []
    """ Plugins providing data conversion configurations """
    
    data_converter_observer_plugins = []
    """ Plugins that want to observe the conversion process """

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global data_converter
        import data_converter.adapter.input.input_adapter
        import data_converter.adapter.output.output_adapter
        import data_converter.data_converter_system
        import data_converter.console_data_converter
      
    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.data_converter = data_converter.data_converter_system.DataConverter(self)
        self.console_data_converter = data_converter.console_data_converter.ConsoleDataConverter(self)
        self.input_adapter = data_converter.adapter.input.input_adapter.InputAdapter(self)
        self.output_adapter = data_converter.adapter.output.output_adapter.OutputAdapter(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.data_converter = None
        self.console_data_converter = None
        self.input_adapter = None
        self.output_adapter = None

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.data_converter", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.data_converter", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)
        
    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.data_converter", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)   
            
    def convert(self, data_converter_configuration_plugin_id):
        """
        Converts data from one source medium and schema to another.
        
        @param data_converter_configuration_plugin_id: Unique identifier for the plugin that provides the necessary configurations for the conversion.
        """
        self.data_converter.convert(data_converter_configuration_plugin_id)
        
    def get_console_extension_name(self):
        return self.console_data_converter.get_console_extension_name()

    def get_all_commands(self):
        return self.console_data_converter.get_all_commands()

    def get_handler_command(self, command):
        return self.console_data_converter.get_handler_command(command)

    def get_help(self):
        return self.console_data_converter.get_help()
                        
    @colony.plugins.decorators.load_allowed_capability("io")
    def io_load_allowed(self, plugin, capability):
        self.io_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("io")
    def io_unload_allowed(self, plugin, capability):
        self.io_plugins.remove(plugin)
        
    @colony.plugins.decorators.load_allowed_capability("data_converter_configuration")
    def data_converter_configuration_load_allowed(self, plugin, capability):
        self.data_converter_configuration_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("data_converter_configuration")
    def data_converter_configuration_unload_allowed(self, plugin, capability):
        self.data_converter_configuration_plugins.remove(plugin)
        
    @colony.plugins.decorators.load_allowed_capability("data_converter_observer")
    def data_converter_observer_load_allowed(self, plugin, capability):
        self.data_converter_observer_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("data_converter_observer")
    def data_converter_observer_unload_allowed(self, plugin, capability):
        self.data_converter_observer_plugins.remove(plugin)

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.tasks.task_manager")
    def set_task_manager_plugin(self, task_manager_plugin):
        self.task_manager_plugin = task_manager_plugin
        
    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.log")
    def set_logger_plugin(self, logger_plugin):
        self.logger_plugin = logger_plugin
