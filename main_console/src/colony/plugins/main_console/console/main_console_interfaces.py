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

import types

SPECIAL_CHARACTER_ORDINAL = 0xe0
""" The special character ordinal """

BACKSPACE_CHARACTER_ORDINAL = 0x08
""" The backspace character ordinal """

TAB_CHARACTER_ORDINAL = 0x09
""" The tab character ordinal """

ENTER_CHARACTER_ORDINAL = 0x0d
""" The enter character ordinal """

UP_CHARACTER_ORDINAL = (
    SPECIAL_CHARACTER_ORDINAL,
    0x48
)
""" The up character ordinal """

DOWN_CHARACTER_ORDINAL = (
    SPECIAL_CHARACTER_ORDINAL,
    0x50
)
""" The down character ordinal """

RIGHT_CHARACTER_ORDINAL = (
    SPECIAL_CHARACTER_ORDINAL,
    0x4d
)
""" The right character ordinal """

LEFT_CHARACTER_ORDINAL = (
    SPECIAL_CHARACTER_ORDINAL,
    0x4b
)
""" The right character ordinal """

LINE_HISTORY_LIST_MAXIMUM_SIZE = 100
""" The line history list maximum size """

class MainConsoleInterfaceCharacter:
    """
    The main console interface character.
    Provides the basic abstraction to handle things like
    command history and cursor movement.
    Some internals structure are required for the handling
    of these kind of operations.
    """

    main_console = None
    """ The main console """

    console_handler = None
    """ The console handler """

    console_context = None
    """ The console context """

    character_methods_map = {}
    """ The character methods map """

    line_history_index = None
    """ The line history index """

    line_buffer = []
    """ The current line buffer """

    line_history_list = []
    """ The current line history list """

    def __init__(self, main_console, console_handler, console_context):
        """
        Constructor of the class.

        @type main_console: MainConsole
        @param main_console: The main console.
        @type console_handler: ConsoleHandler
        @param console_handler: The console handler to be used.
        @type console_context: ConsoleContext
        @param console_context: The console context to be used.
        """

        self.main_console = main_console
        self.console_handler = console_handler
        self.console_context = console_context

        self.character_methods_map = {
            BACKSPACE_CHARACTER_ORDINAL : self._process_backspace_character,
            TAB_CHARACTER_ORDINAL : self._process_tab_character,
            ENTER_CHARACTER_ORDINAL : self._process_enter_character,
            UP_CHARACTER_ORDINAL : self._process_up_character,
            DOWN_CHARACTER_ORDINAL : self._process_down_character,
            RIGHT_CHARACTER_ORDINAL : self._process_right_character,
            LEFT_CHARACTER_ORDINAL : self._process_left_character
        }

        self.line_buffer = []
        self.line_history_list = []

    def start(self, parameters):
        # clears the line history list
        self.line_history_list = []

    def stop(self, parameters):
        pass

    def cleanup(self, parameters):
        pass

    def get_size(self):
        """
        Retrieves the size of the terminal currently being used.
        This method is considered to be fail prone and so the
        caller must the cautious in the handling of it.
        On failure this function returns an invalid value (none).

        @rtype: Tuple
        @return: A tuple containing the width and the height of
        the current console window.
        """

        return None

    def start_line(self):
        # start the line buffer
        self.line_buffer = []

        # adds the temporary element to history
        self._add_history()

        # starts the line history index value
        self.line_history_index = -1

    def end_line(self):
        # removes the last element (temporary) from history
        self._remove_history()

        # in case the line buffer is valid (not empty) and the line history list
        # is not valid or the line buffer is different than the list item in the line history
        if self.line_buffer and (not self.line_history_list or not self.line_buffer == self.line_history_list[-1]):
            # adds the current line buffer to history
            self._add_history()

        # joins the line buffer to retrieve the line
        line = "".join(self.line_buffer)

        # returns the line
        return line

    def process_character(self, character, character_ordinal):
        # retrieves the character method from the character method
        # map using the character ordinal value
        character_method = self.character_methods_map.get(character_ordinal, None)

        # in case the character method is defined
        if character_method:
            # calls the character method with the
            # character and the character ordinal
            # and retrieves the return value
            return_value = character_method(character, character_ordinal)
        elif character_ordinal > 0x19:
            # calls the process writable character
            # method
            return_value = self._process_writable_character(character, character_ordinal)
        # otherwise
        else:
            # sets the return value to false
            return_value = False

        # returns the return value
        return return_value

    def _process_writable_character(self, character, character_ordinal):
        # retrieve the character type
        character_type = type(character)

        # in case the character type is not string
        if not character_type == types.StringType:
            # returns immediately false (not end of line)
            return

        # prints the character
        self.console_handler._print(character)

        # adds the character to the line buffer
        self.line_buffer.append(character)

        # returns false (not end of line)
        return False

    def _process_backspace_character(self, character, character_ordinal):
        # in case the line buffer is
        # not valid
        if not self.line_buffer:
            # returns immediately false (not end of line)
            return False

        # removes a character from the standard output
        self.console_handler._remove_character()

        # pops an item from the line buffer
        self.line_buffer.pop()

        # returns false (not end of line)
        return False

    def _process_tab_character(self, character, character_ordinal):
        # retrieves the current line
        current_line = self._get_current_line()

        # retrieves the current last token
        current_last_token = self._get_current_last_token()

        # splits the command line into command and arguments
        command, arguments = self.main_console.split_command_line(current_line, True)

        # retrieves the alternatives list and the best match
        # for the current command and arguments
        alternatives_list, best_match = self.console_context.get_command_line_alternatives(command, arguments)

        # sorts the alternatives list (alphabetically)
        alternatives_list.sort()

        # retrieves the alternatives list length
        alternatives_list_length = len(alternatives_list)

        # in case no alternatives are found
        if alternatives_list_length == 0:
            # ignores the choice
            pass
        # in case one alternative is found
        elif alternatives_list_length == 1:
            # completes the alternative
            self._complete_alternative(best_match)
        # in case many alternatives are found
        else:
            # in case the best match is the same
            # as the current last token
            if best_match == current_last_token:
                # shows the alternatives
                self._show_alternatives(alternatives_list)
            # otherwise the current line
            # must be completed
            else:
                # completes the alternative
                self._complete_alternative(best_match)

        # returns false (not end of line)
        return False

    def _process_enter_character(self, character, character_ordinal):
        # breaks the line
        self.console_handler._print("\n")

        # returns true (end of line)
        return True

    def _process_up_character(self, character, character_ordinal):
        # retrieves the line history list length
        line_history_list_length = len(self.line_history_list)

        # in case the line history index overflows
        if self.line_history_index * -1 >= line_history_list_length:
            # returns immediately false (not end of line)
            return False

        # decrements the line history index
        self.line_history_index -= 1

        # shows the history
        self._show_history()

        # returns false (not end of line)
        return False

    def _process_down_character(self, character, character_ordinal):
        # in case the line history index overflows
        if self.line_history_index * -1 <= 1:
            # returns immediately false (not end of line)
            return False

        # increments the line history index
        self.line_history_index += 1

        # shows the history
        self._show_history()

        # returns false (not end of line)
        return False

    def _process_right_character(self, character, character_ordinal):
        self.console_handler._cursor_right()

        # returns false (not end of line)
        return False

    def _process_left_character(self, character, character_ordinal):
        self.console_handler._cursor_left()

        # returns false (not end of line)
        return False

    def _add_history(self):
        """
        Adds the current line buffer element
        to the history "list".
        """

        # retrieves the line history length
        line_history_length = len(self.line_history_list)

        # in case the line history overflows
        if line_history_length > LINE_HISTORY_LIST_MAXIMUM_SIZE:
            # pops the last "oldest" element
            # from the line history
            self.line_history_list.pop(0)

        # adds the line buffer to the line
        # history list
        self.line_history_list.append(self.line_buffer)

    def _remove_history(self):
        """
        Removes the last element from the
        history "list".
        """

        # pops the temporary value
        self.line_history_list.pop()

    def _show_history(self):
        """
        Shows the current history in the output
        method.
        """

        # retrieves the line buffer length
        line_buffer_length = len(self.line_buffer)

        # iterates over the range of the line
        # buffer length
        for _index in range(line_buffer_length):
            # removes a character from the standard output
            self.console_handler._remove_character()

        # pops the last line buffer from the line history list
        self.line_buffer = self.line_history_list[self.line_history_index]

        # joins the line buffer to retrieve the current line
        current_line = "".join(self.line_buffer)

        # prints the current line
        self.console_handler._print(current_line)

    def _complete_alternative(self, best_match):
        """
        Completes the current line value with the
        given best match.

        @type best_match: String
        @param best_match: The best match to complete
        the current line value.
        """

        # retrieves the current last token
        current_last_token = self._get_current_last_token()

        # retrieves the length of the current last token
        current_last_token_length = len(current_last_token)

        # retrieves the delta value
        delta_value = best_match[current_last_token_length:]

        # converts the delta value to list
        delta_list = list(delta_value)

        # extends the line buffer with the delta list,
        # updating the line buffer
        self.line_buffer.extend(delta_list)

        # prints the delta value
        self.console_handler._print(delta_value)

    def _show_alternatives(self, alternatives_list):
        """
        Shows the given alternatives list in the output
        method.

        @type alternatives_list: List
        @param alternatives_list: The list of alternatives to
        show.
        """

        # retrieves the current line
        current_line = self._get_current_line()

        # breaks the line
        self.console_handler._print("\n")

        # layouts the alternatives list to obtains the maximum
        # usage from the available console space
        self.console_context.layout_items(alternatives_list, self._write)

        # prints the caret
        self.console_handler._print_caret()

        # prints the current line
        self.console_handler._print(current_line)

    def _get_current_line(self):
        # joins the line buffer to retrieve the current line
        current_line = "".join(self.line_buffer)

        # returns the current line
        return current_line

    def _get_current_last_token(self):
        # joins the line buffer to retrieve the current line
        current_line = "".join(self.line_buffer)

        # splits the current line into a list of tokens
        current_line_list = self.main_console.split_command_line_arguments(current_line, True)

        # retrieves the current last token
        current_last_token = current_line_list and current_line_list[-1] or ""

        # returns the current last token
        return current_last_token

    def _write(self, text, new_line = True):
        """
        Writes the given text to the standard output,
        may use a newline or not.

        @type text: String
        @param text: The text to be written to the standard output.
        @type new_line: bool
        @param new_line: If the text should be suffixed with a newline.
        """

        # prints (writes) the text contents
        self.console_handler._print(text)

        # in case a newline should be appended
        # writes it
        new_line and self.console_handler._print("\n")
