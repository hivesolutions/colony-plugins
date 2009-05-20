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
    Provides a means to convert data from one medium and schema to another.
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
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.data_converter.intermediate_structure", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.tasks.task_manager", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.log", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.resource_manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    data_converter = None
    """ Data converter backend """

    console_data_converter = None
    """ Console for the data converter """

    intermediate_structure_plugin = None
    """ Intermediate structure plugin """

    logger_plugin = None
    """ Logger plugin """

    task_manager_plugin = None
    """ Task manager plugin """

    resource_manager_plugin = None
    """ Resource manager plugin """

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global data_converter
        import data_converter.data_converter_system
        import data_converter.console_data_converter

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.data_converter = data_converter.data_converter_system.DataConverter(self)
        self.console_data_converter = data_converter.console_data_converter.ConsoleDataConverter(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.data_converter = None
        self.console_data_converter = None
        self.intermediate_structure_plugin = None
        self.logger_plugin = None
        self.task_manager_plugin = None
        self.resource_manager_plugin = None

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

    def get_console_extension_name(self):
        return self.console_data_converter.get_console_extension_name()

    def get_all_commands(self):
        return self.console_data_converter.get_all_commands()

    def get_handler_command(self, command):
        return self.console_data_converter.get_handler_command(command)

    def get_help(self):
        return self.console_data_converter.get_help()

    def convert_data(self, input_options, output_options, conversion_options):
        """
        Converts data from one intermediate structure to another transforming its schema along the way.

        @type input_options: Dictionary
        @param input_options: Options used to determine how the input intermediate structure should retrieve its data.
        @type output_options: Dictionary
        @param output_options: Options used to determine how the output intermediate structure should save its data.
        @type conversion_options: Dictionary
        @param conversion_options: Options used to determine how to perform the conversion process.
        """

        self.data_converter.convert_data(input_options, output_options, conversion_options)

    def get_intermediate_structure_plugin(self):
        return self.intermediate_structure_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.data_converter.intermediate_structure")
    def set_intermediate_structure_plugin(self, intermediate_structure_plugin):
        self.intermediate_structure_plugin = intermediate_structure_plugin

    def get_task_manager_plugin(self):
        return self.task_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.tasks.task_manager")
    def set_task_manager_plugin(self, task_manager_plugin):
        self.task_manager_plugin = task_manager_plugin

    def get_logger_plugin(self):
        return self.logger_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.log")
    def set_logger_plugin(self, logger_plugin):
        self.logger_plugin = logger_plugin

    def get_resource_manager_plugin(self):
        return self.resource_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin
