#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys

import colony.base.system
import colony.libs.map_util

import exceptions

console_interface_class = None

try:
    if not console_interface_class:
        import interface_win32
        console_interface_class = interface_win32.ConsoleInterfaceWin32
except:
    pass

try:
    if not console_interface_class:
        import interface_unix
        console_interface_class = interface_unix.ConsoleInterfaceUnix
except:
    pass

CARET = "$"
""" The caret to be used in the console display """

LOGIN_AS_MESSAGE = "Login as"
""" The login as message """

PASSWORD_MESSAGE = "Password"
""" The password message """

LOGIN_FAILED_MESSAGE = "Login failed, try again..."
""" The login failed message """

ACTIVE_VALUE = "active"
""" The active value """

CONSOLE_CONTEXT_VALUE = "console_context"
""" The console context value """

TEST_VALUE = "test"
""" The test value """

ANONYMOUS_VALUE = "anonymous"
""" The anonymous value """

class ConsoleInterface(colony.base.system.System):
    """
    The console interface class.
    """

    console_inteface_configuration = {}
    """ The console interface configuration """

    console_interface = None
    """ The console interface reference to be
    used in the current console interface """

    continue_flag = True
    """ The continue flag, used to control the
    shutdown of the plugin """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)
        self.console_interface_configuration = {}
        self.continue_flag = True

    def load_console(self):
        """
        Loads the console system and all of its internal structures.
        The loading of the console may involve the correct creation of
        the console context and the authorization of the user.
        """

        # retrieves the console plugin
        console_plugin = self.plugin.console_plugin

        # notifies the ready semaphore
        self.plugin.release_ready_semaphore()

        # retrieves the active configuration value (checks if
        # the console interface should start)
        active = self.console_interface_configuration.get(ACTIVE_VALUE, True)

        # in case the active flag is not set, must return immediately
        # no need to load the console
        if not active: return

        # in case the console interface class is not defined, must
        # raise the undefined console exception
        if not console_interface_class:
            raise exceptions.UndefinedConsoleInterface("no class available")

        # creates a new console interface system and uses it to
        # create a new console context to be used
        self.console_interface = console_interface_class(self.plugin, self)
        console_context = console_plugin.create_console_context()

        try:
            # defines the parameters
            parameters = {
                CONSOLE_CONTEXT_VALUE : console_context,
                TEST_VALUE : True
            }

            # starts the console interface
            self.console_interface.start(parameters)

            # sets the console interface get line method
            # as the console interface method
            console_interface_method = self.console_interface.get_line
        except BaseException, exception:
            # prints a warning message
            self.plugin.warning("Problem starting console interface: %s" % unicode(exception))

            # sets the read line method as the console interface
            # method as a method for fallback
            console_interface_method = sys.stdin.readline

        # sets the method used to retrieve a line in the current
        # console's context
        console_context.set_get_line(console_interface_method)

        # sets the method used to retrieve the console size in the current
        # console's context
        console_context.set_get_size(self.console_interface.get_size)

        try:
            # prompts the login using the console context
            self._prompt_login(console_context, console_interface_method)

            # prompts the command line using the console context
            self._prompt_command_line(console_context, console_interface_method)
        finally:
            # stops the console interface
            self.console_interface.stop({})

    def unload_console(self):
        """
        Unloads the console system and all of its internal structures.
        """

        # clenaups the console interface in case
        # it's valid (defined and loaded)
        self.console_interface and self.console_interface.cleanup({})

        # unsets the continue flag
        self.continue_flag = False

        # notifies the ready semaphore
        self.plugin.release_ready_semaphore()

    def set_configuration_property(self, configuration_property):
        # retrieves the configuration
        configuration = configuration_property.get_data()

        # cleans the console interface configuration
        colony.libs.map_util.map_clean(self.console_interface_configuration)

        # copies the service configuration to the console interface configuration
        colony.libs.map_util.map_copy(configuration, self.console_interface_configuration)

    def unset_configuration_property(self):
        # cleans the console interface configuration
        colony.libs.map_util.map_clean(self.console_interface_configuration)

    def _prompt_login(self, console_context, console_interface_method):
        # unsets the authentication result
        authentication_result = None

        # if the continue flag is valid continues the iteration
        while self.continue_flag:
            # prompts the login as message using the console
            # interface method, retrieving the username
            username = self._prompt_value(LOGIN_AS_MESSAGE + ": ", console_interface_method)

            # prompts the password message using the console
            # interface method, retrieving the password
            password = self._prompt_value(PASSWORD_MESSAGE + ": ", console_interface_method)

            # authenticates the user (throught the console system)
            authentication_result = console_context.authenticate_user(username, password)

            # in case the authentication as succeed
            if authentication_result:
                # breaks the cycle
                break

            # writes the login failed message
            sys.stdout.write(LOGIN_FAILED_MESSAGE + "\n")

            # flushes the standard output
            sys.stdout.flush()

    def _prompt_command_line(self, console_context, console_interface_method):
        # if the continue flag is valid continues the iteration
        while self.continue_flag:
            # prints the caret
            self._print_caret(console_context)

            # flushes the standard output
            sys.stdout.flush()

            # retrieves the line using the console interface method
            line = console_interface_method()

            # in case there is no valid line
            if not line:
                # continues the cycle (nothing
                # to be processed in this line)
                continue

            # processes the command line, outputting the result to
            # the default method
            console_context.process_command_line(line, None)

    def _prompt_value(self, message, console_interface_method):
        # writes the message
        sys.stdout.write(message)

        # flushes the standard output
        sys.stdout.flush()

        # retrieves the read value using the console interface method
        read_value = console_interface_method()

        # strips the read value
        read_value = read_value and read_value.rstrip("\n") or read_value

        # returns the read value
        return read_value

    def _print_caret(self, console_context):
        # retrieves the console user
        console_user = console_context.get_user()

        # retrieves the console user
        console_user = console_user or ANONYMOUS_VALUE

        # retrieves the console base name
        console_base_name = console_context.get_base_name()

        # writes the start line value
        sys.stdout.write("[%s@%s]" % (console_user, console_base_name))

        # writes the caret character
        sys.stdout.write(CARET + " ")
