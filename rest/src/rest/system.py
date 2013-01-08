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
import time
import heapq
import datetime
import threading

import colony.base.system
import colony.libs.quote_util
import colony.libs.string_buffer_util

import exceptions

REGEX_COMILATION_LIMIT = 99
""" The regex compilation limit """

HANDLER_BASE_FILENAME = "/dynamic/rest/"
""" The handler base filename """

HANDLER_EXTENSION = "py"
""" The handler extension """

HANDLER_FILENAME = "rest.py"
""" The handler filename """

LIST_METHODS_NAME = "system.listMethods"
""" The list methods name """

APACHE_CONTAINER = "apache"
""" The apache container """

HANDLER_NAME = "rest"
""" The handler name """

HANDLER_PORT = 80
""" The handler port """

SERVICES_SERVICE_NAME = "services"
""" The services service name """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

COOKIE_VALUE = "Cookie"
""" The cookie value """

SET_COOKIE_VALUE = "Set-Cookie"
""" The set cookie value """

SESSION_ID_VALUE = "session_id"
""" The session id value """

LANG_VALUE = "lang"
""" The lang value """

EXPIRES_VALUE = "expires"
""" The expires value """

PATH_VALUE = "path"
""" The path value """

DOMAIN_VALUE = "domain"
""" The domain value """

SECURE_VALUE = "secure"
""" The secure value """

LOCALHOST_VALUES = (
    "localhost",
    "127.0.0.1"
)
""" The localhost values """

HOST_VALUE = "Host"
""" The host value """

LOCATION_VALUE = "Location"
""" The location value """

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
""" The date format """

DEFAULT_EXPIRATION_DATE = "Thu, 01 Jan 1970 00:00:00 GMT"
""" The default expiration date """

DEFAULT_LANG_VALUE = "en"
""" The default lang value """

DEFAULT_EXPIRATION_DELTA_TIMESTAMP = 31536000
""" The default expiration delta timestamp """

DEFAULT_PATH = "/"
""" The default path """

DEFAULT_STATUS_CODE = 200
""" The default status code """

DEFAULT_TIMEOUT = 10800
""" The default timeout (three hours of life) """

DEFAULT_MAXIMUM_TIMEOUT = DEFAULT_TIMEOUT * 64
""" The default maximum timeout (sixty four
times the timeout value) """

DEFAULT_TOUCH_SECURE_DELTA = 360
""" The default time delta used to introduce a security
factor in the timestamp used in the touching of the
(modified) date """

