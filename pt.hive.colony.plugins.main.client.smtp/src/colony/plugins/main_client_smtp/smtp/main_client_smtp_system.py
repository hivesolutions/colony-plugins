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

import socket
import select
import base64

import colony.libs.string_buffer_util

import main_client_smtp_exceptions

DEFAULT_PORT = 25
""" The default port """

DEFAULT_SOCKET_NAME = "normal"
""" The default socket name """

DEFAULT_AUTHENTICATION_METHOD = "plain"
""" The default authentication method """

RESPONSE_TIMEOUT = 60
""" The response timeout """

CHUNK_SIZE = 4096
""" The chunk size """

END_TOKEN_VALUE = "\r\n"
""" The end token value """

AUTHENTICATION_METHOD_VALUE = "authentication_method"
""" The authentication method value """

class MainClientSmtp:
    """
    The main client smtp class.
    """

    main_client_smtp_plugin = None
    """ The main client smtp plugin """

    def __init__(self, main_client_smtp_plugin):
        """
        Constructor of the class.

        @type main_client_smtp_plugin: MainClientSmtp
        @param main_client_smtp_plugin: The main client smtp plugin.
        """

        self.main_client_smtp_plugin = main_client_smtp_plugin

    def create_client(self, parameters):
        """
        Creates a client object for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to be used in creating
        the client object.
        @rtype: SmtpClient
        @return: The created client object.
        """

        # creates the smtp client
        smtp_client = SmtpClient(self)

        # returns the smtp client
        return smtp_client

    def create_request(self, parameters):
        pass

