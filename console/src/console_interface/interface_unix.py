#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import time
import fcntl
import select
import struct
import termios

import exceptions

KEYBOARD_KEY_TIMEOUT = 0.02
""" The keyboard key timeout """

KEYBOARD_SELECT_TIMEOUT = 1.0
""" The keyboard select timeout """

CHARACTER_CONVERSION_MAP = {
    "\x0a" : "\x0d",
    "\x7f" : "\x08",
    ("\x1b", "\x5b", "\x41") : ("\xe0", "\x48"),
    ("\x1b", "\x5b", "\x42") : ("\xe0", "\x50"),
    ("\x1b", "\x5b", "\x43") : ("\xe0", "\x4d"),
    ("\x1b", "\x5b", "\x44") : ("\xe0", "\x4b")
}
""" The map for character conversion """

CHARACTER_ORDINAL_CONVERSION_MAP = {
    0x0a : 0x0d,
    0x7f : 0x08,
    (0x1b, 0x5b, 0x41) : (0xe0, 0x48),
    (0x1b, 0x5b, 0x42) : (0xe0, 0x50),
    (0x1b, 0x5b, 0x43) : (0xe0, 0x4d),
    (0x1b, 0x5b, 0x44) : (0xe0, 0x4b)
}
""" The map for character ordinal conversion """

IFLAG = 0
""" The iflag value """

CFLAG = 2
""" The cflag value """

LFLAG = 3
""" The lflag value """

CC = 6
""" The cc value """

CONSOLE_CONTEXT_VALUE = "console_context"
""" The console context value """

TEST_VALUE = "test"
""" The test value """

SPECIAL_CHARACTER_ORDINAL_VALUE = 0x1b
""" The special character ordinal value """

EXTRA_CHARACTER_ORDINAL_VALUE = 0x5b
""" The extra character ordinal value """

