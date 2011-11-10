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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import gzip

import colony.libs.path_util

TARGET_DIRECTORY_VALUE = "target_directory"
""" The target directory value """

BUNDLES_DIRECTORY_VALUE = "bundles_directory"
""" The bundles directory value """

PLUGINS_DIRECTORY_VALUE = "plugins_directory"
""" The plugins directory value """

CONTAINERS_DIRECTORY_VALUE = "containers_directory"
""" The containers directory value """

TARGET_VALUE = "target"
""" The target value """

REPOSITORY_NAME_VALUE= "repository_name"
""" The repository name value """

REPOSITORY_DESCRIPTION = "repository_description"
""" The repository description value """

REPOSITORY_LAYOUT = "repository_layout"
""" The repository layout value """

PACKED_BUNDLES_VALUE = "packed_bundles"
""" The packed bundles value """

PACKED_PLUGINS_VALUE = "packed_plugins"
""" The packed plugins value """

PACKED_CONTAINERS_VALUE = "packed_containers"
""" The packed containers value """

BUNDLE_EXTENSION_VALUE = ".cbx"
""" The bundle extension value """

PLUGIN_EXTENSION_VALUE = ".cpx"
""" The plugin extension value """

CONTAINER_EXTENSION_VALUE = ".ccx"
""" The container extension value """

COLONY_VALUE = "colony"
""" The colony value """

BUNDLES_VALUE = "bundles"
""" The bundles value """

PLUGINS_VALUE = "plugins"
""" The plugins value """

CONTAINERS_VALUE = "containers"
""" The containers value """

ID_VALUE = "id"
""" The id value """

VERSION_VALUE = "version"
""" The version value """

DEFAULT_REPOSITORY_DESCRIPTOR_NAME = "repository_descriptor.xml"
""" The default repository descriptor name """

