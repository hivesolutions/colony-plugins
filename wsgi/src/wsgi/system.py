#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import datetime
import threading
import traceback

import colony

from . import exceptions

POWERED_BY_STRING = "colony/%s (%s)"
""" The string to be used in the powered by HTTP
header to be sent to the end used as a sign of
the underlying infra-structure of WSGI """

IDENTIFIER_STRING = "Colony Framework / %s (%s)"
""" The template to be used for the string to be
returned in diagnostic messages like errors """

ALLOW_ORIGIN = "*"
""" The default value to be used in the "Access-Control-Allow-Origin"
header value, this should not be too restrictive """

ALLOW_HEADERS = "*, X-Requested-With"
""" The default value to be used in the "Access-Control-Allow-Headers"
header value, this should not be too restrictive """

ALLOW_METHODS = "GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS"
""" The default value to be used in the "Access-Control-Allow-Methods"
header value, this should not be too restrictive """

CONTENT_SECURITY = "default-src * ws://* wss://* data: blob:; script-src * 'unsafe-inline' 'unsafe-eval'; style-src * 'unsafe-inline';"
""" The default value to be used in the "Content-Security-Policy"
header value, this should not be too restrictive """

FRAME_OPTIONS = "SAMEORIGIN"
""" The value to be as the default/original for the "X-Frame-Options"
header, this should ensure that the same origin is always used when
trying to embed a dynamic content into a web page """

XSS_PROTECTION = "1; mode=block"
""" Value to be used as the original one for the "X-XSS-Protection"
header value, should provide a way of preventing XSS attach under the
internet explorer browser """

CONTENT_OPTIONS = "nosniff"
""" Default "X-Content-Type-Options" header value to be used to prevent
the sniffing of content type values, ensuring that the browser sticks to
value of content type provided by the server """

PATH_INFO_PREFIX = "/dynamic/rest"
""" The prefix to be used at the start of the
path info so that every request URI is inserted
within this context (this way the URI is shorter) """

CHUNK_SIZE = 4096
""" The size (in bytes) of the message piece
to be retrieved from the message provider from
each iteration, if this value is too small the
overhead for sending may be a problem """

DEFAULT_CHARSET = "utf-8"
""" The default charset to be used by the request
this value is defined in such a way that all the
knows characters are able to be encoded """

