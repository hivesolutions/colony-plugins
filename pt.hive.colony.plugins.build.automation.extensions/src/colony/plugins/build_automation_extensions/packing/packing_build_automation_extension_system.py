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

import colony.libs.map_util
import colony.libs.crypt_util

import packing_build_automation_extension_exceptions

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

BUNDLES_DIRECTORY_VALUE = "bundles_directory"
""" The bundles directory value """

PLUGINS_DIRECTORY_VALUE = "plugins_directory"
""" The plugins directory value """

CONTAINERS_DIRECTORY_VALUE = "containers_directory"
""" The containers directory value """

TARGET_PATH_VALUE = "target_path"
""" The target path value """

PLUGINS_PATH_VALUE = "plugins_path"
""" The plugins path value """

COLONY_VALUE = "colony"
""" The colony value """

SPECIFICATION_FILE_VALUE = "specification_file"
""" The specification file value """

SPECIFICATION_VALUE = "specification"
""" The specification value """

RESOURCES_SPECIFICATIONS_VALUE = "resource_specifications"
""" The resource specifications value """

TYPE_VALUE = "type"
""" The type value """

BUNDLE_VALUE = "bundle"
""" The bundle value """

PLUGIN_VALUE = "plugin"
""" The plugin value """

CONTAINER_VALUE = "container"
""" The container value """

ID_VALUE = "id"
""" The id value """

VERSION_VALUE = "version"
""" The version value """

DEPENDENCIES_VALUE = "dependencies"
""" The dependencies value """

HASH_DIGEST_VALUE = "hash_digest"
""" The hash digest value """

PACKED_BUNDLES_VALUE = "packed_bundles"
""" The packed bundles value """

PACKED_PLUGINS_VALUE = "packed_plugins"
""" The packed plugins value """

PACKED_CONTAINERS_VALUE = "packed_containers"
""" The packed containers value """

PACKAGE_PACKED_KEY_MAP = {
    BUNDLE_VALUE : PACKED_BUNDLES_VALUE,
    PLUGIN_VALUE : PACKED_PLUGINS_VALUE,
    CONTAINER_VALUE : PACKED_CONTAINERS_VALUE
}
""" The map associating the package file with the packed key """

PACKAGE_FILE_EXTENSION_MAP = {
    BUNDLE_VALUE : ".cbx",
    PLUGIN_VALUE : ".cpx",
    CONTAINER_VALUE : ".ccx"
}
""" The map associating the package file with the extension """

