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

__revision__ = "$LastChangedRevision: 2072 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-20 12:02:33 +0100 (Mon, 20 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class DataConverterIntermediateStructureIoAdapterSqliteTestPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Data Converter Intermediate Structure Io Adapter Sqlite Test plugin.
    """

    id = "pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.sqlite_test"
    name = "Data Converter Input Output Sqlite Test Plugin"
    short_name = "Data Converter Input Output Sqlite Test"
    description = "Data Converter Input Output Sqlite Test Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["plugin_test_case_bundle"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.data_converter.intermediate_structure", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.resource_manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    io_adapter_sqlite_test = None
    """ The sqlite input output adapter tests """

    intermediate_structure_plugin = None
    """ The intermediate structure plugin """

    resource_manager_plugin = None
    """ The resource manager plugin """

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global data_converter_intermediate_structure_io_adapter_sqlite
        import data_converter_intermediate_structure_io_adapter_sqlite.test.io_adapter_sqlite_test
        self.io_adapter_sqlite_test = data_converter_intermediate_structure_io_adapter_sqlite.test.io_adapter_sqlite_test.IoAdapterSqliteTest(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.io_adapter_sqlite_test = None
        self.intermediate_structure_plugin = None
        self.resource_manager_plugin = None

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.data_converter.intermediate_structure.io_adapter.sqlite_test", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_plugin_test_case_bundle(self):
        return self.io_adapter_sqlite_test.get_plugin_test_case_bundle()

    def get_intermediate_structure_plugin(self):
        return self.intermediate_structure_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.data_converter.intermediate_structure")
    def set_intermediate_structure_plugin(self, intermediate_structure_plugin):
        self.intermediate_structure_plugin = intermediate_structure_plugin

    def get_resource_manager_plugin(self):
        return self.resource_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin
