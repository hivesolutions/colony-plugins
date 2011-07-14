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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import stat
import struct

import packaging_ar_exceptions

import colony.libs.string_buffer_util

FILE_PATH_VALUE = "file_path"
""" The file path value """

FILE_PROPERTIES_VALUE = "file_properties"
""" The file properties value """

PADDING_BYTE_VALUE = "\x0a"
""" The padding byte value """

MAGIC_FILE_STRING_VALUE = "\x60\x0a"
""" The magic file string value """

MAGIC_STRING_VALUE = "!<arch>\n"
""" The magic string value """

MAGIC_STRING_SIZE = 8
""" The magic string size (in bytes) """

FILE_HEADER_SIZE = 60
""" The file header size (in bytes) """

BUFFER_SIZE = 1024
""" The size of the buffer """

READ_MODE = "rb"
""" The read mode """

WRITE_MODE = "wb+"
""" The write mode """

DEFAULT_MODE = READ_MODE
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
        ar_file = ArFile(self, file_path)

        # returns the ar file
        return ar_file

class ArFile:
    """
    The ar file class.
    """

    packing_ar = None
    """ The packing ar to be used """

    file_path = None
    """ The file path for the file """

    mode = None
    """ The mode being used """

    file = None
    """ The file currently being used """

    header_written = False
    """ The flag to control if the header is written """

    index_map = {}
    """ The index map associating the archive path with the file descriptor """

    def __init__(self, packing_ar, file_path):
        """
        Constructor of the class.

        @type packing_ar: PackagingAr
        @param packing_ar: The packing ar to be used.
        @type file_path: String
        @param file_path: The path to the file to be used.
        """

        self.packing_ar = packing_ar
        self.file_path = file_path

        self.index_map = {}

    def open(self, mode = DEFAULT_MODE):
        """
        Opens the file in the given mode.

        @type mode: String
        @param mode: The mode to open the file.
        """

        # saves the current mode
        self.mode = mode

        # opens the file with the current mode
        self.file = open(self.file_path, mode)

    def close(self):
        """
        Closes the current file, being used.
        """

        # closes the current file
        self.file.close()

    def extract_all(self, target_path, parameters = {}):
        # retrieves the index map
        index_map = self.get_index()

        # iterates over all the archives in
        # the index map
        for archive_path in index_map:
            # reads the archive contents
            archive_contents = self.read(archive_path, parameters)

            # creates the full archive path
            full_archive_path = target_path + "/" + archive_path

            # retrieves the directory path from the full archive path
            full_archive_directory_path = os.path.dirname(full_archive_path)

            # in case the path does not exists
            if not os.path.exists(full_archive_directory_path):
                # creates the directories if necessary
                os.makedirs(full_archive_directory_path)

            # opens the archive file
            archive_file = open(full_archive_path, "wb")

            try:
                # writes the archive contents
                archive_file.write(archive_contents)
            finally:
                # closes the archive file
                archive_file.close()

    def write(self, file_path, archive_path = None, parameters = {}):
        # in case the path does not exist
        if not os.path.exists(file_path):
            # raises the file not found exception
            raise packaging_ar_exceptions.FileNotFound("the file path does not exist: " + file_path)

        # in case the archive path is not defined
        if not archive_path:
            # separates the drive from the base file path
            _drive, base_file_path = os.path.splitdrive(file_path)

            # strips the base file path from the trailing separators
            archive_path = base_file_path.strip("/\\")

        # retrieves the file stat
        file_stat = os.stat(file_path)

        # retrieves the various attributes from the file stat
        modification_timestamp = file_stat[stat.ST_MTIME]
        owner_id = file_stat[stat.ST_UID]
        group_id = file_stat[stat.ST_GID]
        mode = file_stat[stat.ST_MODE]
        size = file_stat[stat.ST_SIZE]

        # tries to retrieve the file properties
        file_properties = parameters.get(FILE_PROPERTIES_VALUE, {})

        # sets the file properties values
        file_properties["modification_timestamp"] = modification_timestamp
        file_properties["owner_id"] = owner_id
        file_properties["group_id"] = group_id
        file_properties["mode"] = mode
        file_properties["size"] = size

        # sets the file properties in the parameters
        parameters[FILE_PROPERTIES_VALUE] = file_properties

        # opens the file for reading
        file = open(file_path, "rb")

        try:
            # writes the file to the current file
            self._write_file(file, archive_path, parameters)
        finally:
            # closes the file
            file.close()

    def write_file(self, file, archive_path, parameters = {}):
        # tries to retrieve the file properties
        file_properties = parameters.get(FILE_PROPERTIES_VALUE, {})

        # forwards the file to the end position
        file.seek(0, os.SEEK_END)

        # retrieves the current offset (file size)
        size = file.tell()

        # rewinds the file to the initial position
        file.seek(0, os.SEEK_SET)

        # sets the file properties values
        file_properties["size"] = size

        # sets the file properties in the parameters
        parameters[FILE_PROPERTIES_VALUE] = file_properties

        # writes the file to the current file
        self._write_file(file, archive_path, parameters)

    def write_string_value(self, string_value, archive_path, parameters = {}):
        # creates the string buffer to hold the string value
        string_buffer = colony.libs.string_buffer_util.StringBuffer(False)

        # writes the string value to the string buffer
        string_buffer.write(string_value)

        # rewinds the string buffer to the initial position
        string_buffer.seek(0, os.SEEK_SET)

        # tries to retrieve the file properties
        file_properties = parameters.get(FILE_PROPERTIES_VALUE, {})

        # retrieves the string value length (file size)
        size = len(string_value)

        # sets the file properties values
        file_properties["size"] = size

        # sets the file properties in the parameters
        parameters[FILE_PROPERTIES_VALUE] = file_properties

        # writes the file to the current file
        self._write_file(string_buffer, archive_path, parameters)

    def read(self, archive_path, parameters = {}):
        # retrieves the index map
        index_map = self.get_index()

        # in case the archive path is not found in the index map
        if not archive_path in index_map:
            # raises the file not found exception
            raise packaging_ar_exceptions.FileNotFound("archive file does not exist: " + archive_path)

        # retrieves the archive file entry from the index map
        archive_file_entry = index_map[archive_path]

        # retrieves the archive file offset
        archive_file_offset = archive_file_entry.get_offset()

        # retrieves the archive file size
        archive_file_size = archive_file_entry.get_size()

        # jumps the file contents
        self.file.seek(archive_file_offset)

        # reads the archive file contents
        archive_file_contents = self.file.read(archive_file_size)

        # reads the archive file contents
        return archive_file_contents

    def get_index(self):
        # in case the index map is not defined
        if not self.index_map:
            # reads the index
            self._read_index()

        # returns the index map
        return self.index_map

    def get_names(self):
        # retrieves the index map
        index_map = self.get_index()

        # retrieves the keys of the index map (the name of the file)
        index_map_keys = index_map.keys()

        # returns the index map keys
        return index_map_keys

    def _write_file(self, file, archive_path, parameters = {}):
        """
        Writes the given file object to the current file, using the given
        archive path as the path to the stored object.

        @type file: File
        @param file: The file object to be written.
        @type archive_path: String
        @param archive_path: The path to be used by the file in the archive.
        @type parameters: Dictionary
        @param parameters: The parameters to the write.
        """

        # retrieves the file properties map from the parameters
        file_properties = parameters.get(FILE_PROPERTIES_VALUE, {})

        # retrieves the values from the file properties map
        modification_timestamp = file_properties.get("modification_timestamp", 0)
        owner_id = file_properties.get("owner_id", 0)
        group_id = file_properties.get("group_id", 0)
        mode = file_properties.get("mode", 0)
        size = file_properties.get("size", 0)

        # converts the numeric values to string values
        modification_timestamp_string = str(modification_timestamp)
        owner_id_string = str(owner_id)
        group_id_string = str(group_id)
        mode_string = "%o" % mode
        size_string = str(size)

        # checks the header
        self._check_header()

        # goes to the end of the file
        self.file.seek(0, os.SEEK_END)

        # creates the file header from the various file components in string format
        file_header = struct.pack("16s12s6s6s8s10s2s", archive_path, modification_timestamp_string, owner_id_string, group_id_string, mode_string, size_string, MAGIC_FILE_STRING_VALUE)

        # replaces the null values in the file header for spaces (standard)
        file_header = file_header.replace("\0", " ")

        # writes the file header
        self.file.write(file_header)

        # loops indefinitely
        while True:
            # reads the file contents
            file_contents = file.read(BUFFER_SIZE)

            # in case there are no file contents,
            # the end of file is reached
            if not file_contents:
                # breaks the loop
                break

            # writes the file contents to the file
            self.file.write(file_contents)

        # checks if the size is odd
        if size % 2:
            # writes the padding character
            # to align the data part of the file
            self.file.write(PADDING_BYTE_VALUE)

    def _check_header(self):
        """
        Checks the header, to see if it
        is written.
        """

        # in case the header is not
        # yet written (flag is not set)
        if not self.header_written:
            # seeks to the beginning of the file
            self.file.seek(0)

            # reads the magic string
            magic_string = self.file.read(MAGIC_STRING_SIZE)

            # in case the magic string does not match
            if not magic_string == MAGIC_STRING_VALUE:
                # writes the header
                self._write_header()

            # sets the header written flag
            self.header_written = True

    def _write_header(self):
        """
        Writes the header into the file.
        """

        # seeks to the beginning of the file
        self.file.seek(0)

        # writes the magic string value
        self.file.write(MAGIC_STRING_VALUE)

    def _read_index(self):
        # start the current offset value
        current_offset = 0

        # reads the magic string
        magic_string = self.file.read(MAGIC_STRING_SIZE)

        # increments the current offset value
        current_offset += MAGIC_STRING_SIZE

        # in case the magic string does not match
        if not magic_string == MAGIC_STRING_VALUE:
            # raises the invalid file format exception
            raise packaging_ar_exceptions.InvalidFileFormat("invalid magic string value: " + magic_string)

        # loops continuously
        while True:
            # reads the file header from the file
            file_header = self.file.read(FILE_HEADER_SIZE)

            # increments the current offset value
            current_offset += FILE_HEADER_SIZE

            # in case the file header is not file (end of file)
            if not file_header:
                break

            # unpacks the values from the file header
            name, modification_timestamp, owner_id, group_id, mode, size, magic_value = struct.unpack("16s12s6s6s8s10s2s", file_header)

            # in case the magic value is not valid
            if not magic_value == MAGIC_FILE_STRING_VALUE:
                # raises the invalid file format exception
                raise packaging_ar_exceptions.InvalidFileFormat("invalid magic file string value: " + magic_value)

            # strips the name from the extra values (spaces)
            name = name.strip()

            # converts the various string integer values to the numeric representation
            modification_timestamp_numeric = int(modification_timestamp)
            owner_id_numeric = int(owner_id)
            group_id_numeric = int(group_id)
            mode_numeric = int(mode, 8)
            size_numeric = int(size)

            # creates the ar file entry from the values
            ar_file_entry = ArFileEntry(name, modification_timestamp_numeric, owner_id_numeric, group_id_numeric, mode_numeric, size_numeric, magic_value, current_offset)

            # sets the file entry in the index map
            self.index_map[name] = ar_file_entry

            # checks if the size is odd
            if size_numeric % 2:
                # increments the padding byte
                size_numeric += 1

            # jumps the file contents
            self.file.seek(size_numeric, os.SEEK_CUR)

            # increments the current offset value
            current_offset += size_numeric

