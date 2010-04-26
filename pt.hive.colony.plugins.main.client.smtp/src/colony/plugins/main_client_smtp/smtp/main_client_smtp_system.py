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
import socket
import select

import colony.libs.string_buffer_util

import main_client_smtp_exceptions

DEFAULT_PORT = 25
""" The default port """

DEFAULT_SOCKET_NAME = "normal"
""" The default socket name """

RESPONSE_TIMEOUT = 10
""" The response timeout """

CHUNK_SIZE = 4096
""" The chunk size """

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

        # sends the request for the given sender,
        # recipients list, message and parameters
        request = self.send_request(sender, recipients_list, message, parameters)

        # retrieves the response
        response = self.retrieve_response(request)

        # returns the response
        return response

    def send_request(self, sender, recipients_list, message, parameters):
        """
        Sends the request for the given parameters.

        @type queries: List
        @param queries: The list of queries to be sent.
        @type parameters: Dictionary
        @param parameters: The parameters to the request.
        @rtype: SmtpRequest
        @return: The sent request for the given parameters..
        """

        # creates the smtp request with the the sender,
        # the recipients_list, the message and the parameters
        request = SmtpRequest(sender, recipients_list, message, parameters)

        # retrieves the result value from the request
        result_value = request.get_result()

        # sends the result value
        self.smtp_connection.send(result_value)

        # returns the request
        return request

    def retrieve_response(self, request, response_timeout = RESPONSE_TIMEOUT):
        """
        Retrieves the response from the sent request.

        @rtype: SmtpRequest
        @return: The request that originated the response.
        @type response_timeout: int
        @param response_timeout: The timeout for the response retrieval.
        @rtype: SmtpResponse
        @return: The response from the sent request.
        """

        # creates a response object
        response = SmtpResponse(request)

        # todo: tenho de ter aki um ciclo
        # para receber a resposta como deve de ser
        # como no cliente de http

        # receives the data
        data = self.retrieve_data()

        # processes the data
        response.process_data(data)

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

class SmtpRequest:
    """
    The smtp request class.
    """

    message = "none"
    """ The received message """

    command = "none"
    """ The received command """

    arguments = "none"
    """ The received arguments """

    session = None
    """ The session """

    message_stream = None
    """ The message stream """

    properties = {}
    """ The properties """

    def __init__(self):
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

        # retrieves the result string value
        message = self.message_stream.get_value()

        # in case the response messages
        # are defined
        if self.response_messages:
            # initializes the return message
            return_message_buffer = colony.libs.string_buffer_util.StringBuffer()

            # starts the counter value
            counter = len(self.response_messages)

            # iterates over all the response messages
            for response_message in self.response_messages:
                # in case the counter is one (last response message)
                if counter == 1:
                    # adds the response code with the response message
                    return_message_buffer.write(str(self.response_code) + " " + response_message + "\r\n")
                else:
                    # adds the response code with the response message (separated with a dash)
                    return_message_buffer.write(str(self.response_code) + "-" + response_message + "\r\n")

                # decrements the counter
                counter -= 1

            # retrieves the return message from the return message buffer
            return_message = return_message_buffer.get_value()
        else:
            # creates the return message
            return_message = str(self.response_code) + " " + self.response_message + "\r\n"

            # in case the message is not empty
            if not message == "":
                return_message += message + "\r\n"

        # returns the return message
        return return_message

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
        Sets the command.

        @type command: String
        @param command: The command.
        """

        self.command = command

    def get_arguments(self):
        """
        Retrieves the arguments.

        @rtype: List
        @return: The arguments.
        """

        return self.arguments

    def set_arguments(self, arguments):
        """
        Sets the arguments.

        @type arguments: List
        @param arguments: The arguments.
        """

        self.arguments = arguments

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

    def __init__(self, request):
        """
        Constructor of the class.
        """

        self.request = request
