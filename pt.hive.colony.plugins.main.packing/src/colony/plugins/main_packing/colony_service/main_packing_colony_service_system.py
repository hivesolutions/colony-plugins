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

__revision__ = "$LastChangedRevision: 7147 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-12-21 16:50:46 +0000 (seg, 21 Dez 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

import os.path

SERVICE_NAME = "colony"
""" The service name """

ID_VALUE = "id"
""" The id value """

VERSION_VALUE = "version"
""" The version value """

RESOURCES_VALUE = "resources"
""" The resources value """

JSON_PLUGIN_REGEX = ".*plugin.json$"
""" The json plugin regex """

class MainPackingColonyService:
    """
    The main packing colony service class.
    """

    main_packing_colony_service_plugin = None
    """ The main packing colony service plugin """

    def __init__(self, main_packing_colony_service_plugin):
        """
        Constructor of the class.

        @type main_packing_colony_service_plugin: MainPackingColonyServicePlugin
        @param main_packing_colony_service_plugin: The main packing colony service plugin.
        """

        self.main_packing_colony_service_plugin = main_packing_colony_service_plugin

    def get_service_name(self):
        """
        Retrieves the service name.

        @rtype: String
        @return: The service name.
        """

        return SERVICE_NAME

    def pack_directory(self, directory_path, properties):
        """
        Packs the directory using the service.

        @type directory_path: String
        @param directory_path: The path to the directory to be used
        in the packing.
        @type properties: Dictionary
        @param properties: The properties for the packing.
        """

        # compiles the plugin regex
        plugin_regex = re.compile(JSON_PLUGIN_REGEX)

        # retrieves the directory file list
        directory_file_list = os.listdir(directory_path)

        # iterates over all the directory file name
        for directory_file_name in directory_file_list:
            # in case there is a match in the directory file name
            if plugin_regex.match(directory_file_name):
                # creates the full file path as the directory path and
                # the directory file name
                full_file_path = directory_path + "/" + directory_file_name

                # processes the plugin file
                self._process_plugin_file(full_file_path)

    def pack_files(self, file_paths_list, properties):
        """
        Packs the given files using the service.

        @type file_paths_list: List
        @param file_paths_list: The list of file paths to be used in the packing.
        @type properties: Dictionary
        @param properties: The properties for the packing.
        """

        print "packing random files"

    def _process_plugin_file(self, file_path):
        # retrieves the plugin specification for the given file
        plugin_specification = self.main_packing_colony_service_plugin.specification_manager_plugin.get_plugin_specification(file_path, {})

        # retrieves the plugin id
        plugin_id = plugin_specification.get_property(ID_VALUE)

        # retrieves the plugin version
        plugin_version = plugin_specification.get_property(VERSION_VALUE)

        # retrieves the plugin resources
        plugin_resources = plugin_specification.get_property(RESOURCES_VALUE)

        # in case the plugin contains resources
        if plugin_resources:
            # retrieves the base directory
            base_directory = os.path.dirname(file_path)

            import tarfile

            tar_file = tarfile.open("c:/plugins/" + plugin_id + "_" + plugin_version + ".cpx", "w:bz2")

            for plugin_resource in plugin_resources:
                tar_file.add(base_directory + "/" + plugin_resource, plugin_resource)

            tar_file.close()
