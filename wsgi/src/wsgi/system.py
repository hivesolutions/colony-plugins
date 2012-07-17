#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types
import datetime

import colony.base.system

POWERED_BY_STRING = "colony/%s (%s)"
""" The string to be used in the powered by http
header to be sent to the end used as a sign of
the underlying infra-structure of wsgi """

PATH_INFO_PREFIX = "/dynamic/rest"
""" The prefix to be used at the start of the
path info so that every request uri is inserted
within this context (this way the uri is shorter) """

CHUNK_SIZE = 4096
""" The size (in bytes) of the message piece
to be retrieved from the message provider from
each iteration, if this value is too small the
overhead for sending may be a problem """

DEFAULT_CHARSET = "utf-8"
""" The default charset to be used by the request
this value is defined in such a way that all the
knows characters are able to be encoded """

class Wsgi(colony.base.system.System):
    """
    The wsgi class.
    """

    def handle(self, environ, start_response):
        # retrieves the reference to the currently executing
        # plugin manager to be used further ahead
        plugin_manager = self.plugin.manager

        # retrieves the reference to the rest plugin from the
        # upper level wsgi plugin
        rest_plugin = self.plugin.rest_plugin

        # retrieves the string based version of the currently
        # executing plugin manager, this value is going to be
        # used in the formating of the powered by string
        manager_version = plugin_manager.get_version()
        manager_environment = plugin_manager.get_environment()

        # sets the default status code value as success,
        # all the request are considered to be successful
        # unless otherwise is state (exception raised)
        code = 200

        # creates a new wsgi request object with the provided
        # environment map (this object should be able to "emulate"
        # the default rest request) then provides the rest plugin
        # with the request for handling, handling the resulting
        # data or setting the exception values
        request = WsgiRequest(environ)
        try: rest_plugin.handle_request(request)
        except BaseException, exception: code = 500; content = [str(exception)]
        else: code = request.status_code; content = request.message_buffer

        # sets the content type to be returned as the one provided
        # by the request or default to the basic one, then tries
        # to calculate the content length based on the size of the
        # various items present in the content sequence (list)
        content_type = request.content_type or "text/plain"
        content_length = sum([len(value) for value in content])

        # in case the request is mediated additional operations may
        # be taken to provide the compatibility layer, the content
        # sequence must be a generator function and the size must
        # be pre calculated
        if request.is_mediated():
            content_length = request.mediated_handler.get_size()
            content = request.mediate()

        # update the status line with the provided code value and then
        # creates the response headers list with the created values and
        # sends these values as the start response
        status = "%d OK" % code
        response_headers = [
            ("Content-Type", content_type),
            ("Content-Length", str(content_length)),
            ("X-Powered-By", POWERED_BY_STRING % (manager_version, manager_environment))
        ]
        start_response(status, response_headers)

        # returns the content sequence to the caller method so that is
        # possible to render the appropriate message to the client
        return content

