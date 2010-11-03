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
import types
import base64
import random

import colony.libs.string_buffer_util

MIME_VERSION_VALUE = "MIME-Version"
""" The mime version value """

CONTENT_TYPE_VALUE = "Content-Type"
""" The content type value """

DEFAULT_PROTOCOL_VERSION = "1.0"
""" The default protocol version """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

MULTI_PART_MESSAGE = "This is a multi-part message in MIME format"
""" The multi part message """

VALID_BOUNDARY_CHARACTERS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                             "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                             "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                             "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
                             "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7",
                             "8", "9", "+", "/")
""" The tuple containing the valid boundary characters """

class FormatMime:
    """
    The format mime class.
    """

    format_mime_plugin = None
    """ The format mime plugin """

    extension_map = {}
    """ The map of extension reference """

    def __init__(self, format_mime_plugin):
        """
        Constructor of the class.

        @type format_mime_plugin: FormatMimePlugin
        @param format_mime_plugin: The format mime plugin.
        """

        self.format_mime_plugin = format_mime_plugin

        self.extension_map = {}

    def create_message(self, parameters):
        return MimeMessage()

    def create_message_part(self, parameters):
        return MimeMessagePart()

    def get_mime_type_file_name(self, file_name):
        # retrieves the base name and extension from the
        # file name
        _base, extension = os.path.splitext(file_name)

        # retrieves the (mime) type from the extension mime type mapping
        mime_type = self.extension_map.get(extension, None)

        # returns the mime type
        return mime_type

    def set_configuration_property(self, configuration_propery):
        # retrieves the configuration
        configuration = configuration_propery.get_data()

        # retrieves the extension map
        extension_map = configuration["extension"]

        # sets the extension map
        self.extension_map = extension_map

    def unset_configuration_property(self):
        # sets the extension map
        self.extension_map = {}