class SmtpClient:
    """
    The smtp client class, representing
    a client connection in the smtp protocol.
    """

    main_client_smtp = None
    """ The main client smtp object """

    def __init__(self, main_client_smtp):
        """
        Constructor of the class.

        @type main_client_smtp: MainClientSmtp
        @param main_client_smtp: The main client smtp object.
        @type protocol_version: String
        @param protocol_version: The version of the smtp protocol to
        be used.
        @type content_type_charset: String
        @param content_type_charset: The charset to be used by the content.
        """

        self.main_client_smtp = main_client_smtp

    def send_mail(self, host, port, sender, recipients_list, message, parameters = {}, socket_name = DEFAULT_SOCKET_NAME):
        # retrieves (generates a socket)
        self.smtp_connection = self._get_socket(socket_name)

        # connects to the socket
        self.smtp_connection.connect((host, port))

        # creates the session object
        session = SmtpSession()

        # runs the initial login
        self.login(session, parameters)

        # runs the ehlo command
        self.ehlo(session, parameters)

        # retrieves the use tls flag
        tls = parameters.get("tls", False)

        # in case the tls flag is active
        if tls:
            # tries to start tls
            self.starttls(session, parameters)

            # runs the ehlo command (again, because of tls)
            self.ehlo(session, parameters)

        # retrieves the verify user flag
        verify_user = parameters.get("verify_user", False)

        # in case the verify user flag is active
        if verify_user:
            # runs the vrfy command
            self.vrfy(session, parameters)

        # tries to retrieve the username from the parameters
        username = parameters.get("username", "")

        # in case a username is defined
        if username:
            # tries to retrieve the password from the parameters
            password = parameters.get("password", "")

            # runs the auth command (starting the authentication process)
            self.auth(session, username, password, parameters)

        # runs the main command (starting the mail sending)
        self.mail(session, sender, parameters)

        # runs the rcpt command
        self.rcpt(session, recipients_list, parameters)

        # runs the data command and sends the raw data (message)
        self.data(session, message, parameters)

        # runs the quit command
        self.quit(session, parameters)

    def send_request(self, command, message, session, parameters):
        """
        Sends the request for the given parameters.

        @type command: String
        @param command: The command to be sent.
        @type message: String
        @param message: The message to be sent.
        @type session: SmtpSession
        @param session: The current smtp session.
        @type parameters: Dictionary
        @param parameters: The parameters to the request.
        @rtype: SmtpRequest
        @return: The sent request for the given parameters..
        """

        # creates the smtp request
        request = SmtpRequest()

        # sets the session object in the request
        request.set_session(session)

        # sets the command in the request
        request.set_command(command)

        # sets the message in the request
        request.set_message(message)

        # retrieves the result value from the request
        result_value = request.get_result()

        # sends the result value
        self.smtp_connection.send(result_value)

        # returns the request
        return request

    def send_request_data(self, data, session, parameters):
        """
        Sends the data request for the given parameters.

        @type data: String
        @param data: The string containing the data to be sent.
        @type session: SmtpSession
        @param session: The current smtp session.
        @type parameters: Dictionary
        @param parameters: The parameters to the request.
        @rtype: SmtpRequest
        @return: The sent request for the given parameters..
        """

        # creates the smtp request
        request = SmtpRequest()

        # writes the data to the request
        request.write(data)

        # retrieves the result value from the request
        result_value = request.get_result()

        # sends the result value
        self.smtp_connection.send(result_value)

        # returns the request
        return request

    def retrieve_response(self, request, session, response_timeout = RESPONSE_TIMEOUT):
        """
        Retrieves the response from the sent request.

        @rtype: SmtpRequest
        @return: The request that originated the response.
        @type session: SmtpSession
        @param session: The current smtp session.
        @type response_timeout: int
        @param response_timeout: The timeout for the response retrieval.
        @rtype: SmtpResponse
        @return: The response from the sent request.
        """

        # creates the string buffer for the message
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates a response object
        response = SmtpResponse(request)

        # continuous loop
        while True:
            # retrieves the data
            data = self.retrieve_data(response_timeout)

            # in case no valid data was received
            if data == "":
                raise main_client_smtp_exceptions.SmtpInvalidDataException("empty data received")

            # writes the data to the string buffer
            message.write(data)

            # retrieves the message value from the string buffer
            message_value = message.get_value()

            # retrieves the message value length
            message_value_length = len(message_value)

            # finds the first end token value
            end_token_index = message_value.rfind(END_TOKEN_VALUE)

            # calculates the last end token index, using the message
            # value length as reference
            last_end_token_index = message_value_length - 2

            # in case the end token is found in the last position
            # of the message
            if end_token_index == last_end_token_index:
                # tries to find a previous value of the newline
                # in order to check if it is the "last newline"
                value = message_value.rfind(END_TOKEN_VALUE, 0, last_end_token_index)

                # in case no previous newline is found
                if value == -1:
                    # sets the base value as zero (string initial)
                    base_value = 0
                else:
                    # sets the base value as the index of the find
                    # plus two indexes (the length of the end token value)
                    base_value = value + 2

                # retrieves the comparison character (the character that
                # indicates if it is the final line)
                comparison_character = message_value[base_value + 3]

                # in case the comparison character is a dash (not the final line)
                if comparison_character == "-":
                    continue
                elif not comparison_character == " ":
                    raise main_client_smtp_exceptions.SmtpInvalidDataException("invalid comparison character")

                # retrieves the smtp message
                smtp_message = message_value[:end_token_index]

                # splits the smtp message in lines
                smtp_message_lines = smtp_message.split("\r\n")

                # retrieves the number of smtp message lines
                smtp_message_lines_length = len(smtp_message_lines)

                # starts the index counter
                index = 1

                # iterates over all the smtp message lines
                for smtp_message_line in smtp_message_lines:
                    # in case it's the last line
                    if index == smtp_message_lines_length:
                        # splits the smtp message line
                        smtp_message_line_splitted = smtp_message_line.split(" ", 1)

                        # retrieves the smtp code
                        smtp_code = int(smtp_message_line_splitted[0])

                        # retrieves the smtp message
                        smtp_message = smtp_message_line_splitted[1]

                        # sets the smtp code in the response
                        response.set_code(smtp_code)

                        # sets the smtp message in the response
                        response.set_message(smtp_message)

                        # adds the smtp message to the list of
                        # messages in response
                        response.add_message(smtp_message)
                    # in case it's not the last line
                    else:
                        # splits the smtp message line
                        smtp_message_line_splitted = smtp_message_line.split("-", 1)

                        # retrieves the smtp message
                        smtp_message = smtp_message_line_splitted[1]

                        # adds the smtp message to the list of
                        # messages in response
                        response.add_message(smtp_message)

                    # increments the index counter
                    index += 1

                # sets the session object in the response
                response.set_session(session)

                # returns the response
                return response

    def retrieve_data(self, response_timeout = RESPONSE_TIMEOUT, chunk_size = CHUNK_SIZE):
        try:
            # sets the connection to non blocking mode
            self.smtp_connection.setblocking(0)

            # runs the select in the smtp connection, with timeout
            selected_values = select.select([self.smtp_connection], [], [], response_timeout)

            # sets the connection to blocking mode
            self.smtp_connection.setblocking(1)
        except:
            raise main_client_smtp_exceptions.ResponseClosed("invalid socket")

        if selected_values == ([], [], []):
            self.smtp_connection.close()
            raise main_client_smtp_exceptions.ClientResponseTimeout("%is timeout" % response_timeout)
        try:
            # receives the data in chunks
            data = self.smtp_connection.recv(chunk_size)
        except:
            raise main_client_smtp_exceptions.ServerResponseTimeout("timeout")

        # returns the data
        return data

    def login(self, session, parameters = {}):
        # retrieves the initial response value
        response = self.retrieve_response(None, session)

        # checks the response for errors
        self._check_response_error(response, (220,), "problem establishing connection: ")

    def ehlo(self, session, parameters = {}):
        # sends the hello request
        request = self.send_request("ehlo", "mail.sender.com", session, parameters)

        # retrieves the response
        response = self.retrieve_response(request, session)

        # checks the response for errors
        self._check_response_error(response, (250,), "problem establishing connection: ")

    def starttls(self, session, parameters = {}):
        # sends the starttls request
        request = self.send_request("starttls", None, session, parameters)

        # retrieves the response
        response = self.retrieve_response(request, session)

        # checks the response for errors
        self._check_response_error(response, (220,), "problem starting tls: ")

        # upgrades the smtp connection to use ssl (tls)
        self.smtp_connection = self._upgrade_socket(self.smtp_connection, "ssl")

    def vrfy(self, session, parameters = {}):
        # retrieves the verification user
        verification_user = parameters.get("verification_user", None)

        # in case no verification user is defined
        if not verification_user:
            # raises an smtp runtime exception
            raise main_client_smtp_exceptions.SmtpRuntimeException("invalid verification user")

        # sends the verify request
        request = self.send_request("vrfy", verification_user, session, parameters)

        # retrieves the response
        response = self.retrieve_response(request, session)

        # checks the response for errors
        self._check_response_error(response, (250, 251, 252), "problem verifying the user: ")

    def auth(self, session, username, password, parameters = {}):
        # tries to retrieve the username from the parameters
        username = parameters.get("username", "")

        # tries to retrieve the password from the parameters
        password = parameters.get("password", "")

        # retrieves the authentication method
        authentication_method = parameters.get(AUTHENTICATION_METHOD_VALUE, DEFAULT_AUTHENTICATION_METHOD)

        # creates the authentication method name
        authentication_method_name = "authenticate_" + authentication_method

        # in case the authentication method is not defined in the current object
        if not hasattr(self, authentication_method_name):
            # raises the smtp runtime exception
            raise main_client_smtp_exceptions.SmtpRuntimeException("authentication method not found: " + authentication_method)

        # retrieves the authentication method from the object
        authentication_method = getattr(self, authentication_method_name)

        # calls the authentication method with the request, session
        # and authentication arguments
        authentication_method(session, parameters, username, password)

    def mail(self, session, sender, parameters = {}):
        # sends the mail request
        request = self.send_request("mail", "from:<" + sender + ">", session, parameters)

        # retrieves the response
        response = self.retrieve_response(request, session)

        # checks the response for errors
        self._check_response_error(response, (250,), "problem sending email: ")

    def rcpt(self, session, recipients_list, parameters = {}):
        # iterates over all the recipients in the recipients list
        for recipient in recipients_list:
            # sends the rcpt request
            request = self.send_request("rcpt", "to:<" + recipient + ">", session, parameters)

            # retrieves the response
            response = self.retrieve_response(request, session)

            # checks the response for errors
            self._check_response_error(response, (250,), "problem sending email: ")

    def data(self, session, data, parameters = {}):
        # sends the data request
        request = self.send_request("data", None, session, parameters)

        # retrieves the response
        response = self.retrieve_response(request, session)

        # checks the response for errors
        self._check_response_error(response, (250, 354), "problem sending email: ")

        # "stuffes" the data according to smtp specification
        data_stuffed = data.replace("\r\n.", "\r\n..")

        # sends the data in raw format
        request = self.send_request_data(data_stuffed + "\r\n.", session, parameters)

        # retrieves the response
        response = self.retrieve_response(request, session)

        # checks the response for errors
        self._check_response_error(response, (250,), "problem sending email data: ")

    def quit(self, session, parameters = {}):
        # sends the quit request
        request = self.send_request("quit", None, session, parameters)

        # retrieves the response
        response = self.retrieve_response(request, session)

        # checks the response for errors
        self._check_response_error(response, (221,), "problem sending email data: ")

    def authenticate_plain(self, session, parameters, username, password):
        # creates the authentication string for the username and password
        authentication_string = "\x00%s\x00%s\x00" % (username, password)

        # converts the authentication string to base64
        authentication_string_base64 = base64.b64encode(authentication_string)

        # sends the auth request
        request = self.send_request("auth", "plain " + authentication_string_base64, session, parameters)

        # retrieves the response
        response = self.retrieve_response(request, session)

        # checks the response for errors
        self._check_response_error(response, (235,), "problem in login authentication: ")

    def authenticate_login(self, session, parameters, username, password):
        # converts the username to base64
        username_base64 = base64.b64encode(username)

        # converts the password to base64
        password_base64 = base64.b64encode(password)

        # sends the auth request
        request = self.send_request("auth", "login", session, parameters)

        # retrieves the response
        response = self.retrieve_response(request, session)

        # checks the response for errors
        self._check_response_error(response, (334,), "problem initializing login: ")

        # sends the username data
        request = self.send_request_data(username_base64, session, parameters)

        # retrieves the response
        response = self.retrieve_response(request, session)

        # checks the response for errors
        self._check_response_error(response, (334,), "problem in username login: ")

        # sends the password data
        request = self.send_request_data(password_base64, session, parameters)

        # retrieves the response
        response = self.retrieve_response(request, session)

        # checks the response for errors
        self._check_response_error(response, (235,), "problem in login authentication: ")

    def _get_transaction_id(self):
        """
        Retrieves the transaction id, incrementing the
        current transaction id counter.

        @rtype: int
        @return: The newly generated transaction id.
        """

        # in case the limit is reached
        if self.current_transaction_id == 0xffff:
            # resets the current transaction id
            self.current_transaction_id = 0x0000

        # increments the current transaction id
        self.current_transaction_id += 1

        # returns the current transaction id
        return self.current_transaction_id

    def _check_response_error(self, response, accepted_codes, message = ""):
        """
        Checks the given response for errors, in case
        of errors using the given accepted codes list as the base
        value for checking. In case of error it raises an exception with the
        given message as prefix.

        @type response: SmtpResponse
        @param response: The response
        @type accepted_codes: List
        @param accepted_codes: The list of accepted codes.
        @type message: String
        @param message: The message to be used as base for the exception.
        """

        # retrieves the response code
        response_code = response.get_code()

        # in case the response code is not "accepted"
        if not response_code in accepted_codes:
            # raises the smtp response error
            raise main_client_smtp_exceptions.SmtpResponseError(message + str(response))

    def _get_socket(self, socket_name = "normal"):
        """
        Retrieves the socket for the given socket name
        using the socket provider plugins.

        @type socket_name: String
        @param socket_name: The name of the socket to be retrieved.
        @rtype: Socket
        @return: The socket for the given socket name.
        """

        # retrieves the socket provider plugins
        socket_provider_plugins = self.main_client_smtp.main_client_smtp_plugin.socket_provider_plugins

        # iterates over all the socket provider plugins
        for socket_provider_plugin in socket_provider_plugins:
            # retrieves the provider name from the socket provider plugin
            socket_provider_plugin_provider_name = socket_provider_plugin.get_provider_name()

            # in case the names are the same
            if socket_provider_plugin_provider_name == socket_name:
                # creates a new socket with the socket provider plugin
                socket = socket_provider_plugin.provide_socket()

                # returns the socket
                return socket

    def _upgrade_socket(self, socket, socket_name = "normal"):
        """
        Upgrades the socket for the given socket name
        using the socket upgrader plugins.

        @type socket: Socket
        @param socket: The socket to be upgraded.
        @type socket_name: String
        @param socket_name: The name of the socket to be retrieved for upgrading.
        @rtype: Socket
        @return: The upgraded socket for the given socket name.
        """

        # retrieves the socket upgrader plugins
        socket_upgrader_plugins = self.main_client_smtp.main_client_smtp_plugin.socket_upgrader_plugins

        # iterates over all the socket upgrader plugins
        for socket_upgrader_plugin in socket_upgrader_plugins:
            # retrieves the upgrader name from the socket upgrader plugin
            socket_upgrader_plugin_upgrader_name = socket_upgrader_plugin.get_upgrader_name()

            # in case the names are the same
            if socket_upgrader_plugin_upgrader_name == socket_name:
                # creates a new socket with the socket upgrader plugin
                socket = socket_upgrader_plugin.upgrade_socket(socket)

                # returns the socket
                return socket