class Rest(colony.base.system.System):
    """
    The rest (manager) class.
    """

    matching_regex_list = []
    """ The list of matching regex to be used in route matching """

    matching_regex_base_values_map = {}
    """ The map containing the base values for the various matching regex """

    rest_service_routes_map = {}
    """ The rest service routes map """

    plugin_id_plugin_map = {}
    """ The plugin id plugin map """

    regex_index_plugin_id_map = {}
    """ The regex index plugin id map """

    service_methods = []
    """ The service methods list """

    service_methods_map = {}
    """ The service methods map """

    rest_session_list = []
    """ The list used as priority queue for session cancellation """

    rest_session_map = {}
    """ The map associating the session id with the rest session """

    rest_session_lock = None
    """ The lock that controls the access to the critical sections in session information """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)
        self.matching_regex_list = []
        self.matching_regex_base_values_map = {}
        self.rest_service_routes_map = {}
        self.plugin_id_plugin_map = {}
        self.regex_index_plugin_id_map = {}
        self.service_methods = []
        self.service_methods_map = {}
        self.rest_session_list = []
        self.rest_session_map = {}
        self.rest_session_lock = threading.RLock()

    def get_handler_filename(self):
        """
        Retrieves the handler filename.

        @rtype: String
        @return: The handler filename.
        """

        return HANDLER_FILENAME

    def is_request_handler(self, request):
        """
        Retrieves if it's an handler for the given request.

        @type request: Request
        @param request: The request to be used in the test.
        @rtype: bool
        @return: If it's an handler for the given request.
        """

        # retrieves the request filename
        request_filename = request.uri

        # in case the handler base filename is in the start of the request filename
        if request_filename.find(HANDLER_BASE_FILENAME) == 0:
            return True
        else:
            return False

    def handle_request(self, request):
        """
        Handles the given request.

        @type request: Request
        @param request: The request to be handled.
        """

        # retrieves the rest encoder plugins
        rest_encoder_plugins = self.plugin.rest_encoder_plugins

        # retrieves the request filename
        request_filename = request.uri

        # retrieves the handler base filename length
        handler_base_filename_length = len(HANDLER_BASE_FILENAME)

        # retrieves the resource path
        resource_path = request_filename[handler_base_filename_length:]

        # splits the resource path
        resource_path_splitted = resource_path.split("/")

        # retrieves the rest resource name
        resource_name = resource_path_splitted[0]

        # retrieves the middle path name
        middle_path_name = resource_path_splitted[1:-1]

        # retrieves the last path name
        last_path_name = resource_path_splitted[-1]

        # splits the last path name
        last_path_name_splitted = last_path_name.rsplit(".", 1)

        # retrieves the last path name splitted length
        last_path_name_splitted_length = len(last_path_name_splitted)

        # sets the default last path initial extension
        last_path_initial_extension = None

        # in case there is an extension defined
        if last_path_name_splitted_length >= 2:
            # retrieves the last path initial name
            last_path_initial_name = last_path_name_splitted[0]

            # retrieves the last path extension
            last_path_initial_extension = last_path_name_splitted[1]
        # in case there is no extension defined
        elif last_path_name_splitted_length == 1:
            # retrieves the last path initial name
            last_path_initial_name, = last_path_name_splitted
        else:
            # raises a bad service request exception
            raise exceptions.InvalidPath("invalid last path name value size: " + str(last_path_name_splitted_length))

        # retrieves the encoder name
        encoder_name = last_path_initial_extension

        # constructs the rest path list
        path_list = middle_path_name + [last_path_initial_name]

        # updates the session list (garbage collection)
        self.update_session_list()

        # creates the rest request
        rest_request = RestRequest(self, request)

        try:
            # updates the rest request session
            # loading the appropriate session in
            # case it exists
            rest_request.update_session()
        except:
            # logs a debug message
            self.plugin.debug("Session is invalid no session loaded or updated")

        # "touches" the rest request updating it's
        # internal timing structures
        rest_request.touch()

        # sets the resource name in the rest request
        rest_request.set_resource_name(resource_name)

        # sets the path list in the rest request
        rest_request.set_path_list(path_list)

        # sets the encoder name in the rest request
        rest_request.set_encoder_name(encoder_name)

        # sets the rest encoder plugins in the rest request
        rest_request.set_rest_encoder_plugins(rest_encoder_plugins)

        # in case the request is meant to be handled by services
        if resource_name == SERVICES_SERVICE_NAME:
            # handles the request with the services request handler
            self.handle_rest_request_services(rest_request)

            # returns immediately
            return
        # otherwise it's a "general" request
        else:
            # iterates over all the matching regex in the matching regex list
            for matching_regex in self.matching_regex_list:
                # retrieves the resource path match
                resource_path_match = matching_regex.match(resource_path)

                # in case there is no valid resource path match, must
                # continue the loop to try to find one
                if not resource_path_match: continue

                # retrieves the base value for the matching regex
                base_value = self.matching_regex_base_values_map[matching_regex]

                # retrieves the index of the captured group
                group_index = resource_path_match.lastindex

                # calculates the rest service plugin index from the base value,
                # the group index and subtracts one value
                rest_service_plugin_index = base_value + group_index - 1

                # retrieves the plugin id from the rest service plugin index
                plugin_id = self.regex_index_plugin_id_map[rest_service_plugin_index]

                # retrieves the rest service plugin using the plugin id
                rest_service_plugin = self.plugin_id_plugin_map[plugin_id]

                # handles the rest request to the rest service plugin
                rest_service_plugin.handle_rest_request(rest_request)

                # returns immediately
                return

        # raises the rest request not handled exception
        raise exceptions.RestRequestNotHandled("no rest service plugin could handle the request")

    def handle_rest_request_services(self, rest_request):
        """
        Handles the rest request meant for services.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled.
        """

        # retrieves the request
        request = rest_request.get_request()

        # retrieves the rest path list
        path_list = rest_request.get_path_list()

        # retrieves the rest encoder name
        encoder_name = rest_request.get_encoder_name()

        # creates the real method name, joining the rest path list
        method_name = ".".join(path_list)

        # in case there is a list methods request
        if method_name == LIST_METHODS_NAME:
            result = self.service_methods
        # tries to call the requested method
        elif method_name in self.service_methods_map:
            # retrieves the rpc method
            rpc_method = self.service_methods_map[method_name]

            # creates the arguments map
            arguments_map = {}

            # iterates over all the variable names in the function
            # variables
            for variable_name in rpc_method.func_code.co_varnames:
                if variable_name in request.attributes_map:
                    # retrieves the variable value from the attributes map
                    variable_value = request.attributes_map[variable_name]

                    # unquotes the variable value
                    variable_value = colony.libs.quote_util.unquote_plus(variable_value)

                    # sets the variable value in the arguments map
                    arguments_map[variable_name] = variable_value

            # calls the rpc method with the arguments map
            result = rpc_method(**arguments_map)
        # in case the method name is not valid
        else:
            # raises the invalid method exception
            raise exceptions.InvalidMethod("the method name " + method_name + " is not valid")

        # serializes the result for the given encoder name retrieving the content type
        # and the translated result
        content_type, result_translated = self.translate_result(result, encoder_name)

        # sets the default status code for the rest request
        rest_request.set_status_code(DEFAULT_STATUS_CODE)

        # sets the content type for the rest request
        rest_request.set_content_type(content_type)

        # sets the result for the rest request
        rest_request.set_result_translated(result_translated)

        # flushes the rest request
        rest_request.flush()

    def is_active(self):
        """
        Tests if the service is active.

        @rtype: bool
        @return: If the service is active.
        """

        # retrieves the plugin manager
        manager = self.plugin.manager

        # in case the current container is apache
        if manager.container == APACHE_CONTAINER:
            return True
        else:
            return False

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        # returns the handler name
        return HANDLER_NAME

    def get_handler_port(self):
        """
        Retrieves the handler port.

        @rtype: int
        @return: The handler port.
        """

        # returns the handler port
        return HANDLER_PORT

    def get_handler_properties(self):
        """
        Retrieves the handler properties.

        @rtype: Dictionary
        @return: The handler properties.
        """

        return {
            "handler_base_filename" : HANDLER_BASE_FILENAME,
            "handler_extension" : HANDLER_EXTENSION
        }

    def load_rest_service_plugin(self, rest_service_plugin):
        """
        Loads the rest service plugin, in the rest manager.

        @type rest_service_plugin: Plugin
        @param rest_service_plugin: The rest service plugin to be loaded.
        """

        # retrieves the rest service plugin id
        rest_service_plugin_id = rest_service_plugin.id

        # retrieves the rest service plugin routes
        routes_list = rest_service_plugin.get_routes()

        # initializes the rest service plugin id routes list
        self.rest_service_routes_map[rest_service_plugin_id] = routes_list

        # sets the rest service plugin in the plugin id plugin map
        self.plugin_id_plugin_map[rest_service_plugin_id] = rest_service_plugin

        # updates the matching regex
        self._update_matching_regex()

    def unload_rest_service_plugin(self, rest_service_plugin):
        """
        Unloads the rest service plugin, from the rest manager.

        @type rest_service_plugin: Plugin
        @param rest_service_plugin: The rest service plugin to be unloaded.
        """

        # retrieves the rest service plugin id
        rest_service_plugin_id = rest_service_plugin.id

        # deletes the route list for the plugin
        del self.rest_service_routes_map[rest_service_plugin_id]

        # deletes the rest service plugin from the plugin id plugin map
        del self.plugin_id_plugin_map[rest_service_plugin_id]

        # updates the matching regex
        self._update_matching_regex()

    def update_service_methods(self, updated_rpc_service_plugin = None):
        if updated_rpc_service_plugin:
            updated_rpc_service_plugins = [
                updated_rpc_service_plugin
            ]
        else:
            # clears the service methods list
            self.service_methods = []

            # clears the service map
            self.service_methods_map = {}

            # retrieves the updated rpc service plugins
            updated_rpc_service_plugins = self.plugin.rpc_service_plugins

        for rpc_service_plugin in updated_rpc_service_plugins:
            # retrieves all the method names for the current rpc service
            available_rpc_methods = rpc_service_plugin.get_available_rpc_methods()

            # retrieves all the method alias for the current rpc service
            available_rpc_methods_alias = rpc_service_plugin.get_rpc_methods_alias()

            # in case the plugin contains the rpc method metadata
            if rpc_service_plugin.contains_metadata_key("rpc_method"):
                # retrieves the metadata values for the rpc method
                metadata_values = rpc_service_plugin.get_metadata_key("rpc_method")

                # iterates over all the metadata values
                for metadata_value in metadata_values:
                    # retrieves the method name of the rpc method
                    method_name = metadata_value["method_name"]

                    # retrieves the alias for the rpc method
                    alias = metadata_value["alias"]

                    # retrieves the method for the rpc method from the plugin instance
                    method = getattr(rpc_service_plugin, method_name)

                    # adds the method to the list of available rpc methods
                    available_rpc_methods.append(method)

                    # adds the alias to the list of available rpc methods alias
                    available_rpc_methods_alias[method] = alias

            # retrieves the list of all the available rpc methods
            available_rpc_methods_string = [value.__name__ for value in available_rpc_methods]

            # iterates over all the rpc method alias keys
            for available_rpc_method_alias_key in available_rpc_methods_alias:
                available_rpc_methods_alias_string = available_rpc_methods_alias[available_rpc_method_alias_key]
                available_rpc_methods_string.extend(available_rpc_methods_alias_string)

            # extends the service methods list with the available rpc methods string
            self.service_methods.extend(available_rpc_methods_string)

            # retrieves the service id
            service_id = rpc_service_plugin.get_service_id()

            # retrieves the list of service alias
            service_alias = rpc_service_plugin.get_service_alias()

            # creates a list with all the possible service names
            service_names = [service_id] + service_alias

            # iterates over all the possible service names
            for service_name in service_names:
                for available_rpc_method_string in available_rpc_methods_string:
                    composite_available_rpc_method_string = service_name + "." + available_rpc_method_string
                    self.service_methods.append(composite_available_rpc_method_string)

            # iterates over all the available rpc methods to generate the service methods map
            for available_rpc_method in available_rpc_methods:
                # creates the service method names list
                service_method_names = []

                # creates the service method basic names list
                service_method_basic_names = []

                # adds the available rpc method to the service method names list
                service_method_names.append(available_rpc_method.__name__)

                # adds the available rpc method to the service basic method names list
                service_method_basic_names.append(available_rpc_method.__name__)

                # retrieves all the alias to the current service methods
                alias_service_method_names = [value for value in available_rpc_methods_alias[available_rpc_method]]

                # adds the available rpc method alias to the service method names list
                service_method_names.extend(alias_service_method_names)

                # adds the available rpc method alias to the service basic method names list
                service_method_basic_names.extend(alias_service_method_names)

                # iterates over all the service names
                for service_name in service_names:
                    for service_method_basic_name in service_method_basic_names:
                        service_method_complex_name = service_name + "." + service_method_basic_name
                        service_method_names.append(service_method_complex_name)

                # iterates over all the service method names
                for service_method_name in service_method_names:
                    # adds the available rpc method to the map with the service method name as key
                    self.service_methods_map[service_method_name] = available_rpc_method

    def translate_request(self, data):
        """
        Translates the given encoded data data into a python request.

        @type data: String
        @param data: The encoded data to be translated into a python request.
        @rtype: Any
        @return: The translated python request.
        """

        # returns the translated request
        return data

    def translate_result(self, result, encoder_name = None):
        """
        Translates the given python result into the encoding defined.

        @type result: Any
        @param result: The python result to be translated into encoded data.
        @type method_name: String
        @param method_name: The name of the encoder to be used.
        @rtype: Tuple
        @return: The content type and the translated data.
        """

        # retrieves the rest encoder plugins
        rest_encoder_plugins = self.plugin.rest_encoder_plugins

        # in case the encoder name is defined
        if encoder_name:
            # iterates over all the rest encoder plugins
            for rest_encoder_plugin in rest_encoder_plugins:
                if rest_encoder_plugin.get_encoder_name() == encoder_name:
                    # retrieves the content type from the rest encoder plugin
                    content_type = rest_encoder_plugin.get_content_type()

                    # calls the the encoder plugin to encode the result
                    result_encoded = rest_encoder_plugin.encode_value(result)

                    # returns the content type and the encoded result
                    return content_type, result_encoded

            # raises the invalid encoder exception
            raise exceptions.InvalidEncoder("the " + encoder_name + " encoder is invalid")
        else:
            # sets the default content type
            content_type = "text/plain"

            # retrieves the result encoded with the default encoder
            result_encoded = str(result)

            # returns the content type and the encoded result
            return content_type, result_encoded

    def add_session(self, session):
        """
        Adds a session to the sessions map.

        @type session: RestSession
        @param session: The session to be added to the map.
        """

        # retrieves the session id and the expire
        # time to be able to create the session tuple
        session_id = session.get_session_id()
        session_expire_time = session.get_expire_time()

        # creates the session tuple form the session
        # expire time and id (to be used for session cancellation)
        session_tuple = (session_expire_time, session_id)

        # pushes the session tuple to the rest session list (heap)
        heapq.heappush(self.rest_session_list, session_tuple)

        # sets the session in the rest session map
        self.rest_session_map[session_id] = session

    def remove_session(self, session):
        """
        Removes a session from the sessions map.

        @type session: RestSession
        @param session: The session to be removed from the map.
        """

        # retrieves the session id
        session_id = session.get_session_id()

        # in case the session  id exist in the rest
        # session map
        if session_id in self.rest_session_map:
            # unsets the session from the rest session map
            del self.rest_session_map[session_id]

    def update_session(self, session):
        """
        Updates a session instance in the current rest request
        this updates the session list with the new values.

        @type session: RestSession
        @param session: The session to be updated.
        """

        # retrieves the session id and the expire
        # time to be able to create the session tuple
        session_id = session.get_session_id()
        session_expire_time = session.get_expire_time()

        # creates the session tuple form the session
        # expire time and id (to be used for session cancellation)
        session_tuple = (session_expire_time, session_id)

        # pushes the session tuple to the rest session list (heap)
        heapq.heappush(self.rest_session_list, session_tuple)

    def clear_sessions(self):
        """
        Removes all the sessions from the current internal
        structures, this is equivalent to the invalidation
        of all the sessions in the rest manager.
        """

        # removes the complete set of session timeout tuples
        # so that no more session invalidation occurs
        self.rest_session_list = []

        # clears the rest session map, removing all the
        # registered session from it
        self.rest_session_map.clear()

    def get_session(self, session_id):
        """
        Retrieves the session with the given session id
        from the sessions map.

        @type session_id: String
        @param session_id: The id of the session to retrieve.
        """

        return self.rest_session_map.get(session_id, None)

    def update_session_list(self):
        """
        Updates the session list, checking for old
        session and stopping them (garbage collection).
        """

        # retrieves the current time
        current_time = time.time()

        # iterates continuously
        while True:
            # in case the rest session list
            # is not valid (empty), breaks the
            # loop since there is nothing to be done
            if not self.rest_session_list: break

            # acquires the rest session lock
            self.rest_session_lock.acquire()

            try:
                # retrieves the first session information
                # form the rest session list (ordered list)
                session_expire_time, session_id = self.rest_session_list[0]

                # in case the session expire time is still in the
                # future, breaks the loop because there are no
                # more sessions to be removed (ordered list)
                if session_expire_time > current_time: break

                # retrieves the session for the current session id and verifies that it
                # is valid (exists in the current internal structures) in case it does
                # not, continues the loop to continue session invalidation
                session = self.get_session(session_id)
                if session == None:
                    # pops the last element from the res
                    # session list (heap) and continues the loop
                    heapq.heappop(self.rest_session_list)
                    continue

                # retrieves the expire time for the current session
                session_expire_time_current = session.get_expire_time()

                # in case the session expire time for current time
                # is the same (no touch in between) the session should
                # be removed (garbage collection)
                if session_expire_time_current == session_expire_time:
                    # removes the session from the rest manager structures
                    self.remove_session(session)
                # otherwise there has been a new session expire time
                # update (no cancellation should be made)
                else:
                    # creates the session tuple form the session
                    # expire (current) time and id (to be used for
                    # session cancellation)
                    session_tuple = (session_expire_time_current, session_id)

                    # pushes the session tuple to the rest session list (heap)
                    heapq.heappush(self.rest_session_list, session_tuple)

                # pops the last element from the res
                # session list (heap)
                heapq.heappop(self.rest_session_list)
            finally:
                # releases the rest session lock
                self.rest_session_lock.release()

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

        # sets the is first plugin flag
        is_first_plugin = True

        # starts the index value
        index = 0

        # starts the current base value
        current_base_value = 0

        # iterates over all the items in the rest service routes map
        for rest_service_plugin_id, routes_list in self.rest_service_routes_map.items():
            # in case it's the first plugin
            if is_first_plugin:
                # unsets the is first plugin flag
                is_first_plugin = False
            else:
                # adds the or operand to the matching regex value buffer
                matching_regex_value_buffer.write("|")

            # adds the group part of the regex to the matching regex value buffer
            matching_regex_value_buffer.write("(")

            # sets the is first flag
            is_first = True

            # iterates over all the routes in the routes list
            for route in routes_list:
                # in case it's the first route
                if is_first:
                    # unsets the is first flag
                    is_first = False
                else:
                    # adds the or operand to the matching regex value buffer
                    matching_regex_value_buffer.write("|")

                # adds the route to the matching regex value buffer
                matching_regex_value_buffer.write(route)

            # closes the matching regex value group
            matching_regex_value_buffer.write(")")

            # sets the rest service plugin id in the regex index
            # plugin id map
            self.regex_index_plugin_id_map[index] = rest_service_plugin_id

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

