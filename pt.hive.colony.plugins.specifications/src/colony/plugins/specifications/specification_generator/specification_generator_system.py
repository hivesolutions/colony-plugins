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

        @type specification_generator_plugin: Plugin
        @param specification_generator_plugin: The specification generator plugin.
        """

        self.specification_generator_plugin = specification_generator_plugin

        self.specification_generator_handler_name_specification_generator_handler_plugin_map = {}

    def generate_plugin_specification(self, plugin_id, plugin_version, file_path, properties):
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
        @type file_path: String
        @param file_path: The to store the file being generated.
        @type properties: Dictionary
        @param properties: The properties for plugin specification generation.
        """

        pass

    def generate_specification_file_buffer(self, plugin_id, plugin_version, properties):
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
        """

        pass

    def specification_specification_generator_handler_load(self, specification_generator_handler_plugin):
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

    def specification_specification_generator_handler_unload(self, specification_generator_handler_plugin):
        """
        Unloads the given specification parser plugin.

        @type specification_generator_handler_plugin: Plugin
        @param specification_generator_handler_plugin: he specification generator handler plugin to be loaded.
        """

        # retrieves specification generator handler plugin name
        specification_generator_handler_name = specification_generator_handler_plugin.get_specification_generator_handler_name()

        # removes the specification generator handler plugin from the specification generator handler name
        # specification generator handler plugin map
        del self.specification_generator_handler_name_specification_generator_handler_plugin_map[specification_generator_handler_name]
