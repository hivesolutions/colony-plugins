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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

CONSOLE_EXTENSION_NAME = "automation"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### BUILD AUTOMATION HELP ###\n\
run_automation <plugin-id> [plugin-version] - runs the build automation in the plugin with the given id and version\n\
showall_automation                          - shows all the build automations"
""" The help text """

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

    commands = ["run_automation", "showall_automation"]

    build_automation_plugin = None
    """ The build automation plugin """

    def __init__(self, build_automation_plugin):
        """
        Constructor of the class.

        @type build_automation_plugin: BuildAutomationPlugin
        @param build_automation_plugin: The build automation plugin.
        """

        self.build_automation_plugin = build_automation_plugin

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_run_automation(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the plugin id
        plugin_id = args[0]

        # retrieves the real
        real_plugin_id = self.get_plugin_id(plugin_id)

        # runs the automation for the plugin
        self.build_automation_plugin.build_automation.run_automation_plugin_id_version(real_plugin_id)

    def process_showall_automation(self, args, output_method):
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

            for x in range(COLUMN_SPACING - len(build_automation_id_str)):
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