class RestRequest:
    """
    The rest request class.
    """

    rest = None
    """ The rest """

    request = None
    """ The associated request """

    session = None
    """ The associated session """

    resource_name = None
    """ The resource name """

    path_list = None
    """ The path list """

    encoder_name = None
    """ The encoder name """

    content_type = None
    """ The content type """

    result_translated = None
    """ The translated result """

    rest_encoder_plugins = []
    """ The rest encoder plugins """

    rest_encoder_plugins_map = []
    """ The rest encoder plugins map """

    parameters_map = {}
    """ The parameters map, used to store temporary data """

    _generation_time = None
    """ The original time of generation of the rest request
    measured as seconds since the epoch """

    _generation_clock = None
    """ The original time of generation of the rest request
    measured as seconds since the start of the system process """

    def __init__(self, rest, request):
        """
        Constructor of the class.

        @type rest: MainRestManager
        @param rest: The rest.
        @type request: Request
        @param request: The associated request.
        """

        self.rest = rest
        self.request = request

        self.rest_encoder_plugins = []
        self.rest_encoder_plugins_map = {}
        self.parameters_map = {}

        # updates the generation time value with the current
        # time (useful for generation time) also updates the
        # clock value (useful for benchmarking)
        self._generation_time = time.time()
        self._generation_clock = time.clock()

    def start_session(self, force = False, session_id = None, timeout = DEFAULT_TIMEOUT, maximum_timeout = DEFAULT_MAXIMUM_TIMEOUT):
        """
        Starts the session for the given session id,
        or generates a new session id.
        In case the session id is not provided a new
        session id is generated in a secure manner.

        @type force: bool
        @param force: If the session should be created if a session
        is already selected.
        @type session_id: String
        @param session_id: The session id to be used.
        @type timeout: float
        @param timeout: The timeout to be used in the session.
        @type maximum_timeout: float
        @param maximum_timeout: The maximum timeout to be used in the session.
        """

        # in case a session exists and force flag is disabled
        # avoids creation (provides duplicate creation blocking)
        # must return immediately
        if self.session and not force: return

        # in case no session id is defined
        if not session_id:
            # retrieves the random plugin
            random_plugin = self.rest.plugin.random_plugin

            # creates a new random session id
            session_id = random_plugin.generate_random_md5_string()

        # creates a new rest session and sets
        # it as the current session (uses the timeout information)
        self.session = RestSession(
            session_id,
            timeout = timeout,
            maximum_timeout = maximum_timeout
        )

        # retrieves the host name value
        domain = self._get_domain()

        # checks if the current request is secure, in case
        # it is the session start must be encrypted and only
        # used in secure channels (the cookie must be set accordingly)
        is_secure = self.request.is_secure()

        # starts the session with the defined domain
        self.session.start(domain, secure = is_secure)

        # adds the session to the rest
        self.rest.add_session(self.session)

    def stop_session(self):
        """
        Stops the current session.
        """

        # in case no session is defined, creates
        # a new empty session
        if not self.session: self.session = RestSession()

        # retrieves the host name value
        domain = self._get_domain()

        # stops the session with the defined domain
        self.session.stop(domain)

        # removes the session from the rest
        self.rest.remove_session(self.session)

    def clear_sessions(self):
        """
        Removes all the sessions from the rest manager internal
        structures, this is equivalent to the invalidation
        of all the sessions in the rest manager.
        """

        # clears the session related structures, removing all
        # the sessions from the rest manager and then invalidate
        # the current session
        self.rest.clear_sessions()
        self.session = None

    def update_session(self):
        """
        Updates the current session.
        This method tries to "load" the session associated
        with the current request.
        The updating of the session will be archived using
        a set of predefined techniques.
        """

        # updates the session using the attribute method
        # this strategy goes through the especially designated
        # session id attribute to load the session
        self._update_session_attribute()

        # updates the session using the cookie method, this
        # strategy loads the cookie from the session id attribute
        # defined in the cookie header
        self._update_session_cookie()

    def touch(self):
        """
        Touches the internal session, updating the expire
        time with the timeout value.
        """

        # in case the session is defined updates the
        # expire time according to the timeout and
        # the current time
        self.session and self.session.update_expire_time()

    def touch_date(self, secure_delta = DEFAULT_TOUCH_SECURE_DELTA):
        """
        Touches the last modified timestamp value, setting it
        to the current date information including a "small"
        security oriented delta value to avoid browser problems.

        @type secure_delta: float
        @param secure_delta: The delta value to be removed from the
        current time value to avoid browser problems
        """

        # updates the last modified timestamp value with the current
        # time value reduced by the secure delta value
        self.request.last_modified_timestamp = time.time() - secure_delta

    def update_timeout(self, timeout, maximum_timeout = None):
        """
        Updates the session timeout (and maximum timeout) values
        so that the session may be extended or shortened.

        This method provides extra security tools for session
        timing control.

        @type timeout: float
        @param timeout: The timeout value to be used as the "new"
        timeout of the session.
        @type maximum_timeout: float
        @param maximum_timeout: The maximum timeout value to be
        used as the "new" maximum timeout of the session.
        """

        # in case no session is defined must return immediately
        # not possible to change timeout in case no session is
        # currently defined
        if not self.session: return

        # sets the maximum timeout value in case is not currently
        # set as the triple value of the timeout
        maximum_timeout = maximum_timeout or timeout * 3

        # updates the session timeout and maximum timeout values
        # and then generates the expire time from the current
        # time and the given timeout and maximum timeout
        self.session.timeout = timeout
        self.session.maximum_timeout = maximum_timeout
        self.session._generate_expire_time(timeout, maximum_timeout)

        # updates the session in the rest request, provides
        # the infra-structure to update expire structures
        self.rest.update_session(self.session)

    def read(self):
        """
        Reads the contents of the request associated with this
        rest request, this operation may take some performance
        impact as the complete data is stored in memory.

        @rtype: String
        @return: The complete data contents of the request associated
        with the current rest request.
        """

        return self.request.read()

    def write(self, data):
        """
        Writes the provided chunk data to the underlying request
        structures. The data is not immediately flushed to the
        client side.

        @type data: String
        @param data: The data to be written to the underlying
        request structures.
        """

        return self.request.write(data)

    def process(self):
        """
        Processes the underlying request object, this should
        start the flushing of the data to the client peer.

        Use this method with care as it may corrupt the request
        life-cycle and create unexpected issues in the server.
        """

        # retrieves the request elements, the service handler and the
        # service connection to be used in the processing then uses
        # them to process the request (send request to client)
        service = self.request.get_service()
        service_connection = self.request.get_service_connection()
        service.process_request(self.request, service_connection)

    def parse_post(self):
        """
        Parses the post message using the default,
        parses and the default encoding.
        """

        # parses the post attributes
        self.request.parse_post_attributes()

    def is_get(self):
        """
        Tests the request to check if it is of type
        get method.

        @rtype: bool
        @return: If the request method is of type get.
        """

        # in case the operation is of type get must return
        # valid otherwise returns false (default validation)
        if self.request.operation_type == GET_METHOD_VALUE: return True
        else: return False

    def is_post(self):
        """
        Tests the request to check if it is of type
        post method.

        @rtype: bool
        @return: If the request method is of type post.
        """

        # in case the operation is of type post must return
        # valid otherwise returns false (default validation)
        if self.request.operation_type == POST_METHOD_VALUE: return True
        else: return False

    def is_debug(self, minimum_level = 6):
        """
        In case the request should be set in debug mode.
        Maximum verbosity, in actions like exception handling.

        @type minimum_level: int
        @param minimum_level: The minimum level to be used for verbosity.
        """

        # retrieves the rest plugin
        rest_plugin = self.rest.plugin

        # retrieves the resources manager plugin
        resources_manager_plugin = rest_plugin.resources_manager_plugin

        # retrieves the debug level
        debug_level = resources_manager_plugin.get_resource("system.debug.level")

        # in case the debug level does meet the required
        # level returns valid otherwise return not valid
        if debug_level and debug_level.data >= minimum_level: return True
        else: return False

    def flush(self):
        """
        Flushes the rest request buffer, this operation should
        generate all the required information (partial generation)
        and send it to the underlying request object.

        This is a potentially costy operation so it should be called
        with care (and not very often).
        """

        # in case there is a session available
        if self.session:
            # retrieves the session cookie
            session_cookie = self.session.get_cookie()

            # in case there is a session cookie and the
            # the request is set to allow setting of cookies
            # (provides extra security on single domain access)
            if session_cookie and self.request.allow_cookies:
                # serializes the session cookie into the appropriate
                # representation to be set
                serialized_session_cookie = session_cookie.serialize()

                # sets the session id in the cookie and then invalidates
                # it so that no extra cookies are set
                self.request.append_header(SET_COOKIE_VALUE, serialized_session_cookie)
                self.session.set_cookie(None)

        # sets the content type for the request, this should
        # be able to asset the correct content type in the
        # target request object
        self.request.content_type = self.content_type

        # writes the result translated and flushes the
        # request, sending the output to the client
        self.request.write(self.result_translated)
        self.request.flush()

    def redirect(self, target_path, status_code = 302, quote = True, attributes_map = None):
        """
        Redirects the request logically, so it
        becomes readable as a new resource.

        An optional attributes map may be used to use
        url parameters in the redirect.

        @type target_path: String
        @param target_path: The target path of the redirection.
        @type status_code: int
        @param status_code: The status code to be used.
        @type quote: bool
        @param quote: If the target path should be quoted.
        @type attributes_map: Dictionary
        @param attributes_map: Map containing the series of
        attributes to be sent over the target path in the
        redirect url.
        """

        # quotes the target path
        target_path_quoted = quote and colony.libs.quote_util.quote(target_path, "/") or target_path

        # creates the final target path using the attributes
        # map in case they are present (by appending them to
        # the target path) otherwise (in case no attributes map
        # is present) the target path is used
        target_path_quoted = attributes_map and target_path_quoted + "?" + colony.libs.quote_util.url_encode(attributes_map) or target_path_quoted

        # sets the status code
        self.request.status_code = status_code

        # sets the location header (using the quoted target path)
        self.request.set_header(LOCATION_VALUE, target_path_quoted)

    def execute_background(self, callable, retries = 0, timeout = 0.0, timestamp = None):
        """
        Executes the given callable object in a background
        thread.
        This method is useful for avoid blocking the request
        handling method in non critic tasks.

        @type callable: Callable
        @param callable: The callable to be called in background.
        @type retries: int
        @param retries: The number of times to retry executing the
        callable in case exception is raised.
        @type timeout: float
        @param timeout: The time to be set in between calls of the
        callable, used together with the retry value.
        @type timestamp: float
        @param timestamp: The unix second based timestamp for the
        first execution of the callable.
        """

        self.request.execute_background(
            callable,
            retries = retries,
            timeout = timeout,
            timestamp = timestamp
        )

    def allow_cookies(self):
        """
        Allows the setting of cookies through the typical http
        header technique.

        This technique may prove to be not required for simple
        non interactive user agents.
        """

        self.request.allow_cookies()

    def deny_cookies(self):
        """
        Denies the setting of cookies through the typical http
        header technique.

        This technique may prove to be not required for simple
        non interactive user agents.
        """

        self.request.deny_cookies()

    def get_header(self, header_name):
        """
        Retrieves an header value of the request,
        or none if no header is defined for the given
        header name.

        @type header_name: String
        @param header_name: The name of the header to be retrieved.
        @rtype: Object
        @return: The value of the request header.
        """

        return self.request.get_header(header_name)

    def set_header(self, header_name, header_value):
        """
        Set a response header value on the request.

        @type header_name: String
        @param header_name: The name of the header to be set.
        @type header_value: Object
        @param header_value: The value of the header to be sent
        in the response.
        """

        self.request.set_header(header_name, header_value)

    def get_attributes_list(self):
        """
        Retrieves the list of available attribute names.

        @rtype: List
        @return: The list of available attribute names.
        """

        return self.request.get_attributes_list()

    def get_attribute(self, attribute_name):
        """
        Retrieves the attribute for the given attribute name.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to retrieve.
        @rtype: Object
        @return: The value of the retrieved attribute.
        """

        return self.request.get_attribute(attribute_name)

    def set_attribute(self, attribute_name, attribute_value):
        """
        Sets the attribute with the given name with the given
        value.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to set.
        @type attribute_value: Object
        @param attribute_value: The value to set the attribute.
        """

        self.request.set_attribute(attribute_name, attribute_value)

    def get_parameter(self, parameter_name):
        """
        Retrieves the parameter for the given parameter name.

        This parameter should be used to compute temporary
        data (not for long term storage).

        @type parameter_name: String
        @param parameter_name: The name of the parameter to retrieve.
        @rtype: Object
        @return: The value of the retrieved parameter.
        """

        return self.parameters_map.get(parameter_name, None)

    def set_parameter(self, parameter_name, parameter_value):
        """
        Sets the parameter with the given name with the given
        value.

        This parameter should be used to compute temporary
        data (not for long term storage).

        @type parameter_name: String
        @param parameter_name: The name of the parameter to set.
        @type parameter_value: Object
        @param parameter_value: The value to set the parameter.
        """

        self.parameters_map[parameter_name] = parameter_value

    def get_session_attributes_map(self):
        """
        Retrieves the session attributes map.
        In case the session is not defined the default (empty)
        attributes map is returned.

        @rtype: Dictionary
        @return: The session attributes map.
        """

        # retrieves the session attributes map in case the session
        # is defined otherwise retrieves the default map
        session_attributes_map = self.session and self.session.attributes_map or {}

        # returns the session attributes map
        return session_attributes_map

    def get_plugin_manager(self):
        """
        Retrieves the plugin manager for the context
        of the rest request.

        @rtype: PluginManager
        @return: The plugin manager for the context
        of the rest request.
        """

        # retrieves the rest plugin and then
        # uses it to retrieve the plugin manager
        rest_plugin = self.rest.plugin
        plugin_manager = rest_plugin.manager

        # retrieves the plugin manager for the current context
        return plugin_manager

    def get_request(self):
        """
        Retrieves the associated request.

        @rtype: Request
        @return: The associated request.
        """

        return self.request

    def set_request(self, request):
        """
        Sets the associated request.

        @type request: Request
        @param request: The associated request.
        """

        self.request = request

    def get_session(self, block = True):
        """
        Retrieves the associated session.

        @type block: bool
        @param block: If the lock should be
        used while accessing the session.
        @rtype: RestSession
        @return: The associated session.
        """

        # in case the session is not set or the
        # block (lock) flag is not set the
        # session may be returned immediately
        if not self.session or not block:
            # returns the session immediately,
            # no need to run through blocking
            return self.session

        # locks the current session to avoid
        # any erroneous modification
        self.session.lock()

        try:
            # saves the current session into
            # a local variable for "safe" return
            session = self.session
        finally:
            # releases the session lock allowing
            # usage by other thread
            self.session.release()

        # returns the "just" retrieved session
        # in a safe manner (run through lock)
        return session

    def set_session(self, session):
        """
        Sets the associated session.

        @type session: RestSession
        @param session: The associated session.
        """

        self.session = session

    def lock_session(self):
        """
        Locks the session so that any subsequent access to
        the underlying logic will block the call.
        """

        # in case no session is defined the control
        # returns immediately to the caller
        if not self.session: return

        # runs the lock operation on the session object
        # blocking any future accesses to the session
        self.session.lock()

    def release_session(self):
        """
        Releases the lock for the access to the session, any
        subsequent access to the session will be "allowed".
        """

        # in case no session is defined the control
        # returns immediately to the caller
        if not self.session: return

        # runs the release operation on the session object
        # allowing any future accesses to the session
        self.session.release()

    def reset_session(self):
        """
        Resets the session present in the current rest request,
        to reset the session is to unset it from the rest request.

        This method is useful for situation where a new session
        context is required or one is meant to be created always.
        """

        # "saves" the session into a temporary
        # attribute so that the session may
        # be removed from the current request
        session = self.session

        # locks the current session to avoid
        # any erroneous modification
        session.lock()

        try:
            # resets the session in the current
            # rest request (removes it from request)
            self.session = None
        finally:
            # releases the session lock allowing
            # usage by other thread
            session.release()

    def get_type(self):
        """
        Retrieves the content type for the current rest request
        using the associated header and processing it.

        @rtype: String
        @return: The content type value (base value) for the
        current request.
        """

        # retrieves the content type header from the current rest request
        # the treats it in case it's a valid content type and returns it
        # to the caller method
        content_type = self.get_header("Content-Type")
        content_type = content_type and content_type.split(";")[0].strip() or None
        return content_type

    def get_resource_name(self):
        """
        Retrieves the resource name.

        @rtype: String
        @return: The resource name.
        """

        return self.resource_name

    def set_resource_name(self, resource_name):
        """
        Sets the resource name.

        @type resource_name: String
        @param resource_name: The resource name.
        """

        self.resource_name = resource_name

    def get_path_list(self):
        """
        Retrieves the path list.

        @rtype: List
        @return: The path list.
        """

        return self.path_list

    def set_path_list(self, path_list):
        """
        Sets the path list.

        @type path_list: String
        @param path_list: The path list.
        """

        self.path_list = path_list

    def get_encoder_name(self):
        """
        Retrieves the encoder name.

        @rtype: String
        @return: The encoder name.
        """

        return self.encoder_name

    def set_encoder_name(self, encoder_name):
        """
        Sets the encoder name.

        @type encoder_name: String
        @param encoder_name: The encoder name.
        """

        self.encoder_name = encoder_name

    def get_content_type(self):
        """
        Retrieves the content type.

        @rtype: String
        @return: The content type.
        """

        return self.content_type

    def set_content_type(self, content_type, flush = False):
        """
        Sets the content type, in case the flush
        flag is set the content type is immediately
        set on the current target request.

        @type content_type: String
        @param content_type: The content type.
        @type flush: bool
        @param flush: If the content type should be
        immediately set on the target request object
        (underlying layer of abstraction).
        """

        self.content_type = content_type
        if flush: self.request.content_type = content_type

    def get_result_translated(self):
        """
        Retrieves the result translated.

        @rtype: String
        @return: The result translated.
        """

        return self.result_translated

    def set_result_translated(self, result_translated):
        """
        Sets the result translated.

        @type result_translated: String
        @param result_translated: The result translated.
        """

        self.result_translated = result_translated

    def get_rest_encoder_plugins(self):
        """
        Retrieves the rest encoder plugins.

        @rtype: List
        @return: The rest encoder plugins.
        """

        return self.rest_encoder_plugins

    def set_rest_encoder_plugins(self, rest_encoder_plugins):
        """
        Sets the rest encoder plugins.

        @type rest_encoder_plugins: List
        @param rest_encoder_plugins: The rest encoder plugins.
        """

        self.rest_encoder_plugins = rest_encoder_plugins

    def get_rest_encoder_plugins_map(self):
        """
        Retrieves the rest encoder plugins map.

        @rtype: Dictionary
        @return: The rest encoder plugins map.
        """

        return self.set_rest_encoder_plugins_map

    def set_rest_encoder_plugins_map(self, set_rest_encoder_plugins_map):
        """
        Sets the rest encoder plugins.

        @type set_rest_encoder_plugins_map: Dictionary
        @param set_rest_encoder_plugins_map: The rest encoder plugins map.
        """

        self.set_rest_encoder_plugins_map = set_rest_encoder_plugins_map

    def get_status_code(self):
        """
        Retrieves the status code.

        @rtype: int
        @return: The status code.
        """

        return self.request.status_code

    def set_status_code(self, status_code):
        """
        Sets the status code.

        @type status_code: int
        @param status_code: The status code.
        """

        self.request.status_code = status_code

    def set_delayed(self, value):
        """
        Sets the request as delayed, this should avoid automatic
        processing of the request (response sending).

        If the delayed mode is set an additional call to the
        process method is required to flush the data to the
        client side.

        @type value: bool
        @param value: The boolean value for the setting of
        the delayed mode flag.
        """

        self.request.delayed = value

    def get_service(self):
        """
        Retrieves the reference to the service responsible for
        the handling of the current request (owner).

        @rtype: Service
        @return: The service responsible for the handling of
        the current request.
        """

        return self.request.get_service()

    def get_service_connection(self):
        """
        Retrieves the reference to the service connection
        associated with the handling of the request.

        @rtype: ServiceConnection
        @return: The reference to the service connection
        associated with the handling of the request.
        """

        return self.request.get_service_connection()

    def get_address(self):
        """
        Retrieves the (ip) address of the service connection
        associated with the rest request.

        @rtype: String
        @return: The (ip) address of the service connection.
        """

        # retrieves the service connection for the request,
        # unpacks the connection address into the address
        service_connection = self.request.service_connection
        address = service_connection.connection_address[0]
        return address

    def get_port(self):
        """
        Retrieves the (tcp) port of the service connection
        associated with the rest request.

        @rtype: String
        @return: The (tcp) port of the service connection.
        """

        # retrieves the service connection for the request,
        # unpacks the connection port into the port
        service_connection = self.request.service_connection
        port = service_connection.connection_address[1]
        return port

    def _update_session_cookie(self):
        """
        Updates the current session.
        This method retrieves information from the cookie to
        update the session based in the session id.
        """

        # in case there's already a loaded session for
        # the current rest request returns immediately
        if self.session: return

        # retrieves the cookie value from the request
        cookie_value = self.request.get_header(COOKIE_VALUE)

        # in case there is not valid cookie value,
        # must return immediately
        if not cookie_value: return

        # creates a new cookie, using the header value of
        # it and then parses it to populate the attributes
        cookie = Cookie(cookie_value)
        cookie.parse()

        # retrieves the session id
        session_id = cookie.get_attribute(SESSION_ID_VALUE)

        # in case there is no session id defined in the
        # current cookie, must return immediately
        if not session_id: return

        # retrieves the session from the session id
        self.session = self.rest.get_session(session_id)

        # if no session is selected, raises an invalid session
        # exception to indicate the error
        if not self.session: raise exceptions.InvalidSession("no session started or session timed out")

    def _update_session_attribute(self):
        """
        Updates the current session.
        This method retrieves information from the attribute to
        update the session based in the session id.
        """

        # in case there's already a loaded session for
        # the current rest request returns immediately
        if self.session: return

        # retrieves the session id attribute value from the request
        session_id = self.request.get_attribute(SESSION_ID_VALUE)

        # in case there is no valid session id
        # returns immediately
        if not session_id: return

        # retrieves the session from the session id
        self.session = self.rest.get_session(session_id)

        # if no session is selected, raises an invalid session
        # exception to indicate the error
        if not self.session: raise exceptions.InvalidSession("no session started or session timed out")

    def _get_domain(self):
        """
        Retrieves the domain using the http request header
        host value.

        @rtype: Sring
        @return: The currently used domain.
        """

        # retrieves the host value from the request headers
        host = self.request.get_header(HOST_VALUE)

        # in case the host is not defined
        if not host:
            # returns invalid
            return None

        # retrieves the domain removing the port part
        # of the host value
        domain = host.rsplit(":", 1)[0]

        # returns the domain
        return domain

