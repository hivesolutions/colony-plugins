#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2018 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import re
import sys
import types

import colony

from . import interfaces
from . import exceptions
from . import authentication

VALID_VALUE = "valid"
""" The valid value """

EXCEPTION_VALUE = "exception"
""" The exception value """

MESSAGE_VALUE = "message"
""" The message value """

USERNAME_VALUE = "username"
""" The username value """

CURRENT_VALUE = "current"
""" The current value """

PENDING_NEWLINE_VALUE = "pending_newline"
""" The pending newline value """

NEWLINE_VALUE = "newline"
""" The newline value """

ACTION_VALUE = "action"
""" The action value """

PROGRESS_VALUE = "progress"
""" The progress value """

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

COMPLETE_PERCENTAGE = 100
""" The percentage value that defines a completed task """

SEQUENCE_TYPES = (
    list,
    tuple
)
""" The sequence types """

class Console(colony.System):
    """
    The console class.
    """

    console_authentication = None
    """ The console authentication """

    commands_map = {}
    """ The map with the command association with
    the command information """

    console_configuration = {}
    """ The console configuration """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)

        self.commands_map = {}
        self.console_configuration = {}

        # creates the console authentication
        self.console_authentication = authentication.ConsoleAuthentication(plugin)

    def create_console_context(self):
        """
        Creates a new console context for third party usage.

        :rtype: ConsoleContext
        :return: The creates console context.
        """

        return ConsoleContext(self)

    def create_console_interface_character(self, console_handler, console_context):
        """
        Creates a new console interface character based
        from the given console handler.

        :type console_handler: ConsoleHandler
        :param console_handler: The console handler to be used.
        :type console_context: ConsoleContext
        :param console_context: The console context to be used.
        :rtype: ConsoleInterfaceCharacter
        :return: The create console interface character.
        """

        return interfaces.ConsoleInterfaceCharacter(self, console_handler, console_context)

    def authenticate_user(self, username, password, console_context = None):
        # retrieves the authentication properties from the console configuration
        authentication_properties = self.console_configuration.get("authentication_properties", {})

        # handles the authentication with the console authentication and
        # retrieves the authentication result
        authentication_result = self.console_authentication.handle_authentication(username, password, authentication_properties)

        # returns the authentication result
        return authentication_result

    def process_command_line(self, command_line, output_method = None, console_context = None):
        """
        Processes the given command line, with the given output method.

        :type command_line: String
        :param command_line: The command line to be processed.
        :type output_method: Method
        :param output_method: The output method to be used in the processing.
        :type console_context: ConsoleContext
        :param console_context: The console context to be used to process
        the command line.
        :rtype: bool
        :return: If the processing of the command line was successful.
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
        # retrieves the command handler and the arguments map in success
        command_handler, arguments_map = self._validate_command(command, arguments, output_method)

        # in case the validation failed
        if not command_handler:
            # returns false (invalid)
            return False

        try:
            # runs the command handler with the arguments,
            # the arguments map, the output method and the console context
            command_handler(arguments, arguments_map, output_method, console_context)
        except Exception as exception:
            # prints the exception message
            output_method(COMMAND_EXCEPTION_MESSAGE + ": " + colony.legacy.UNICODE(exception))

            # logs the stack trace value
            self.plugin.log_stack_trace()

            # returns false (invalid)
            return False

        # returns true (valid)
        return True

    def get_default_output_method(self):
        """
        Retrieves the default output method.

        :rtype: Method
        :return: The default output method for console.
        """

        return self.write

    def get_command_line_alternatives(self, command, arguments, console_context = None):
        """
        Processes the given command line, with the given output method.
        Retrieves the alternative (possible) values for the given command
        and arguments.

        :type command: String
        :param command: The command to be retrieve the alternatives.
        :type arguments: String
        :param arguments: The list of arguments
        :type console_context: ConsoleContext
        :param console_context: The console context to be used to retrieve
        the command line alternatives.
        :rtype: Tuple
        :return: A tuple containing the list of alternatives for the given
        command line and the current best match.
        """

        # in case the argument are valid
        if arguments:
            # retrieves the list of argument alternatives
            alternatives_list = self._get_argument_alternatives(command, arguments, console_context)
        # otherwise we're completing a command only
        else:
            # retrieves the list of command alternatives
            alternatives_list = self._get_command_alternatives(command)

        # retrieves the best match for the alternatives list
        best_match = self._get_best_match(alternatives_list)

        # creates the alternatives tuple containing
        # the alternatives list and the best match
        alternatives_tuple = (
            alternatives_list,
            best_match
        )

        # returns the alternatives tuple
        return alternatives_tuple

    def split_command_line(self, command_line, include_extra_space = False):
        """
        Splits the given command line into command and arguments.

        :type command_line: String
        :param command_line: The command line to be splitted.
        :type include_extra_space: bool
        :param include_extra_space: If an eventual extra space to the right
        should be considered a token.
        :rtype: Tuple
        :return: A tuple containing the command and the arguments.
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
        command_tuple = (
            command,
            arguments
        )

        # returns the command tuple
        return command_tuple

    def console_command_extension_load(self, console_command_extension_plugin):
        # retrieves the commands map from the console command extension
        commands_map = console_command_extension_plugin.get_commands_map()

        # copies the plugin commands map to the commands map
        colony.map_copy(commands_map, self.commands_map)

    def console_command_extension_unload(self, console_command_extension_plugin):
        # retrieves the commands map from the console command extension
        commands_map = console_command_extension_plugin.get_commands_map()

        # removes the plugin commands map from the plugins commands map
        colony.map_remove(commands_map, self.commands_map)

    def set_configuration_property(self, configuration_property):
        # retrieves the configuration
        configuration = configuration_property.get_data()

        # cleans the console configuration
        colony.map_clean(self.console_configuration)

        # copies the service configuration to the console configuration configuration
        colony.map_copy(configuration, self.console_configuration)

    def unset_configuration_property(self):
        # cleans the console configuration
        colony.map_clean(self.console_configuration)

    def split_command_line_arguments(self, command_line, include_extra_space = False):
        """
        Separates the various command line arguments per space or per quotes.

        :type command_line: String
        :param command_line: The command line string.
        :type include_extra_space: bool
        :param include_extra_space: If an eventual extra space to the right
        should be considered a token.
        :rtype: List
        :return: The list containing the various command line arguments.
        """

        # splits the line using the command line regex
        line_split = COMMAND_LINE_REGEX.findall(command_line)

        # retrieves the line split length
        line_split_length = len(line_split)

        # iterates over the range of the line split length
        for line_split_length_index in colony.legacy.xrange(line_split_length):
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

        :type text: String
        :param text: The text to be written to the standard output.
        :type new_line: bool
        :param new_line: If the text should be suffixed with a newline.
        """

        # writes the text contents
        sys.stdout.write(text)

        # in case a newline should be appended
        # writes it
        new_line and sys.stdout.write("\n")

        # flushes the standard output value
        sys.stdout.flush()

    def _validate_command(self, command, arguments, output_method):
        # retrieves the command information
        command_information = self.commands_map.get(command, None)

        # in case no command information is found
        # (command not found)
        if not command_information:
            # print the invalid command message
            output_method(INVALID_COMMAND_MESSAGE)

            # returns none (invalid)
            return (
                None,
                None
            )

        # retrieves the command arguments
        command_arguments = command_information.get("arguments", [])

        # retrieves the command mandatory arguments from the
        # the command information
        command_mandatory_arguments = self.__get_command_mandatory_arguments(command_arguments)

        # retrieves the command mandatory arguments length
        command_mandatory_arguments_length = len(command_mandatory_arguments)

        # retrieves the arguments length
        arguments_length = len(arguments)

        # in case the arguments length is smaller than the
        # command mandatory arguments length
        if arguments_length < command_mandatory_arguments_length:
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
            return (
                None,
                None
            )

        # retrieves the command handler
        command_handler = command_information.get("handler", None)

        # in case no command handler is defined
        if not command_handler:
            # print the internal configuration problem message
            output_method(INTERNAL_CONFIGURATION_PROBLEM_MESSAGE)

            # returns none (invalid)
            return (
                None,
                None
            )

        # retrieves the received arguments list
        received_arguments = command_arguments[:arguments_length]

        # retrieves the received argument names
        received_argument_names = [value.get("name", "undefined") for value in received_arguments]

        # zip the received argument names and the arguments list
        received_arguments_tuple = zip(received_argument_names, arguments)

        # creates the arguments map from the received
        # arguments tuple
        arguments_map = dict(received_arguments_tuple)

        # creates the command tuple from the command handler
        # and the arguments map
        command_tuple = (
            command_handler,
            arguments_map
        )

        # returns the command tuple
        return command_tuple

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

    def _get_argument_alternatives(self, command, arguments, console_context):
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
            alternatives_base_list = command_argument_values(target_argument, console_context)

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
        for index in colony.legacy.xrange(first_alternative_length):
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
                if not base_character == alternative_character:
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

    def __get_command_mandatory_arguments(self, command_arguments):
        # creates the command mandatory arguments (list)
        command_mandatory_arguments = []

        # iterates over the command arguments
        for command_argument in command_arguments:
            # retrieves the command argument mandatory
            command_argument_mandatory = command_argument.get("mandatory", False)

            # in case the command argument adds it
            # to the command mandatory arguments
            command_argument_mandatory and command_mandatory_arguments.append(command_argument)

        # returns the command mandatory arguments
        return command_mandatory_arguments

class ConsoleContext(colony.Protected):
    """
    The console context class.
    This class defines the context for the current
    console execution.
    It also contains some useful functions for extra
    information retrieval.
    """

    console = None
    """ The console reference """

    path = None
    """ The current console path """

    user = None
    """ The current console user """

    authentication_information = None
    """ The current authentication information/result """

    _get_line = None
    """ The reference to the console's method to retrieve a line """

    _get_size = None
    """ The reference to the console's method to retrieve the console's size """

    def __init__(self, console):
        """
        Constructor of the class.

        :type console: Console
        :param console: The console reference.
        """

        self.console = console

        # sets the current path in the context
        self.path = os.getcwd()

    @colony.public
    def authenticate_user(self, username, password):
        try:
            # tries to authenticate the user retrieving the result, this call
            # should returns the authentication map, then uses this map to
            # retrieve the boolean result from it (represents the validation result)
            authentication_result = self.console.authenticate_user(username, password, self._proxy_instance)
            authentication_result_valid = authentication_result.get(VALID_VALUE, False)

            # in case the authentication is not valid
            if not authentication_result_valid:
                # retrieves the authentication result information
                authentication_result_exception = authentication_result.get(EXCEPTION_VALUE, {})
                authentication_result_exception_message = authentication_result_exception.get(MESSAGE_VALUE, "undefined error")

                # raises the authentication failed exception
                raise exceptions.AuthenticationFailed(authentication_result_exception_message)

            # retrieves the username from the authentication result
            username = authentication_result.get(USERNAME_VALUE, None)

            # sets the user value according to the
            # authentication result
            self.user = username

            # sets the authentication information with the authentication
            # result value
            self.authentication_information = authentication_result
        except BaseException as exception:
            # prints a debug message
            self.console.plugin.debug("Problem authenticating user: %s" % colony.legacy.UNICODE(exception))

            # invalidates the user and authentication information as
            # the authentication failed
            self.user = None
            self.authentication_information = None

        # returns the user
        return self.user

    @colony.public
    def create_handlers_map(self, output_method):
        # creates the map that defined the state
        # for the current console context of execution
        state = {
            CURRENT_VALUE : str(),
            PENDING_NEWLINE_VALUE : False
        }

        def newline():
            # in case there's a newline character
            # pending to be flushed to the output
            if state[PENDING_NEWLINE_VALUE]:
                # outputs the newline character
                output_method("", True)
            # otherwise no newline is yet pending
            else:
                # sets the state to pending newline
                state[PENDING_NEWLINE_VALUE] = True

        def message(string_value):
            # processes the possible pending newline
            # characters in the buffer
            newline()

            # outputs the string value to the output
            # and updates the current value in the state
            output_method(string_value, False)
            state[CURRENT_VALUE] = string_value

        def action(action_name):
            # processes the possible pending newline
            # characters in the buffer
            newline()

            # outputs the name of the action to the output
            # (before asking for input values)
            output_method(action_name + " [y/N]? ", False)

            # retrieves the line using the appropriate method
            # in the console context and strips it
            line = self.get_line()
            line = line.rstrip("\n")

            # sets the state to not pending newline
            state[PENDING_NEWLINE_VALUE] = False

            # in case the retrieved line value is considered
            # to be a confirmation (yes)
            if line in ("y", "Y", "yes"):
                # returns valid value
                return True
            # otherwise it's considered to be a negation
            # of the action
            else:
                # returns invalid value
                return False

        def progress(percentage):
            # in case the percentage represents a complete
            # case (no more data to be processed)
            if percentage == COMPLETE_PERCENTAGE:
                output_method("\r" + state[CURRENT_VALUE] + " " + "Done", False)
            # otherwise the task is not considered to be
            # completed and so the percentage value is printed
            else:
                output_method("\r" + state[CURRENT_VALUE] + " " + str(percentage) + "%", False)

        # creates the map containing the various handlers
        # to be used during the operations
        handlers_map = {
            NEWLINE_VALUE : newline,
            MESSAGE_VALUE : message,
            ACTION_VALUE : action,
            PROGRESS_VALUE : progress
        }

        # returns the map of handlers to be used
        # in a console operation
        return handlers_map

    @colony.public
    def flush_handlers_map(self, handlers_map):
        return colony.notify("newline", handlers_map)

    @colony.public
    def layout_items(self, items, output_method):
        """
        "Layouts" a set of items flushing them to the current
        output in an ordered fashion.
        This method falls-back to an unordered strategy in case
        not all the information could be retrieved from the console.

        :type items: List
        :param items: A list/set of items to output using the given
        output method in an ordered fashion.
        :type output_method: Function
        :param output_method: Method used to output string to the
        current output flow.
        """

        # retrieves the size structure
        size_structure = self.get_size()

        # in case the size structure is defined
        # (it's possible to retrieve console size)
        if size_structure:
            # layouts the items as a set of columns (using
            # the console size)
            self._layout_items_column(items, output_method)
        # otherwise the console size it's not possible to be
        # retrieved (must layout vertically)
        else:
            # layouts the various items as a flow of items
            # in a vertical fashion
            self._layout_items_flow(items, output_method)

    @colony.public
    def get_line(self):
        """
        Retrieves a (command) line using the current best match
        for console input.
        This method shall preferably use a method that can provide
        feature like: history and cursor movement.

        :rtype: String
        :return: The string value of the line that has been read.
        """

        # retrieves the correct get line method according
        # to the internal defined value
        get_line_method = self._get_line or sys.stdin.readline

        # returns the result of the get line method calling
        # the system method is used in case none is defined
        return get_line_method()

    @colony.public
    def get_size(self):
        """
        Retrieves the current console size using the current
        best match for it.

        :rtype: Tuple
        :return: A tuple containing the width and the height
        of the current console window, or invalid in case it
        could not be retrieved.
        """

        # retrieves the size tuple for the appropriate get size
        # method or sets it as invalid
        size_tuple = self._get_size and self._get_size() or None

        # returns the size tuple
        return size_tuple

    @colony.public
    def process_command_line(self, command_line, output_method):
        return self.console.process_command_line(command_line, output_method, self._proxy_instance)

    @colony.public
    def get_command_line_alternatives(self, command, arguments):
        return self.console.get_command_line_alternatives(command, arguments, self._proxy_instance)

    @colony.public
    def create_console_interface_character(self, console_handler):
        return self.console.create_console_interface_character(console_handler)

    @colony.public
    def set_get_line(self, get_line):
        """
        Sets the get line method (method
        to retrieve a line).

        :type get_line: Function
        :param get_line: The get line method
        (method to retrieve a line).
        """

        self._get_line = get_line

    @colony.public
    def set_get_size(self, get_size):
        """
        Sets the get size method (method
        to retrieve the console size).

        :type get_line: Function
        :param get_line: The get size method (method
        to retrieve the console size).
        """

        self._get_size = get_size

    @colony.public
    def get_base_name(self):
        """
        Returns the base name.

        :rtype: String
        :return: The base name.
        """

        # retrieves the base name
        base_name = os.path.basename(self.path)

        # returns the base name
        return base_name

    @colony.public
    def get_full_path(self, base_path):
        """
        Returns the full path for the given
        base path value.

        :type base_path: base_path
        :param base_path: The base path to retrieve
        the full path.
        :rtype: String
        :return: The full path for the given base path.
        """

        # retrieves the value of the is absolute path
        is_absolute_path = os.path.isabs(base_path)

        # in case the base path is absolute
        if is_absolute_path:
            # sets the path as the base path
            path = base_path
        else:
            # joins the current path with the base path
            # to creates the path
            path = os.path.join(self.path, base_path)

        # normalizes the path
        path = os.path.normpath(path)

        # returns the path
        return path

    @colony.public
    def get_path(self):
        """
        Returns the path.

        :rtype: String
        :return: The path.
        """

        return self.path

    @colony.public
    def set_path(self, path):
        """
        Sets the path.

        :rtype: String
        :return: The path.
        """

        self.path = path

    @colony.public
    def get_user(self):
        """
        Returns the user.

        :rtype: String
        :return: The user.
        """

        return self.user

    def set_user(self, user):
        """
        Sets the user.

        :rtype: String
        :return: The user.
        """

        self.user = user

    def _layout_items_flow(self, items, output_method):
        # iterates over all the items to print them
        for item in items:
            # outputs the current items
            output_method(item)

    def _layout_items_column(self, items, output_method):
        # in case no items are defined
        if not items:
            # returns immediately
            return

        # retrieves the size structure
        width, _height = self.get_size()

        # starts the initial length for the
        # biggest item
        biggest_length = 0

        # iterates over all the items to determine
        # the biggest item
        for item in items:
            # retrieves the item length
            item_length = len(item)

            # sets the "new" biggest (item) length according to the
            # item length just read (updating it if necessary)
            biggest_length = item_length > biggest_length and item_length or biggest_length

        # increments the biggest length by one (extra space)
        biggest_length += 1

        # initializes the current index counter
        current_index = 0

        # calculates the biggest (item) length taking into account
        # possible item width "overflow"
        biggest_length = biggest_length >= width and width - 1 or biggest_length

        # iterates over all the items to print them
        for item in items:
            # retrieves the item length
            item_length = len(item)

            # in case the current line is going to overflow
            # (need to reset line value)
            if current_index + biggest_length >= width:
                # resets the current index value and
                # print a newline character
                current_index = 0
                output_method("")

            # writes the value of the path item
            output_method(item, False)

            # starts the line spacing string
            line_spacing = ""

            # iterates over the remaining space to be filled
            # with space characters
            for _index in colony.legacy.xrange(biggest_length - item_length):
                # adds a space to the line spacing string
                # value (augments the line string)
                line_spacing += " "

            # writes the line spacing to the output
            output_method(line_spacing, False)

            # increments the current index with the length
            # (width) of the biggest item
            current_index += biggest_length

        # print a newline character
        output_method("")
