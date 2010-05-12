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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import struct

import packaging_ar_exceptions

FILE_PATH_VALUE = "file_path"
""" The file path value """

MAGIC_STRING_VALUE = "!<arch>\n"
""" The magic string value """

MAGIC_STRING_SIZE = 8
""" The magic string size (in bytes) """

FILE_HEADER_SIZE = 60
""" The file header size (in bytes) """

DEFAULT_MODE = "rb"
""" The default file opening mode """

class PackagingAr:
    """
    The packaging ar class.
    """

    packaging_ar_plugin = None
    """ The packaging ar plugin """

    def __init__(self, packaging_ar_plugin):
        """
        Constructor of the class.

        @type packaging_ar_plugin: PackagingArPlugin
        @param packaging_ar_plugin: The packaging ar plugin.
        """

        self.packaging_ar_plugin = packaging_ar_plugin

    def create_file(self, parameters):
        """
        Creates the file for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the file creation.
        @rtype: ArFile
        @return: The created file.
        """

        # in case the file path is not in the parameters map
        if not FILE_PATH_VALUE in parameters:
            # raises the missing parameter exception
            raise packaging_ar_exceptions.MissingParameter(FILE_PATH_VALUE)

        # retrieves the file path from the parameters
        file_path = parameters[FILE_PATH_VALUE]

        # creates a new ar file
        ar_file = ArFile(file_path)

        # returns the ar file
        return ar_file

class ArFile:
    """
    The ar file class.
    """

    file_path = None
    """ The file path for the file """

    file = None
    """ The file currently being used """

    def __init__(self, file_path):
        """
        Constructor of the class.

        @type file_path: String
        @param file_path: The path to the file to be used.
        """

        self.file_path = file_path

    def open(self, mode = DEFAULT_MODE):
        # opens the file with the current mode
        self.file = open(self.file_path, mode)

    def close(self):
        # closes the current file
        self.file.close()

    def write(self, file_path, archive_path, parameters = {}):
        pass

    def read(self, archive_path, parameters = {}):
        pass

    def read_index(self):
        # reads the magic string
        magic_string = self.file.read(MAGIC_STRING_SIZE)

        # in case the magic string does not match
        if not magic_string == MAGIC_STRING_VALUE:
            # raises the invalid file format exception
            raise packaging_ar_exceptions.InvalidFileFormat("invalid magic string value: " + magic_string)

        while 1:
            # reads the file header from the file
            file_header = self.file.read(FILE_HEADER_SIZE)

            # in case the file header is not file (end of file)
            if not file_header:
                break

            name, modification_timestamp, owner_id, group_id, mode, size, magic_value = struct.unpack("16s12s6s6s8s10s2s", file_header)

            modification_timestamp_numeric = int(modification_timestamp)

            owner_id_numeric = int(owner_id)

            group_id_numeric = int(group_id)

            mode_numeric = int(mode, 8)

            size_numeric = int(size)

            file_contents = self.file.read(size)

            if not magic_value == "\x60\x0a":
                # raises the invalid file format exception
                raise packaging_ar_exceptions.InvalidFileFormat("invalid magic value: " + magic_value)

            print repr(file_contents)
