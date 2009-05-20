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

class DataConverterIntermediateStructurePlugin(colony.plugins.plugin_system.Plugin):
    """
    Provides an intermediate structure used to hold the results of each conversion step.
    """

    id = "pt.hive.colony.plugins.data_converter.intermediate_structure"
    name = "Data Converter Intermediate Structure plugin"
    short_name = "Data Converter Intermediate Structure"
    description = "Provides an intermediate structure the data converter can use to hold the results of each migration step"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = []
    capabilities_allowed = ["data_converter_intermediate_structure_io_adapter"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.log", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.resource_manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    io_adapter_plugins = []
    """ Input output adapter plugins for the intermediate structure """

    logger_plugin = None
    """ Logger plugin """

    resource_manager_plugin = None
    """ Resource manager plugin """

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global data_converter_intermediate_structure
        import data_converter_intermediate_structure.intermediate_structure.intermediate_structure_system

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.io_adapter_plugins = []
        self.logger_plugin = None
        self.resource_manager_plugin = None

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.data_converter.intermediate_structure", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.data_converter.intermediate_structure", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.data_converter.intermediate_structure", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_intermediate_structure(self):
        intermediate_structure = data_converter_intermediate_structure.intermediate_structure.intermediate_structure_system.IntermediateStructure(self)
        return intermediate_structure

    @colony.plugins.decorators.load_allowed_capability("data_converter_intermediate_structure_io_adapter")
    def data_converter_intermediate_structure_io_adapter_load_allowed(self, plugin, capability):
        self.io_adapter_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("data_converter_intermediate_structure_io_adapter")
    def data_converter_intermediate_structure_io_adapter_unload_allowed(self, plugin, capability):
        self.io_adapter_plugins.remove(plugin)

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