class ConsoleInterfaceUnix:
    """
    The console interface unix.
    """

    console_interface_plugin = None
    """ The console interface plugin """

    console_interface = None
    """ The console interface """

    console_interface_character = None
    """ The console interface character """

    console_context = None
    """ The console context """

    stdin_file_number = None
    """ The standard input file number """

    new_terminal_reference = None
    """ The new terminal reference """

    old_terminal_reference = None
    """ The old terminal reference """

    new_flags = None
    """ The new flags """

    old_flags = None
    """ The old flags """

    def __init__(self, console_interface_plugin, console_interface):
        """
        Constructor of the class.

        @type console_interface_plugin: ConsoleInterfacePlugin
        @param console_interface_plugin: The console interface plugin.
        @type console_interface: ConsoleInterface
        @param console_interface: The console interface.
        """

        self.console_interface_plugin = console_interface_plugin
        self.console_interface = console_interface

    def start(self, arguments):
        # retrieves the console plugin
        console_plugin = self.console_interface_plugin.console_plugin

        # retrieves the console context
        console_context = arguments.get(CONSOLE_CONTEXT_VALUE, None)

        # retrieves the test value
        test = arguments.get(TEST_VALUE, True)

        # sets the console context
        self.console_context = console_context

        # in case test mode is not enabled
        # runs the test
        test and self._run_test()

        # retrieves the standard input file number
        self.stdin_file_number = sys.stdin.fileno()

        # invalidates the "old" backup values
        self.old_flags = None

        # retrieves the terminal reference as new and old
        self.new_terminal_reference = termios.tcgetattr(self.stdin_file_number)
        self.old_terminal_reference = termios.tcgetattr(self.stdin_file_number)

        # changes the new terminal reference for echo
        self.new_terminal_reference[IFLAG] = self.new_terminal_reference[IFLAG] & ~(termios.BRKINT | termios.ICRNL | termios.INPCK | termios.ISTRIP | termios.IXON)
        self.new_terminal_reference[CFLAG] = self.new_terminal_reference[CFLAG] & ~(termios.CSIZE | termios.PARENB)
        self.new_terminal_reference[CFLAG] = self.new_terminal_reference[CFLAG] | termios.CS8
        self.new_terminal_reference[LFLAG] = self.new_terminal_reference[LFLAG] & ~(termios.ECHO | termios.ICANON | termios.IEXTEN)
        self.new_terminal_reference[CC][termios.VMIN] = 1
        self.new_terminal_reference[CC][termios.VTIME] = 0

        # sets the new terminal reference in the standard input
        termios.tcsetattr(self.stdin_file_number, termios.TCSANOW, self.new_terminal_reference)

        # retrieves the "old" flags for the standard input
        self.old_flags = fcntl.fcntl(self.stdin_file_number, fcntl.F_GETFL)

        # creates the new flags from the old flags
        self.new_flags = self.old_flags | os.O_NONBLOCK #@UndefinedVariable

        # creates the console interface character
        self.console_interface_character = console_plugin.create_console_interface_character(self, self.console_context)

        # starts the console interface character
        self.console_interface_character.start(arguments)

    def stop(self, arguments):
        # unsets the console context
        self.console_context = None

        # sets the old terminal reference in the standard input
        (not self.old_terminal_reference == None) and termios.tcsetattr(self.stdin_file_number, termios.TCSAFLUSH, self.old_terminal_reference)

        # sets the old flags in the standard input
        (not self.old_flags == None) and fcntl.fcntl(self.stdin_file_number, fcntl.F_SETFL, self.old_flags)

        # unsets the old terminal reference and the old flags
        self.old_terminal_reference = None
        self.old_flags = None

        # stops the console interface character
        self.console_interface_character and self.console_interface_character.stop(arguments)

    def cleanup(self, arguments):
        # sets the old terminal reference in the standard input
        (not self.old_terminal_reference == None) and termios.tcsetattr(self.stdin_file_number, termios.TCSAFLUSH, self.old_terminal_reference)

        # sets the old flags in the standard input
        (not self.old_flags == None) and fcntl.fcntl(self.stdin_file_number, fcntl.F_SETFL, self.old_flags)

        # unsets the old terminal reference and the old flags
        self.old_terminal_reference = None
        self.old_flags = None

        # cleanups the console interface character
        self.console_interface_character and self.console_interface_character.cleanup(arguments)

    def get_line(self):
        # starts the line
        self.console_interface_character.start_line()

        # iterates continuously
        while True:
            # in case the continue flag is not set
            if not self.console_interface.continue_flag:
                # returns immediately
                return

            # "selects" the standard input
            selected_values = select.select([sys.stdin], [], [], KEYBOARD_SELECT_TIMEOUT)

            # in case no values are selected (timeout)
            if selected_values == ([], [], []):
                # continues the loop
                continue

            try:
                # retrieves the character from the
                # standard input
                character = sys.stdin.read(1)
            except IOError:
                # sleeps for a while
                time.sleep(KEYBOARD_KEY_TIMEOUT)

                # continues the loop
                continue

            # converts the character to ordinal
            character_ordinal = ord(character)

            # in case the character ordinal value is possibly "special"
            if character_ordinal == SPECIAL_CHARACTER_ORDINAL_VALUE:
                try:
                    # retrieves an extra character from the
                    # standard input
                    extra_character = sys.stdin.read(1)

                    # convert the extra character to ordinal
                    extra_character_ordinal = ord(extra_character)

                    # in case the character ordinal value is "special"
                    if extra_character_ordinal == EXTRA_CHARACTER_ORDINAL_VALUE:
                        # retrieves the final character from the
                        # standard input
                        final_character = sys.stdin.read(1)

                        # convert the final character to ordinal
                        final_character_ordinal = ord(final_character)

                        # sets the character as the tuple
                        # with the final character
                        character = (
                            character,
                            extra_character,
                            final_character
                        )

                        # sets the character ordinal as the tuple
                        # with the extra character ordinal
                        character_ordinal = (
                            character_ordinal,
                            extra_character_ordinal,
                            final_character_ordinal
                        )
                except IOError:
                    # ignores no special sequence
                    pass

            # tries to convert the character using the conversion map
            character = CHARACTER_CONVERSION_MAP.get(character, character)

            # tries to convert the character ordinal using the conversion map
            character_ordinal = CHARACTER_ORDINAL_CONVERSION_MAP.get(character_ordinal, character_ordinal)

            # processes the character
            if self.console_interface_character.process_character(character, character_ordinal):
                # breaks the loop
                break

            # flushes the standard output
            sys.stdout.flush()

        # ends the line and returns it
        line = self.console_interface_character.end_line()

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
            # retrieves the console size value from the termios
            # reference values
            console_size_value = fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack("HHHH", 0, 0, 0, 0))

            # unpacks the console size value into height and width
            # and the hp and wp values
            height, width, _hp, _wp = struct.unpack("HHHH", console_size_value)

            # creates the size tuple from the
            # width and the height of the console
            size_tuple = (width, height)
        except:
            # in case the retrieval of the size fails
            # the size tuple is invalidated
            size_tuple = None

        # returns the size tuple value
        return size_tuple

    def _run_test(self):
        # retrieves the is tty value
        is_tty = sys.stdin.isatty()

        # in case the current standard input is not tty
        # must raise the incompatible console interface
        # to be able to indicate that the performance of
        # the current system will be compromised (not tty)
        if not is_tty:
            raise exceptions.IncompatibleConsoleInterface("invalid terminal mode")

    def _print(self, string_value):
        # writes the string value to the
        # standard output
        sys.stdout.write(string_value)

    def _print_caret(self):
        # prints the caret using the
        # console interface
        self.console_interface._print_caret(self.console_context)

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
        sys.stdout.write("\033[%dA", amount)

    def _cursor_down(self, amount = 1):
        sys.stdout.write("\033[%dB", amount)

    def _cursor_right(self, amount = 1):
        sys.stdout.write("\033[%dC" % amount)

    def _cursor_left(self, amount = 1):
        sys.stdout.write("\033[%dD" % amount)