class RestSession:
    """
    The rest session class.
    """

    session_id = None
    """ The session id """

    timeout = None
    """ The timeout """

    maximum_timeout = None
    """ The maximum timeout """

    expire_time = None
    """ The expire time """

    cookie = None
    """ The cookie """

    attributes_map = {}
    """ The attributes map """

    _maximum_expire_time = None
    """ The maximum expire time """

    _access_lock = None
    """ The lock used to control the access to the session """

    def __init__(self, session_id = None, timeout = DEFAULT_TIMEOUT, maximum_timeout = DEFAULT_MAXIMUM_TIMEOUT):
        """
        Constructor of the class.

        @type session_id: String
        @param session_id: The session id.
        @type timeout: float
        @param timeout: The timeout.
        @type maxmimum_timeout: float
        @param maxmimum_timeout: The maximum timeout.
        """

        self.session_id = session_id
        self.timeout = timeout
        self.maximum_timeout = maximum_timeout

        self.attributes_map = {}

        self._access_lock = threading.RLock()

        # generates the expire time from the
        # current time and the given timeout
        # and maximum timeout
        self._generate_expire_time(timeout, maximum_timeout)

    def update(self, domain = None, include_sub_domain = False, secure = False):
        self.start(
            domain = domain,
            include_sub_domain = include_sub_domain,
            secure = secure
        )

    def start(self, domain = None, include_sub_domain = False, secure = False):
        """
        Starts the current session.

        @type domain: String
        @param domain: The domain to be used by the cookie.
        @type include_sub_domain: bool
        @param include_sub_domain: Controls if the sub domain should be included.
        @type secure: bool
        @param secure: Controls if the cookie should be considered secure,
        and only available through secure connections.
        """

        current_timestamp = time.time()
        current_timestamp += DEFAULT_EXPIRATION_DELTA_TIMESTAMP
        current_date_time = datetime.datetime.utcfromtimestamp(current_timestamp)
        current_date_time_formatted = current_date_time.strftime(DATE_FORMAT)

        self.cookie = Cookie()
        self.cookie.set_main_attribute_name(SESSION_ID_VALUE)
        self.cookie.set_attribute(SESSION_ID_VALUE, self.session_id)
        self.cookie.set_attribute(LANG_VALUE, DEFAULT_LANG_VALUE)
        self.cookie.set_attribute(EXPIRES_VALUE, current_date_time_formatted)

        self._set_domain(domain, include_sub_domain)
        self._set_secure(secure)

    def stop(self, domain = None, include_sub_domain = False, secure = False):
        """
        Stops the current session.

        @type domain: String
        @param domain: The domain used by the cookie.
        @type include_sub_domain: bool
        @param include_sub_domain: Controls if the sub domain should be included.
        @type secure: bool
        @param secure: Controls if the cookie should be considered secure,
        and only available through secure connections.
        """

        self.session_id = None

        self.cookie = Cookie()
        self.cookie.set_main_attribute_name(SESSION_ID_VALUE)
        self.cookie.set_attribute(SESSION_ID_VALUE, "")
        self.cookie.set_attribute(LANG_VALUE, DEFAULT_LANG_VALUE)
        self.cookie.set_attribute(EXPIRES_VALUE, DEFAULT_EXPIRATION_DATE)

        self._set_domain(domain, include_sub_domain)
        self._set_secure(secure)

    def update_expire_time(self):
        """
        Updates the expire time value according
        to the currently defined timeout and
        maximum timeout values.
        """

        self._generate_expire_time(self.timeout, self.maximum_timeout)

    def lock(self):
        """
        Locks the session so that any subsequent access to
        the underlying logic will block the call.
        """

        self._access_lock.acquire()

    def release(self):
        """
        Releases the lock for the access to the session, any
        subsequent access to the session will be "allowed".
        """

        self._access_lock.release()

    def get_session_id(self):
        """
        Retrieves the session id.

        @rtype: String
        @return: The session id.
        """

        return self.session_id

    def set_session_id(self, session_id):
        """
        Sets the session id.

        @type session_id: String
        @param session_id: The session id.
        """

        self.session_id = session_id

    def get_timeout(self):
        """
        Retrieves the timeout.

        @rtype: float
        @return: The timeout.
        """

        return self.timeout

    def set_timeout(self, timeout):
        """
        Sets the timeout.

        @type timeout: float
        @param timeout: The timeout.
        """

        self.timeout = timeout

    def get_maximum_timeout(self):
        """
        Retrieves the maximum timeout.

        @rtype: float
        @return: The maximum timeout.
        """

        return self.maximum_timeout

    def set_maximum_timeout(self, maximum_timeout):
        """
        Sets the maximum timeout.

        @type maximum_timeout: float
        @param maximum_timeout: The maximum timeout.
        """

        self.maximum_timeout = maximum_timeout

    def get_expire_time(self):
        """
        Retrieves the expire time.

        @rtype: float
        @return: The expire time.
        """

        return self.expire_time

    def set_expire_time(self, expire_time):
        """
        Sets the expire time.

        @type expire_time: float
        @param expire_time: The expire time.
        """

        self.expire_time = expire_time

    def get_cookie(self):
        """
        Retrieves the cookie.

        @type cookie: Cookie
        @param cookie: The cookie.
        """

        return self.cookie

    def set_cookie(self, cookie):
        """
        Sets the cookie.

        @type cookie: Cookie
        @param cookie: The cookie.
        """

        self.cookie = cookie

    def get_attribute(self, attribute_name):
        """
        Retrieves the attribute value for the given
        attribute name.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to retrieve.
        @rtype: String
        @return: The retrieved attribute value.
        """

        return self.attributes_map.get(attribute_name, None)

    def set_attribute(self, attribute_name, attribute_value):
        """
        Sets the attribute with the given name with the
        provided value.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to set.
        @type attribute_value: String
        @param attribute_value: The attribute value to set.
        """

        self.attributes_map[attribute_name] = attribute_value

    def unset_attribute(self, attribute_name):
        """
        Unsets the attribute with the given name.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to unset.
        """

        # in case the attribute name exists in
        # the attributes map must unset it from
        # the exiting attributes map
        if attribute_name in self.attributes_map:
            del self.attributes_map[attribute_name]

    def get_attributes_map(self):
        """
        Retrieves the attributes map.

        @rtype: Dictionary
        @return: The attributes map.
        """

        return self.attributes_map

    def set_attributes_map(self, attributes_map):
        """
        Sets the attributes map.

        @type attributes_map: Dictionary
        @param attributes_map: The attributes map.
        """

        self.attributes_map = attributes_map

    def _set_domain(self, domain, include_sub_domain = False):
        """
        Sets the domain "attributes" in the session cookie.

        An optional include sub domains attribute may be used
        to allow the cookie to be propagated to sub domains
        (by default it's disabled).

        @type domain: String
        @param domain: The domain used by the cookie.
        @type include_sub_domain: bool
        @param include_sub_domain: Controls if the sub domain should be included.
        """

        # in case the domain is not defined defined
        # should return immediately
        if not domain: return

        # sets the domain in the cookie
        self.cookie.set_attribute(PATH_VALUE, DEFAULT_PATH)

        # in case the domain is local, returns immediately
        # to avoid problems in the browser
        if domain in LOCALHOST_VALUES: return

        # in case the domain is "valid" and sub domains
        # flag is active, sets the domain in the cookie
        # (including sub domains) otherwise sets only the
        # current domain in the cookie
        if include_sub_domain: self.cookie.set_attribute(DOMAIN_VALUE, "." + domain)
        else: self.cookie.set_attribute(DOMAIN_VALUE, domain)

    def _set_secure(self, secure = False):
        """
        Sets the secure "attributes" in the session cookie.

        An optional include sub domains may be used to allow
        the cookie to be propagated to sub domains (by default
        it's disabled).

        @type secure: bool
        @param secure: Flag that controls if the cookie should
        be considered secure.
        """

        # in case the secure flag is set adds the simple secure
        # attribute to the cookie
        if secure: self.cookie.set_attribute(SECURE_VALUE)

    def _generate_expire_time(self, timeout, maximum_timeout):
        """
        Generates the expire time value from the
        given timeout value using the current
        time.
        The maximum timeout is used to control the generated
        expire time, and for calculation of the maximum expire time.

        @type timeout: float
        @param timeout: The timeout value to be
        used for expire time generation.
        @type maximum_timeout: float
        @param maximum_timeout: The maximum timeout value to be
        used to control the new expire time.
        """

        # retrieves the current time for
        # expire time calculation
        current_time = time.time()

        # calculates the maximum expire time in case it's not defined
        self._maximum_expire_time = self._maximum_expire_time or current_time + maximum_timeout

        # calculates the expire time incrementing
        # the timeout to the current time
        expire_time = current_time + timeout

        # sets the expire time as the calculated expire time
        # or as the maximum expire time in case it's smaller
        self.expire_time = self._maximum_expire_time > expire_time and expire_time or self._maximum_expire_time

