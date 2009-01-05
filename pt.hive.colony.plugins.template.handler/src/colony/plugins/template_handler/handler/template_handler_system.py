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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

JAVASCRIPT_TAG_START = "<script type=\"text/javascript\">"
""" The javascript start tag """

JAVASCRIPT_TAG_END = "</script>"
""" The javascript end tag """

DEFAULT_CONTENT_TYPE = "text/html"
""" The default content type """

class TemplateHandler:
    """
    The template handler class.
    """

    template_handler_plugin = None
    """ The template handler plugin """

    default_stdout = None
    """ The default stdout """

    def __init__(self, template_handler_plugin):
        """
        Constructor of the class.
        
        @type template_handler_plugin: TemplateHandlerPlugin
        @param template_handler_plugin: The template handler plugin.
        """

        self.template_handler_plugin = template_handler_plugin

        self.default_stdout = sys.stdout

    def get_handler_filename(self):
        return HANDLER_FILENAME

    def is_request_handler(self, request):
        # retrieves the template handler extension plugins
        template_handler_extension_plugins = self.template_handler_plugin.template_handler_extension_plugins

        # retrieves the file extension from the filename
        file_name_extension = request.filename.split(".")[-1]

        if file_name_extension == TEMPLATE_FILE_EXENSION:
            return True
        else:
            # retrieves the request file name
            request_filename = request.uri

            # left strips the request file name
            request_filename_striped = request_filename.lstrip("/")

            # iterates over all the template handler extension plugins
            for template_handler_extension_plugin in template_handler_extension_plugins:
                # retrieves the handler file name
                handler_filename = template_handler_extension_plugin.get_handler_filename()

                # in case the handler file name is found in the beginning of the request file name
                if request_filename_striped.find(handler_filename) == 0:
                    return True

            return False

    def handle_request(self, request):
        # retrieves the template handler extension plugins
        template_handler_extension_plugins = self.template_handler_plugin.template_handler_extension_plugins

        # sets the default base directory
        base_directory = "C:/Program Files/Apache Software Foundation/Apache2.2/htdocs"

        # retrieves the request file name
        request_filename = request.uri

        # creates the default complete path
        complete_path = base_directory + "/" + request_filename

        # left strips the request file name
        request_filename_striped = request_filename.lstrip("/")

        # iterates over all the template handler extension plugins
        for template_handler_extension_plugin in template_handler_extension_plugins:
            # retrieves the handler file name
            handler_filename = template_handler_extension_plugin.get_handler_filename()

            # in case the handler file name is the same as the request file name
            if handler_filename == request_filename_striped:
                # retrieves the complete path
                complete_path = template_handler_extension_plugin.get_template_path()
                break;
            elif request_filename_striped.find(handler_filename) == 0:
                # retrieves the handler file name length
                handler_filename_length = len(handler_filename)

                # retrieves the file path value
                file_path_value = request_filename_striped[handler_filename_length:]

                # retrieves the resource map
                resources_map = template_handler_extension_plugin.get_resources_paths_map()

                # @todo
                # tenho de iterar por todos
                # fazer append dos valores de path que tem la
                # ver se o ficheiro existe

                # retrieves the base path
                base_path = resources_map["/"]

                # sets the complete path
                complete_path = base_path + "/" + file_path_value

                # retrieves the file extension from the filename
                file_name_extension = request.filename.split(".")[-1]

                # in case the file extension is of type template
                if file_name_extension == TEMPLATE_FILE_EXENSION:
                    break
                else:
                    # sets the empty content type
                    request.content_type = ""

                    # opens the requested file
                    file = open(complete_path, "rb")

                    # reads the file contents
                    file_contents = file.read()

                    # writes the file contents
                    request.write(file_contents)

                    # returns the call (the file is readed)
                    return

        # in case the paths does not exist
        if not os.path.exists(complete_path):
            # raises file not found exception with 404 http error code
            raise template_handler_exceptions.FileNotFoundException(request_filename, 404)

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

        # sets the stdout as request
        sys.stdout = request

        # sets the default content type
        request.content_type = DEFAULT_CONTENT_TYPE

        try:
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

            # retrieves the final words
            final_words = file_contents[current_carret:file_contensts_length]

            # writes the final words in the request
            request.write(final_words)
        finally:
            # restores the default stdout
            sys.stdout = self.default_stdout

            # closes the file
            file.close()

    def import_js_library(self, library_name):
        """
        Imports the javascript library with the given name.
        
        @type library_name: String
        @param library_name: The name of the library to be imported.
        """

        # retrieves the plugin manager
        manager = self.template_handler_plugin.manager

        # retrieves the plugin path
        plugin_path = manager.get_plugin_path_by_id(self.template_handler_plugin.id)

        # creates the library file name
        library_file_name = library_name + ".js"

        # retrieves the full library path
        library_path = plugin_path + "/template_handler/handler/resources/js_libs/" + library_file_name

        # opens the library file
        library_file = open(library_path, "r")

        # reads the library file contents
        library_file_contents = library_file.read()

        # prints the javascript start tag
        print JAVASCRIPT_TAG_START

        # prints the library file contents
        print library_file_contents

        # prints the javascript end tag
        print JAVASCRIPT_TAG_END

        # closes the library file
        library_file.close()

    def parse_request_attributes(self, request):
        """
        Parses the request attributes in the default response format.
        
        @type request: HttpRequest
        @param request: The http request to be parsed for attributes.
        @rtype: Dictionary
        @return: The map with the parsed attributes.
        """

        # creates the request attributes map
        request_attributes_map = {}

        # retrieves the received message
        received_message = request.read()

        # splits the received message in the "&" character
        # to retrieve the received message pairs
        received_message_pairs = received_message.split("&")

        # iterates over all the received message pairs
        for received_message_pair in received_message_pairs:
            # splits the received message in the "=" character to retrieve
            # both the key and the value for the attribute
            received_message_pair_split = received_message_pair.split("=")

            # in case the retrieval was successful
            if len(received_message_pair_split) > 1:
                # retrieves the key and the value
                key, value = received_message_pair_split
            else:
                # breaks the iteration loop
                break

            # sets the attribute key and value
            request_attributes_map[key] = value

        # returns the request attributes map
        return request_attributes_map

    def escape_dots(self, string_value):
        """
        Escapes the "." changing it to "-".
        
        @type string_value: String
        @param string_value: The string to be escaped.
        @rtype: String
        @return: The escaped string.
        """

        # escapes the string value, replacing the "." character
        # with the "-" character
        escaped_string_value = string_value.replace(".", "-")

        # returns the escaped string value
        return escaped_string_value

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
