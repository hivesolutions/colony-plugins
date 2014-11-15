#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import base64
import random
import mimetypes

import colony

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

VALID_BOUNDARY_CHARACTERS = (
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
    "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
    "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
    "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "+", "/"
)
""" The tuple containing the valid boundary characters """

class Mime(colony.System):
    """
    The mime class, responsible for operations related with
    the standards related with the mime specification.
    """

    extension_map = {}
    """ The map of extension references, that maps the extension
    name with the associated mime type """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.extension_map = {}

    def create_message(self, parameters):
        return MimeMessage()

    def create_message_part(self, parameters):
        return MimeMessagePart()

    def get_mime_type_file_name(self, file_name, fallback = True):
        # retrieves the base name and extension from the
        # file name and then converts the extension value
        # into its lower cased version to be normalizes in
        # the way it's the mime is retrieved
        _base, extension = os.path.splitext(file_name)
        extension = extension.lower()

        # retrieves the (mime) type from the extension mime type mapping,
        # this strategy uses the current extension map registry
        mime_type = self.extension_map.get(extension, None)

        # in case the mime type is not retrieved with success and the
        # fallback flag is set the inner system strategy is used
        if not mime_type and fallback:
            mime_type, _encoding = mimetypes.guess_type(file_name)

        # returns the resolved mime type, this value may be invalid/unset
        # in case no resolution was possible
        return mime_type

    def set_configuration_property(self, configuration_propery):
        # retrieves the configuration and verifies that the retrieved
        # value is valid to be processed in the current handler
        configuration = configuration_propery.get_data()
        if not configuration: return

        # retrieves the extension map from the configuration and
        # and updates the current extension map reference so that
        # the new values are used instead
        extension_map = configuration["extension"]
        self.extension_map = extension_map

    def unset_configuration_property(self):
        # sets the extension map
        self.extension_map = {}

