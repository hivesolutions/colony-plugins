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

import os
import re
import stat
import types
import zipfile
import tarfile

import colony.libs.path_util

import main_packing_colony_service_exceptions

SERVICE_NAME = "colony"
""" The service name """

ID_VALUE = "id"
""" The id value """

VERSION_VALUE = "version"
""" The version value """

RESOURCES_VALUE = "resources"
""" The resources value """

PLUGINS_VALUE = "plugins"
""" The plugins value """

SPECIFICATION_VALUE = "specification"
""" The specification value """

RECURSIVE_VALUE = "recursive"
""" The recursive value """

BUNDLE_REGEX_VALUE = "bundle_regex"
""" The bundle regex value """

PLUGIN_REGEX_VALUE = "plugin_regex"
""" The plugin regex value """

CONTAINER_REGEX_VALUE = "container_regex"
""" The container regex value """

TARGET_PATH_VALUE = "target_path"
""" The target path value """

PLUGINS_PATH_VALUE = "plugins_path"
""" The plugins path value """

MAIN_FILE_VALUE = "main_file"
""" The main file value """

SPECIFICATION_FILE_PATH_VALUE = "specification_file_path"
""" The specification file path value """

JSON_BUNDLE_REGEX = ".+bundle.json$"
""" The json bundle regex """

JSON_PLUGIN_REGEX = ".+plugin.json$"
""" The json plugin regex """

JSON_CONTAINER_REGEX = ".+container.json$"
""" The json container regex """

ZIP_FILE_MODE = 1
""" The zip file mode """

TAR_FILE_MODE = 2
""" The tar file mode """

RESOURCES_BASE_PATH = "resources"
""" The resources base path """

PLUGINS_BASE_PATH = "plugins"
""" The plugins base path """

DEFAULT_COLONY_COMPRESSED_FILE_MODE = ZIP_FILE_MODE
""" The default colony compressed file mode """

DEFAULT_COLONY_BUNDLE_FILE_EXTENSION = ".cbx"
""" The default colony bundle file extension """

DEFAULT_COLONY_PLUGIN_FILE_EXTENSION = ".cpx"
""" The default colony plugin file extension """

DEFAULT_COLONY_CONTAINER_FILE_EXTENSION = ".ccx"
""" The default colony container file extension """

DEFAULT_TARGET_PATH = "."
""" The default target path """

DEFAULT_TAR_COMPRESSION_FORMAT = "bz2"
""" The default tar compression format """

DEFAULT_SPECIFICATION_FILE_PATH = "specification.json"
""" The default specification file path """

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

