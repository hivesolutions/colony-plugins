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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

ASCII_NUMBER_TO_LETTER = 17
""" The value to be added to a number value in ascii to letter """

class WebMvc:
    """
    The web mvc class.
    """

    web_mvc_plugin = None
    """ The web mvc plugin """

    matching_regex = None
    """ The matching regex to be used in patterns matching """

    web_mvc_service_patterns_map = {}
    """ The web mvc service patterns map """

    web_mvc_service_patterns_list = []
    """ The web mvc service patterns list for indexing """

    def __init__(self, web_mvc_plugin):
        """
        Constructor of the class.

        @type web_mvc_plugin: WebMvcPlugin
        @param web_mvc_plugin: The web mvc plugin.
        """

        self.web_mvc_plugin = web_mvc_plugin

        self.web_mvc_service_patterns_map = {}
        self.web_mvc_service_patterns_list = []

    def get_routes(self):
        """
        Retrieves the list of regular expressions to be used as route,
        to the rest service.

        @rtype: List
        @return: The list of regular expressions to be used as route,
        to the rest service.
        """

        return [r"^mvc/.*$"]

    def handle_rest_request(self, rest_request):
        """
        Handles the given rest request.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the path list
        path_list = rest_request.get_path_list()

        # joins the path list to creates the resource path
        resource_path = "/".join(path_list)

        # tries to math the resource path
        resource_path_match = self.matching_regex.match(resource_path)

        # in case there is a valid resource path match
        if resource_path_match:
            # retrieves the groups map from the resource path match
            groups_map = resource_path_match.groupdict()

            # iterates over all the group items
            for group_name, group_value in groups_map.items():
                # in case the group value is valid
                if group_value:
                    # converts the group name to a valid number
                    index_number = self._deserialize_number(group_name)

                    # retrieves the pattern
                    pattern = self.web_mvc_service_patterns_list[index_number]

                    # retrieves the pattern handler method
                    handler_method = self.web_mvc_service_patterns_map[pattern]

                    # handles the web mvc request to the handler method
                    return handler_method(rest_request)

        # returns true
        return True

    def load_web_mvc_service_plugin(self, web_mvc_service_plugin):
        """
        Loads the given web mvc service plugin.

        @type web_mvc_service_plugin: Plugin
        @param web_mvc_service_plugin: The web mvc service plugin to be loaded.
        """

        # retrieves the web mvc service plugin patterns
        web_mvc_service_plugin_patterns = web_mvc_service_plugin.get_patterns()

        # iterates over all the patterns in the web mvc service plugin patterns
        for pattern_key, pattern_value in web_mvc_service_plugin_patterns.items():
            # adds the pattern to the web mvc service patterns map
            self.web_mvc_service_patterns_map[pattern_key] = pattern_value

        # updates the matching regex
        self._update_matching_regex()

    def unload_web_mvc_service_plugin(self, web_mvc_service_plugin):
        """
        Unloads the given web mvc service plugin.

        @type web_mvc_service_plugin: Plugin
        @param web_mvc_service_plugin: The web mvc service plugin to be unloaded.
        """

        # retrieves the web mvc service plugin patterns
        web_mvc_service_plugin_patterns = web_mvc_service_plugin.get_patterns()

        # iterates over all the patterns in the web mvc service plugin patterns
        for pattern_key in web_mvc_service_plugin_patterns:
            # removes the pattern from the web mvc service patterns map
            del self.web_mvc_service_patterns_map[pattern_key]

        # updates the matching regex
        self._update_matching_regex()

    def _update_matching_regex(self):
        """
        Updates the matching regex.
        """

        # starts the matching regex value
        matching_regex_value = r""

        # sets the is first plugin flag
        is_first_plugin = True

        # clears the web mvc service patterns list
        self.web_mvc_service_patterns_list = []

        # starts the index counter
        index = 0

        # iterates over all the patterns in the web mvc service patterns map
        for pattern in self.web_mvc_service_patterns_map:
            # in case it's the first plugin
            if is_first_plugin:
                # unsets the is first plugin flag
                is_first_plugin = False
            else:
                # adds the or operand to the matching regex value
                matching_regex_value += "|"

            # serializes the index to avoid problems with
            # the group naming
            index_serialized = self._serialize_number(index)

            # adds the group name part of the regex to the matching regex value
            matching_regex_value += "(?P<" + str(index_serialized) + ">" + pattern + ")"

            # adds the pattern to the web mvc service patterns list
            self.web_mvc_service_patterns_list.append(pattern)

            # increments the index
            index += 1

        # compiles the matching regex value
        self.matching_regex = re.compile(matching_regex_value)

    def _serialize_number(self, number):
        """
        Serializes a number into a string of characters
        representing the number in ascii.

        @type number: int
        @param number: The number to be serialized.
        @rtype: String
        @return: The serialized version of the number.
        """

        # converts the number to string
        number_string = str(number)

        # initializes the number string serialized
        number_string_serialized = ""

        # iterates over all the number string characters
        for number_string_character in number_string:
            number_string_serialized += chr(ord(number_string_character) + ASCII_NUMBER_TO_LETTER)

        # returns the number string serialized
        return number_string_serialized

    def _deserialize_number(self, number_string_serialized):
        """
        Deserializes a number in the character ascii form into
        the original number.

        @type number_string_serialized: String
        @param number_string_serialized: The number serialized in the ascii form.
        @rtype: int
        @return: The deserialized version of the number.
        """

        # initializes the number string
        number_string = ""

        # iterates over all the number string serialized characters
        for number_string_serialized_character in number_string_serialized:
            number_string += chr(ord(number_string_serialized_character) - ASCII_NUMBER_TO_LETTER)

        # retrieves the number from the number string
        number = int(number_string)

        # returns the number
        return number
