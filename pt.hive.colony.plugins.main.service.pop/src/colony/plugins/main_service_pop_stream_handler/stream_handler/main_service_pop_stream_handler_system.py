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

import os
import time
import base64

import main_service_pop_stream_handler_exceptions

HANDLER_NAME = "stream"
""" The handler name """

AUTHENTICATION_VALUE = "authentication"
""" The authentication value """

AUTHENTICATION_TYPE_VALUE = "authentication_type"
""" The authentication type value """

DEFAULT_AUTHENTICATION_TYPE = "plain"
""" The default authentication type """

MESSAGE = """Return-Path: <joamag@gmail.com>
Received: from [93.108.84.220] (220.84.108.93.rev.vodafone.pt [93.108.84.220])
        by mx.google.com with ESMTPS id 13sm5671510fad.7.2010.05.07.01.38.17
        (version=TLSv1/SSLv3 cipher=RC4-MD5);
        Fri, 07 May 2010 01:38:20 -0700 (PDT)
Message-Id: <722CD92D-15EB-4F19-8AF5-88B5B88908AE@gmail.com>
From: =?utf-8?Q?Jo=C3=A3o_Magalh=C3=A3es?= <joamag@gmail.com>
To: me <joamag@gmail.com>
Content-Type: text/plain;
    charset=us-ascii;
    format=flowed;
    delsp=yes
Content-Transfer-Encoding: 7bit
X-Mailer: iPhone Mail (7E18)
Mime-Version: 1.0 (iPhone Mail 7E18)
Subject: Elaborar tops e restaurantes na moda
Date: Fri, 7 May 2010 09:38:03 +0100

Ter tb a possibilidade de focar no prato saber informacoes e depois
saber quem o serve

Sent from my iPhone"""