class SmtpRequest:
    """
    The smtp request class.
    """

    message = None
    """ The message """

    command = None
    """ The command """

    session = None
    """ The session """

    message_stream = None
    """ The message stream """

    properties = {}
    """ The properties """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.messages = []
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()
        self.properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.command, self.message)

    def read(self):
        return self.message

    def write(self, message):
        self.message_stream.write(message)

    def get_result(self):
        """
        Retrieves the result value, processing
        the current request structure.

        @rtype: String
        @return: The result value for the current
        request structure.
        """

        # retrieves the result stream
        result = colony.libs.string_buffer_util.StringBuffer()

        # in case the command is defined
        if self.command:
            # writes the command to the result stream
            result.write(self.command)

        # in case both the command and the
        # message are defined
        if self.command and self.message:
            # writes the separator space to the
            # result stream
            result.write(" ")

        # in case the message is defined
        if self.message:
            # writes the message to the result stream
            result.write(self.message)

        # retrieves the result string value
        message = self.message_stream.get_value()

        # in case the message is not empty
        if not message == "":
            # writes the message to the result stream
            result.write(message)

        # writes the end of mail to the result stream
        result.write("\r\n")

        # retrieves the value from the result buffer
        result_value = result.get_value()

        # returns the result value
        return result_value

    def get_message(self):
        """
        Retrieves the message.

        @rtype: String
        @return: The message.
        """

        return self.message

    def set_message(self, message):
        """
        Sets the message.

        @type message: String
        @param message: The message.
        """

        self.message = message

    def get_command(self):
        """
        Retrieves the command.

        @rtype: String
        @return: The command.
        """

        return self.command

    def set_command(self, command):
        """
        Sets the code.

        @type command: String
        @param command: The command.
        """

        self.command = command

    def get_messages(self):
        """
        Retrieves the messages.

        @rtype: List
        @return: The messages.
        """

        return self.messages

    def set_messages(self, messages):
        """
        Sets the messages.

        @type messages: List
        @param messages: The messages.
        """

        self.messages = messages

    def get_session(self):
        """
        Retrieves the session.

        @rtype: Session
        @return: The session.
        """

        return self.session

    def set_session(self, session):
        """
        Sets the session.

        @type session: Session
        @param session: The session.
        """

        self.session = session

