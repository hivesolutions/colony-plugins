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

import main_service_pop_stream_handler_exceptions

HANDLER_NAME = "stream"
""" The handler name """

VALID_VALUE = "valid"
""" The valid value """

AUTHENTICATION_TYPE_VALUE = "authentication_type"
""" The authentication type value """

DEFAULT_AUTHENTICATION_TYPE = "plain"
""" The default authentication type """

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
        self.assert_arguments(arguments, 2)

        # retrieves the user argument
        user_argument = arguments[0]

        # sets the current user
        session.set_current_user(user_argument)

        # sets the request response code
        request.set_response_code("+OK")

        # sets the request response message
        request.set_response_message("Hello again %s you're authenticated" % user_argument)

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

        # asserts the capa arguments
        self.assert_arguments(arguments, 0)

        # sets the request response code
        request.set_response_code("+OK")

        # sets the response messages in the request
        request.set_response_messages(["capability list follows", "top", "user", "resp-codes", "uidl", "stls"])

        # sets the extensions as active
        session.set_extensions_active(True)

    def process_stls(self, request, session, arguments):
        """
        Processes the stls command.

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
        request.set_response_code("+OK")

        # sets the response message in the request
        request.set_response_message("ready to start tls")

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

        # handles the session
        session.handle()

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

        # retrieves the current mailbox
        mailbox = session.get_mailbox()

        # retrieves the messages
        messages_count = mailbox.get_messages_count()

        # retrieves the octets count
        octets_count = mailbox.get_messages_size()

        # sets the request response code
        request.set_response_code("+OK")

        # sets the request response message
        request.set_response_message("%i %i" % (messages_count, octets_count))

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

        # creates the response messages list
        response_messages = []

        # retrieves the current mailbox
        mailbox = session.get_mailbox_messages()

        # retrieves the messages
        messages_count = mailbox.get_messages_count()

        # retrieves the octets count
        octets_count = mailbox.get_messages_size()

        # adds the initial line message to the response messages
        response_messages.append("%i messages (%i octets)" % (messages_count, octets_count))

        # retrieves the mailbox messages
        mailbox_messages = mailbox.get_messages()

        # starts the index counter
        index = 1

        # iterates over all the messages in the mailbox
        for message in mailbox_messages:
            # retrieves the message contents size
            message_contents_size = message.get_contents_size()

            # creates the response message
            message = "%i %i" % (index, message_contents_size)

            # adds the (response) message to the list
            # of response messages
            response_messages.append(message)

            # increments the index counter
            index += 1

        # generates the message id uid map
        self._generate_message_id_uid_map(session, mailbox)

        # sets the request response code
        request.set_response_code("+OK")

        # sets the request response messages
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
        message_id = int(arguments[0])

        # retrieves the message id uid map
        message_id_uid_map = self.get_message_id_uid_map(session)

        # creates the response messages list
        response_messages = []

        # retrieves the message uid from the message id uid map
        message_uid = message_id_uid_map[message_id]

        # retrieves the message for the given uid
        message = session.get_message(message_uid)

        # retrieves the message contents
        message_contents = message.get_contents()

        # retrieves the message contents size
        message_contents_size = message_contents.get_contents_size()

        # retrieves the message contents data
        message_contents_data = message_contents.get_contents_data()

        # adds the initial line to the response messages
        response_messages.append("%i octets" % message_contents_size)

        # adds the message contents data to the response messages
        response_messages.append(message_contents_data)

        # sets the request response code
        request.set_response_code("+OK")

        # sets the request response messages
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

        # asserts the retr arguments
        self.assert_arguments(arguments, 1)

        # retrieves the message id uid map
        message_id_uid_map = self.get_message_id_uid_map(session)

        # retrieves the message id argument
        message_id = int(arguments[0])

        # retrieves the message uid from the message id uid map
        message_uid = message_id_uid_map[message_id]

        # removes the message for the given uid
        session.remove_message(message_uid)

        # sets the request response code
        request.set_response_code("+OK")

        # sets the request response message
        request.set_response_message("message %i removed" % message_id)

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

        # retrieves the arguments length
        arguments_length = len(arguments)

        # retrieves the message id uid map
        message_id_uid_map = self.get_message_id_uid_map(session)

        if arguments_length > 0:
            # retrieves the message id argument
            message_id = int(arguments[0])

            # retrieves the message uid associated with the message id
            message_uid = message_id_uid_map[message_id]

            # sets the request response code
            request.set_response_code("+OK")

            # sets the request response message
            request.set_response_message("%i %s" % (message_id, message_uid))
        else:
            # retrieves the current mailbox
            mailbox = session.get_mailbox()

            # retrieves the messages
            messages_count = mailbox.get_messages_count()

            # creates the response messages list
            response_messages = []

            # adds the initial response message
            response_messages.append("%i messages" % messages_count)

            # iterates over the ranges of messages count
            for index in range(messages_count):
                # retrieves the message id
                message_id = index + 1

                # retrieves the message uid from the message id uid map
                message_uid = message_id_uid_map[message_id]

                # creates the message associating the message id to the
                # message uid
                message = "%i %s" % (message_id, message_uid)

                # adds the message to the list of response messages
                response_messages.append(message)

            # sets the request response code
            request.set_response_code("+OK")

            # sets the request response messages
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

        # retrieves the authentication result valid
        authentication_result_valid = authentication_result.get(VALID_VALUE, False)

        # in case the authentication was successful
        if authentication_result_valid:
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

    def get_message_id_uid_map(self, session):
        """
        Retrieves the message id uid map for the given session.

        @type session: PopSession
        @param session: The session to retrieve the map.
        @rtype: Dictionary
        @return: The message id uid map for the given session.
        """

        # retrieves the message id uid map generated
        message_id_uid_map_generated = session.get_message_id_uid_map_generated()

        # in case the message id uid map as not been generated
        if not message_id_uid_map_generated:
            # generates the message id uid map
            self._generate_message_id_uid_map(session)

        # retrieves the message id uid map
        message_id_uid_map = session.get_message_id_uid_map()

        # returns the message id uid map
        return message_id_uid_map

    def _generate_message_id_uid_map(self, session, mailbox = None):
        """
        Generates the message id uid map for the given session, and if given
        using the given mailbox structure.

        @type session: PopSession
        @param session: The session to be used in the map generation.
        @type mailbox: Mailbox
        @param mailbox: The mailbox to be used in the map generation.
        """

        # in case the mailbox is not defined
        if not mailbox:
            # retrieves the current mailbox
            mailbox = session.get_mailbox_messages()

        # starts the message id uid map
        session.message_id_uid_map = {}

        # retrieves the mailbox messages
        mailbox_messages = mailbox.get_messages()

        # starts the index counter
        index = 1

        # iterates over all the messages in the mailbox
        for message in mailbox_messages:
            # retrieves the message uid
            message_uid = message.get_uid()

            # sets the message uid in the message id uid map
            session.message_id_uid_map[index] = message_uid

            # increments the index counter
            index += 1

        # sets the message id uid map generated flag
        session.set_message_id_uid_map_generated(True)
