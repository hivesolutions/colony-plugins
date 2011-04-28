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
import time
import types
import tarfile
import hashlib

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

CONTROL_VALUE = "control"
""" The control value """

CONFFILES_VALUE = "conffiles"
""" The conffiles value """

CONFIG_VALUE = "config"
""" The config value """

POSTINST_VALUE = "postinst"
""" The postinst value """

POSTRM_VALUE = "postrm"
""" The postrm value """

PRERM_VALUE = "prerm"
""" The prerm value """

SHLIBS_VALUE = "shlibs"
""" The shlibs value """

MD5SUMS_VALUE = "md5sums"
""" The md5sums value """

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

FILE_EXTENSIONS_MAP = {
    TAR_FILE_FORMAT : ".tar",
    TAR_GZ_FILE_FORMAT : ".tar.gz",
    TAR_BZ2_FILE_FORMAT : ".tar.bz2",
    TAR_BZ2_FILE_FORMAT : ".tar.lzma"
}
""" The file extensions map """

CONTROL_FILE_MODE = "w:gz"
""" The control file mode """

CONTROL_FILE_READ_MODE = "r:gz"
""" The control file read mode """

BUFFER_SIZE = 1024
""" The size of the buffer """

DEBIAN_BINARY_VALUE = "2.0\n"
""" The debian binary value """

REGISTER_TYPE = "register"
""" The register type """

LINK_TYPE = "link"
""" The link type """

