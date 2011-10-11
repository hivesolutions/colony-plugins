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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
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

    def gzip_contents(self, contents_string):
        # creates a new string buffer
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # writes the magic header
        string_buffer.write("\037\213")

        # writes the compression method
        string_buffer.write("\010")

        # writes the flag values
        string_buffer.write(chr(0))

        # writes the timestamp value
        string_buffer.write(struct.pack("<L", long(time.time())))

        # writes some heading values
        string_buffer.write("\002")
        string_buffer.write("\377")

        # compresses the contents with the zlib
        contents_string_compressed = zlib.compress(contents_string, DEFAULT_COMPRESSION_LEVEL)

        # writes the the contents string compressed into the string buffer
        string_buffer.write(contents_string_compressed[2:])

        # computes the contents string crc 32
        contents_string_crc32 = zlib.crc32(contents_string)

        # writes the crc 32 lower values
        string_buffer.write(struct.pack("<L", contents_string_crc32))

        # retrieves the string value from the string buffer
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value
