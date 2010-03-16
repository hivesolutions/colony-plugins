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
import zipfile
import tarfile

import os.path

SERVICE_NAME = "colony"
""" The service name """

ID_VALUE = "id"
""" The id value """

VERSION_VALUE = "version"
""" The version value """

RESOURCES_VALUE = "resources"
""" The resources value """

SPECIFICATION_VALUE = "specification"
""" The specification value """

RECURSIVE_VALUE = "recursive"
""" The recursive value """

PLUGIN_REGEX_VALUE = "plugin_regex"
""" The plugin regex value """

TARGET_PATH_VALUE = "target_path"
""" The target path value """

JSON_PLUGIN_REGEX = ".+plugin.json$"
""" The json plugin regex """

ZIP_FILE_MODE = 1
""" The zip file mode """

TAR_FILE_MODE = 2
""" The tar file mode """

DEFAULT_COLONY_PLUGIN_FILE_MODE = ZIP_FILE_MODE
""" The default colony plugin file mode """

DEFAULT_COLONY_PLUGIN_FILE_EXTENSION = ".cpx"
""" The default colony plugin file extension """

DEFAULT_TARGET_PATH = "colony"
""" The default target path """

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

        # retrieves the recursive property
        recursive = properties.get(RECURSIVE_VALUE, False)

        # compiles the plugin regex
        plugin_regex = re.compile(JSON_PLUGIN_REGEX)

        # sets the plugin regex in the properties
        properties[PLUGIN_REGEX_VALUE] = plugin_regex

        # in case the recursion is activated
        if recursive:
            # walks throughout the directory path
            os.path.walk(directory_path, self._pack_directory, properties)
        else:
            # retrieves the directory file list
            directory_file_list = os.listdir(directory_path)

            # packs the directory
            self._pack_directory(properties, directory_path, directory_file_list)

    def pack_files(self, file_paths_list, properties):
        """
        Packs the given files using the service.

        @type file_paths_list: List
        @param file_paths_list: The list of file paths to be used in the packing.
        @type properties: Dictionary
        @param properties: The properties for the packing.
        """

        # compiles the plugin regex
        plugin_regex = re.compile(JSON_PLUGIN_REGEX)

        # retrieves the target path property
        target_path = properties.get(TARGET_PATH_VALUE, DEFAULT_TARGET_PATH)

        # iterates over all the file path in the
        # file paths list
        for file_path in file_paths_list:
            # in case there is a match in the directory file name
            if plugin_regex.match(file_path):
                # processes the plugin file
                self._process_plugin_file(file_path, target_path)

    def unpack_files(self, file_paths_list, properties):
        """
        Unpacks the given files using the service.

        @type file_paths_list: List
        @param file_paths_list: The list of file paths to be used in the unpacking.
        @type properties: Dictionary
        @param properties: The properties for the unpacking.
        """

        # retrieves the target path property
        target_path = properties.get(TARGET_PATH_VALUE, DEFAULT_TARGET_PATH)

        # iterates over all the file path in the
        # file paths list
        for file_path in file_paths_list:
            # unprocesses the plugin file
            self._unprocess_plugin_file(file_path, target_path)

    def _pack_directory(self, arguments, directory_path, directory_file_list):
        # retrieves the plugin regex attribute
        plugin_regex = arguments[PLUGIN_REGEX_VALUE]

        # retrieves the target path attribute
        target_path = arguments.get(TARGET_PATH_VALUE, DEFAULT_TARGET_PATH)

        # iterates over all the directory file name
        for directory_file_name in directory_file_list:
            # in case there is a match in the directory file name
            if plugin_regex.match(directory_file_name):
                # creates the full file path as the directory path and
                # the directory file name
                full_file_path = directory_path + "/" + directory_file_name

                # processes the plugin file
                self._process_plugin_file(full_file_path, target_path)

    def _process_plugin_file(self, file_path, target_path):
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

            # retrieves the base path and extension from the file path
            _file_base_path, file_extension = os.path.splitext(file_path)

            # creates a new compressed file
            compressed_file = ColonyPluginCompressedFile()

            # opens the compressed file
            compressed_file.open(target_path + "/" + plugin_id + "_" + plugin_version + DEFAULT_COLONY_PLUGIN_FILE_EXTENSION)

            # iterates over all the plugin resources
            for plugin_resource in plugin_resources:
                # adds the plugin resource to the compressed file, using
                # the correct relative paths
                compressed_file.add(base_directory + "/" + plugin_resource, plugin_resource)

            # adds the specification file to the compressed file
            compressed_file.add(file_path, SPECIFICATION_VALUE + file_extension)

            # closes the compressed file
            compressed_file.close()

    def _unprocess_plugin_file(self, file_path, target_path):
        # retrieves the plugin specification for the given file
        plugin_specification = self.main_packing_colony_service_plugin.specification_manager_plugin.get_plugin_specification(file_path, {})

        # tenho de abrir o plugin processar a specification e imprimir alguma coisa para o logger
        # tipo installing plugin xpto

        # depois tenho de descomprimir em ultimo lugar o main plugin file
        # para que nao exista problema no auto loading

class ColonyPluginCompressedFile:
    """
    The colony plugin compressed file class, that
    abstracts the creation of the colony plugin file.
    """

    mode = DEFAULT_COLONY_PLUGIN_FILE_MODE
    """ The file mode to be used to organize the plugin file """

    file = None
    """ The file reference to be used in writing """

    def __init__(self, mode = DEFAULT_COLONY_PLUGIN_FILE_MODE):
        """
        Constructor of the class.

        @type mode: int
        @param mode: The mode to be used in the file.
        """

        self.mode = mode

    def open(self, file_path):
        """
        Opens the file in the given file path.

        @type file_path: String
        @param file_path: The path to the file to open.
        """

        if self.mode == ZIP_FILE_MODE:
            self.file = zipfile.ZipFile(file_path, "w", compression = zipfile.ZIP_DEFLATED)
        elif self.mode == TAR_FILE_MODE:
            self.file = tarfile.open(file_path, "w:gz")

    def close(self):
        """
        Closes the current file.
        """

        self.file.close()

    def add(self, file_path, target_file_path):
        """
        Adds the file in the given path as the logical (target)
        file in compressed file.

        @type file_path: String
        @param file_path: The path to the file to be added.
        @type target_file_path: String
        @param target_file_path: The target logical path to be used in
        the compressed file.
        """

        if self.mode == ZIP_FILE_MODE:
            self.file.write(file_path, target_file_path)
        elif self.mode == TAR_FILE_MODE:
            self.file.add(file_path, target_file_path)

    def extract(self, file_path, target_path):
        #ZipFile.extract(member[, path[, pwd]])
        #TarFile.extract(member, path="")
        pass

    def extract_all(self, target_path):
        #ZipFile.extractall([path[, members[, pwd]]])
        #TarFile.extractall(path=".", members=None)
        pass

    def read(self, file_path):
        #ZipFile.read(name[, pwd])
        #TarFile.extractfile(member)
        pass
