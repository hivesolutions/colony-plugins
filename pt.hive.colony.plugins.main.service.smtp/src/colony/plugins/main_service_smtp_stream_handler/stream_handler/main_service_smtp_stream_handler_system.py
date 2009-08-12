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

import main_service_smtp_stream_handler_exceptions

HANDLER_NAME = "stream"
""" The handler name """

PLUGIN_HANDLER_VALUE = "plugin_handler"
""" The plugin handler value """

class MainServiceSmtpStreamHandler:
    """
    The main service smtp stream handler class.
    """

    main_service_smtp_stream_handler_plugin = None
    """ The main service smtp stream handler plugin """

    def __init__(self, main_service_smtp_stream_handler_plugin):
        """
        Constructor of the class.

        @type main_service_smtp_console_handler_plugin: MainServiceSmtpStreamHandlerPlugin
        @param main_service_smtp_stream_handler_plugin: The main service smtp stream handler plugin.
        """

        self.main_service_smtp_stream_handler_plugin = main_service_smtp_stream_handler_plugin

    def get_handler_name(self):
        return HANDLER_NAME

    def handle_request(self, request):
        # retrieves the current session
        session = request.get_session()

        # in case the data transmission mode is active
        if session.get_data_transmission():
            if "authentication" in session.get_properties() and session.get_properties()["authentication"]:
                auth_value = request.get_message()

                # sets the request response code
                request.set_response_code(235)

                # sets the request response message
                request.set_response_message("2.7.0 Authentication successful")
            else:
                # sets the data transmission mode to false
                session.set_data_transmission(False)

                # sets the request response code
                request.set_response_code(250)

                # sets the request response message
                request.set_response_message("OK: message queued for delivery")

        # retrieves the command
        command = request.get_command()

        # retrieves the arguments
        arguments = request.get_arguments()

        if command == "helo":
            # retrieves the client hostname
            client_hostname = arguments[0]

            # sets the request response code
            request.set_response_code(250)

            # sets the request response message
            request.set_response_message("Hello pleased to meet you")

            # sets the client hostname
            session.set_client_hostname(client_hostname)

        elif command == "ehlo":
            # sets the request response code
            request.set_response_code(250)

            # este ja faz parte das extensoes SE CALHAR DEVE SER METIDO A PARTE (TLX..... ver isso) !!!!
            request.set_response_messages(["Hello pleased to meet you", "AUTH PLAIN"])

            session.set_extensions_active(True)

            session.set_client_hostname(arguments[0])

        elif command == "mail":
            sub_command, value = arguments[0].split(":")

            sub_command = sub_command.lower()

            if sub_command == "from":
                # sets the request response code
                request.set_response_code(250)

                # sets the request response message
                request.set_response_message("Sender OK")

        elif command == "rcpt":
            sub_command, value = arguments[0].split(":")

            sub_command = sub_command.lower()

            if sub_command == "to":
                # sets the request response code
                request.set_response_code(250)

                # sets the request response message
                request.set_response_message("Accepted")

        elif command == "data":
            # sets the request response code
            request.set_response_code(354)

            # sets the request response message
            request.set_response_message("End data with \".\"")

            # sets the data transmission mode to true
            session.set_data_transmission(True)

        # este ja faz parte das extensoes SE CALHAR DEVE SER METIDO A PARTE (TLX..... ver isso) !!!!
        elif command == "auth":
            # retrieves the authentication type
            authentication_type = arguments[0]

            # sets the authentication type in the session properties
            session.get_properties()["authentication_type"] = authentication_type

            # in case the number of arguments is bigger than one
            if arguments > 1:
                # retrieves the authentication token
                authentication_token = arguments[1]

                import base64

                # decodes the authentication token
                authentication_token_decoded = base64.b64decode(authentication_token)

                invalid, username, password = authentication_token_decoded.split("\x00")

                print "trying to login with: " + username + ", " + password

                # se falhar 535 5.7.8  Authentication credentials invalid
                # se nao tiver o mecanismo certo 534 5.7.9  Authentication mechanism is too weak

                # sets the request response code
                request.set_response_code(235)

                # sets the request response message
                request.set_response_message("2.7.0 Authentication successful")
            else:
                # sets the data transmission mode to true
                session.set_data_transmission(True)

                # sets the authentication property
                session.get_properties()["authentication"] = True

                # sets the request response code
                request.set_response_code(334)

                # sets the request response message
                request.set_response_message("Authentication started")

        elif command == "quit":
            # sets the request response code
            request.set_response_code(221)

            # sets the request response message
            request.set_response_message("Bye")

            # sets the session as closed
            session.set_closed(True)

    def handle_initial_request(self, request):
        # sets the request response code
        request.set_response_code(220)

        # sets the request response message
        request.set_response_message("localhost ESMTP Colony Smtp Server")

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
