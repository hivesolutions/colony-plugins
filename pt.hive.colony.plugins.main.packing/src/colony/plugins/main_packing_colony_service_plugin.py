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

import colony.base.plugin_system

class MainPackingColonyServicePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Packing Colony Service Main plugin.
    """

    id = "pt.hive.colony.plugins.main.packing.colony_service"
    name = "Packing Colony Service Main Plugin"
    short_name = "Packing Colony Service Main"
    description = "Packing Colony Service Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_packing/colony_service/resources/baf.xml"
    }
    capabilities = [
        "packing_service",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.specifications.specification_manager", "1.0.0")
    ]
    main_modules = [
        "main_packing.colony_service.main_packing_colony_service_exceptions",
        "main_packing.colony_service.main_packing_colony_service_system"
    ]

    main_packing_colony_service = None
    """ The main packing colony service """

    specification_manager_plugin = None
    """ The specification manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_packing.colony_service.main_packing_colony_service_system
        self.main_packing_colony_service = main_packing.colony_service.main_packing_colony_service_system.MainPackingColonyService(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_service_name(self):
        """
        Retrieves the service name.

        @rtype: String
        @return: The service name.
        """

        return self.main_packing_colony_service.get_service_name()

    def get_packing_information(self, file_path, properties):
        """
        Retrieves the packing information from the file
        in the given file path using the service.

        @type file_path: String
        @param file_path: The path of the file to retrieve
        packing information.
        @type properties: Dictionary
        @param properties: The properties for the retrieval.
        @rtype: Specification
        @return: The packing information for the file.
        """

        return self.main_packing_colony_service.get_packing_information(file_path, properties)

    def get_packing_file_contents(self, file_path, properties):
        """
        Retrieves the packing file contents from the file
        in the given file path using the service.

        @type file_path: String
        @param file_path: The path of the file to retrieve
        packing file contents.
        @type properties: Dictionary
        @param properties: The properties for the retrieval.
        @rtype: String
        @return: The packing file contents for the file.
        """

        return self.main_packing_colony_service.get_packing_file_contents(file_path, properties)

    def pack_directory(self, directory_path, properties):
        """
        Packs the directory using the service.

        @type directory_path: String
        @param directory_path: The path to the directory to be used
        in the packing.
        @type properties: Dictionary
        @param properties: The properties for the packing.
        """

        return self.main_packing_colony_service.pack_directory(directory_path, properties)

    def pack_files(self, file_paths_list, properties):
        """
        Packs the given files using the service.

        @type file_paths_list: List
        @param file_paths_list: The list of file paths to be used in the packing.
        @type properties: Dictionary
        @param properties: The properties for the packing.
        """

        return self.main_packing_colony_service.pack_files(file_paths_list, properties)

    def unpack_files(self, file_paths_list, properties):
        """
        Unpacks the given files using the service.

        @type file_paths_list: List
        @param file_paths_list: The list of file paths to be used in the unpacking.
        @type properties: Dictionary
        @param properties: The properties for the unpacking.
        """

        return self.main_packing_colony_service.unpack_files(file_paths_list, properties)

    def get_specification_manager_plugin(self):
        return self.specification_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.specifications.specification_manager")
    def set_specification_manager_plugin(self, specification_manager_plugin):
        self.specification_manager_plugin = specification_manager_plugin
