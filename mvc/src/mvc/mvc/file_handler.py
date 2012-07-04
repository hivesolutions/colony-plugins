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

import os
import re
import stat
import hashlib

import colony.libs.string_buffer_util

import exceptions

CHUNK_FILE_SIZE_LIMIT = 4096
""" The chunk file size limit """

CHUNK_SIZE = 1024
""" The chunk size """

EXPIRATION_DELTA_TIMESTAMP = 31536000
""" The expiration delta timestamp """

INVALID_EXPIRATION_STRING_VALUE = "-1"
""" The invalid expiration string value """

RELATIVE_PATHS_REGEX_VALUE = "^\.\.|\/\.\.\/|\\\.\.\\|\.\.$"
""" The relative paths regex value """

RELATIVE_PATHS_REGEX = re.compile(RELATIVE_PATHS_REGEX_VALUE)
""" The relative paths regex """

class MvcFileHandler:
    """
    The mvc file handler class.
    """

    mvc_plugin = None
    """ The mvc plugin """

    def __init__(self, mvc_plugin):
        """
        Constructor of the class.

        @type mvc_plugin: MvcPlugin
        @param mvc_plugin: The mvc plugin
        """

        self.mvc_plugin = mvc_plugin

    def handle_request(self, request, file_path):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the format mime plugin
        format_mime_plugin = self.mvc_plugin.format_mime_plugin

        # retrieves the associated mime type
        mime_type = format_mime_plugin.get_mime_type_file_name(file_path)

        # in case the file path does not exist
        if not os.path.exists(file_path):
            # raises file not found exception with 404 http error code
            raise exceptions.FileNotFoundException(file_path, 404)

        # retrieves the file stat
        file_stat = os.stat(file_path)

        # retrieves the modified timestamp
        modified_timestamp = file_stat[stat.ST_MTIME]

        # computes the etag value base in the file stat and
        # modified timestamp
        etag_value = self._compute_etag(file_stat, modified_timestamp)

        # verifies the resource to validate any modification
        if not request.verify_resource_modification(modified_timestamp, etag_value):
            # sets the request mime type
            request.content_type = mime_type

            # sets the request status code
            request.status_code = 304

            # returns immediately
            return True

        # calculates the expiration timestamp from the modified timestamp
        # incrementing the delta timestamp for expiration
        expiration_timestamp = modified_timestamp + EXPIRATION_DELTA_TIMESTAMP

        # sets the request mime type
        request.content_type = mime_type

        # sets the request status code
        request.status_code = 200

        # sets the last modified timestamp
        request.set_last_modified_timestamp(modified_timestamp)

        # sets the expiration timestamp in the request
        request.set_expiration_timestamp(expiration_timestamp)

        # sets the etag in the request
        request.set_etag(etag_value)

        # opens the requested file
        file = open(file_path, "rb")

        # retrieves the file size
        file_size = os.path.getsize(file_path)

        # in case the file size is bigger than
        # the chunk file size limit
        if file_size > CHUNK_FILE_SIZE_LIMIT:
            # creates the chunk handler instance
            chunk_handler = ChunkHandler(file, file_size)

            # sets the request as mediated
            request.mediated = True

            # sets the mediated handler in the request
            request.mediated_handler = chunk_handler
        else:
            # reads the file contents
            file_contents = file.read()

            # closes the file
            file.close()

            # writes the file contents
            request.write(file_contents, 1, False)

        return True

    def _compute_etag(self, file_stat, modified_timestamp):
        """
        Computes the etag for the given file stat and
        modified timestamp.

        @type file_stat: Dictionary
        @param file_stat: The file stat values dictionary.
        @type modified_timestamp: int
        @param modified_timestamp: The last modified timestamp.
        @rtype: String
        @return: The etag value.
        """

        # retrieves the md5 builder
        md5 = hashlib.md5()

        # retrieves the size
        size = file_stat[stat.ST_SIZE]

        # creates the modification plus size string
        modification_size_string = str(modified_timestamp + size)

        # updates the md5 hash with the modification
        # plus size string
        md5.update(modification_size_string)

        # retrieves the md5 hex digest as the etag value
        etag_value = md5.hexdigest()

        # returns the etag value
        return etag_value

    def _escape_relative_paths(self, path):
        """
        Escapes the relative path values in the given path.

        @type path: String
        @param path: The path to be escaped.
        @rtype: String
        @return: The escaped path.
        """

        # escapes the paths in the relative paths value
        escaped_path = RELATIVE_PATHS_REGEX.sub("", path)

        # returns the escaped path
        return escaped_path

class ChunkHandler:
    """
    The chunk handler class.
    """

    file = None
    """ The file """

    file_size = None
    """ The file size """

    _closed = False
    """ The falg that controls the close state of the chunk handler """

    def __init__(self, file, file_size):
        """
        Constructor of the class.

        @type file: File
        @param file: The file.
        @type file_size: int
        @param file_size: The file size.
        """

        self.file = file
        self.file_size = file_size

    def encode_file(self, encoding_handler, encoding_name):
        """
        Encodes the file using the given encoding handler with the given name.

        @type encoding_handler: Method
        @param encoding_handler: The encoding handler method to be used.
        @type encoding_name: String
        @param encoding_name: The name of the encoding to be used.
        """

        # reads the file contents
        file_contents = self.file.read()

        # encodes the file contents using the given encoding handler
        file_contents_encoded = encoding_handler(file_contents)

        # creates a new string buffer to used as a memory file
        # for the encoded file
        file_contents_encoded_file_buffer = colony.libs.string_buffer_util.StringBuffer(False)

        # writes the file contents encoded into the file contents
        # file buffer
        file_contents_encoded_file_buffer.write(file_contents_encoded)

        # sets the new file
        self.file = file_contents_encoded_file_buffer

        # sets the new file size
        self.file_size = file_contents_encoded_file_buffer.tell()

        # seeks to the beginning of the file
        file_contents_encoded_file_buffer.seek(0)

    def get_size(self):
        """
        Retrieves the size of the file being chunked.

        @rtype: int
        @return: The size of the file being chunked.
        """

        return self.file_size

    def get_chunk(self, chunk_size = CHUNK_SIZE):
        """
        Retrieves the a chunk with the given size.

        @rtype: chunk_size
        @return: The size of the chunk to be retrieved.
        @rtype: String
        @return: A chunk with the given size.
        """

        # in case the chunk handler is
        # currently closed
        if self._closed:
            # returns none (nothing to be retrieved
            # from a closed chunk handler)
            return None

        return self.file.read(chunk_size)

    def close(self):
        """
        Closes the chunked handler.
        """

        # in case the chunk handler is already closed
        if self._closed:
            # returns immediately
            return

        # sets the closed flag
        self._closed = True

        # closes the file
        self.file.close()
