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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "build_automation_descriptor_generator"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### BUILD AUTOMATION DESCRIPTOR GENERATOR HELP ###\n\
generate_plugin_descriptor <plugin_id> - generates a plugin descriptor file for a specific plugin\
generate_plugin_descriptors - generates a plugin descriptor files for all plugins"
""" The help text """

class ConsoleBuildAutomationDescriptorGenerator:
    """
    The console build automation descriptor generator class.
    """

    build_automation_descriptor_generator_plugin = None
    """ The build automation descriptor generator plugin """

    commands = ["generate_plugin_descriptor", "generate_plugin_descriptors"]
    """ The commands list """

    def __init__(self, build_automation_descriptor_generator_plugin):
        """
        Constructor of the class.

        @type build_automation_descriptor_generator_plugin: BuildAutomationDescriptorGeneratorPlugin
        @param build_automation_descriptor_generator_plugin: The build automation descriptor generator plugin.
        """

        self.build_automation_descriptor_generator_plugin = build_automation_descriptor_generator_plugin

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

    def process_generate_plugin_descriptor(self, args, output_method):
        # returns in case the not enough arguments were provided
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the plugin's id
        plugin_id = args[0]

        # generates a plugin descriptor for the specified plugin
        self.build_automation_descriptor_generator_plugin.generate_plugin_descriptor(plugin_id)

    def process_generate_plugin_descriptors(self, args, output_method):
        # generates the descriptors for all plugins
        self.build_automation_descriptor_generator_plugin.generate_plugin_descriptors()
