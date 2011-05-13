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

import base64

import main_service_smtp_stream_handler_exceptions

HANDLER_NAME = "stream"
""" The handler name """

VALID_VALUE = "valid"
""" The valid value """

AUTHENTICATION_VALUE = "authentication"
""" The authentication value """

AUTHENTICATION_TYPE_VALUE = "authentication_type"
""" The authentication type value """

USERNAME_VALUE = "username"
""" The username value """

AUTHENTICATION_MESSAGE_INDEX_VALUE = "authentication_message_index"
""" The authentication message index value """

USERNAME_BASE64_VALUE = "VXNlcm5hbWU6"
""" The username base64 value """

PASSWORD_BASE64_VALUE = "UGFzc3dvcmQ6"
""" The password base64 value """

SEPARATOR_TOKEN_VALUE = "\x00"
""" The separator token value """

END_TOKEN_DATA_VALUE = "\r\n.\r\n"
""" The end token data value """

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

        # in case there was data transmission processed
        if self.process_data_transmission(request, session):
            # returns immediately
            return

        # retrieves the command
        command = request.get_command()

        # retrieves the arguments
        arguments = request.get_arguments()

        # creates the command method name
        command_method_name = "process_" + command

        # in case the command method is not defined in the current object
        if not hasattr(self, command_method_name):
            # raises the invalid smtp command exception
            raise main_service_smtp_stream_handler_exceptions.InvalidSmtpCommand("command method not found: " + command)

        # retrieves the command method from the object
        command_method = getattr(self, command_method_name)

        # calls the command method with the request, session
        # and command arguments
        command_method(request, session, arguments)

    def process_data_transmission(self, request, session):
        """
        Processes a data transmission "command".

        @type request: SmtpRequest
        @param request: The smtp request to be processed.
        @type session: SmtpSession
        @param session: The current used smtp session.
        """

        # in case the data transmission mode is active
        if not session.get_data_transmission():
            # returns invalid (no data transmission to be processed)
            return False

        # retrieves the session properties
        session_properties = session.get_properties()

        # retrieves the authentication value
        authentication_value = session_properties.get(AUTHENTICATION_VALUE, None)

        # in case there is a valid authentication value defined
        # the data is the authentication token
        if authentication_value:
            # retrieves the authentication type from the session properties
            authentication_type = session_properties[AUTHENTICATION_TYPE_VALUE]

            # creates the authentication method name
            authentication_method_name = "process_authentication_" + authentication_type

            # in case the authentication method is not defined in the current object
            if not hasattr(self, authentication_method_name):
                # raises the invalid smtp command exception
                raise main_service_smtp_stream_handler_exceptions.InvalidSmtpCommand("authentication method not found: " + authentication_type)

            # retrieves the authentication method from the object
            authentication_method = getattr(self, authentication_method_name)

            # calls the authentication method with the request, session
            # and authentication arguments
            authentication_method(request, session, [])
        # the data is the message contents
        else:
            # retrieves the current message
            message = session.get_current_message()

            # retrieves the contents from the request
            contents = request.get_message()

            # "de-stuffes" the contents of the message
            contents_destuffed = contents.replace("\r\n..", "\r\n.")

            # sets the contents in the message
            message.set_contents(contents_destuffed)

            # resets the end token to the default value
            session.reset_end_token()

            # sets the data transmission mode to false
            session.set_data_transmission(False)

            # handles the session
            session.handle()

            # sets the request response code
            request.set_response_code(250)

            # sets the request response message
            request.set_response_message("OK: message queued for delivery")

        # returns valid (data transmission processed)
        return True

    def process_helo(self, request, session, arguments):
        """
        Processes the helo command.

        @type request: SmtpRequest
        @param request: The smtp request to be processed.
        @type session: SmtpSession
        @param session: The current used smtp session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the helo arguments
        self.assert_arguments(arguments, 1)

        # retrieves the client hostname
        client_hostname = arguments[0]

        # sets the request response code
        request.set_response_code(250)

        # sets the request response message
        request.set_response_message("Hello pleased to meet you")

        # sets the client hostname
        session.set_client_hostname(client_hostname)

    def process_ehlo(self, request, session, arguments):
        """
        Processes the ehlo command.

        @type request: SmtpRequest
        @param request: The smtp request to be processed.
        @type session: SmtpSession
        @param session: The current used smtp session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the ehlo arguments
        self.assert_arguments(arguments, 1)

        # retrieves the client hostname
        client_hostname = arguments[0]

        # sets the request response code
        request.set_response_code(250)

        # sets the response messages in the request
        request.set_response_messages(["Hello pleased to meet you", "8bitmime", "auth plain", "auth login", "starttls"])

        # sets the extensions as active
        session.set_extensions_active(True)

        # sets the client hostname
        session.set_client_hostname(client_hostname)

    def process_starttls(self, request, session, arguments):
        """
        Processes the starttls command.

        @type request: SmtpRequest
        @param request: The smtp request to be processed.
        @type session: SmtpSession
        @param session: The current used smtp session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # sets the upgrade flag
        session.set_upgrade(True)

        # sets the request response code
        request.set_response_code(220)

        # sets the response message in the request
        request.set_response_message("Ready to start TLS")

    def process_mail(self, request, session, arguments):
        """
        Processes the mail command.

        @type request: SmtpRequest
        @param request: The smtp request to be processed.
        @type session: SmtpSession
        @param session: The current used smtp session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the mail arguments
        self.assert_arguments(arguments, 1)

        # retrieves the from argument
        from_argument = arguments[0]

        # retrieves the from command and the from value
        from_command, from_value = from_argument.split(":")

        # normalizes the from command
        from_command = from_command.lower()

        # in case the from command is not valid
        if not from_command == "from":
            # raises the invalid smtp command
            raise main_service_smtp_stream_handler_exceptions.InvalidSmtpCommand("malformed mail command")

        # generates a new message for the session
        session.generate_message()

        # retrieves the current message
        message = session.get_current_message()

        # retrieves the sender from the from value
        sender = from_value.strip("<>")

        # sets the sender in the message
        message.set_sender(sender)

        # sets the request response code
        request.set_response_code(250)

        # sets the request response message
        request.set_response_message("Sender OK")

    def process_rcpt(self, request, session, arguments):
        """
        Processes the rcpt command.

        @type request: SmtpRequest
        @param request: The smtp request to be processed.
        @type session: SmtpSession
        @param session: The current used smtp session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the rcpt arguments
        self.assert_arguments(arguments, 1)

        # retrieves the to argument
        to_argument = arguments[0]

        # retrieves the to command and the from value
        to_command, to_value = to_argument.split(":")

        # normalizes the to command
        to_command = to_command.lower()

        # in case the to command is not valid
        if not to_command == "to":
            # raises the invalid smtp command
            raise main_service_smtp_stream_handler_exceptions.InvalidSmtpCommand("malformed rcpt command")

        # retrieves the current message
        message = session.get_current_message()

        # retrieves the sender from the to value
        recipient = to_value.strip("<>")

        # adds the recipient to the message
        message.add_recipient(recipient)

        # sets the request response code
        request.set_response_code(250)

        # sets the request response message
        request.set_response_message("Accepted")

    def process_data(self, request, session, arguments):
        """
        Processes the data command.

        @type request: SmtpRequest
        @param request: The smtp request to be processed.
        @type session: SmtpSession
        @param session: The current used smtp session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # sets the request response code
        request.set_response_code(354)

        # sets the request response message
        request.set_response_message("End data with \\r\\n.\\r\\n")

        # sets the data value end token
        session.set_end_token(END_TOKEN_DATA_VALUE)

        # sets the data transmission mode to true
        session.set_data_transmission(True)

    def process_auth(self, request, session, arguments):
        """
        Processes the auth command.

        @type request: SmtpRequest
        @param request: The smtp request to be processed.
        @type session: SmtpSession
        @param session: The current used smtp session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

        # asserts the auth arguments
        self.assert_arguments(arguments, 1, -1)

        # retrieves the authentication type
        authentication_type = arguments[0]

        # "lowercases" the authentication type
        authentication_type = authentication_type.lower()

        # prints an info message
        self.main_service_smtp_stream_handler_plugin.info("Trying to login using authentication method '%s'" % authentication_type)

        # retrieves the session properties
        session_properties = session.get_properties()

        # sets the authentication type in the session properties
        session_properties[AUTHENTICATION_TYPE_VALUE] = authentication_type

        # creates the authentication method name
        authentication_method_name = "process_authentication_" + authentication_type

        # in case the authentication method is not defined in the current object
        if not hasattr(self, authentication_method_name):
            # raises the invalid smtp command exception
            raise main_service_smtp_stream_handler_exceptions.InvalidSmtpCommand("authentication method not found: " + authentication_type)

        # retrieves the authentication method from the object
        authentication_method = getattr(self, authentication_method_name)

        # calls the authentication method with the request, session
        # and authentication arguments
        authentication_method(request, session, arguments)

    def process_quit(self, request, session, arguments):
        """
        Processes the quit command.

        @type request: SmtpRequest
        @param request: The smtp request to be processed.
        @type session: SmtpSession
        @param session: The current used smtp session.
        @type arguments: List
        @param arguments: The list of arguments for the request.
        """

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

    def process_authentication_plain(self, request, session, arguments):
        # asserts the mail arguments
        self.assert_arguments(arguments, 2, -1)

        # retrieves the authentication token
        authentication_token = arguments[1]

        # decodes the authentication token
        authentication_token_decoded = base64.b64decode(authentication_token)

        # splits the authentication token retrieving the username and password
        username, password = authentication_token_decoded.strip(SEPARATOR_TOKEN_VALUE).split(SEPARATOR_TOKEN_VALUE)

        # tries to authenticate with the session mechanism
        authentication_result = session.authenticate(username, password)

        # retrieves the authentication result valid
        authentication_result_valid = authentication_result.get(VALID_VALUE, False)

        # in case the authentication was successful
        if authentication_result_valid:
            # sets the request response code
            request.set_response_code(235)

            # sets the request response message
            request.set_response_message("2.7.0 Authentication successful")
        # in case the authentication was not successful
        else:
            # sets the request response code
            request.set_response_code(535)

            # sets the request response message
            request.set_response_message("5.7.8 Authentication credentials invalid")

    def process_authentication_login(self, request, session, arguments):
        # asserts the mail arguments
        self.assert_arguments(arguments, 0, -1)

        # retrieves the session properties
        session_properties = session.get_properties()

        # retrieves the authentication message index
        authentication_message_index = session_properties.get(AUTHENTICATION_MESSAGE_INDEX_VALUE, 0)

        # in case it's the first communication message
        if authentication_message_index == 0:
            # sets the authentication property
            session_properties[AUTHENTICATION_VALUE] = True

            # increments the authentication message index and set the value
            # in the session properties map
            session_properties[AUTHENTICATION_MESSAGE_INDEX_VALUE] = authentication_message_index + 1

            # sets the data transmission mode to true
            session.set_data_transmission(True)

            # sets the request response code
            request.set_response_code(334)

            # sets the request response message
            request.set_response_message(USERNAME_BASE64_VALUE)
        elif authentication_message_index == 1:
            # retrieves the contents from the request
            contents = request.get_message()

            # strips the contents
            contents = contents.strip()

            # decodes the contents using base64 and sets them as the username
            # in the session properties
            session_properties[USERNAME_VALUE] = base64.b64decode(contents)

            # increments the authentication message index and set the value
            # in the session properties map
            session_properties[AUTHENTICATION_MESSAGE_INDEX_VALUE] = authentication_message_index + 1

            # sets the request response code
            request.set_response_code(334)

            # sets the request response message
            request.set_response_message(PASSWORD_BASE64_VALUE)
        elif authentication_message_index == 2:
            # retrieves the username from the session properties
            username = session_properties[USERNAME_VALUE]

            # retrieves the contents from the request
            contents = request.get_message()

            # strips the contents
            contents = contents.strip()

            # decodes the contents using base64 and sets them in the password variable
            password = base64.b64decode(contents)

            # tries to authenticate with the session mechanism
            authentication_result = session.authenticate(username, password)

            # in case the authentication was successful
            if authentication_result:
                # sets the request response code
                request.set_response_code(235)

                # sets the request response message
                request.set_response_message("2.7.0 Authentication successful")
            # in case the authentication was not successful
            else:
                # sets the request response code
                request.set_response_code(535)

                # sets the request response message
                request.set_response_message("5.7.8 Authentication credentials invalid")

            # sets the data transmission mode to true
            session.set_data_transmission(False)

            # deletes the authentication session properties
            del session_properties[AUTHENTICATION_MESSAGE_INDEX_VALUE]
            del session_properties[AUTHENTICATION_VALUE]
            del session_properties[USERNAME_VALUE]
        else:
            # raises the invalid smtp command exception
            raise main_service_smtp_stream_handler_exceptions.InvalidSmtpCommand("invalid authentication index")

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
            # raises the invalid smtp command exception
            raise main_service_smtp_stream_handler_exceptions.InvalidSmtpCommand("invalid number of arguments: " + str(arguments_length))