STATUS_MESSAGES = {
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
""" The status code messages map, that associates
the HTTP status code as an integer with the descriptive
value of the error (message) """

class WSGI(colony.System):
    """
    The WSGI class, responsible for the implementation
    of the colony side of the WSGI specification.

    :see: http://www.python.org/dev/peps/pep-0333/
    """

    def handle(
        self,
        environ,
        start_response,
        prefix = None,
        alias = None,
        rewrite = None
    ):
        # retrieves some of the configuration values that are
        # going to control the request handling behaviour
        secure_headers = colony.conf("WSGI_SECURE_HEADERS", True, cast = bool)
        allow_origin = colony.conf("WSGI_CORS", ALLOW_ORIGIN)
        allow_origin = colony.conf("WSGI_ALLOW_ORIGIN", allow_origin)
        allow_headers = colony.conf("WSGI_ALLOW_HEADERS", ALLOW_HEADERS)
        allow_methods = colony.conf("WSGI_ALLOW_METHODS", ALLOW_METHODS)
        content_security = colony.conf("WSGI_CONTENT_SECURITY", CONTENT_SECURITY)
        frame_options = colony.conf("WSGI_FRAME_OPTIONS", FRAME_OPTIONS)
        xss_protection = colony.conf("WSGI_XSS_PROTECTION", XSS_PROTECTION)
        content_options = colony.conf("WSGI_CONTENT_OPTIONS", CONTENT_OPTIONS)

        # retrieves the reference to the currently executing
        # plugin manager to be used further ahead
        plugin_manager = self.plugin.manager

        # retrieves the reference to the rest plugin from the
        # upper level WSGI plugin, this value may not be set
        # in case there was a problem in the manager loading
        rest_plugin = self.plugin.rest_plugin

        # retrieves the string based version of the currently
        # executing plugin manager, this value is going to be
        # used in the formating of the powered by string
        manager_version = plugin_manager.get_version()
        manager_environment = plugin_manager.get_environment()

        # sets the default status code value as success,
        # all the request are considered to be successful
        # unless otherwise is state (exception raised) note
        # that the status string is also defined as valid
        code = 200
        status = "OK"

        # creates a new WSGI request object with the provided
        # environment map (this object should be able to "emulate"
        # the default request) then provides the rest plugin
        # with the request for handling, handling the resulting
        # data or setting the exception values
        request = WSGIRequest(
            self,
            environ,
            prefix = prefix,
            alias = alias,
            rewrite = rewrite
        )
        try:
            rest_plugin.handle_request(request)
            request.finish()
        except Exception as exception:
            has_code = hasattr(exception, "status_code")
            code = exception.status_code if has_code else 500
            try: code = int(code)
            except Exception: code = 500
            status = "Not OK"
            message = self.error_message(exception, code = code)
            is_unicode = colony.legacy.is_unicode(message)
            if is_unicode: message = message.encode(request.content_type_charset)
            content = [message]
            headers_out_l = []
        else:
            code = request.status_code
            status = request.get_status_message()
            content = request.message_buffer
            headers_out = request.headers_out
            headers_out_l = colony.legacy.items(headers_out)

        # verifies if the current content to be handled is generator based
        # if that's the case special handling is required meaning for example
        # that the complete set of contents is considered to be the generator
        is_generator = content and colony.legacy.is_generator(content[0])
        if is_generator: content = content[0]

        # sets the content type to be returned as the one provided
        # by the request or defaults to the basic one, then tries
        # to calculate the content length based on the size of the
        # various items present in the content sequence (list)
        content_type = request.content_type or "text/plain"
        if is_generator: content_length = -1
        else: content_length = sum([len(value) for value in content])

        # in case the request is mediated additional operations may
        # be taken to provide the compatibility layer, the content
        # sequence must be a generator function and the size must
        # be pre calculated
        if request.is_mediated():
            content_length = request.mediated_handler.get_size()
            content = request.mediate()

        # creates the final runtime powered by string and ensures that
        # it's represented by a proper bytes string
        powered_by = colony.legacy.bytes(
            POWERED_BY_STRING % (manager_version, manager_environment),
            force = True
        )

        # update the status line with the provided code value and then
        # creates the initial/static response headers list with the
        # created values to be used as part of the initial response
        status = "%d %s" % (code, status)
        response_headers = [
            ("Content-Type", content_type),
            ("X-Powered-By", powered_by)
        ]

        # verifies if the provided content length value is considered
        # valid and if that's the case adds it's value as an header
        if not content_length == -1: response_headers.append(
            ("Content-Length", str(content_length))
        )

        # in case the secure headers flag is set, runs the setting operation
        # over the complete set of secure headers
        if secure_headers and allow_origin:
            response_headers.append(("Access-Control-Allow-Origin", allow_origin))
        if secure_headers and allow_headers:
            response_headers.append(("Access-Control-Allow-Headers", allow_headers))
        if secure_headers and allow_methods:
            response_headers.append(("Access-Control-Allow-Methods", allow_methods))
        if secure_headers and content_security:
            response_headers.append(("Content-Security-Policy", content_security))
        if secure_headers and frame_options:
            response_headers.append(("X-Frame-Options", frame_options))
        if secure_headers and xss_protection:
            response_headers.append(("X-XSS-Protection", xss_protection))
        if secure_headers and content_options:
            response_headers.append(("X-Content-Type-Options", content_options))

        # extends the current list of response headers with the list
        # retrieved from the request (headers out)
        response_headers.extend(headers_out_l)

        # runs the initial start response method, part of the WSGI spec
        # so that the proper initialization of the status code and the
        # headers is provided and the handling of the request started
        start_response(status, response_headers)

        # returns the content sequence to the caller method so that is
        # possible to render the appropriate message to the client
        return content

    def error_message(self, error, code = 500):
        """
        Formats the error as message and returns it so it can be
        used to notify the end user.

        The retrieved message is set as an undefined encoding string
        and may be used with care to avoid encoding problems.

        :type error: Exception
        :param error: The exception object to be used in the creation
        of the message string to be returned.
        :type code: int
        :param code: The HTTP status code that should be included in
        the created message default to internal error (500).
        :rtype: String
        :return: The constructed error message as a string that represents
        the error that was passed as an argument
        """

        # retrieves the plugin manager for the current system instance
        # and uses it to retrieve the current version and environment
        # to be used in the construction of the identifier string
        plugin_manager = self.plugin.manager
        version = plugin_manager.get_version()
        manager_environment = plugin_manager.get_environment()
        identifier_s = IDENTIFIER_STRING % (version, manager_environment)

        # verifies if the current (plugin) manager instance is
        # running under the development mode
        is_development = plugin_manager.is_development()

        # converts the error into a string bases and then creates the
        # complete error message string from the various components,
        # returning the resulting value as the result
        error_s = str(error)
        message = "[%d] %s\n%s\n" % (code, error_s, identifier_s)
        if not is_development: return message
        trace = "\n".join(self.stacktrace_message())
        message += "\n%s\n" % trace
        return message

    def stacktrace_message(self):
        """
        Retrieves/yields the contents of the stack trace associated with
        an exception raised under the current context.

        This method returns a generator and proper usage methods should
        be used to avoid miss-usage.

        :rtype: Generator
        :return: The sequence containing the the various values/lines of
        the stack trace associated with the current context.
        """

        # retrieves the complete set of lines for the exception stack trace
        # and iterates over them to yield the value of them to the caller
        # method (a lazy loaded approach is used to reduce usage)
        lines = traceback.format_exc().splitlines()
        for line in lines: yield line

class WSGIRequest(object):
    """
    Represents an HTTP request to be handled
    in the WSGI context, this value may be
    used as a compatibility mock to the internal
    HTTP request object and as such must comply
    with the same interface (protocol).
    """

    service = None
    """ The service instance associated with the request
    this should be the owner of this request and any
    external object access should be done through this """

    environ = {}
    """ The map containing the various environment
    variables defined in the WSGI specification as
    the input for processing a certain request """

    status_code = 200
    """ The status code for the HTTP request, this
    is considered to be the valid (OK) status code
    by default (optimistic approach) """

    status_message = None
    """ The message that is going to be sent after the
    status code as part of the HTTP request, by default
    no value is set and the message is instead inferred
    from the status code """

    content_type = None
    """ The content type as a string that defined
    the content (response) to be returned from this
    request """

    operation_type = None
    """ The type of operation (HTTP method) for the
    current request, this value should be capitalized
    so that an uniform version is used """

    path = None
    """ The (URL) path created by joining the joining
    the prefix value and the provided path info, this
    is the virtual value to be used by colony """

    original_path = None
    """ The original path, without unquoting resulting
    from the joining from both info part of the path
    and the query string, this path should reflect the
    value provided by the server and not the virtual one """

    uri = None
    """ The "partial" domain name relative part of
    the URL that reference the resource """

    query_string = None
    """ The string containing the query part of the URL
    that may be parsed for arguments """

    arguments = None
    """ The arguments part of the query or post data if
    it's an URL encoded value """

    multipart = None
    """ The multipart string value (contents) of a message
    that is meant to parsed in multiple contexts (parts) """

    attributes_map = {}
    """ The map containing the various attributes resulting
    from the parsing of the URL encoded part of the get parameters
    or from the content of a post message """

    headers_out = {}
    """ The map that hold the set of headers to be sent
    to the client (output headers) indexed by name and
    associated with the value for them  """

    received_message = None
    """ The complete linear buffer containing the set of data
    sent by the client as the payload of the request """

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

    max_age = None
    """ The maximum age value in seconds to be used to
    control the client side cache of the returned resource,
    use this value carefully to avoid mismatches in cache """

    etag = None
    """ The etag representing the file in an unique
    way to, usually through an hash function  """

    expiration_timestamp = None
    """ The expiration timestamp for the current request
    to be send for the client side cache control """

    last_modified_timestamp = None
    """ The last modified timestamp for the current request
    to be send for the client side cache control """

    message_buffer = []
    """ The list containing the message buffer to
    be returned as the contents for the response
    associated with this request, this value is not
    used in case the response is mediated"""

    def __init__(
        self,
        service,
        environ,
        content_type_charset = DEFAULT_CHARSET,
        prefix = None,
        alias = None,
        rewrite = None
    ):
        # sets the current "owner" service of the request
        # in the current request, this is going to be used
        # to access external resources
        self.service = service

        # retrieves the "base" value from the environment
        # map so that the basic request values may be constructed
        # the value are used with default values
        request_method = environ.get("REQUEST_METHOD", "")
        script_name = environ.get("SCRIPT_NAME", "")
        path_info = environ.get("PATH_INFO", "")
        query_string = environ.get("QUERY_STRING", "")
        content_type = environ.get("CONTENT_TYPE", "")
        content_length = int(environ.get("CONTENT_LENGTH", "") or 0)
        input = environ.get("wsgi.input", None)

        # resolves the provided path information so that if any alias
        # value matches the start of the path info it's replaced by
        # the correct matching value
        path_info_r = self._resolve_path(path_info, alias)

        # creates the "final" path info (resolved) value by adding
        # the "static" path info prefix to it, so that smaller
        # URI's may be used in WSGI, in case the "extra" prefix variable
        # is set an "extra" prefix is prepended to the path info
        if prefix: path_info_r = PATH_INFO_PREFIX + prefix + path_info_r
        else: path_info_r = PATH_INFO_PREFIX + path_info_r

        # creates the complete "original" path info value by adding
        # the script name (routing base value) to the path info, this
        # value may be used internally as the original (path) value
        path_info_o = script_name + path_info if script_name else path_info

        # runs the shorten operation on the original so that the stored
        # value may be shorter than the original allowing proper absolute
        # resolution even under complex proxy based configurations
        path_info_o = self._shorten_path(path_info_o, rewrite)

        # sets the various default request values using the "calculated"
        # WSGI based values as reference
        self.environ = environ
        self.content_type_charset = content_type_charset
        self.operation_type = request_method
        self.uri = path_info_r
        self.path = path_info_r + "?" + query_string if query_string else path_info_r
        self.original_path = path_info_o + "?" + query_string if query_string else path_info_o

        # starts the map that will hold the various attributes
        # resulting from the parsing of the request
        self.attributes_map = colony.OrderedMap(True)

        # creates the map that will hold the various headers to
        # sent to the client (output headers)
        self.headers_out = {}

        # starts the "static" message buffer list as an empty
        # list, so that further values are appended
        self.message_buffer = []

        # in case the input object is defined reads the complete
        # set of contents from it and sets it as the received
        # message (eager loading of the contents)
        self.received_message = input and input.read(content_length)

        # parses the get attributes so that the corresponding map
        # is populated with the arguments, preserving their order
        self.__parse_get_attributes__()

        # in case the content type of the request is form urlencoded
        # must parse and process the post attributes
        if content_type.startswith("application/x-www-form-urlencoded"):
            self.parse_post_attributes()

        # in case the content type of the request is multipart form data
        # must parse and process the post multipart
        elif content_type.startswith("multipart/form-data"):
            self.parse_post_multipart()

    def __getattributes__(self, attribute_name, default = None):
        """
        Retrieves the attribute from the attributes map.

        :type attribute_name: String
        :param attribute_name: The name of the attribute to retrieve.
        :type default: Object
        :param default: The default object value to be returned in
        case the attribute is not found.
        :rtype: Object
        :return: The retrieved attribute.
        """

        return self.attributes_map.get(attribute_name, default)

    def __setattributes__(self, attribute_name, attribute_value):
        """
        Sets the given attribute in the request. The referenced
        attribute is the HTTP request attribute and the setting takes
        into account a possible duplication of the values.

        :type attribute_name: String
        :param attribute_name: The name of the attribute to be set.
        :type attribute_value: Object
        :param attribute_value: The value of the attribute to be set.
        """

        # in case the attribute name is already defined
        # in the attributes map (duplicated reference), it
        # requires a list structure to be used
        if attribute_name in self.attributes_map:
            # retrieves the attribute value reference from the attributes map
            attribute_value_reference = self.attributes_map[attribute_name]

            # retrieves the attribute value reference type
            attribute_value_reference_type = type(attribute_value_reference)

            # in case the attribute value reference type is (already)
            # a list
            if attribute_value_reference_type == list:
                # adds the attribute value to the attribute value reference
                attribute_value_reference.append(attribute_value)
            # otherwise the attributes is not a list and it must be created
            # for the first time
            else:
                # sets the list with the previously defined attribute reference
                # and the attribute value
                self.attributes_map[attribute_name] = [
                    attribute_value_reference,
                    attribute_value
                ]
        # otherwise the attribute is not defined and a normal
        # set must be performed (single and simple set)
        else:
            # sets the attribute value in the attributes map
            self.attributes_map[attribute_name] = attribute_value

    def __parse_get_attributes__(self):
        # splits the (original) path to get the attributes path of
        # the request and retrieves the length of this result
        path_splitted = self.original_path.split("?")
        path_splitted_length = len(path_splitted)

        # in case there are no arguments to be parsed
        if path_splitted_length < 2: return

        # retrieves the query string from the path splitted
        # and sets the arguments values as the query string
        # then uses these arguments for parsing
        self.query_string = path_splitted[1]
        self.arguments = self.query_string
        self.parse_arguments()

    def finish(self):
        """
        Finishes the current request running the final set
        of validations in the request so that it remains
        valid for the current set of standards.

        This is also the method that sets the default values
        in the request in case they were not set during the
        normal handling workflow.
        """

        if not "Cache-Control" in self.headers_out:
            self.headers_out["Cache-Control"] = "no-cache, must-revalidate"

    def parse_post_attributes(self):
        """
        Parses the post attributes from the standard post
        syntax. This call should only be made in case the
        received message contains an urlencoded value.
        """

        # sets the arguments as the received message
        # and then uses this attribute to parse them
        self.arguments = colony.legacy.str(self.received_message)
        self.parse_arguments()

    def parse_post_multipart(self):
        """
        Parses the post multipart from the standard post
        syntax. This call should only be made in case the
        received message contains an multipart value.
        """

        # sets the multipart as the received message
        # and then uses this attribute to parse them
        self.multipart = self.received_message
        self.parse_multipart()

    def parse_arguments(self):
        """
        Parses the arguments, using the currently defined
        arguments string (in the request).
        The parsing of the arguments is based in the default get
        arguments parsing.
        """

        # retrieves the attribute fields list
        attribute_fields_list = self.arguments.split("&")

        # iterates over all the attribute fields
        for attribute_field in attribute_fields_list:
            # splits the attribute field in the equals operator
            # and retrieves the length of the result for processing
            attribute_field_splitted = attribute_field.split("=", 1)
            attribute_field_splitted_length = len(attribute_field_splitted)

            # in case the attribute field splitted length is invalid,
            # must continue the loop (invalid value)
            if attribute_field_splitted_length == 0 or attribute_field_splitted_length > 2:
                continue

            # in case the attribute field splitted length is two, this
            # refers a valid (normal) key and value attribute
            if attribute_field_splitted_length == 2:
                # retrieves the attribute name and the attribute value,
                # from the attribute field splitted, then "unquotes" the
                # attribute value from the URL encoding
                attribute_name, attribute_value = attribute_field_splitted
                attribute_value = colony.unquote_plus(attribute_value)

            # in case the attribute field splitted length is one, this refers
            # a valid single key attribute (with an unset value)
            elif attribute_field_splitted_length == 1:
                # retrieves the attribute name, from the attribute field splitted
                # and sets the value as invalid (not set)
                attribute_name, = attribute_field_splitted
                attribute_value = None

            # "unquotes" the attribute name from the URL encoding and sets
            # the attribute for the current name in the current instance
            attribute_name = colony.unquote_plus(attribute_name)
            self.__setattributes__(attribute_name, attribute_value)

    def parse_multipart(self):
        """
        Parses the multipart using the currently defined multipart value.
        The processing of multipart is done according the standard
        specifications and RFQs.

        :see: http://en.wikipedia.org/wiki/MIME
        """

        # retrieves the content type header
        content_type = self.get_header("Content-Type")

        # in case no content type is defined
        if not content_type:
            # raises the HTTP invalid multipart request exception
            raise exceptions.WSGIRuntimeException(
                "no content type defined"
            )

        # splits the content type and then strips the first
        # value of it from any "extra" character
        content_type_splitted = content_type.split(";")
        content_type_value = content_type_splitted[0].strip()

        # in case the content type value is not valid raises an
        # exception indicating the error
        if not content_type_value == "multipart/form-data":
            raise exceptions.WSGIRuntimeException(
                "invalid content type defined: " + content_type_value
            )

        # retrieves the boundary value and then splits it
        # into the appropriate values (around the separator
        # token for the boundary key and value)
        boundary = content_type_splitted[1].strip()
        boundary_splitted = boundary.split("=")

        # in case the length of the boundary is not two (invalid)
        # this is considered invalid and an exception is raised
        if not len(boundary_splitted) == 2:
            raise exceptions.WSGIRuntimeException(
                "invalid boundary value: " + boundary
            )

        # retrieves (unpacks) the boundary reference and the boundary value
        # and retrieves the length of the boundary value
        _boundary, boundary_value = boundary_splitted
        boundary_value_length = len(boundary_value)

        # ensures that the boundary value is properly converted into the
        # base bytes based representation (required for search)
        boundary_value = colony.legacy.bytes(boundary_value)

        # sets the initial index as the as the boundary value length
        # plus the base boundary value of two (equivalent to: --)
        current_index = boundary_value_length + 2

        # iterates indefinitely for the parsing of the various content
        # parts, and setting the attributes in the current request
        while True:
            # retrieves the end index (boundary start index)
            end_index = self.multipart.find(boundary_value, current_index)

            # in case the end index is invalid (end of multipart)
            # must break the loop
            if end_index == -1: break

            # parses the multipart part retrieving the headers map and the contents
            # the sent indexes avoid the extra newline values incrementing and decrementing
            # the value of two at the end and start
            headers_map, contents = self._parse_multipart_part(current_index + 2, end_index - 2)

            # parses the content disposition header retrieving the content
            # disposition map and list (with the attributes order) then
            # sets the contents in the content disposition map and retrieves
            # the name from the content disposition map
            content_disposition_map = self._parse_content_disposition(headers_map)
            content_disposition_map["contents"] = contents
            name = content_disposition_map["name"]

            # sets the attribute attribute in the current request and
            # then sets the current index as the end index
            self.__setattributes__(name, content_disposition_map)
            current_index = end_index + boundary_value_length

    def get_header(self, header_name):
        # normalizes the header name into the uppercase
        # and underscore based version and then adds
        # the HTTP prefix so that it becomes standard to
        # the WSGI specification, then uses it to retrieve
        # the value from the environment map
        header_name = header_name.upper()
        header_name = header_name.replace("-", "_")
        header_name_b = "HTTP_" + header_name
        header = self.environ.get(header_name, None)
        return self.environ.get(header_name_b, header)

    def set_header(self, header_name, header_value, encode = True):
        """
        Set a response header value on the request.
        The header that is set is sent to the client after
        the request handling.

        :type header_name: String
        :param header_name: The name of the header to be set.
        :type header_value: Object
        :param header_value: The value of the header to be sent
        in the response.
        :type encode: bool
        :param encode: If the header value should be encoded in
        case the type is unicode.
        """

        # retrieves the header value type
        header_value_type = type(header_value)

        # in case the header value type is unicode
        # and the encode flag is set must encode the
        # header value using the current encoding
        if header_value_type == colony.legacy.UNICODE and encode:
            header_value = header_value.encode(self.content_type_charset)

        # converts the header value string into a compatible
        # string (according to all versions of python) so that
        # an unicode is used instead for python 3
        header_value = colony.legacy.str(header_value)

        # sets the header value in the headers map so that
        # any further access to the map will reflect the change
        self.headers_out[header_name] = header_value

    def append_header(self, header_name, header_value):
        """
        Appends an header value to a response header.
        This method calls the set header method in case the
        header is not yet defined.

        :type header_name: String
        :param header_name: The name of the header to be appended
        with the value.
        :type header_value: Object
        :param header_value: The value of the header to be appended
        in the response.
        """

        # in case the header is already defined
        if header_name in self.headers_out:
            # retrieves the current header value and then creates the
            # final header value as the appending of both the current
            # and the concatenation value
            current_header_value = self.headers_out[header_name]
            final_header_value = current_header_value + header_value
        else:
            # sets the final header value as the header value
            final_header_value = header_value

        # sets the final header value
        self.set_header(header_name, final_header_value)

    def read(self):
        """
        Reads the complete set of data present in the current
        current request, this call may bloc the control (in a
        blocking service).

        :rtype: String
        :return: The buffer containing the full data (message body)
        for the current request.
        """

        return self.received_message

    def write(self, message, flush = 1, encode = True):
        # retrieves the message type and in case it's unicode
        # it must be encoded using the currently set encoding
        # then adds the resulting message into the message
        # buffer to be flushed into the connection
        message_type = type(message)
        if message_type == colony.legacy.UNICODE and encode:
            message = message.encode(self.content_type_charset)
        self.message_buffer.append(message)

    def execute_background(self, callable, retries = 0, timeout = 0.0, timestamp = None):
        """
        Executes the given callable object in a background
        thread, avoiding the blocking of the current thread.
        This method is useful for avoid blocking the request
        handling method in non critic tasks.

        :type callable: Callable
        :param callable: The callable to be called in background.
        :type retries: int
        :param retries: The number of times to retry executing the
        callable in case exception is raised.
        :type timeout: float
        :param timeout: The time to be set in between calls of the
        callable, used together with the retry value.
        :type timestamp: float
        :param timestamp: The unix second based timestamp for the
        first execution of the callable.
        """

        self._execute_background_thread(
            callable,
            retries = retries,
            timeout = timeout,
            timestamp = timestamp
        )

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

    def is_secure(self):
        """
        Checks if the current request is being transmitted over a secure
        channel, the verification is made at a connection abstraction
        level (down socket verification).

        :rtype: bool
        :return: If the current request is being transmitted over a secure
        channel (secure request).
        """

        # retrieves the URL scheme for the current request and returns
        # the result of the comparison of it against the secure scheme
        url_scheme = self.environ.get("wsgi.url_scheme", None)
        return url_scheme == "https"

    def get_attributes_list(self):
        """
        Retrieves the list of attribute names in the
        current attributes map.

        :rtype: List
        :return: The list of attribute names in the
        current attributes map.
        """

        return colony.legacy.keys(self.attributes_map)

    def get_attribute(self, attribute_name, default = None):
        return self.__getattributes__(attribute_name, default)

    def set_attribute(self, attribute_name, attribute_value):
        self.__setattributes__(attribute_name, attribute_value)

    def get_operation_type(self):
        return self.operation_type

    def set_operation_type(self, operation_type):
        self.operation_type = operation_type

    def get_method(self):
        """
        Retrieves the method used in the current request
        object for the current request.
        This method is an alias to the retrieval of the
        operation type.

        :rtype: String
        :return: The method used in the current request
        context.
        """

        return self.get_operation_type()

    def get_max_age(self):
        return self.max_age

    def set_max_age(self, max_age):
        self.max_age = max_age
        self.headers_out["Cache-Control"] = "max-age=%d" % max_age

    def get_etag(self):
        return self.etag

    def set_etag(self, etag):
        self.etag = etag
        self.headers_out["ETag"] = etag

    def get_expiration_timestamp(self):
        return self.expiration_timestamp

    def set_expiration_timestamp(self, expiration_timestamp):
        self.expiration_timestamp = expiration_timestamp

    def get_last_modified_timestamp(self):
        return self.last_modified_timestamp

    def set_last_modified_timestamp(self, last_modified_timestamp):
        self.last_modified_timestamp = last_modified_timestamp
        last_modified = datetime.datetime.fromtimestamp(self.last_modified_timestamp)
        last_modified_f = last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.headers_out["Last-Modified"] = last_modified_f

    def get_status_message(self):
        """
        Retrieves the current status message value.
        The method returns the defined status message value,
        or the default in case none is defined.

        :rtype: String
        :return: The status message as the string that
        describes the currently defined status code.
        """

        if self.status_message:
            return self.status_message
        else:
            return STATUS_MESSAGES.get(self.status_code, "Invalid")

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
            except Exception:
                # prints a warning for not being able to check the modification date
                self.service.plugin.warning("Problem while checking modification date")

        # retrieves the if none match value and in case it is
        # defined together with the etag value the etag based
        # checking must be performed
        if_none_match_header = self.get_header("If-None-Match")
        if etag_value and if_none_match_header:
            # in case the value of the if none match header is the same
            # as the etag value of the file (no modification) must
            # return false as there was no modification
            if if_none_match_header == etag_value: return False

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

    def _resolve_path(self, path_info, alias, separator = "/"):
        """
        Resolves the provided path info string using the provided
        alias list, if there's a match at beginning of the string in
        the path info the value is replaced.

        If the separator string is set then the `/` separator is ensured
        to be present in between the matching and the next token, this is
        considered the default alias resolution behaviour.

        :type path_info: String
        :param path_info: The path information string containing the
        path to be resolved using the alias list.
        :type alias: List
        :param alias: The list containing prefix to resolution values
        associations that will be used in the resolution.
        :type separator: String
        :param separator: The separator to be ensured to be present
        in between the matching alias token and the remainder string.
        :rtype: String
        :return: The resolved path string resulting from the resolution
        of the path info string according to the provided list.
        """

        # in case the alias list is not valid or is not set the value
        # could not be resolved and the original path info is returned
        if not alias: return path_info

        # iterates over all the alias keys present in the list of alias
        # to try to find one that matches the start of the path info
        # in case it does happen the value is replaced
        for key, value in alias:
            if not path_info.startswith(key): continue
            if separator and not len(path_info) == len(key) and\
               not path_info[len(key)] == separator: continue
            key_l = len(key)
            path_info = value + path_info[key_l:]
            break

        # returns the "new" path info string object resulting from the
        # correct resolution of it's prefix value
        return path_info

    def _shorten_path(self, path_info, rewrite):
        """
        Shortens the provided path info value by removing any prefix
        that is defined under the provided rewrite list.

        The prefix is then replaced by the associated tuple item
        value, considered to be the original prefix.

        This operation is especially useful for scenarios of proxy
        based configurations where the front-end server root path
        points to a sub-path on the back-end server.

        :type path_info: String
        :param path_info: The path information string containing the
        path to be shortened using the rewrite list.
        :type rewrite: List
        :param rewrite: The list containing prefix to target value
        association to be used in the shortening operations.
        :rtype: String
        :return: The shortened path string resulting from the shortening
        of the path info string according to the provided list.
        """

        # in case the provided list of rewrite tuples is not valid or
        # is empty the path info is returned with no changes applied
        if not rewrite: return path_info

        # iterates over the complete set of rewrite tuples and verifies
        # if the current path info value start with the prefix and if
        # that the case removed such prefix from the path and prepends
        # the requested suffix instead
        for key, value in rewrite:
            if not path_info.startswith(key): continue
            key_l = len(key)
            path_info = value + path_info[key_l:]
            break

        # returns the "final" path info string value with the proper
        # shortening operation applied (reduced value)
        return path_info

    def _parse_multipart_part(self, start_index, end_index):
        """
        Parses a "part" of the whole multipart content bases on the
        interval of send indexes.

        :type start_index: int
        :param start_index: The start index of the "part" to be processed.
        :type end_index: int
        :param end_index: The end index of the "part" to be processed.
        :rtype: Tuple
        :return: A tuple with a map of headers for the "part" and the
        content of the "part", note that the headers value ios going to be
        decoded using the default/set encoding (or content type).
        """

        # creates the headers map, that is going to be populated with
        # the complete set of headers for the current part
        headers_map = {}

        # retrieves the end header index and uses it to retrieve
        # the headers (string) from the multipart then splits it
        # "around" the several lines contained in it
        end_header_index = self.multipart.find(b"\r\n\r\n", start_index, end_index)
        headers = self.multipart[start_index:end_header_index]
        headers_splitted = headers.split(b"\r\n")

        # iterates over the headers lines to process their header
        # values (key and value pairs)
        for header_splitted in headers_splitted:
            # finds the header separator
            division_index = header_splitted.find(b":")

            # retrieves the header name and value from the
            # splitted value and then sets both of them in
            # the headers map (as expected by specification)
            header_name = header_splitted[:division_index].strip()
            header_value = header_splitted[division_index + 1:].strip()
            header_name = header_name.decode(self.content_type_charset)
            header_value = header_value.decode(self.content_type_charset)
            headers_map[header_name] = header_value

        # retrieves the contents from the multipart then uses them
        # to return the headers map and the contents as a tuple
        contents = self.multipart[end_header_index + 4:end_index - 2]
        return (headers_map, contents)

    def _parse_content_disposition(self, headers_map):
        """
        Parses the content disposition value from the headers map.
        This method returns a map containing associations of key and value
        of the various content disposition values.

        :type headers_map: Dictionary
        :param headers_map: The map containing the headers and the values.
        :rtype: Dictionary
        :return: The map containing the various disposition values in a map.
        """

        # retrieves the content disposition header
        content_disposition = headers_map.get("Content-Disposition", None)

        # in case no content disposition is defined must raise an
        # exception because the header field is required
        if not content_disposition:
            raise exceptions.WSGIRuntimeException(
                "missing content disposition in multipart value"
            )

        # splits the content disposition to obtain the attributes and
        # creates (and starts) the content disposition map
        content_disposition_attributes = content_disposition.split(";")
        content_disposition_map = {}

        # iterates over all the content disposition attributes
        # the content disposition attributes are not stripped
        for content_disposition_attribute in content_disposition_attributes:
            # strips and split the content disposition attribute around
            # the separator token (for key and value) and then retrieves
            # the length of the result for verification
            content_disposition_attribute_stripped = content_disposition_attribute.strip()
            content_disposition_attribute_splitted = content_disposition_attribute_stripped.split("=")
            content_disposition_attribute_splitted_length = len(content_disposition_attribute_splitted)

            # in case the length is two, it's a "normal" key value
            # pair based attribute case
            if content_disposition_attribute_splitted_length == 2:
                # retrieves the key and the value, then strips
                # the value from the string items and sets the
                # key and value association in the map
                key, value = content_disposition_attribute_splitted
                value_stripped = value.strip("\"")
                content_disposition_map[key] = value_stripped

            # in case the length is one the current attribute refers
            # a single attribute with no value set
            elif content_disposition_attribute_splitted_length == 1:
                # retrieves the key value from the content disposition
                # attribute and set it in the map with an invalid value
                key = content_disposition_attribute_splitted[0]
                content_disposition_map[key] = None

            # otherwise it's an invalid value and an exception must
            # be raised indicating the error
            else:
                raise exceptions.WSGIRuntimeException(
                    "invalid content disposition value in multipart value: " +
                    content_disposition_attribute_stripped
                )

        # returns the content disposition map, containing the
        # complete set of headers for the content disposition
        return content_disposition_map

    def _execute_background_thread(self, callable, retries = 0, timeout = 0.0, timestamp = None):
        """
        Simple implementation of the background execution of
        a callable for the WSGI request using a thread.

        This method should be used as a fallback strategy as
        it represents a huge overhead in creation (thread
        creation is slow).

        :type callable: Callable
        :param callable: The callable to be called in background.
        :type retries: int
        :param retries: The number of times to retry executing the
        callable in case exception is raised.
        :type timeout: float
        :param timeout: The time to be set in between calls of the
        callable, used together with the retry value.
        :type timestamp: float
        :param timestamp: The unix second based timestamp for the
        first execution of the callable.
        """

        thread = threading.Thread(target = callable)
        thread.start()