class MimeMessage:
    """
    Class representing a mime message.
    """

    part = False
    """ If the current message is part of an upper message """

    multi_part = False
    """ Flag controlling if the message is of type multi part """

    boundary = None
    """ The boundary value for multi part encoding """

    protocol_version = DEFAULT_PROTOCOL_VERSION
    """ The version of the "protocol" """

    content_type_charset = DEFAULT_CHARSET
    """ The content type charset """

    part_list = []
    """ The list of parts to be included in the multi part message """

    headers_map = {}
    """ The map containing the header values """

    message_stream = None
    """ The message stream """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.part_list = []
        self.headers_map = {}
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

    def write_base_64(self, message, flush = 1):
        # encodes the mesage into base 64
        message = base64.b64encode(message)

        # writes the message to the message stream
        self.message_stream.write(message)

    def add_part(self, part):
        self.part_list.append(part)

    def remove_part(self, part):
        self.part_list.remove(part)

    def get_value(self):
        # retrieves the result stream
        result = colony.libs.string_buffer_util.StringBuffer()

        # in case this is multi part message
        if self.multi_part:
            # in case this message is not a part
            if not self.part:
                # writes the multi part format message
                self.message_stream.write(MULTI_PART_MESSAGE)

            # encodes the multi part message
            self._encode_multi_part()

        # retrieves the result string value
        message = self.message_stream.get_value()

        # creates the ordered map to hold the header values
        headers_ordered_map = colony.libs.structures_util.OrderedMap()

        # in case this is multi part message
        if self.multi_part:
            # sets the content type
            headers_ordered_map[CONTENT_TYPE_VALUE] = "multipart/" + self.multi_part + ";" + "boundary=\"" + self.boundary + "\""

        # in case this message is not a part, writes the
        # main headers
        if not self.part:
            # sets the mime version
            headers_ordered_map[MIME_VERSION_VALUE] = self.protocol_version

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

    def get_header(self, header_name):
        """
        Retrieves an header value of the message,
        or none if no header is defined for the given
        header name.

        @type header_name: String
        @param header_name: The name of the header to be retrieved.
        @rtype: Object
        @return: The value of the request header.
        """

        return self.headers_map.get(header_name, None)

    def set_header(self, header_name, header_value):
        """
        Set a mime header value in the message.

        @type header_name: String
        @param header_name: The name of the header to be set.
        @type header_value: Object
        @param header_value: The value of the header to be sent
        in the response.
        """

        self.headers_map[header_name] = header_value

    def get_multi_part(self):
        """
        Retrieves the multi part.

        @rtype: String
        @return: The multi part.
        """

        return self.multi_part

    def set_multi_part(self, multi_part):
        """
        Sets the multi part.

        @type multi_part: String
        @param multi_part: The multi part.
        """

        self.multi_part = multi_part

    def get_boundary(self):
        """
        Retrieves the boundary.

        @rtype: String
        @return: The boundary.
        """

        return self.boundary

    def set_boundary(self, boundary):
        """
        Sets the boundary.

        @type boundary: String
        @param boundary: The boundary
        """

        self.boundary = boundary

    def get_user_protocol_verion(self):
        """
        Retrieves the protocol version.

        @rtype: String
        @return: The protocol version.
        """

        return self.protocol_version

    def set_protocol_version(self, protocol_version):
        """
        Sets the protocol version.

        @type protocol_version: String
        @param protocol_version: The protocol version.
        """

        self.protocol_version = protocol_version

    def get_content_type_charset(self):
        """
        Retrieves the content type charset.

        @rtype: String
        @return: The content type charset.
        """

        return self.content_type_charset

    def set_content_type_charset(self, content_type_charset):
        """
        Sets the content type charset.

        @type content_type_charset: String
        @param content_type_charset: The content type charset.
        """

        self.content_type_charset = content_type_charset

    def _encode_multi_part(self):
        """
        Encodes the multi part message using the given
        current buffer.
        """

        # creates the part values list
        part_values = []

        # iterates over all the parts n the part list
        for part in self.part_list:
            # retrieves the part value
            part_value = part.get_value()

            # adds the part value to the part values
            part_values.append(part_value)

        # generates the initial loop
        self.boundary = self._generate_boundary()

        # loops continuously
        while True:
            # checks the part values for the boundary in case it succeeds
            # the boundary is valid
            if self._check_part_values_boundary(self.boundary, part_values):
                # breaks the loop
                break

            # regenerates the boundary value
            self.boundary = self._generate_boundary(self.boundary)

        # iterates over all the part values
        for part_value in part_values:
            # writes the initial boundary value
            self.write("\r\n--" + self.boundary + "\r\n")

            # writes the part value
            self.write(part_value)

        # writes the final boundary value
        self.write("\r\n--" + self.boundary + "--\r\n")

    def _generate_boundary(self, boundary = None):
        """
        Generates a boundary, using the given boundary as the
        base value in case it is given.

        @type boundary: String
        @param boundary: The base boundary to be used.
        @rtype: String
        @return: The new generated boundary.
        """

        # creates a new boundary if necessary
        boundary = boundary or str()

        # creates the boundary string buffer
        boundary_string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # iterates over the range to generate the random value
        for _index in range(32):
            # generates a normalized random values
            random_value = random.random() * 63

            # converts the random value to integer
            random_value_integer = int(random_value)

            # converts the random value to character
            random_value_character = VALID_BOUNDARY_CHARACTERS[random_value_integer]

            # writes the random value character to the boundary string buffer
            boundary_string_buffer.write(random_value_character)

        # retrieves the boundary string value
        boundary_string_value = boundary_string_buffer.get_value()

        # adds the boundary string value to the boundary
        boundary += boundary_string_value

        # returns the (new) boundary
        return boundary

    def _check_part_values_boundary(self, boundary, part_values):
        """
        Checks the parts in order to validate the boundary.
        In case any of the files contains the boundary the
        checks fails and returns invalid.

        @type boundary: String
        @param boundary: The boundary to be checked.
        @type part_values: List
        @param part_values: The values of the various parts.
        @rtype: bool
        @return: The result of the check.
        """

        # iterates over all the part values
        for part_value in part_values:
            # in case the part value contains the boundary value
            if not part_value.find(boundary) == -1:
                # returns invalid
                return False

        # returns valid
        return True

class MimeMessagePart(MimeMessage):
    """
    Class representing a part mime message.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        MimeMessage.__init__(self)

        # sets the part value to true
        # so that no extra values are set
        self.part = True