class ArFileEntry:
    """
    The ar file entry class.
    Represents an ar file index entry.
    """

    name = None
    """ The name of the ar file """

    modification_timestamp = None
    """ The modification timestamp """

    owner_id = None
    """ The owner id """

    group_id = None
    """ The group id """

    mode = None
    """ The mode of access to the file """

    size = None
    """ The size of the ar file """

    magic_value = None
    """ The magic value of the ar file """

    offset = None
    """ The offser of the file in the archive file """

    def __init__(self, name = None, modification_timestamp = None, owner_id = None, group_id = None, mode = None, size = None, magic_value = None, offset = None):
        """
        Constructor of the file.
        """

        self.name = name
        self.modification_timestamp = modification_timestamp
        self.owner_id = owner_id
        self.group_id = group_id
        self.mode = mode
        self.size = size
        self.magic_value = magic_value
        self.offset = offset

    def get_name(self):
        """
        Retrieves the name.

        @rtype: String
        @return: The name.
        """

        return self.name

    def set_name(self, name):
        """
        Sets the name.

        @type name: String
        @param name: The name.
        """

        self.name = name

    def get_modification_timestamp(self):
        """
        Retrieves the modification timestamp.

        @rtype: int
        @return: The modification timestamp.
        """

        return self.modification_timestamp

    def set_modification_timestamp(self, modification_timestamp):
        """
        Sets the modification timestamp.

        @type modification_timestamp: int
        @param modification_timestamp: The modification timestamp.
        """

        self.modification_timestamp = modification_timestamp

    def get_owner_id(self):
        """
        Retrieves the owner id.

        @rtype: int
        @return: The owner id.
        """

        return self.owner_id

    def set_owner_id(self, owner_id):
        """
        Sets the owner id.

        @type owner_id: int
        @param owner_id: The owner id.
        """

        self.owner_id = owner_id

    def get_group_id(self):
        """
        Retrieves the group id.

        @rtype: int
        @return: The group id.
        """

        return self.group_id

    def set_group_id(self, group_id):
        """
        Sets the group id.

        @type group_id: int
        @param group_id: The group id.
        """

        self.group_id = group_id

    def get_mode(self):
        """
        Retrieves the mode.

        @rtype: int
        @return: The mode.
        """

        return self.group_id

    def set_mode(self, mode):
        """
        Sets the mode.

        @type mode: int
        @param mode: The mode.
        """

        self.mode = mode

    def get_size(self):
        """
        Retrieves the size.

        @rtype: int
        @return: The size.
        """

        return self.size

    def set_size(self, size):
        """
        Sets the size.

        @type size: int
        @param size: The size.
        """

        self.size = size

    def get_magic_value(self):
        """
        Retrieves the magic value.

        @rtype: String
        @return: The magic value.
        """

        return self.magic_value

    def set_magic_value(self, magic_value):
        """
        Sets the size.

        @type magic_value: String
        @param magic_value: The magic value.
        """

        self.magic_value = magic_value

    def get_offset(self):
        """
        Retrieves the offset.

        @rtype: int
        @return: The offset.
        """

        return self.offset

    def set_offset(self, offset):
        """
        Sets offset.

        @type offset: String
        @param offset: The offset.
        """

        self.offset = offset
