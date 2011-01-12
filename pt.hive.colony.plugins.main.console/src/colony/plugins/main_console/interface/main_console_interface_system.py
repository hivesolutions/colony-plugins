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

import main_console_interface_exceptions

try:
    import main_console_interface_win32
    main_console_interface_class = main_console_interface_win32.MainConsoleInterfaceWin32
except Exception, exception:
    print exception

    try:
        import main_console_interface_unix
        main_console_interface_class = main_console_interface_unix.MainConsoleInterfaceUnix
    except:
        main_console_interface_class = None

CARET = ">>"
""" The caret to be used in the console display """

TEST_VALUE = "test"
""" The test value """

class MainConsoleInterface:
    """
    The main console interface class.
    """

    main_console_interface_plugin = None
    """ The main console interface plugin """

    continue_flag = True
    """ The continue flag, used to control the shutdown of the plugin """

    def __init__(self, main_console_interface_plugin):
        """
        Constructor of the class.

        @type main_console_interface_plugin: MainConsoleInterfacePlugin
        @param main_console_interface_plugin: The main console interface plugin.
        """

        self.main_console_interface_plugin = main_console_interface_plugin

        self.continue_flag = True

    def load_console(self):
        """
        Loads the console system.
        """

        # retrieves the main console plugin
        main_console_plugin = self.main_console_interface_plugin.main_console_plugin

        # notifies the ready semaphore
        self.main_console_interface_plugin.release_ready_semaphore()

        # in case the main console interface class is
        # not defined
        if not main_console_interface_class:
            # raises the undefined console interface exception
            raise main_console_interface_exceptions.UndefinedConsoleInterface("no class available")

        # creates a new main console interface system
        main_console_interface = main_console_interface_class(self.main_console_interface_plugin, self)

        try:
            # starts the main console interface
            main_console_interface.start({TEST_VALUE : True})

            # sets the main console interface get line method
            # as the main console interface method
            main_console_interface_method = main_console_interface.get_line
        except BaseException, exception:
            # prints a warning message
            self.main_console_interface_plugin.warning("Problem starting main console interface: %s" % unicode(exception))

            # sets the read line method as the main console interface
            # method as a method for fallback
            main_console_interface_method = sys.stdin.readline

        try:
            # if the continue flag is valid continues the iteration
            while self.continue_flag:
                # prints the caret
                self._print_caret()

                # retrieves the line using the main console interface method
                line = main_console_interface_method()

                # flushes the stdout
                sys.stdout.flush()

                # in case there is no valid line
                if not line:
                    # continues the cycle
                    continue

                # processes the command line, outputting the result to
                # the default method
                main_console_plugin.process_command_line(line, None)
        finally:
            # stops the main console interface
            main_console_interface.stop({})

    def unload_console(self):
        """
        Unloads the console system.
        """

        # unsets the continue flag
        self.continue_flag = False

        # notifies the ready semaphore
        self.main_console_interface_plugin.release_ready_semaphore()

    def _print_caret(self):
        # writes the caret character
        sys.stdout.write(CARET + " ")
