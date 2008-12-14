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

import os.path

import main_service_http_file_handler_exceptions

HANDLER_NAME = "file"
""" The handler name """

FILE_MIME_TYPE_MAPPING = {"html" : "text/html", "txt" : "text/plain",
                          "jpg" : "image/jpg", "png" : "image/png"}
""" The map that relates the file extension and the associated mime type """

class MainServiceHttpFileHandler:
    """
    The main service http file handler class.
    """

    main_service_http_file_handler_plugin = None
    """ The main service http file handler plugin """

    def __init__(self, main_service_http_file_handler_plugin):
        """
        Constructor of the class.
        
        @type main_service_http_file_handler_plugin: MainServiceHttpFileHandlerPlugin
        @param main_service_http_file_handler_plugin: The main service http file handler plugin.
        """

        self.main_service_http_file_handler_plugin = main_service_http_file_handler_plugin

    def get_handler_name(self):
        return HANDLER_NAME

    def handle_request(self, request):
        # sets the base directory
        base_directory = "c:/tobias_web"

        path = request.path

        if path == "/":
            path = "/index.html"

        extension = path.split(".")[-1]

        if extension in FILE_MIME_TYPE_MAPPING:
            mime_type = FILE_MIME_TYPE_MAPPING[extension]
        else:
            mime_type = None

        complete_path = base_directory + "/" + path

        if not os.path.exists(complete_path):
            raise main_service_http_file_handler_exceptions.FileNotFoundException(path)

        # opens the requested file
        file = open(complete_path, "rb")

        # reads the file contents
        file_contents = file.read()

        request.content_type = mime_type
        request.status_code = 200
        request.write(file_contents)
