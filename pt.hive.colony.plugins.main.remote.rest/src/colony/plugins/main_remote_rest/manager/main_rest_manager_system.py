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

__revision__ = "$LastChangedRevision: 7147 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-12-21 16:50:46 +0000 (seg, 21 Dez 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import time
import datetime

import colony.libs.quote_util
import colony.libs.string_buffer_util

import main_rest_manager_exceptions

REGEX_COMILATION_LIMIT = 99
""" The regex compilation limit """

HANDLER_BASE_FILENAME = "/colony_mod_python/rest/"
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

LOCALHOST_VALUES = ("localhost", "127.0.0.1")
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

class MainRestManager:
    """
    The main rest manager class.
    """

    main_rest_manager_plugin = None
    """ The main rest manager plugin """

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

    rest_session_map = {}
    """ The map associating the session id with the rest session """

    def __init__(self, main_rest_manager_plugin):
        """
        Constructor of the class.

        @type main_rest_manager_plugin: MainRestManagerPlugin
        @param main_rest_manager_plugin: The main rest manager plugin.
        """

        self.main_rest_manager_plugin = main_rest_manager_plugin

        self.matching_regex_list = []
        self.matching_regex_base_values_map = {}
        self.rest_service_routes_map = {}
        self.plugin_id_plugin_map = {}
        self.regex_index_plugin_id_map = {}
        self.service_methods = []
        self.service_methods_map = {}
        self.rest_session_map = {}

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
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the rest encoder plugins
        rest_encoder_plugins = self.main_rest_manager_plugin.rest_encoder_plugins

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
            raise main_rest_manager_exceptions.InvalidPath("invalid last path name value size: " + str(last_path_name_splitted_length))

        # retrieves the encoder name
        encoder_name = last_path_initial_extension

        # constructs the rest path list
        path_list = middle_path_name + [last_path_initial_name]

        # creates the rest request
        rest_request = RestRequest(self, request)

        try:
            # updates the rest request session
            rest_request.update_session()
        except:
            # logs a debug message
            self.main_rest_manager_plugin.debug("Session is invalid no session loaded or updated")

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
            return self.handle_rest_request_services(rest_request)
        else:
            # iterates over all the matching regex in the matching regex list
            for matching_regex in self.matching_regex_list:
                # retrieves the resource path match
                resource_path_match = matching_regex.match(resource_path)

                # in case there is a valid resource path match
                if resource_path_match:
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

                    # handles the rest request to the rest servicxe plugin
                    return rest_service_plugin.handle_rest_request(rest_request)

            # raises the rest request not handled exception
            raise main_rest_manager_exceptions.RestRequestNotHandled("no rest service plugin could handle the request")

        # returns true
        return True

    def handle_rest_request_services(self, rest_request):
        """
        Handles the rest request meant for services.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled.
        @rtype: bool
        @return: The result of the handling.
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
            raise main_rest_manager_exceptions.InvalidMethod("the method name " + method_name + " is not valid")

        # serializes the result for the given encoder name retrieving the content type
        # and the translated result
        content_type, result_translated = self.translate_result(result, encoder_name)

        # sets the content type for the rest request
        rest_request.set_content_type(content_type)

        # sets the result for the rest request
        rest_request.set_result_translated(result_translated)

        # flushes the rest request
        rest_request.flush()

        # returns true
        return True

    def is_active(self):
        """
        Tests if the service is active.

        @rtype: bool
        @return: If the service is active.
        """

        # retrieves the plugin manager
        manager = self.main_rest_manager_plugin.manager

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
            updated_rpc_service_plugins = [updated_rpc_service_plugin]
        else:
            # clears the service methods list
            self.service_methods = []

            # clears the service map
            self.service_methods_map = {}

            # retrieves the updated rpc service plugins
            updated_rpc_service_plugins = self.main_rest_manager_plugin.rpc_service_plugins

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
        rest_encoder_plugins = self.main_rest_manager_plugin.rest_encoder_plugins

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
            raise main_rest_manager_exceptions.InvalidEncoder("the " + encoder_name + " encoder is invalid")
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

        # retrieves the session id
        session_id = session.get_session_id()

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

    def get_session(self, session_id):
        """
        Retrieves the session with the given session id
        from the sessions map.

        @type session_id: String
        @param session_id: The id of the session to retrieve.
        """

        return self.rest_session_map.get(session_id, None)

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

    main_rest_manager = None
    """ The main rest manager """

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

    def __init__(self, main_rest_manager, request):
        """
        Constructor of the class.

        @type main_rest_manager: MainRestManager
        @param main_rest_manager: The main rest manager.
        @type request: Request
        @param request: The associated request.
        """

        self.main_rest_manager = main_rest_manager
        self.request = request

        self.rest_encoder_plugins = []
        self.rest_encoder_plugins_map = {}

    def start_session(self, force = False, session_id = None):
        """
        Starts the session for the given session id,
        or generates a new session id.

        @type force: bool
        @param force: If the session should be created if a session
        is already selected.
        @type session_id: String
        @param session_id: The session id to be used.
        """

        # in case a session exists and force flag is disabled
        # avoids creation
        if self.session and not force:
            # returns immediately
            return

        # in case no session id is defined
        if not session_id:
            # retrieves the random plugin
            random_plugin = self.main_rest_manager.main_rest_manager_plugin.random_plugin

            # creates a new random session id
            session_id = random_plugin.generate_random_md5_string()

        # creates a new rest session and sets
        # it as the current session
        self.session = RestSession(session_id)

        # retrieves the host name value
        domain = self._get_domain()

        # starts the session with the defined domain
        self.session.start(domain)

        # adds the session to the main rest manager
        self.main_rest_manager.add_session(self.session)

    def stop_session(self):
        """
        Stops the current session.
        """

        # in case no session is defined
        if not self.session:
            # crates a new empty session
            self.session = RestSession()

        # retrieves the host name value
        domain = self._get_domain()

        # stops the session with the defined domain
        self.session.start(domain)

        # removes the session from the main rest manager
        self.main_rest_manager.remove_session(self.session)

    def update_session(self):
        """
        Updates the current session.
        The updating of the session will be archived using
        a set of predefined techniques.
        """

        # updates the session using the cookie method
        self._update_session_cookie()

        # updates the session using the attribute method
        self._update_session_attribute()

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

        # in case the operation is of type get
        if self.request.operation_type == GET_METHOD_VALUE:
            # returns true (valid)
            return True
        # otherwise
        else:
            # returns false (invalid)
            return False

    def is_post(self):
        """
        Tests the request to check if it is of type
        post method.

        @rtype: bool
        @return: If the request method is of type post.
        """

        # in case the operation is of type post
        if self.request.operation_type == POST_METHOD_VALUE:
            # returns true (valid)
            return True
        # otherwise
        else:
            # returns false (invalid)
            return False

    def is_debug(self, minimum_level = 6):
        """
        In case the request should be set in debug mode.
        Maximum verbosity, in actions like exception handling.

        @type minimum_level: int
        @param minimum_level: The minimum level to be used for verbosity.
        """

        # retrieves the main rest manager plugin
        main_rest_manager_plugin = self.main_rest_manager.main_rest_manager_plugin

        # retrieves the resource manager plugin
        resource_manager_plugin = main_rest_manager_plugin.resource_manager_plugin

        # retrieves the debug level
        debug_level = resource_manager_plugin.get_resource("system.debug.level")

        # in case the debug level does meet
        # the required level
        if debug_level and debug_level.data >= minimum_level:
            return True
        else:
            return False

    def flush(self):
        """
        Flushes the rest request buffer.
        """

        # in case there is a session available
        if self.session:
            # retrieves the session cookie
            session_cookie = self.session.get_cookie()

            # in case there is a session cookie
            if session_cookie:
                # serializes the session cookie
                serialized_session_cookie = session_cookie.serialize()

                # sets the session id in the cookie
                self.request.append_header(SET_COOKIE_VALUE, serialized_session_cookie)

                # invalidates the cookie
                self.session.set_cookie(None)

        # sets the content type for the request
        self.request.content_type = self.content_type

        # writes the result translated
        self.request.write(self.result_translated)

        # flushes the request, sending the output to the client
        self.request.flush()

    def redirect(self, target_path, status_code = 302, quote = True):
        """
        Redirects the request logically, so it
        becomes readable as a new resource.

        @type target_path: String
        @param target_path: The target path of the redirection.
        @type status_code: int
        @param status_code: The status code to be used.
        @type quote: bool
        @param quote: If the target path should be quoted.
        """

        # quotes the target path
        target_path_quoted = quote and colony.libs.quote_util.quote(target_path, "/") or target_path

        # sets the status code
        self.request.status_code = status_code

        # sets the location header (using the quoted target path)
        self.request.set_header(LOCATION_VALUE, target_path_quoted)

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

    def get_session(self):
        """
        Retrieves the associated session.

        @rtype: RestSession
        @return: The associated session.
        """

        return self.session

    def set_session(self, session):
        """
        Sets the associated session.

        @type session: RestSession
        @param session: The associated session.
        """

        self.session = session

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

    def set_content_type(self, content_type):
        """
        Sets the content type.

        @type content_type: String
        @param content_type: The content type.
        """

        self.content_type = content_type

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

    def _update_session_cookie(self):
        """
        Updates the current session.
        This method retrieves information from the cookie to
        update the session based in the session id.
        """

        # retrieves the cookie value from the request
        cookie_value = self.request.get_header(COOKIE_VALUE)

        # in case there is not valid cookie value
        if not cookie_value:
            # returns immediately
            return

        # creates a new cookie
        cookie = Cookie(cookie_value)

        # parses the cookie
        cookie.parse()

        # retrieves the session id
        session_id = cookie.get_attribute(SESSION_ID_VALUE)

        # retrieves the session from the session id
        self.session = self.main_rest_manager.get_session(session_id)

        # if no session is selected
        if not self.session:
            # raises an invalid session exception
            raise main_rest_manager_exceptions.InvalidSession("no session started or session timed out")

    def _update_session_attribute(self):
        """
        Updates the current session.
        This method retrieves information from the attribute to
        update the session based in the session id.
        """

        # retrieves the session id attribute value from the request
        session_id = self.request.get_attribute(SESSION_ID_VALUE)

        # in case there is no valid session id
        if not session_id:
            # returns immediately
            return

        # retrieves the session from the session id
        self.session = self.main_rest_manager.get_session(session_id)

        # if no session is selected
        if not self.session:
            # raises an invalid session exception
            raise main_rest_manager_exceptions.InvalidSession("no session started or session timed out")

    def _get_domain(self):
        """
        Retrieves the domain using the http request header
        host value.

        @rtype: Sring
        @return: The currently used domain.
        """

        # retrieves the host value from the request headers
        host = self.request.headers_map.get(HOST_VALUE, None)

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

    cookie = None
    """ The cookie """

    attributes_map = {}
    """ The attributes map """

    def __init__(self, session_id = None):
        """
        Constructor of the class.

        @type session_id: String
        @param session_id: The session id.
        """

        self.session_id = session_id

        self.attributes_map = {}

    def start(self, domain = None, include_sub_domain = True):
        """
        Starts the current session.

        @type domain: String
        @param domain: The domain to be used by the cookie.
        @type include_sub_domain: bool
        @param include_sub_domain: Controls if the sub domain should be included.
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

    def stop(self, domain, include_sub_domain = True):
        """
        Stops the current session.

        @type domain: String
        @param domain: The domain used by the cookie.
        @type include_sub_domain: bool
        @param include_sub_domain: Controls if the sub domain should be included.
        """

        self.session_id = None

        self.cookie = Cookie()
        self.cookie.set_main_attribute_name(SESSION_ID_VALUE)
        self.cookie.set_attribute(SESSION_ID_VALUE, "")
        self.cookie.set_attribute(LANG_VALUE, DEFAULT_LANG_VALUE)
        self.cookie.set_attribute(EXPIRES_VALUE, DEFAULT_EXPIRATION_DATE)

        self._set_domain(domain, include_sub_domain)

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
        # the attributes map
        if attribute_name in self.attributes_map:
            # unsets the attribute from the attributes map
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

    def _set_domain(self, domain, include_sub_domain = True):
        """
        Sets the domain "attributes" in the session cookie.

        @type domain: String
        @param domain: The domain used by the cookie.
        @type include_sub_domain: bool
        @param include_sub_domain: Controls if the sub domain should be included.
        """

        # in case the domain is not defined defined
        if not domain:
            # returns immediately
            return

        # sets the domain in the cookie
        self.cookie.set_attribute(PATH_VALUE, DEFAULT_PATH)

        # in case the domain is local
        if domain in LOCALHOST_VALUES:
            # returns immediately
            return

        # in case the domain is "valid" and sub domains
        # flag is active
        if include_sub_domain:
            # sets the domain in the cookie (including sub domains)
            self.cookie.set_attribute(DOMAIN_VALUE, "." + domain)
        else:
            # sets the domain in the cookie
            self.cookie.set_attribute(DOMAIN_VALUE, domain)

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
            raise main_rest_manager_exceptions.InvalidCookie("invalid cookie string value")

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

    def set_attribute(self, attribute_name, attribute_value):
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

    def _serialize_attribute(self, attribute_name, attribute_value):
        """
        Serializes the given attribute (name and value) into
        a valid cookie string.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to be serialized.
        @type attribute_value: Object
        @param attribute_value: The of the attribute to be serialized.
        @rtype: String
        @return: The cookie serialized string.
        """

        # in case the attribute value is invalid
        if attribute_value == None:
            return attribute_name + "=;"
        # in case the attribute value is valid
        else:
            return attribute_name + "=" + str(attribute_value) + ";"
