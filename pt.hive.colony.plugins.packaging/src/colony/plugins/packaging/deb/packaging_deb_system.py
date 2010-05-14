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
import stat
import types
import tarfile

import packaging_deb_exceptions

import colony.libs.string_buffer_util

FILE_PATH_VALUE = "file_path"
""" The file path value """

FILE_PROPERTIES_VALUE = "file_properties"
""" The file properties value """

FILE_FORMAT_VALUE = "file_format"
""" The file format value """

DEB_FILE_ARGUMENTS_VALUE = "deb_file_arguments"
""" The deb file arguments value """

READ_MODE = "rb"
""" The read mode """

WRITE_MODE = "wb+"
""" The write mode """

TAR_FILE_FORMAT = "tar"
""" The tar file format """

TAR_GZ_FILE_FORMAT = "tar_gz"
""" The tar gz file format """

TAR_BZ2_FILE_FORMAT = "tar_bz2"
""" The tar bz2 file format """

TAR_LZMA_FILE_FORMAT = "tar_bz2"
""" The tar lzma file format """

DEFAULT_MODE = READ_MODE
""" The default file opening mode """

DEFAULT_FILE_FORMAT = TAR_FILE_FORMAT
""" The default file format """

DEFAULT_DEB_FILE_ARGUMENTS = {}
""" The default deb file arguments """

FILE_EXTENSIONS_MAP = {TAR_FILE_FORMAT : ".tar",
                       TAR_GZ_FILE_FORMAT : ".tar.gz",
                       TAR_BZ2_FILE_FORMAT : ".tar.bz2",
                       TAR_BZ2_FILE_FORMAT : ".tar.lzma"}
""" The file extensions map """

CONTROL_FILE_MODE = "w:gz"
""" The control file mode """

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

        # in case the file path is not in the parameters map
        if not FILE_PATH_VALUE in parameters:
            # raises the missing parameter exception
            raise packaging_deb_exceptions.MissingParameter(FILE_PATH_VALUE)

        # retrieves the file path from the parameters
        file_path = parameters[FILE_PATH_VALUE]

        # retrieves the file format from the parameters
        file_format = parameters.get(FILE_FORMAT_VALUE, DEFAULT_FILE_FORMAT)

        # retrieves the file path references from the parameters
        deb_file_arguments = parameters.get(DEB_FILE_ARGUMENTS_VALUE, DEFAULT_DEB_FILE_ARGUMENTS)

        # creates a new deb file
        deb_file = DebFile(self, file_path, file_format, deb_file_arguments)

        # returns the deb file
        return deb_file

