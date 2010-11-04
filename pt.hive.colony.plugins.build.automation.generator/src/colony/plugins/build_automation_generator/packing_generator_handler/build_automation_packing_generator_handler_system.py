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

import colony.base.plugin_system
import colony.libs.string_buffer_util

DEFAULT_ENCODING = "Cp1252"
""" The default encoding """

BUILD_AUTOMATION_GENERATOR_HANDLER_NAME = "packing"
""" The build automation generator handler name """

TEMPLATE_FILE_PATH = "build_automation_generator/packing_generator_handler/resources/baf.xml.tpl"
""" The template file path """

class BuildAutomationPackingGeneratorHandler:
    """
    The build automation packing generator handler class.
    """

    build_automation_packing_generator_handler_plugin = None
    """ The build automation packing generator handler """

    def __init__(self, build_automation_packing_generator_handler_plugin):
        """
        Constructor of the class.

        @type build_automation_packing_generator_handler_plugin: BuildAutomationPackingGeneratorHandler
        @param build_automation_packing_generator_handler_plugin: The build automation packing generator handler plugin.
        """

        self.build_automation_packing_generator_handler_plugin = build_automation_packing_generator_handler_plugin

    def get_build_automation_generator_handler_name(self):
        return BUILD_AUTOMATION_GENERATOR_HANDLER_NAME

    def generate_plugin_build_automation(self, plugin, properties):
        """
        Generates a build automation string describing the structure
        and specification of the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin to be used to generate plugin build automation.
        @type properties: Dictionary
        @param properties: The properties for plugin build automation generation.
        @rtype: String
        @return: The generated plugin build automation string.
        """

        # retrieves the plugin manager
        plugin_manager = self.build_automation_packing_generator_handler_plugin.manager

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.build_automation_packing_generator_handler_plugin.template_engine_manager_plugin

        # retrieves the build automation packing generator handler plugin path
        build_automation_packing_generator_handler_plugin_path = plugin_manager.get_plugin_path_by_id(self.build_automation_packing_generator_handler_plugin.id)

        # creates the full template file path
        template_file_path = build_automation_packing_generator_handler_plugin_path + "/" + TEMPLATE_FILE_PATH

        # parses the template file path
        template_file = template_engine_manager_plugin.parse_file_path_encoding(template_file_path, DEFAULT_ENCODING)

        # generates the build automation map for the plugin
        build_automation_map = self._generate_build_automation_map(plugin)

        # assigns the build automation to the template file
        template_file.assign("build_automation", build_automation_map)

        # processes the template file
        processed_template_file = template_file.process()

        # returns the processed template file
        return processed_template_file

    def _generate_build_automation_map(self, plugin):
        """
        Generates the build automation map for the given plugin.
        The build automation map contains all the information
        necessary to generate the build automation file for the plugin.

        @type plugin: Plugin
        @param plugin: The plugin to be used to generate
        the build automation map.
        @rtype: Dictionary
        @return: The build automation map.
        """

        # creates the build automation map
        build_automation_map = {}

        # sets the build automation map attributes
        build_automation_map["platform"] = "python"
        build_automation_map["sub_platforms"] = self._serialize_sub_platforms(plugin.platforms)
        build_automation_map["id"] = plugin.id
        build_automation_map["name"] = plugin.name
        build_automation_map["short_name"] = plugin.short_name
        build_automation_map["description"] = plugin.description
        build_automation_map["version"] = plugin.version
        build_automation_map["author"] = plugin.author
        build_automation_map["capabilities"] = self._serialize_capabilities(plugin.capabilities)
        build_automation_map["capabilities_allowed"] = self._serialize_capabilities(plugin.capabilities_allowed)
        build_automation_map["dependencies"] = self._serialize_dependencies(plugin.dependencies)
        build_automation_map["packing_file"] = self._serialize_packing_file(plugin)

        # returns the build automation map
        return build_automation_map

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

    def _serialize_packing_file(self, plugin):
        # retrieves the plugin manager
        plugin_manager = self.build_automation_packing_generator_handler_plugin.manager

        # retrieves the plugin module name for the plugin id
        plugin_module_name = plugin_manager.get_plugin_module_name_by_id(plugin.id)

        # creates the packing file by appending the python extension
        # to the plugin module name
        packing_file = plugin_module_name + ".json"

        # returns the packing file
        return packing_file
