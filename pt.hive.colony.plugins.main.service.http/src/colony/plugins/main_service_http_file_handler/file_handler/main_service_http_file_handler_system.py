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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import re
import stat
import hashlib
import datetime

import colony.libs.map_util
import colony.libs.path_util
import colony.libs.quote_util
import colony.libs.string_buffer_util

import main_service_http_file_handler_exceptions

HANDLER_NAME = "file"
""" The handler name """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

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

ACCEPT_RANGES_VALUE = "Accept-Ranges"
""" The accept ranges value """

CONTENT_RANGE_VALUE = "Content-Range"
""" The content range value """

LOCATION_VALUE = "Location"
""" The location value """

RANGE_VALUE = "Range"
""" The range value """

BYTES_VALUE = "bytes"
""" The bytes value """

DEFAULT_VALUE = "default"
""" The default value """

FOLDER_TYPE = "folder"
""" The folder type """

FILE_TYPE = "file"
""" The file type """

UNKNOWN_TYPE = "unknown"
""" The unknown type """

ITEM_SORT_MAP = {
    FOLDER_TYPE : 1,
    FILE_TYPE : 2,
    UNKNOWN_TYPE : 3
}
""" Map used for list sorting """

class MainServiceHttpFileHandler:
    """
    The main service http file handler class.
    """

    main_service_http_file_handler_plugin = None
    """ The main service http file handler plugin """

    http_service_directory_list_handler_plugins_map = {}
    """ The http service directory list handler plugins map """

    handler_configuration = {}
    """ The handler configuration """

    def __init__(self, main_service_http_file_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_file_handler_plugin: MainServiceHttpFileHandlerPlugin
        @param main_service_http_file_handler_plugin: The main service http file handler plugin.
        """

        self.main_service_http_file_handler_plugin = main_service_http_file_handler_plugin

        self.http_service_directory_list_handler_plugins_map = {}
        self.handler_configuration = {}

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        """

        # retrieves the format mime plugin
        format_mime_plugin = self.main_service_http_file_handler_plugin.format_mime_plugin

        # retrieves the resource manager plugin
        resource_manager_plugin = self.main_service_http_file_handler_plugin.resource_manager_plugin

        # retrieves the default path
        default_path = self.handler_configuration.get("default_path", "/")

        # retrieves the default page
        default_page = self.handler_configuration.get("default_page", "index.html")

        # retrieves the default relative paths
        relative_paths = self.handler_configuration.get("relative_paths", False)

        # retrieves the base directory for file search
        base_directory = request.properties.get("base_path", default_path)

        # retrieves the default page
        default_page = request.properties.get("default_page", default_page)

        # retrieves the relative paths
        relative_paths = request.properties.get("relative_paths", relative_paths)

        # retrieves the requested resource path
        resource_path = request.get_resource_path_decoded()

        # retrieves the handler path
        handler_path = request.get_handler_path()

        # retrieves the real base directory
        real_base_directory = resource_manager_plugin.get_real_string_value(base_directory)

        # in case the relative paths are disabled
        if not relative_paths:
            # escapes the resource path in the relatives paths
            resource_path = self._escape_relative_paths(resource_path)

        # in case there is a valid handler path
        if handler_path:
            path = resource_path.replace(handler_path, "", 1)
        # otherwise
        else:
            path = resource_path

        # in case the path is the base one
        if path == "/" or path == "":
            path = "/" + default_page

        # retrieves the mime type for the path
        mime_type = format_mime_plugin.get_mime_type_file_name(path)

        # strips the path value from the initial and final slash
        path = path.strip("/")

        # creates the complete path appending the real base
        # directory and the path
        complete_path = os.path.join(real_base_directory, path)

        # normalizes the complete path
        complete_path = os.path.normpath(complete_path)

        # prints a debug message
        self.main_service_http_file_handler_plugin.debug("Trying to retrieve system file '%s'" % complete_path)

        # in case the paths does not exist
        if not os.path.exists(complete_path):
            # raises file not found exception with 404 http error code
            raise main_service_http_file_handler_exceptions.FileNotFoundException(resource_path, 404)

        # retrieves the file stat
        file_stat = os.stat(complete_path)

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
            return

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

        # in case the complete path is a directory
        if os.path.isdir(complete_path):
            # processes the path as a directory
            self._process_directory(request, complete_path)
        # otherwise
        else:
            # processes the path as a file
            self._process_file(request, complete_path)

    def http_service_directory_list_handler_load(self, http_service_directory_list_handler_plugin):
        # retrieves the plugin directory list handler name
        directory_list_handler_name = http_service_directory_list_handler_plugin.get_directory_list_handler_name()

        self.http_service_directory_list_handler_plugins_map[directory_list_handler_name] = http_service_directory_list_handler_plugin

    def http_service_directory_list_handler_unload(self, http_service_directory_list_handler_plugin):
        # retrieves the plugin directory list handler name
        directory_list_handler_name = http_service_directory_list_handler_plugin.get_directory_list_handler_name()

        del self.http_service_directory_list_handler_plugins_map[directory_list_handler_name]

    def set_handler_configuration_property(self, handler_configuration_property):
        # retrieves the handler configuration
        handler_configuration = handler_configuration_property.get_data()

        # cleans the handler configuration
        colony.libs.map_util.map_clean(self.handler_configuration)

        # copies the handler configuration to the handler configuration
        colony.libs.map_util.map_copy(handler_configuration, self.handler_configuration)

    def unset_handler_configuration_property(self):
        # cleans the handler configuration
        colony.libs.map_util.map_clean(self.handler_configuration)

    def default_directory_list_handler(self, request, directory_list):
        """
        The default directory list handler for exception sending.

        @type request: HttpRequest
        @param request: The request to send the directory list.
        @type directory_list: List
        @param directory_list: The list of directory entries.
        """

        # sets the request content type
        request.content_type = "text/plain"

        # retrieves the resource base path
        resource_base_path = request.get_resource_base_path_decoded()

        # strips the resource base path
        resource_base_path = resource_base_path.strip("/")

        # writes the header message in the message
        request.write("directory listing - " + resource_base_path + "\n")

        # retrieves the directory entries
        directory_entries = directory_list["entries"]

        # iterates over all the directory entries in the directory
        # entries (list) to write their values in the request
        for directory_entry in directory_entries:
            # retrieves the directory entry name
            directory_entry_name = directory_entry["name"]

            # writes the directory entry name
            request.write(directory_entry_name + "\n")

    def _process_directory(self, request, complete_path):
        """
        Processes a directory request for the given complete
        path and request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        @type complete_path: String
        @param complete_path: The complete path to the directory.
        """

        # retrieves the requested resource base path
        resource_base_path = request.get_resource_base_path_decoded()

        # in case the resource base path does not end with a slash
        if not resource_base_path.endswith("/"):
            # adds the extra slash to the resource base path
            # in order to avoid file redirection problems
            resource_path = resource_base_path.encode(DEFAULT_CHARSET) + "/"

            # redirects the request to the resource path
            self._redirect(request, resource_path)

            # returns immediately
            return

        # retrieves the directory names for the complete path
        directory_names = os.listdir(complete_path)

        # creates a list for the directory entries
        directory_entries = []

        # iterates over all the directory names
        for directory_name in directory_names:
            # creates the complete file path
            file_path = complete_path + "/" + directory_name

            # normalizes the file path
            file_path =  colony.libs.path_util.normalize_path(file_path)

            # retrieves the file stat
            file_stat = os.stat(file_path)

            # retrieves the file properties
            file_size = file_stat[stat.ST_SIZE]
            file_modified_date = datetime.datetime.fromtimestamp(file_stat[stat.ST_MTIME])

            # retrieves the file mode
            file_mode = file_stat[stat.ST_MODE]

            # in case the file is of type directory or link
            if stat.S_ISDIR(file_mode) or stat.S_ISLNK(file_mode):
                file_type = FOLDER_TYPE
                file_size = 0
            # in case the file is of type register
            elif stat.S_ISREG(file_mode):
                file_type = FILE_TYPE
            # otherwise
            else:
                file_type = UNKNOWN_TYPE

            # creates the file entry
            file_entry = {}

            # sets the file entry values
            file_entry["name"] = directory_name
            file_entry["size"] = file_size
            file_entry["modified_date"] = file_modified_date
            file_entry["type"] = file_type

            # adds the file entry to the directory entries
            directory_entries.append(file_entry)

        # retrieves the comparator attribute from the request
        comparator = request.get_attribute("comparator") or "name"

        # generates a new comparator method using the comparator string
        comparator_method = self.generate_comparator(comparator)

        # sorts the directory entries
        directory_entries.sort(comparator_method)
        directory_entries.sort(self.type_comparator)

        # creates the directory list structure
        directory_list = {}

        # sets the entries in the directory list structure
        directory_list["entries"] = directory_entries
        directory_list["comparator"] = comparator

        # handles the directory list
        self._handle_directory_list(self.handler_configuration, request, directory_list)

    def _process_file(self, request, complete_path):
        """
        Processes a file request for the given complete
        path and request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        @type complete_path: String
        @param complete_path: The complete path to the file.
        """

        # opens the requested file
        file = open(complete_path, "rb")

        # retrieves the file size
        file_size = os.path.getsize(complete_path)

        # processes and retrieves the ranges to be used
        ranges = self._process_ranges(request, file_size)

        # in case the file size is bigger than
        # the chunk file size limit
        if file_size > CHUNK_FILE_SIZE_LIMIT:
            # creates the chunk handler instance
            chunk_handler = ChunkHandler(file, file_size, ranges)

            # processes the ranges value in the chunk handler
            chunk_handler.process_ranges()

            # sets the request as mediated
            request.mediated = True

            # sets the mediated handler in the request
            request.mediated_handler = chunk_handler
        # otherwise it's a small file and may be read
        # completely on the request handler
        else:
            # reads the file contents
            file_contents = file.read()

            # closes the file
            file.close()

            # writes the file contents
            request.write(file_contents, 1, False)

    def _handle_directory_list(self, handler_configuration, request, directory_list):
        # retrieves the preferred directory list handlers list
        preferred_directory_list_handlers_list = handler_configuration.get("preferred_directory_list_handlers", (DEFAULT_VALUE,))

        # retrieves the http service directory list handler plugins map
        http_service_directory_list_handler_plugins_map = self.http_service_directory_list_handler_plugins_map

        # iterates over all the preferred directory list handlers
        for preferred_directory_list_handler in preferred_directory_list_handlers_list:
            # in case the preferred directory list handler is the default one
            if preferred_directory_list_handler == DEFAULT_VALUE:
                # handles the directory list with the default directory list handler
                self.default_directory_list_handler(request, directory_list)

                # breaks the loop
                break
            else:
                # in case the preferred directory list handler exist in the http service
                # directory list handler plugins map
                if preferred_directory_list_handler in http_service_directory_list_handler_plugins_map:
                    # retrieves the http service directory list handler plugin
                    http_service_directory_list_handler_plugin = http_service_directory_list_handler_plugins_map[preferred_directory_list_handler]

                    # calls the handle directory list in the http service directory list handler plugin
                    http_service_directory_list_handler_plugin.handle_directory_list(request, directory_list)

                    # breaks the loop
                    break

    def _redirect(self, request, target_path, status_code = 301, quote = True):
        """
        Redirects the given request to the target path.

        @type request: HttpRequest
        @param request: The http request to be handled.
        @type target_path: String
        @param target_path: The target path of the redirection.
        @type status_code: int
        @param status_code: The status code to be used.
        @type quote: bool
        @param quote: If the target path should be quoted.
        """

        # quotes the target path
        target_path_quoted = quote and colony.libs.quote_util.quote(target_path, "/") or target_path

        # sets the status code
        request.status_code = status_code

        # sets the location header (using the quoted target path)
        request.set_header(LOCATION_VALUE, target_path_quoted)

    def _process_ranges(self, request, file_size):
        """
        Processes the ranges for the given request,
        using the given file size.

        @type request: HttpRequest
        @param request: The http request to used in the processing.
        @type file_size: int
        @param file_size: The size of the file to be used.
        """

        # sets the accept ranges header
        request.set_header(ACCEPT_RANGES_VALUE, BYTES_VALUE)

        # retrieves the range header
        range_header = request.get_header(RANGE_VALUE)

        # in case there is no range header
        if not range_header:
            # returns immediately
            return None

        # splits the range header retrieving the key
        # and the values
        key, values = range_header.split("=")

        # in case the key is not bytes
        if not key == BYTES_VALUE:
            # return immediately
            return None

        # splits the values retrieving the range values
        range_values = values.split(",")

        # creates the list of ranges in number mode
        ranges_number_list = []

        # iterates over all the range values
        for range_value in range_values:
            # splits the range retrieving the initial value
            # and the end value
            initial_value, end_value = range_value.split("-")

            # converts both the initial and the end values to number
            initial_value_number = initial_value and int(initial_value) or - 1
            end_value_number = end_value and int(end_value) or - 1

            # creates the range number tuple with both the initial and end values
            range_number_tuple = (
                initial_value_number,
                end_value_number
            )

            # adds the range number tuple to the ranges number list
            ranges_number_list.append(range_number_tuple)

        # retrieves the length of the ranges number list
        ranges_number_list_length = len(ranges_number_list)

        # in case the length of the ranges number list
        # is bigger than one, the feature is not implemented
        if ranges_number_list_length > 1:
            # raises the not implemented exception
            raise main_service_http_file_handler_exceptions.NotImplementedException("no support for multiple ranges", 501)

        # retrieves the first range value
        first_range_value = ranges_number_list[0]

        # converts the first range value to string
        first_range_string_value = self._range_to_string(first_range_value, file_size)

        # sets the content range header value
        request.set_header(CONTENT_RANGE_VALUE, first_range_string_value)

        # sets the request status code
        request.status_code = 206

        # returns the ranges number list
        return ranges_number_list

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

    def _range_to_string(self, range_value, file_size):
        """
        Converts the given range value to a string value,
        using the given file size as reference.

        @type range_value: Tuple
        @param range_value: The range value to be converted to string.
        @type file_size: int
        @param file_size: The size of the file to be used as reference.
        @rtype: String
        @return: The string value for the range.
        """

        # creates a string buffer to hold the range
        range_string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # retrieves the range initial and end values
        initial_value, end_value = range_value

        # writes the initial part
        range_string_buffer.write(BYTES_VALUE)
        range_string_buffer.write(" ")

        # converts both the initial and end values to string
        initial_value_string = initial_value == -1 and "0" or str(initial_value)
        end_value_string = end_value == -1 and str(file_size - 1) or str(end_value)

        # writes the initial and end values to the range string buffer
        range_string_buffer.write(initial_value_string)
        range_string_buffer.write("-")
        range_string_buffer.write(end_value_string)

        # writes the final file size part in the
        # the range string buffer
        range_string_buffer.write("/")
        range_string_buffer.write(str(file_size))

        # retrieves the range string value
        range_string_value = range_string_buffer.get_value()

        # returns the range string value
        return range_string_value

    def type_comparator(self, first_item, second_item):
        """
        Comparator based on the type of the items.

        @type first_item: Object
        @param first_item: The first item to be compared.
        @type second_item: Object
        @param second_item: The second item to be compared.
        @rtype: int
        @return: The result of the comparison.
        """

        # retrieves the item types
        first_item_type = first_item["type"]
        second_item_type = second_item["type"]

        # retrieves the difference between the item values
        return ITEM_SORT_MAP[first_item_type] - ITEM_SORT_MAP[second_item_type]

    def generate_comparator(self, reference):
        """
        Generates a method that can be used as a comparator.

        @type reference: String
        @param reference: The refernce value to the comparison.
        """

        def comparator(first_item, second_item):
            """
            Comparator function to that returns the result
            of the comparison between two item.

            @type first_item: Object
            @param first_item: The first item to be compared.
            @type second_item: Object
            @param second_item: The second item to be compared.
            @rtype: int
            @return: The result of the comparison.
            """

            # retrieves the item values
            first_item_value = first_item[reference]
            second_item_value = second_item[reference]

            # returns the result of the comparison of the
            # first and second item values
            return cmp(first_item_value, second_item_value)

        # returns the comparator method
        return comparator

class ChunkHandler:
    """
    The chunk handler class.
    """

    file = None
    """ The file """

    file_size = None
    """ The file size """

    ranges = None
    """ The list of ranges """

    def __init__(self, file, file_size, ranges):
        """
        Constructor of the class.

        @type file: File
        @param file: The file.
        @type file_size: int
        @param file_size: The file size.
        @type ranges: List
        @param ranges: The list of ranges.
        """

        self.file = file
        self.file_size = file_size
        self.ranges = ranges

    def process_ranges(self):
        """
        Processes the ranges of the file request.
        """

        # in case no ranges are defined
        if not self.ranges:
            # returns immediately
            return

        # retrieves the first range
        first_range = self.ranges[0]

        # retrieves both the initial and end value
        # from the first range
        initial_value, _end_value = first_range

        # in case the initial value is valid
        if not initial_value == -1:
            # seeks the file into the initial value
            self.file.seek(initial_value)

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

        return self.file.read(chunk_size)

    def close(self):
        """
        Closes the chunked handler.
        """

        # closes the file
        self.file.close()
