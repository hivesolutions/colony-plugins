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

import re
import sys

import os.path

import template_handler_exceptions

HANDLER_FILENAME = "template_handler.py"
""" The handler filename """

TEMPLATE_FILE_EXENSION = "ctp"
""" The template file extension """

START_TAG_VALUE = "<\?colony"
""" The start tag value """

END_TAG_VALUE = "\?>"
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

        # retrieves the file contents length
        file_contensts_length = len(file_contents)

        # creates the colony start regex
        colony_start_regex = re.compile(START_TAG_VALUE)

        # creates the colony end regex
        colony_end_regex = re.compile(END_TAG_VALUE)

        # creates the match orderer list
        match_orderer_list = []

        # retrieves the start matches iterator
        start_matches_iterator = colony_start_regex.finditer(file_contents)

        # iterates over all the start matches
        for start_match in start_matches_iterator:
            start_math_orderer = MatchOrderer(start_match)
            match_orderer_list.append(start_math_orderer)

        # retrieves the end matches iterator
        end_matches_iterator = colony_end_regex.finditer(file_contents)

        # iterates over all the end matches
        for end_match in end_matches_iterator:
            end_match_orderer = MatchOrderer(end_match)
            match_orderer_list.append(end_match_orderer)

        # orders the match orderer list
        match_orderer_list.sort()

        # reverses the list so that it's ordered in ascending form
        match_orderer_list.reverse()

        # start the index accumulator
        index = 0

        # sets the current carret position
        current_carret = 0

        # retrieves the match orderer list length
        match_orderer_list_length = len(match_orderer_list)

        # sets the plugin manager value
        plugin_manager = self.template_handler_plugin.manager

        # creates a backup for the stdout
        backup_stdout = sys.stdout

        # sets the stdout as request
        sys.stdout = request

        # iterates over the match orderer list in size two jumps
        while index < match_orderer_list_length:
            # retrieves the start match orderer
            start_match_orderer = match_orderer_list[index]

            # retrieves the end match orderer
            end_macth_orderer = match_orderer_list[index + 1]

            # retrieves the start match
            start_match = start_match_orderer.match

            # retrieves the end match
            end_match = end_macth_orderer.match

            # retrieves the start index of the start match
            start_match_start = start_match.start()

            # retrieves the end index of the start match
            start_match_end = start_match.end()

            # retrieves the start index of the end match
            end_match_start = end_match.start()

            # retrieves the end index of the end match
            end_match_end = end_match.end()

            # retrieves the middle words
            middle_words = file_contents[current_carret:start_match_start]

            # writes the middle words in the request
            sys.stdout.write(middle_words)

            # retrieves the python text to be processed
            process_text = file_contents[start_match_end:end_match_start]

            # strips the process text
            process_text_striped = process_text.strip()

            # substitutes the windows style of newlines to the unix one
            process_text_replaced = process_text_striped.replace("\r\n", "\n")

            # executes the python code
            exec(process_text_replaced) in globals(), locals()

            # sets the current carret
            current_carret = end_match_end

            # updates the index accumulator value
            index += 2

        # restores the original stdout
        sys.stdout = backup_stdout

        # retrieves the final words
        final_words = file_contents[current_carret:file_contensts_length]

        # writes the final words in the request
        request.write(final_words)

        # closes the file
        file.close()

class MatchOrderer:
    """
    The match orderer class.
    """

    match = None
    """ The match object to be ordered """

    def __init__(self, match):
        self.match = match

    def __cmp__(self, other):
        return other.match.start() - self.match.start()
