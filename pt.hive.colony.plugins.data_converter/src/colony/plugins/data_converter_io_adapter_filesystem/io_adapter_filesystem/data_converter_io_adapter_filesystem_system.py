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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import re

import data_converter_io_adapter_filesystem_exceptions

DIRECTORY_PATHS_VALUE = "directory_paths"
""" The directory paths value """

INPUT_ATTRIBUTE_HANDLERS_VALUE = "input_attribute_handlers"
""" The input attribute handlers value """

INPUT_ENTITY_HANDLERS_VALUE = "input_entity_handlers"
""" The input entity handlers value """

ENTITY_NAME_PATH_REGEX_MAP_VALUE = "entity_name_path_regex_map"
""" The entity name path regex map value """

class IoAdapterFilesystem:
    """
    Input output adapter used to load and save data converter intermediate
    structures to and from filesystem format.
    """

    io_adapter_filesystem_plugin = None
    """ Io adapter filesystem plugin """

    def __init__(self, io_adapter_filesystem_plugin):
        """
        Constructor of the class.

        @type io_adapter_filesystem_plugin: IoAdapterFilesystemPlugin
        @param io_adapter_filesystem_plugin: Input output adapter filesystem plugin.
        """

        self.io_adapter_filesystem_plugin = io_adapter_filesystem_plugin

    def load_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Populates the intermediate structure with data retrieved from the
        filesystem source specified in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure where to
        load the data into.
        @type options: Dictionary
        @param options: Options used to determine how to load data into the
        provided intermediate structure.
        """

        # extracts the mandatory options
        directory_paths = options[DIRECTORY_PATHS_VALUE]
        entity_name_path_regex_map = options[ENTITY_NAME_PATH_REGEX_MAP_VALUE]

        # compiles the regular expressions
        entity_name_path_regex_map = dict([(entity_name, re.compile(path_regex)) for entity_name, path_regex in entity_name_path_regex_map.items()])

        # indexes the files in the inside the specified directory paths
        file_name_directory_path_map = self.index_files(directory_paths)

        # loads the files into the specified directory contents
        # into the intermediate structure
        for file_name, directory_path in file_name_directory_path_map.iteritems():
            file_path = os.path.join(directory_path, file_name)

            # retrieves the names of the entities that must be created for this file
            entity_names = [entity_name for entity_name, path_regex in entity_name_path_regex_map.items() if path_regex.match(file_path)]

            # creates an entity representing the file in case it exists
            if os.path.exists(file_path):
                self.load_intermediate_structure_entities(intermediate_structure, options, file_path, entity_names)

    def load_intermediate_structure_entities(self, intermediate_structure, options, file_path, entity_names):
        # extracts the non-mandatory options
        input_entity_handlers = options.get(INPUT_ENTITY_HANDLERS_VALUE, [])
        input_attribute_handlers = options.get(INPUT_ATTRIBUTE_HANDLERS_VALUE, [])

        # creates entities representing this file
        for entity_name in entity_names:

            # creates the entity used to represent the file
            entity = intermediate_structure.create_entity(entity_name)

            # retrieves file statistics
            file_name = os.path.basename(file_path)
            file_name_without_extension, extension_name = os.path.splitext(file_name)
            file_size = os.path.getsize(file_path)
            creation_time = os.path.getctime(file_path)
            last_change_time = os.path.getctime(file_path)
            last_access_time = os.path.getatime(file_path)

            # creates a file entity and sets its attributes
            entity.set_attribute("name", file_name)
            entity.set_attribute("name_without_extension", file_name_without_extension)
            entity.set_attribute("extension", extension_name)
            entity.set_attribute("path", file_path)
            entity.set_attribute("size", file_size)
            entity.set_attribute("creation_time", creation_time)
            entity.set_attribute("last_change_time", last_change_time)
            entity.set_attribute("last_access_time", last_access_time)

            # passes the data through the specified input attribute handlers
            attribute_name_value_map = entity.get_attributes()
            attribute_values = attribute_name_value_map.values()
            for attribute_value in attribute_values:
                for input_attribute_handler in input_attribute_handlers:
                    attribute_value = input_attribute_handler(intermediate_structure, entity, attribute_value)

            # passes the entity through the specified input entity handlers
            for input_entity_handler in input_entity_handlers:
                entity = input_entity_handler(intermediate_structure, entity)

    def save_intermediate_structure(self, configuration, intermediate_structure, options):
        """
        Saves the intermediate structure to a file in filesystem format at the location
        and with characteristics defined in the options.

        @type configuration: DataConverterConfiguration
        @param configuration: The data converter configuration currently being used.
        @type intermediate_structure: IntermediateStructure
        @param intermediate_structure: Intermediate structure one wants to save.
        @type options: Dictionary
        @param options: Options used to determine how to save the intermediate
        structure into filesystem format.
        """

        raise data_converter_io_adapter_filesystem_exceptions.IoAdapterFilesystemMethodNotImplemented()

    def index_files(self, directory_paths):
        """
        Crawls the provided directories searching for files and indexing
        their names to their directory path.

        @type directory_paths: List
        @param directory_paths: List with directory paths where to search for tables.
        @rtype: Dictionary
        @return: Map associating the names of the discovered files with the
        paths of the directories they are contained in.
        """

        file_name_directory_path_map = {}

        # crawls the specified directory paths indexing the discovered files
        for directory_path in directory_paths:
            for root_path, _directories, files in os.walk(directory_path, topdown = True):
                for file_name in files:
                    file_name_directory_path_map[file_name] = root_path

        return file_name_directory_path_map
