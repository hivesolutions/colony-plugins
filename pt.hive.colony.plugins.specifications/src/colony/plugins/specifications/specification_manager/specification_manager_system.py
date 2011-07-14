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

import specification_manager_exceptions

SPECIFICATION_PARSER_VALUE = "specification_parser"
""" The specification parser value """

DEFAULT_SPECIFICATION_PARSER_NAME = "json"
""" The default specification parser name """

class SepecificationManager:
    """
    The specification manager class.
    """

    specification_manager_plugin = None
    """ The specification manager plugin """

    specification_parser_name_specification_parser_plugin_map = {}
    """ The map associating the specification parser name with the specification parser plugin """

    def __init__(self, specification_manager_plugin):
        """
        Constructor of the class.

        @type specification_manager_plugin: SpecificationManagerPlugin
        @param specification_manager_plugin: The specification manager plugin.
        """

        self.specification_manager_plugin = specification_manager_plugin

        self.specification_parser_name_specification_parser_plugin_map = {}

    def get_specification(self, file_path, properties):
        """
        Retrieves a structure describing the structure and specification
        of a colony packing file. This structure is created from the given file and
        using the given properties.

        @type file_path: String
        @param file_path: The path to the specification file.
        @type properties: Dictionary
        @param properties: The properties for the file parsing.
        """

        # retrieves the specification parser name
        specification_parser_name = properties.get(SPECIFICATION_PARSER_VALUE, DEFAULT_SPECIFICATION_PARSER_NAME)

        # retrieves the specification parser plugin
        specification_parser_plugin = self._get_specification_parser_plugin_by_specification_parser_name(specification_parser_name)

        # creates a new specification with the given file path
        specification = Specification(file_path)

        # forces the specification parser plugin to parser the specification
        specification_parser_plugin.parse_specification(specification)

        # returns the specification
        return specification

    def get_specification_file_buffer(self, file_buffer, properties):
        """
        Retrieves a structure describing the structure and specification
        of a colony packing file. This structure is created from the given
        file buffer and using the given properties.

        @type file_buffer: String
        @param file_buffer: The buffer to the specification file.
        @type properties: Dictionary
        @param properties: The properties for the file parsing.
        """

        # retrieves the specification parser name
        specification_parser_name = properties.get(SPECIFICATION_PARSER_VALUE, DEFAULT_SPECIFICATION_PARSER_NAME)

        # retrieves the specification parser plugin
        specification_parser_plugin = self._get_specification_parser_plugin_by_specification_parser_name(specification_parser_name)

        # creates a new specification with the given file buffer
        specification = Specification(None, file_buffer)

        # forces the specification parser plugin to parser the specification
        specification_parser_plugin.parse_specification(specification)

        # returns the specification
        return specification

    def specification_parser_load(self, specification_parser_plugin):
        """
        Loads the given specification parser plugin.

        @type specification_parser_plugin: Plugin
        @param specification_parser_plugin: The specification parser plugin to be loaded.
        """

        # retrieves specification parser plugin name
        specification_parser_name = specification_parser_plugin.get_specification_parser_name()

        # sets the specification parser plugin in the specification parser name
        # specification parser plugin map
        self.specification_parser_name_specification_parser_plugin_map[specification_parser_name] = specification_parser_plugin

    def specification_parser_unload(self, specification_parser_plugin):
        """
        Unloads the given specification parser plugin.

        @type specification_parser_plugin: Plugin
        @param specification_parser_plugin: The specification parser plugin to be unloaded.
        """

        # retrieves specification parser plugin name
        specification_parser_name = specification_parser_plugin.get_specification_parser_name()

        # removes the specification parser plugin from the specification parser name
        # specification parser plugin map
        del self.specification_parser_name_specification_parser_plugin_map[specification_parser_name]

    def _get_specification_parser_plugin_by_specification_parser_name(self, specification_parser_name):
        """
        Retrieves the specification parser plugin for the given
        specification parser name.

        @type specification_parser_name: String
        @param specification_parser_name: The specification parser name to retrieve
        the specification parser plugin.
        @rtype: Plugin
        @return: The specification parser plugin.
        """

        # in case the specification parser name does not exist in the
        # specification parser name specification parser plugin map
        if not specification_parser_name in self.specification_parser_name_specification_parser_plugin_map:
            # raises the specification parser not available exception
            raise specification_manager_exceptions.SpecificationParserNotAvailable("the specification parser is not available: " + specification_parser_name)

        # retrieves the specification parser plugin
        specification_parser_plugin = self.specification_parser_name_specification_parser_plugin_map[specification_parser_name]

        # returns the specification parser plugin
        return specification_parser_plugin

class Specification:
    """
    The specification class representing
    a plugin specification including the properties of it.
    """

    file_path = None
    """ The path to the specification file """

    file_buffer = None
    """ The buffer to the specification file """

    properties = {}
    """ The specification properties """

    def __init__(self, file_path = None, file_buffer = None):
        """
        Constructor of the class.

        @type file_path: String
        @param file_path: The path to the specification file.
        @type file_buffer: String
        @param file_buffer: The buffer to the specification file.
        """

        self.file_path = file_path
        self.file_buffer = file_buffer

        self.properties = {}

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, file_path):
        self.file_path = file_path

    def get_file_buffer(self):
        return self.file_buffer

    def set_file_buffer(self, file_buffer):
        self.file_buffer = file_buffer

    def get_property(self, property_name, property_value_default = None):
        return self.properties.get(property_name, property_value_default)

    def set_property(self, property_name, property_value):
        self.properties[property_name] = property_value
