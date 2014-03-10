#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import types

import colony

import exceptions
import file_handler
import communication

NAMED_GROUPS_REGEX_VALUE = "\(\?\P\<[a-zA-Z_][a-zA-Z0-9_]*\>(.+?)\)"
""" The named groups regex value """

NAMED_GROUPS_REGEX = re.compile(NAMED_GROUPS_REGEX_VALUE)
""" The named groups regex """

REPLACE_REGEX = re.compile("(?<!\(\?P)\<((\w+):)?(\w+)\>")
""" The regular expression to be used in the replacement
of the capture groups for the urls, this regex will capture
any named group not change until this stage (eg: int,
string, regex, etc.) """

INT_REGEX = re.compile("\<int:(\w+)\>")
""" The regular expression to be used in the replacement
of the integer type based groups for the urls """

REGEX_COMPILATION_LIMIT = 99
""" The regex compilation limit """

GET_DEFAULT_PARAMETERS_VALUE = "get_default_parameters"
""" The get default parameters value """

DEFAULT_STATUS_CODE = 200
""" The default status code, by default every request
is considered to be successful """

TYPES_R = dict(
    int = int,
    str = str
)
""" Map that resolves a data type from the string representation
to the proper type value to be used in casting """

class Mvc(colony.System):
    """
    The mvc class.
    """

    mvc_file_handler = None
    """ The mvc file handler """

    mvc_communication_handler = None
    """ The mvc communication handler """

    clear_pending = False
    """ Flag that controls if the rest sessions should be
    cleared at the next tick of handling """

    matching_regex_list = []
    """ The list of matching regex to be used in
    patterns matching """

    matching_regex_base_map = {}
    """ The map containing the base (values) for the
    various matching regex, this is the base index
    for the computation of index """

    communication_matching_regex_list = []
    """ The list of matching regex to be used in
    communication patterns matching """

    communication_matching_regex_base_map = {}
    """ The map containing the base indexes for the
    various communication matching regex """

    resource_matching_regex_list = []
    """ The list of matching regex to be used in
    resource patterns matching """

    resource_matching_regex_base_map = {}
    """ The map containing the base indexes for the
    various resource matching regex """

    patterns_map = {}
    """ The patterns map """

    pattern_escaped_map = {}
    """ The pattern escaped map """

    pattern_compiled_map = {}
    """ The pattern compiled map """

    patterns_list = []
    """ The patterns list for indexing """

    communication_patterns_map = {}
    """ The communication patterns map """

    communication_patterns_list = []
    """ The communication patterns list
    for indexing """

    resource_patterns_map = {}
    """ The resource patterns map """

    resource_patterns_list = []
    """ The resource patterns list for indexing """

    patterns_index = {}
    """ Dictionary associating the action method name, as a string with
    the plugin name, controller name and action name with the proper
    pattern tuple, this is going to be used for runtime based resolution
    of routes as defined by the specification """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)

        self.matching_regex_list = []
        self.matching_regex_base_map = {}
        self.communication_matching_regex_list = []
        self.communication_matching_regex_base_map = {}
        self.resource_matching_regex_list = []
        self.resource_matching_regex_base_map = {}
        self.patterns_map = {}
        self.pattern_escaped_map = {}
        self.pattern_compiled_map = {}
        self.patterns_list = []
        self.communication_patterns_map = {}
        self.communication_patterns_list = []
        self.resource_patterns_map = {}
        self.resource_patterns_list = []
        self.patterns_index = {}

        self.mvc_file_handler = file_handler.MvcFileHandler(plugin)
        self.mvc_communication_handler = communication.MvcCommunicationHandler(plugin)

    def start_system(self):
        """
        Starts the mvc system structures.
        This method starts all the persistent and
        background execution tasks for mvc.

        Note that the execution og background tasks
        is conditioned to the current thread execution
        policy and permissions from the manager.
        """

        # retrieves the plugin manager reference and uses it to check
        # if the communication handler processing system should be
        # started, because if threads are not allowed no process should
        # be started (violates manger rules)
        plugin_manager = self.plugin.manager
        if plugin_manager.allow_threads: self.mvc_communication_handler.start_processing()

    def stop_system(self):
        """
        Stops the mvc system structures.
        This method stops all the persistent and
        background execution tasks for mvc.
        """

        # retrieves the plugin manager to recall the option to load or not
        # the communication handler in case the handler has been started it
        # must now be stopped to avoid any memory or other resource leak
        plugin_manager = self.plugin.manager
        if plugin_manager.allow_threads: self.mvc_communication_handler.stop_processing()

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
        Handles the given rest request, the method starts by
        trying to match any of the regular expression in the
        various areas, in case it matches handles it accordingly
        and processes the request (post request execution).

        The execution follows a order of resources, communication
        and at last normal (dynamic) handling.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled, this
        value is going to be encapsulated into an abstract request
        interface to be handled by the underlying mvc services.
        """

        # in case the clear pending flag is set must remove
        # (clear) all the current sessions from the rest manager
        # this is a global reset (side problems may occur)
        if self.clear_pending: rest_request.clear_sessions(); self.clear_pending = False

        # retrieves the path list, then joins the path list
        # to create the resource path
        path_list = rest_request.get_path_list()
        resource_path = "/".join(path_list)

        # iterates over all the resource matching regex in the
        # resource matching regex list to try to match any of
        # them and execute the proper action if such occurs
        for resource_matching_regex in self.resource_matching_regex_list:
            # tries to math the resource path in case there is no
            # valid resource path match must continue the loop
            resource_path_match = resource_matching_regex.match(resource_path)
            if not resource_path_match: continue

            # handles the match using the resource handler, this should update the
            # response object with the proper contents, then runs the post handling
            # request processor so that the request object remains in the expected state
            self._handle_resource_match(
                rest_request,
                resource_path,
                resource_path_match,
                resource_matching_regex
            )
            self._process_request(rest_request)

            # returns immediately, no more matching tries should
            # occur (already matched)
            return

        # iterates over all the communication matching regex in the
        # communication matching regex list to try to match any of
        # them and execute the proper action if such occurs
        for communication_matching_regex in self.communication_matching_regex_list:
            # tries to math the communication path in case there is no
            # valid communication path match must continue the loop
            communication_path_match = communication_matching_regex.match(resource_path)
            if not communication_path_match: continue

            # handles the match using the communication handler, this should update the
            # response object with the proper contents, then runs the post handling
            # request processor so that the request object remains in the expected state
            self._handle_communication_match(
                rest_request,
                resource_path,
                communication_path_match,
                communication_matching_regex
            )
            self._process_request(rest_request)

            # returns immediately
            return

        # iterates over all the (dynamic) matching regex in the
        # (dynamic) matching regex list to try to match any of
        # them and execute the proper action if such occurs
        for matching_regex in self.matching_regex_list:
            # tries to math the resource path in case there is
            # no valid resource path match must continue the loop
            resource_path_match = matching_regex.match(resource_path)
            if not resource_path_match: continue

            # validate the match and retrieves the handle tuple and in
            # case the handle tuple is invalid continues immediately
            # because it's not possible to process the request
            handle_tuple = self._validate_match(
                rest_request, resource_path, resource_path_match, matching_regex
            )
            if not handle_tuple: continue

            # handles the match using the (dynamic) handler, this should update the
            # response object with the proper contents, then runs the post handling
            # request processor so that the request object remains in the expected state
            self._handle_match(rest_request, handle_tuple)
            self._process_request(rest_request)

            # returns immediately
            return

        # raises the mvc request not handled exception, because no mvc
        # service was found for the current request constraints
        raise exceptions.MvcRequestNotHandled("no mvc service plugin could handle the request")

    def load_mvc_service_plugin(self, mvc_service_plugin):
        """
        Loads the given mvc service plugin, this process is focused
        on the extraction of the patterns from the plugin and in
        the correct update of the internal structures of the mvc
        to handling these "new" patterns.

        @type mvc_service_plugin: Plugin
        @param mvc_service_plugin: The mvc service plugin to be loaded.
        """

        # verifies the existence of all the method in the facade of the plugin
        # that are going to be used fore retrieval of patterns so that only the
        # ones that exist are called and for the others fallback values are used
        has_patterns = hasattr(mvc_service_plugin, "get_patterns")
        has_communication_patterns = hasattr(mvc_service_plugin, "get_communication_patterns")
        has_resource_patterns = hasattr(mvc_service_plugin, "get_resource_patterns")

        # retrieves the complete set of patterns from the
        # mvc service plugin to load them into the internal structures
        patterns = mvc_service_plugin.get_patterns() if has_patterns else ()
        communication_patterns = mvc_service_plugin.get_communication_patterns() if has_communication_patterns else ()
        resource_patterns = mvc_service_plugin.get_resource_patterns() if has_resource_patterns else ()

        # runs the normalization process for the various patterns
        # that have been retrieved so that the patterns are correctly
        # processed and converted from their canonical form, note that
        # the first set of patters are normalized with some extra operations
        # applied to them meaning that some meta information is also added
        # to each of the pattern tuples (as defined in specification)
        patterns = self._normalize_patterns(patterns, extra = True)
        communication_patterns = self._normalize_patterns(communication_patterns)
        resource_patterns = self._normalize_patterns(resource_patterns)

        # runs the underling registration of the complete set of patterns
        # so that they may be resolved at runtime from name to route
        self.register_patterns(patterns)

        # iterates over all the patterns to update the internal structures
        # to reflect their changes
        for pattern in patterns:
            # retrieves both the pattern key and value, the first element
            # of the pattern is the key and the remaining elements are
            # considered to be the values
            pattern_key = pattern[0]
            pattern_value = pattern[1:]

            # tries to retrieve the pattern validation regex from the
            # pattern compiled map, then in case it's not found compiles
            # it (only one compilation should occur)
            pattern_validation_regex = self.pattern_compiled_map.get(pattern_key, None)
            pattern_validation_regex = pattern_validation_regex or re.compile(pattern_key)

            # creates the pattern attributes (tuple) with both the validation
            # regex and the value
            pattern_attributes = (
                pattern_validation_regex,
                pattern_value
            )

            # escapes the pattern key replacing the named
            # group selectors, this is required so that the
            # proper key matching is possible
            pattern_key_escaped = NAMED_GROUPS_REGEX.sub("\g<1>", pattern_key)

            # in case the pattern key escaped does not exists
            # in the patterns map must add it to the structures
            if not pattern_key_escaped in self.patterns_map:
                # creates a new (pattern attributes) list for the pattern key in the
                # mvc service patterns map and then add the escaped pattern key
                # to the list of patterns
                self.patterns_map[pattern_key_escaped] = []
                self.patterns_list.append(pattern_key_escaped)

            # retrieves the pattern attributes list from the patterns map
            # and then adds pattern attributes to the pattern attributes list
            pattern_attributes_list = self.patterns_map[pattern_key_escaped]
            pattern_attributes_list.append(pattern_attributes)

            # saves the escaped and compiled values of the pattern for latter usage
            self.pattern_escaped_map[pattern_key] = pattern_key_escaped
            self.pattern_compiled_map[pattern_key] = pattern_validation_regex

        # iterates over all the communication patterns to add their key and
        # value to the internal structures
        for pattern_key, pattern_value in communication_patterns:
            # adds the pattern to the communication patterns map for the
            # provided key and the key to the communication patterns list
            self.communication_patterns_map[pattern_key] = pattern_value
            self.communication_patterns_list.append(pattern_key)

        # iterates over all the resource patterns to add their key and
        # value to the internal structures
        for pattern_key, pattern_value in resource_patterns:
            # adds the pattern to the resource patterns map for the
            # provided key and the key to the resource patterns list
            self.resource_patterns_map[pattern_key] = pattern_value
            self.resource_patterns_list.append(pattern_key)

        # updates the complete set of matching regex, this should
        # be able to provide the correct version of the regex handler
        # methods association
        self._update_matching_regex()
        self._update_communication_matching_regex()
        self._update_resource_matching_regex()

    def unload_mvc_service_plugin(self, mvc_service_plugin):
        """
        Unloads the given mvc service plugin, this should remove
        any reference of the various patterns contained in the
        mvc service plugin from the current internal structures.

        Any further mvc request should not be able to be handled
        by the plugins's patterns.

        @type mvc_service_plugin: Plugin
        @param mvc_service_plugin: The mvc service plugin to be unloaded.
        """

        # sets the clear (session) pending flag so that the sessions
        # are cleared for the next handling tick
        self.clear_pending = True

        # verifies the existence of all the method in the facade of the plugin
        # that are going to be used fore retrieval of patterns so that only the
        # ones that exist are called and for the others fallback values are used
        has_patterns = hasattr(mvc_service_plugin, "get_patterns")
        has_communication_patterns = hasattr(mvc_service_plugin, "get_communication_patterns")
        has_resource_patterns = hasattr(mvc_service_plugin, "get_resource_patterns")

        # retrieves the complete set of patterns from the
        # mvc service plugin to unload them from the internal structures
        patterns = mvc_service_plugin.get_patterns() if has_patterns else ()
        communication_patterns = mvc_service_plugin.get_communication_patterns() if has_communication_patterns else ()
        resource_patterns = mvc_service_plugin.get_resource_patterns() if has_resource_patterns else ()

        # runs the normalization process for the various patterns
        # that have been retrieved so that the patterns are correctly
        # processed and converted from their canonical form, note that
        # the first set of patters are normalized with some extra operations
        # applied to them meaning that some meta information is also added
        # to each of the pattern tuples (as defined in specification)
        patterns = self._normalize_patterns(patterns, extra = True)
        communication_patterns = self._normalize_patterns(communication_patterns)
        resource_patterns = self._normalize_patterns(resource_patterns)

        # runs the underling unregistration of the complete set of patterns
        # so that they no longer may be resolved at runtime from name to route
        self.unregister_patterns(patterns)

        # iterates over all the patterns to update the internal structures
        # to reflect their changes (removes references)
        for pattern in patterns:
            # retrieves both the pattern key and value, the first element
            # of the pattern is the key and the remaining elements are
            # considered to be the values
            pattern_key = pattern[0]
            pattern_value = pattern[1:]

            # retrieves the pattern key escaped from the pattern
            # escaped map
            pattern_key_escaped = self.pattern_escaped_map[pattern_key]

            # in case the pattern key escaped exists in the patterns map
            # must update the internal structures
            if pattern_key_escaped in self.patterns_map:
                # retrieves the pattern validation regex from the pattern
                # compiled map
                pattern_validation_regex = self.pattern_compiled_map[pattern_key]

                # creates the pattern attributes (tuple) with both the validation
                # regex and the value
                pattern_attributes = (
                    pattern_validation_regex,
                    pattern_value
                )

                # retrieves the pattern attributes list from the mvc service
                # patterns map and then removes the pattern attributes
                # from the pattern attributes list
                pattern_attributes_list = self.patterns_map[pattern_key_escaped]
                pattern_attributes_list.remove(pattern_attributes)

                # in case the pattern attributes list is not empty, there are
                # more patterns associated with the pattern key, no need
                # to remove the patter key references, continues the loop
                if pattern_attributes_list: continue

                # removes the pattern attributes list from the patterns map
                # and then removes the pattern from the patterns list
                del self.patterns_map[pattern_key_escaped]
                self.patterns_list.remove(pattern_key_escaped)

        # iterates over all the communication patterns to remove their
        # references from the internal structures
        for pattern_key, _pattern_value in communication_patterns:
            # in case the pattern key exists in the current communication
            # patterns updates both the communication patterns map and
            # list by removing associations
            if not pattern_key in self.communication_patterns_map: continue
            del self.communication_patterns_map[pattern_key]
            self.communication_patterns_list.remove(pattern_key)

        # iterates over all the resource patterns to remove their
        # references from the internal structures
        for pattern_key, _pattern_value in resource_patterns:
            # in case the pattern key exists in the current
            # resource patterns updates both the resource patterns
            # map and list by removing associations
            if not pattern_key in self.resource_patterns_map: continue
            del self.resource_patterns_map[pattern_key]
            self.resource_patterns_list.remove(pattern_key)

        # updates the complete set of matching regex, this should
        # be able to provide the correct version of the regex handler
        # methods association
        self._update_matching_regex()
        self._update_communication_matching_regex()
        self._update_resource_matching_regex()

    def process_mvc_patterns_reload_event(self, event_name, plugin):
        # unloads the mvc service plugin and then load it again
        # this should reflect a reloading event
        self.unload_mvc_service_plugin(plugin)
        self.load_mvc_service_plugin(plugin)

    def process_mvc_patterns_load_event(self, event_name, plugin):
        # loads the mvc service plugin
        self.load_mvc_service_plugin(plugin)

    def process_mvc_patterns_unload_event(self, event_name, plugin):
        # unloads the mvc service plugin
        self.unload_mvc_service_plugin(plugin)

    def process_mvc_communication_event(self, event_name, connection_name, message):
        # sends the broadcast message
        self.mvc_communication_handler.send_broadcast(connection_name, message)

    def register_patterns(self, patterns):
        for pattern in patterns: self.register_pattern(pattern)

    def unregister_patterns(self, patterns):
        for pattern in patterns: self.unregister_pattern(pattern)

    def register_pattern(self, pattern):
        name = self.pattern_name(pattern)
        self.patterns_index[name] = pattern

    def unregister_pattern(self, pattern):
        name = self.pattern_name(pattern)
        del self.patterns_index[name]

    def pattern_name(self, pattern):
        method = pattern[1]
        is_method = hasattr(method, "im_class")
        if is_method:
            cls = method.im_class
            self = method.im_self
            name = method.__name__
            cls_name = cls.__name__
            cls_name = colony.to_underscore(cls_name)
            if cls_name.endswith("_controller"): cls_name = cls_name[:-11]
            short_name = self.plugin.short_name
            name = "%s.%s.%s" % (short_name, cls_name, name)
        else:
            name = method.__name__
        return name

    def resolve(self, request, name, *args, **kwargs):
        # retrieves the controller associated with the request and
        # uses it to retrieve the associated plugin and short name
        # of (to be used in default name resolution)
        controller = request.controller
        plugin = controller.plugin
        short_name = plugin.short_name
        name_s = "%s.%s" % (short_name, name)

        # tries the resolution of the patter using both the minimized
        # (no plugin identifier) approach (fallback) and the full
        # base name approach, and in case no pattern is resolved
        # returns immediately (no resolution was possible)
        pattern = self.patterns_index.get(name_s, None)
        pattern = self.patterns_index.get(name, pattern)
        if not pattern: return None

        # retrieves the patter meta information map from the pattern
        # tuple and uses it to retrieve the original route name and
        # the list of name tuples (for replacement in regex)
        meta = pattern[5]
        base = meta.get("original", None)
        names_t = meta.get("names_t", {})

        # strips the base name from the possible trailing values (that
        # are not part of the url path)
        base = base.rstrip("$")
        base = base.lstrip("^/")

        # creates the list that will hold the various key to value strings
        # that are going to be used as part of the query string
        query = []

        # iterates over all the keyword based arguments to try to either
        # populate the various parts of the url with arguments or the
        # parameters part of the query sequence with key based values
        for key, value in kwargs.iteritems():
            value_t = type(value)
            is_string = value_t in types.StringTypes
            if not is_string: value = str(value)
            replacer = names_t.get(key, None)
            if replacer:
                base = base.replace(replacer, value)
            else:
                key_q = colony.quote(key)
                value_q = colony.quote(value)
                param = key_q + "=" + value_q
                query.append(param)

        # quotes the final base url value (already processed)
        # and joins the complete set of key values for the query
        # concatenating then the result from both (final resolution)
        location = colony.quote(base)
        query_s = "&".join(query)
        return location + "?" + query_s if query_s else location

    def _handle_resource_match(self, rest_request, resource_path, path_match, matching_regex):
        # retrieves the base index (offset index) for the matching regex
        # this is going to be used in the calculus of the service index
        base_index = self.resource_matching_regex_base_map[matching_regex]

        # retrieves the group index from the resource path match
        group_index = path_match.lastindex

        # calculates the mvc service index from the base index,
        # the group index and subtracts one value and uses it
        # to retrieves the resource pattern
        mvc_service_index = base_index + group_index - 1
        pattern = self.resource_patterns_list[mvc_service_index]

        # retrieves the (resource) information and then unpacks it
        # into the base path and the initial token values
        information = self.resource_patterns_map[pattern]
        base_path, initial_token = information

        # in case the resource path does not start with the resource
        # initial token raises the invalid token value
        if not resource_path.startswith(initial_token):
            raise exceptions.InvalidTokenValue("invalid initial path request")

        # retrieves the resources initial token length and uses it
        # to create the file path from the base path and file path
        # note that the encoder name is only added in case it's
        # currently defined (as defined in the specification)
        initial_token_l = len(initial_token)
        file_path = base_path + "/" + resource_path[initial_token_l + 1:]
        if rest_request.encoder_name: file_path += "." + rest_request.encoder_name

        # handles the given request by the mvc file handler
        self.mvc_file_handler.handle_request(
            rest_request.request,
            file_path
        )

    def _handle_communication_match(self, rest_request, resource_path, path_match, matching_regex):
        # retrieves the base index (offset index) for the matching regex
        # this is going to be used in the calculus of the service index
        base_index = self.communication_matching_regex_base_map[matching_regex]

        # retrieves the group index from the communication path match
        group_index = path_match.lastindex

        # calculates the mvc service index from the base index,
        # the group index and subtracts one value and uses it to
        # retrieves the communication pattern
        mvc_service_index = base_index + group_index - 1
        pattern = self.communication_patterns_list[mvc_service_index]

        # retrieves the (communication) information and then unpacks it
        # into the delegate (object) and connection name
        information = self.communication_patterns_map[pattern]
        delegate, connection_name = information

        # handles the given request by the mvc communication handler
        self.mvc_communication_handler.handle_request(
            rest_request,
            delegate,
            connection_name
        )

    def _validate_match(self, rest_request, resource_path, path_match, matching_regex):
        # retrieves the base index (offset index) for the matching regex
        # this is going to be used in the calculus of the service index
        base_index = self.matching_regex_base_map[matching_regex]

        # retrieves the group index from the resource path match
        group_index = path_match.lastindex

        # calculates the mvc service index from the base index,
        # the group index and subtracts one value and uses it to
        # retrieve the pattern
        mvc_service_index = base_index + group_index - 1
        pattern = self.patterns_list[mvc_service_index]

        # retrieves the pattern attributes list from the
        # mvc service patterns map
        pattern_attributes_list = self.patterns_map[pattern]

        # starts the return value
        return_value = None

        # iterates over all the pattern attributes (handler attributes)
        # in the pattern attributes list
        for handler_attributes in pattern_attributes_list:
            # tries to validation the match using the rest request,
            # handler attributes and the resource path
            return_value = self.__validate_match(rest_request, handler_attributes, resource_path)

            # in case the return value is not valid
            # (no success in validation) must continue
            # the loop (keep trying)
            if not return_value: continue

            # breaks the loop (valid match)
            break

        # returns the return value
        return return_value

    def _handle_match(self, rest_request, handler_tuple):
        """
        Handles a regular expression match, redirecting the
        control flow into the appropriate registered handler method.

        This is the method that is equivalent to the general concept
        of "dispatching" for the request.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be "handled".
        @type handler_tuple: Tuple
        @param handler_tuple: The tuple containing the handler method
        and the parameters to be used for handling.
        """

        # unpacks the handler tuple into the handler
        # method and the parameters
        handler_method, parameters = handler_tuple

        # retrieves some of the parameters as they are going to
        # be used to infer the real (type converted) value for
        # each of the patterns to be sent to the method
        encoder = parameters.get("encoder_name", None)
        pattern_names = parameters.get("pattern_names", {})
        meta = parameters.get("meta", {})
        names = meta.get("names", {})

        # iterates over the complete set of values in the names
        # map to converts the various patterns into the defined
        # target type as defined in pattern expression
        for name, type_r in names.iteritems():
            value = pattern_names.get(name, None)
            try: value = type_r(value)
            except: value = value
            pattern_names[name] = value

        # verifies if the handler method is either a method (received
        # the self context as first argument) or a plain function so
        # that if it is a method the context will be considered the
        # controller and so it must be set in the rest request for
        # context based diffusion (may be used to retrieve controller
        # inside a model context) as defined in specification, this
        # operation is considered to be the controller injection
        has_self = hasattr(handler_method, "im_self")
        controller = handler_method.im_self if has_self else None
        rest_request.controller = controller

        # injects the parameters in the rest request so that any
        # underlying method is able to recover the parameters without
        # the proper parameters passing (useful for simplifications)
        rest_request.parameters = parameters

        # sets the reference to the resolve method in the request
        # this is the method from which it's possible to resolve a
        # dynamic resource into a proper relative url path, it may
        # be used during the life time of the request
        rest_request.resolve = self.resolve

        # in case there's an encoder name defined and the controller
        # plugin references an encoding plugin that candidates for that
        # type of encoding the same plugin is set as the serializer for
        # the current rest request being handled
        if encoder and hasattr(controller.plugin, encoder + "_plugin"):
            encoder_plugin = getattr(controller.plugin, encoder + "_plugin")
            parameters["serializer"] = encoder_plugin
            rest_request.serializer = encoder_plugin

        # retrieves the controller for the handlers method
        # and then uses it to retrieve its default parameters
        # after that uses the default parameters to extend the
        # parameters map of the handler tuple
        controller = type(handler_method) == types.MethodType and handler_method.im_self
        default_parameters = controller and\
            hasattr(controller, GET_DEFAULT_PARAMETERS_VALUE) and\
            controller.get_default_parameters() or {}
        colony.map_extend(parameters, default_parameters, copy_base_map = False)

        # handles the mvc request to the handler method (rest
        # request flow) note that the call is done using the safe
        # call method so that only the valid arguments are passed
        # to the handler method (pattern names validation)
        colony.call_safe(
            handler_method,
            rest_request,
            parameters = parameters,
            **pattern_names
        )

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
        # and in case it's not sets the default code (no error)
        is_set_status_code = rest_request_status_code and True or False
        not is_set_status_code and rest_request.set_status_code(DEFAULT_STATUS_CODE)

    def _update_matching_regex(self):
        """
        Updates the matching regex, this operation should
        update the internal structured so that any further
        requests should be handled according to the patterns
        defined in the internal structures.
        """

        # starts the matching regex value buffer
        matching_regex_buffer = colony.StringBuffer()

        # clears both the matching regex list and the associated
        # base indexes map (reset operation)
        self.matching_regex_list = []
        self.matching_regex_base_map.clear()

        # starts the various control values to be used in the
        # iteration that will create the matching regex
        index = 0
        current_base_index = 0
        is_first = True

        # iterates over all the patterns in the patterns list to
        # add then to the matching regex buffer and to calculate
        # their base indexes
        for pattern in self.patterns_list:
            # in case it's not the first iteration adds the
            #or operand to the matching regex value buffer
            if is_first: is_first = False
            else: matching_regex_buffer.write("|")

            # adds the group name part of the regex to the matching
            # regex value buffer
            matching_regex_buffer.write("(" + pattern + ")")

            # increments the index value, because one more pattern
            # was added to the matching regex buffer
            index += 1

            # in case the current index is in the limit of the python
            # regex compilation, must flush regex operation
            if not index % REGEX_COMPILATION_LIMIT == 0: continue

            # retrieves the matching regex value from the matching
            # regex value buffer compiles it and adds it to both
            # the matching regex list and base indexes map
            matching_regex_value = matching_regex_buffer.get_value()
            matching_regex = re.compile(matching_regex_value)
            self.matching_regex_list.append(matching_regex)
            self.matching_regex_base_map[matching_regex] = current_base_index

            # re-sets the current matching regex buffer value and
            # then updates the base index to the current index and
            # sets the is first flag
            matching_regex_buffer.reset()
            current_base_index = index
            is_first = True

        # retrieves the (matching) regex value from the matching
        # regex value buffer and in case is not valid returns
        # immediately no further processing
        matching_regex_value = matching_regex_buffer.get_value()
        if not matching_regex_value: return

        # compiles the matching regex value and adds it to
        # the matching regex list and base indexes map
        matching_regex = re.compile(matching_regex_value)
        self.matching_regex_list.append(matching_regex)
        self.matching_regex_base_map[matching_regex] = current_base_index

    def _update_communication_matching_regex(self):
        """
        Updates the communication matching regex, this
        operation should update the internal structured
        so that any further requests should be handled
        according to the patterns defined in the internal
        structures.
        """

        # starts the matching regex value buffer
        communication_matching_regex_buffer = colony.StringBuffer()

        # clears both the matching regex list and the associated
        # base indexes map (reset operation)
        self.communication_matching_regex_list = []
        self.communication_matching_regex_base_map.clear()

        # starts the various control values to be used in the
        # iteration that will create the matching regex
        index = 0
        current_base_index = 0
        is_first = True

        # iterates over all the patterns in the patterns list to
        # add then to the matching regex buffer and to calculate
        # their base indexes
        for pattern in self.communication_patterns_list:
            # in case it's not the first iteration adds the
            #or operand to the matching regex value buffer
            if is_first: is_first = False
            else: communication_matching_regex_buffer.write("|")

            # adds the group name part of the regex to the matching
            # regex value buffer
            communication_matching_regex_buffer.write("(" + pattern + ")")

            # increments the index value, because one more pattern
            # was added to the matching regex buffer
            index += 1

            # in case the current index is in the limit of the python
            # regex compilation, must flush regex operation
            if not index % REGEX_COMPILATION_LIMIT == 0: continue

            # retrieves the matching regex value from the matching
            # regex value buffer compiles it and adds it to both
            # the matching regex list and base indexes map
            communication_matching_regex_value = communication_matching_regex_buffer.get_value()
            communication_matching_regex = re.compile(communication_matching_regex_value)
            self.communication_matching_regex_list.append(communication_matching_regex)
            self.communication_matching_regex_base_map[communication_matching_regex] = current_base_index

            # re-sets the current matching regex buffer value and
            # then updates the base index to the current index and
            # sets the is first flag
            communication_matching_regex_buffer.reset()
            current_base_index = index
            is_first = True

        # retrieves the (matching) regex value from the matching
        # regex value buffer and in case is not valid returns
        # immediately no further processing
        communication_matching_regex_value = communication_matching_regex_buffer.get_value()
        if not communication_matching_regex_value: return

        # compiles the matching regex value and adds it to
        # the matching regex list and base indexes map
        communication_matching_regex = re.compile(communication_matching_regex_value)
        self.communication_matching_regex_list.append(communication_matching_regex)
        self.communication_matching_regex_base_map[communication_matching_regex] = current_base_index

    def _update_resource_matching_regex(self):
        """
        Updates the resource matching regex, this
        operation should update the internal structured
        so that any further requests should be handled
        according to the patterns defined in the internal
        structures.
        """

        # starts the matching regex value buffer
        resource_matching_regex_buffer = colony.StringBuffer()

        # clears both the matching regex list and the associated
        # base indexes map (reset operation)
        self.resource_matching_regex_list = []
        self.resource_matching_regex_base_map.clear()

        # starts the various control values to be used in the
        # iteration that will create the matching regex
        index = 0
        current_base_index = 0
        is_first = True

        # iterates over all the patterns in the patterns list to
        # add then to the matching regex buffer and to calculate
        # their base indexes
        for pattern in self.resource_patterns_list:
            # in case it's not the first iteration adds the
            #or operand to the matching regex value buffer
            if is_first: is_first = False
            else: resource_matching_regex_buffer.write("|")

            # adds the group name part of the regex to the matching
            # regex value buffer
            resource_matching_regex_buffer.write("(" + pattern + ")")

            # increments the index value, because one more pattern
            # was added to the matching regex buffer
            index += 1

            # in case the current index is in the limit of the python
            # regex compilation, must flush regex operation
            if not index % REGEX_COMPILATION_LIMIT == 0: continue

            # retrieves the matching regex value from the matching
            # regex value buffer compiles it and adds it to both
            # the matching regex list and base indexes map
            resource_matching_regex_value = resource_matching_regex_buffer.get_value()
            resource_matching_regex = re.compile(resource_matching_regex_value)
            self.resource_matching_regex_list.append(resource_matching_regex)
            self.resource_matching_regex_base_map[resource_matching_regex] = current_base_index

            # re-sets the current matching regex buffer value and
            # then updates the base index to the current index and
            # sets the is first flag
            resource_matching_regex_buffer.reset()
            current_base_index = index
            is_first = True

        # retrieves the (matching) regex value from the matching
        # regex value buffer and in case is not valid returns
        # immediately no further processing
        resource_matching_regex_value = resource_matching_regex_buffer.get_value()
        if not resource_matching_regex_value: return

        # compiles the matching regex value and adds it to
        # the matching regex list and base indexes map
        resource_matching_regex = re.compile(resource_matching_regex_value)
        self.resource_matching_regex_list.append(resource_matching_regex)
        self.resource_matching_regex_base_map[resource_matching_regex] = current_base_index

    def _normalize_patterns(self, patterns, extra = False):
        # creates the list that will hold the final version
        # of the patterns (after normalization process), this
        # value will contain various list defining the patterns
        _patterns = []

        # iterates over the complete set of provided patterns to
        # normalize each of them and then add the resulting value
        # to the list of "new" patterns
        for pattern in patterns:
            pattern = self._normalize_pattern(pattern, extra = extra)
            _patterns.append(pattern)

        # returns the final (normalized) list of patterns to the
        # caller method, this new patterns have been converted and
        # may contain some extra (meta) information
        return _patterns

    def _normalize_pattern(self, pattern, extra = False):
        # converts the provided pattern (expected to be a tuple) into
        # a list type so that it becomes mutable as required, then gets
        # the length of the pattern to be used ahead and extracts the
        # first element from it as the expression of the pattern, then
        # saves the "original" expression value in a private variable
        # as it's going to be used latter for naming to type resolution
        pattern = list(pattern)
        pattern_l = len(pattern)
        expression = pattern[0]
        _expression = expression

        # verifies if the start line and end line tokens are defined
        # in the expression and in case they're not adds then to the
        # current expression string as they are mandatory
        if not expression.startswith("^"): expression = "^" + expression
        if not expression.endswith("$"): expression = expression + "$"

        # runs the regex based replacement chain that should translate
        # the expression from a simplified domain into a regex based domain
        # that may be correctly compiled into the rest environment, then sets
        # the new expression value as the first element of the pattern
        expression = INT_REGEX.sub(r"(?P[\1>[\d]+)", expression)
        expression = REPLACE_REGEX.sub(r"(?P[\3>[\:\s\w-]+)", expression)
        expression = expression.replace("?P[", "?P<")
        pattern[0] = expression

        # in case no extra normalization operations are requested the method
        # should returns the "new" pattern list immediately to the caller method
        # as this is the specific behavior for such situations
        if not extra: return pattern

        # creates the names dictionary that will hold the association between
        # the name and the data type associated with that name for runtime
        # resolution of the argument values, also generates the structure that
        # will map the various variable names to the replacer expression
        names = dict()
        names_t = dict()

        # iterates over the complete set of matches for the replacer values
        # to be able to find the various names and then associate native
        # data types that will then be used for conversion at runtime for
        # the parameters of the handler function
        iterator = REPLACE_REGEX.finditer(_expression)
        for match in iterator:
            _type_s, type_t, name = match.groups()
            type_r = TYPES_R.get(type_t, str)
            if type_t: target = "<" + type_t + ":" + name + ">"
            else: target = "<" + name + ">"
            names[name] = type_r
            names_t[name] = target

        # in case any of the pattern components is missing defaults to the
        # default value for each of them so that the meta field (last one)
        # may be added as it is required by the specification
        if pattern_l < 3: pattern.append("get")
        if pattern_l < 4: pattern.append(None)
        if pattern_l < 5: pattern.append({})

        # creates the meta dictionary containing the values that will be used
        # for runtime based processing and then adds the value to the pattern
        meta = dict(names = names, names_t = names_t, original = _expression)
        pattern.append(meta)

        # returns the final list based pattern containing the complete set
        # of fields (including the meta one) to the caller method
        return pattern

    def __validate_match(self, rest_request, handler_attributes, resource_path):
        # unpacks the handler attributes, retrieving the handler
        # validation regex and the handler arguments
        validation_regex, arguments = handler_attributes

        # matches the resource path against the validation match
        # in case there is no (resource path) validation match
        # raises the runtime request exception
        validation_match = validation_regex.match(resource_path)
        if not validation_match:
            raise exceptions.RuntimeRequestException("invalid resource path validation match")

        # retrieves the length of the handler arguments, in order to be able
        # to conditionally validate the various parameters from it
        arguments_length = len(arguments)

        # retrieves the complete set of arguments that were provided
        # to be used as attributes by the handler
        method = arguments_length > 0 and arguments[0] or None
        operation_types = arguments_length > 1 and arguments[1] or ("get", "put", "post", "delete")
        encoders = arguments_length > 2 and arguments[2] or None
        contraints = arguments_length > 3 and arguments[3] or {}
        meta = arguments_length > 4 and arguments[4] or {}

        # casts both the operation types and the encoders as tuples
        # so that they remain compatible with the execution code
        operation_types = self.__cast_tuple(operation_types)
        encoders = self.__cast_tuple(encoders)

        # retrieves the request from the rest request to be used
        # in the retrieval of some attributes
        request = rest_request.get_request()

        # retrieves the various attributes associated with both the
        # request and the rest request that are going to be used in
        # the validation process
        operation_type_r = request.operation_type
        operation_type_r = operation_type_r.lower()
        encoder_name_r = rest_request.encoder_name

        # in case the request operation type does not exists in the
        # operation types, must returns with invalid value (validation
        # of operation type failed)
        if not operation_type_r in operation_types: return None

        # in case the encoders are defined and the request encoder name
        # does not exists in the encoders set must return with invalid
        # state (validation of encoder failed)
        if encoders and not encoder_name_r in encoders: return None

        # iterates over the complete set of constraints to be able to
        # ensure that they are valid for the current execution and if
        # the're not the return value is invalid (validation failed)
        for contraint_name, contraint_value in contraints.items():
            # retrieves the handler constraint value type
            contraint_value_t = type(contraint_value)

            # retrieves the attribute value base on the
            # handler constraint name
            attribute_value = rest_request.get_attribute(contraint_name)

            # tries to cast the attribute value using the constraint
            # type in case it fails returns in error
            try: attribute_value_c = contraint_value_t(attribute_value)
            except: return None

            # in case the attribute value (casted) is not equals
            # to the handler constraint value must return in error
            if attribute_value_c == contraint_value: return None

        # retrieves the (resource path) validation match groups map
        validation_match_groups_map = validation_match.groupdict()

        # creates the map containing the various parameters to be
        # "pushed" to the lower layer of the mvc stack
        parameters = dict(
            file_handler = self.mvc_file_handler,
            communication_handler = self.mvc_communication_handler,
            method = operation_type_r,
            encoder_name = encoder_name_r,
            pattern_names = validation_match_groups_map,
            meta = meta
        )

        # creates the handler tuple, containing both the method to
        # be used for handling and the parameters to be passed and
        # returns it to the caller method
        handler_tuple = (
            method,
            parameters
        )
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

        # in case the value is invalid, returns
        # the value immediately
        if value == None: return value

        # creates the tuple value from the value and returns
        # the value to the caller method
        tuple_value = type(value) == types.TupleType and value or (value,)
        return tuple_value
