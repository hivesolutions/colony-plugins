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

__version__ = "1.0.1"
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
import types
import base64
import threading

import colony.libs.map_util
import colony.libs.quote_util
import colony.libs.structures_util
import colony.libs.string_buffer_util

import main_client_http_exceptions

HTTP_PREFIX_VALUE = "http://"
""" The http prefix value """

HTTPS_PREFIX_VALUE = "https://"
""" The https prefix value """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

HTTP_1_1_VERSION = "HTTP/1.1"
""" The http 1.1 protocol version """

WWW_FORM_URLENCODED_VALUE = "application/x-www-form-urlencoded"
""" The www form urlencoded value """

REQUEST_TIMEOUT = 30
""" The request timeout """

RESPONSE_TIMEOUT = 30
""" The response timeout """

CHUNK_SIZE = 4096
""" The chunk size """

USER_AGENT_NAME = "Hive-Colony-Web-Client"
""" The user agent name """

USER_AGENT_VERSION = "1.0.0"
""" The user agent version """

ENVIRONMENT_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + "-" + str(sys.version_info[3])
""" The environment version """

USER_AGENT_IDENTIFIER = USER_AGENT_NAME + "/" + USER_AGENT_VERSION + " (python/" + sys.platform + "/" + ENVIRONMENT_VERSION + ")"
""" The user agent identifier """

DEFAULT_CONTENT_TYPE = None
""" The default content type """

DEFAULT_CHARSET = None
""" The default charset """

DEFAULT_URL_CHARSET = "utf-8"
""" The default url charset """

STATUS_CODE_VALUES = {
    100 : "Continue",
    101 : "Switching Protocols",
    200 : "OK",
    201 : "Created",
    202 : "Accepted",
    203 : "Non-Authoritative Information",
    204 : "No Content",
    205 : "Reset Content",
    206 : "Partial Content",
    207 : "Multi-Status",
    301 : "Moved permanently",
    302 : "Found",
    303 : "See Other",
    304 : "Not Modified",
    305 : "Use Proxy",
    306 : "(Unused)",
    307 : "Temporary Redirect",
    400 : "Bad Request",
    401 : "Unauthorized",
    402 : "Payment Required",
    403 : "Forbidden",
    404 : "Not Found",
    405 : "Method Not Allowed",
    406 : "Not Acceptable",
    407 : "Proxy Authentication Required",
    408 : "Request Timeout",
    409 : "Conflict",
    410 : "Gone",
    411 : "Length Required",
    412 : "Precondition Failed",
    413 : "Request Entity Too Large",
    414 : "Request-URI Too Long",
    415 : "Unsupported Media Type",
    416 : "Requested Range Not Satisfiable",
    417 : "Expectation Failed",
    500 : "Internal Server Error",
    501 : "Not Implemented",
    502 : "Bad Gateway",
    503 : "Service Unavailable",
    504 : "Gateway Timeout",
    505 : "HTTP Version Not Supported"
}
""" The status code values map """

CHUNKED_VALUE = "chunked"
""" The chunked value """

HOST_VALUE = "Host"
""" The host value """

USER_AGENT_VALUE = "User-Agent"
""" The user agent value """

CONTENT_LENGTH_VALUE = "Content-Length"
""" The content length value """

CONTENT_TYPE_VALUE = "Content-Type"
""" The content type value """

KEEP_ALIVE_VALUE = "Keep-Alive"
""" The keep alive value """

CONNECTION_VALUE = "Connection"
""" The connection value """

CACHE_CONTROL_VALUE = "Cache-Control"
""" The cache control value """

AUTHORIZATION_VALUE = "Authorization"
""" The authorization value """

TRANSFER_ENCODING_VALUE = "Transfer-Encoding"
""" The transfer encoding value """

TRANSFER_ENCODING_LOWER_VALUE = "transfer-encoding"
""" The transfer encoding value """

LOCATION_VALUE = "Location"
""" The location value """

BASIC_VALUE = "Basic"
""" The basic value """

NO_CACHE_VALUE = "no-cache"
""" The no cache value """