class PackingBuildAutomationExtension:
    """
    The packing build automation extension class.
    """

    packing_build_automation_extension_plugin = None
    """ The packing build automation extension plugin """

    def __init__(self, packing_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type packing_build_automation_extension_plugin: PackingBuildAutomationExtensionPlugin
        @param packing_build_automation_extension_plugin: The packing build automation extension plugin.
        """

        self.packing_build_automation_extension_plugin = packing_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # retrieves the build properties
        build_properties = build_automation_structure.get_all_build_properties()

        # retrieves the bundles directory
        bundles_directory = build_properties[BUNDLES_DIRECTORY_VALUE]

        # retrieves the plugins directory
        plugins_directory = build_properties[PLUGINS_DIRECTORY_VALUE]

        # retrieves the containers directory
        containers_directory = build_properties[CONTAINERS_DIRECTORY_VALUE]

        # retrieves the type
        type = parameters.get(TYPE_VALUE, PLUGIN_VALUE)

        # retrieves the specification file
        specification_file = parameters[SPECIFICATION_FILE_VALUE]

        # creates the "main" specification
        specification = {
            TYPE_VALUE : type,
            SPECIFICATION_FILE_VALUE : specification_file
        }

        # retrieves the resource specifications
        resource_specifications = parameters.get(RESOURCES_SPECIFICATIONS_VALUE, {})

        # retrieves the resource specifications
        specifications = colony.libs.map_util.map_get_values(resource_specifications, SPECIFICATION_VALUE)

        # packs the main specification
        self._pack_specification(specification, bundles_directory, plugins_directory, containers_directory, build_automation_structure, logger)

        # iterates over all the specifications
        for specification in specifications:
            # packs the (resource) specification
            self._pack_specification(specification, bundles_directory, plugins_directory, containers_directory, build_automation_structure, logger)

        # returns true (success)
        return True

    def _pack_specification(self, specification, bundles_directory, plugins_directory, containers_directory, build_automation_structure, logger):
        # retrieves the main packing manager plugin
        main_packing_manager_plugin = self.packing_build_automation_extension_plugin.main_packing_manager_plugin

        # retrieves the build automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # retrieves the specification type
        type = specification[TYPE_VALUE]

        # retrieves the specification specification file
        specification_file = specification[SPECIFICATION_FILE_VALUE]

        # creates the file paths list
        file_paths_list = [
            specification_file
        ]

        # in case the packing type is bundle
        if type == BUNDLE_VALUE:
            target_path = bundles_directory
        # in case the packing type is plugin
        elif type == PLUGIN_VALUE:
            target_path = plugins_directory
        # in case the packaing type is container
        elif type == CONTAINER_VALUE:
            target_path = containers_directory
        # otherwise it must be invalid
        else:
            # raises the invalid packing type exception
            raise packing_build_automation_extension_exceptions.InvalidPackingTypeException(type)

        # creates the properties map for the directory packing
        properties = {
            TARGET_PATH_VALUE : target_path,
            PLUGINS_PATH_VALUE : plugins_directory
        }

        # prints an info message
        logger.info("Packing files using specification file %s into %s" % (specification_file, target_path))

        # packs the files into the directory
        main_packing_manager_plugin.pack_files(file_paths_list, properties, COLONY_VALUE)

        # updates the build automation structure with the new packing
        self._update_build_automation_structure(type, specification_file, target_path, build_automation_structure_runtime)

    def _update_build_automation_structure(self, type, specification_file, target_path, build_automation_structure_runtime):
        # loads the specification from the specification file
        specification = self._load_specification(specification_file)

        # retrieves the packed items key frm the type
        packed_items_key = PACKAGE_PACKED_KEY_MAP.get(type, None)

        # in case the packed items key does not exist in the build automation
        # structure runtime properties a packed items list must be created
        if not packed_items_key in build_automation_structure_runtime.global_properties:
            # sets the initial list for the packed items list
            build_automation_structure_runtime.global_properties[packed_items_key] = []

        # retrieves the packed items list from the build automation structure
        # runtime properties
        packed_items_list = build_automation_structure_runtime.global_properties[packed_items_key]

        # retrieves the specification id, version and dependencies
        specification_id = specification[ID_VALUE]
        specification_version = specification[VERSION_VALUE]
        specification_dependencies = specification[DEPENDENCIES_VALUE]

        # retrieves the package file extension for the type
        package_file_extension = PACKAGE_FILE_EXTENSION_MAP.get(type, None)

        # creates the package file path from the concatenation of the id, version and extension
        package_file_name = specification_id + "_" + specification_version + package_file_extension
        package_file_path = os.path.join(target_path, package_file_name)

        # generates the hash digest map for the package file
        hash_digest_map = colony.libs.crypt_util.generate_hash_digest_map(package_file_path)

        # creates the packed item from the specification id, version,
        # dependencies and hash digest
        packed_item = {
            ID_VALUE : specification_id,
            VERSION_VALUE : specification_version,
            DEPENDENCIES_VALUE : specification_dependencies,
            HASH_DIGEST_VALUE : hash_digest_map
        }

        # checks if the packed item already exists in the
        # packed items list
        packed_item_exists = packed_item in packed_items_list

        # adds the packed item to the packed items list
        # in case it does not already exists (avoids duplicates)
        not packed_item_exists and packed_items_list.append(packed_item)

    def _load_specification(self, specification_file_path):
        # retrieves the json plugin
        json_plugin = self.packing_build_automation_extension_plugin.json_plugin

        # opens the specification file
        specification_file = open(specification_file_path)

        try:
            # retrieves the specification file contents
            specification_file_contents = specification_file.read()

            # decodes the specification file contents using
            # the default encoding
            specification_file_contents = specification_file_contents.decode(DEFAULT_ENCODING)
        finally:
            # closes the specification file
            specification_file.close()

        # retrieves the specification from the specification file contents
        specification = json_plugin.loads(specification_file_contents)

        # returns the specification
        return specification
