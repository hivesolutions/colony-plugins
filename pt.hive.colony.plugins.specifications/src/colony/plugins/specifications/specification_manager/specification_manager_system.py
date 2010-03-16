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

class SepecificationManager:
    """
    The specification manager class.
    """

    specification_manager_plugin = None
    """ The specification manager plugin """

    specification_parser_name_specification_parser_plugin = {}
    """ The map associating the specification parser name with the specification parser plugin """

    def __init__(self, specification_manager_plugin):
        """
        Constructor of the class.

        @type specification_manager_plugin: Plugin
        @param specification_manager_plugin: The specification manager plugin.
        """

        self.specification_manager_plugin = specification_manager_plugin

        self.specification_parser_name_specification_parser_plugin = {}

    def get_plugin_specification(self, file_path, properties):
        """
        Retrieves a structure describing the structure and specification
        of a plugin. This structure is created from the given file and
        using the given properties.

        @type file_path: String
        @param file_path: The path to the specification file.
        @type properties: Dictionary
        @param properties: The properties for the file parsing.
        """

        pass

    def specification_parser_load(self, specification_parser_plugin):
        """
        Loads the given specification parser plugin.

        @type specification_parser_plugin: Plugin
        @param specification_parser_plugin: The specification parser plugin to be loaded.
        """

        # retrieves specification parser plugin name
        specification_parser_name = specification_parser_plugin.get_specification_parser_name()

        # sets the specification parser plugin in the specification parser name
        # specification parser plugin
        self.specification_parser_name_specification_parser_plugin[specification_parser_name] = specification_parser_plugin

    def packing_service_unload(self, specification_parser_plugin):
        """
        Unloads the given specification parser plugin.

        @type specification_parser_plugin: Plugin
        @param specification_parser_plugin: The specification parser plugin to be loaded.
        """

        # retrieves specification parser plugin name
        specification_parser_name = specification_parser_plugin.get_specification_parser_name()

        # removes the specification parser plugin from the specification parser name
        # specification parser plugin
        self.specification_parser_name_specification_parser_plugin[specification_parser_name] = specification_parser_plugin