PROTOCOL_VERSION_VALUE = "protocol_version"
""" The protocol version value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

DEFAULT_PORTS = (80, 443)
""" The tuple of default ports """

DEFAULT_PERSISTENT = True
""" The default persistent """

DEFAULT_KEEP_ALIVE_TIMEOUT = 115
""" The default keep alive timeout """

DEFAULT_SOCKET_PARAMETERS = {}
""" The default socket parameters """

UNDEFINED_CONTENT_LENGTH = None
""" The undefined content length """

UNDEFINED_CONTENT_LENGTH_STATUS_CODES = (204, 304)
""" The status codes for undefined content length """

REDIRECT_STATUS_CODES = (301, 302, 307)
""" The status codes for redirection """

PROTOCOL_SOCKET_NAME_MAP = {
    HTTP_PREFIX_VALUE : "normal",
    HTTPS_PREFIX_VALUE : "ssl"
}
""" The map associating the http protocol prefixed with the name of the socket """

PROTOCOL_DEFAULT_PORT_MAP = {
    HTTP_PREFIX_VALUE : 80,
    HTTPS_PREFIX_VALUE : 443
}
""" The map associating the http protocol prefixed with the port number """

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
""" The date format """

class MainClientHttp:
    """
    The main client http class.
    """

    main_client_http_plugin = None
    """ The main client http plugin """

    def __init__(self, main_client_http_plugin):
        """
        Constructor of the class.

        @type main_client_http_plugin: MainClientHttpPlugin
        @param main_client_http_plugin: The main client http plugin.
        """

        self.main_client_http_plugin = main_client_http_plugin

    def create_client(self, parameters):
        """
        Creates a client object for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to be used in creating
        the client object.
        @rtype: HttpClient
        @return: The created client object.
        """

        # retrieves the protovol version
        protocol_version = parameters.get(PROTOCOL_VERSION_VALUE, None)

        # retrieves the content type charset
        content_type_charset = parameters.get(CONTENT_TYPE_CHARSET_VALUE, DEFAULT_CHARSET)

        # creates the http client
        http_client = HttpClient(self, protocol_version, content_type_charset)

        # returns the http client
        return http_client

    def create_request(self, parameters):
        pass

class HttpClient:
    """
    The http client class, representing
    a client connection in the http protocol.
    """

    main_client_http = None
    """ The main client http object """

    protocol_version = "none"
    """ The version of the http protocol """

    content_type_charset = None
    """ The content type charset """

    authentication = False
    """ The authentication flag """

    username = "none"
    """ The username to be used in authentication """

    password = "none"
    """ The password to be used in authentication """

    no_cache = False
    """ The no cache flag """

    redirect = True
    """ The value controlling the "auto" redirection """

    client_connection = None
    """ The current client connection """

    _http_client = None
    """ The http client object used to provide connections """

    _http_client_lock = None
    """ Lock to control the fetching of the queries """

    def __init__(self, main_client_http, protocol_version, content_type_charset = DEFAULT_CHARSET):
        """
        Constructor of the class.

        @type main_client_http: MainClientHttp
        @param main_client_http: The main client http object.
        @type protocol_version: String
        @param protocol_version: The version of the http protocol to
        be used.
        @type content_type_charset: String
        @param content_type_charset: The charset to be used by the content.
        """

        self.main_client_http = main_client_http
        self.protocol_version = protocol_version
        self.content_type_charset = content_type_charset

        self._http_client_lock = threading.RLock()

    def open(self, parameters):
        # generates the parameters
        client_parameters = self._generate_client_parameters(parameters)

        # creates the http client, generating the internal structures
        self._http_client = self.main_client_http.main_client_http_plugin.main_client_utils_plugin.generate_client(client_parameters)

        # starts the http client
        self._http_client.start_client()

    def close(self, parameters):
        # stops the http client
        self._http_client.stop_client()

    def fetch_url(self, url, method = GET_METHOD_VALUE, parameters = {}, protocol_version = HTTP_1_1_VERSION, headers = {}, content_type = DEFAULT_CONTENT_TYPE, content_type_charset = DEFAULT_CHARSET, encode_path = False, contents = None, save_message = True, yield_response = False, handlers_map = {}):
        """
        Fetches the url for the given url, method and (http) parameters.

        @type url: String
        @param url: The url to be fetched.
        @type method: String
        @param method: The method to be used.
        @type parameters: Dictionary
        @param parameters: The (http) parameters to be used in the fetching.
        @type protocol_version: String
        @param protocol_version: The version of the protocol to be used.
        @type headers: Dictionary
        @param headers: The (http) headers to be used in the fetching.
        @type content_type: String
        @param content_type: The content type of the message.
        @type content_type_charset: String
        @param content_type_charset: The content type charset to be used.
        @type encode_path: bool
        @param encode_path: If the path should be encoded.
        @type contents: String
        @param contents: The contents of the message to be sent.
        @type save_message: bool
        @param save_message: If the message part of the response
        should be saved (at the expense of memory).
        @type yield_response: bool
        @param yield_response: If the response value should be yielded
        for progressive retrieval. Setting this flag changes the return
        value to an iterator that may be used for reponse retrieval.
        @type handlers_map: Dictionary
        @param handlers_map: The map of event handlers for the various
        client events.
        @rtype: HttpResponse
        @return: The retrieved response object.
        """

        # retrieves the main client http plugin
        main_client_http_plugin = self.main_client_http.main_client_http_plugin

        # print a debug message
        main_client_http_plugin.debug("Fetching url '%s' with '%s' method" % (url, method))

        # parses the url retrieving the protocol the host, the username,
        # the password, the port, the path, the base url and the options map
        protocol, username, password, host, port, path, base_url, options_map = self._parse_url(url)

        # extends the parameters map with the options map
        parameters = colony.libs.map_util.map_extend(parameters, options_map)

        # retrieves the persistent (default)
        persistent = DEFAULT_PERSISTENT

        # retrieves the socket name from the protocol socket map
        socket_name = PROTOCOL_SOCKET_NAME_MAP.get(protocol, None)

        # retrieves the socket parameters (default)
        socket_parameters = DEFAULT_SOCKET_PARAMETERS

        # defines the connection parameters
        connection_parameters = (
            host,
            port,
            persistent,
            socket_name,
            socket_parameters
        )

        # retrieves the corresponding (http) client connection
        self.client_connection = self._http_client.get_client_connection(connection_parameters)

        # acquires the http client lock
        self._http_client_lock.acquire()

        # saves the old authentication
        # values for later restore
        _authentication = self.authentication
        _username = self.username
        _password = self.password

        # in case the username and password are
        # set using the url
        if username and password:
            # sets the authentication flag
            self.authentication = True

            # sets the username and password
            # in the current client
            self.username = username
            self.password = password

        try:
            # sends the request for the host, port, path,
            # parameters, method, headers, protocol version, content type,
            # content type charset, encode path, contents, url and base url
            # and retrieves the request
            request = self.send_request(host, port, path, parameters, method, headers, protocol_version, content_type, content_type_charset, encode_path, contents, url, base_url)

            # retrieves the response, controls the saving of the message
            # and calls the appropriate handlers, the yield state is respected
            # it the yield response is set
            response = self.retrieve_response(request, save_message, yield_response, handlers_map)

            # retrieves the response according to the state of the yield response
            response = yield_response and response or ([value for value in response][0])
        finally:
            # sets the authentication flag
            self.authentication = _authentication

            # sets the username and password
            # in the current client
            self.username = _username
            self.password = _password

            # releases the http client lock
            self._http_client_lock.release()

        # returns the response
        return response

    def build_url(self, base_url, method, parameters):
        """
        Builds the url for the given base url, method
        and parameters.

        @type base_url: String
        @param base_url: The base url to build the final
        url.
        @type method: String
        @param method: The method to be used in the url retrieval.
        @type parameters: Dicionary
        @param parameters: The parameters to be used in the url
        retrieval.
        @rtype: String
        @return: The final url value.
        """

        # in case the request method is not get
        if not method == GET_METHOD_VALUE:
            # returns the base url
            return base_url

        # creates the http request to build the url
        request = HttpRequest(attributes_map = parameters)

        # encodes the request attributes
        encoded_attributes = request._encode_attributes()

        # in case the encoded attributes string
        # is not valid or is empty the url remain
        # the base one
        if not encoded_attributes:
            # returns the base url
            return base_url

        # in case no exclamation mark exists in
        # the url
        if base_url.find("?") == -1:
            # creates the url by adding the encoded attributes
            # as the first parameters
            url = base_url + "?" + encoded_attributes
        # in case an exclamation mark already exists in the
        # url (parameters exist)
        else:
            # creates the url by adding the encoded attributes
            # to the existing parameters
            url = base_url + "&" + encoded_attributes

        # return the built url
        return url

    def send_request(self, host, port, path, parameters, operation_type, headers, protocol_version, content_type, content_type_charset, encode_path, contents, url, base_url):
        """
        Sends the request for the given parameters.

        @type host: String
        @param host: The host to be used by the request.
        @type port: int
        @param port: The tcp port to be used.
        @type path: String
        @param path: The path to be retrieve via http.
        @type parameters: Dictionary
        @param parameters: The parameters to the request.
        @type operation_type: String
        @param operation_type: The operation type for the request.
        @type headers: Dictionary
        @param headers: The headers to the request.
        @type protocol_version: String
        @param protocol_version: The protocol version of the request.
        @type content_type: String
        @param content_type: The content type of the message.
        @type content_type_charset: String
        @param content_type_charset: The content type charset.
        @type encode_path: bool
        @param encode_path: If the path should be encoded.
        @type contents: String
        @param contents: The contents of the message to be sent.
        @type url: String
        @param url: The complete url of the request.
        @type base_url: String
        @param base_url: The base url of the request.
        @rtype: HttpRequest
        @return: The sent request for the given parameters.
        """

        # creates the http request with the host, the port, the path, the parameters, operation type,
        # the headers, the protocol version, the content type, the content type charset, the encode path,
        # the url and the base url
        request = HttpRequest(host, port, path, parameters, operation_type, headers, protocol_version, content_type, content_type_charset, encode_path, url, base_url)

        # in case the contents are defined
        if contents:
            # writes the contents to the request
            request.write(contents)

        # in case authentication is set
        if self.authentication:
            # sets the authentication in the request
            request.set_authentication(self.username, self.password)

        # in case no cache is set
        if self.no_cache:
            # sets the no cache in the request
            request.set_no_cache(self.no_cache)

        # retrieves the result value from the request
        result_value = request.get_result()

        # sends the result value
        self.client_connection.send(result_value)

        # returns the request
        return request

    def retrieve_response(self, request, save_message = True, yield_response = False, handlers_map = {}, response_timeout = None):
        """
        Retrieves the response from the sent request.

        @type request: HttpRequest
        @param request: The request that originated the response.
        @type save_message: bool
        @param save_message: If the message part of the response
        should be saved (at the expense of memory).
        @type yield_response: bool
        @param yield_response: If the response value should be yielded
        for progressive retrieval.
        @type handlers_map: Dictionary
        @param handlers_map: The map of event handlers for the various
        client events.
        @type response_timeout: int
        @param response_timeout: The timeout for the response retrieval.
        @rtype: HttpResponse
        @return: The response from the sent request.
        """

        # creates the string buffer for the message
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates a response object
        response = HttpResponse(request)

        # creates the start line loaded flag
        start_line_loaded = False

        # creates the header loaded flag
        header_loaded = False

        # creates the message loaded flag
        message_loaded = False

        # creates the message offset index, representing the
        # offset byte to the initialization of the message
        message_offset_index = 0

        # creates the message size value
        message_size = 0

        # creates the received data size (counter)
        received_data_size = 0

        # unsets the undefined content length finished
        undefined_content_length_finished = False

        # continuous loop
        while True:
            # receives the data
            data = self.client_connection.receive(response_timeout, CHUNK_SIZE)

            # in case no valid data was received
            if data == "":
                # in case the message size is undefined
                if message_size == UNDEFINED_CONTENT_LENGTH:
                    # sets the undefined contents length finished flag
                    undefined_content_length_finished = True
                # otherwise the message size must be defined
                else:
                    # raises the http invalid data exception
                    raise main_client_http_exceptions.HttpInvalidDataException("empty data received")

            # retrieves the data length
            data_length = len(data)

            # increments the received data size (counter)
            received_data_size += data_length

            # in case the undefined content length
            # search is finished
            if undefined_content_length_finished:
                # calculates the message size from the current
                # received data size
                message_size = received_data_size - message_offset_index

            # writes the data to the string buffer, only in case
            # the headers are not yet loaded or the save message is set
            (not header_loaded or save_message) and message.write(data)

            # calls the data handler (data event)
            self._call_handler_data("data", handlers_map, response, data)
            if yield_response: yield "data", response, data

            # calls the message data handler (message data event)
            header_loaded and self._call_handler_data("message_data", handlers_map, response, data)
            if header_loaded and yield_response: yield "message_data", response, data

            # in case the header is not loaded or the message contents are completely loaded
            if not header_loaded or received_data_size == message_size + message_offset_index:
                # retrieves the message value from the string buffer
                message_value = message.get_value()
            # in case there's no need to inspect the message contents
            else:
                # continues the loop
                continue

            # in case the start line is not loaded
            if not start_line_loaded:
                # finds the first new line value
                start_line_index = message_value.find("\r\n")

                # in case there is a new line value found
                if not start_line_index == -1:
                    # retrieves the start line
                    start_line = message_value[:start_line_index]

                    # splits the start line in spaces
                    start_line_splitted = start_line.split(" ", 2)

                    # retrieves the start line splitted length
                    start_line_splitted_length = len(start_line_splitted)

                    # in case the length of the splitted line is not valid
                    if start_line_splitted_length < 3:
                        # raises the http invalid data exception
                        raise main_client_http_exceptions.HttpInvalidDataException("invalid data received: " + start_line)

                    # retrieve the protocol version the status code and the satus message
                    # from the start line splitted
                    protocol_version, status_code, status_message = start_line_splitted

                    # converts the status code to integer
                    status_code_integer = int(status_code)

                    # sets the response protocol version
                    response.set_protocol_version(protocol_version)

                    # sets the response status code
                    response.set_status_code(status_code_integer)

                    # sets the response status message
                    response.set_status_message(status_message)

                    # sets the start line loaded flag
                    start_line_loaded = True

                    # calls the start line (end) handler (start line event)
                    self._call_handler("start_line", handlers_map, response)
                    if yield_response: yield "start_line", response

            # in case the header is not loaded
            if not header_loaded:
                # retrieves the end header index (two new lines)
                end_header_index = message_value.find("\r\n\r\n")

                # in case the end header index is found
                if not end_header_index == -1:
                    # sets the message offset index as the end header index
                    # plus the two sequences of newlines (four characters)
                    message_offset_index = end_header_index + 4

                    # sets the header loaded flag
                    header_loaded = True

                    # retrieves the start header index
                    start_header_index = start_line_index + 2

                    # retrieves the headers part of the message
                    headers = message_value[start_header_index:end_header_index]

                    # splits the headers by line
                    headers_splitted = headers.split("\r\n")

                    # iterates over the headers lines
                    for header_splitted in headers_splitted:
                        # finds the header separator
                        division_index = header_splitted.find(":")

                        # retrieves the header name
                        header_name = header_splitted[:division_index].strip()

                        # retrieves the header value
                        header_value = header_splitted[division_index + 1:].strip()

                        # sets the header in the headers map
                        response.headers_map[header_name] = header_value

                    # in case the content length exists in the headers map
                    if CONTENT_LENGTH_VALUE in response.headers_map:
                        # retrieves the message size as the content length value
                        message_size = int(response.headers_map[CONTENT_LENGTH_VALUE])
                    # in case the current status code refers to a response
                    # with no message body
                    elif self._status_code_no_message_body(status_code_integer):
                        # sets the message size as zero
                        message_size = 0
                    # otherwise it must be a response with no content
                    # length defined (must wait for closing of connection)
                    else:
                        # sets the message size as undefined content
                        # length value
                        message_size = UNDEFINED_CONTENT_LENGTH

                    # calls the headers (end) handler (headers event)
                    self._call_handler("headers", handlers_map, response)
                    if yield_response: yield "headers", response

                    # retrieves the transfer encoding value
                    transfer_encoding = response.headers_map.get(TRANSFER_ENCODING_VALUE, None)

                    # retrieves the transfer encoding value using the lower cased value
                    transfer_encoding = response.headers_map.get(TRANSFER_ENCODING_LOWER_VALUE, transfer_encoding)

                    # retrieves the start message index (the end header
                    # index plus the newline characters) then uses it
                    # to retrieve the start message value (initial data)
                    start_message_index = end_header_index + 4
                    start_message_value = message_value[start_message_index:]

                    # in case the transfer encoding is chunked
                    if transfer_encoding == CHUNKED_VALUE:
                        # retrieves the response in chunked mode, sends the start (initial)
                        # message value
                        chunked_generator = self.retrieve_response_chunked(response, start_message_value, save_message, yield_response, handlers_map, response_timeout)

                        # iterates over all the chunked items in the chunked
                        # generator to yield them
                        for chunked_item in chunked_generator:
                            # yields the current chunked item
                            if yield_response: yield chunked_item

                        # breaks the loop
                        break
                    # otherwise it's a normal handling but we still have to
                    # call the message data event handlers with the initial
                    # data (if any)
                    else:
                        # calls the message data handler (message data event)
                        start_message_value and self._call_handler_data("message_data", handlers_map, response, start_message_value)
                        if yield_response and start_message_value: yield "message_data", response, start_message_value

            # in case the message is not loaded and the header is loaded
            if not message_loaded and header_loaded:
                # retrieves the start message size
                start_message_index = end_header_index + 4

                # retrieves the message value length
                message_value_length = not save_message and received_data_size or len(message_value)

                # calculates the message value message length
                message_value_message_length = message_value_length - start_message_index

                # in case the length of the message value message is the same
                # or greater as the message size and the message size
                # is not undefined
                if message_value_message_length >= message_size and not message_size == UNDEFINED_CONTENT_LENGTH:
                    # retrieves the message part of the message value
                    message_value_message = message_value[start_message_index:]

                    # sets the message loaded flag
                    message_loaded = True

                    # sets the received message, taking into account
                    # the save message flag (empty received message, no saving)
                    response.received_message = save_message and message_value_message or ""

                    # decodes the response if necessary
                    self.decode_response(response)

                    # processes the redirection of the request
                    redirection_value = self._process_redirection(request, response)

                    # sets the final response value
                    response = redirection_value or response

                    # calls the message (end) handler (message event)
                    self._call_handler("message", handlers_map, response)
                    if yield_response: yield "message", response

                    # breaks the loop
                    break

        # returns the response
        yield response

    def retrieve_response_chunked(self, response, message_value, save_message = True, yield_response = False, handlers_map = {}, response_timeout = None):
        # creates the message string buffer
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates the contents string buffer
        contents = colony.libs.string_buffer_util.StringBuffer()

        # writes the message value to the message
        message.write(message_value)

        # calls the message data handler (message data event)
        self._call_handler_data("message_data", handlers_map, response, message_value)
        if yield_response: yield "message_data", response, message_value

        # tries to find the octet end index
        octet_end_index = message_value.find("\r\n")

        # loops indefinitely
        while True:
            # iterates while the end of octets part is not found
            while octet_end_index == -1:
                # receives the data
                data = self.client_connection.receive(response_timeout, CHUNK_SIZE)

                # in case no valid data was received
                if data == "":
                    # raises the http invalid data exception
                    raise main_client_http_exceptions.HttpInvalidDataException("empty data received")

                # retrieves the data length
                data_length = len(data)

                # writes the data to the message
                message.write(data)

                # calls the data handler (data event)
                self._call_handler_data("data", handlers_map, response, data)
                if yield_response: yield "data", response, data

                # calls the message data handler (message data event)
                self._call_handler_data("message_data", handlers_map, response, data)
                if yield_response: yield "message_data", response, data

                # retrieves the message value
                message_value = message.get_value()

                # tries to find the octet end index
                octet_end_index = message_value.find("\r\n")

            # retrieves the octet size string
            octet_size_string = message_value[:octet_end_index]

            # converts the octet size string to integer
            octet_size = int(octet_size_string.strip(), 16)

            # in case the octet size is zero (end of chunk encoding)
            if octet_size == 0:
                # breaks the loop
                break

            # retrieves the partial message (extra message in data retrieval)
            partial_message = message_value[octet_end_index + 2:]

            # calculates the partial message length
            partial_message_length = len(partial_message)

            # resets the message (buffer)
            message.reset()

            # writes the (initial) partial message to the message
            message.write(partial_message)

            # calculates the initial message size
            message_size = partial_message_length

            # calculates the octet end as the octet size plus
            # the two extra end of chunk characters
            octet_end = octet_size + 2

            # iterates while the message size is lower
            # than the octet size plus the extra end of chunk characters
            while message_size < octet_end:
                # receives the data
                data = self.client_connection.receive(response_timeout)

                # in case no valid data was received
                if data == "":
                    # raises the http invalid data exception
                    raise main_client_http_exceptions.HttpInvalidDataException("empty data received")

                # retrieves the data length
                data_length = len(data)

                # writes the data to the message
                message.write(data)

                # increments the message size with
                # the data length
                message_size += data_length

                # calls the data handler (data event)
                self._call_handler_data("data", handlers_map, response, data)
                if yield_response: yield "data", response, data

                # calls the message data handler (message data event)
                self._call_handler_data("message_data", handlers_map, response, data)
                if yield_response: yield "message_data", response, data

            # retrieves the message value
            message_value = message.get_value()

            # retrieves the contents value for the current chunk
            contents_value = message_value[:octet_size]

            # writes the contents value in the contents (buffer)
            save_message and contents.write(contents_value)

            # resets the message (buffer)
            message.reset()

            # retrieves the partial message (extra contents message)
            partial_message = message_value[octet_end:]

            # writes the partial message in the message
            message.write(partial_message)

            # sets the partial data as the new message value
            message_value = partial_message

            # tries to find the octet end index
            octet_end_index = message_value.find("\r\n")

        # retrieves the contents value
        contents_value = contents.get_value()

        # sets the received message in the response
        response.received_message = contents_value

    def decode_response(self, response):
        """
        Decodes the response message for the encoding
        specified in the response.

        @type response: HttpResponse
        @param response: The response to be decoded.
        """

        # in case the content type charset is not defined
        # (no decoding should take place)
        if not self.content_type_charset:
            # returns immediately
            return

        # retrieves the received message value
        received_message_value = response.received_message

        # decodes the message value into unicode using the given charset
        received_message_value_decoded = received_message_value.decode(self.content_type_charset)

        # sets the decoded message value in the received message field
        response.received_message = received_message_value_decoded

    def set_authentication(self, username, password):
        """
        Sets the authentication values, to be used in the request.

        @type username: String
        @param username: The username to be used in the authentication.
        @type password: String
        @param password: The password to be used in the authentication.
        """

        # sets the authentication flag
        self.authentication = True

        # sets the authentication values
        self.username = username
        self.password = password

    def set_no_cache(self, no_cache):
        """
        Sets the value controlling the explicit invalidation
        of the cache in the http request.


        @type no_cache: bool
        @param no_cache: The value controlling the explicit invalidation
        of the cache in the http request.
        """

        # sets the no cache flag
        self.no_cache = no_cache

    def set_redirect(self, redirect):
        """
        Sets the value controlling the "auto" redirection to be
        used in the request.

        @type redirect: bool
        @param redirect: The value controlling the "auto" redirection to be
        used in the request.
        """

        # sets the redirect flag
        self.redirect = redirect

    def _generate_client_parameters(self, parameters):
        """
        Retrieves the client parameters map from the base parameters
        map.

        @type parameters: Dictionary
        @param parameters: The base parameters map to be used to build
        the final client parameters map.
        @rtype: Dictionary
        @return: The client service parameters map.
        """

        # creates the default parameters
        default_parameters = {
            "client_plugin" : self.main_client_http.main_client_http_plugin,
            "request_timeout" : REQUEST_TIMEOUT,
            "response_timeout" : RESPONSE_TIMEOUT
        }

        # creates the parameters map, from the default parameters
        parameters = colony.libs.map_util.map_extend(parameters, default_parameters, False)

        # returns the parameters
        return parameters

    def _parse_url(self, url):
        """
        Parses the url, retrieving a tuple structure containing
        the protocol, the username, the password, the host, the port,
        the path, the base url and the options map for the given url.

        @type url: String
        @param url: The url to be parsed.
        @rtype: Tuple
        @return: A tuple containing the protocol, the username, the password
        the host, the port, the path, the base url and the options map.
        """

        # retrieves the url parser plugin
        url_parser_plugin = self.main_client_http.main_client_http_plugin.url_parser_plugin

        # parses the url retrieving the structure
        url_structure = url_parser_plugin.parse_url(url)

        # in case the url structure contains the protocol
        if url_structure.protocol:
            # converts the protocol to lower case
            protocol = url_structure.protocol.lower()
        else:
            # raises the http invalid url data exception
            raise main_client_http_exceptions.HttpInvalidUrlData("missing protocol information: " + url)

        # in case the url structure contains the protocol
        if url_structure.username and url_structure.password:
            # retrieves the username
            username = url_structure.username

            # retrieves the password
            password = url_structure.password
        else:
            # sets the username as invalid (not set)
            username = None

            # sets the password as invalid (not set)
            password = None

        # in case the url structure contains the base name
        if url_structure.base_name:
            # retrieves the base name as the host
            host = url_structure.base_name
        else:
            # raises the http invalid url data exception
            raise main_client_http_exceptions.HttpInvalidUrlData("missing host information: " + url)

        # in case the url structure contains the port
        if url_structure.port:
            # retrieves the port
            port = url_structure.port
        else:
            # sets the port retrieving it from the default port map
            port = PROTOCOL_DEFAULT_PORT_MAP.get(protocol, None)

        # in case the url structure contains the resource reference
        if url_structure.resource_reference:
            # retrieves the resource reference as the path
            path = url_structure.resource_reference
        else:
            # sets the default path (root)
            path = "/"

        # in case the url structure contains the base url
        if url_structure.base_url:
            # retrieves the base url
            base_url = url_structure.base_url
        else:
            # sets the base url as invalid
            base_url = None

        # in case the url structure contains the options map
        if url_structure.options_map:
            # retrieves the options map
            options_map = url_structure.options_map
        else:
            # sets the options map as empty
            options_map = {}

        # returns the tuple containing the protocol, the username,
        # the password, the host, the port, the path, the base url
        # and the options map
        return (
            protocol,
            username,
            password,
            host,
            port,
            path,
            base_url,
            options_map
        )

    def _process_redirection(self, request, response):
        """
        Processes the redirection part of the response,
        retrieving the new response in case there is a
        redirection defined.

        @type request: HttpRequest
        @param request: The http request to be used in
        the processing.
        @type response: HttpResponse
        @param response: The http response to be used in
        the processing.
        @rtype: HttpResponse
        @return: The http response resulting from the
        redirection (or none if not redirected).
        """

        # retrieves the main client http plugin
        main_client_http_plugin = self.main_client_http.main_client_http_plugin

        # in case the location value is not set in the response header
        if not LOCATION_VALUE in response.headers_map:
            # returns invalid
            return None

        # retrieves the location
        location = response.headers_map[LOCATION_VALUE]

        # decodes the location using the default url charset
        location = location.decode(DEFAULT_URL_CHARSET)

        # retrieves the url of the request
        request_url = request.url

        # retrieves the status code
        status_code = response.status_code

        # in case the location does not start with the http prefix
        # it's not an absolute path but a relative one
        if not location.startswith(HTTP_PREFIX_VALUE) and not location.startswith(HTTPS_PREFIX_VALUE):
            # in case the location starts with the slash value
            # the address refers to a base address
            if location.startswith("/"):
                # retrieves the base url of the request
                request_base_url = request.base_url

                # creates the "absolute" location value
                location = request_base_url + location
            # the address is relative to the current one
            else:
                # retrieves the request base url (without the last token)
                request_url = request_url.rsplit("/", 1)[0]

                # sets the "relative" location value
                location = request_url + "/" + location

        # in case the location is not the same, the status code is
        # of type redirect and the redirect flag is set
        if not location == request_url and status_code in REDIRECT_STATUS_CODES and self.redirect:
            # prints a debug message
            main_client_http_plugin.debug("Redirecting request to '%s'" % location)

            # retrieves the request headers
            request_headers = request.headers_map

            # returns the "new" fetched url (redirection)
            return self.fetch_url(location, GET_METHOD_VALUE, headers = request_headers)

        # returns invalid
        return None

    def _status_code_no_message_body(self, status_code_integer):
        """
        Tests if the given status code (integer) refers
        to a response with no message body contents.

        @type status_code_integer: int
        @param status_code_integer: The status code (integer)
        to be tested.
        @rtype: bool
        @return: If the given status code (integer) refers
        to a response with no message body contents.
        """

        return (status_code_integer >= 100 and status_code_integer < 200) or status_code_integer in UNDEFINED_CONTENT_LENGTH_STATUS_CODES

    def _call_handler(self, event_name, handlers_map, response):
        """
        Calls an handler for the given event name and
        using the given map of handlers (methods).
        For the calling of this type of handler only the
        response is passed as argument.

        @type event_name: String
        @param event_name: The name of the event to be used
        to call the handler.
        @type handlers_map: Dictionary
        @param handlers_map: The map of handlers to be used in
        the calling of the handler.
        @type response: HttpResponse
        @param response: The response object to be passed as argument
        to the handler.
        """

        # tries to retrieve the handler method from the
        # handlers map, for the given event name
        handler_method = handlers_map.get(event_name, None)

        # in case the handler method is not defined
        if not handler_method:
            # returns immediately
            return

        # calls the handler method with the response
        # as first argument
        handler_method(response)

    def _call_handler_data(self, handler_name, handlers_map, response, data):
        """
        Calls an handler for the given event name and
        using the given map of handlers (methods).
        For the calling of this type of handler both the
        response and the data are passed as arguments.

        @type event_name: String
        @param event_name: The name of the event to be used
        to call the handler.
        @type handlers_map: Dictionary
        @param handlers_map: The map of handlers to be used in
        the calling of the handler.
        @type response: HttpResponse
        @param response: The response object to be passed as argument
        to the handler.
        @type data: String
        @param data: The data to be to be passed as argument
        to the handler.
        """

        # tries to retrieve the handler method from the
        # handlers map, for the given event name
        handler_method = handlers_map.get(handler_name, None)

        # in case the handler method is not defined
        if not handler_method:
            # returns immediately
            return

        # calls the handler method with the response
        # as first argument and the data as second
        handler_method(response, data)

class HttpRequest:
    """
    The http request class.
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

    authentication = False
    """ The authentication flag """

    username = "none"
    """ The username of the authentication """

    password = "none"
    """ The password of the authentication """

    authentication_token = "none"
    """ The authentication used in authentication """

    no_cache = False
    """ The no cache flag """

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

    encode_path = False
    """ The encode path """

    url = None
    """ The complete url """

    base_url = None
    """ The base url """

    content_length = None
    """ The content length """

    def __init__(self, host = "none", port = None, path = "none", attributes_map = {}, operation_type = GET_METHOD_VALUE, headers_map = {}, protocol_version = HTTP_1_1_VERSION, content_type = DEFAULT_CONTENT_TYPE, content_type_charset = DEFAULT_CHARSET, encode_path = False, url = None, base_url = None):
        """
        Constructor of the class.

        @type host: String
        @param host: The host value.
        @type port: int
        @param port: The port value.
        @type path: String
        @param path: The path.
        @type attributes_map: Dictionary
        @param attributes_map: The attributes map.
        @type operation_type: String
        @param operation_type: The operation type.
        @type headers_map: Dictionary
        @param headers_map: The headers map.
        @type protocol_version: String
        @param protocol_version: The protocol version.
        @type content_type: String
        @param content_type: The content type.
        @type content_type_charset: String
        @param content_type_charset: The content type charset.
        @type encode_path: bool
        @param encode_path: If the path should be encoded.
        @type url: String
        @param url: The complete url.
        @type base_url: String
        @param base_url: The base url.
        """

        self.host = host
        self.port = port
        self.path = path
        self.attributes_map = attributes_map
        self.operation_type = operation_type
        self.headers_map = headers_map
        self.protocol_version = protocol_version
        self.content_type = content_type
        self.content_type_charset = content_type_charset
        self.encode_path = encode_path
        self.url = url
        self.base_url = base_url

        self.message_stream = colony.libs.string_buffer_util.StringBuffer()

    def write(self, message, flush = 1, encode = True):
        # retrieves the message type
        message_type = type(message)

        # in case the message type is unicode
        if message_type == types.UnicodeType and encode:
            # encodes the message with the defined content type charset
            message = message.encode(self.content_type_charset)

        # writes the message to the message stream
        self.message_stream.write(message)

    def flush(self):
        pass

    def get_result(self):
        """
        Retrieves the result string (serialized) value of
        the request.

        @rtype: String
        @return: The result string (serialized) value of
        the request.
        """

        # validates the current request
        self.validate()

        # retrieves the result stream
        result = colony.libs.string_buffer_util.StringBuffer()

        # encodes the path if required
        path = self.encode_path and self._encode_path() or self._encode(self.path)

        # encodes the attributes
        encoded_attributes = self._encode_attributes()

        # in case the encoded attributes string
        # is valid and not empty
        if encoded_attributes:
            # in case the operation is of type get
            if self.operation_type == GET_METHOD_VALUE:
                # in case no exclamation mark exists in
                # the path
                if self.path.find("?") == -1:
                    path = path + "?" + encoded_attributes
                else:
                    path = path + "&" + encoded_attributes
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
        self.content_length = len(message)

        # writes the http command in the string buffer (version, status code and status value)
        result.write(self.operation_type + " " + path + " " + self.protocol_version + "\r\n")

        # creates the ordered map to hold the header values
        headers_ordered_map = colony.libs.structures_util.OrderedMap()

        # in case there is a content type defined
        if self.content_type:
            headers_ordered_map[CONTENT_TYPE_VALUE] = self.content_type

        # in case the content length is valid
        if self.content_length > 0:
            headers_ordered_map[CONTENT_LENGTH_VALUE] = str(self.content_length)

        # in case authentication is set
        if self.authentication:
            headers_ordered_map[AUTHORIZATION_VALUE] = self.authentication_token

        # in case no cache is set
        if self.no_cache:
            headers_ordered_map[CACHE_CONTROL_VALUE] = NO_CACHE_VALUE

        # sets the base request header values
        headers_ordered_map[HOST_VALUE] = real_host
        headers_ordered_map[USER_AGENT_VALUE] = USER_AGENT_IDENTIFIER
        headers_ordered_map[KEEP_ALIVE_VALUE] = str(DEFAULT_KEEP_ALIVE_TIMEOUT)
        headers_ordered_map[CONNECTION_VALUE] = KEEP_ALIVE_VALUE

        # extends the headers ordered map with the headers map
        headers_ordered_map.extend(self.headers_map)

        # iterates over all the header values to be sent
        for header_name, header_value in headers_ordered_map.items():
            # writes the header value in the result
            result.write(header_name + ": " + header_value + "\r\n")

        # writes the end of the headers and the message
        # values into the result
        result.write("\r\n")
        result.write(message)

        # retrieves the value from the result buffer
        result_value = result.get_value()

        # returns the result value
        return result_value

    def validate(self):
        """
        Validates the current request, raising exception
        in case validation fails.
        """

        pass

    def set_authentication(self, username, password):
        """
        Sets the authentication values, to be used in the request.

        @type username: String
        @param username: The username to be used in the authentication.
        @type password: String
        @param password: The password to be used in the authentication.
        """

        # sets the authentication flag
        self.authentication = True

        # sets the authentication values
        self.username = username
        self.password = password

        # creates the authentication token encoding the username
        # and password in base 64
        self.authentication_token = BASIC_VALUE + " " + base64.b64encode(username + ":" + password)

    def get_no_cache(self, no_cache):
        """
        Retrieves the no cache value.

        @rtype: bool
        @return: The no cache value.
        """

        return self.no_cache

    def set_no_cache(self, no_cache):
        """
        Sets the no cache value.

        @type no_cache: bool
        @param no_cache: The no cache value.
        """

        self.no_cache = no_cache

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
            # sets the host appended with the port value
            host = self.host + ":" + str(self.port)
        # in case the port is not defined
        else:
            # sets only the host
            host = self.host

        # encodes the host value
        host_encoded = self._encode(host)

        # returns the host encoded
        return host_encoded

    def _encode_path(self):
        """
        Encodes the current path into the current encoding.

        @rtype: String
        @return: The encoded path string.
        """

        # encodes the path
        path_encoded = self._encode(self.path)

        # quotes the path
        path_quoted = colony.libs.quote_util.quote(path_encoded, "/")

        # returns the quoted path
        return path_quoted

    def _encode_attributes(self):
        """
        Encodes the current attributes into url encoding.

        @rtype: String
        @return: The encoded attributes string.
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
            attribute_key_quoted = colony.libs.quote_util.quote_plus(attribte_key_encoded)
            attribute_value_quoted = colony.libs.quote_util.quote_plus(attribte_value_encoded)

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

        # in case the content type charset is not defined
        # (no encoding should take place)
        if not self.content_type_charset:
            # returns the string value
            # (without encoding)
            return string_value

        # converts the string value to unicode
        unicode_value = unicode(string_value)

        # encodes the unicode value
        unicode_value_encoded =  unicode_value.encode(self.content_type_charset)

        # returns the encoded unicode value
        return unicode_value_encoded

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

    received_message = None
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
