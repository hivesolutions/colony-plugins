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

__revision__ = "$LastChangedRevision: 12939 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-02-01 17:54:16 +0000 (Tue, 01 Feb 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

CONSOLE_EXTENSION_NAME = "automation"
""" The console extension name """

TABLE_TOP_TEXT = "ID      BUILD AUTOMATION ID"
""" The table top text """

COLUMN_SPACING = 8
""" The column spacing """

ID_REGEX = "[0-9]+"
""" The regular expression to retrieve the id of the build automation """

class ConsoleBuildAutomation:
    """
    The console build automation class.
    """

    build_automation_plugin = None
    """ The build automation plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, build_automation_plugin):
        """
        Constructor of the class.

        @type build_automation_plugin: BuildAutomationPlugin
        @param build_automation_plugin: The build automation plugin.
        """

        self.build_automation_plugin = build_automation_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_run_automation(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the run automation command, with the given
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

        # retrieves the build automation instance
        build_automation = self.build_automation_plugin.build_automation

        # retrieves the mandatory arguments
        plugin_id = arguments_map["plugin_id"]

        # retrieves the optional arguments
        recursive_level = arguments_map.get("recursive_level", 1)
        stage = arguments_map.get("stage", None)
        plugin_version = arguments_map.get("plugin_version", None)

        # converts the recursive level to an integer
        recursive_level = int(recursive_level)

        # retrieves the real
        real_plugin_id = self.get_plugin_id(plugin_id)

        # runs the automation for the plugin
        build_automation.run_automation(real_plugin_id, plugin_version, stage, recursive_level)

    def process_show_all_automation(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the show all automation command, with the given
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

        # prints the table top text
        output_method(TABLE_TOP_TEXT)

        # retrieves the build automation instance
        build_automation = self.build_automation_plugin.build_automation

        # retrieves all the available build automation item plugins
        build_automation_item_plugins = build_automation.get_all_build_automation_item_plugins()

        # iterates over all the build automation item plugins
        for build_automation_item_plugin in build_automation_item_plugins:
            # retrieves the internal id of the build automation
            build_automation_id = build_automation.build_automation_item_plugin_id_map[build_automation_item_plugin]

            # converts the internal id of the build automation to string
            build_automation_id_str = str(build_automation_id)

            # retrieves the build automation item plugin id
            build_automation_item_plugin_id = build_automation_item_plugin.id

            output_method(build_automation_id_str, False)

            for _index in range(COLUMN_SPACING - len(build_automation_id_str)):
                output_method(" ", False)

            output_method(build_automation_item_plugin_id, True)

    def get_plugin_id(self, id):
        plugin_id = None
        valid = False

        # compiles the regular expression
        compilation = re.compile(ID_REGEX)
        result = compilation.match(id)

        # in case there is at least one match
        if result:
            valid = result.group() == id

        # in case it matches the regular expression
        if valid:
            int_value = int(id)

            # retrieves the build automation instance
            build_automation = self.build_automation_plugin.build_automation

            if int_value in build_automation.id_build_automation_item_plugin_map:
                plugin = build_automation.id_build_automation_item_plugin_map[int_value]
                plugin_id = plugin.id
        else:
            plugin_id = id

        return plugin_id

    def get_plugin_id_list(self, argument, console_context):
        # retrieves the plugin manager
        plugin_manager = self.build_automation_plugin.manager

        # retrieves the plugin id list
        plugin_id_list = plugin_manager.plugin_instances_map.keys()

        # returns the plugin id list
        return plugin_id_list

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
                        "run_automation" : {
                            "handler" : self.process_run_automation,
                            "description" : "runs the build automation for the stage and recursive level in the plugin with the given id and version",
                            "arguments" : [
                                {
                                    "name" : "plugin_id",
                                    "description" : "the id of the plugin to perform the build automation in",
                                    "values" : self.get_plugin_id_list,
                                    "mandatory" : True
                                }, {
                                    "name" : "recursive_level",
                                    "description" : "the build automation recursive level",
                                    "values" : str,
                                    "mandatory" : False
                                }, {
                                    "name" : "stage",
                                    "description" : "the build automation stage",
                                    "values" : str,
                                    "mandatory" : False
                                }, {
                                    "name" : "plugin_version",
                                    "description" : "the version of the plugin to perform the build automation in",
                                    "values" : str,
                                    "mandatory" : False
                                }
                            ]
                        },
                        "show_all_automation" : {
                            "handler" : self.process_show_all_automation,
                            "description" : "shows all the build automations"
                        }
                    }

        # returns the commands map
        return commands_map
