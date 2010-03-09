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
import urllib

import main_rest_manager_exceptions

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

class MainRestManager:
    """
    The main rest manager class.
    """

    main_rest_manager_plugin = None
    """ The main rest manager plugin """

    matching_regex = None
    """ The matching regex to be used in route matching """

    rest_service_routes_map = {}
    """ The rest service routes map """

    plugin_id_undotted_plugin_map = {}
    """ The plugin id undotted plugin map """

    service_methods = []
    """ The service methods list """

    service_methods_map = {}
    """ The service methods map """

    def __init__(self, main_rest_manager_plugin):
        """
        Constructor of the class.

        @type main_rest_manager_plugin: MainRestManagerPlugin
        @param main_rest_manager_plugin: The main rest manager plugin.
        """

        self.main_rest_manager_plugin = main_rest_manager_plugin

        self.rest_service_routes_map = {}
        self.plugin_id_undotted_plugin_map = {}
        self.service_objects = []
        self.service_methods_map = {}

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
        last_path_name_splitted = last_path_name.split(".")

        # retrieves the last path name splitted length
        last_path_name_splitted_length = len(last_path_name_splitted)

        # sets the default last path initial extension
        last_path_initial_extension = None

        # in case there is an extension defined
        if last_path_name_splitted_length >= 2:
            # retrieves the last path initial name
            last_path_initial_name = last_path_name_splitted[0]

            # retrieves the last path extension
            last_path_initial_extension = last_path_name_splitted[-1]
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
        rest_request = RestRequest(request)

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
            # retrieves the resource path match
            resource_path_match = self.matching_regex.match(resource_path)

            # in case there is a valid resource path match
            if resource_path_match:
                # retrieves the groups map from the resource path match
                groups_map = resource_path_match.groupdict()

                # iterates over all the group items
                for group_name, group_value in groups_map.items():
                    # in case the group value is valid
                    if group_value:
                        # retrieves the rest service plugin
                        rest_service_plugin = self.plugin_id_undotted_plugin_map[group_name]

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
                    variable_value = urllib.unquote(variable_value)

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

        return {"handler_base_filename" : HANDLER_BASE_FILENAME, "handler_extension" : HANDLER_EXTENSION}

    def load_rest_service_plugin(self, rest_service_plugin):
        """
        Loads the rest service plugin, in the rest manager.

        @type rest_service_plugin: Plugin
        @param rest_service_plugin: The rest service plugin to be loaded.
        """

        # retrieves the rest service plugin id
        rest_service_plugin_id = rest_service_plugin.id

        # remove all the dots from the rest service plugin id
        rest_service_plugin_id_undotted = rest_service_plugin_id.replace(".", "")

        # retrieves the rest service plugin routes
        routes_list = rest_service_plugin.get_routes()

        # initializes the rest service plugin id routes list
        self.rest_service_routes_map[rest_service_plugin_id_undotted] = routes_list

        # sets the rest service plugin in the plugin id undotted plugin map
        self.plugin_id_undotted_plugin_map[rest_service_plugin_id_undotted] = rest_service_plugin

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

        # remove all the dots from the rest service plugin id
        rest_service_plugin_id_undotted = rest_service_plugin_id.replace(".", "")

        # deletes the route list for the plugin
        del self.rest_service_routes_map[rest_service_plugin_id_undotted]

        # deletes the rest service plugin from the plugin id undotted plugin map
        del self.plugin_id_undotted_plugin_map[rest_service_plugin_id_undotted]

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

    def _update_matching_regex(self):
        """
        Updates the matching regex.
        """

        # starts the matching regex value
        matching_regex_value = r""

        # sets the is first plugin flag
        is_first_plugin = True

        # iterates over all the items in the rest service routes map
        for rest_service_plugin_id_undotted, routes_list in self.rest_service_routes_map.items():
            # in case it's the first plugin
            if is_first_plugin:
                # unsets the is first plugin flag
                is_first_plugin = False
            else:
                # adds the or operand to the matching regex value
                matching_regex_value += "|"

            # adds the group name part of the regex to the matching regex value
            matching_regex_value += "(?P<" + rest_service_plugin_id_undotted + ">"

            # sets the is first flag
            is_first = True

            # iterates over all the routes in the routes list
            for route in routes_list:
                # in case it's the first route
                if is_first:
                    # unsets the is first flag
                    is_first = False
                else:
                    # adds the or operand to the matching regex value
                    matching_regex_value += "|"

                # adds the route to the matching regex value
                matching_regex_value += route

            # closes the matching regex value group
            matching_regex_value += ")"

        # compiles the matching regex value
        self.matching_regex = re.compile(matching_regex_value)

class RestRequest:
    """
    The rest request class.
    """

    request = None
    """ The associated request """

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

    def __init__(self, request):
        """
        Constructor of the class.

        @type request: Request
        @param request: The associated request.
        """

        self.request = request

    def parse_post(self):
        """
        Parses the post message using the default,
        parses and the default encoding.
        """

        # parses the post attributes
        self.request.parse_post_attributes()

    def flush(self):
        """
        Flushes the rest request buffer.
        """

        # sets the content type for the request
        self.request.content_type = self.content_type

        # writes the result translated
        self.request.write(self.result_translated)

        # flushes the request, sending the output to the client
        self.request.flush()

    def redirect(self, target_path):
        """
        Redirects the request logically, so it
        becomes readable as a new resource.

        @type target_path: String
        @param target_path: The target path of the redirection.
        """

        # sets the status code as temporary redirect
        self.request.status_code = 307

        # sets the redirection headers
        self.request.set_header("Location", target_path)
        self.request.set_header("Request-URI", target_path)

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
