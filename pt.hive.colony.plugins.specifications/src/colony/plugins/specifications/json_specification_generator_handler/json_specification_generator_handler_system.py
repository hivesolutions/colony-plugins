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

SPECIFICATION_GENERATOR_HANDLER_NAME = "json"
""" The specification genertor handler name """

TEMPLATE_FILE_PATH = "specifications/json_specification_generator_handler/resources/plugin_specification.json.tpl"
""" The template file path """

class JsonSepecificationGeneratorHandler:
    """
    The json specification generator handler class.
    """

    json_specification_generator_handler_plugin = None
    """ The json specification generator handler """

    def __init__(self, json_specification_generator_handler_plugin):
        """
        Constructor of the class.

        @type json_specification_generator_handler_plugin: JsonSpecificationGeneratorHandlerPlugin
        @param json_specification_generator_handler_plugin: The json specification generator handler plugin.
        """

        self.json_specification_generator_handler_plugin = json_specification_generator_handler_plugin

    def get_specification_generator_handler_name(self):
        return SPECIFICATION_GENERATOR_HANDLER_NAME

    def generate_plugin_specification(self, plugin, properties):
        """
        Generates a specification string describing the structure
        and specification of the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin to be used to generate plugin specification.
        @type properties: Dictionary
        @param properties: The properties for plugin specification generation.
        @rtype: String
        @return: The generated plugin specification string.
        """

        # retrieves the plugin manager
        plugin_manager = self.json_specification_generator_handler_plugin.manager

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.json_specification_generator_handler_plugin.template_engine_manager_plugin

        # retrieves the json specification generator handler plugin path
        json_specification_generator_handler_plugin_path = plugin_manager.get_plugin_path_by_id(self.json_specification_generator_handler_plugin.id)

        # creates the full template file path
        template_file_path = json_specification_generator_handler_plugin_path + "/" + TEMPLATE_FILE_PATH

        # parses the template file path
        template_file = template_engine_manager_plugin.parse_file_path(template_file_path)

        # generates the specification for the plugin
        specification_map = self._generate_specification_map(plugin)

        # assigns the specification to the template file
        template_file.assign("specification", specification_map)

        # processes the template file
        processed_template_file = template_file.process()

        # decodes the processed template file into a unicode object
        processed_template_file_decoded = processed_template_file.decode("Cp1252")

        # returns the processed template file decoded (plugin specification)
        return processed_template_file_decoded

    def _generate_specification_map(self, plugin):
        """
        Generates the specification map for the given plugin.
        The specification map contains all the information
        necessary to generate the specification file for the plugin.

        @type plugin: Plugin
        @param plugin: The plugin to be used to generate
        the specification map.
        @rtype: Dictionary
        @return: The specification map.
        """

        # creates the specification map
        specification_map = {}

        # sets the specification map attributes
        specification_map["id"] = plugin.id
        specification_map["version"] = plugin.version

        # returns the specification map
        return specification_map
