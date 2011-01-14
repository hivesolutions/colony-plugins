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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import sys

import colony.libs.map_util

import main_console_interfaces

COMMAND_EXCEPTION_MESSAGE = "there was an exception"
""" The command exception message """

INVALID_COMMAND_MESSAGE = "invalid command"
""" The invalid command message """

INTERNAL_CONFIGURATION_PROBLEM_MESSAGE = "internal configuration problem"
""" The internal configuration problem message """

COMMAND_LINE_REGEX_VALUE = "\"[^\"]*\"|[^ \s]+"
""" The regular expression to retrieve the command line arguments """

COMMAND_LINE_REGEX = re.compile(COMMAND_LINE_REGEX_VALUE)
""" The regular expression to retrieve the command line arguments (compiled) """

class MainConsole:
    """
    The main console class.
    """

    main_console_plugin = None
    """ The main console plugin """

    commands_map = {}
    """ The map with the command association with the command information """

    def __init__(self, main_console_plugin):
        """
        Constructor of the class.

        @type main_console_plugin: MainConsolePlugin
        @param main_console_plugin: The main console plugin.
        """

        self.main_console_plugin = main_console_plugin

        self.commands_map = {}

    def process_command_line(self, command_line, output_method = None):
        """
        Processes the given command line, with the given output method.

        @type command_line: String
        @param command_line: The command line to be processed.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @rtype: bool
        @return: If the processing of the command line was successful.
        """

        # in case there is no output method defined
        if not output_method:
            # uses the write function as the output method
            output_method = self.write

        # splits the command line arguments
        line_split = self.split_command_line_arguments(command_line)

        # retrieves the line split length
        line_split_length = len(line_split)

        # in case the line is not empty
        if line_split_length == 0:
            # returns false (invalid)
            return False

        # retrieves the command value
        command = line_split[0]

        # retrieves the arguments
        arguments = line_split[1:]

        # retrieves the command information
        command_information = self.commands_map.get(command, None)

        # in case no command information is found (command
        # not found)
        if not command_information:
            # print the internal configuration problem message
            output_method(INTERNAL_CONFIGURATION_PROBLEM_MESSAGE)

            # returns false (invalid)
            return False

        # retrieves the command handler
        command_handler = command_information.get("handler", None)

        if not command_handler:
            # print the invalid command message
            output_method(INVALID_COMMAND_MESSAGE)

            # returns false (invalid)
            return False

        try:
            # runs the command handler with the arguments
            # and the output method
            command_handler(arguments, output_method)
        except Exception, exception:
            # prints the exception message
            output_method(COMMAND_EXCEPTION_MESSAGE + ": " + unicode(exception))

            # logs the stack trace value
            self.main_console_plugin.log_stack_trace()

            # returns false (invalid)
            return False

        # returns true (valid)
        return True

    def get_command_line_alternatives(self, command_line):
        """
        Processes the given command line, with the given output method.

        @type command_line: String
        @param command_line: The command line to be retrieve the alternatives.
        @rtype: List
        @return: If list of alternatives for the given command line.
        """

        # creates the alternatives list
        alternatives_list = []

        # iterates over all the commands in the
        # commands map
        for command in self.commands_map:
            # in case the command starts with the
            # value in the command line
            command.startswith(command_line) and alternatives_list.append(command)

        # returns the alternatives list
        return alternatives_list

    def get_default_output_method(self):
        """
        Retrieves the default output method.

        @rtype: Method
        @return: The default output method for console.
        """

        return self.write

    def create_console_interface_character(self, console_handler):
        """
        Creates a new console interface character based
        from the given console handler.

        @type console_handler: ConsoleHandler
        @param console_handler: The console handler to be used.
        @rtype: ConsoleInterfaceCharacter
        @return: The create console interface character.
        """

        return main_console_interfaces.MainConsoleInterfaceCharacter(self.main_console_plugin, self, console_handler)

    def console_command_extension_load(self, console_command_extension_plugin):
        # retrieves the commands map from the console command extension
        commands_map = console_command_extension_plugin.get_commands_map()

        # copies the plugin commands map to the commands map
        colony.libs.map_util.map_copy(commands_map, self.commands_map)

    def console_command_extension_unload(self, console_command_extension_plugin):
        # retrieves the commands map from the console command extension
        commands_map = console_command_extension_plugin.get_commands_map()

        # removes the plugin commands map from the plugins commands map
        colony.libs.map_util.map_remove(commands_map, self.commands_map)

    def split_command_line_arguments(self, command_line):
        """
        Separates the various command line arguments per space or per quotes.

        @type command_line: String
        @param command_line: The command line string.
        @rtype: List
        @return: The list containing the various command line arguments.
        """

        # splits the line using the command line regex
        line_split = COMMAND_LINE_REGEX.findall(command_line)

        # retrieves the line split length
        line_split_length = len(line_split)

        # iterates over the range of the line split length
        for line_split_length_index in range(line_split_length):
            # retrieves the current line
            line = line_split[line_split_length_index]

            # removes the "extra" characters from the line
            line = line.replace("\"", "")

            # sets the line in the line split list
            line_split[line_split_length_index] = line

        # returns the line split
        return line_split

    def write(self, text, new_line = True):
        """
        Writes the given text to the standard output,
        may use a newline or not.

        @type text: String
        @param text: The text to be written to the standard output.
        @type new_line: bool
        @param new_line: If the text should be suffixed with a newline.
        """

        # writes the text contents
        sys.stdout.write(text)

        # in case a newline should be appended
        # writes it
        new_line and sys.stdout.write("\n")
