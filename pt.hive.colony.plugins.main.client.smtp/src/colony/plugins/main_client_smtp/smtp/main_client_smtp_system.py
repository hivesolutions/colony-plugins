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

        # creates the session object
        session = SmtpSession()

        # retrieves the initial response value
        response = self.retrieve_response(None, session)

        # sends the request for the given sender,
        # recipients list, message and parameters
        request = self.send_request("hello", "mail.sender.com", parameters)

        # retrieves the response
        response = self.retrieve_response(request)

        # returns the response
        return response

    def send_request(self, command, message, parameters):
        """
        Sends the request for the given parameters.

        @type queries: List
        @param queries: The list of queries to be sent.
        @type parameters: Dictionary
        @param parameters: The parameters to the request.
        @rtype: SmtpRequest
        @return: The sent request for the given parameters..
        """

        # creates the smtp request
        request = SmtpRequest()

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

            # in case the session is in data transmission mode
            if session.data_transmission:
                end_token = ".\r\n"
            else:
                end_token = "\r\n"

            # finds the first end token value
            end_token_index = message_value.find(end_token)

            # in case there is an end token found
            if not end_token_index == -1:
                # retrieves the smtp message
                smtp_message = message_value[:end_token_index]

                # in case the session is not in data transmission mode
                if not session.data_transmission:
                    # splits the smtp message
                    smtp_message_splitted = smtp_message.split(" ", 1)

                    # retrieves the smtp code
                    smtp_code = int(smtp_message_splitted[0])

                    # retrieves the smtp message
                    smtp_message = smtp_message_splitted[1]

                    # sets the smtp code in the response
                    response.set_code(smtp_code)

                    # sets the smtp message in the response
                    response.set_message(smtp_message)

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

#
#class SmtpClientHandler:
#    """
#    The smtp client handler.
#    Handles the client request and response for predefined
#    operations.
#    """
#
#    smtp_connection = None
#    """ The smtp connection to be used """
#
#    host = None
#    """ The host for the connection """
#
#    port = None
#    """ The port for the connection """
#
#    def __init__(self, smtp_connection, host, port):
#        """
#        Constructor of the class.
#
#        @type smtp_connection: Socket
#        @param smtp_connection: The smtp connection (socket) to be used.
#        @type host: String
#        @param host: The host for the connection.
#        @type port: int
#        @param port: The port for the connection.
#        """
#
#        smtp_connection
#
#    def send_email(self, sender, recipients_list, message, parameters = {}):
#        # creates a new response
#        response = SmtpResponse()
#
#        response.process_data(data)
#
#        request = SmtpRequest()
#
#        request.set_command("HELO")
#
#        request.set_message("OK: message queued for delivery")
#
#        pass
#
#    def retrieve_response(self):

class SmtpRequest:
    """
    The smtp request class.
    """

    message = "none"
    """ The message """

    command = "none"
    """ The command """

    messages = []
    """ The messages """

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

        # retrieves the result string value
        message = self.message_stream.get_value()

        # in case the messages are defined
        if self.messages:
            # initializes the return message
            return_message_buffer = colony.libs.string_buffer_util.StringBuffer()

            # starts the counter value
            counter = len(self.messages)

            # iterates over all the messages
            for message in self.messages:
                # in case the counter is one (last message)
                if counter == 1:
                    # adds the code with the message
                    return_message_buffer.write(self.command + " " + message + "\r\n")
                else:
                    # adds the code with the message (separated with a dash)
                    return_message_buffer.write(self.command + "-" + message + "\r\n")

                # decrements the counter
                counter -= 1

            # retrieves the return message from the return message buffer
            return_message = return_message_buffer.get_value()
        else:
            # creates the return message
            return_message = self.command + " " + self.message + "\r\n"

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

    message = "none"
    """ The message """

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

    def get_code(self):
        """
        Retrieves the code.

        @rtype: int
        @return: The code.
        """

        return self.message

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