class ColonyRepositoryGeneratorBuildAutomationExtension:
    """
    The colony repository generator build automation extension class.
    """

    colony_repository_generator_build_automation_extension_plugin = None
    """ The colony repository generator build automation extension plugin """

    def __init__(self, colony_repository_generator_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type colony_repository_generator_build_automation_extension_plugin: ColonyRepositoryGeneratorBuildAutomationExtensionPlugin
        @param colony_repository_generator_build_automation_extension_plugin: The colony repository generator build automation extension plugin.
        """

        self.colony_repository_generator_build_automation_extension_plugin = colony_repository_generator_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # retrieves the repository descriptor generator plugin
        repository_descriptor_generator_plugin = self.colony_repository_generator_build_automation_extension_plugin.repository_descriptor_generator_plugin

        # retrieves the build automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the target directory
        target_directory = build_properties[TARGET_DIRECTORY_VALUE]

        # retrieves the bundles directory
        bundles_directory = build_properties[BUNDLES_DIRECTORY_VALUE]

        # retrieves the plugins directory
        plugins_directory = build_properties[PLUGINS_DIRECTORY_VALUE]

        # retrieves the containers directory
        containers_directory = build_properties[CONTAINERS_DIRECTORY_VALUE]

        # retrieves the repository name
        repository_name = parameters[REPOSITORY_NAME_VALUE]

        # retrieves the repository description
        repository_description = parameters[REPOSITORY_DESCRIPTION]

        # retrieves the repository layout
        repository_layout = parameters[REPOSITORY_LAYOUT]

        # retrieves the packed bundles, plugins and containers from
        # the build automation structure runtime
        packed_bundles = build_automation_structure_runtime.global_properties.get(PACKED_BUNDLES_VALUE, [])
        packed_plugins = build_automation_structure_runtime.global_properties.get(PACKED_PLUGINS_VALUE, [])
        packed_containers = build_automation_structure_runtime.global_properties.get(PACKED_CONTAINERS_VALUE, [])

        # retrieves the target
        target = parameters.get(TARGET_VALUE, target_directory)

        # creates the full target directory appending the colony plugins
        # suffix value
        full_target_directory = target + "/" + COLONY_VALUE

        # in case the full target directory does not exist
        if not os.path.exists(full_target_directory):
            # cretes the full target directory
            os.makedirs(full_target_directory)

        # creates the repository descriptor file path
        repository_descriptor_file_path = full_target_directory + "/" + DEFAULT_REPOSITORY_DESCRIPTOR_NAME

        # generates the repository descriptor file using the given artifacts
        repository_descriptor_generator_plugin.generate_repository_descriptor_file_artifacts(repository_descriptor_file_path, repository_name, repository_description, repository_layout, packed_bundles, packed_plugins, packed_containers)

        # compresses the repository descriptor
        self._compress_repository_descriptor(repository_descriptor_file_path)

        # processes the bundles copying them to the repository directory
        self._process_bundles(packed_bundles, bundles_directory, full_target_directory)

        # processes the plugins copying them to the repository directory
        self._process_plugins(packed_plugins, plugins_directory, full_target_directory)

        # processes the containers copying them to the repository directory
        self._process_containers(packed_containers, containers_directory, full_target_directory)

        # returns true (success)
        return True

    def _compress_repository_descriptor(self, repository_descriptor_file_path):
        # creates the repository descriptor gzip file path
        repository_descriptor_gzip_file_path = repository_descriptor_file_path + ".gz"

        # opens the repository descriptor file
        repository_descriptor_file = open(repository_descriptor_file_path, "rb")

        try:
            # retrieves the repository descriptor contents
            repository_descriptor_contents = repository_descriptor_file.read()
        finally:
            # closes the repository descriptor file
            repository_descriptor_file.close()

        # opens the repository descriptor gzip file
        repository_descriptor_gzip_file = gzip.open(repository_descriptor_gzip_file_path, "wb")

        try:
            # writes the repository descriptor contents to the
            # compressed (gzip) file
            repository_descriptor_gzip_file.write(repository_descriptor_contents)
        finally:
            # closes the repository descriptor gzip file
            repository_descriptor_gzip_file.close()

    def _process_bundles(self, packed_bundles, bundles_directory, full_target_directory):
        # creates the full bundles directory
        full_bundles_directory = full_target_directory + "/" + BUNDLES_VALUE

        # in case the full bundles directory does not exist
        if not os.path.exists(full_bundles_directory):
            # creates the full bundles directory
            os.makedirs(full_bundles_directory)

        # iterates over all the packed bundles to copy the files
        for packed_bundle in packed_bundles:
            # installs (deploy) the bundle to the target path
            self._deploy_packed_item(packed_bundle, BUNDLE_EXTENSION_VALUE, bundles_directory, full_bundles_directory)

    def _process_plugins(self, packed_plugins, plugins_directory, full_target_directory):
        # creates the full plugins directory
        full_plugins_directory = full_target_directory + "/" + PLUGINS_VALUE

        # in case the full plugins directory does not exist
        if not os.path.exists(full_plugins_directory):
            # creates the full plugins directory
            os.makedirs(full_plugins_directory)

        # iterates over all the packed plugins to copy the files
        for packed_plugin in packed_plugins:
            # installs (deploy) the plugin to the target path
            self._deploy_packed_item(packed_plugin, PLUGIN_EXTENSION_VALUE, plugins_directory, full_plugins_directory)

    def _process_containers(self, packed_containers, containers_directory, full_target_directory):
        # creates the full containers directory
        full_containers_directory = full_target_directory + "/" + CONTAINERS_VALUE

        # in case the full containers directory does not exist
        if not os.path.exists(full_containers_directory):
            # creates the full containers directory
            os.makedirs(full_containers_directory)

        # iterates over all the packed containers to copy the files
        for packed_container in packed_containers:
            # installs (deploy) the container to the target path
            self._deploy_packed_item(packed_container, CONTAINER_EXTENSION_VALUE, containers_directory, full_containers_directory)

    def _deploy_packed_item(self, packed_item, packed_item_extension, packed_item_directoy, full_packed_item_directory):
        # retrieves the packed item id and version
        packed_item_id = packed_item[ID_VALUE]
        packed_item_version = packed_item[VERSION_VALUE]

        # creates the packed item file name from the packed item id and version
        packed_item_file_name = packed_item_id + "_" + packed_item_version + packed_item_extension

        # creates the packed item file paths
        packed_item_file_path = packed_item_directoy + "/" + packed_item_file_name
        packed_item_target_file_path = full_packed_item_directory + "/" + packed_item_file_name

        # in case the source packed item path does not exists
        if not os.path.exists(packed_item_file_path):
            # returns immediately
            return

        # copies the packed item file from the packed item directory to the repository directory
        colony.libs.path_util.copy_file(packed_item_file_path, packed_item_target_file_path)
