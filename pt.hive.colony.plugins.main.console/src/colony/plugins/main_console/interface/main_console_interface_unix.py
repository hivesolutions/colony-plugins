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
import fcntl
import termios

KEYBOARD_KEY_TIMEOUT = 0.02
""" The keyboard key timeout """

class MainConsoleInterfaceUnix:
    """
    The main console interface unix.
    """

    main_console_interface_plugin = None
    """ The main console interface plugin """

    main_console_interface = None
    """ The main console interface """

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
        # retrieves the standard input file number
        self.stdin_file_number = sys.stdin.fileno()

        # retrieves the terminal reference as new and old
        self.new_terminal_reference = termios.tcgetattr(self.stdin_file_number)
        self.old_terminal_reference = termios.tcgetattr(self.stdin_file_number)

        # changes the new terminal reference for echo
        self.new_terminal_reference[3] = self.new_terminal_reference[3] & ~termios.ICANON & ~termios.ECHO

        # sets the new terminal reference in the standard input
        termios.tcsetattr(self.stdin_file_number, termios.TCSANOW, self.new_terminal_reference)

        # retrieves the "old" flags for the standard input
        self.old_flags = fcntl.fcntl(self.stdin_file_number, fcntl.F_GETFL)

        # creates the new flags from the old flags
        self.new_flgags = self.old_flags | os.O_NONBLOCK #@UndefinedVariable

        # sets the new flags in the standard input
        fcntl.fcntl(self.stdin_file_number, fcntl.F_SETFL, self.new_flgags)

    def stop(self, arguments):
        # sets the old terminal reference in the standard input
        termios.tcsetattr(self.stdin_file_number, termios.TCSAFLUSH, self.old_terminal_reference)

        # sets the old flags in the standard input
        fcntl.fcntl(self.stdin_file_number, fcntl.F_SETFL, self.old_flags)

    def get_line(self):
        # iterates continuously
        while True:
            # in case the continue flag is not set
            if not self.main_console_interface.continue_flag:
                # returns immediately
                return

            try:
                # retrieves the character from the
                # standard input
                character = sys.stdin.read(1)

                # prints the character
                print character,
            except IOError:
                # sleeps for a while
                time.sleep(KEYBOARD_KEY_TIMEOUT)
