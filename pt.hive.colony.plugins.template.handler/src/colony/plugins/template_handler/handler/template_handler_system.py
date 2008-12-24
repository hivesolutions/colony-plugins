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

__revision__ = "$LastChangedRevision: 516 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-28 14:30:47 +0000 (Sex, 28 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys

import os.path

import template_handler_exceptions

HANDLER_FILENAME = "template_handler.py"
""" The handler filename """

TEMPLATE_FILE_EXENSION = "ctp"
""" The template file extension """

START_TAG_VALUE = "<?colony"
""" The start tag value """

END_TAG_VALUE = "?>"
""" The end tag value """

class TemplateHandler:
    """
    The template handler class.
    """

    template_handler_plugin = None
    """ The template handler plugin """

    def __init__(self, template_handler_plugin):
        """
        Constructor of the class.
        
        @type template_handler_plugin: TemplateHandlerPlugin
        @param template_handler_plugin: The template handler plugin.
        """

        self.template_handler_plugin = template_handler_plugin

    def get_handler_filename(self):
        return HANDLER_FILENAME

    def is_request_handler(self, request):
        # retrieves the file extension from the filename
        file_name_extension = request.filename.split(".")[-1]

        if file_name_extension == TEMPLATE_FILE_EXENSION:
            return True
        else:
            return False

    def handle_request(self, request):
        # sets the base directory
        base_directory = "C:/Program Files/Apache Software Foundation/Apache2.2/htdocs"

        # retrieves the requested path
        path = request.path

        # creates the complete path
        complete_path = base_directory + "/" + path

        # in case the paths does not exist
        if not os.path.exists(complete_path):
            # raises file not found exception with 404 http error code
            raise main_service_http_file_handler_exceptions.FileNotFoundException(path, 404)

        # opens the requested file
        file = open(complete_path, "rb")

        # reads the file contents
        file_contents = file.read()

        import re

        colony_start_regex = re.compile("<\?colony")

        colony_end_regex = re.compile("\?>")

        search_value = colony_regex.search(file_contents)

        start_index = file_contents.find(START_TAG_VALUE)

        end_index = file_contents.find(END_TAG_VALUE)

        start_code_index = start_index + 8
        end_code_index = end_index

        request.write(file_contents[:start_index])

        process_text = file_contents[start_code_index:end_code_index]

        process_text_striped = process_text.strip()

        process_text_replaced = process_text_striped.replace("\r\n", "\n")

        sys.stdout = request

        plugin_manager = self.template_handler_plugin.manager

        exec(process_text_replaced) in globals(), locals()

        # closes the file
        file.close()
