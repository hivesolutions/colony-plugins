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
import colony.plugins.decorators

class DataConverterPlugin(colony.plugins.plugin_system.Plugin):
    """
    Provides a means to convert data from one medium and schema to another.
    """

    id = "pt.hive.colony.plugins.data_converter"
    name = "Data Converter plugin"
    short_name = "Data Converter"
    description = "Provides plugin to convert data from one medium and schema to another"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["console_command_extension"]
    capabilities_allowed = ["data_converter_io_adapter",
                            "data_converter_configuration"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.log", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.resources.resource_manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    data_converter = None
    """ Data converter backend """

    console_data_converter = None
    """ Data converter console """

    io_adapter_plugins = []
    """ Input output adapter plugins """

    configuration_plugins = []
    """ Data converter configuration plugins """

    logger_plugin = None
    """ Logger plugin """

    resource_manager_plugin = None
    """ Resource manager plugin """

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global data_converter
        import data_converter.data_converter.data_converter_system
        import data_converter.data_converter.console_data_converter
        self.data_converter = data_converter.data_converter.data_converter_system.DataConverter(self)
        self.console_data_converter = data_converter.data_converter.console_data_converter.ConsoleDataConverter(self)
        self.data_converter.load_data_converter()

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.data_converter = None
        self.io_adapter_plugins = []
        self.configuration_plugins = []
        self.logger_plugin = None
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

    def get_loaded_configuration_ids(self):
        """
        Retrieves the unique identifiers for the currently loaded configurations.

        @rtype: List
        @return: List with the unique identifiers for the loaded configurations.
        """

        return self.data_converter.get_loaded_configuration_ids()

    def get_loaded_configuration(self, configuration_id):
        """
        Retrieves the currently loaded data converter configuration.

        @type configuration_id: int
        @param configuration_id: Unique identifier for the data converter configuration
        one wants to retrieve.
        @rtype: DataConverterConfiguration
        @return: Data converter configuration one wants to retrieve.
        """

        return self.data_converter.get_loaded_configuration(configuration_id)

    def load_configuration(self, configuration_plugin_id):
        """
        Unique identifier for the data converter configuration one wants to load.

        @type configuration_plugin_id: String
        @param configuration_plugin_id: Unique identifier for the
        data converter plugin one wants to load the configuration from.
        """

        self.data_converter.load_configuration(configuration_plugin_id)

    def unload_configuration(self, configuration_id):
        """
        Unique identifier for the data converter configuration one wants to unload.

        @type configuration_id: int
        @param configuration_id: Unique identifier for the data converter configuration
        one wants to unload.
        """

        self.data_converter.unload_configuration(configuration_id)

    def create_intermediate_structure(self, configuration_map):
        """
        Creates an intermediate structure instance.

        @type configuration_map: Dictionary
        @param configuration_map: Map defining the intermediate structure's schema.
        @rtype: IntermediateStructure
        @return: The created intermediate structure.
        """

        return self.data_converter.create_intermediate_structure(configuration_map)

    def load_intermediate_structure(self, intermediate_structure, io_adapter_plugin_id, options):
        """
        Populates the intermediate structure with data retrieved from the source
        specified in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to load the data into.
        @type io_adapter_plugin_id: String
        @param io_adapter_plugin_id: Unique identifier for the input output adapter
        plugin one wants to use to save intermediate structure.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the provided
        intermediate structure.
        @rtype: IntermediateStructure
        @return: The loaded intermediate structure.
        """

        return self.data_converter.load_intermediate_structure(intermediate_structure, io_adapter_plugin_id, options)

    def save_intermediate_structure(self, intermediate_structure, io_adapter_plugin_id, options):
        """
        Saves the intermediate structure to a file in format at the location and
        with characteristics defined in the options.

        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type io_adapter_plugin_id: String
        @param io_adapter_plugin_id: Unique identifier for the input output adapter
        plugin one wants to use to save intermediate structure.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate structure.
        """

        self.data_converter.save_intermediate_structure(intermediate_structure, io_adapter_plugin_id, options)

    def convert_data(self, configuration_id):
        """
        Converts data from one intermediate structure to another transforming
        its schema along the way.

        @type configuration_id: int
        @param configuration_id: Unique identifier for the data converter configuration
        one wants to retrieve.
        @rtype: IntermediateStructure
        @return: Output intermediate structure.
        """

        return self.data_converter.convert_data(configuration_id)

    @colony.plugins.decorators.load_allowed_capability("data_converter_io_adapter")
    def data_converter_io_adapter_load_allowed(self, plugin, capability):
        self.io_adapter_plugins.append(plugin)
        self.data_converter.add_io_adapter_plugin(plugin)

    @colony.plugins.decorators.unload_allowed_capability("data_converter_io_adapter")
    def data_converter_io_adapter_unload_allowed(self, plugin, capability):
        self.io_adapter_plugins.remove(plugin)
        self.data_converter.remove_io_adapter_plugin(plugin)

    @colony.plugins.decorators.load_allowed_capability("data_converter_configuration")
    def data_converter_configuration_load_allowed(self, plugin, capability):
        self.configuration_plugins.append(plugin)
        self.data_converter.add_configuration_plugin(plugin)

    @colony.plugins.decorators.unload_allowed_capability("data_converter_configuration")
    def data_converter_configuration_unload_allowed(self, plugin, capability):
        self.configuration_plugins.remove(plugin)
        self.data_converter.remove_configuration_plugin(plugin)

    def get_logger_plugin(self):
        return self.logger_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.log")
    def set_logger_plugin(self, logger_plugin):
        self.logger_plugin = logger_plugin

    def get_resource_manager_plugin(self):
        return self.resource_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.resources.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin

    def get_data_converter_configuration_tokens(self):
        return self.data_converter.get_data_converter_configuration_tokens()
