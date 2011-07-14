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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 12670 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-01-13 13:08:29 +0000 (qui, 13 Jan 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "descriptor_generator"
""" The console extension name """

class ConsoleDescriptorGenerator:
    """
    The console descriptor generator class.
    """

    descriptor_generator_plugin = None
    """ The descriptor generator plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, descriptor_generator_plugin):
        """
        Constructor of the class.

        @type descriptor_generator_plugin: DescriptorGeneratorPlugin
        @param descriptor_generator_plugin: The descriptor generator plugin.
        """

        self.descriptor_generator_plugin = descriptor_generator_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_generate_descriptor(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the generate descriptor command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the descriptor generator instance
        descriptor_generator = self.descriptor_generator_plugin.descriptor_generator

        # retrieves the plugin id from the arguments
        plugin_id = arguments_map.get("plugin_id", None)

        # generates a plugin descriptor for the specified plugin in case an id was specified
        if plugin_id:
            descriptor_generator.generate_plugin_descriptor(plugin_id)
        else:
            # otherwise generates descriptors for all plugins that fail validation
            descriptor_generator.generate_plugin_descriptors()

    def get_plugin_id_list(self, argument, console_context):
        # retrieves the plugin manager
        plugin_manager = self.descriptor_generator_plugin.manager

        # retrieves the plugin id list
        plugin_id_list = plugin_manager.plugin_instances_map.keys()

        # returns the plugin id list
        return plugin_id_list

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "generate_descriptor" : {
                "handler" : self.process_generate_descriptor,
                "description" : "generates the plugin descriptor",
                "arguments" : [
                    {
                        "name" : "plugin_id",
                        "description" : "the plugin id",
                        "values" : self.get_plugin_id_list,
                        "mandatory" : False
                    }
                ]
            }
        }

        # returns the commands map
        return commands_map
