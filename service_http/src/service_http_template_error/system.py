#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import sys
import time
import traceback

import colony

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

DEFAULT_TEMPLATE_ENCODING = "utf-8"
""" The default template encoding """

ERROR_HANDLER_NAME = "template"
""" The error handler name """

HTML_MIME_TYPE = "text/html"
""" The HTML mime type """

TEMPLATE_ERROR_RESOURCES_PATH = "service_http_template_error/resources"
""" The template error resources path """

ERROR_HTML_TEMPLATE_FILE_NAME = "error.html.tpl"
""" The error HTML template file name """

STATUS_MESSAGES = {
    100: "Continue",
    101: "Switching Protocols",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    301: "Moved permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "(Unused)",
    307: "Temporary Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Long",
    415: "Unsupported Media Type",
    416: "Requested Range Not Satisfiable",
    417: "Expectation Failed",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
}
""" The status code messages map """

STATUS_CODE_IMAGES = {
    100: "none",
    101: "none",
    200: "none",
    201: "none",
    202: "none",
    203: "none",
    204: "none",
    205: "none",
    206: "none",
    207: "none",
    301: "none",
    302: "none",
    303: "none",
    304: "none",
    305: "none",
    306: "none",
    307: "none",
    400: "logo_question_mark",
    401: "logo_lock",
    402: "logo_question_mark",
    403: "logo_question_mark",
    404: "logo_question_mark",
    405: "logo_question_mark",
    406: "logo_question_mark",
    407: "logo_question_mark",
    408: "logo_question_mark",
    409: "logo_question_mark",
    410: "logo_question_mark",
    411: "logo_question_mark",
    412: "logo_question_mark",
    413: "logo_question_mark",
    414: "logo_question_mark",
    415: "logo_question_mark",
    416: "logo_question_mark",
    417: "logo_question_mark",
    500: "logo_thunder",
    501: "logo_thunder",
    502: "logo_thunder",
    503: "logo_thunder",
    504: "logo_thunder",
    505: "logo_thunder",
}
""" The status code images map """


class ServiceHTTPTemplateError(colony.System):
    """
    The service HTTP template error (handler) class.
    """

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
        error_string = (
            colony.legacy.UNICODE(error) + " (" + error.__class__.__name__ + ")"
        )

        # retrieves the execution information
        _type, _value, traceback_list = sys.exc_info()

        # in case the traceback list is valid
        if traceback_list:
            # creates the (initial) formated traceback
            formated_traceback = traceback.format_tb(traceback_list)

            # retrieves the file system encoding
            file_system_encoding = sys.getfilesystemencoding()

            # decodes the traceback values using the file system encoding
            formated_traceback = [
                (
                    value.decode(file_system_encoding)
                    if value == colony.legacy.BYTES
                    else value
                )
                for value in formated_traceback
            ]
        # otherwise there is no traceback list
        else:
            # sets an empty formated traceback
            formated_traceback = ()

        # retrieves the error description
        error_description = STATUS_MESSAGES.get(error_code, "No description")

        # retrieves the error image
        error_image = STATUS_CODE_IMAGES.get(error_code, "none")

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the template engine plugin
        template_engine_plugin = self.plugin.template_engine_plugin

        # retrieves the plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(self.plugin.id)

        # creates the template file path
        template_file_path = (
            plugin_path
            + "/"
            + TEMPLATE_ERROR_RESOURCES_PATH
            + "/"
            + ERROR_HTML_TEMPLATE_FILE_NAME
        )

        # parses the template file path
        template_file = template_engine_plugin.parse_template(
            template_file_path, encoding=DEFAULT_TEMPLATE_ENCODING
        )

        # assigns the template variables
        template_file.assign("error_code", error_code)
        template_file.assign("error_description", error_description)
        template_file.assign("error_image", error_image)
        template_file.assign("delta_time", delta_time_rounded)
        template_file.assign("error", error_string)
        template_file.assign("traceback", formated_traceback)

        # processes the template file
        processed_template_file = template_file.process()

        # encodes the processed template file using the default encoding
        processed_template_file_encoded = processed_template_file.encode(
            DEFAULT_ENCODING
        )

        # sets the status code in the request
        request.status_code = error_code

        # writes the processed template file encoded to the request
        request.write(processed_template_file_encoded)
