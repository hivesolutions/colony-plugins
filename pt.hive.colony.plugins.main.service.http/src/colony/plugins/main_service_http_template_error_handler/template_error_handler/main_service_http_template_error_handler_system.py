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

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

DEFAULT_TEMPLATE_ENCODING = "Cp1252"
""" The default template encoding """

ERROR_HANDLER_NAME = "template"
""" The error handler name """

HTML_MIME_TYPE = "text/html"
""" The html mime type """

TEMPLATE_ERROR_HANDLER_RESOURCES_PATH = "main_service_http_template_error_handler/template_error_handler/resources"
""" The template error handler resources path """

HTTP_SERVICE_ERROR_HTML_TEMPLATE_FILE_NAME = "http_service_error.html.tpl"
""" The http service error html template file name """

STATUS_CODE_VALUES = {100 : "Continue", 101 : "Switching Protocols",
                      200 : "OK", 201 : "Created", 202 : "Accepted", 203 : "Non-Authoritative Information",
                      204 : "No Content", 205 : "Reset Content", 206 : "Partial Content", 207 : "Multi-Status",
                      301 : "Moved permanently", 302 : "Found", 303 : "See Other", 304 : "Not Modified",
                      305 : "Use Proxy", 306 : "(Unused)", 307 : "Temporary Redirect",
                      400 : "Bad Request", 401 : "Unauthorized", 402 : "Payment Required", 403 : "Forbidden",
                      404 : "Not Found", 405 : "Method Not Allowed", 406 : "Not Acceptable", 407 : "Proxy Authentication Required",
                      408 : "Request Timeout", 409 : "Conflict", 410 : "Gone", 411 : "Length Required", 412 : "Precondition Failed",
                      413 : "Request Entity Too Large", 414 : "Request-URI Too Long", 415 : "Unsupported Media Type",
                      416 : "Requested Range Not Satisfiable", 417 : "Expectation Failed",
                      500 : "Internal Server Error", 501 : "Not Implemented", 502 : "Bad Gateway",
                      503 : "Service Unavailable", 504 : "Gateway Timeout", 505 : "HTTP Version Not Supported"}
""" The status code values map """

STATUS_CODE_IMAGES = {100 : "none", 101 : "none",
                      200 : "none", 201 : "none", 202 : "none", 203 : "none",
                      204 : "none", 205 : "none", 206 : "none", 207 : "none",
                      301 : "none", 302 : "none", 303 : "none", 304 : "none",
                      305 : "none", 306 : "none", 307 : "none",
                      400 : "logo_question_mark", 401 : "logo_lock", 402 : "logo_question_mark",
                      403 : "logo_question_mark", 404 : "logo_question_mark", 405 : "logo_question_mark",
                      406 : "logo_question_mark", 407 : "logo_question_mark", 408 : "logo_question_mark",
                      409 : "logo_question_mark", 410 : "logo_question_mark", 411 : "logo_question_mark",
                      412 : "logo_question_mark", 413 : "logo_question_mark", 414 : "logo_question_mark",
                      415 : "logo_question_mark", 416 : "logo_question_mark", 417 : "logo_question_mark",
                      500 : "logo_thunder", 501 : "logo_thunder", 502 : "logo_thunder",
                      503 : "logo_thunder", 504 : "logo_thunder", 505 : "logo_thunder"}
""" The status code images map """

class MainServiceHttpTemplateErrorHandler:
    """
    The main service http template error handler class.
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
        request.content_type = HTML_MIME_TYPE

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

        # retrieves the error string
        error_string = unicode(error) + " (" + error.__class__.__name__ + ")"

        # retrieves the execution information
        _type, _value, traceback_list = sys.exc_info()

        # in case the traceback list is valid
        if traceback_list:
            # creates the (initial) formated traceback
            formated_traceback = traceback.format_tb(traceback_list)

            # retrieves the file system encoding
            file_system_encoding = sys.getfilesystemencoding()

            # decodes the traceback values using the file system encoding
            formated_traceback = [value.decode(file_system_encoding) for value in formated_traceback]
        else:
            # sets an empty formated traceback
            formated_traceback = ()

        # retrieves the error description
        error_description = STATUS_CODE_VALUES.get(error_code, "No description")

        # retrieves the error image
        error_image = STATUS_CODE_IMAGES.get(error_code, "none")

        # retrieves the plugin manager
        plugin_manager = self.main_service_http_template_error_handler_plugin.manager

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.main_service_http_template_error_handler_plugin.template_engine_manager_plugin

        # retrieves the main service http template error handler plugin path
        main_service_http_template_error_handler_plugin_path = plugin_manager.get_plugin_path_by_id(self.main_service_http_template_error_handler_plugin.id)

        # creates the template file path
        template_file_path = main_service_http_template_error_handler_plugin_path + "/" + TEMPLATE_ERROR_HANDLER_RESOURCES_PATH + "/" + HTTP_SERVICE_ERROR_HTML_TEMPLATE_FILE_NAME

        # parses the template file path
        template_file = template_engine_manager_plugin.parse_file_path_encoding(template_file_path, DEFAULT_TEMPLATE_ENCODING)

        # assigns the error code to the template file
        template_file.assign("error_code", error_code)

        # assigns the error description to the template file
        template_file.assign("error_description", error_description)

        # assigns the error image to the template file
        template_file.assign("error_image", error_image)

        # assigns the delta time to the template file
        template_file.assign("delta_time", delta_time_rounded)

        # assigns the error to the template file
        template_file.assign("error", error_string)

        # assigns the traceback to the template file
        template_file.assign("traceback", formated_traceback)

        # processes the template file
        processed_template_file = template_file.process()

        # encodes the processed template file using the default encoding
        processed_template_file_encoded = processed_template_file.encode(DEFAULT_ENCODING)

        # sets the status code in the request
        request.status_code = error_code

        # writes the processed template file encoded to the request
        request.write(processed_template_file_encoded)