class DebFile:
    """
    The deb file class.
    """

    packing_deb = None
    """ The packing deb """

    file_path = None
    """ The file path for the file """

    file_format = None
    """ The file format for the file """

    deb_file_arguments = None
    """ The arguments to the deb file structure creation """

    mode = None
    """ The mode being used """

    file = None
    """ The file currently being used """

    pending_files = []
    """ The list of pending files to be flushed """

    index_map = {}
    """ The index map associating the archive path with the file descriptor """

    def __init__(self, packing_deb, file_path, file_format, deb_file_arguments):
        """
        Constructor of the class.

        @type packing_deb: PackagingDeb
        @param packing_deb: The packing deb to be used.
        @type file_path: String
        @param file_path: The path to the file to be used.
        @type file_format: String
        @param file_format: The file format to be used.
        @type deb_file_arguments: Dictionary
        @param deb_file_arguments: The arguments specific for deb files.
        """

        self.packing_deb = packing_deb
        self.file_path = file_path
        self.file_format = file_format
        self.deb_file_arguments = deb_file_arguments

        self.pending_files = []
        self.index_map = {}

    def open(self, mode = DEFAULT_MODE):
        """
        Opens the file in the given mode.

        @type mode: String
        @param mode: The mode to open the file.
        """

        # sets the current mode
        self.mode = mode

        # retrieves the packing ar plugin
        packaging_ar_plugin = self.packing_deb.packaging_deb_plugin.packaging_ar_plugin

        # creates the file
        self.file = packaging_ar_plugin.create_file({FILE_PATH_VALUE : self.file_path})

        # opens the file with the current mode
        self.file.open(mode)

    def close(self):
        """
        Closes the current file, being used.
        """

        # in case the current mode is write
        if self.mode == WRITE_MODE:
            # writes the control
            self._write_control()

            # writes the data
            self._write_data()

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

    def _write_control(self):
        if not "control" in self.deb_file_arguments:
            # raises the missing parameter exception
            raise packaging_deb_exceptions.MissingParameter("control")

        # create a new empty string buffer
        empty_string_buffer = colony.libs.string_buffer_util.StringBuffer(False)

        # retrieves the control strings from the deb file arguments
        # the string can be a path or a file object with the
        # contents of the control file
        control = self.deb_file_arguments["control"]
        conffiles = self.deb_file_arguments.get("conffiles", empty_string_buffer)
        postinst = self.deb_file_arguments.get("postinst", empty_string_buffer)
        postrm = self.deb_file_arguments.get("postrm", empty_string_buffer)
        prerm = self.deb_file_arguments.get("prerm", empty_string_buffer)
        shlibs = self.deb_file_arguments.get("shlibs", empty_string_buffer)

        # retrieves the control files from the control string
        control_file = self._get_file(control)
        conffiles_file = self._get_file(conffiles)
        postinst_file = self._get_file(postinst)
        postrm_file = self._get_file(postrm)
        prerm_file = self._get_file(prerm)
        shlibs_file = self._get_file(shlibs)

        try:
            # creates the string buffer to hold the control file
            control_string_buffer = colony.libs.string_buffer_util.StringBuffer(False)

            # creates the compressed file using the control string buffer as
            # the base file buffer
            compressed_file = tarfile.open(None, CONTROL_FILE_MODE, control_string_buffer)

            # writes the various control files
            self._write_control_file(compressed_file, control_file, "control")
            self._write_control_file(compressed_file, conffiles_file, "conffiles")
            self._write_control_file(compressed_file, postinst_file, "postinst")
            self._write_control_file(compressed_file, postrm_file, "postrm")
            self._write_control_file(compressed_file, prerm_file, "prerm")
            self._write_control_file(compressed_file, shlibs_file, "shlibs")

            # closes the compressed file
            compressed_file.close()

            # writes the control string buffer in the base file
            self.file.write_file(control_string_buffer, "control.tar.gz")

            # closes the control string buffer
            control_string_buffer.close()
        finally:
            # closes the control files
            control_file.close()
            conffiles_file.close()
            postinst_file.close()
            postrm_file.close()
            prerm_file.close()
            shlibs_file.close()

    def _write_control_file(self, compressed_file, file, file_name):
        # creates the file info from the file
        file_info = compressed_file.gettarinfo(fileobj = file)

        # sets the file name in the file info
        file_info.name = file_name

        # adds the file to the compressed file using the
        # given file info
        compressed_file.addfile(file_info, file)

    def _write_data(self):
        # creates the string buffer to hold the data file
        data_string_buffer = colony.libs.string_buffer_util.StringBuffer(False)

        # in case the file format is tar
        if self.file_format == TAR_FILE_FORMAT:
            mode = "w"
        # in case the file format is tar gz
        elif self.file_format == TAR_GZ_FILE_FORMAT:
            mode = "w:gz"
        # in case the file format is tar bz2s
        elif self.file_format == TAR_BZ2_FILE_FORMAT:
            mode = "w:bz2"
        else:
            # raises the invalid file format exception
            raise packaging_deb_exceptions.InvalidFileFormat(self.file_format)

        # creates the compressed file using the data string buffer as
        # the base file buffer
        compressed_file = tarfile.open(None, mode, data_string_buffer)

        # iterates over all the pending files
        for pending_file in self.pending_files:
            # retrieves the pending file descriptor from the index map
            pending_file_descriptor = self.index_map[pending_file]

            # creates a new padding file info (tar info)
            pending_file_info = tarfile.TarInfo()

            # sets the various values of the tar info structure
            pending_file_info.name = pending_file_descriptor.get_name()
            pending_file_info.size = pending_file_descriptor.get_size()
            pending_file_info.mtime = pending_file_descriptor.get_modification_timestamp()
            pending_file_info.mode = pending_file_descriptor.get_mode()
            pending_file_info.type = tarfile.REGTYPE
            pending_file_info.uid = pending_file_descriptor.get_owner_id()
            pending_file_info.gid = pending_file_descriptor.get_group_id()

            # retrieves the pending file buffer
            pending_file_buffer = pending_file_descriptor.get_file()

            # adds the pending file to the compressed file using the
            # given file info
            compressed_file.addfile(pending_file_info, pending_file_buffer)

            # closes the pending file buffer
            pending_file_buffer.close()

        # closes the compressed file
        compressed_file.close()

        # retrieves the file extension base on the current file format
        file_extension = FILE_EXTENSIONS_MAP.get(self.file_format, ".out")

        # writes the file base on the file extension
        self.file.write_file(data_string_buffer, "data" + file_extension)

        # closes the data string buffer
        data_string_buffer.close()

    def _get_file(self, file_value):
        # retrieves the file value type
        file_value_type = type(file_value)

        # in case it is a file path (string value)
        if file_value_type in types.StringTypes:
            # in case the path does not exist
            if not os.path.exists(file_value):
                # raises the file not found exception
                raise packaging_deb_exceptions.FileNotFound("the file paths does not exist: " + file_value)

            # opens the file
            file = open(file_value, DEFAULT_MODE)
        # it must be a file type
        else:
            # sets the file as the file value
            file = file_value

        # returns the file
        return file

    def write(self, file_path, archive_path = None, parameters = {}):
        # in case the path does not exist
        if not os.path.exists(file_path):
            # raises the file not found exception
            raise packaging_deb_exceptions.FileNotFound("the file paths does not exist: " + file_path)

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

        # writes the file to the current file
        self._write_file(file, archive_path, parameters)

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

        # creates the file entry from the file information
        file_entry = DebFileEntry(archive_path, modification_timestamp, owner_id, group_id, mode, size, file)

        # sets the file entry in the index map
        self.index_map[archive_path] = file_entry

        # adds the archive path to the list of pending files
        self.pending_files.append(archive_path)

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

class DebFileEntry:
    """
    The deb file entry class.
    Represents an deb file index entry.
    """

    name = None
    """ The name of the deb file """

    modification_timestamp = None
    """ The modification timestamp """

    owner_id = None
    """ The owner id """

    group_id = None
    """ The group id """

    mode = None
    """ The mode of access to the file """

    size = None
    """ The size of the deb file """

    file = None
    """ The file of the deb file """

    def __init__(self, name = None, modification_timestamp = None, owner_id = None, group_id = None, mode = None, size = None, file = None):
        """
        Constructor of the file.
        """

        self.name = name
        self.modification_timestamp = modification_timestamp
        self.owner_id = owner_id
        self.group_id = group_id
        self.mode = mode
        self.size = size
        self.file = file

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

    def get_file(self):
        """
        Retrieves the file.

        @rtype: File
        @return: The file.
        """

        return self.file

    def set_file(self, file):
        """
        Sets the file.

        @type file: File
        @param file: The file.
        """

        self.file = file
