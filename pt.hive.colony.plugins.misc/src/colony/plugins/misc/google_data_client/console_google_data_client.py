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

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

CONSOLE_EXTENSION_NAME = "google_data_client"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

INVALID_OPERATION_MESSAGE = "invalid operation"
""" The invalid operation message """

HELP_TEXT = "### GOOGLE DATA CLIENT HELP ###\n\
google_connect <username> <password>     - connects to the google data services\n\
google_youtube <operation> [arguments..] - uses one of the google services"
""" The help text """

class ConsoleGoogleDataClient:
    """
    The console google data client class.
    """

    google_data_client_plugin = None
    """ The google data client plugin """

    commands = ["google_connect", "google_youtube"]
    """ The commands list """

    def __init__(self, google_data_client_plugin):
        """
        Constructor of the class.

        @type google_data_client_plugin: GoogleDataClientPlugin
        @param google_data_client_plugin: The google data client plugin.
        """

        self.google_data_client_plugin = google_data_client_plugin

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_google_connect(self, args, output_method):
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        google_username = args[0]
        google_password = args[1]

        self.google_data_client_plugin.google_data_client.connect(google_username, google_password)

    def process_google_youtube(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        youtube_operation = args[0]
        youtube_arguments = args[1:]

        method_name = "youtube_" + youtube_operation

        # in case the operation is not valid (it does no exist)
        if not hasattr(self.google_data_client_plugin.google_data_client, method_name):
            output_method(INVALID_OPERATION_MESSAGE)
            return

        method = getattr(self.google_data_client_plugin.google_data_client, method_name)

        value = method(*youtube_arguments)

        output_method("the return value is: " + str(value))
