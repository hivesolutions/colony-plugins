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

import os
import sys
import time
import msvcrt

import main_console_interface_exceptions

LINE_HISTORY_LIST_MAXIMUM_SIZE = 100
""" The line history list maximum size """

KEYBOARD_KEY_TIMEOUT = 0.02
""" The keyboard key timeout """

ASYNCHRONOUS_MODE_VALUE = 0x4000
""" The asynchronous  mode value """

TEST_VALUE = "test"
""" The test value """

class MainConsoleInterfaceWin32:
    """
    The main console interface win32.
    """

    main_console_interface_plugin = None
    """ The main console interface plugin """

    main_console_interface = None
    """ The main console interface """

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

    def start(self, arguments):
        # retrieves the test value
        test = arguments.get(TEST_VALUE, True)

        # starts the line history list
        self.line_history_list = []

        # in case test mode is not enabled
        if not test:
            # returns immediately
            return

        # retrieves the standard input file number
        stdin_file_number = sys.stdin.fileno()

        # tries to set the binary mode
        mode_value = msvcrt.setmode(stdin_file_number, os.O_TEXT)

        # in case the mode value is not valid
        if not mode_value == ASYNCHRONOUS_MODE_VALUE:
            # raises the incompatible console interface
            raise main_console_interface_exceptions.IncompatibleConsoleInterface("eof found while reading standard input")

    def stop(self, arguments):
        pass

    def get_line(self):
        # retrieves the main console plugin
        main_console_plugin = self.main_console_interface_plugin.main_console_plugin

        # creates the line buffer
        self.line_buffer = []

        # adds the temporary element to history
        self._add_history()

        # starts the index value
        index = -1

        # iterates continuously
        while True:
            # in case the continue flag is not set
            if not self.main_console_interface.continue_flag:
                # returns immediately
                return

            # in case there is a character (key) available
            if msvcrt.kbhit():
                # reads a character from the standard input (locks)
                character = msvcrt.getch()
            # otherwise
            else:
                # sleeps for a while
                time.sleep(KEYBOARD_KEY_TIMEOUT)

                # continues the loop
                continue

            # converts the character to ordinal
            character_ordinal = ord(character)

            # in case the character ordinal value is (up)
            if character_ordinal == 0xe0 and msvcrt.kbhit():
                # reads a character from the standard input (locks)
                extraCharacter = msvcrt.getch()

                # convert the extra character to ordinal
                extraCharacterOrdinal = ord(extraCharacter)

                # in case the character ordinal value is (up)
                if extraCharacterOrdinal == 0x48:
                    if index * -1 < len(self.line_history_list):
                        # decrements the index
                        index -= 1

                        # shows the history for the index
                        self._show_history(index)
                # in case the character ordinal value is (down)
                elif extraCharacterOrdinal == 0x50:
                    if index * -1 > 1:
                        # increments the index
                        index += 1

                        # shows the history for the index
                        self._show_history(index)
            # in case the character ordinal value is "backspace"
            elif character_ordinal == 0x08:
                # in case the line buffer is
                # not valid
                if not self.line_buffer:
                    # continues the loop
                    continue

                # removes a character from the standard output
                self._remove_character()

                # pops an item from the line buffer
                self.line_buffer.pop()
            # in case the character ordinal value is "tab"
            elif character_ordinal == 0x09:
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
                    sys.stdout.write("\r\n")

                    # iterates over all the alternatives
                    for alternative in alternatives:
                        sys.stdout.write(alternative + "\r\n")

                    # prints the caret
                    self.main_console_interface._print_caret()

                    # writes the current line
                    sys.stdout.write(current_line)
            # in case the character ordinal value is "enter"
            elif character_ordinal == 0x0d:
                # breaks the line
                sys.stdout.write("\r\n")

                # breaks the loop
                break
            # otherwise, in case the character is "visible"
            # use it as normal character
            elif character_ordinal > 0x19:
                # writes the character to the standard output
                sys.stdout.write(character)

                # adds the character to the line buffer
                self.line_buffer.append(character)

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

    def _handle_enter(self):
        pass

    def _add_history(self):
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
        # pops the temporary value
        self.line_history_list.pop()

    def _show_history(self, index):
        # retrieves the line buffer length
        line_buffer_length = len(self.line_buffer)

        # iterates over the range of the line
        # buffer length
        for _index in range(line_buffer_length):
            # removes a character from the standard output
            self._remove_character()

        # pops the last line buffer from the line history list
        self.line_buffer = self.line_history_list[index]

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
