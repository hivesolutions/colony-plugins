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

import os

import packaging_deb_exceptions

FILE_PATH_VALUE = "file_path"
""" The file path value """

READ_MODE = "rb"
""" The read mode """

WRITE_MODE = "wb+"
""" The write mode """

DEFAULT_MODE = READ_MODE
""" The default file opening mode """

class PackagingDeb:
    """
    The packaging deb class.
    """

    packaging_deb_plugin = None
    """ The packaging deb plugin """

    def __init__(self, packaging_deb_plugin):
        """
        Constructor of the class.

        @type packaging_deb_plugin: PackagingDebPlugin
        @param packaging_deb_plugin: The packaging deb plugin.
        """

        self.packaging_deb_plugin = packaging_deb_plugin

    def create_file(self, parameters):
        """
        Creates the file for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the file creation.
        @rtype: DebFile
        @return: The created file.
        """

        # in case the file path is not in the parameters map
        if not FILE_PATH_VALUE in parameters:
            # raises the missing parameter exception
            raise packaging_deb_exceptions.MissingParameter(FILE_PATH_VALUE)

        # retrieves the file path from the parameters
        file_path = parameters[FILE_PATH_VALUE]

        # creates a new deb file
        deb_file = DebFile(file_path)

        # returns the deb file
        return deb_file

class DebFile:
    """
    The deb file class.
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
        """
        Opens the file in the given mode.

        @type mode: String
        @param mode: The mode to open the file.
        """

        # opens the file with the current mode
        self.file = open(self.file_path, mode)

    def close(self):
        """
        Closes the current file, being used.
        """

        # tenho de fechar o ficherio criando a parte de controlo e
        # escrevendo a data

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
            raise packaging_deb_exceptions.FileNotFound("the file paths does not exist: " + file_path)



    def read(self, archive_path, parameters = {}):
        # retrieves the index map
        index_map = self.get_index()

        # in case the archive path is not found in the index map
        if not archive_path in index_map:
            # raises the file not found exception
            raise packaging_deb_exceptions.FileNotFound("archive file does not exist: " + archive_path)

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

        return self.timestamp

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
