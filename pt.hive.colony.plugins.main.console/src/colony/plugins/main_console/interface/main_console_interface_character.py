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

__revision__ = "$LastChangedRevision: 7613 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-19 08:18:06 +0000 (sex, 19 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys

SPECIAL_CHARACTER_ORDINAL = 0xe0
""" The special character ordinal """

BACKSPACE_CHARACTER_ORDINAL = 0x08
""" The backspace character ordinal """

TAB_CHARACTER_ORDINAL = 0x09
""" The tab character ordinal """

ENTER_CHARACTER_ORDINAL = 0x0d
""" The enter character ordinal """

UP_CHARACTER_ORDINAL = (SPECIAL_CHARACTER_ORDINAL, 0x48)
""" The up character ordinal """

DOWN_CHARACTER_ORDINAL = (SPECIAL_CHARACTER_ORDINAL, 0x50)
""" The down character ordinal """

LINE_HISTORY_LIST_MAXIMUM_SIZE = 100
""" The line history list maximum size """

class MainConsoleInterfaceCharacter:
    """
    The main console interface character.
    """

    main_console_interface_plugin = None
    """ The main console interface plugin """

    main_console_interface = None
    """ The main console interface """

    character_methods_map = {}
    """ The character methods map """

    line_history_index = None
    """ The line history index """

    line_buffer = []
    """ The current line buffer """

    line_history_list = []
    """ The current line history list """

    def __init__(self, main_console_interface_plugin, main_console_interface):
        """
        Constructor of the class.

        @type main_console_interface_plugin: MainConsoleInterfacePlugin
        @param main_console_interface_plugin: The main console interface plugin.
        @type main_console_interface: MainConsoleInterface
        @param main_console_interface: The main console interface.
        """

        self.main_console_interface_plugin = main_console_interface_plugin
        self.main_console_interface = main_console_interface

        self.character_methods_map = {BACKSPACE_CHARACTER_ORDINAL : self._process_backspace_character,
                                      TAB_CHARACTER_ORDINAL : self._process_tab_character,
                                      ENTER_CHARACTER_ORDINAL : self._process_enter_character,
                                      UP_CHARACTER_ORDINAL : self._process_up_character,
                                      DOWN_CHARACTER_ORDINAL : self._process_down_character}

        self.line_buffer = []
        self.line_history_list = []

    def start(self, parameters):
        # clears the line history list
        self.line_history_list = []

    def stop(self, parameters):
        pass

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
        # writes the character to the standard output
        sys.stdout.write(character)

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
        self._remove_character()

        # pops an item from the line buffer
        self.line_buffer.pop()

        # returns false (not end of line)
        return False

    def _process_tab_character(self, character, character_ordinal):
        # retrieves the main console plugin
        main_console_plugin = self.main_console_interface_plugin.main_console_plugin

        # joins the line buffer to retrieve the current line
        current_line = "".join(self.line_buffer)

        # retrieves the alternatives for the current line
        alternatives = main_console_plugin.get_command_line_alternatives(current_line)

        # sorts the alternatives
        alternatives.sort()

        # retrieves the alternatives length
        alternatives_length = len(alternatives)

        # in case no alternatives are found
        if alternatives_length == 0:
            pass
        # in case one alternative is found
        elif alternatives_length == 1:
            # retrieves the length of the current line
            current_line_length = len(current_line)

            # retrieves the first alternative
            first_alternative = alternatives[0]

            # retrieves the delta value
            delta_value = first_alternative[current_line_length:]

            # converts the delta value to list
            delta_list = list(delta_value)

            # extends the line buffer with the delta list
            self.line_buffer.extend(delta_list)

            # writes the delta value
            sys.stdout.write(delta_value)
        # in case many alternatives are found
        else:
            # breaks the line
            sys.stdout.write("\n")

            # iterates over all the alternatives
            for alternative in alternatives:
                # prints the alternative
                sys.stdout.write(alternative + "\n")

            # prints the caret
            self.main_console_interface._print_caret()

            # writes the current line
            sys.stdout.write(current_line)

        # returns false (not end of line)
        return False

    def _process_enter_character(self, character, character_ordinal):
        # breaks the line
        sys.stdout.write("\n")

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
            self._remove_character()

        # pops the last line buffer from the line history list
        self.line_buffer = self.line_history_list[self.line_history_index]

        # joins the line buffer to retrieve the current line
        current_line = "".join(self.line_buffer)

        # writes the current line
        sys.stdout.write(current_line)

    def _remove_character(self):
        """
        Removes a character from the standard output.
        """

        # writes the backspace character to the standard output
        sys.stdout.write("\x08")

        # writes the character to the standard output
        sys.stdout.write(" ")

        # writes the backspace character to the standard output
        sys.stdout.write("\x08")