DIRECTORY_TYPE = "directory"
""" The directory type """

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

    debian_binary = None
    """ The debian binary value """

    pending_files = []
    """ The list of pending files to be flushed """

    index_map = {}
    """ The index map associating the archive path with the file descriptor """

    md5_map = {}
    """ The map associating the archive path with the md5 value """

    control_map = {}
    """ The map containing the control file contents """

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
        self.md5_map = {}
        self.control_map = {}

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

        # defines the file parameters
        file_parameters = {
            FILE_PATH_VALUE : self.file_path
        }

        # creates the file
        self.file = packaging_ar_plugin.create_file(file_parameters)

        # opens the file with the current mode
        self.file.open(mode)

        # in case the current mode is read
        if self.mode == READ_MODE:
            # reads the debian binary
            self._read_debian_binary()

            # reads the control
            self._read_control()

    def close(self):
        """
        Closes the current file, being used.
        """

        # in case the current mode is write
        if self.mode == WRITE_MODE:
            # writes the debian binary
            self._write_debian_binary()

            # writes the control
            self._write_control()

            # writes the data
            self._write_data()

        # closes the current file
        self.file.close()

    def extract_all(self, target_path, parameters = {}):
        pass

    def write(self, file_path, archive_path = None, parameters = {}):
        # in case the path does not exist
        if not os.path.exists(file_path):
            # raises the file not found exception
            raise packaging_deb_exceptions.FileNotFound("the file path does not exist: " + file_path)

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

        # normalizes the mode removing the extra parameters
        mode = stat.S_IMODE(mode)

        # tries to retrieve the file properties
        file_properties = parameters.get(FILE_PROPERTIES_VALUE, {})

        # sets the file properties values
        file_properties["modification_timestamp"] = file_properties.get("modification_timestamp", modification_timestamp)
        file_properties["owner_id"] = file_properties.get("owner_id", owner_id)
        file_properties["group_id"] = file_properties.get("group_id", group_id)
        file_properties["mode"] = file_properties.get("mode", mode)
        file_properties["size"] = file_properties.get("size", size)

        # sets the file properties in the parameters
        parameters[FILE_PROPERTIES_VALUE] = file_properties

        # opens the file for reading
        file = open(file_path, "rb")

        # "writes" the file to the current file
        self._write_file(file, archive_path, parameters)

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

    def write_register_value(self, archive_path, parameters = {}):
        # creates the string buffer to hold the string value
        string_buffer = colony.libs.string_buffer_util.StringBuffer(False)

        # writes the file to the current file
        self._write_file(string_buffer, archive_path, parameters)

    def read(self, archive_path, parameters = {}):
        pass

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

    def get_debian_binary(self):
        """
        Retrieves the debian binary.

        @rtype: String
        @return: The debian binary.
        """

        return self.debian_binary

    def get_control_map(self):
        """
        Retrieves the control map.

        @rtype: Dictionary
        @return: The control map.
        """

        return self.control_map

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
        type = file_properties.get("type", REGISTER_TYPE)
        link_name = file_properties.get("link_name", "")
        owner_id = file_properties.get("owner_id", 0)
        group_id = file_properties.get("group_id", 0)
        mode = file_properties.get("mode", 0)
        size = file_properties.get("size", 0)

        # creates the file entry from the file information
        file_entry = DebFileEntry(archive_path, modification_timestamp, type, link_name, owner_id, group_id, mode, size, file)

        # sets the file entry in the index map
        self.index_map[archive_path] = file_entry

        # adds the archive path to the list of pending files
        self.pending_files.append(archive_path)

    def _write_debian_binary(self):
        """
        Writes the debian binary file to the
        current file.
        """

        # writes the debian binary value in the base file
        self.file.write_string_value(DEBIAN_BINARY_VALUE, "debian-binary")

    def _write_control(self):
        """
        Writes the control file to the
        current file.
        """

        if not CONTROL_VALUE in self.deb_file_arguments:
            # raises the missing parameter exception
            raise packaging_deb_exceptions.MissingParameter(CONTROL_VALUE)

        # create a new empty string buffer
        empty_string_buffer = colony.libs.string_buffer_util.StringBuffer(False)

        # retrieves the control strings from the deb file arguments
        # the string can be a path or a file object with the
        # contents of the control file
        control = self.deb_file_arguments[CONTROL_VALUE]
        conffiles = self.deb_file_arguments.get(CONFFILES_VALUE, empty_string_buffer)
        config = self.deb_file_arguments.get(CONFIG_VALUE, empty_string_buffer)
        postinst = self.deb_file_arguments.get(POSTINST_VALUE, empty_string_buffer)
        postrm = self.deb_file_arguments.get(POSTRM_VALUE, empty_string_buffer)
        prerm = self.deb_file_arguments.get(PRERM_VALUE, empty_string_buffer)
        shlibs = self.deb_file_arguments.get(SHLIBS_VALUE, empty_string_buffer)

        # retrieves the control files from the control string
        control_file = self._get_file(control)
        conffiles_file = self._get_file(conffiles)
        config_file = self._get_file(config)
        postinst_file = self._get_file(postinst)
        postrm_file = self._get_file(postrm)
        prerm_file = self._get_file(prerm)
        shlibs_file = self._get_file(shlibs)
        md5sums_file = self._generate_md5_sums_file()

        try:
            # creates the string buffer to hold the control file
            control_string_buffer = colony.libs.string_buffer_util.StringBuffer(False)

            # creates the compressed file using the control string buffer as
            # the base file buffer
            compressed_file = tarfile.open(None, CONTROL_FILE_MODE, control_string_buffer)

            # writes the various control files
            self._write_control_file(compressed_file, control_file, CONTROL_VALUE)
            self._write_control_file(compressed_file, conffiles_file, CONFFILES_VALUE)
            self._write_control_file(compressed_file, config_file, CONFIG_VALUE)
            self._write_control_file(compressed_file, postinst_file, POSTINST_VALUE)
            self._write_control_file(compressed_file, postrm_file, POSTRM_VALUE)
            self._write_control_file(compressed_file, prerm_file, PRERM_VALUE)
            self._write_control_file(compressed_file, shlibs_file, SHLIBS_VALUE)
            self._write_control_file(compressed_file, md5sums_file, MD5SUMS_VALUE)

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

    def _write_data(self):
        """
        Writes the data file to the
        current file.
        """

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
            pending_file_info.type = pending_file_descriptor.get_tar_type()
            pending_file_info.linkname = pending_file_descriptor.get_link_name()
            pending_file_info.uid = pending_file_descriptor.get_owner_id()
            pending_file_info.gid = pending_file_descriptor.get_group_id()

            # retrieves the pending file buffer
            pending_file_buffer = pending_file_descriptor.get_file()

            # goes to the beginning of the file buffer
            pending_file_buffer.seek(0, os.SEEK_SET)

            # adds the pending file to the compressed file using the
            # given file info
            compressed_file.addfile(pending_file_info, pending_file_buffer)

            # closes the pending file buffer
            pending_file_buffer.close()

        # closes the compressed file
        compressed_file.close()

        # retrieves the file extension base on the current file format
        file_extension = FILE_EXTENSIONS_MAP.get(self.file_format, ".out")

        # writes the data string buffer in the base file
        self.file.write_file(data_string_buffer, "data" + file_extension)

        # closes the data string buffer
        data_string_buffer.close()

    def _write_control_file(self, compressed_file, file, file_name):
        """
        Writes the given control file to the given
        compressed file with the given name.

        @type compressed_file: TarFile
        @param compressed_file: The compressed file to write the
        current file.
        @type file: File
        @param file: The file to write into the compressed file.
        @type file_name: String
        @param file_name: The name of the file to be used in the compressed
        file.
        """

        # creates a new file info (tar info)
        file_info = tarfile.TarInfo()

        # forwards the file to the end position
        file.seek(0, os.SEEK_END)

        # retrieves the current offset (file size)
        file_size = file.tell()

        # rewinds the file to the initial position
        file.seek(0, os.SEEK_SET)

        # sets the various values of the tar info structure
        file_info.name = file_name
        file_info.size = file_size
        file_info.mtime = int(time.time())
        file_info.mode = 0
        file_info.type = tarfile.REGTYPE
        file_info.uid = 0
        file_info.gid = 0

        # adds the file to the compressed file using the
        # given file info
        compressed_file.addfile(file_info, file)

    def _read_debian_binary(self):
        """
        Reads the debian binary from the
        current file.
        """

        # reads the debian binary value from the base file
        self.debian_binary = self.file.read("debian-binary")

    def _read_control(self):
        """
        Reads the control file from the
        current file.
        """

        # retrieves the control contents
        control_contents = self.file.read("control.tar.gz")

        # creates the control contents buffer to hold the control contents value
        control_contents_buffer = colony.libs.string_buffer_util.StringBuffer(False)

        # writes the control contents to the control contents buffer
        control_contents_buffer.write(control_contents)

        # rewinds the control contents buffer to the initial position
        control_contents_buffer.seek(0, os.SEEK_SET)

        # reads the control value from the base file
        file = tarfile.open(None, CONTROL_FILE_READ_MODE, control_contents_buffer)

        # retrieves the names in the file
        names = file.getnames()

        # extracts the various control files
        control_file_contents = CONTROL_VALUE in names and file.extractfile(CONTROL_VALUE).read() or ""
        conffiles_file_contents = CONFFILES_VALUE in names and file.extractfile(CONFFILES_VALUE).read() or ""
        config_file_contents = CONFIG_VALUE in names and file.extractfile(CONFIG_VALUE).read() or ""
        postinst_file_contents = POSTINST_VALUE in names and file.extractfile(POSTINST_VALUE).read() or ""
        postrm_file_contents = POSTRM_VALUE in names and file.extractfile(POSTRM_VALUE).read() or ""
        prerm_file_contents = PRERM_VALUE in names and file.extractfile(PRERM_VALUE).read() or ""
        shlibs_file_contents = SHLIBS_VALUE in names and file.extractfile(SHLIBS_VALUE).read() or ""
        md5sums_file_contents = MD5SUMS_VALUE in names and file.extractfile(MD5SUMS_VALUE).read() or ""

        # sets the control file contents in the control map
        self.control_map[CONTROL_VALUE] = control_file_contents
        self.control_map[CONFFILES_VALUE] = conffiles_file_contents
        self.control_map[CONFIG_VALUE] = config_file_contents
        self.control_map[POSTINST_VALUE] = postinst_file_contents
        self.control_map[POSTRM_VALUE] = postrm_file_contents
        self.control_map[PRERM_VALUE] = prerm_file_contents
        self.control_map[SHLIBS_VALUE] = shlibs_file_contents
        self.control_map[MD5SUMS_VALUE] = md5sums_file_contents

    def _generate_md5_sums_file(self):
        """
        Generates and returns the md5 sums file,
        to be used in the control.

        @rtype: File
        @return: The md5 sums file.
        """

        # updates the md5 index
        self._update_md5_index()

        # creates the string buffer to hold the md5 sums file
        string_value = colony.libs.string_buffer_util.StringBuffer(False)

        # iterates over all the items in the md5 map
        for archive_path, md5_value in self.md5_map.items():
            # writes the md5 value
            string_value.write(md5_value)

            # writes a space
            string_value.write(" ")

            # writes the archive path
            string_value.write(archive_path)

            # writes a newline
            string_value.write("\n")

        # returns the string value (md5 sums file)
        return string_value

    def _update_md5_index(self):
        """
        Updates the md5 index, computing
        all the md5 values for the pending files.
        """

        # iterates over all the pending files
        for pending_file in self.pending_files:
            # retrieves the pending file descriptor from the index map
            pending_file_descriptor = self.index_map[pending_file]

            # calculates the md5 value for the file
            pending_file_md5 = pending_file_descriptor.compute_md5()

            # sets the md5 in the md5 map
            self.md5_map[pending_file] = pending_file_md5

    def _get_file(self, file_value):
        """
        Retrieves the file for the given file value.
        In case the file value is a string a file in the path
        described in the string is return, in case the file value
        is a file this file is returned.

        @type file_value: String/File
        @param file_value: The file value to be interpreted.
        @rtype: File
        @return: The file corresponding to the given string value.
        """

        # retrieves the file value type
        file_value_type = type(file_value)

        # in case it is a file path (string value)
        if file_value_type in types.StringTypes:
            # in case the path does not exist
            if not os.path.exists(file_value):
                # raises the file not found exception
                raise packaging_deb_exceptions.FileNotFound("the file path does not exist: " + file_value)

            # opens the file
            file = open(file_value, DEFAULT_MODE)
        # it must be a file type
        else:
            # sets the file as the file value
            file = file_value

        # returns the file
        return file

