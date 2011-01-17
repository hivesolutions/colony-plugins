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

import os
import re
import sys
import types

import colony.libs.map_util

import main_console_interfaces

COMMAND_EXCEPTION_MESSAGE = "there was an exception"
""" The command exception message """

INVALID_COMMAND_MESSAGE = "invalid command"
""" The invalid command message """

MISSING_MANDATORY_ARGUMENTS_MESSAGE = "missing mandatory arguments"
""" The missing mandatory arguments message """

INTERNAL_CONFIGURATION_PROBLEM_MESSAGE = "internal configuration problem"
""" The internal configuration problem message """

COMMAND_LINE_REGEX_VALUE = "\"[^\"]*\"|[^ \s]+"
""" The regular expression to retrieve the command line arguments """

COMMAND_LINE_REGEX = re.compile(COMMAND_LINE_REGEX_VALUE)
""" The regular expression to retrieve the command line arguments (compiled) """

SEQUENCE_TYPES = (types.ListType, types.TupleType)
""" The sequence types """

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

    def create_console_context(self):
        """
        Creates a new console context for third party usage.

        @rtype: ConsoleContext
        @return: The creates console context.
        """

        return ConsoleContext(self)

    def process_command_line(self, command_line, output_method = None, console_context = None):
        """
        Processes the given command line, with the given output method.

        @type command_line: String
        @param command_line: The command line to be processed.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context to be used to process
        the command line.
        @rtype: bool
        @return: If the processing of the command line was successful.
        """

        # in case there is no output method defined
        if not output_method:
            # uses the write function as the output method
            output_method = self.write

        # splits the command line arguments
        line_split = self.split_command_line_arguments(command_line)

        # in case the line is not valid (empty)
        if not line_split:
            # returns false (invalid)
            return False

        # retrieves the command value
        command = line_split[0]

        # retrieves the arguments
        arguments = line_split[1:]

        # validates the command with the given arguments and
        # retrieves the command handler in success
        command_handler = self._validate_command(command, arguments, output_method)

        # in case the validation failed
        if not command_handler:
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

    def get_default_output_method(self):
        """
        Retrieves the default output method.

        @rtype: Method
        @return: The default output method for console.
        """

        return self.write

    def get_command_line_alternatives(self, command, arguments):
        """
        Processes the given command line, with the given output method.
        Retrieves the alternative (possible) values for the given command
        and arguments.

        @type command: String
        @param command: The command to be retrieve the alternatives.
        @type arguments: String
        @param arguments: The list of arguments
        @rtype: Tuple
        @return: A tuple containing the list of alternatives for the given
        command line and the current best match.
        """

        # in case the argument are valid
        if arguments:
            # retrieves the list of argument alternatives
            alternatives_list = self._get_argument_alternatives(command, arguments)
        # otherwise we're completing a command only
        else:
            # retrieves the list of command alternatives
            alternatives_list = self._get_command_alternatives(command)

        # retrieves the best match for the alternatives list
        best_match = self._get_best_match(alternatives_list)

        # creates the alternatives tuple containing
        # the alternatives list and the best match
        alternatives_tuple = (alternatives_list, best_match)

        # returns the alternatives tuple
        return alternatives_tuple

    def split_command_line(self, command_line, include_extra_space = False):
        """
        Splits the given command line into command and arguments.

        @type command_line: String
        @param command_line: The command line to be splitted.
        @type include_extra_space: bool
        @param include_extra_space: If an eventual extra space to the right
        should be considered a token.
        @rtype: Tuple
        @return: A tuple containing the command and the arguments.
        """

        # splits the command line arguments
        line_split = self.split_command_line_arguments(command_line, include_extra_space)

        # in case the line is not valid (empty)
        if not line_split:
            # returns "empty" command
            # tuple value
            return ("", [])

        # retrieves the command value
        command = line_split[0]

        # retrieves the arguments
        arguments = line_split[1:]

        # creates the command tuple with the command
        # and the arguments
        command_tuple = (command, arguments)

        # returns the command tuple
        return command_tuple

    def create_console_interface_character(self, console_handler):
        """
        Creates a new console interface character based
        from the given console handler.

        @type console_handler: ConsoleHandler
        @param console_handler: The console handler to be used.
        @rtype: ConsoleInterfaceCharacter
        @return: The create console interface character.
        """

        return main_console_interfaces.MainConsoleInterfaceCharacter(self, console_handler)

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

    def split_command_line_arguments(self, command_line, include_extra_space = False):
        """
        Separates the various command line arguments per space or per quotes.

        @type command_line: String
        @param command_line: The command line string.
        @type include_extra_space: bool
        @param include_extra_space: If an eventual extra space to the right
        should be considered a token.
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

        # in case the include extra space flag is set,
        # the command line is not empty or invalid
        # and the last element in the command line is a
        # space character
        if include_extra_space and command_line and command_line[-1] == " ":
            # adds an empty element to the line split
            # representing the extra space
            line_split.append("")

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

    def _validate_command(self, command, arguments, output_method):
        # retrieves the command information
        command_information = self.commands_map.get(command, None)

        # in case no command information is found
        # (command not found)
        if not command_information:
            # print the invalid command message
            output_method(INVALID_COMMAND_MESSAGE)

            # returns none (invalid)
            return None

        # retrieves the command arguments
        command_arguments = command_information.get("arguments")

        # creates the command mandatory arguments (list)
        command_mandatory_arguments = []

        # iterates over the command arguments
        for command_argument in command_arguments:
            # retrieves the command argument mandatory
            command_argument_mandatory = command_argument.get("mandatory", False)

            # in case the command argument adds it
            # to the command mandatory arguments
            command_argument_mandatory and command_mandatory_arguments.append(command_argument)

        # retrieves the command mandatory arguments length
        command_mandatory_arguments_length = len(command_mandatory_arguments)

        # retrieves the arguments length
        arguments_length = len(arguments)

        # in case the command mandatory arguments length is larger
        # than the arguments length
        if command_mandatory_arguments_length > arguments_length:
            # retrieves the missing arguments count, by subtracting the arguments
            # length from the command mandatory arguments length
            missing_arguments_count = command_mandatory_arguments_length - arguments_length

            # retrieves the missing arguments list
            missing_arguments = command_mandatory_arguments[missing_arguments_count * -1:]

            # creates the missing argument names list
            missing_argument_names = [value.get("name", "undefined") for value in missing_arguments]

            # joins the missing argument names to create the missing
            # argument names line
            missing_argument_names_line = ", ".join(missing_argument_names)

            # print the missing mandatory arguments message
            output_method(MISSING_MANDATORY_ARGUMENTS_MESSAGE + ": " + missing_argument_names_line)

            # returns none (invalid)
            return None

        # retrieves the command handler
        command_handler = command_information.get("handler", None)

        # in case no command handler is defined
        if not command_handler:
            # print the internal configuration problem message
            output_method(INTERNAL_CONFIGURATION_PROBLEM_MESSAGE)

            # returns none (invalid)
            return None

        # returns the command handler
        return command_handler

    def _get_command_alternatives(self, command):
        # creates the alternatives list
        alternatives_list = []

        # iterates over all the commands in the
        # commands map
        for _command in self.commands_map:
            # retrieves the command information
            command_information = self.commands_map[_command]

            # retrieves the command arguments
            command_arguments = command_information.get("arguments", [])

            # recreates the command value base on either the command
            # contains arguments or not
            _command = command_arguments and _command + " " or _command

            # in case the command starts with the
            # value in the command
            _command.startswith(command) and alternatives_list.append(_command)

        # returns the alternatives list
        return alternatives_list

    def _get_argument_alternatives(self, command, arguments):
        # creates the alternatives list
        alternatives_list = []

        # retrieves the command information for the command
        command_information = self.commands_map.get(command, None)

        # in case the command information is not defined
        if not command_information:
            # returns immediately an empty
            # alternatives list (no alternatives)
            return alternatives_list

        # retrieves the arguments index
        arguments_index = len(arguments) - 1

        # retrieves the "target" argument
        target_argument = arguments[arguments_index]

        # retrieves the command arguments
        command_arguments = command_information.get("arguments", [])

        # retrieves the command arguments length
        command_arguments_length = len(command_arguments)

        # in case the command arguments list does not
        # contain argument complete for the required argument
        if not command_arguments_length > arguments_index:
            # returns immediately an empty
            # alternatives list (no alternatives)
            return alternatives_list

        # retrieves the command "target" argument
        command_argument = command_arguments[arguments_index]

        # retrieves the command argument values
        command_argument_values = command_argument.get("values", None)

        # retrieves the command argument values type
        command_argument_values_type = type(command_argument_values)

        # creates the list to hold the alternatives
        # base values list
        alternatives_base_list = []

        # in case the command argument values is a sequence
        if command_argument_values_type in SEQUENCE_TYPES:
            # sets the alternatives base list as the command
            # argument values
            alternatives_base_list = command_argument_values
        # in the command argument value is a method
        elif command_argument_values_type == types.MethodType:
            # sets the alternatives base list as the return
            # of the command argument values call
            alternatives_base_list = command_argument_values()

        # iterates over all the commands in the
        # commands map
        for alternative_base in alternatives_base_list:
            # recreates the alternative base value based on either
            # the command contains any more arguments or not
            alternative_base = command_arguments_length > arguments_index + 1 and alternative_base + " " or alternative_base

            # in case the alternative base starts with the
            # value in the target argument
            alternative_base.startswith(target_argument) and alternatives_list.append(alternative_base)

        # returns the alternatives list
        return alternatives_list

    def _get_best_match(self, alternatives_list):
        # in case the alternatives list is not set
        if not alternatives_list:
            # returns empty string (invalid)
            return ""

        # retrieves the first alternative
        first_alternative = alternatives_list[0]

        # retrieves the first alternative length
        first_alternative_length = len(first_alternative)

        # creates the best match list
        best_match_list = []

        # iterates over the range of the first
        # alternative length
        for index in range(first_alternative_length):
            # retrieves the base character from the first
            # alternative (for the current index)
            base_character = first_alternative[index]

            # sets the valid flag
            valid = True

            # iterates over all the alternatives in the
            # alternatives list
            for alternative in alternatives_list:
                # retrieves the alternative length
                alternative_length = len(alternative)

                # retrieves the (current) alternative
                # character (in case the alternative length is valid)
                alternative_character = alternative_length > index and alternative[index] or None

                # in case the base character and the alternative
                # character are not the same
                if not base_character ==  alternative_character:
                    # unsets the valid flag
                    valid = False

                    # breaks the loop
                    break

            # in case the valid flag
            # is not set
            if not valid:
                # breaks the (outer) loop
                break

            # adds the base character to the best
            # match list
            best_match_list.append(base_character)

        # joins the best match list to retrieve
        # the best match
        best_match = "".join(best_match_list)

        # returns the best match
        return best_match

class ConsoleContext:
    """
    The console context class.
    """

    main_console = None
    """ The main console reference """

    path = None
    """ The current console path """

    user = None
    """ The current console user """

    def __init__(self, main_console):
        """
        Constructor of the class.

        @type main_console: MainConsole
        @param main_console: The main console reference.
        """

        self.main_console = main_console

        # sets the current path in the context
        self.path = os.getcwd()

    def process_command_line(self, command_line, output_method):
        return self.main_console.process_command_line(command_line, output_method, self)

    def get_command_line_alternatives(self, command, arguments):
        return self.main_console.get_command_line_alternatives(command, arguments)

    def create_console_interface_character(self, console_handler):
        return self.main_console.create_console_interface_character(console_handler)

    def get_path(self):
        """
        Returns the path.

        @rtype: String
        @return: The path.
        """

        return self.path

    def set_path(self, path):
        """
        Sets the path.

        @rtype: String
        @return: The path.
        """

        return self.path

    def get_user(self):
        """
        Returns the user.

        @rtype: String
        @return: The user.
        """

        return self.user

    def set_user(self, user):
        """
        Sets the user.

        @rtype: String
        @return: The user.
        """

        return self.user