class SmtpResponse:
    """
    The smtp response class.
    """

    request = None
    """ The request that originated the response """

    message = None
    """ The message """

    messages = []
    """ The messages """

    code = None
    """ The code """

    session = None
    """ The session """

    properties = {}
    """ The properties """

    def __init__(self, request):
        """
        Constructor of the class.
        """

        self.request = request

        self.properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.code, self.message)

    def read(self):
        return self.message

    def add_message(self, message):
        """
        Adds a message to the list of messages.

        @type message: String
        @param message: The message to be added to the list
        of messages.
        """

        self.messages.append(message)

    def get_request(self):
        """
        Retrieves the request.

        @rtype: SmtpRequest
        @return: The request.
        """

        return self.request

    def set_request(self, request):
        """
        Sets the request.

        @type request: SmtpRequest
        @param request:  The request.
        """

        self.request = request

    def get_message(self):
        """
        Retrieves the message.

        @rtype: String
        @return: The message.
        """

        return self.message

    def set_message(self, message):
        """
        Sets the message.

        @type message: String
        @param message: The message.
        """

        self.message = message

    def get_messages(self):
        """
        Retrieves the messages.

        @rtype: List
        @return: The messages.
        """

        return self.messages

    def set_messages(self, messages):
        """
        Sets the messages.

        @type messages: List
        @param messages: The messages.
        """

        self.messages = messages

    def get_code(self):
        """
        Retrieves the code.

        @rtype: int
        @return: The code.
        """

        return self.code

    def set_code(self, code):
        """
        Sets the code.

        @type code: int
        @param code: The code.
        """

        self.code = code

    def get_session(self):
        """
        Retrieves the session.

        @rtype: Session
        @return: The session.
        """

        return self.session

    def set_session(self, session):
        """
        Sets the session.

        @type session: Session
        @param session: The session.
        """

        self.session = session