class MainPackingColonyService:
    """
    The main packing colony service class.
    """

    main_packing_colony_service_plugin = None
    """ The main packing colony service plugin """

    bundle_regex = None
    """ The bundle regex """

    plugin_regex = None
    """ The plugin regex """

    container_regex = None
    """ The container regex """

    def __init__(self, main_packing_colony_service_plugin):
        """
        Constructor of the class.

        @type main_packing_colony_service_plugin: MainPackingColonyServicePlugin
        @param main_packing_colony_service_plugin: The main packing colony service plugin.
        """

        self.main_packing_colony_service_plugin = main_packing_colony_service_plugin

        # compiles the regex values
        self.bundle_regex = re.compile(JSON_BUNDLE_REGEX)
        self.plugin_regex = re.compile(JSON_PLUGIN_REGEX)
        self.container_regex = re.compile(JSON_CONTAINER_REGEX)

    def get_service_name(self):
        """
        Retrieves the service name.

        @rtype: String
        @return: The service name.
        """

        return SERVICE_NAME

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

        # retrieves the specification manager plugin
        specification_manager_plugin = self.main_packing_colony_service_plugin.specification_manager_plugin

        # retrieves the specification file path property
        specification_file_path = properties.get(SPECIFICATION_FILE_PATH_VALUE, DEFAULT_SPECIFICATION_FILE_PATH)

        # creates a new compressed file
        compressed_file = ColonyCompressedFile()

        # opens the compressed file
        compressed_file.open(file_path, "r")

        try:
            # reads the specification file from the compressed file
            specification_file_buffer = compressed_file.read(specification_file_path)
        finally:
            # closes the compressed file
            compressed_file.close()

        # retrieves the (bundle) specification for the given file
        specification = specification_manager_plugin.get_specification_file_buffer(specification_file_buffer, {})

        # returns the specification
        return specification

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

        # retrieves the specification file path property
        specification_file_path = properties.get(SPECIFICATION_FILE_PATH_VALUE, DEFAULT_SPECIFICATION_FILE_PATH)

        # creates a new compressed file
        compressed_file = ColonyCompressedFile()

        # opens the compressed file
        compressed_file.open(file_path, "r")

        try:
            # reads the specification file from the compressed file
            specification_file_buffer = compressed_file.read(specification_file_path)
        finally:
            # closes the compressed file
            compressed_file.close()

        # returns the specification file buffer
        return specification_file_buffer

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

        # sets the plugin regex in the properties
        properties[PLUGIN_REGEX_VALUE] = self.plugin_regex

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

        # retrieves the target path property
        target_path = properties.get(TARGET_PATH_VALUE, DEFAULT_TARGET_PATH)

        # retrieves the plugins path property
        plugins_path = properties.get(PLUGINS_PATH_VALUE, DEFAULT_TARGET_PATH)

        # iterates over all the file path in the
        # file paths list
        for file_path in file_paths_list:
            # in case there is a bundle match in
            # the directory file name
            if self.bundle_regex.match(file_path):
                # processes the bundle file
                self._process_bundle_file(file_path, target_path, plugins_path)
            # in case there is a plugin match in
            # the directory file name
            elif self.plugin_regex.match(file_path):
                # processes the plugin file
                self._process_plugin_file(file_path, target_path)
            # in case there is a container match in
            # the directory file name
            elif self.container_regex.match(file_path):
                # processes the container file
                self._process_container_file(file_path, target_path)
            # otherwise the file path is not valid
            else:
                # raises the invalid file path exception
                raise main_packing_colony_service_exceptions.InvalidFilePath(file_path)

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

        # retrieves the specification file path property
        specification_file_path = properties.get(SPECIFICATION_FILE_PATH_VALUE, DEFAULT_SPECIFICATION_FILE_PATH)

        # iterates over all the file path in the
        # file paths list
        for file_path in file_paths_list:
            # splits the file path into base name and extension
            _file_base_name, file_extension = os.path.splitext(file_path)

            # in case it's a bundle extension
            if file_extension == DEFAULT_COLONY_BUNDLE_FILE_EXTENSION:
                # (un)processes the bundle file using the given specification file path
                self._unprocess_bundle_file(file_path, target_path, specification_file_path)
            # in case it's a plugin extension
            elif file_extension == DEFAULT_COLONY_PLUGIN_FILE_EXTENSION:
                # (un)processes the plugin file using the given specification file path
                self._unprocess_plugin_file(file_path, target_path, specification_file_path)
            # in case it's a container extension
            elif file_extension == DEFAULT_COLONY_CONTAINER_FILE_EXTENSION:
                # (un)processes the container file using the given specification file path
                self._unprocess_plugin_container(file_path, target_path, specification_file_path)
            # otherwise the file extension is not valid
            else:
                # raises the invalid file extension
                raise main_packing_colony_service_exceptions.InvalidFileExtension(file_extension)

    def _pack_directory(self, arguments, directory_path, directory_file_list):
        """
        Method to be used as callback for the walking procedure.
        This method processes the given directory entries packing the files
        taht are valid.

        @type arguments: Object
        @param arguments: The arguments sent to the walking procedure.
        @type directory_path: String
        @param directory_path: The path to the current directory.
        @type directory_file_list: List
        @param directory_file_list: The list of files in the current directory.
        """

        # retrieves the bundle regex attribute
        bundle_regex = arguments[BUNDLE_REGEX_VALUE]

        # retrieves the plugin regex attribute
        plugin_regex = arguments[PLUGIN_REGEX_VALUE]

        # retrieves the container regex attribute
        container_regex = arguments[CONTAINER_REGEX_VALUE]

        # retrieves the target path attribute
        target_path = arguments.get(TARGET_PATH_VALUE, DEFAULT_TARGET_PATH)

        # iterates over all the directory file name
        for directory_file_name in directory_file_list:
            # creates the full file path as the directory path and
            # the directory file name
            full_file_path = directory_path + "/" + directory_file_name

            # in case there is a bundle match in the directory file name
            if bundle_regex.match(directory_file_name):
                # processes the bundle file
                self._process_bundle_file(full_file_path, target_path)
            # in case there is a plugin match in the directory file name
            elif plugin_regex.match(directory_file_name):
                # processes the plugin file
                self._process_plugin_file(full_file_path, target_path)
            # in case there is a container match in the directory file name
            elif container_regex.match(directory_file_name):
                # processes the container file
                self._process_container_file(full_file_path, target_path)

    def _process_bundle_file(self, file_path, target_path, plugins_path):
        """
        Processes the bundle file in the given file path, putting
        the results in the target path.

        @type file_path: String
        @param file_path: The path to the bundle file to be processed.
        @type target_path: String
        @param target_path: The target path to be used in the results.
        @type plugins_path: String
        @param plugins_path: The plugins path to be used in the retrieval
        of plugin files.
        """

        # retrieves the specification manager plugin
        specification_manager_plugin = self.main_packing_colony_service_plugin.specification_manager_plugin

        # retrieves the bundle specification for the given file
        bundle_specification = specification_manager_plugin.get_specification(file_path, {})

        # retrieves the bundle id
        bundle_id = bundle_specification.get_property(ID_VALUE)

        # retrieves the bundle version
        bundle_version = bundle_specification.get_property(VERSION_VALUE)

        # retrieves the bundle plugins
        bundle_plugins = bundle_specification.get_property(PLUGINS_VALUE)

        # retrieves the base path and extension from the file path
        _file_base_path, file_extension = os.path.splitext(file_path)

        # creates a new compressed file
        compressed_file = ColonyCompressedFile()

        # opens the compressed file
        compressed_file.open(target_path + "/" + bundle_id + "_" + bundle_version + DEFAULT_COLONY_BUNDLE_FILE_EXTENSION, "w")

        try:
            # iterates over all the bundle plugins
            for bundle_plugin in bundle_plugins:
                # retrieves the bundle plugin id
                bundle_plugin_id = bundle_plugin[ID_VALUE]

                # retrieves the bundle plugin version
                bundle_plugin_version = bundle_plugin[VERSION_VALUE]

                # creates the bundle plugin name
                bundle_plugin_name = bundle_plugin_id + "_" + bundle_plugin_version + DEFAULT_COLONY_PLUGIN_FILE_EXTENSION

                # creates the bundle plugin path
                bundle_plugin_path = plugins_path + "/" + bundle_plugin_name

                # adds the bundle plugin file to the compressed file
                compressed_file.add(bundle_plugin_path, PLUGINS_BASE_PATH + "/" + bundle_plugin_name)

            # adds the specification file to the compressed file
            compressed_file.add(file_path, SPECIFICATION_VALUE + file_extension)
        finally:
            # closes the compressed file
            compressed_file.close()

    def _process_plugin_file(self, file_path, target_path):
        """
        Processes the plugin file in the given file path, putting
        the results in the target path.

        @type file_path: String
        @param file_path: The path to the plugin file to be processed.
        @type target_path: String
        @param target_path: The target path to be used in the results.
        """

        # retrieves the specification manager plugin
        specification_manager_plugin = self.main_packing_colony_service_plugin.specification_manager_plugin

        # retrieves the plugin specification for the given file
        plugin_specification = specification_manager_plugin.get_specification(file_path, {})

        # retrieves the plugin id
        plugin_id = plugin_specification.get_property(ID_VALUE)

        # retrieves the plugin version
        plugin_version = plugin_specification.get_property(VERSION_VALUE)

        # retrieves the plugin resources
        plugin_resources = plugin_specification.get_property(RESOURCES_VALUE)

        # in case the plugin contains no resources
        if not plugin_resources:
            # raises the plugin processing exception
            raise main_packing_colony_service_exceptions.PluginProcessingException("no plugin resources found")

        # retrieves the base directory
        base_directory = os.path.dirname(file_path)

        # retrieves the base path and extension from the file path
        _file_base_path, file_extension = os.path.splitext(file_path)

        # creates a new compressed file
        compressed_file = ColonyCompressedFile()

        # opens the compressed file
        compressed_file.open(target_path + "/" + plugin_id + "_" + plugin_version + DEFAULT_COLONY_PLUGIN_FILE_EXTENSION, "w")

        try:
            # iterates over all the plugin resources
            for plugin_resource in plugin_resources:
                # adds the plugin resource to the compressed file, using
                # the correct relative paths
                compressed_file.add(base_directory + "/" + plugin_resource, RESOURCES_BASE_PATH + "/" + plugin_resource)

            # adds the specification file to the compressed file
            compressed_file.add(file_path, SPECIFICATION_VALUE + file_extension)
        finally:
            # closes the compressed file
            compressed_file.close()

    def _process_container_file(self, file_path, target_path):
        """
        Processes the container file in the given file path, putting
        the results in the target path.

        @type file_path: String
        @param file_path: The path to the container file to be processed.
        @type target_path: String
        @param target_path: The target path to be used in the results.
        """

        # retrieves the specification manager plugin
        specification_manager_plugin = self.main_packing_colony_service_plugin.specification_manager_plugin

        # retrieves the plugin specification for the given file
        plugin_specification = specification_manager_plugin.get_specification(file_path, {})

        # retrieves the plugin id
        plugin_id = plugin_specification.get_property(ID_VALUE)

        # retrieves the plugin version
        plugin_version = plugin_specification.get_property(VERSION_VALUE)

        # retrieves the plugin resources
        plugin_resources = plugin_specification.get_property(RESOURCES_VALUE)

        # in case the plugin contains no resources
        if not plugin_resources:
            # raises the plugin processing exception
            raise main_packing_colony_service_exceptions.PluginProcessingException("no plugin resources found")

        # retrieves the base directory
        base_directory = os.path.dirname(file_path)

        # retrieves the base path and extension from the file path
        _file_base_path, file_extension = os.path.splitext(file_path)

        # creates a new compressed file
        compressed_file = ColonyCompressedFile()

        # opens the compressed file
        compressed_file.open(target_path + "/" + plugin_id + "_" + plugin_version + DEFAULT_COLONY_PLUGIN_FILE_EXTENSION, "w")

        try:
            # iterates over all the plugin resources
            for plugin_resource in plugin_resources:
                # adds the plugin resource to the compressed file, using
                # the correct relative paths
                compressed_file.add(base_directory + "/" + plugin_resource, RESOURCES_BASE_PATH + "/" + plugin_resource)

            # adds the specification file to the compressed file
            compressed_file.add(file_path, SPECIFICATION_VALUE + file_extension)
        finally:
            # closes the compressed file
            compressed_file.close()

    def _unprocess_bundle_file(self, file_path, target_path, specification_file_path):
        """
        (Un)processes the bundle file in the given file path, putting
        the results in the target path.

        @type file_path: String
        @param file_path: The path to the bundle file to be (un)processed.
        @type target_path: String
        @param target_path: The target path to be used in the results.
        @type specification_file_path: String
        @param specification_file_path: The specification file path in the bundle file.
        """

        # prints a debug message
        self.main_packing_colony_service_plugin.debug("Unpacking bundle file '%s' into '%s'" % (file_path, target_path))

        # retrieves the specification manager plugin
        specification_manager_plugin = self.main_packing_colony_service_plugin.specification_manager_plugin

        # creates a new compressed file
        compressed_file = ColonyCompressedFile()

        # opens the compressed file
        compressed_file.open(file_path, "r")

        try:
            # reads the specification file from the compressed file
            specification_file_buffer = compressed_file.read(specification_file_path)

            # retrieves the bundle specification for the given file
            bundle_specification = specification_manager_plugin.get_specification_file_buffer(specification_file_buffer, {})

            # retrieves the bundle resources
            bundle_plugins = bundle_specification.get_property("plugins")

            # iterates over all the bundle resources
            for bundle_plugin in bundle_plugins:
                # retrieves the bundle plugin id
                bundle_plugin_id = bundle_plugin[ID_VALUE]

                # retrieves the bundle plugin version
                bundle_plugin_version = bundle_plugin[VERSION_VALUE]

                # creates the bundle plugin name
                bundle_plugin_name = bundle_plugin_id + "_" + bundle_plugin_version + DEFAULT_COLONY_PLUGIN_FILE_EXTENSION

                # creates the bundle plugin path
                bundle_plugin_path = PLUGINS_BASE_PATH + "/" + bundle_plugin_name

                # creates the bundle plugin target path
                bundle_plugin_target_path = target_path + "/" + PLUGINS_BASE_PATH + "/" + bundle_plugin_name

                # prints a debug message
                self.main_packing_colony_service_plugin.debug("Extracting plugin '%s'" % bundle_plugin_name)

                # extracts the plugin
                compressed_file.extract(bundle_plugin_path, bundle_plugin_target_path, False)
        finally:
            # closes the compressed file
            compressed_file.close()

    def _unprocess_plugin_file(self, file_path, target_path, specification_file_path):
        """
        (Un)processes the plugin file in the given file path, putting
        the results in the target path.

        @type file_path: String
        @param file_path: The path to the plugin file to be (un)processed.
        @type target_path: String
        @param target_path: The target path to be used in the results.
        @type specification_file_path: String
        @param specification_file_path: The specification file path in the plugin file.
        """

        # prints a debug message
        self.main_packing_colony_service_plugin.debug("Unpacking plugin file '%s' into '%s'" % (file_path, target_path))

        # retrieves the specification manager plugin
        specification_manager_plugin = self.main_packing_colony_service_plugin.specification_manager_plugin

        # creates a new compressed file
        compressed_file = ColonyCompressedFile()

        # opens the compressed file
        compressed_file.open(file_path, "r")

        try:
            # reads the specification file from the compressed file
            specification_file_buffer = compressed_file.read(specification_file_path)

            # retrieves the plugin specification for the given file
            plugin_specification = specification_manager_plugin.get_specification_file_buffer(specification_file_buffer, {})

            # retrieves the plugin main file
            main_file = plugin_specification.get_property(MAIN_FILE_VALUE)

            # retrieves the plugin resources
            plugin_resources = plugin_specification.get_property(RESOURCES_VALUE)

            # in case the plugin contains no resources
            if not plugin_resources:
                # raises the plugin (un)processing exception
                raise main_packing_colony_service_exceptions.PluginUnprocessingException("no plugin resources found")

            # iterates over all the plugin resources
            for plugin_resource in plugin_resources:
                # in case the resource is the main file
                # (because it should be extracted at the end)
                if plugin_resource == main_file:
                    # continues the loop
                    continue

                # creates the plugin resource path
                plugin_resource_path = RESOURCES_BASE_PATH + "/" + plugin_resource

                # creates the plugin resource target path
                plugin_resource_target_path = target_path + "/" + plugin_resource

                # prints a debug message
                self.main_packing_colony_service_plugin.debug("Extracting resource '%s'" % plugin_resource)

                # extracts the resource
                compressed_file.extract(plugin_resource_path, plugin_resource_target_path, False)

            # creates the plugin main file path
            plugin_main_file_path = RESOURCES_BASE_PATH + "/" + main_file

            # creates the plugin main file target path
            plugin_main_file_target_path = target_path + "/" + main_file

            # the main file is extracted at the end to avoid any problem
            compressed_file.extract(plugin_main_file_path, plugin_main_file_target_path, False)
        finally:
            # closes the compressed file
            compressed_file.close()

