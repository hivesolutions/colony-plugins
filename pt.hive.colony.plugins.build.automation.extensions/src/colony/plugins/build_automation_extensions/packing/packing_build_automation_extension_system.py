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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.map_util

import packing_build_automation_extension_exceptions

BUNDLES_DIRECTORY_VALUE = "bundles_directory"
""" The bundles directory value """

PLUGINS_DIRECTORY_VALUE = "plugins_directory"
""" The plugins directory value """

LIBRARIES_DIRECTORY_VALUE = "libraries_directory"
""" The libraries directory value """

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

LIBRARY_VALUE = "library"
""" The library value """

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

        # retrieves the libraries directory
        libraries_directory = build_properties[LIBRARIES_DIRECTORY_VALUE]

        # retrieves the type
        type = parameters.get(TYPE_VALUE, PLUGIN_VALUE)

        # retrieves the specification file
        specification_file = parameters[SPECIFICATION_FILE_VALUE]

        # creates the "main" specification
        specification = {TYPE_VALUE : type, SPECIFICATION_FILE_VALUE : specification_file}

        # retrieves the resource specifications
        resource_specifications = parameters.get(RESOURCES_SPECIFICATIONS_VALUE, {})

        # retrieves the resource specifications
        specifications = colony.libs.map_util.map_get_values(resource_specifications, SPECIFICATION_VALUE)

        # packs the main specification
        self._pack_specification(specification, bundles_directory, plugins_directory, libraries_directory, logger)

        # iterates over all the specifications
        for specification in specifications:
            # packs the (resource) specification
            self._pack_specification(specification, bundles_directory, plugins_directory, libraries_directory, logger)

        # returns true (success)
        return True

    def _pack_specification(self, specification, bundles_directory, plugins_directory, libraries_directory, logger):
        # retrieves the main packing manager plugin
        main_packing_manager_plugin = self.packing_build_automation_extension_plugin.main_packing_manager_plugin

        # retrieves the specification type
        type = specification[TYPE_VALUE]

        # retrieves the specification specification file
        specification_file = specification[SPECIFICATION_FILE_VALUE]

        # creates the file paths list
        file_paths_list = [specification_file]

        # in case the packing type is bundle
        if type == BUNDLE_VALUE:
            target_path = bundles_directory
        # in case the packing type is plugin
        elif type == PLUGIN_VALUE:
            target_path = plugins_directory
        elif type == LIBRARY_VALUE:
            target_path = libraries_directory
        else:
            # raises the invalid packing type exception
            raise packing_build_automation_extension_exceptions.InvalidPackingTypeException(type)

        # creates the properties map for the directory packing
        properties = {TARGET_PATH_VALUE : target_path,
                      PLUGINS_PATH_VALUE : plugins_directory}

        # print an info message
        logger.info("Packing files using specification file %s into %s" % (specification_file, target_path))

        # packs the directory
        main_packing_manager_plugin.pack_files(file_paths_list, properties, COLONY_VALUE)
