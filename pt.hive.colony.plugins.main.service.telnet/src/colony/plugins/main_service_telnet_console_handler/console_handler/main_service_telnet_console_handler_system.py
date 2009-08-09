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

import os.path

import main_service_telnet_console_handler_exceptions

HANDLER_NAME = "console"
""" The handler name """

PLUGIN_HANDLER_VALUE = "plugin_handler"
""" The plugin handler value """

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

        # processes the command line
        self.main_service_telnet_console_handler_plugin.main_console_plugin.process_command_line(message, self.create_write(request))

        # writes the caret
        request.write(">> ")

    def create_write(self, request):
        def write(text, new_line = True):
            # replaces the newlines to newlines with carriage return
            raw_text = text.replace("\n", "\r\n")

            # in case a newline is required
            if new_line:
                request.write(raw_text + "\r\n")
            else:
                request.write(raw_text)

        return write
