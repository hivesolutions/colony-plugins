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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

import copy

DIRECTORY_LIST_HANDLER_NAME = "template"
""" The error handler name """

HTML_MIME_TYPE = "text/html"
""" The html mime type """

TEMPLATE_DIRECTORY_LIST_HANDLER_RESOURCES_PATH = "main_service_http_template_directory_list_handler/template_directory_list_handler/resources"
""" The template directory list handler resources path """

HTTP_SERVICE_DIRECTORY_LIST_HTML_TEMPLATE_FILE_NAME = "http_service_directory_list.html.tpl"
""" The http service directory list html template file name """

SIZE_UNITS_LIST = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
""" The size units list """

SIZE_UNIT_COEFFICIENT = 1024
""" The size unit coefficient """

DEFAULT_MINIMUM = 1000
""" The default minimum value """

FORMATS_MAP = {"table" : "",
               "mosaic" : "",
               "thumbnail" : ""}
""" The formats map """

class MainServiceHttpTemplateDirectoryListHandler:
    """
    The main service http template directory list handler class.
    """

    main_service_http_template_directory_list_handler_plugin = None
    """ The main service http template directory list handlers plugin """

    def __init__(self, main_service_http_template_directory_list_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_template_directory_list_handler_plugin: MainServiceHttpTemplateDirectoryListHandlerPlugin
        @param main_service_http_template_directory_list_handler_plugin: The main service http template directory list handler plugin.
        """

        self.main_service_http_template_directory_list_handler_plugin = main_service_http_template_directory_list_handler_plugin

    def get_directory_list_handler_name(self):
        return DIRECTORY_LIST_HANDLER_NAME

    def handle_directory_list(self, request, directory_list):
        # sets the request content type
        request.content_type = HTML_MIME_TYPE

        # retrieves the plugin manager
        plugin_manager = self.main_service_http_template_directory_list_handler_plugin.manager

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.main_service_http_template_directory_list_handler_plugin.template_engine_manager_plugin

        # retrieves the main service http template directory list handler plugin path
        main_service_http_template_directory_list_handler_plugin_path = plugin_manager.get_plugin_path_by_id(self.main_service_http_template_directory_list_handler_plugin.id)

        # creates the template file path
        template_file_path = main_service_http_template_directory_list_handler_plugin_path + "/" + TEMPLATE_DIRECTORY_LIST_HANDLER_RESOURCES_PATH + "/" + HTTP_SERVICE_DIRECTORY_LIST_HTML_TEMPLATE_FILE_NAME

        # parses the template file path
        template_file = template_engine_manager_plugin.parse_file_path(template_file_path)

        # retrieves the directory entries
        directory_entries = directory_list["entries"]

        # iterates over all the directory entries in the directory
        # entries (list) to process their values for the template
        for directory_entry in directory_entries:
            # retrieves the directory entry type
            directory_entry_type = directory_entry["type"]

            # retrieves the directory entry size
            directory_entry_size = directory_entry["size"]

            # in case the directory entry type is file
            if directory_entry_type == "file":
                directory_entry_size_string = self._round_size_unit(directory_entry_size)
            else:
                directory_entry_size_string = "-"

            # sets the directory entry size string value
            directory_entry["size_string"] = directory_entry_size_string

        # retrieves the requested resource path
        resource_path = request.get_resource_path_decoded()

        # splits the resource path into various values
        resource_path_values = resource_path.strip("/").split("/")

        # retrieves the prefix resource path values
        prefix_resource_path_values = resource_path_values[:-1]

        # retrieves the suffix resource path value
        suffix_resouces_path_value = resource_path_values[-1]

        # creates the directory list
        directory_list = []

        # starts the index value with the length of the
        # prefix resource path values
        index = len(prefix_resource_path_values)

        for prefix_resource_path_value in prefix_resource_path_values:
            # creates the resource item
            resource_item = {}

            # sets the resource item value
            resource_item["name"] = prefix_resource_path_value
            resource_item["link"] = "../" * index

            # decrements the index value
            index -= 1

            # adds the resources item to the directory list
            directory_list.append(resource_item)

        # retrieves the format attribute from the request
        format = request.get_attribute("format") or "table"

        # creates the format file path
        format_file = "formats/" + format + ".html.tpl"

        # creates a new formats map from the original one
        formats_map = copy.copy(FORMATS_MAP)

        # sets the current format as active
        formats_map[format] = "active"

        # assigns the directory list to the template file
        template_file.assign("directory_list", directory_list)

        # assigns the directory final item to the template file
        template_file.assign("directory_final_item", suffix_resouces_path_value)

        # assigns the directory entries to the template file
        template_file.assign("directory_entries", directory_entries)

        # assigns the format to the template file
        template_file.assign("format", format)

        # assigns the format file to the template file
        template_file.assign("format_file", format_file)

        # assigns the formats map to the template file
        template_file.assign("formats_map", formats_map)

        # processes the template file
        processed_template_file = template_file.process()

        # decodes the processed template file into a unicode object
        processed_template_file_decoded = processed_template_file.decode("utf-8")

        # writes the processed template file encoded to the request
        request.write(processed_template_file_decoded)

    def _round_size_unit(self, size_value, minimum = DEFAULT_MINIMUM, depth = 0):
        """
        Rounds the size unit, returning a string representation
        of the value with a good rounding precision.

        @type size_value: int
        @param size_value: The current size value.
        @type minimum: int
        @param minimum: The minimum value to be used.
        @type depth: int
        @param depth: The current iteration depth value.
        @rtype: String
        @return: The string representation of the value in
        a simplified manner.
        """

        # in case the current size value is
        # acceptable (less than the minimum)
        if size_value < minimum:
            # rounds the size value
            rounded_size_value = int(size_value)

            # converts the rounded size value to string
            rounded_size_value_string = str(rounded_size_value)

            # retrieves the size unit (string mode)
            size_unit = SIZE_UNITS_LIST[depth]

            # creates the size value string appending the rounded
            # size value string and the size unit
            size_value_string = rounded_size_value_string + size_unit

            # returns the size value string
            return size_value_string
        else:
            # re-calculates the new size value
            new_size_value = size_value / SIZE_UNIT_COEFFICIENT

            # increments the depth
            new_depth = depth + 1

            # runs the round size unit again with the new values
            return self._round_size_unit(new_size_value, minimum, new_depth)
