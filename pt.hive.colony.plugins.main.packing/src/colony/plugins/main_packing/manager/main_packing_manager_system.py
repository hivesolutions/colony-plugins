#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 7147 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-12-21 16:50:46 +0000 (seg, 21 Dez 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import main_packing_manager_exceptions

class MainPackingManager:
    """
    The main packing manager class.
    """

    main_packing_manager_plugin = None
    """ The main packing manager plugin """

    service_name_packing_service_plugin_map = {}
    """ The map associating the service name with the packing service plugin """

    def __init__(self, main_packing_manager_plugin):
        """
        Constructor of the class.

        @type main_packing_manager_plugin: MainPackingManagerPlugin
        @param main_packing_manager_plugin: The main packing manager plugin.
        """

        self.main_packing_manager_plugin = main_packing_manager_plugin

        self.service_name_packing_service_plugin_map = {}

    def get_packing_information(self, file_path, properties, service_name):
        """
        Retrieves the packing information from the file
        in the given file path using the provided service name.

        @type file_path: String
        @param file_path: The path of the file to retrieve
        packing information.
        @type properties: Dictionary
        @param properties: The properties for the retrieval.
        @type service_name: String
        @param service_name: The name of the service to be used
        for retrieving information.
        @rtype: Specification
        @return: The packing information for the file.
        """

        # retrieves the packing service plugin for the service name
        packing_service_plugin = self._get_service_name_plugin_by_packing_service_name(service_name)

        # retrieves the packing information using the packing service plugin
        return packing_service_plugin.get_packing_information(file_path, properties)

    def get_packing_file_contents(self, file_path, properties, service_name):
        """
        Retrieves the packing file contents from the file
        in the given file path using the provided service name.

        @type file_path: String
        @param file_path: The path of the file to retrieve
        packing file contents.
        @type properties: Dictionary
        @param properties: The properties for the retrieval.
        @type service_name: String
        @param service_name: The name of the service to be used
        for retrieving the file contents.
        @rtype: String
        @return: The packing file contents for the file.
        """

        # retrieves the packing service plugin for the service name
        packing_service_plugin = self._get_service_name_plugin_by_packing_service_name(service_name)

        # retrieves the packing file contents using the packing service plugin
        return packing_service_plugin.get_packing_file_contents(file_path, properties)

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

        # retrieves the packing service plugin for the service name
        packing_service_plugin = self._get_service_name_plugin_by_packing_service_name(service_name)

        # packs the directory with the packing service plugin
        packing_service_plugin.pack_directory(directory_path, properties)

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

        # retrieves the packing service plugin for the service name
        packing_service_plugin = self._get_service_name_plugin_by_packing_service_name(service_name)

        # packs the files with the packing service plugin
        packing_service_plugin.pack_files(file_paths_list, properties)

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

        # retrieves the packing service plugin for the service name
        packing_service_plugin = self._get_service_name_plugin_by_packing_service_name(service_name)

        # unpacks the files with the packing service plugin
        packing_service_plugin.unpack_files(file_paths_list, properties)

    def packing_service_load(self, packing_service_plugin):
        """
        Loads the given packing service plugin.

        @type packing_service_plugin: Plugin
        @param packing_service_plugin: The packing service plugin to be loaded.
        """

        # retrieves packing service plugin service name
        service_name = packing_service_plugin.get_service_name()

        # sets the packing service plugin in the service name packing service plugin map
        self.service_name_packing_service_plugin_map[service_name] = packing_service_plugin

    def packing_service_unload(self, packing_service_plugin):
        """
        Unloads the given packing service plugin.

        @type packing_service_plugin: Plugin
        @param packing_service_plugin: The packing service plugin to be loaded.
        """

        # retrieves packing service plugin service name
        service_name = packing_service_plugin.get_service_name()

        # removes the packing service plugin from the service name packing service plugin map
        del self.service_name_packing_service_plugin_map[service_name]

    def _get_service_name_plugin_by_packing_service_name(self, service_name):
        """
        Retrieves the packing service plugin for the given
        service name.

        @type service_name: String
        @param service_name: The service name to retrieve
        the packing service plugin.
        @rtype: Plugin
        @return: The packing service plugin.
        """

        # in case the service name does not exist in the service
        # name packing service plugin map
        if not service_name in self.service_name_packing_service_plugin_map:
            # raises the packing service not available exception
            raise main_packing_manager_exceptions.PackingServiceNotAvailable("the service is not available: " + service_name)

        # retrieves the packing service plugin
        packing_service_plugin = self.service_name_packing_service_plugin_map[service_name]

        # returns the packing service plugin
        return packing_service_plugin