class DebFileEntry:
    """
    The deb file entry class.
    Represents an deb file index entry.
    """

    name = None
    """ The name of the deb file """

    modification_timestamp = None
    """ The modification timestamp """

    type = None
    """ The type of the entry """

    link_name = None
    """ The link name for file link """

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

    def __init__(self, name = None, modification_timestamp = None, type = None, link_name = None, owner_id = None, group_id = None, mode = None, size = None, file = None):
        """
        Constructor of the file.

        @type name: String
        @param name: The name of the deb file.
        @type modification_timestamp: int
        @param modification_timestamp: The modification timestamp.
        @type type: String
        @param type: The type of the entry.
        @type link_name: String
        @param link_name: The link name for file link.
        @type owner_id: int
        @param owner_id: The owner id.
        @type group_id: int
        @param group_id: The group id.
        @type mode: int
        @param mode: The mode of access to the file.
        @type size: int
        @param size: The size of the deb file.
        @type file: File
        @param file: The file of the deb file.
        """

        self.name = name
        self.modification_timestamp = modification_timestamp
        self.type = type
        self.link_name = link_name
        self.owner_id = owner_id
        self.group_id = group_id
        self.mode = mode
        self.size = size
        self.file = file

    def compute_md5(self):
        """
        Calculates the md5 for the current file, and
        returns the hexadecimal string value.

        @rtype: String
        @return: The hexadeciaml value of the md5 value.
        """

        # goes to the beginning of the file
        self.file.seek(0, os.SEEK_SET)

        # create the md5 structure
        md5_structure = hashlib.md5()

        # loops indefinitely
        while True:
            # reads the file contents
            file_contents = self.file.read(BUFFER_SIZE)

            # in case there are no file contents,
            # the end of file is reached
            if not file_contents:
                # breaks the loop
                break

            # updates the md5 structure with the file contents
            md5_structure.update(file_contents)

        # retrieves the md5 in hexadecimal string value
        md5_hexadecimal = md5_structure.hexdigest()

        # returns the md5 in hexadecimal
        return md5_hexadecimal

    def get_tar_type(self):
        """
        Retrieves the tar type for the
        currently selected type.

        @rtype: int
        @return: The tar type for the currently
        selected type.
        """

        if self.type == REGISTER_TYPE:
            return tarfile.REGTYPE
        elif self.type == LINK_TYPE:
            return tarfile.SYMTYPE
        elif self.type == DIRECTORY_TYPE:
            return tarfile.DIRTYPE

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

    def get_type(self):
        """
        Retrieves the type.

        @rtype: String
        @return: The type.
        """

        return self.type

    def set_type(self, type):
        """
        Sets the type.

        @type type: String
        @param type: The type.
        """

        self.type = type

    def get_link_name(self):
        """
        Retrieves the link name.

        @rtype: String
        @return: The link name.
        """

        return self.link_name

    def set_link_name(self, link_name):
        """
        Sets the link name.

        @type link_name: String
        @param link_name: The link name.
        """

        self.link_name = link_name

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

        return self.mode

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
