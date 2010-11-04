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

import os

import colony.base.plugin_system
import colony.libs.string_buffer_util

DEFAULT_ENCODING = "Cp1252"
""" The default encoding """

SPECIFICATION_GENERATOR_HANDLER_NAME = "json"
""" The specification generator handler name """

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
        template_file = template_engine_manager_plugin.parse_file_path_encoding(template_file_path, DEFAULT_ENCODING)

        # generates the specification map for the plugin
        specification_map = self._generate_specification_map(plugin)

        # assigns the specification to the template file
        template_file.assign("specification", specification_map)

        # processes the template file
        processed_template_file = template_file.process()

        # returns the processed template file (plugin specification)
        return processed_template_file

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
        specification_map["platform"] = "python"
        specification_map["sub_platforms"] = self._serialize_sub_platforms(plugin.platforms)
        specification_map["id"] = plugin.id
        specification_map["name"] = plugin.name
        specification_map["short_name"] = plugin.short_name
        specification_map["description"] = plugin.description
        specification_map["version"] = plugin.version
        specification_map["author"] = plugin.author
        specification_map["capabilities"] = self._serialize_capabilities(plugin.capabilities)
        specification_map["capabilities_allowed"] = self._serialize_capabilities(plugin.capabilities_allowed)
        specification_map["dependencies"] = self._serialize_dependencies(plugin.dependencies)
        specification_map["main_file"] = self._serialize_main_file(plugin)
        specification_map["resources"] = self._serialize_resources(plugin)

        # returns the specification map
        return specification_map

    def _serialize_sub_platforms(self, platforms):
        # initializes the string buffer
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # writes the list start
        string_buffer.write("[")

        # sets the is first flag
        is_first = True

        # iterates over all the platforms
        for platform in platforms:
            if is_first:
                is_first = False
            else:
                string_buffer.write(", ")

            if platform == colony.base.plugin_system.CPYTHON_ENVIRONMENT:
                string_buffer.write("\"cpython\"")
            elif platform == colony.base.plugin_system.JYTHON_ENVIRONMENT:
                string_buffer.write("\"jython\"")
            elif platform == colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT:
                string_buffer.write("\"iron_python\"")

        # writes the list end
        string_buffer.write("]")

        # retrieves the string value
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value

    def _serialize_capabilities(self, capabilities):
        # initializes the string buffer
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # writes the list start
        string_buffer.write("[")

        # sets the is first flag
        is_first = True

        # iterates over all the capabilities
        for capability in capabilities:
            if is_first:
                is_first = False
            else:
                string_buffer.write(", ")

            # @todo: avoid problems when using composite capabilities
            # refer to the specification of the colony file
            string_buffer.write("\"" + str(capability) + "\"")

        # writes the list end
        string_buffer.write("]")

        # retrieves the string value
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value

    def _serialize_dependencies(self, dependencies):
        # initializes the string buffer
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # writes the list start
        string_buffer.write("[")

        # sets the is first flag
        is_first = True

        # iterates over all the dependencies
        for dependency in dependencies:
            if is_first:
                is_first = False
            else:
                string_buffer.write(", ")

            if dependency.__class__ == colony.base.plugin_system.PluginDependency:
                string_buffer.write("{\"id\" : \"%s\", \"version\" : \"%s\"}" % (dependency.plugin_id, dependency.plugin_version))

        # writes the list end
        string_buffer.write("]")

        # retrieves the string value
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value

    def _serialize_main_file(self, plugin):
        # retrieves the plugin manager
        plugin_manager = self.json_specification_generator_handler_plugin.manager

        # retrieves the plugin module name for the plugin id
        plugin_module_name = plugin_manager.get_plugin_module_name_by_id(plugin.id)

        # creates the main file by appending the python extension
        # to the plugin module name
        main_file = plugin_module_name + ".py"

        # returns the main file
        return main_file

    def _serialize_resources(self, plugin):
        # retrieves the plugin manager
        plugin_manager = self.json_specification_generator_handler_plugin.manager

        # retrievs the plugin path for the plugin id
        plugin_path = plugin_manager.get_plugin_path_by_id(plugin.id)

        # initializes the string buffer
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # writes the list start
        string_buffer.write("[")

        # writes the plugin file
        string_buffer.write("\"" + self._serialize_main_file(plugin) + "\"")

        # retrieves the directories entries from the plugin path
        directory_entries = os.listdir(plugin_path)

        # iterates over all the directory entries
        for directory_entry in directory_entries:
            full_directory_entry = plugin_path + "/" + directory_entry

            if os.path.isdir(full_directory_entry):
                os.path.walk(full_directory_entry, self._serializer_aux, (plugin_path, string_buffer))

        # writes the list end
        string_buffer.write("]")

        # retrieves the string value
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value

    def _serializer_aux(self, arg, dirname, names):
        plugin_path, string_buffer = arg

        if ".svn" in dirname:
            return

        complete_paths_list = [(dirname + "/" + value).replace(plugin_path, "") for value in names if not os.path.isdir(dirname + "/" + value)]

        for complete_path in complete_paths_list:
            string_buffer.write(", \"" + complete_path.replace("\\", "/").strip("/") + "\"")