class MainServicePopStreamHandler:
    """
    The main service pop stream handler class.
    """

    main_service_pop_stream_handler_plugin = None
    """ The main service pop stream handler plugin """

    def __init__(self, main_service_pop_stream_handler_plugin):
        """
        Constructor of the class.

        @type main_service_pop_console_handler_plugin: MainServicePopStreamHandlerPlugin
        @param main_service_pop_stream_handler_plugin: The main service pop stream handler plugin.
        """

        self.main_service_pop_stream_handler_plugin = main_service_pop_stream_handler_plugin

    def get_handler_name(self):
        return HANDLER_NAME

    def handle_request(self, request):
        # retrieves the current session
        session = request.get_session()

        # retrieves the command
        command = request.get_command()

        # retrieves the arguments
        arguments = request.get_arguments()

        # creates the command method name
        command_method_name = "process_" + command

        # in case the command method is not defined in the current object
        if not hasattr(self, command_method_name):
            # raises the invalid pop command exception
            raise main_service_pop_stream_handler_exceptions.InvalidPopCommand("command method not found: " + command)

        # retrieves the command method from the object
        command_method = getattr(self, command_method_name)

        # calls the command method with the request, session
        # and command arguments
        command_method(request, session, arguments)

    def process_apop(self, request, session, arguments):
        """
        Processes the apop command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the helo arguments
        self.assert_arguments(arguments, 1)

        # retrieves the client hostname
        client_hostname = arguments[0]

        # sets the request response code
        request.set_response_code("+OK")

        # sets the request response message
        request.set_response_message("Hello pleased to meet you")

        # sets the client hostname
        session.set_client_hostname(client_hostname)

    def process_capa(self, request, session, arguments):
        """
        Processes the capa command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the ehlo arguments
        self.assert_arguments(arguments, 0)

        # sets the request response code
        request.set_response_code("+OK")

        # sets the response messages in the request
        request.set_response_messages(["capability list follows", "top", "user", "resp-codes", "uidl", "starttls"])

        # sets the extensions as active
        session.set_extensions_active(True)

    def process_starttls(self, request, session, arguments):
        """
        Processes the starttls command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # sets the upgrade flag
        session.set_upgrade(True)

        # sets the request response code
        request.set_response_code(220)

        # sets the response message in the request
        request.set_response_message("Ready to start TLS")

    def process_user(self, request, session, arguments):
        """
        Processes the user command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the user arguments
        self.assert_arguments(arguments, 1)

        # retrieves the user argument
        user_argument = arguments[0]

        # sets the current user
        session.set_current_user(user_argument)

        # sets the request response code
        request.set_response_code("+OK")

        # sets the request response message
        request.set_response_message("user valid")

    def process_pass(self, request, session, arguments):
        """
        Processes the pass command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the pass arguments
        self.assert_arguments(arguments, 1)

        # retrieves the password argument
        password_argument = arguments[0]

        # sets the password
        session.set_current_password(password_argument)

        # retrieves the session properties
        session_properties = session.get_properties()

        # retrieves the authentication type from the session properties
        authentication_type = session_properties.get(AUTHENTICATION_TYPE_VALUE, DEFAULT_AUTHENTICATION_TYPE)

        # creates the authentication method name
        authentication_method_name = "process_authentication_" + authentication_type

        # in case the authentication method is not defined in the current object
        if not hasattr(self, authentication_method_name):
            # raises the invalid pop command exception
            raise main_service_pop_stream_handler_exceptions.InvalidPopCommand("authentication method not found: " + authentication_type)

        # retrieves the authentication method from the object
        authentication_method = getattr(self, authentication_method_name)

        # calls the authentication method with the request, session
        # and authentication arguments
        authentication_method(request, session, [])

    def process_stat(self, request, session, arguments):
        """
        Processes the stat command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the stat arguments
        self.assert_arguments(arguments, 0)

        # sets the request response code
        request.set_response_code("+OK")

        message_count = 1

        octets_count = len(MESSAGE)

        # sets the request response message
        request.set_response_message("%i %i" % (message_count, octets_count))

    def process_list(self, request, session, arguments):
        """
        Processes the list command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the list arguments
        self.assert_arguments(arguments, 0)

        response_messages = []

        message_count = 1

        octets_count = len(MESSAGE)

        response_messages.append("%i messages (%i octets)" % (message_count, octets_count))

        message_description_list = ((1, len(MESSAGE)),)

        for message_description in message_description_list:
            message_id, message_size = message_description

            message = "%i %i" % (message_id, message_size)

            response_messages.append(message)

        # sets the request response code
        request.set_response_code("+OK")

        request.set_response_messages(response_messages)

    def process_retr(self, request, session, arguments):
        """
        Processes the retr command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the retr arguments
        self.assert_arguments(arguments, 1)

        # retrieves the message id argument
        message_id = arguments[0]

        response_messages = []

        octets_count = len(MESSAGE)

        # sets the request response code
        request.set_response_code("+OK")

        response_messages.append("%i octets" % octets_count)

        buffer = MESSAGE

        response_messages.append(buffer)

        request.set_response_messages(response_messages)

    def process_dele(self, request, session, arguments):
        """
        Processes the dele command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # sets the request response code
        request.set_response_code("-ERR")

        # sets the request response message
        request.set_response_message("not implemented")

    def process_uidl(self, request, session, arguments):
        """
        Processes the uidl command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the retr arguments
        self.assert_arguments(arguments, 0, 1)

        arguments_length = len(arguments)

        message_count = 1

        if arguments_length > 0:
            # retrieves the message id argument
            message_id = arguments[0]

            message_uid = "ABDD"

            request.set_response_code("+OK")

            request.set_response_message("%i %s" % (message_id, message_uid))
        else:
            response_messages = []

            response_messages.append("%i messages" % message_count)

            for index in range(message_count):
                message_id = index + 1

                message_uid = "ABDD"

                message = "%i %s" % (message_id, message_uid)

                response_messages.append(message)

            request.set_response_code("+OK")

            request.set_response_messages(response_messages)

    def process_auth(self, request, session, arguments):
        """
        Processes the auth command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # sets the request response code
        request.set_response_code("-ERR")

        # sets the request response message
        request.set_response_message("auth not supported")

    def process_quit(self, request, session, arguments):
        """
        Processes the quit command.

        @type request: PopRequest
        @param request: The pop request to be processed.
        @type session: PopSession
        @param session: The current used pop session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # sets the request response code
        request.set_response_code("+OK")

        # sets the request response message
        request.set_response_message("signing off")

        # sets the session as closed
        session.set_closed(True)

    def handle_initial_request(self, request):
        # retrieves the current time
        current_time = time.time()

        # retrieves the pid
        pid = os.getpid()

        # creates the timestamp string base on the pid and current time
        timestamp_string = "<" + str(pid) + "." + str(current_time) + "@localhost>"

        # sets the request response code
        request.set_response_code("+OK")

        # sets the request response message
        request.set_response_message("pop3 server ready " + timestamp_string)

    def process_authentication_plain(self, request, session, arguments):
        # retrieves the current user (as the username)
        username = session.get_current_user()

        # retrieves the current password
        password = session.get_current_password()

        # tries to authenticate with the session mechanism
        authentication_result = session.authenticate(username, password)

        # in case the authentication was successful
        if authentication_result:
            # sets the request response code
            request.set_response_code("+OK")

            # sets the request response message
            request.set_response_message("authentication successful")
        # in case the authentication was not successful
        else:
            # sets the request response code
            request.set_response_code("-ERR")

            # sets the request response message
            request.set_response_message("authentication credentials invalid")

    def create_write(self, request):
        def write(text, new_line = True):
            # replaces the newlines to newlines with carriage return
            raw_text = text.replace("\n", "\r\n")

            # in case a newline is required
            if new_line:
                request.write(raw_text + "\r\n")
            # in case no newline is required
            else:
                request.write(raw_text)

        # returns the write method
        return write

    def assert_arguments(self, arguments, minimum_number = 0, maximum_number = None):
        """
        Asserts that the given arguments list respects the given
        conditions of minimum and maximum number of arguments.

        @type arguments: List
        @param arguments: The list of arguments to be verified.
        @type minimum_number: int
        @param minimum_number: The minimum number that the list must contain.
        @type maximum_number: int
        @param maximum_number: The maximum number that the list must contain.
        """

        # in case the maximum number of arguments
        # is not defined the minimum value is used
        if maximum_number == None:
            # sets the maximum number of arguments with
            # the same values as the minimum
            maximum_number = minimum_number

        # retrieves the arguments length
        arguments_length = len(arguments)

        # in case the length of the arguments list is invalid (lower
        # than the minimum or greater than the maximum)
        if arguments_length < minimum_number or (arguments_length > maximum_number and maximum_number >= 0):
            # raises the invalid pop command exception
            raise main_service_pop_stream_handler_exceptions.InvalidPopCommand("invalid number of arguments: " + str(arguments_length))
