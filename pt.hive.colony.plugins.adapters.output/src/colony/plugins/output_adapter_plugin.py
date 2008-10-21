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

__revision__ = "$LastChangedRevision: 2100 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 13:24:05 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class OutputAdapterPlugin(colony.plugins.plugin_system.Plugin):
    """
    Generic output adapter
    """

    id = "pt.hive.colony.plugins.adapters.output"
    name = "Output Adapter Plugin"
    short_name = "Output Adapter"
    description = "Provides an output adapter using SqlAlchemy and version 1.0.0 of the domain"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["adapter.output"]
    capabilities_allowed = ["adapter.output.configuration"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.io.sqlalchemy", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.log", "1.0.0")]
    events_handled = ["output_configuration_changed"]
    events_registrable = []
    valid = True

    codebase = None
    """ Base code supplied by this plugin, meant to be accessible only with the methods supplied by the plugin class"""

    sqlalchemy_plugin = None
    """ Plugin to access SqlAlchemy """

    configuration_plugin = None
    """ Plugin that contains the configuration properties for this plugin to act on """

    logger_plugin = None
    """ Reference to the logger plugin """

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global adapters_output
        import adapters_output.output_adapter
        self.codebase = adapters_output.output_adapter.OutputAdapter(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.codebase = None
        self.sqlalchemy_plugin = None
        self.configuration_plugin = None

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)
        if colony.plugins.plugin_system.is_capability_or_sub_capability_in_list("adapter.output.configuration", plugin.capabilities):
            self.configuration_plugin = plugin

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)
        if colony.plugins.plugin_system.is_capability_or_sub_capability_in_list("adapter.output.configuration", plugin.capabilities):
            self.configuration_plugin = None

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)
        if colony.plugins.plugin_system.is_capability_or_sub_capability_in_list("io.sqlalchemy", plugin.capabilities):
            self.sqlalchemy_plugin = plugin
        elif colony.plugins.plugin_system.is_capability_or_sub_capability_in_list("log", plugin.capabilities):
            self.logger_plugin = plugin

    def process_query(self, task, args):
        """
        Processes a query on the output data source
        
        @param task: Task monitoring object used to inform the status of the query
        @param args: Dictionary with configuration parameters for the query
        @return: The query's results, if any.
        """
        self.codebase.process_convert(task, args)