class SmtpSession:
    """
    The smtp session class.
    """

    client_hostname = "none"
    """ The client hostname """

    extensions_active = False
    """ The extensions active flag """

    data_transmission = False
    """ The data transmission flag """

    closed = False
    """ The closed flag """

    current_message = None
    """ The current message being processed """

    messages = []
    """ The messages associated with the session """

    properties = {}
    """ The properties of the current session """

    def __init__(self):
        self.messages = []
        self.properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.client_hostname, self.properties)

    def generate_message(self, set_current_message = True):
        # creates the new message
        message = SmtpMessage()

        # adds the message to the messages list
        self.add_message(message)

        # in case the set current message flag
        # is active
        if set_current_message:
            # sets the message as the current message
            self.set_current_message(message)

    def add_message(self, message):
        """
        Adds a message to the list of messages
        of the current session.

        @type message: SmtpMessage
        @param message: The message to be added
        to the session.
        """

        self.messages.append(message)

    def get_client_hostname(self):
        """
        Retrieves the client hostname.

        @rtype: String
        @return: The client hostname.
        """

        return self.client_hostname

    def set_client_hostname(self, client_hostname):
        """
        Sets the client hostname.

        @type client_hostname: String
        @param client_hostname: The client hostname.
        """

        self.client_hostname = client_hostname

    def get_extensions_active(self):
        """
        Retrieves the extensions active.

        @rtype: bool
        @return: The extensions active.
        """

        return self.extensions_active

    def set_extensions_active(self, extensions_active):
        """
        Sets the extensions active.

        @type extensions_active: bool
        @param extensions_active: The extensions active.
        """

        self.extensions_active = extensions_active

    def get_data_transmission(self):
        """
        Retrieves the data transmission.

        @rtype: bool
        @return: The data transmission.
        """

        return self.data_transmission

    def set_data_transmission(self, data_transmission):
        """
        Sets the data transmission.

        @type data_transmission: bool
        @param data_transmission: The data transmission.
        """

        self.data_transmission = data_transmission

    def get_closed(self):
        """
        Retrieves the closed.

        @rtype: bool
        @return: The closed.
        """

        return self.closed

    def set_closed(self, closed):
        """
        Sets the closed.

        @type closed: bool
        @param closed: The closed.
        """

        self.closed = closed

    def get_current_message(self):
        """
        Retrieves the current message.

        @rtype: SmtpMessage
        @return: The current message.
        """

        return self.current_message

    def set_current_message(self, current_message):
        """
        Sets the current message.

        @type current_message: SmtpMessage
        @param current_message: The current message.
        """

        self.current_message = current_message

    def get_messages(self):
        """
        Retrieves the messages.

        @rtype: List
        @return: The messages.
        """

        return self.messages

    def set_messages(self, messages):
        """
        Sets the messages.

        @type messages: List
        @param messages: The messages.
        """

        self.messages = messages

    def get_properties(self):
        """
        Retrieves the properties.

        @rtype: Dictionary
        @return: The properties.
        """

        return self.properties

    def set_properties(self, properties):
        """
        Sets the properties.

        @type properties: Dictionary
        @param properties: The properties.
        """

        self.properties = properties

