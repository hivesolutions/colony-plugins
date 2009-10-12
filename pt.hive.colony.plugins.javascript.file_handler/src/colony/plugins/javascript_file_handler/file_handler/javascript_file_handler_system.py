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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

HANDLER_FILENAME = "none"

FILE_MIME_TYPE_MAPPING = {"html" : "text/html", "txt" : "text/plain", "css" : "text/css",
                          "jpg" : "image/jpg", "png" : "image/png"}
""" The map that relates the file extension and the associated mime type """

DEFAULT_MIME_TYPE = "text/plain"
""" The default mime type """

DEFAULT_CHARSET = "Cp1252"
""" The default charset """

class JavascriptFileHandler:
    """
    The javascript file handler class.
    """

    javascript_file_handler_plugin = None
    """ The javascript file handler plugin """

    def __init__(self, javascript_file_handler_plugin):
        """
        Constructor of the class.

        @type javascript_file_handler_plugin: JavascriptFileHandlerPlugin
        @param javascript_file_handler_plugin: The javascript file handler plugin.
        """

        self.javascript_file_handler_plugin = javascript_file_handler_plugin

    def get_handler_filename(self):
        return HANDLER_FILENAME

    def is_request_handler(self, request):
        # retrieves the simple filename from the complete path filename
        simple_filename = request.filename.split("/")[-1]

        if simple_filename == HANDLER_FILENAME:
            return True
        else:
            return False

    def handle_request(self, request):
        # retrieves the javascript handler plugins
        javascript_handler_plugins = self.javascript_file_handler_plugin.javascript_handler_plugins

        # retrieves the javascript manager plugin
        javascript_manager_plugin = self.javascript_file_handler_plugin.javascript_manager_plugin

        # splits the uri using the "/" character
        uri_splited = request.uri.split("/")

        # retrieves the list o components for the relative path
        relative_path_list = uri_splited[3:]

        # start the relative path string
        relative_path = ""

        # iterates over the list of relative path
        for relative_path_item in relative_path_list:
            relative_path += relative_path_item + "/"

        # retrieves the full path for the file
        full_path = javascript_manager_plugin.get_file_full_path(relative_path)

        # retrieves the file extension
        file_extension = full_path.split(".")[-1]

        # opens the file for reading
        file = open(full_path, "rb")

        # reads the file contents
        file_contents = file.read()

        # closes the file
        file.close()

        # retrieves the mime type for the given file
        mime_type = FILE_MIME_TYPE_MAPPING.get(file_extension, DEFAULT_MIME_TYPE)

        # sets the content type for the request
        request.content_type = mime_type + ";charset=" + DEFAULT_CHARSET

        # iterates over all the javascript handler plugins
        for javascript_handler_plugin in javascript_handler_plugins:
            # handles the contents to the javascript handler plugin
            file_contents = javascript_handler_plugin.handle_contents(file_contents)

        # writes the file contents to the request
        request.write(file_contents)

        # in case the file is of type js
        if file_extension == "js":
            # writes the file footer
            request.write("loaded(\"plugins/" + relative_path.strip("/") + "\");")

        # flushes the request, sending the output to the client
        request.flush()

        # returns true
        return True
