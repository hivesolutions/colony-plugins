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

import copy
import time

import colony.base.system
import colony.libs.size_util

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

DEFAULT_TEMPLATE_ENCODING = "utf-8"
""" The default template encoding """

DIRECTORY_HANDLER_NAME = "template"
""" The directory handler name """

HTML_MIME_TYPE = "text/html"
""" The html mime type """

TEMPLATE_DIRECTORY_RESOURCES_PATH = "service_http/template_directory/resources"
""" The template directory resources path """

DIRECTORY_HTML_TEMPLATE_FILE_NAME = "directory.html.tpl"
""" The directory html template file name """

FORMATS_MAP = {
    "table" : "",
    "mosaic" : "",
    "thumbnail" : ""
}
""" The formats map """

class ServiceHttpTemplateDirectory(colony.base.system.System):
    """
    The service http template directory (handler) class.
    """

    def get_directory_handler_name(self):
        return DIRECTORY_HANDLER_NAME

    def handle_directory_list(self, request, directory_list):
        # sets the request content type
        request.content_type = HTML_MIME_TYPE

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the template engine plugin
        template_engine_plugin = self.plugin.template_engine_plugin

        # retrieves the service http template directory handler plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(self.plugin.id)

        # creates the template file path
        template_file_path = plugin_path +\
            "/" + TEMPLATE_DIRECTORY_RESOURCES_PATH + "/" + DIRECTORY_HTML_TEMPLATE_FILE_NAME

        # parses the template file path
        template_file = template_engine_plugin.parse_file_path_encoding(template_file_path, DEFAULT_TEMPLATE_ENCODING)

        # retrieves the directory entries
        directory_entries = directory_list["entries"]

        # iterates over all the directory entries in the directory
        # entries (list) to process their values for the template
        for directory_entry in directory_entries:
            # retrieves the directory entry type
            directory_entry_type = directory_entry["type"]

            # retrieves the directory entry size
            directory_entry_size = directory_entry["size"]

            # in case the directory entry type is file must round
            # the size of the file according to the predefined rules
            # otherwise a slice must be used to indicate the size
            if directory_entry_type == "file":
                directory_entry_size_string = colony.libs.size_util.size_round_unit(directory_entry_size)
            else: directory_entry_size_string = "-"

            # sets the directory entry size string value
            directory_entry["size_string"] = directory_entry_size_string

        # retrieves the requested resource base path
        resource_base_path = request.get_resource_base_path_decoded()

        # splits the resource base path into various values
        resource_path_values = resource_base_path.strip("/").split("/")

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

        # retrieves the initial time
        start_time = request.request_time

        # retrieves the end time
        end_time = time.time()

        # calculates the delta time
        delta_time = end_time - start_time

        # rounds the delta time
        delta_time_rounded = round(delta_time, 2)

        # sets the current format as active
        formats_map[format] = "active"

        # assigns the template variables
        template_file.assign("directory_list", directory_list)
        template_file.assign("directory_final_item", suffix_resouces_path_value)
        template_file.assign("directory_entries", directory_entries)
        template_file.assign("format", format)
        template_file.assign("format_file", format_file)
        template_file.assign("formats_map", formats_map)
        template_file.assign("delta_time", delta_time_rounded)

        # processes the template file
        processed_template_file = template_file.process()

        # encodes the processed template file using the default encoding
        processed_template_file_encoded = processed_template_file.encode(DEFAULT_ENCODING)

        # writes the processed template file encoded to the request
        request.write(processed_template_file_encoded)
