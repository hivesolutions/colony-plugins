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

import zlib
import time
import struct

import colony.libs.string_buffer_util

DEFAULT_COMPRESSION_LEVEL = 3
""" The default compression level """

class Gzip:
    """
    Provides functions to interact with gzip files.
    """

    gzip_plugin = None
    """ The gzip plugin """

    def __init__(self, gzip_plugin):
        """
        Constructor of the class.

        @type gzip_plugin: GzipPlugin
        @param gzip_plugin: The gzip plugin.
        """

        self.gzip_plugin = gzip_plugin

    def gzip_contents(self, contents_string, file_name = None):
        """
        Compresses the given contents using the deflate compression
        algorithm and encapsulating it into the gzip file format.

        @type contents_string: String
        @param contents_string: A string containing the contents
        to be compressed.
        @type file_name: String
        @param file_name: The name to be set to the file in the
        generated compressed buffer.
        @rtype: String
        @return: The string containing the compressed buffer.
        """

        # creates a new string buffer
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # writes the magic header
        string_buffer.write("\x1f\x8b")

        # writes the compression method
        string_buffer.write("\x08")

        # writes the flag values
        file_name and string_buffer.write("\x08") or string_buffer.write("\x00")

        # writes the timestamp value
        string_buffer.write(struct.pack("<L", long(time.time())))

        # writes some extra heading values
        # (includes operating system)
        string_buffer.write("\x02")
        string_buffer.write("\xff")

        # writes the file name
        file_name and string_buffer.write(file_name + "\0")

        # compresses the contents with the zlib
        contents_string_compressed = zlib.compress(contents_string, DEFAULT_COMPRESSION_LEVEL)

        # writes the the contents string compressed into the string buffer
        string_buffer.write(contents_string_compressed[2:-4])

        # computes the contents string crc 32
        # and convert it to unsigned number
        contents_string_crc32 = zlib.crc32(contents_string)
        contents_string_crc32_unsigned = self._unsigned(contents_string_crc32)

        # writes the crc 32 lower values
        string_buffer.write(struct.pack("<L", contents_string_crc32_unsigned))

        # retrieves the contents string size
        # and the writes the size lower values
        contents_string_length = len(contents_string)
        contents_string_length_unsigned = self._unsigned(contents_string_length)
        string_buffer.write(struct.pack("<L", contents_string_length_unsigned))

        # retrieves the string value from the string buffer
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value

    def _unsigned(self, number):
        """
        Converts the given number to unsigned assuming
        a 32 bit value.

        @type number: int
        @param number: The number to be converted to unsigned.
        @rtype: int
        @return: The given number converted to unsigned.
        """

        # in case the number is positive or zero
        # (no need to convert)
        if number >= 0:
            # returns the immediately with
            # the current number value
            return number

        # runs the modulus in the number
        # to convert it to unsigned
        return number + 4294967296
