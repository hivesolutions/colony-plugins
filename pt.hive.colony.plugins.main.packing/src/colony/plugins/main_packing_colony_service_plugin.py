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

__author__ = "João Magalhães <joamag@hive.pt>"
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

class MainPackingColonyServicePlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Packing Colony Service Main plugin.
    """

    id = "pt.hive.colony.plugins.main.packing.colony_service"
    name = "Packing Colony Service Main Plugin"
    short_name = "Packing Colony Service Main"
    description = "Packing Colony Service Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["packing_service"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["main_packing.colony_service.main_packing_colony_service_system"]

    main_packing_colony_service = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_packing
        import main_packing.colony_service.main_packing_colony_service_system
        self.main_packing_manager = main_packing.colony_service.main_packing_colony_service_system.MainPackingColonyService(self)

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

    def get_service_name(self):
        """
        Retrieves the service name.

        @rtype: String
        @return: The service name.
        """

        return self.main_packing_colony_service.get_service_name()

    def pack_directory(self, directory_path, recursive):
        """
        Packs the directory using the service.

        @type directory_path: String
        @param directory_path: The path to the directory to be used
        in the packing.
        @type recursive: bool
        @param recursive: If the packing should be made recursive.
        """

        self.main_packing_colony_service.pack_directory(directory_path, recursive)

    def pack_files(self, file_paths_list):
        """
        Packs the given files using the service.

        @type file_paths_list: List
        @param file_paths_list: The list of file paths to be used in the packing.
        """

        self.main_packing_colony_service.pack_files(file_paths_list)