class Cookie:
    """
    The cookie class representing an http cookie.
    """

    string_value = None
    """ The string value """

    main_attribute_name = None
    """ The main attribute name """

    attributes_map = {}
    """ The attributes map """

    def __init__(self, string_value = None):
        """
        Constructor of the class.

        @type string_value: String
        @param string_value: The cookie string value.
        """

        self.string_value = string_value

        self.attributes_map = {}

    def parse(self):
        """
        Parses the string value creating the attributes
        map, with all the name and values association.
        """

        # in case the string value is invalid
        if self.string_value == None:
            # raises an invalid cookie exception
            raise exceptions.InvalidCookie("invalid cookie string value")

        # retrieves the value pairs by splitting the
        # string value
        value_pairs = self.string_value.split(";")

        # iterates over all the value pairs to
        # retrieve the name and value pairs
        for value_pair in value_pairs:
            # strips the value pair to remove
            # extra white spaces
            value_pair_stripped = value_pair.strip()

            # splits the value pair
            value_splitted = value_pair_stripped.split("=")

            # in case the value pairs does respect
            # the key value
            if len(value_splitted) == 2:
                # retrieves the name and the value
                name, value = value_splitted
            else:
                # sets the name as the first element
                name = value_splitted[0]

                # sets the value as invalid (not set)
                value = None

            # sets the value in the attributes map
            self.attributes_map[name] = value

    def serialize(self):
        """
        Serializes the cookie into a string value, using
        the current attributes map.
        """

        # starts the string value
        string_value = str()

        # in case the main attribute name exists and exists in the
        # attributes map
        if self.main_attribute_name and self.main_attribute_name in self.attributes_map:
            # retrieves the main attribute value
            main_attribute_value = self.attributes_map[self.main_attribute_name]

            # serializes the main attribute
            serialized_attribute = self._serialize_attribute(self.main_attribute_name, main_attribute_value)

            # appends the serialized attribute to the string value
            string_value += serialized_attribute

        # iterates over all the attribute name and value in
        # the attributes map
        for attribute_name, attribute_value in self.attributes_map.items():
            # in case the attribute is not the main one
            if not attribute_name == self.main_attribute_name:
                # serializes the attribute
                serialized_attribute = self._serialize_attribute(attribute_name, attribute_value)

                # appends the serialized attribute to the string value
                string_value += serialized_attribute

        # returns the string value
        return string_value

    def get_attribute(self, attribute_name):
        """
        Retrieves an attribute using the attribute name.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to retrieve.
        """

        return self.attributes_map.get(attribute_name, None)

    def set_attribute(self, attribute_name, attribute_value = None):
        """
        Retrieves an attribute using the attribute name.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to set.
        @type attribute_value: Object
        @param attribute_value: The value of the attribute to set.
        """

        self.attributes_map[attribute_name] = attribute_value

    def set_main_attribute_name(self, main_attribute_name):
        """
        Sets the main attribute name.

        @type main_attribute_name: String
        @param main_attribute_name: The main attribute name.
        """

        self.main_attribute_name = main_attribute_name

    def _serialize_attribute(self, attribute_name, attribute_value = None):
        """
        Serializes the given attribute (name and value) into
        a valid cookie string.

        In case no attribute value is provided the attribute
        is considered to be singleton no equal sign.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to be serialized.
        @type attribute_value: Object
        @param attribute_value: The of the attribute to be serialized.
        @rtype: String
        @return: The cookie serialized string.
        """

        # converts the attribute into the correct key value
        # pair defaulting to a single name attribute in case
        # no value is defined
        if attribute_value == None: return attribute_name + ";"
        else: return attribute_name + "=" + str(attribute_value) + ";"
