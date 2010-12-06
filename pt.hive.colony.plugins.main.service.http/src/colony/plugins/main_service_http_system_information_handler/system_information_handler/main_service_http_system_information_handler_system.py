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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

HANDLER_NAME = "system_information"
""" The handler name """

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

DEFAULT_TEMPLATE_ENCODING = "Cp1252"
""" The default template encoding """

HTML_MIME_TYPE = "text/html"
""" The html mime type """

SYSTEM_INFORMATION_HANDLER_RESOURCES_PATH = "main_service_http_system_information_handler/system_information_handler/resources"
""" The system information handler resources path """

HTTP_SERVICE_SYSTEM_INFORMATION_HTML_TEMPLATE_FILE_NAME = "http_service_system_information.html.tpl"
""" The http service system information html template file name """

class MainServiceHttpSystemInformationHandler:
    """
    The main service http system information handler class.
    """

    main_service_http_system_information_handler_plugin = None
    """ The main service http system information handler plugin """

    def __init__(self, main_service_http_system_information_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_system_information_handler_plugin: MainServiceHttpSystemInformationHandlerPlugin
        @param main_service_http_system_information_handler_plugin: The main service http system information handler plugin.
        """

        self.main_service_http_system_information_handler_plugin = main_service_http_system_information_handler_plugin

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

        # sets the request content type
        request.content_type = HTML_MIME_TYPE

        # retrieves the plugin manager
        plugin_manager = self.main_service_http_system_information_handler_plugin.manager

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.main_service_http_system_information_handler_plugin.template_engine_manager_plugin

        # retrieves the main service http system information handler plugin path
        main_service_http_system_information_handler_plugin_path = plugin_manager.get_plugin_path_by_id(self.main_service_http_system_information_handler_plugin.id)

        # creates the template file path
        template_file_path = main_service_http_system_information_handler_plugin_path + "/" + SYSTEM_INFORMATION_HANDLER_RESOURCES_PATH + "/" + HTTP_SERVICE_SYSTEM_INFORMATION_HTML_TEMPLATE_FILE_NAME

        # parses the template file path
        template_file = template_engine_manager_plugin.parse_file_path_encoding(template_file_path, DEFAULT_TEMPLATE_ENCODING)

#        # assigns the directory list to the template file
#        template_file.assign("directory_list", directory_list)
#
#        # assigns the directory final item to the template file
#        template_file.assign("directory_final_item", suffix_resouces_path_value)
#
#        # assigns the directory entries to the template file
#        template_file.assign("directory_entries", directory_entries)
#
#        # assigns the format to the template file
#        template_file.assign("format", format)
#
#        # assigns the format file to the template file
#        template_file.assign("format_file", format_file)
#
#        # assigns the formats map to the template file
#        template_file.assign("formats_map", formats_map)
#
#        # assigns the delta time to the template file
#        template_file.assign("delta_time", delta_time_rounded)

        # processes the template file
        processed_template_file = template_file.process()

        # encodes the processed template file using the default encoding
        processed_template_file_encoded = processed_template_file.encode(DEFAULT_ENCODING)

        # writes the processed template file encoded to the request
        request.write(processed_template_file_encoded)
