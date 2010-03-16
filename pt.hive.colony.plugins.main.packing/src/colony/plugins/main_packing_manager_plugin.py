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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 429 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-21 13:03:27 +0000 (Sex, 21 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class MainPackingManagerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Packing Manager Main plugin.
    """

    id = "pt.hive.colony.plugins.main.packing.manager"
    name = "Packing Manager Main Plugin"
    short_name = "Packing Manager Main"
    description = "Packing Manager Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["packing_manager"]
    capabilities_allowed = ["packing_service"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["main_packing.manager.main_packing_manager_exceptions", "main_packing.manager.main_packing_manager_system"]

    main_packing_manager = None

    packing_service_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_packing
        import main_packing.manager.main_packing_manager_system
        self.main_packing_manager = main_packing.manager.main_packing_manager_system.MainPackingManager(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.main.packing.manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.main.packing.manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def pack_directory(self, directory_path, properties, service_name):
        """
        Packs the directory using the provided service name.

        @type directory_path: String
        @param directory_path: The path to the directory to be used
        in the packing.
        @type properties: Dictionary
        @param properties: The properties for the packing.
        @type service_name: String
        @param service_name: The name of the service to be used for packing.
        """

        self.main_packing_manager.pack_directory(directory_path, properties, service_name)

    def pack_files(self, file_paths_list, properties, service_name):
        """
        Packs the given files using the provided service name.

        @type file_paths_list: List
        @param file_paths_list: The list of file paths to be used in the packing.
        @type properties: Dictionary
        @param properties: The properties for the packing.
        @type service_name: String
        @param service_name: The name of the service to be used for packing.
        """

        self.main_packing_manager.pack_files(file_paths_list, properties, service_name)

    def unpack_files(self, file_paths_list, properties, service_name):
        """
        Unpacks the given files using the provided service name.

        @type file_paths_list: List
        @param file_paths_list: The list of file paths to be used in the unpacking.
        @type properties: Dictionary
        @param properties: The properties for the unpacking.
        @type service_name: String
        @param service_name: The name of the service to be used for unpacking.
        """

        self.main_packing_manager.unpack_files(file_paths_list, properties, service_name)

    @colony.plugins.decorators.load_allowed_capability("packing_service")
    def packing_service_capability_load_allowed(self, plugin, capability):
        self.packing_service_plugins.append(plugin)
        self.main_packing_manager.packing_service_load(plugin)

    @colony.plugins.decorators.unload_allowed_capability("packing_service")
    def packing_service_capability_unload_allowed(self, plugin, capability):
        self.packing_service_plugins.remove(plugin)
        self.main_packing_manager.packing_service_unload(plugin)