class MimeMessage(object):
    """
    Class representing a mime message, this is the
    mains structure where the mime transforms will
    occur. Should provide a simple interface for
    interaction with the mime contents.
    """

    part = False
    """ If the current message is part of an upper message,
    meaning that is some kind of child/part value """

    multi_part = False
    """ Flag controlling if the message is of type multi part,
    meaning that it should contain child/part elements """

    boundary = None
    """ The boundary value for multi part encoding, this
    must be determined using a strategy that avoids any
    kind of collisions with the part contents """

    protocol_version = DEFAULT_PROTOCOL_VERSION
    """ The version of the "protocol" that is going to be
    used as the default fallback """

    content_type_charset = DEFAULT_CHARSET
    """ The content type charset, for which the current
    message will follow and encode its data """

    part_list = []
    """ The list of parts to be included in the multi part
    message, these are considered to be the child parts """

    headers_map = {}
    """ The map containing the header values to be set in
    the current mime container/message """

    message_stream = None
    """ The message stream, containing the partial values for
    the message contents associated  """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.part_list = []
        self.headers_map = {}
        self.message_stream = colony.StringBuffer()

    def read_simple(self, message_contents, decode = True):
        # retrieves the data type of the provided message contents
        # string value to be used for encoding evaluation
        message_type = type(message_contents)

        # in case the data type of the message to be read is bytes
        # based and the decode flag is set the provided contents
        # should be decoded so that an unicode string is used instead
        if message_type == colony.legacy.BYTES and decode:
            message_contents = message_contents.decode(self.content_type_charset)

        # strips the message contents and then finds the index
        # for the end of the headers section to be used in parsing
        message_contents = message_contents.lstrip()
        end_headers_index = message_contents.find("\r\n\r\n")

        # in case there are no header values in the message
        if end_headers_index == -1:
            # sets the header lines as empty and the headers index
            # to a valid value for later message contents retrieval
            headers_lines = []
            end_headers_index = -4
        # otherwise there are header values in the message
        else:
            # retrieves the header contents string value and
            # splits the headers around the lines
            headers_contents = message_contents[:end_headers_index]
            headers_lines = headers_contents.split("\r\n")

        # iterates over all the headers lines
        # to construct the headers map
        for header_line in headers_lines:
            # splits the header line around the divider
            # and checks the length of the resulting values
            header_values = header_line.split(":", 1)
            header_values_length = len(header_values)

            # in case the length of the header values is
            # "valid"
            if header_values_length > 1:
                # unpacks the header values into name
                # and value
                header_name, header_value = header_values
            # otherwise it's a "simple" header with no value
            else:
                # only unpacks the name value and sets the
                # value to default
                header_name, = header_values
                header_value = ""

            # strips both the header name and value
            header_name = header_name.strip()
            header_value = header_value.strip()

            # sets the header in the headers map
            self.headers_map[header_name] = header_value

        # retrieves the message (contents) value
        message_value = message_contents[end_headers_index + 4:]

        # writes the message value in the message stream
        self.message_stream.write(message_value)

    def write(self, message, flush = 1, encode = True):
        # retrieves the message type
        message_type = type(message)

        # in case the data type of the provided message string
        # is bytes based and the decoding flag is set the value
        # is decoded according to the currently defined charset
        if message_type == colony.legacy.BYTES and encode:
            message = message.decode(self.content_type_charset)

        # writes the message to the message stream, note that the
        # value should be unicode based to avoid possible join
        # issues at the final part of the message assembling
        self.message_stream.write(message)

    def write_base_64(self, message, flush = 1):
        # makes sure that the message is a byte string
        # and encodes the message into base 64 and then
        # writes the encoded value to the stream
        message = colony.legacy.bytes(message)
        message = base64.b64encode(message)
        message = colony.legacy.str(message)
        self.message_stream.write(message)

    def add_part(self, part):
        self.part_list.append(part)

    def remove_part(self, part):
        self.part_list.remove(part)

    def get_value(self):
        # creates the buffer that is going to hold the
        # final message stream value (to be joined latter)
        # note that the base type is enforced to be unicode
        result = colony.StringBuffer(btype = colony.legacy.UNICODE)

        # in case this is a multi part message
        if self.multi_part:
            # in case this message is not a part must
            # write a simple multi part information message
            if not self.part:
                self.message_stream.write(MULTI_PART_MESSAGE)

            # encodes the multi part message, staring the
            # logic of encoding the multiple parts that
            # compose the current mime message (iterative)
            self._encode_multi_part()

        # retrieves the result string value
        message = self.message_stream.get_value()

        # creates the ordered map to hold the header values
        headers_ordered_map = colony.OrderedMap()

        # in case this is multi part message, updates
        # the content type value with the appropriate
        # multipart value with the proper boundary
        if self.multi_part:
            headers_ordered_map[CONTENT_TYPE_VALUE] = "multipart/" + self.multi_part +\
                ";" + "boundary=\"" + self.boundary + "\""

        # in case this message is not a part, writes the
        # main headers, including the mime indication
        if not self.part:
            headers_ordered_map[MIME_VERSION_VALUE] = self.protocol_version

        # extends the headers ordered map with the headers map
        headers_ordered_map.extend(self.headers_map)

        # iterates over all the header values to be sent in order
        # to write their tuple association to the current buffer
        for header_name, header_value in colony.legacy.items(headers_ordered_map):
            result.write(header_name + ": " + header_value + "\r\n")

        # writes the end of the headers and the message
        # values into the result
        result.write("\r\n")
        result.write(message)

        # retrieves the value from the result buffer and returns
        # it to the caller method as the final message string
        result_value = result.get_value()
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

    def set_header(self, header_name, header_value, decode = True):
        """
        Set a mime header value in the message, the operation
        of this method will decode the header value if required.

        @type header_name: String
        @param header_name: The name of the header to be set.
        @type header_value: Object
        @param header_value: The value of the header to be sent
        in the response.
        @type decode: bool
        @param decode: If the header value should be decoded in
        case the type is byte string based.
        """

        # retrieves the header value type
        header_value_type = type(header_value)

        # in case the data type of the header value is byte string based
        # and the decoding flag is set the value is decoded so that an
        # unicode string is store in the header to value association
        if header_value_type == colony.legacy.BYTES and decode:
            header_value = header_value.decode(self.content_type_charset)

        # sets the header value in the headers map
        # key to value association map
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
        boundary_string_buffer = colony.StringBuffer()

        # iterates over the range to generate the random value
        for _index in colony.legacy.xrange(32):
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
            # in case the part value does not contains the boundary value
            # must skip the current iteration (nothing to be done)
            if part_value.find(boundary) == -1: continue

            # returns invalid as the boundary has been found in at least
            # one of the parts, so the boundary is considered invalid
            return False

        # returns valid
        return True

class MimeMessagePart(MimeMessage):
    """
    Class representing a part mime message, this is a
    specialized of the mime message that offers extra
    operations for only message parts.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        MimeMessage.__init__(self)

        # sets the part value to true
        # so that no extra values are set
        self.part = True