class ColonyCompressedFile:
    """
    The colony compressed file class, that abstracts
    the creation of the colony compressed file.
    """

    mode = DEFAULT_COLONY_COMPRESSED_FILE_MODE
    """ The file mode to be used to organize the compressed file """

    file = None
    """ The file reference to be used in writing """

    def __init__(self, mode = DEFAULT_COLONY_COMPRESSED_FILE_MODE):
        """
        Constructor of the class.

        @type mode: int
        @param mode: The mode to be used in the file.
        """

        self.mode = mode

    def open(self, file_path, mode = "rw"):
        """
        Opens the file in the given file path.

        @type file_path: String
        @param file_path: The path to the file to open.
        @type mode: String
        @param mode: The opening mode to be used.
        """

        if self.mode == ZIP_FILE_MODE:
            self.file = zipfile.ZipFile(file_path, mode, compression = zipfile.ZIP_DEFLATED)
        elif self.mode == TAR_FILE_MODE:
            self.file = tarfile.open(file_path, mode + ":" + DEFAULT_TAR_COMPRESSION_FORMAT)

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
            # retrieves the file mode
            mode = os.stat(file_path)[stat.ST_MODE]

            # in case the file is not a directory
            if stat.S_ISDIR(mode):
                # retrieves the directory file list
                directory_file_list = os.listdir(file_path)

                # iterates over all the directory file name
                for directory_file_name in directory_file_list:
                    # creates the full file path as the file path and
                    # the directory file name
                    full_file_path = file_path + "/" + directory_file_name

                    # creates the full target file path as the target file path and
                    # the directory file name
                    full_target_file_path = target_file_path + "/" + directory_file_name

                    # retrieves the file mode
                    mode = os.stat(full_file_path)[stat.ST_MODE]

                    # in case the file is not a directory
                    if stat.S_ISDIR(mode):
                        self.add(full_file_path, full_target_file_path)
                    else:
                        # normalizes the full target file path
                        full_target_file_path_normalized = self._normalize_file_path(full_target_file_path)

                        # writes the file to the compressed file
                        self.file.write(full_file_path, full_target_file_path_normalized)
            else:
                # normalizes the target file path
                target_file_path_normalized = self._normalize_file_path(target_file_path)

                # writes the file to the compressed file
                self.file.write(file_path, target_file_path_normalized)
        elif self.mode == TAR_FILE_MODE:
            self.file.add(file_path, target_file_path)

    def extract(self, file_path, target_path = "", proccess_relative = True):
        if self.mode == ZIP_FILE_MODE:
            self._extract_zip(file_path, target_path, proccess_relative)
        elif self.mode == TAR_FILE_MODE:
            self.file.extract(file_path, target_path)

    def extract_all(self, target_path = ""):
        if self.mode == ZIP_FILE_MODE:
            self._extract_all_zip(target_path)
        elif self.mode == TAR_FILE_MODE:
            self.file.extractall(target_path)

    def read(self, file_path):
        if self.mode == ZIP_FILE_MODE:
            # retrieves the file contents from the
            # compressed file
            file_contents = self.file.read(file_path)
        elif self.mode == TAR_FILE_MODE:
            # retrieves the file from the compressed
            # file
            file = self.file.extractfile(file_path)

            # reads the file contents from the file
            file_contents = file.read()

        # returns the file contents
        return file_contents

    def _extract_zip(self, file_path, target_path, proccess_relative = True):
        # in case the process relative flag is set
        if proccess_relative:
            # creates the complete target path by appending the
            # file path to the target path
            complete_target_path = target_path + "/" + file_path
        else:
            # sets the complete target path as the target path
            complete_target_path = target_path

        # normalizes the target path
        target_path_normalized = colony.libs.path_util.normalize_path(complete_target_path)

        # retrieves all the upper directories
        upper_directory_paths = os.path.dirname(target_path_normalized)

        # in case the upper directory does no exists and is valid
        if upper_directory_paths and not os.path.exists(upper_directory_paths):
            # creates all the upper directories
            os.makedirs(upper_directory_paths)

        # reads the zip file contents
        zip_file_contents = self.file.read(file_path)

        # opens the target file for writing
        target_file = open(complete_target_path, "wb")

        try:
            # writes the zip file contents into
            # the target file
            target_file.write(zip_file_contents)
        finally:
            # closes the target file
            target_file.close()

    def _extract_all_zip(self, target_path):
        # retrieves the member paths from the zip file
        member_paths = self.file.namelist()

        # iterates over all the member paths
        for member_path in member_paths:
            # extracts the member path to the target path
            self._extract_zip(member_path, target_path)

    def _normalize_file_path(self, file_path):
        """
        Normalizes the given file path using (if required)
        the default encoding.

        @type file_path: String
        @param file_path: The file path to be normalized.
        @rtype: String
        @return: The normalized file path.
        """

        # retrieves the file path type
        file_path_type = type(file_path)

        # in case the file path type is unicode
        if file_path_type == types.UnicodeType:
            # encodes the file path with the default encoding
            file_path_normalized = file_path.encode(DEFAULT_ENCODING)
        else:
            # the normalized file path is the file path itself
            file_path_normalized = file_path

        # returns the file path normalized
        return file_path_normalized
