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

import colony.libs.string_buffer_util

import web_mvc_exceptions

REGEX_COMILATION_LIMIT = 99
""" The regex compilation limit """

class WebMvc:
    """
    The web mvc class.
    """

    web_mvc_plugin = None
    """ The web mvc plugin """

    matching_regex_list = []
    """ The list of matching regex to be used in patterns matching """

    matching_regex_base_values_map = []
    """ The map containing the base values for the various matching regex """

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

        self.matching_regex_list = []
        self.matching_regex_base_values_map = {}
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

        # iterates over all the matching regex in the matching regex list
        for matching_regex in self.matching_regex_list:
            # tries to math the resource path
            resource_path_match = matching_regex.match(resource_path)

            # in case there is a valid resource path match
            if resource_path_match:
                # retrieves the base value for the matching regex
                base_value = self.matching_regex_base_values_map[matching_regex]

                # retrieves the group index from the resource path match
                group_index = resource_path_match.lastindex

                # calculates the web mvc service index from the base value,
                # the group index and subtracts one value
                web_mvc_service_index = base_value + group_index - 1

                # retrieves the pattern for the web mvc service index
                pattern = self.web_mvc_service_patterns_list[web_mvc_service_index]

                # retrieves the pattern handler method
                handler_method = self.web_mvc_service_patterns_map[pattern]

                # tries to retrieve the rest request session
                rest_request_session = rest_request.get_session()

                # in case there is a valid rest request session
                if rest_request_session:
                    # sets the parameters as the session attributes map
                    parameters = rest_request_session.get_attributes_map()
                else:
                    # sets the parameters as an empty map
                    parameters = {}

                # handles the web mvc request to the handler method
                return handler_method(rest_request, parameters)

        # raises the mvc request not handled exception
        raise web_mvc_exceptions.MvcRequestNotHandled("no mvc service plugin could handle the request")

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

        # starts the matching regex value buffer
        matching_regex_value_buffer = colony.libs.string_buffer_util.StringBuffer()

        # clears the web mvc service patterns list
        self.web_mvc_service_patterns_list = []

        # clears the matching regex list
        self.matching_regex_list = []

        # clears the matching regex base value map
        self.matching_regex_base_values_map.clear()

        # sets the is first flag
        is_first = True

        # starts the index value
        index = 0

        # starts the current base value
        current_base_value = 0

        # iterates over all the patterns in the web mvc service patterns map
        for pattern in self.web_mvc_service_patterns_map:
            # in case it's the first
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # adds the or operand to the matching regex value buffer
                matching_regex_value_buffer.write("|")

            # adds the group name part of the regex to the matching regex value buffer
            matching_regex_value_buffer.write("(" + pattern + ")")

            # adds the pattern to the web mvc service patterns list
            self.web_mvc_service_patterns_list.append(pattern)

            # increments the index
            index += 1

            # in case the current index is in the limit of the python
            # regex compilation
            if index % REGEX_COMILATION_LIMIT == 0:
                # retrieves the matching regex value from the matching
                # regex value buffer
                matching_regex_value = matching_regex_value_buffer.get_value()

                # compiles the matching regex value
                matching_regex = re.compile(matching_regex_value)

                # adds the matching regex to the matching regex list
                self.matching_regex_list.append(matching_regex)

                # sets the base value in matching regex base values map
                self.matching_regex_base_values_map[matching_regex] = current_base_value

                # re-sets the current base value
                current_base_value = index

                # resets the matching regex value buffer
                matching_regex_value_buffer.reset()

                # sets the is first flag
                is_first = True

        # retrieves the matching regex value from the matching
        # regex value buffer
        matching_regex_value = matching_regex_value_buffer.get_value()

        # compiles the matching regex value
        matching_regex = re.compile(matching_regex_value)

        # adds the matching regex to the matching regex list
        self.matching_regex_list.append(matching_regex)

        # sets the base value in matching regex base values map
        self.matching_regex_base_values_map[matching_regex] = current_base_value
