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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.map_util
import colony.libs.string_buffer_util

import main_service_policy_exceptions

CONNECTION_TYPE = "connection"
""" The connection type """

BIND_HOST = ""
""" The bind host value """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 5
""" The request timeout """

RESPONSE_TIMEOUT = 5
""" The response timeout """

CHUNK_SIZE = 4096
""" The chunk size """

NUMBER_THREADS = 2
""" The number of threads """

MAXIMUM_NUMBER_THREADS = 4
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

MAXIMUM_NUMBER_WORKS_THREAD = 5
""" The maximum number of works per thread """

WORK_SCHEDULING_ALGORITHM = 1
""" The work scheduling algorithm """

DEFAULT_PORT = 843
""" The default port """

VALID_REQUEST_VALUE = "<policy-file-request/>"
""" The valid request value """

MAIN_SERVICE_POLICY_RESOURCES_PATH = "main_service_policy/policy/resources"
""" The web mvc manager resources path """

DEFAULT_POLICY_FILE = MAIN_SERVICE_POLICY_RESOURCES_PATH + "/default.policy"
""" The default policy file """

ERROR_POLICY_FILE = MAIN_SERVICE_POLICY_RESOURCES_PATH + "/error.policy"
""" The error policy file """

class MainServicePolicy:
    """
    The main service policy class.
    """

    main_service_policy_plugin = None
    """ The main service policy plugin """

    policy_service_handler_plugins_map = {}
    """ The policy service handler plugins map """

    policy_service = None
    """ The policy service reference """

    policy_service_configuration = {}
    """ The policy service configuration """

    def __init__(self, main_service_policy_plugin):
        """
        Constructor of the class.

        @type main_service_policy_plugin: MainServicePolicyPlugin
        @param main_service_policy_plugin: The main service policy plugin.
        """

        self.main_service_policy_plugin = main_service_policy_plugin

        self.policy_service_handler_plugin_map = {}
        self.policy_service_configuration = {}

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # retrieves the main service utils plugin
        main_service_utils_plugin = self.main_service_policy_plugin.main_service_utils_plugin

        # generates the parameters
        service_parameters = self._generate_service_parameters(parameters)

        # generates the policy service using the given service parameters
        self.policy_service = main_service_utils_plugin.generate_service(service_parameters)

        # starts the policy service
        self.policy_service.start_service()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to stop the service.
        """

        # starts the policy service
        self.policy_service.stop_service()

    def policy_service_handler_load(self, policy_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = policy_service_handler_plugin.get_handler_name()

        self.policy_service_handler_plugins_map[handler_name] = policy_service_handler_plugin

    def policy_service_handler_unload(self, policy_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = policy_service_handler_plugin.get_handler_name()

        del self.policy_service_handler_plugins_map[handler_name]

    def set_service_configuration_property(self, service_configuration_property):
        # retrieves the service configuration
        service_configuration = service_configuration_property.get_data()

        # cleans the policy service configuration
        colony.libs.map_util.map_clean(self.policy_service_configuration)

        # copies the service configuration to the policy service configuration
        colony.libs.map_util.map_copy(service_configuration, self.policy_service_configuration)

    def unset_service_configuration_property(self):
        # cleans the policy service configuration
        colony.libs.map_util.map_clean(self.policy_service_configuration)

    def _get_service_configuration(self):
        """
        Retrieves the service configuration map.

        @rtype: Dictionary
        @return: The service configuration map.
        """

        return self.policy_service_configuration

    def _generate_service_parameters(self, parameters):
        """
        Retrieves the service parameters map from the base parameters
        map.

        @type parameters: Dictionary
        @param parameters: The base parameters map to be used to build
        the final service parameters map.
        @rtype: Dictionary
        @return: The final service parameters map.
        """

        # retrieves the end points value
        end_points = parameters.get("end_points", [])

        # retrieves the socket provider value
        socket_provider = parameters.get("socket_provider", None)

        # retrieves the port value
        port = parameters.get("port", DEFAULT_PORT)

        # retrieves the socket parameters value
        socket_parameters = parameters.get("socket_parameters", {})

        # retrieves the service configuration
        service_configuration = self._get_service_configuration()

        # retrieves the end points configuration value
        end_points = service_configuration.get("default_end_points", end_points)

        # retrieves the socket provider configuration value
        socket_provider = service_configuration.get("default_socket_provider", socket_provider)

        # retrieves the port configuration value
        port = service_configuration.get("default_port", port)

        # retrieves the socket parameters configuration value
        socket_parameters = service_configuration.get("default_socket_parameters", socket_parameters)

        # retrieves the number threads configuration value
        number_threads = service_configuration.get("default_number_threads", NUMBER_THREADS)

        # retrieves the scheduling algorithm configuration value
        scheduling_algorithm = service_configuration.get("default_scheduling_algorithm", SCHEDULING_ALGORITHM)

        # retrieves the maximum number threads configuration value
        maximum_number_threads = service_configuration.get("default_maximum_number_threads", MAXIMUM_NUMBER_THREADS)

        # retrieves the maximum number work threads configuration value
        maximum_number_work_threads = service_configuration.get("default_maximum_number_work_threads", MAXIMUM_NUMBER_WORKS_THREAD)

        # retrieves the work scheduling algorithm configuration value
        work_scheduling_algorithm = service_configuration.get("default_work_scheduling_algorithm", WORK_SCHEDULING_ALGORITHM)

        # creates the pool configuration map
        pool_configuration = {"name" : "policy pool",
                              "description" : "pool to support policy client connections",
                              "number_threads" : number_threads,
                              "scheduling_algorithm" : scheduling_algorithm,
                              "maximum_number_threads" : maximum_number_threads,
                              "maximum_number_works_thread" : maximum_number_work_threads,
                              "work_scheduling_algorithm" : work_scheduling_algorithm}

        # creates the extra parameters map
        extra_parameters = {}

        # creates the parameters map
        parameters = {"type" : CONNECTION_TYPE,
                      "service_plugin" : self.main_service_policy_plugin,
                      "service_handling_task_class" : PolicyClientServiceHandler,
                      "end_points" : end_points,
                      "socket_provider" : socket_provider,
                      "bind_host" : BIND_HOST,
                      "port" : port,
                      "socket_parameters" : socket_parameters,
                      "chunk_size" : CHUNK_SIZE,
                      "service_configuration" : service_configuration,
                      "extra_parameters" :  extra_parameters,
                      "pool_configuration" : pool_configuration,
                      "client_connection_timeout" : CLIENT_CONNECTION_TIMEOUT,
                      "connection_timeout" : REQUEST_TIMEOUT,
                      "request_timeout" : REQUEST_TIMEOUT,
                      "response_timeout" : RESPONSE_TIMEOUT}

        # returns the parameters
        return parameters

class PolicyClientServiceHandler:
    """
    The policy client service handler class.
    """

    service_plugin = None
    """ The service plugin """

    service_connection_handler = None
    """ The service connection handler """

    service_configuration = None
    """ The service configuration """

    service_utils_exception_class = None
    """" The service utils exception class """

    def __init__(self, service_plugin, service_connection_handler, service_configuration, service_utils_exception_class, extra_parameters):
        """
        Constructor of the class.

        @type service_plugin: Plugin
        @param service_plugin: The service plugin.
        @type service_connection_handler: AbstractServiceConnectionHandler
        @param service_connection_handler: The abstract service connection handler, that
        handles this connection.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration.
        @type main_service_utils_exception: Class
        @param main_service_utils_exception: The service utils exception class.
        @type extra_parameters: Dictionary
        @param extra_parameters: The extra parameters.
        """

        self.service_plugin = service_plugin
        self.service_connection_handler = service_connection_handler
        self.service_configuration = service_configuration
        self.service_utils_exception_class = service_utils_exception_class

    def handle_opened(self, service_connection):
        pass

    def handle_closed(self, service_connection):
        pass

    def handle_request(self, service_connection):
        try:
            # retrieves the request
            request = self.retrieve_request(service_connection)
        except main_service_policy_exceptions.MainServicePolicyException:
            # prints a debug message about the connection closing
            self.service_plugin.debug("Connection: %s closed by peer, timeout or invalid request" % str(service_connection))

            # returns false (connection closed)
            return False

        try:
            # prints debug message about request
            self.service_plugin.debug("Handling request: %s" % str(request))

            # retrieves the real service configuration,
            # taking the request information into account
            service_configuration = self._get_service_configuration(request)

            # retrieves the plugin manager
            plugin_manager = self.service_plugin.manager

            # retrieves the service plugin path
            service_plugin_path = plugin_manager.get_plugin_path_by_id(self.service_plugin.id)

            # retrieves the policy file path
            policy_file_path = service_configuration.get("policy_file", service_plugin_path + "/" + DEFAULT_POLICY_FILE)

            # sets the file path in the request
            request.set_file_path(policy_file_path)

            try:
                # sends the request to the client (response)
                self.send_request(service_connection, request)
            except main_service_policy_exceptions.MainServicePolicyException:
                # prints a debug message
                self.service_plugin.debug("Connection: %s closed by peer, while sending request" % str(service_connection))

                # returns false (connection closed)
                return False

            # prints a debug message
            self.service_plugin.debug("Connection: %s kept alive for %ss" % (str(service_connection), str(self.service_connection_handler.request_timeout)))
        except Exception, exception:
            # prints info message about exception
            self.service_plugin.info("There was an exception handling the request: " + unicode(exception))

            try:
                # sends the exception
                self.send_exception(service_connection, request, exception)
            except main_service_policy_exceptions.MainServicePolicyException:
                # prints a debug message
                self.service_plugin.debug("Connection: %s closed by peer, while sending exception" % str(service_connection))

                # returns false (connection closed)
                return False

        # returns true (connection remains open)
        return True

    def retrieve_request(self, service_connection):
        """
        Retrieves the request from the received message.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @rtype: PolicyRequest
        @return: The request from the received message.
        """

        # creates the string buffer for the message
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates a request object
        request = PolicyRequest({})

        # creates the start line loaded flag
        start_line_loaded = False

        # creates the received data size (counter)
        received_data_size = 0

        # continuous loop
        while True:
            try:
                # retrieves the data
                data = service_connection.retrieve_data()
            except self.service_utils_exception_class:
                # raises the policy data retrieval exception
                raise main_service_policy_exceptions.PolicyDataRetrievalException("problem retrieving data")

            # in case no valid data was received
            if data == "":
                # raises the policy invalid data exception
                raise main_service_policy_exceptions.PolicyInvalidDataException("empty data received")

            # retrieves the data length
            data_length = len(data)

            # increments the received data size (counter)
            received_data_size += data_length

            # writes the data to the string buffer
            message.write(data)

            # retrieves the message value from the string buffer
            message_value = message.get_value()

            # in case the start line is not loaded
            if not start_line_loaded:
                # finds the first end of string value
                start_line_index = message_value.find("\0")

                # in case there is a new line value found
                if not start_line_index == -1:
                    # retrieves the start line
                    start_line = message_value[:start_line_index]

                    # in case the start line is valid
                    if not start_line == VALID_REQUEST_VALUE:
                        # raises the policy invalid data exception
                        raise main_service_policy_exceptions.PolicyInvalidDataException("invalid data received: " + start_line)

                    # sets the start line loaded flag
                    start_line_loaded = True

                    # returns the request
                    return request

    def send_exception(self, service_connection, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used.
        @type request: PolicyRequest
        @param request: The request to send the exception.
        @type exception: Exception
        @param exception: The exception to be sent.
        """

        # retrieves the plugin manager
        plugin_manager = self.service_plugin.manager

        # retrieves the service plugin path
        service_plugin_path = plugin_manager.get_plugin_path_by_id(self.service_plugin.id)

        # retrieves the error policy file path
        error_policy_file_path = service_plugin_path + "/" + ERROR_POLICY_FILE

        # sets the error policy file path in the request
        request.set_file_path(error_policy_file_path)

        # sends the request to the client (response)
        self.send_request(service_connection, request)

    def send_request(self, service_connection, request):
        # retrieves the result from the request
        result = request.get_result()

        try:
            # sends the result to the service connection
            service_connection.send(result)
        except self.service_utils_exception_class, exception:
            # error in the client side
            self.service_plugin.error("Problem sending request: " + unicode(exception))

            # raises the policy data sending exception
            raise main_service_policy_exceptions.PolicyDataSendingException("problem sending data")

    def _get_service_configuration(self, request):
        """
        Retrieves the service configuration for the given request.
        This retrieval takes into account the request target and characteristics
        to merge the virtual servers configurations.

        @type request: PolicyRequest
        @param request: The request to be used in the resolution
        of the service configuration.
        @rtype: Dictionary
        @return: The resolved service configuration.
        """

        # retrieves the base service configuration
        service_configuration = self.service_configuration

        # returns the service configuration
        return service_configuration

class PolicyRequest:
    """
    The policy request class.
    """

    parameters = {}
    """ The parameters """

    file_path = None
    """ The file path of the policy """

    def __init__(self, parameters):
        """
        Constructor of the class.

        @type parameters: Dictionary
        @param parameters: The request parameters.
        """

        self.parameters = parameters

    def __repr__(self):
        return "(%s)" % self.file_path

    def get_result(self):
        """
        Retrieves the result value for the current request.

        @rtype: String
        @return: The result value for the current request.
        """

        # opens the file path
        file = open(self.file_path, "rb")

        try:
            # reads the file contents
            file_contents = file.read()
        finally:
            # closes the file
            file.close()

        # appends the extra "zero" character
        file_contents += "\0"

        # returns the file contents as the result
        return file_contents

    def set_file_path(self, file_path):
        """
        Sets the file path.

        @type file_path: String
        @param file_path:  The file path.
        """

        self.file_path = file_path
