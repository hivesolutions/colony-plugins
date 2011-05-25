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

CONSOLE_EXTENSION_NAME = "${out value=scaffold_attributes.variable_name /}"
""" The console extension name """

class Console${out value=scaffold_attributes.class_name /}:
    """
    The console ${out value=scaffold_attributes.short_name_lowercase /} class.
    """

    ${out value=scaffold_attributes.variable_name /}_plugin = None
    """ The ${out value=scaffold_attributes.short_name_lowercase /} plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin):
        """
        Constructor of the class.

        @type ${out value=scaffold_attributes.variable_name /}_plugin: ${out value=scaffold_attributes.class_name /}Plugin
        @param ${out value=scaffold_attributes.variable_name /}_plugin: The ${out value=scaffold_attributes.short_name_lowercase /} plugin.
        """

        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_dummy_command(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the dummy command command, with the given
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

        # retrieves the ${out value=scaffold_attributes.short_name_lowercase /}
        ${out value=scaffold_attributes.variable_name /}_plugin = self.${out value=scaffold_attributes.variable_name /}_plugin
        ${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.variable_name /}_plugin.${out value=scaffold_attributes.variable_name /}

        # invokes the plugin's dummy method
        dummy_result = ${out value=scaffold_attributes.variable_name /}.dummy_method()

        # outputs the result
        output_method(dummy_result)

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "dummy_command" : {
                "handler" : self.process_dummy_command,
                "description" : "runs the dummy command",
                "arguments" : [
                    {
                        "name" : "dummy_command",
                        "description" : "performs the dummy command",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            }
        }

        # returns the commands map
        return commands_map
