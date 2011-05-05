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

__revision__ = "$LastChangedRevision: 13947 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-05-05 18:29:17 +0100 (qui, 05 Mai 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import stat

VERSION_VALUE = "version"
""" The version value """

INSTALLED_PACKAGES_VALUE = "installed_packages"
""" The installed packages value """

INSTALLED_BUNDLES_VALUE = "installed_bundles"
""" The installed bundles value """

INSTALLED_PLUGINS_VALUE = "installed_plugins"
""" The installed plugins value """

RELATIVE_REGISTRY_PATH = "registry"
""" The path relative to the variable path for the registry """

PACKAGES_FILE_NAME = "packages.json"
""" The packages file name """

BUNDLES_FILE_NAME = "bundles.json"
""" The bundles file name """

PLUGINS_FILE_NAME = "plugins.json"
""" The plugins file name """

DEFAULT_STRUCTURE_TUPLE = (None, -1)
""" The structure tuple to be used by default """

class SystemRegistry:
    """
    The system registry class.
    """

    system_registry_plugin = None
    """ The system registry plugin """

    structure_tuples_map = {}
    """ The map containing the current structure tuple values """

    def __init__(self, system_registry_plugin):
        """
        Constructor of the class.

        @type system_registry_plugin: SystemRegistryPlugin
        @param system_registry_plugin: The system registry plugin.
        """

        self.system_registry_plugin = system_registry_plugin

        self.structure_tuples_map = {}

    def get_packages_structure(self):
        """
        Retrieves the packages structure.

        @rtype: Dictionary
        @return: The packages structure.
        """

        return self._get_structure(PACKAGES_FILE_NAME)

    def get_bundles_structure(self):
        """
        Retrieves the bundles structure.

        @rtype: Dictionary
        @return: The bundles structure.
        """

        return self._get_structure(BUNDLES_FILE_NAME)

    def get_plugins_structure(self):
        """
        Retrieves the plugins structure.

        @rtype: Dictionary
        @return: The plugins structure.
        """

        return self._get_structure(PLUGINS_FILE_NAME)

    def get_package_information(self, package_id, package_version):
        """
        Retrieves the package information for the package
        with the given id and version.

        @type package_id: String
        @param package_id: The id of the package information
        to retrieve.
        @type package_version: String
        @param package_version: The version of the package information
        to retrieve.
        @rtype: Dictionary
        @return: The package information for the package
        with the given id and version.
        """

        # retrieves the plguins structure
        packages_structure = self.get_packages_structure()

        # retrieves the installed packages
        installed_packages = packages_structure[INSTALLED_PACKAGES_VALUE]

        # retrieves the package "information" from the installed packages
        package_information = installed_packages.get(package_id, {})

        # retrieves the package version information
        package_information_version = package_information.get(VERSION_VALUE, None)

        # in case the package information is not valid or in
        # case the version is not the same
        if not package_information or not package_version == package_information_version:
            # returns invalid
            return None

        # returns the package information
        return package_information

    def get_bundle_information(self, bundle_id, bundle_version):
        """
        Retrieves the bundle information for the bundle
        with the given id and version.

        @type bundle_id: String
        @param bundle_id: The id of the bundle information
        to retrieve.
        @type bundle_version: String
        @param bundle_version: The version of the bundle information
        to retrieve.
        @rtype: Dictionary
        @return: The bundle information for the bundle
        with the given id and version.
        """

        # retrieves the plguins structure
        bundles_structure = self.get_bundles_structure()

        # retrieves the installed bundles
        installed_bundles = bundles_structure[INSTALLED_BUNDLES_VALUE]

        # retrieves the bundle "information" from the installed bundles
        bundle_information = installed_bundles.get(bundle_id, {})

        # retrieves the bundle version information
        bundle_information_version = bundle_information.get(VERSION_VALUE, None)

        # in case the bundle information is not valid or in
        # case the version is not the same
        if not bundle_information or not bundle_version == bundle_information_version:
            # returns invalid
            return None

        # returns the bundle information
        return bundle_information

    def get_plugin_information(self, plugin_id, plugin_version):
        """
        Retrieves the plugin information for the plugin
        with the given id and version.

        @type plugin_id: String
        @param plugin_id: The id of the plugin information
        to retrieve.
        @type plugin_version: String
        @param plugin_version: The version of the plugin information
        to retrieve.
        @rtype: Dictionary
        @return: The plugin information for the plugin
        with the given id and version.
        """

        # retrieves the plguins structure
        plugins_structure = self.get_plugins_structure()

        # retrieves the installed plugins
        installed_plugins = plugins_structure[INSTALLED_PLUGINS_VALUE]

        # retrieves the plugin "information" from the installed plugins
        plugin_information = installed_plugins.get(plugin_id, {})

        # retrieves the plugin version information
        plugin_information_version = plugin_information.get(VERSION_VALUE, None)

        # in case the plugin information is not valid or in
        # case the version is not the same
        if not plugin_information or not plugin_version == plugin_information_version:
            # returns invalid
            return None

        # returns the plugin information
        return plugin_information

    def _get_structure(self, structure_file_name):
        """
        Retrieves the structure from the structure file.
        This method checks the modified date before loading
        the structure file.

        @type structure_file_name: String
        @param structure_file_name: The file name of the structure to
        be loaded.
        @rtype: Dictionary
        @return: The structure retrieved from the structure file.
        """

        # retrieves the plugin manager
        plugin_manager = self.system_registry_plugin.manager

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # retrieves the registry path
        registry_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.join(registry_path, structure_file_name)

        # retrieves the structure tuple from the structure
        # tuples map
        structure_tuple = self.structure_tuples_map.get(structure_file_name, DEFAULT_STRUCTURE_TUPLE)

        # unpacks the structure tuple into structure
        # and structure timestamp
        structure, structure_timestamp = structure_tuple

        # retrieves the file stat
        file_stat = os.stat(structure_file_path)

        # retrieves the modified timestamp
        modified_timestamp = file_stat[stat.ST_MTIME]

        # in case the modified date did not change
        if modified_timestamp == structure_timestamp:
            # returns the structure
            return structure

        # retrieves the structure loading it
        structure = self.__get_structure(structure_file_path)

        # creates the "new" structure tuple
        structure_tuple = (structure, modified_timestamp)

        # sets the structure tuple in the structure tuples map
        self.structure_tuples_map[structure_file_name] = structure_tuple

        # returns the structure
        return structure

    def __get_structure(self, structure_file_path):
        """
        Retrieves the structure from the structure file.
        This method loads the structure file to get the
        structure.

        @type structure_file_path: String
        @param structure_file_path: The file path of the structure to
        be loaded.
        @rtype: Dictionary
        @return: The structure retrieved from the structure file.
        """

        # retrieves the json plugin
        json_plugin = self.system_registry_plugin.json_plugin

        # reads the structure file contents
        structure_file_contents = self._read_file(structure_file_path)

        # loads the structure file contents from json
        structure = json_plugin.loads(structure_file_contents)

        # returns the structure
        return structure

    def _read_file(self, file_path):
        """
        Reads the file contents from the file
        in the given path.

        @type file_path: String
        @param file_path: The path to the file
        to be read.
        @rtype: String
        @return: The file contents read.
        """

        # opens the file
        file = open(file_path)

        try:
            # reads the file contents
            file_contents = file.read()
        finally:
            # closes the file
            file.close()

        # returns the file contents
        return file_contents
