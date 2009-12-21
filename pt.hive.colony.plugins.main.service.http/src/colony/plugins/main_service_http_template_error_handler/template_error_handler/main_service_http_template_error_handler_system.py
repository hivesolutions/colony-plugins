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

import sys
import time
import traceback

ERROR_HANDLER_NAME = "template"
""" The error handler name """

XHTML_MIME_TYPE = "application/xhtml+xml"
""" The xhtml mime type """

TEMPLATE_ERROR_HANDLER_RESOURCES_PATH = "main_service_http_template_error_handler/template_error_handler/resources"
""" The template error handler resources path """

HTTP_SERVICE_ERROR_XHTML_TEMPLATE_FILE_NAME = "http_service_error.xhtml"
""" The http service error xhtml template file name """

STATUS_CODE_VALUES = {200 : "OK", 207 : "Multi-Status",
                      301 : "Moved permanently", 302 : "Found", 303 : "See Other",
                      403 : "Forbidden", 404 : "Not Found",
                      500 : "Internal Server Error"}
""" The status code values map """

class MainServiceHttpTemplateErrorHandler:
    """
    The main service http gzip encoding class.
    """

    main_service_http_template_error_handler_plugin = None
    """ The main service http template error handlers plugin """

    def __init__(self, main_service_http_template_error_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_template_error_handler_plugin: MainServiceHttpTemplateErrorHandlerPlugin
        @param main_service_http_template_error_handler_plugin: The main service http template error handler plugin.
        """

        self.main_service_http_template_error_handler_plugin = main_service_http_template_error_handler_plugin

    def get_error_handler_name(self):
        return ERROR_HANDLER_NAME

    def handle_error(self, request, error):
        # sets the request content type
        request.content_type = "application/xhtml+xml"

        # checks if the error contains a status code
        if hasattr(error, "status_code"):
            # sets the error code
            error_code = error.status_code
        else:
            # sets the internal server error error code
            error_code = 500

        # retrieves the initial time
        start_time = request.request_time

        # retrieves the end time
        end_time = time.time()

        # calculates the delta time
        delta_time = end_time - start_time

        # rounds the delta time
        delta_time_rounded = round(delta_time, 2)

        # retrieves the execution information
        type, value, traceback_list = sys.exc_info()

        # in case the traceback list is valid
        if traceback_list:
            formated_traceback = traceback.format_tb(traceback_list)
        else:
            formated_traceback = ()

        # retrieves the error description
        error_description = STATUS_CODE_VALUES.get(error_code, "No description")

        # retrieves the plugin manager
        plugin_manager = self.main_service_http_template_error_handler_plugin.manager

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.main_service_http_template_error_handler_plugin.template_engine_manager_plugin

        # retrieves the main service http template error handler plugin path
        main_service_http_template_error_handler_plugin_path = plugin_manager.get_plugin_path_by_id(self.main_service_http_template_error_handler_plugin.id)

        # creates the template file path
        template_file_path = main_service_http_template_error_handler_plugin_path + "/" + TEMPLATE_ERROR_HANDLER_RESOURCES_PATH + "/" + HTTP_SERVICE_ERROR_XHTML_TEMPLATE_FILE_NAME

        # parses the template file path
        template_file = template_engine_manager_plugin.parse_file_path(template_file_path)

        # assigns the error code to the template file
        template_file.assign("error_code", error_code)

        # assigns the error description to the template file
        template_file.assign("error_description", error_description)

        # assigns the delta time to the template file
        template_file.assign("delta_time", delta_time_rounded)

        # assigns the traceback to the template file
        template_file.assign("traceback", formated_traceback)

        # processes the template file
        processed_template_file = template_file.process()

        # decodes the processed template file into a unicode object
        processed_template_file_decoded = processed_template_file.decode("utf-8")

        # sets the request content type
        request.content_type = XHTML_MIME_TYPE

        # sets the status code in the request
        request.status_code = error_code

        # writes the processed template file encoded to the request
        request.write(processed_template_file_decoded)
