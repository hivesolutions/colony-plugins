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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import specification_generator_exceptions

import colony.libs.string_buffer_util

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

SPECIFICATION_GENERATOR_VALUE = "specification_generator"
""" The specification generator value """

DEFAULT_SPECIFICATION_GENERATOR_NAME = "json"
""" The default specification generator name """

class SepecificationGenerator:
    """
    The specification generator class.
    """

    specification_generator_plugin = None
    """ The specification generator plugin """

    specification_generator_handler_name_specification_generator_handler_plugin_map = {}
    """ The map associating the specification generator handler name with the specification generator handler plugin """

    def __init__(self, specification_generator_plugin):
        """
        Constructor of the class.

        @type specification_generator_plugin: SpecificationGeneratorPlugin
        @param specification_generator_plugin: The specification generator plugin.
        """

        self.specification_generator_plugin = specification_generator_plugin

        self.specification_generator_handler_name_specification_generator_handler_plugin_map = {}

    def generate_plugin_specification(self, plugin_id, plugin_version, properties, file_path):
        """
        Generates a specification file describing the structure
        and specification of the plugin with the given id and version.
        The file is generated using the plugin internal information and
        is stored in the given file path.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be used for
        specification generation.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be used for
        specification generation.
        @type properties: Dictionary
        @param properties: The properties for plugin specification generation.
        @type file_path: String
        @param file_path: The path to store the file being generated.
        """

        # retrieves the plugin specification string
        plugin_specification_string = self._get_plugin_specification_string(plugin_id, plugin_version, properties)

        # encodes the plugin specification string
        plugin_specification_string_encoded = plugin_specification_string.encode(DEFAULT_ENCODING)

        # opens the file
        file = open(file_path, "wb")

        try:
            # writes the plugin specification string encoded to the file
            file.write(plugin_specification_string_encoded)
        finally:
            # closes the file
            file.close()

    def generate_plugin_specification_file_buffer(self, plugin_id, plugin_version, properties):
        """
        Generates a specification file describing the structure
        and specification of the plugin with the given id and version.
        The file is generated using the plugin internal information and
        is returned in a file buffer.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be used for
        specification generation.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be used for
        specification generation.
        @type properties: Dictionary
        @param properties: The properties for plugin specification generation.
        @rtype: File
        @return: The generated specification file.
        """

        # retrieves the plugin specification string
        plugin_specification_string = self._get_plugin_specification_string(plugin_id, plugin_version, properties)

        # encodes the plugin specification string
        plugin_specification_string_encoded = plugin_specification_string.encode(DEFAULT_ENCODING)

        # initializes the string buffer
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # writes the plugin specification string encoded
        string_buffer.write(plugin_specification_string_encoded)

        # returns the string buffer
        return string_buffer

    def specification_generator_handler_load(self, specification_generator_handler_plugin):
        """
        Loads the given specification generator handler plugin.

        @type specification_generator_handler_plugin: Plugin
        @param specification_generator_handler_plugin: The specification generator handler plugin to be loaded.
        """

        # retrieves specification generator handler plugin name
        specification_generator_handler_name = specification_generator_handler_plugin.get_specification_generator_handler_name()

        # sets the specification generator handler plugin in the specification generator handler name
        # specification generator handler plugin map
        self.specification_generator_handler_name_specification_generator_handler_plugin_map[specification_generator_handler_name] = specification_generator_handler_plugin

    def specification_generator_handler_unload(self, specification_generator_handler_plugin):
        """
        Unloads the given specification generator handler plugin.

        @type specification_generator_handler_plugin: Plugin
        @param specification_generator_handler_plugin: The specification generator handler plugin to be loaded.
        """

        # retrieves specification generator handler plugin name
        specification_generator_handler_name = specification_generator_handler_plugin.get_specification_generator_handler_name()

        # removes the specification generator handler plugin from the specification generator handler name
        # specification generator handler plugin map
        del self.specification_generator_handler_name_specification_generator_handler_plugin_map[specification_generator_handler_name]

    def _get_plugin_specification_string(self, plugin_id, plugin_version, properties):
        # retrieves the plugin manager
        plugin_manager = self.specification_generator_plugin.manager

        # retrieves the specification generator handler name
        specification_generator_handler_name = properties.get(SPECIFICATION_GENERATOR_VALUE, DEFAULT_SPECIFICATION_GENERATOR_NAME)

        # retrieves the specification generator handler plugin
        specification_generator_handler_plugin = self._get_specification_generator_handler_plugin_by_specification_generator_handler_name(specification_generator_handler_name)

        # retrieves the plugin from the plugin id and version
        plugin = plugin_manager._get_plugin_by_id_and_version(plugin_id, plugin_version)

        # retrieves the plugin specification string from the plugin
        plugin_specification_string = specification_generator_handler_plugin.generate_plugin_specification(plugin, properties)

        # returns the plugin specification string
        return plugin_specification_string

    def _get_specification_generator_handler_plugin_by_specification_generator_handler_name(self, specification_generator_handler_name):
        """
        Retrieves the specification generator handler plugin for the given
        specification generator handler name.

        @type specification_generator_handler_name: String
        @param specification_generator_handler_name: The specification generator handler name to retrieve
        the specification generator handler plugin.
        @rtype: Plugin
        @return: The specification generator handler plugin.
        """

        # in case the specification generator handler name does not exist in the
        # specification generator handler name specification generator handler plugin map
        if not specification_generator_handler_name in self.specification_generator_handler_name_specification_generator_handler_plugin_map:
            # raises the specification generator handler not available exception
            raise specification_generator_exceptions.SpecificationGeneratorHandlerNotAvailable("the specification generator handler is not available: " + specification_generator_handler_name)

        # retrieves the specification generator handler plugin
        specification_generator_handler_plugin = self.specification_generator_handler_name_specification_generator_handler_plugin_map[specification_generator_handler_name]

        # returns the specification generator handler plugin
        return specification_generator_handler_plugin
