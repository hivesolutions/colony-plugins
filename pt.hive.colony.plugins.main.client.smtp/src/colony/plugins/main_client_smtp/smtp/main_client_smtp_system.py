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

        # receives the data
        data = self.retrieve_data()

        # processes the data
        response.process_data(data)

        # returns the response
        return response

    def retrieve_data(self, response_timeout = RESPONSE_TIMEOUT, data_size = MESSAGE_MAXIMUM_SIZE):
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
            data = self.smtp_connection.recv(data_size)
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

    host = "none"
    """ The host value """

    port = None
    """ The port value """

    operation_type = "none"
    """ The operation type """

    path = "none"
    """ The path """

    arguments = "none"
    """ The arguments """

    protocol_version = "none"
    """ The protocol version """

    attributes_map = {}
    """ The attributes map """

    headers_map = {}
    """ The headers map """

    content_type = None
    """ The content type """

    message_stream = None
    """ The message stream """

    content_type_charset = None
    """ The content type charset """

    def __init__(self, host = "none", port = None, path = "none", attributes_map = {}, operation_type = GET_METHOD_VALUE, protocol_version = HTTP_1_1_VERSION, content_type_charset = DEFAULT_CHARSET):
        self.host = host
        self.port = port
        self.path = path
        self.attributes_map = attributes_map
        self.operation_type = operation_type
        self.protocol_version = protocol_version
        self.content_type_charset = content_type_charset

        self.headers_map = {}
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()

    def get_result(self):
        # retrieves the result stream
        result = colony.libs.string_buffer_util.StringBuffer()

        # encodes the attributes
        encoded_attributes = self._encode_attributes()

        # sets the initial path
        path = self.path

        # in case the encoded attributes string
        # is valid and not empty
        if encoded_attributes:
            # in case the operation is of type get
            if self.operation_type == GET_METHOD_VALUE:
                # in case no exclamation mark exists in
                # the path
                if self.path.find("?") == -1:
                    path = self.path + "?" + encoded_attributes
                else:
                    path = self.path + "&" + encoded_attributes
            # in case the operation is of type post
            elif self.operation_type == POST_METHOD_VALUE:
                # writes the encoded attributes into the message stream
                self.message_stream.write(encoded_attributes)

                # sets the response content type
                self.content_type = "application/x-www-form-urlencoded"

        # retrieves the real host value
        real_host = self._get_real_host()

        # retrieves the result string value
        message = self.message_stream.get_value()

        # retrieves the content length from the
        # message content itself
        content_length = len(message)

        # writes the http command in the string buffer (version, status code and status value)
        result.write(self.operation_type + " " + path + " " + self.protocol_version + "\r\n")

        # in case there is a content type defined
        if self.content_type:
            result.write(CONTENT_TYPE_VALUE + ": " + self.content_type + "\r\n")

        # in case the content length is valid
        if content_length > 0:
            result.write(CONTENT_LENGTH_VALUE + ": " + str(content_length) + "\r\n")

        result.write(HOST_VALUE + ": " + real_host + "\r\n")
        result.write(USER_AGENT_VALUE + ": " + USER_AGENT_IDENTIFIER + "\r\n")
        result.write("Accept" + ": " + "text/html,application/xhtml+xml,application/xml;q=0.7,*;q=0.7" + "\r\n")
        result.write("Accept-Language" + ": " + "en-us,en;q=0.5" + "\r\n")
        #result.write("Accept-Encoding" + ": " + "gzip,deflate" + "\r\n")
        result.write("Accept-Charset" + ": " + "iso-8859-1,utf-8;q=0.7,*;q=0.7" + "\r\n")
        result.write("Keep-Alive" + ": " + "115" + "\r\n")
        result.write("Connection" + ": " + "keep-alive" + "\r\n")
        result.write("Cache-Control" + ": " + "max-age=0" + "\r\n")

        # iterates over all the header values to be sent
        for header_name, header_value in self.headers_map.items():
            # writes the extra header value in the result
            result.write(header_name + ": " + header_value + "\r\n")

        # writes the end of the headers and the message
        # values into the result
        result.write("\r\n")
        result.write(message)

        # retrieves the value from the result buffer
        result_value = result.get_value()

        # returns the result value
        return result_value

    def _get_real_host(self):
        """
        Retrieves the "real" host value to be sent
        in http header of the request.

        @rtype: String
        @return: The "real" host value.
        """

        # in case the port is defined and
        # is not a default port
        if self.port and self.port not in DEFAULT_PORTS:
            # returns the host appended with the port value
            return self.host + ":" + str(self.port)
        # in case the port is not defined
        else:
            # returns only the host
            return self.host

    def _quote(self, string_value, safe = "/"):
        """
        Quotes the given string value according to
        the url encoding specification.
        The implementation is based on the python base library.

        @type string_value: String
        @param string_value: The string value to be quoted.
        @rtype: String
        @return: The quoted string value.
        """

        # creates the cache key tuple
        cache_key = (safe, QUOTE_SAFE_CHAR)

        try:
            # in case the cache key is not defined
            # in the quote sage maps creates a new entry
            safe_map = QUOTE_SAFE_MAPS[cache_key]
        except KeyError:
            # adds the "base" quote safe characters to the
            # "safe list"
            safe += QUOTE_SAFE_CHAR

            # starts the safe map
            safe_map = {}

            # iterates over all the ascii values
            for index in range(256):
                # retrieves the character for the
                # given index
                character = chr(index)

                # adds the "valid" character ot the safe mao entry
                safe_map[character] = (character in safe) and character or ("%%%02X" % index)

            # sets the safe map in the cache quote safe maps
            QUOTE_SAFE_MAPS[cache_key] = safe_map

        # maps the getitem method of the map to all the string
        # value to retrieve the valid items
        resolution_list = map(safe_map.__getitem__, string_value)

        # joins the resolution list to retrieve the quoted value
        return "".join(resolution_list)

    def _quote_plus(self, string_value, safe = ""):
        """
        Quotes the given string value according to
        the url encoding specification. This kind of quote
        takes into account the plus and the space relation.
        The implementation is based on the python base library.

        @type string_value: String
        @param string_value: The string value to be quoted.
        @rtype: String
        @return: The quoted string value.
        """

        # in case there is at least one white
        # space in the string value
        if " " in string_value:
            # quotes the string value adding the white space
            # to the "safe list"
            string_value = self._quote(string_value, safe + " ")

            # replaces the white spaces with plus signs and
            # returns the result
            return string_value.replace(" ", "+")

        # returns the quoted string value
        return self._quote(string_value, safe)

    def _encode_attributes(self):
        """
        Encodes the current attributes into url encoding.

        @rtype: String
        @return: The encoded parameters.
        """

        # creates a string buffer to hold the encoded attribute values
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # sets the is first flag
        is_first = True

        # iterates over all the attribute keys and values
        for attribute_key, attribute_value in self.attributes_map.items():
            # encodes both the attribute key and value
            attribte_key_encoded = self._encode(attribute_key)
            attribte_value_encoded = self._encode(attribute_value)

            # quotes both the attribute key and value
            attribute_key_quoted = self._quote_plus(attribte_key_encoded)
            attribute_value_quoted = self._quote_plus(attribte_value_encoded)

            # in case it's is the first iteration
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # writes the and continuation in the string buffer
                string_buffer.write("&")

            # adds the quoted key and value strings to the
            # string buffer
            string_buffer.write(attribute_key_quoted)
            string_buffer.write("=")
            string_buffer.write(attribute_value_quoted)

        # retrieves the encoded attributes from the string buffer
        encoded_attributes = string_buffer.get_value()

        # returns the encoded attributes
        return encoded_attributes

    def _encode(self, string_value):
        """
        Encodes the given string value to the current encoding.

        @type string_value: String
        @param string_value: The string value to be encoded.
        @rtype: String
        @return: The given string value encoded in the current encoding.
        """

        return unicode(string_value).encode(self.content_type_charset)

class HttpResponse:
    """
    The http response class.
    """

    request = None
    """ The request that originated the response """

    protocol_version = "none"
    """ The protocol version """

    headers_map = {}
    """ The headers map """

    received_message = "none"
    """ The received message """

    status_code = None
    """ The status code """

    status_message = None
    """ The status message """

    content_type_charset = None
    """ The content type charset """

    def __init__(self, request):
        """
        Constructor of the class.
        """

        self.request = request

        self.attributes_map = {}
        self.headers_map = {}
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()

    def set_protocol_version(self, protocol_version):
        """
        Sets the protocol version.

        @type protocol_version: String
        @param protocol_version: The protocol version.
        """

        self.protocol_version = protocol_version

    def set_status_code(self, status_code):
        """
        Sets the status code.

        @type status_code: int
        @param status_code: The status code.
        """

        self.status_code = status_code

    def set_status_message(self, status_message):
        """
        Sets the status message.

        @type status_message: String
        @param status_message: The status message.
        """

        self.status_message = status_message