class SmtpMessage:
    """
    The smtp message class that represents
    a message to be sent through smtp.
    """

    contents = "none"
    """ The contents of the message """

    sender = "none"
    """ The sender of the message """

    recipients_list = []
    """ The list of recipients for the message """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.recipients_list = []

    def add_recipient(self, recipient):
        """
        Adds a recipient to the recipients list

        @type recipient: String
        @param recipient: The recipient to be added.
        """

        self.recipients_list.append(recipient)

    def get_contents(self):
        """
        Retrieves the contents.

        @rtype: String
        @return: The contents.
        """

        return self.contents

    def set_contents(self, contents):
        """
        Sets the contents.

        @type contents: String
        @param contents: The contents.
        """

        self.contents = contents

    def get_sender(self):
        """
        Retrieves the .

        @rtype: String
        @return: The sender.
        """

        return self.sender

    def set_sender(self, sender):
        """
        Sets the sender.

        @type sender: String
        @param sender: The sender.
        """

        self.sender = sender

    def get_recipients_list(self):
        """
        Retrieves the recipients list.

        @rtype: List
        @return: The recipients list.
        """

        return self.recipients_list

    def set_recipients_list(self, recipients_list):
        """
        Sets the recipients list.

        @type recipients_list: List
        @param recipients_list: The recipients list.
        """

        self.recipients_list = recipients_list
