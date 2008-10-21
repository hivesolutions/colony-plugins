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

__revision__ = "$LastChangedRevision: 2120 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 16:01:47 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

HANDLER_FILENAME = "none"

class JavascriptFileHandler:
    """
    The javascript file handler class.
    """

    file_handler_plugin = None
    """ The file handler plugin """

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
        # sets the content type for the request
        request.content_type = "text/plain;charset=utf-8"

        # writes the serialized result into the buffer
        request.write("tobias")

        #request
        # flushes the request, sending the output to the client
        request.flush()
