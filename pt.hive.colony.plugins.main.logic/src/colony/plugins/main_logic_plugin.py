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

class MainLogicPlugin(colony.plugins.plugin_system.Plugin):
    """
    Provides access to and information on the loaded Diamante migration logic plugins
    """
    
    id = "pt.hive.colony.plugins.main.logic"
    name = "Main Logic Plugin"
    short_name = "Main Logic"
    description = "Provides the main engine to access the logic"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["console_command_extension", "main_logic"]
    capabilities_allowed = ["adapter.input", "adapter.output"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.tasks.task_manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    logic = None
    """ Base code supplied by this plugin, meant to be accessible only with the methods supplied by the plugin class"""
    input_adapters = []
    """ Input adapter plugins available to the conversion logic """
    output_adapters = []
    """ Output adapter plugins available to the conversion logic """
    task_manager_plugin = None
    """ Task manager plugin """

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_logic
        import main_logic.main_logic
        import main_logic.console_main_logic
        self.logic = main_logic.main_logic.MainLogic(self)
        self.console_main_logic = main_logic.console_main_logic.ConsoleMainLogic(self)
        
    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.logic = None
        self.input_adapters = []
        self.output_adapters = []
        self.internal_structure_visualizer_plugin = None
        self.task_manager_plugin = None
    
    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)
        
        if capability == "adapter.input":
            self.input_adapters.append(plugin)
        elif capability == "adapter.output":
            self.output_adapters.append(plugin)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

        if capability == "adapter.input":
            self.input_adapters.remove(plugin)
        elif capability == "adapter.output":
            self.output_adapters.remove(plugin)
            
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)
        if colony.plugins.plugin_system.is_capability_or_sub_capability_in_list("task_manager", plugin.capabilities):
            self.task_manager_plugin = plugin
            
    def process_query(self, args):
        self.logic.process_query(args)
        
    def get_console_extension_name(self):
        return self.console_main_logic.get_console_extension_name()

    def get_all_commands(self):
        return self.console_main_logic.get_all_commands()

    def get_handler_command(self, command):
        return self.console_main_logic.get_handler_command(command)

    def get_help(self):
        return self.console_main_logic.get_help()