class WsgiRequest:
    """
    Represents an http request to be handled
    in the wsgi context, this value may be
    used as a compatibility mock to the internal
    http request object and as such must comply
    with the same interface (protocol).
    """

    environ = {}
    """ The map containing the various environment
    variables defined in the wsgi specification as
    the input for processing a certain request """

    status_code = 200
    """ The status code for the http request, this
    is considered to be the valid (ok) status code
    by default (optimistic approach) """

    content_type = None
    """ The content type as a string that defined
    the content (response) to be returned from this
    request """

    operation_type = None
    """ The type of operation (http method) for the
    current request, this value should be capitalized
    so that an uniform version is used """

    uri = None
    """ The "partial" domain name relative part of
    the url that reference the resource """

    mediated = False
    """ Flag indicating if the current response is
    meant to be mediated (generator based) or is a
    single content buffer is used (default) """

    content_type_charset = None
    """ The content type charset that is going to be
    used to encode the underlying message buffer, this
    must contain a charset that is able to encode all
    the provided data otherwise exception will be raised
    by the writing methods """




    etag = None
    """ The etag """

    expiration_timestamp = None
    """ The expiration timestamp """

    last_modified_timestamp = None
    """ The last modified timestamp """



    message_buffer = []
    """ The list containing the message buffer to
    be returned as the contents for the response
    associated with this request, this value is not
    used in case the response is mediated"""

    def __init__(self, environ, content_type_charset = DEFAULT_CHARSET):
        # retrieves the "base" value from the environment
        # map so that the basic request values may be constructed
        # the value are used with default values
        request_method = environ.get("REQUEST_METHOD", "")
        path_info = environ.get("PATH_INFO", "")
        query_string = environ.get("QUERY_STRING", "")

        # creates the "final" path info value by adding
        # the "static" path info prefix to it, so that smaller
        # uri's may be used in wsgi
        path_info = PATH_INFO_PREFIX + path_info

        # sets the various default request values using the "calculated"
        # wsgi based values as reference
        self.environ = environ
        self.content_type_charset = content_type_charset
        self.operation_type = request_method
        self.uri = query_string and path_info + "?" + query_string or path_info

        # starts the "static" message buffer list as an empty
        # list, so that further values are appended
        self.message_buffer = []

    def get_header(self, header_name):
        # normalizes the header name into the uppercase
        # and underscore based version and then adds
        # the http prefix so that it becomes standard to
        # the wsgi specification, then uses it to retrieve
        # the value from the environment map
        header_name = header_name.upper()
        header_name = header_name.replace("-", "_")
        header_name = "HTTP_" + header_name
        return self.environ.get(header_name, None)

    def write(self, message, flush = 1, encode = True):
        # retrieves the message type and in case it's unicode
        # it must be encoded using the currently set encoding
        # then adds the resulting message into the message
        # buffer to be flushed into the connection
        message_type = type(message)
        if message_type == types.UnicodeType and encode:
            message = message.encode(self.content_type_charset)
        self.message_buffer.append(message)

    def flush(self):
        pass

    def allow_cookies(self):
        self.allow_cookies = True

    def deny_cookies(self):
        self.allow_cookies = False

    def is_mediated(self):
        return self.mediated

    def is_chunked_encoded(self):
        return self.chunked_encoding






    def get_etag(self):
        return self.etag

    def set_etag(self, etag):
        self.etag = etag

    def get_expiration_timestamp(self):
        return self.expiration_timestamp

    def set_expiration_timestamp(self, expiration_timestamp):
        self.expiration_timestamp = expiration_timestamp

    def get_last_modified_timestamp(self):
        return self.last_modified_timestamp

    def set_last_modified_timestamp(self, last_modified_timestamp):
        self.last_modified_timestamp = last_modified_timestamp




    def verify_resource_modification(self, modified_timestamp = None, etag_value = None):
        # retrieves the if modified header value and in case the
        # modified timestamp and if modified header are defined
        # the date time base modification check must be run
        if_modified_header = self.get_header("If-Modified-Since")
        if modified_timestamp and if_modified_header:
            try:
                # converts the if modified header value to date time and then
                # converts the modified timestamp to date time
                if_modified_header_data_time = datetime.datetime.strptime(
                    if_modified_header,
                    "%a, %d %b %Y %H:%M:%S GMT"
                )
                modified_date_time = datetime.datetime.fromtimestamp(modified_timestamp)

                # in case the modified date time is less or the same
                # as the if modified header date time (no modification)
                # must return false as there was no modification
                if modified_date_time <= if_modified_header_data_time: return False
            except:
                # prints a warning for not being able to check the modification date
                self.http_client_service_handler.service_plugin.warning("Problem while checking modification date")

        # retrieves the if none match value and in case it is
        # defined together with the etag value the etag based
        # checking must be performed
        if_none_match_header = self.get_header("If-None-Match")
        if etag_value and if_none_match_header:
            # in case the value of the if modified header is the same
            # as the etag value of the file (no modification) must
            # return false as there was no modification
            if if_modified_header == etag_value: return False

        # returns true (modified or no information for
        # modification test)
        return True



    def mediate(self):
        # iterates continuously, this generator should return
        # when the mediated handler returns no value, this should
        # represent that no more data is available
        while True:
            # retrieves a "chunk" from the mediated handler and
            # checks if it's valid in case it's not must return
            # the sequence control to the caller otherwise yield
            # the value to the iteration
            mediated_value = self.mediated_handler.get_chunk(CHUNK_SIZE)
            if not mediated_value: return
            else: yield mediated_value
