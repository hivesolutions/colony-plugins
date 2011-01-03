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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys

import main_service_telnet_console_handler_exceptions

HANDLER_NAME = "console"
""" The handler name """

BRANDING_TEXT = "Hive Colony %s (Hive Solutions Lda. r%s:%s %s)"
""" The branding text value """

VERSION_PRE_TEXT = "Python "
""" The version pre text value """

HELP_TEXT = "Type \"help\" for more information."
""" The help text value """

class MainServiceTelnetConsoleHandler:
    """
    The main service telnet console handler class.
    """

    main_service_telnet_console_handler_plugin = None
    """ The main service telnet console handler plugin """

    def __init__(self, main_service_telnet_console_handler_plugin):
        """
        Constructor of the class.

        @type main_service_telnet_console_handler_plugin: MainServiceTelnetConsoleHandlerPlugin
        @param main_service_telnet_console_handler_plugin: The main service telnet console handler plugin.
        """

        self.main_service_telnet_console_handler_plugin = main_service_telnet_console_handler_plugin

    def get_handler_name(self):
        return HANDLER_NAME

    def handle_request(self, request):
        # retrieves the request method
        message = request.get_message()

        try:
            # creates the write function for the given request
            write_function = self.create_write(request)
        except Exception, exception:
            # raises the write function creation error
            raise main_service_telnet_console_handler_exceptions.WriteFunctionCreationError("problem creating write function: " + unicode(exception))

        # processes the command line
        self.main_service_telnet_console_handler_plugin.main_console_plugin.process_command_line(message, write_function)

        # writes the caret
        request.write(">> ")

    def handle_initial_request(self, request):
        # generates the information
        information = self.generate_information()

        # writes the information
        request.write(information)

        # writes the caret
        request.write(">> ")

    def create_write(self, request):
        """
        Create a write function for the given request.

        @type request: IrcRequest
        @param request: The irc request to be used in the
        created write function.
        @rtype: Function
        @return: The created write function.
        """

        def write(text, new_line = True):
            # replaces the newlines to newlines with carriage return
            raw_text = text.replace("\n", "\r\n")

            # in case a newline is required
            if new_line:
                request.write(raw_text + "\r\n")
            else:
                request.write(raw_text)

        # returns the created write function
        return write

    def generate_information(self):
        """
        Generates the system information to be used as into message.

        @rtype: String
        @return: The system information to be used as into message.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_service_telnet_console_handler_plugin.manager

        # retrieves the plugin manager version
        plugin_manager_version = plugin_manager.get_version()

        # retrieves the plugin manager release
        plugin_manager_release = plugin_manager.get_release()

        # retrieves the plugin manager build
        plugin_manager_build = plugin_manager.get_build()

        # retrieves the plugin manager release date
        plugin_manager_release_date = plugin_manager.get_release_date()

        # creates the information string
        information = str()

        # adds the branding information text
        information += BRANDING_TEXT % (plugin_manager_version, plugin_manager_release, plugin_manager_build, plugin_manager_release_date) + "\r\n"

        # adds the python information
        information += VERSION_PRE_TEXT + sys.version + "\r\n"

        # adds the help text
        information += HELP_TEXT + "\r\n"

        # returns the information
        return information
