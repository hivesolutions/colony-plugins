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
import types

import colony.libs.string_buffer_util

import web_mvc_exceptions
import web_mvc_file_handler
import web_mvc_communication_handler

NAMED_GROUPS_REGEX_VALUE = "\(\?\P\<[a-zA-Z_][a-zA-Z0-9_]*\>(.+?)\)"
""" The named groups regex value """

NAMED_GROUPS_REGEX = re.compile(NAMED_GROUPS_REGEX_VALUE)
""" The named groups regex """

REGEX_COMPILATION_LIMIT = 99
""" The regex compilation limit """

FILE_HANDLER_VALUE = "file_handler"
""" The file handler value """

COMMUNICATION_HANDLER_VALUE = "communication_handler"
""" The communication handler value """

METHOD_VALUE = "method"
""" The method value """

ENCODER_NAME_VALUE = "encoder_name"
""" The encoder name value """

PATTERN_NAMES_VALUE = "pattern_names"
""" The pattern names value """

DEFAULT_STATUS_CODE = 200
""" The default status code """

class WebMvc:
    """
    The web mvc class.
    """

    web_mvc_plugin = None
    """ The web mvc plugin """

    web_mvc_file_handler = None
    """ The web mvc file handler """

    web_mvc_communication_handler = None
    """ The web mvc communication handler """

    matching_regex_list = []
    """ The list of matching regex to be used in patterns matching """

    matching_regex_base_values_map = {}
    """ The map containing the base values for the various matching regex """

    communication_matching_regex_list = []
    """ The list of matching regex to be used in communication patterns matching """

    communication_matching_regex_base_values_map = {}
    """ The map containing the base values for the various communication matching regex """

    resource_matching_regex_list = []
    """ The list of matching regex to be used in resource patterns matching """

    resource_matching_regex_base_values_map = {}
    """ The map containing the base values for the various resource matching regex """

    web_mvc_service_patterns_map = {}
    """ The web mvc service patterns map """

    web_mvc_service_pattern_escaped_map = {}
    """ The web mvc service pattern escaped map """

    web_mvc_service_pattern_compiled_map = {}
    """ The web mvc service pattern compiled map """

    web_mvc_service_patterns_list = []
    """ The web mvc service patterns list for indexing """

    web_mvc_service_communication_patterns_map = {}
    """ The web mvc service communication patterns map """

    web_mvc_service_communication_patterns_list = []
    """ The web mvc service communication patterns list for indexing """

    web_mvc_service_resource_patterns_map = {}
    """ The web mvc service resource patterns map """

    web_mvc_service_resource_patterns_list = []
    """ The web mvc service resource patterns list for indexing """

    def __init__(self, web_mvc_plugin):
        """
        Constructor of the class.

        @type web_mvc_plugin: WebMvcPlugin
        @param web_mvc_plugin: The web mvc plugin.
        """

        self.web_mvc_plugin = web_mvc_plugin

        self.matching_regex_list = []
        self.matching_regex_base_values_map = {}
        self.communication_matching_regex_list = []
        self.communication_matching_regex_base_values_map = {}
        self.resource_matching_regex_list = []
        self.resource_matching_regex_base_values_map = {}
        self.web_mvc_service_patterns_map = {}
        self.web_mvc_service_pattern_escaped_map = {}
        self.web_mvc_service_pattern_compiled_map = {}
        self.web_mvc_service_patterns_list = []
        self.web_mvc_service_communication_patterns_map = {}
        self.web_mvc_service_communication_patterns_list = []
        self.web_mvc_service_resource_patterns_map = {}
        self.web_mvc_service_resource_patterns_list = []

        self.web_mvc_file_handler = web_mvc_file_handler.WebMvcFileHandler(web_mvc_plugin)
        self.web_mvc_communication_handler = web_mvc_communication_handler.WebMvcCommunicationHandler(web_mvc_plugin)

    def get_routes(self):
        """
        Retrieves the list of regular expressions to be used as route,
        to the rest service.

        @rtype: List
        @return: The list of regular expressions to be used as route,
        to the rest service.
        """

        return [
            r"^mvc/.*$"
        ]

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

        # iterates over all the resource matching regex in the resource matching regex list
        for resource_matching_regex in self.resource_matching_regex_list:
            # tries to math the resource path
            resource_path_match = resource_matching_regex.match(resource_path)

            # in case there is no valid resource path match
            if not resource_path_match:
                # continues the loop
                continue

            # handles the match, returning the result of the handling
            self._handle_resource_match(rest_request, resource_path, resource_path_match, resource_matching_regex)

            # runs the process request in the rest request
            self._process_request(rest_request)

            # returns immediately
            return

        # iterates over all the communication matching regex in the communication matching regex list
        for communication_matching_regex in self.communication_matching_regex_list:
            # tries to math the communication path
            communication_path_match = communication_matching_regex.match(resource_path)

            # in case there is no valid communication path match
            if not communication_path_match:
                # continues the loop
                continue

            # handles the match, returning the result of the handling
            self._handle_communication_match(rest_request, resource_path, communication_path_match, communication_matching_regex)

            # runs the process request in the rest request
            self._process_request(rest_request)

            # returns immediately
            return

        # iterates over all the matching regex in the matching regex list
        for matching_regex in self.matching_regex_list:
            # tries to math the resource path
            resource_path_match = matching_regex.match(resource_path)

            # in case there is no valid resource path match
            if not resource_path_match:
                # continues the loop
                continue

            # validate the match and retrieves the handle tuple
            handle_tuple = self._validate_match(rest_request, resource_path, resource_path_match, matching_regex)

            # in case the handle tuple is not valid
            if not handle_tuple:
                # continues the loop
                continue

            # handles the match, returning the result of the handling
            self._handle_match(rest_request, handle_tuple)

            # runs the process request in the rest request
            self._process_request(rest_request)

            # returns immediately
            return

        # raises the mvc request not handled exception
        raise web_mvc_exceptions.MvcRequestNotHandled("no mvc service plugin could handle the request")

    def load_web_mvc_service_plugin(self, web_mvc_service_plugin):
        """
        Loads the given web mvc service plugin.

        @type web_mvc_service_plugin: Plugin
        @param web_mvc_service_plugin: The web mvc service plugin to be loaded.
        """

        # retrieves the web mvc service plugin patterns
        web_mvc_service_plugin_patterns = web_mvc_service_plugin.get_patterns()

        # iterates over all the patterns in the web mvc service plugin patterns
        for web_mvc_service_plugin_pattern in web_mvc_service_plugin_patterns:
            # retrieves the pattern key
            pattern_key = web_mvc_service_plugin_pattern[0]

            # retrieves the pattern value
            pattern_value = web_mvc_service_plugin_pattern[1:]

            # tries to retrieve the pattern validation regex from the web mvc
            # service pattern compiled map
            pattern_validation_regex = self.web_mvc_service_pattern_compiled_map.get(pattern_key, None)

            # compiles (in case it's necessary) the pattern key, retrieving the
            # pattern validation regex (original regex)
            pattern_validation_regex = pattern_validation_regex or re.compile(pattern_key)

            # creates the pattern attributes (tuple)
            pattern_attributes = (
                pattern_validation_regex,
                pattern_value
            )

            # escapes the pattern key replacing the named
            # group selectors
            pattern_key_escaped = NAMED_GROUPS_REGEX.sub("\g<1>", pattern_key)

            # in case the pattern key escaped does not exists
            # in the web mvc service patterns map
            if not pattern_key_escaped in self.web_mvc_service_patterns_map:
                # creates a new (pattern attributes) list for the pattern key in the
                # web mvc service patterns map
                self.web_mvc_service_patterns_map[pattern_key_escaped] = []

                # adds the pattern to the web mvc service patterns list
                self.web_mvc_service_patterns_list.append(pattern_key_escaped)

            # retrieves the pattern attributes list from the web mvc service patterns map
            pattern_attributes_list = self.web_mvc_service_patterns_map[pattern_key_escaped]

            # removes the pattern attributes from the pattern attributes list
            pattern_attributes_list.append(pattern_attributes)

            # saves the escaped and compiled values of the pattern for latter usage
            self.web_mvc_service_pattern_escaped_map[pattern_key] = pattern_key_escaped
            self.web_mvc_service_pattern_compiled_map[pattern_key] = pattern_validation_regex

        # retrieves the web mvc service plugin communication patterns
        web_mvc_service_plugin_communication_patterns = web_mvc_service_plugin.get_communication_patterns()

        # iterates over all the communication patterns in the web mvc service plugin communication patterns
        for pattern_key, pattern_value in web_mvc_service_plugin_communication_patterns:
            # adds the pattern to the web mvc service communication patterns map
            self.web_mvc_service_communication_patterns_map[pattern_key] = pattern_value

            # adds the pattern to the web mvc service communication patterns list
            self.web_mvc_service_communication_patterns_list.append(pattern_key)

        # retrieves the web mvc service plugin resource patterns
        web_mvc_service_plugin_resource_patterns = web_mvc_service_plugin.get_resource_patterns()

        # iterates over all the resource patterns in the web mvc service plugin resource patterns
        for pattern_key, pattern_value in web_mvc_service_plugin_resource_patterns:
            # adds the pattern to the web mvc service resource patterns map
            self.web_mvc_service_resource_patterns_map[pattern_key] = pattern_value

            # adds the pattern to the web mvc service resource patterns list
            self.web_mvc_service_resource_patterns_list.append(pattern_key)

        # updates the matching regex
        self._update_matching_regex()

        # updates the communication matching regex
        self._update_communication_matching_regex()

        # updates the resource matching regex
        self._update_resource_matching_regex()

    def unload_web_mvc_service_plugin(self, web_mvc_service_plugin):
        """
        Unloads the given web mvc service plugin.

        @type web_mvc_service_plugin: Plugin
        @param web_mvc_service_plugin: The web mvc service plugin to be unloaded.
        """

        # retrieves the web mvc service plugin patterns
        web_mvc_service_plugin_patterns = web_mvc_service_plugin.get_patterns()

        # iterates over all the patterns in the web mvc service plugin patterns
        for web_mvc_service_plugin_pattern in web_mvc_service_plugin_patterns:
            # retrieves the pattern key
            pattern_key = web_mvc_service_plugin_pattern[0]

            # retrieves the pattern value
            pattern_value = web_mvc_service_plugin_pattern[1:]

            # retrieves the pattern key escaped from the web mvc service
            # pattern escaped map
            pattern_key_escaped = self.web_mvc_service_pattern_escaped_map[pattern_key]

            # in case the pattern key escaped exists in the web mvc service patterns map
            if pattern_key_escaped in self.web_mvc_service_patterns_map:
                # retrieves the pattern validation regex from the web mvc service
                # pattern compiled map
                pattern_validation_regex = self.web_mvc_service_pattern_compiled_map[pattern_key]

                # creates the pattern attributes (tuple)
                pattern_attributes = (
                    pattern_validation_regex,
                    pattern_value
                )

                # retrieves the pattern attributes list from the web mvc service
                # patterns map
                pattern_attributes_list = self.web_mvc_service_patterns_map[pattern_key_escaped]

                # removes the pattern attributes from the pattern attributes list
                pattern_attributes_list.remove(pattern_attributes)

                # in case the pattern attributes list is not empty, there are
                # more patterns associated with the pattern key, no need
                # to remove the patter key references
                if pattern_attributes_list:
                    # continues the loop
                    continue

                # removes the pattern attributes list from the web mvc service patterns map
                del self.web_mvc_service_patterns_map[pattern_key_escaped]

                # removes the pattern from the web mvc service patterns list
                self.web_mvc_service_patterns_list.remove(pattern_key_escaped)

        # retrieves the web mvc service plugin communication patterns
        web_mvc_service_plugin_communication_patterns = web_mvc_service_plugin.get_communication_patterns()

        # iterates over all the communication patterns in the web mvc service plugin communication patterns
        for pattern_key, _pattern_value in web_mvc_service_plugin_communication_patterns:
            # in case the pattern key exists in the web mvc service communication patterns map
            if pattern_key in self.web_mvc_service_communication_patterns_map:
                # removes the pattern from the web mvc service communication patterns map
                del self.web_mvc_service_communication_patterns_map[pattern_key]

                # removes the pattern from the web mvc service communication patterns list
                self.web_mvc_service_communication_patterns_list.remove(pattern_key)

        # retrieves the web mvc service plugin resource patterns
        web_mvc_service_plugin_resource_patterns = web_mvc_service_plugin.get_resource_patterns()

        # iterates over all the resource patterns in the web mvc service plugin resource patterns
        for pattern_key, _pattern_value in web_mvc_service_plugin_resource_patterns:
            # in case the pattern key exists in the web mvc service resource patterns map
            if pattern_key in self.web_mvc_service_resource_patterns_map:
                # removes the pattern from the web mvc service resource patterns map
                del self.web_mvc_service_resource_patterns_map[pattern_key]

                # removes the pattern from the web mvc service resource patterns list
                self.web_mvc_service_resource_patterns_list.remove(pattern_key)

        # updates the matching regex
        self._update_matching_regex()

        # updates the communication matching regex
        self._update_communication_matching_regex()

        # updates the resource matching regex
        self._update_resource_matching_regex()

    def process_web_mvc_patterns_reload_event(self, event_name, plugin):
        # unloads the web mvc service plugin
        self.unload_web_mvc_service_plugin(plugin)

        # loads the web mvc service plugin
        self.load_web_mvc_service_plugin(plugin)

    def process_web_mvc_patterns_load_event(self, event_name, plugin):
        # loads the web mvc service plugin
        self.load_web_mvc_service_plugin(plugin)

    def process_web_mvc_patterns_unload_event(self, event_name, plugin):
        # unloads the web mvc service plugin
        self.unload_web_mvc_service_plugin(plugin)

    def process_web_mvc_communication_event(self, event_name, connection_name, message):
        # sends the broadcast message
        self.web_mvc_communication_handler.send_broadcast_communication_message(connection_name, message)

    def _handle_resource_match(self, rest_request, resource_path, resource_path_match, resource_matching_regex):
        # retrieves the base value for the matching regex
        base_value = self.resource_matching_regex_base_values_map[resource_matching_regex]

        # retrieves the group index from the resource path match
        group_index = resource_path_match.lastindex

        # calculates the web mvc service index from the base value,
        # the group index and subtracts one value
        web_mvc_service_index = base_value + group_index - 1

        # retrieves the resource pattern for the web mvc service index
        pattern = self.web_mvc_service_resource_patterns_list[web_mvc_service_index]

        # retrieves the resource information
        resource_information = self.web_mvc_service_resource_patterns_map[pattern]

        # unpacks the resource information
        resource_base_path, resource_initial_token = resource_information

        # in case the resource path does not start with the resource
        # initial token
        if not resource_path.startswith(resource_initial_token):
            # raises the invalid token value
            raise web_mvc_exceptions.InvalidTokenValue("invalid initial path request")

        # retrieves the resources initial token length
        resource_initial_token_length = len(resource_initial_token)

        # creates the file path from the resource base path and file path
        file_path = resource_base_path + "/" + resource_path[resource_initial_token_length:] + "." + rest_request.encoder_name

        # handles the given request by the web mvc file handler
        self.web_mvc_file_handler.handle_request(rest_request.request, file_path)

    def _handle_communication_match(self, rest_request, resource_path, communication_path_match, communication_matching_regex):
        # retrieves the base value for the matching regex
        base_value = self.communication_matching_regex_base_values_map[communication_matching_regex]

        # retrieves the group index from the communication path match
        group_index = communication_path_match.lastindex

        # calculates the web mvc service index from the base value,
        # the group index and subtracts one value
        web_mvc_service_index = base_value + group_index - 1

        # retrieves the communication pattern for the web mvc service index
        pattern = self.web_mvc_service_communication_patterns_list[web_mvc_service_index]

        # retrieves the communication information
        communication_information = self.web_mvc_service_communication_patterns_map[pattern]

        # unpacks the communication information
        data_handler_method, connection_changed_handler_method, connection_name = communication_information

        # handles the given request by the web mvc communication handler
        self.web_mvc_communication_handler.handle_request(rest_request.request, data_handler_method, connection_changed_handler_method, connection_name)

    def _validate_match(self, rest_request, resource_path, resource_path_match, matching_regex):
        # retrieves the base value for the matching regex
        base_value = self.matching_regex_base_values_map[matching_regex]

        # retrieves the group index from the resource path match
        group_index = resource_path_match.lastindex

        # calculates the web mvc service index from the base value,
        # the group index and subtracts one value
        web_mvc_service_index = base_value + group_index - 1

        # retrieves the pattern for the web mvc service index
        pattern = self.web_mvc_service_patterns_list[web_mvc_service_index]

        # retrieves the pattern attributes list from the web
        # mvc service patterns map
        pattern_attributes_list = self.web_mvc_service_patterns_map[pattern]

        # starts the return value
        return_value = None

        # iterates over all the pattern attributes (handler attributes)
        # in the pattern attributes list
        for handler_attributes in pattern_attributes_list:
            # tries to validation the match using the rest request,
            # handler attributes and the resource path
            return_value = self.__validate_match(rest_request, handler_attributes, resource_path)

            # in case the return value is not valid
            # (no success in validation)
            if not return_value:
                # continues the loop
                continue

            # breaks the loop (valid match)
            break

        # returns the return value
        return return_value

    def _handle_match(self, rest_request, handler_tuple):
        # unpacks the handler tuple
        handler_method, parameters = handler_tuple

        # handles the web mvc request to the handler method
        handler_method(rest_request, parameters)

    def _process_request(self, rest_request):
        """
        Processes the given rest request, changing its
        attributes to provide a valid rest request.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be "processed".
        """

        # retrieves the rest request status code
        rest_request_status_code = rest_request.get_status_code()

        # checks if the status code is set in the rest request
        is_set_status_code = rest_request_status_code and True or False

        # sets the default status code in case it's not already set
        not is_set_status_code and rest_request.set_status_code(DEFAULT_STATUS_CODE)

    def _update_matching_regex(self):
        """
        Updates the matching regex.
        """

        # starts the matching regex value buffer
        matching_regex_value_buffer = colony.libs.string_buffer_util.StringBuffer()

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

        # iterates over all the patterns in the web mvc service patterns list
        for pattern in self.web_mvc_service_patterns_list:
            # in case it's the first
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # adds the or operand to the matching regex value buffer
                matching_regex_value_buffer.write("|")

            # adds the group name part of the regex to the matching regex value buffer
            matching_regex_value_buffer.write("(" + pattern + ")")

            # increments the index
            index += 1

            # in case the current index is in the limit of the python
            # regex compilation
            if index % REGEX_COMPILATION_LIMIT == 0:
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

        # in case the matching regex value is invalid (empty)
        if not matching_regex_value:
            # returns immediately
            return

        # compiles the matching regex value
        matching_regex = re.compile(matching_regex_value)

        # adds the matching regex to the matching regex list
        self.matching_regex_list.append(matching_regex)

        # sets the base value in matching regex base values map
        self.matching_regex_base_values_map[matching_regex] = current_base_value

    def _update_communication_matching_regex(self):
        """
        Updates the communication matching regex.
        """

        # starts the communication matching regex value buffer
        communication_matching_regex_value_buffer = colony.libs.string_buffer_util.StringBuffer()

        # clears the communication matching regex list
        self.communication_matching_regex_list = []

        # clears the communication matching regex base value map
        self.communication_matching_regex_base_values_map.clear()

        # sets the is first flag
        is_first = True

        # starts the index value
        index = 0

        # starts the current base value
        current_base_value = 0

        # iterates over all the patterns in the web mvc service communication patterns list
        for pattern in self.web_mvc_service_communication_patterns_list:
            # in case it's the first
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # adds the or operand to the communication matching regex value buffer
                communication_matching_regex_value_buffer.write("|")

            # adds the group name part of the regex to the communication matching regex value buffer
            communication_matching_regex_value_buffer.write("(" + pattern + ")")

            # increments the index
            index += 1

            # in case the current index is in the limit of the python
            # regex compilation
            if index % REGEX_COMPILATION_LIMIT == 0:
                # retrieves the communication matching regex value from the communication matching
                # regex value buffer
                communication_matching_regex_value = communication_matching_regex_value_buffer.get_value()

                # compiles the communication matching regex value
                reource_matching_regex = re.compile(communication_matching_regex_value)

                # adds the communication matching regex to the matching regex list
                self.communication_matching_regex_list.append(reource_matching_regex)

                # sets the base value in communication matching regex base values map
                self.communication_matching_regex_base_values_map[reource_matching_regex] = current_base_value

                # re-sets the current base value
                current_base_value = index

                # resets the matching regex value buffer
                communication_matching_regex_value_buffer.reset()

                # sets the is first flag
                is_first = True

        # retrieves the communication matching regex value from the communication matching
        # regex value buffer
        communication_matching_regex_value = communication_matching_regex_value_buffer.get_value()

        # in case the communication matching regex value is invalid (empty)
        if not communication_matching_regex_value:
            # returns immediately
            return

        # compiles the communication matching regex value
        communication_matching_regex = re.compile(communication_matching_regex_value)

        # adds the matching regex to the communication matching regex list
        self.communication_matching_regex_list.append(communication_matching_regex)

        # sets the base value in communication matching regex base values map
        self.communication_matching_regex_base_values_map[communication_matching_regex] = current_base_value

    def _update_resource_matching_regex(self):
        """
        Updates the resource matching regex.
        """

        # starts the resource matching regex value buffer
        resource_matching_regex_value_buffer = colony.libs.string_buffer_util.StringBuffer()

        # clears the resource matching regex list
        self.resource_matching_regex_list = []

        # clears the resource matching regex base value map
        self.resource_matching_regex_base_values_map.clear()

        # sets the is first flag
        is_first = True

        # starts the index value
        index = 0

        # starts the current base value
        current_base_value = 0

        # iterates over all the patterns in the web mvc service resource patterns list
        for pattern in self.web_mvc_service_resource_patterns_list:
            # in case it's the first
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # adds the or operand to the resource matching regex value buffer
                resource_matching_regex_value_buffer.write("|")

            # adds the group name part of the regex to the resource matching regex value buffer
            resource_matching_regex_value_buffer.write("(" + pattern + ")")

            # increments the index
            index += 1

            # in case the current index is in the limit of the python
            # regex compilation
            if index % REGEX_COMPILATION_LIMIT == 0:
                # retrieves the resource matching regex value from the resource matching
                # regex value buffer
                resource_matching_regex_value = resource_matching_regex_value_buffer.get_value()

                # compiles the resource matching regex value
                reource_matching_regex = re.compile(resource_matching_regex_value)

                # adds the resource matching regex to the matching regex list
                self.resource_matching_regex_list.append(reource_matching_regex)

                # sets the base value in resource matching regex base values map
                self.resource_matching_regex_base_values_map[reource_matching_regex] = current_base_value

                # re-sets the current base value
                current_base_value = index

                # resets the matching regex value buffer
                resource_matching_regex_value_buffer.reset()

                # sets the is first flag
                is_first = True

        # retrieves the resource matching regex value from the resource matching
        # regex value buffer
        resource_matching_regex_value = resource_matching_regex_value_buffer.get_value()

        # in case the resource matching regex value is invalid (empty)
        if not resource_matching_regex_value:
            # returns immediately
            return

        # compiles the resource matching regex value
        resource_matching_regex = re.compile(resource_matching_regex_value)

        # adds the matching regex to the resource matching regex list
        self.resource_matching_regex_list.append(resource_matching_regex)

        # sets the base value in resource matching regex base values map
        self.resource_matching_regex_base_values_map[resource_matching_regex] = current_base_value

    def __validate_match(self, rest_request, handler_attributes, resource_path):
        # unpacks the handler attributes, retrieving the handler
        # validation regex and the handler arguments
        handler_validation_regex, handler_arguments = handler_attributes

        # matches the resource path against the validation match
        resource_path_validation_match = handler_validation_regex.match(resource_path)

        # in case there is no resource path validation match
        if not resource_path_validation_match:
            # raises the runtime request exception
            raise web_mvc_exceptions.RuntimeRequestException("invalid resource path validation match")

        # retrieves the length of the handler arguments
        handler_arguments_length = len(handler_arguments)

        # retrieves the handler method from the handler arguments
        handler_method = handler_arguments_length > 0 and handler_arguments[0] or None

        # retrieves the handler operation types from the handler arguments
        handler_operation_types = handler_arguments_length > 1 and handler_arguments[1] or ("get", "put", "post", "delete")

        # retrieves the handler encoders from the handler arguments
        handler_encoders = handler_arguments_length > 2 and handler_arguments[2] or None

        # retrieves the handler constraints from the handler arguments
        handler_contraints = handler_arguments_length > 3 and handler_arguments[3] or {}

        # casts the values to tuples
        handler_operation_types = self.__cast_tuple(handler_operation_types)
        handler_encoders = self.__cast_tuple(handler_encoders)

        # retrieves the request
        request = rest_request.get_request()

        # retrieves the request operation type
        request_operation_type = request.operation_type

        # lowers the request operation type
        request_operation_type = request_operation_type.lower()

        # retrieves the rest request encoder name
        rest_request_encoder_name = rest_request.encoder_name

        # in case the request operation type does not exists in the
        # handler operation types
        if not request_operation_type in handler_operation_types:
            # returns none (invalid)
            return None

        # in case the handler encoders are defined and the rest
        # request encoder name does not exists in the handler encoders
        if handler_encoders and not rest_request_encoder_name in handler_encoders:
            # returns none (invalid)
            return None

        # iterates over all the handler constraints
        for handler_contraint_name, handler_contraint_value in handler_contraints.items():
            # retrieves the handler constraint value type
            handler_contraint_value_type = type(handler_contraint_value)

            # retrieves the attribute value base on the
            # handler constraint name
            attribute_value = rest_request.get_attribute(handler_contraint_name)

            try:
                # casts the attribute value
                attribute_value_casted = handler_contraint_value_type(attribute_value)
            except:
                # returns none (invalid)
                return None

            # in case the attribute value (casted) is not equals
            # to the handler constraint name
            if not attribute_value_casted == handler_contraint_value:
                # returns none (invalid)
                return None

        # retrieves the resource path validation match groups map
        resource_path_validation_match_groups_map = resource_path_validation_match.groupdict()

        # sets the parameters as an empty map
        parameters = {}

        # sets the extra parameters
        parameters[FILE_HANDLER_VALUE] = self.web_mvc_file_handler
        parameters[COMMUNICATION_HANDLER_VALUE] = self.web_mvc_communication_handler
        parameters[METHOD_VALUE] = request_operation_type
        parameters[ENCODER_NAME_VALUE] = rest_request_encoder_name
        parameters[PATTERN_NAMES_VALUE] = resource_path_validation_match_groups_map

        # creates the handler tuple
        handler_tuple = (
            handler_method,
            parameters
        )

        # returns the handler tuple
        return handler_tuple

    def __cast_tuple(self, value):
        """
        Casts the given value to a tuple,
        converting it if required.

        @type value: Object
        @param value: The value to be "casted".
        @rtype: Tuple
        @return: The casted tuple value.
        """

        # in case the value is invalid
        if value == None:
            # returns the value
            return value

        # creates the tuple value from the value
        tuple_value = type(value) == types.TupleType and value or (value,)

        # returns the tuple value
        return tuple_value
