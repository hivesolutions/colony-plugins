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

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import build_automation_generator_exceptions

import colony.libs.string_buffer_util

BUILD_AUTOMATION_GENERATOR_VALUE = "build_automation_generator"
""" The build automation generator value """

DEFAULT_BUILD_AUTOMATION_GENERATOR_NAME = "packing"
""" The default build automation generator name """

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

class BuildAutomationGenerator:
    """
    The build automation generator class.
    """

    build_automation_generator_plugin = None
    """ The build automation generator plugin """

    build_automation_generator_handler_name_build_automation_generator_handler_plugin_map = {}
    """ The map associating the build automation generator handler name with the build automation generator handler plugin """

    def __init__(self, build_automation_generator_plugin):
        """
        Constructor of the class.

        @type build_automation_generator_plugin: BuildAutomationGeneratorPlugin
        @param build_automation_generator_plugin: The build automation generator plugin.
        """

        self.build_automation_generator_plugin = build_automation_generator_plugin

        self.build_automation_generator_handler_name_build_automation_generator_handler_plugin_map = {}

    def generate_plugin_build_automation(self, plugin_id, plugin_version, properties, file_path):
        """
        Generates a build automation file describing the structure
        and specification of the plugin with the given id and version.
        The file is generated using the plugin internal information and
        is stored in the given file path.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be used for
        build automation generation.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be used for
        build automation generation.
        @type properties: Dictionary
        @param properties: The properties for plugin build automation generation.
        @type file_path: String
        @param file_path: The path to store the file being generated.
        """

        # retrieves the plugin build automation string
        plugin_build_automation_string = self._get_plugin_build_automation_string(plugin_id, plugin_version, properties)

        # encodes the plugin build automation string
        plugin_build_automation_string_encoded = plugin_build_automation_string.encode(DEFAULT_ENCODING)

        # opens the file
        file = open(file_path, "wb")

        try:
            # writes the plugin build automation string encoded to the file
            file.write(plugin_build_automation_string_encoded)
        finally:
            # closes the file
            file.close()

    def generate_plugin_build_automation_file_buffer(self, plugin_id, plugin_version, properties):
        """
        Generates a build automation file describing the structure
        and specification of the plugin with the given id and version.
        The file is generated using the plugin internal information and
        is returned in a file buffer.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be used for
        build automation generation.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be used for
        build automation generation.
        @type properties: Dictionary
        @param properties: The properties for plugin build automation generation.
        @rtype: File
        @return: The generated build automation file.
        """

        # retrieves the plugin build automation string
        plugin_build_automation_string = self._get_plugin_build_automation_string(plugin_id, plugin_version, properties)

        # encodes the plugin build automation string
        plugin_build_automation_string_encoded = plugin_build_automation_string.encode(DEFAULT_ENCODING)

        # initializes the string buffer
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # writes the plugin build automation string encoded
        string_buffer.write(plugin_build_automation_string_encoded)

        # returns the string buffer
        return string_buffer

    def build_automation_generator_handler_load(self, build_automation_generator_handler_plugin):
        """
        Loads the given build automation generator handler plugin.

        @type build_automation_generator_handler_plugin: Plugin
        @param build_automation_generator_handler_plugin: The build automation generator handler plugin to be loaded.
        """

        # retrieves build automation generator handler plugin name
        build_automation_generator_handler_name = build_automation_generator_handler_plugin.get_build_automation_generator_handler_name()

        # sets the build automation generator handler plugin in the build automation generator handler name
        # build automation generator handler plugin map
        self.build_automation_generator_handler_name_build_automation_generator_handler_plugin_map[build_automation_generator_handler_name] = build_automation_generator_handler_plugin

    def build_automation_generator_handler_unload(self, build_automation_generator_handler_plugin):
        """
        Unloads the given build automation generator handler plugin.

        @type build_automation_generator_handler_plugin: Plugin
        @param build_automation_generator_handler_plugin: The build_automation generator handler plugin to be loaded.
        """

        # retrieves build automation generator handler plugin name
        build_automation_generator_handler_name = build_automation_generator_handler_plugin.get_build_automation_generator_handler_name()

        # removes the build automation generator handler plugin from the build automation generator handler name
        # build automation generator handler plugin map
        del self.build_automation_generator_handler_name_build_automation_generator_handler_plugin_map[build_automation_generator_handler_name]

    def _get_plugin_build_automation_string(self, plugin_id, plugin_version, properties):
        # retrieves the plugin manager
        plugin_manager = self.build_automation_generator_plugin.manager

        # retrieves the build automation generator handler name
        build_automation_generator_handler_name = properties.get(BUILD_AUTOMATION_GENERATOR_VALUE, DEFAULT_BUILD_AUTOMATION_GENERATOR_NAME)

        # retrieves the build automation generator handler plugin
        build_automation_generator_handler_plugin = self._get_build_automation_generator_handler_plugin_by_build_automation_generator_handler_name(build_automation_generator_handler_name)

        # retrieves the plugin from the plugin id and version
        plugin = plugin_manager._get_plugin_by_id_and_version(plugin_id, plugin_version)

        # retrieves the plugin build automation string from the plugin
        plugin_build_automation_string = build_automation_generator_handler_plugin.generate_plugin_build_automation(plugin, properties)

        # returns the plugin build automation string
        return plugin_build_automation_string

    def _get_build_automation_generator_handler_plugin_by_build_automation_generator_handler_name(self, build_automation_generator_handler_name):
        """
        Retrieves the build automation generator handler plugin for the given
        build automation generator handler name.

        @type build_automation_generator_handler_name: String
        @param build_automation_generator_handler_name: The build automation generator handler name to retrieve
        the build automation generator handler plugin.
        @rtype: Plugin
        @return: The build automation generator handler plugin.
        """

        # in case the build automation generator handler name does not exist in the
        # build automation generator handler name build automation generator handler plugin map
        if not build_automation_generator_handler_name in self.build_automation_generator_handler_name_build_automation_generator_handler_plugin_map:
            # raises the build automation generator handler not available exception
            raise build_automation_generator_exceptions.BuildAutomationGeneratorHandlerNotAvailable("the build automation generator handler is not available: " + build_automation_generator_handler_name)

        # retrieves the build automation generator handler plugin
        build_automation_generator_handler_plugin = self.build_automation_generator_handler_name_build_automation_generator_handler_plugin_map[build_automation_generator_handler_name]

        # returns the build automation generator handler plugin
        return build_automation_generator_handler_plugin
