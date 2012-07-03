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

import os
import sys
import time
import ctypes
import msvcrt
import struct

import main_console_interface_exceptions

KEYBOARD_KEY_TIMEOUT = 0.02
""" The keyboard key timeout """

ASYNCHRONOUS_MODE_VALUE = 0x4000
""" The asynchronous  mode value """

SPECIAL_CHARACTER_ORDINAL_VALUE = 0xe0
""" The special character ordinal value """

CONSOLE_CONTEXT_VALUE = "console_context"
""" The console context value """

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

    main_console_interface_character = None
    """ The main console interface character """

    console_context = None
    """ The console context """

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
        # retrieves the main console plugin
        main_console_plugin = self.main_console_interface_plugin.main_console_plugin

        # retrieves the console context
        console_context = arguments.get(CONSOLE_CONTEXT_VALUE, None)

        # retrieves the test value
        test = arguments.get(TEST_VALUE, True)

        # sets the console context
        self.console_context = console_context

        # in case test mode is not enabled
        # runs the test
        test and self._run_test()

        # creates the main console interface character
        self.main_console_interface_character = main_console_plugin.create_console_interface_character(self, self.console_context)

        # starts the main console interface character
        self.main_console_interface_character.start(arguments)

    def stop(self, arguments):
        # unsets the console context
        self.console_context = None

        # stops the main console interface character
        self.main_console_interface_character and self.main_console_interface_character.stop(arguments)

    def cleanup(self, arguments):
        # cleanups the main console interface character
        self.main_console_interface_character and self.main_console_interface_character.cleanup(arguments)

    def get_line(self):
        # starts the line
        self.main_console_interface_character.start_line()

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

            # in case the character ordinal value is possibly "special"
            # and there is a keyboard hit
            if character_ordinal == SPECIAL_CHARACTER_ORDINAL_VALUE and msvcrt.kbhit():
                # reads a character from the standard input (locks)
                extra_character = msvcrt.getch()

                # convert the extra character to ordinal
                extra_character_ordinal = ord(extra_character)

                # in case the character ordinal value is "special"
                if extra_character_ordinal in (0x48, 0x50, 0x4d, 0x4b):
                    # sets the character as the tuple
                    # with the extra character
                    character = (
                        character,
                        extra_character
                    )

                    # sets the character ordinal as the tuple
                    # with the extra character ordinal
                    character_ordinal = (
                        character_ordinal,
                        extra_character_ordinal
                    )

            # processes the character
            if self.main_console_interface_character.process_character(character, character_ordinal):
                # breaks the loop
                break

            # flushes the standard output
            sys.stdout.flush()

        # ends the line and returns it
        line = self.main_console_interface_character.end_line()

        # returns the line
        return line

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

        try:
            # retrieves the handle to the standard output
            # device (console window)
            stdout_handle = ctypes.windll.kernel32.GetStdHandle(-12) #@UndefinedVariable

            # creates the console buffer info structure and populates
            # it using the get console screen buffer info function
            console_buffer_info = ctypes.create_string_buffer(22)
            result = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(stdout_handle, console_buffer_info) #@UndefinedVariable
        except:
            # returns an invalid value
            return None

        # in case the result is not valid or not
        # set the returned value is none
        if not result:
            # returns an invalid value
            return None

        # unpacks the console buffer info structure into the various
        # components of it
        _buffer_x, _buffer_y, _current_x, _current_y, _wattr, left, top, right, bottom, _max_x, _max_y = struct.unpack("hhhhHhhhhhh", console_buffer_info.raw)

        # calculates the width and the height of the console
        # window from the right, left, bottom, and top positions
        width = right - left + 1
        height = bottom - top + 1

        # creates the size tuple from the
        # width and the height of the console
        size_tuple = (width, height)

        # returns the size tuple value
        return size_tuple

    def _run_test(self):
        # retrieves the standard input file number
        stdin_file_number = sys.stdin.fileno()

        # retrieves the is tty value
        is_tty = sys.stdin.isatty()

        # tries to set the binary mode
        mode_value = msvcrt.setmode(stdin_file_number, os.O_TEXT)

        # in case the current standard input is not tty
        # or the mode value is not valid
        if not is_tty or not mode_value == ASYNCHRONOUS_MODE_VALUE:
            # raises the incompatible console interface
            raise main_console_interface_exceptions.IncompatibleConsoleInterface("invalid terminal mode")

    def _print(self, string_value):
        # writes the string value to the
        # standard output
        sys.stdout.write(string_value)

    def _print_caret(self):
        # prints the caret using the main
        # console interface
        self.main_console_interface._print_caret(self.console_context)

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

    def _cursor_top(self, amount = 1):
        pass

    def _cursor_down(self, amount = 1):
        pass

    def _cursor_right(self, amount = 1):
        pass

    def _cursor_left(self, amount = 1):
        pass
