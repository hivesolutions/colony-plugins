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

import threading

import colony.libs.map_util
import colony.libs.string_buffer_util

import main_client_apple_push_structures

DEFAULT_SOCKET_NAME = "ssl"
""" The default socket name """

DEFAULT_SOCKET_PARAMETERS = {}
""" The default socket parameters """

REQUEST_TIMEOUT = 10
""" The request timeout """

RESPONSE_TIMEOUT = 10
""" The response timeout """

MESSAGE_MAXIMUM_SIZE = 38
""" The message maximum size """

class MainClientApplePush:
    """
    The main client apple push class.
    """

    main_client_apple_push_plugin = None
    """ The main client apple push plugin """

    def __init__(self, main_client_apple_push_plugin):
        """
        Constructor of the class.

        @type main_client_apple_push_plugin: MainClientApplePushPlugin
        @param main_client_apple_push_plugin: The main client apple push plugin.
        """

        self.main_client_apple_push_plugin = main_client_apple_push_plugin

    def create_client(self, parameters):
        """
        Creates a client object for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to be used in creating
        the client object.
        @rtype: ApplePushClient
        @return: The created client object.
        """

        # creates the apple push client
        apple_push_client = ApplePushClient(self)

        # returns the apple push client
        return apple_push_client

    def create_request(self, parameters):
        pass

class ApplePushClient:
    """
    The apple push client class, representing
    a client connection in the apple push protocol.
    """

    main_client_apple_push = None
    """ The main client apple push object """

    client_connection = None
    """ The current client connection """

    _apple_push_client = None
    """ The apple push client object used to provide connections """

    _apple_push_client_lock = None
    """ Lock to control the fetching of the queries """

    def __init__(self, main_client_apple_push):
        """
        Constructor of the class.

        @type main_client_apple_push: MainClientApplePush
        @param main_client_apple_push: The main client apple push object.
        """

        self.main_client_apple_push = main_client_apple_push

        self._apple_push_client_lock = threading.RLock()

    def open(self, parameters):
        # generates the parameters
        client_parameters = self._generate_client_parameters(parameters)

        # creates the apple push client, generating the internal structures
        self._apple_push_client = self.main_client_apple_push.main_client_apple_push_plugin.main_client_utils_plugin.generate_client(client_parameters)

        # starts the apple push client
        self._apple_push_client.start_client()

    def close(self, parameters):
        # stops the apple push client
        self._apple_push_client.stop_client()

    def notify_device(self, host, port, device_token, payload, identifier = None, expiry = None, socket_name = DEFAULT_SOCKET_NAME, socket_parameters = DEFAULT_SOCKET_PARAMETERS):
        # retrieves the corresponding (apple push) client connection
        self.client_connection = self._apple_push_client.get_client_connection((host, port, socket_name, socket_parameters))

        # acquires the apple push client lock
        self._apple_push_client_lock.acquire()

        try:
            # in case both the identifier and the expiry
            # values are defined the type of message is enhanced
            if identifier and expiry:
                # creates the enhanced notification message
                notification_message = main_client_apple_push_structures.EnhancedNotificationMessage(device_token, payload, identifier, expiry)
            # otherwise it must be simple
            else:
                # creates the simple notification message
                notification_message = main_client_apple_push_structures.SimpleNotificationMessage(device_token, payload)

            # sends the request for the notification message
            self.send_request(notification_message)
        finally:
            # releases the apple push client lock
            self._apple_push_client_lock.release()

    def notify_device_error(self, host, port, device_token, payload, identifier = None, expiry = None, socket_name = DEFAULT_SOCKET_NAME, socket_parameters = DEFAULT_SOCKET_PARAMETERS):
        # retrieves the corresponding (apple push) client connection
        self.client_connection = self._apple_push_client.get_client_connection((host, port, socket_name, socket_parameters))

        # acquires the apple push client lock
        self._apple_push_client_lock.acquire()

        try:
            # in case both the identifier and the expiry
            # values are defined the type of message is enhanced
            if identifier and expiry:
                # creates the enhanced notification message
                notification_message = main_client_apple_push_structures.EnhancedNotificationMessage(device_token, payload, identifier, expiry)
            # otherwise it must be simple
            else:
                # creates the simple notification message
                notification_message = main_client_apple_push_structures.SimpleNotificationMessage(device_token, payload)

            # sends the request for the notification message
            request = self.send_request(notification_message)

            # creates the error notification response
            notification_response = main_client_apple_push_structures.ErrorNotificationResponse()

            # retrieves the response for the given request, notification
            # response and size
            response = self.retrieve_response(request, notification_response, 6)
        finally:
            # releases the apple push client lock
            self._apple_push_client_lock.release()

        # returns the response
        return response

    def obtain_feedback(self, host, port, socket_name = DEFAULT_SOCKET_NAME, socket_parameters = DEFAULT_SOCKET_PARAMETERS):
        # retrieves the corresponding (apple push) client connection
        self.client_connection = self._apple_push_client.get_client_connection((host, port, socket_name, socket_parameters))

        # acquires the apple push client lock
        self._apple_push_client_lock.acquire()

        try:
            # creates the error notification response
            notification_response = main_client_apple_push_structures.FeedbackNotificationResponse()

            # retrieves the response for the given notification response and size
            response = self.retrieve_response(None, notification_response, -1)
        finally:
            # releases the apple push client lock
            self._apple_push_client_lock.release()

        # returns the response
        return response

    def send_request(self, notification_message):
        """
        Sends the request for the given parameters.

        @type notification_message: NotificationMessage
        @param notification_message: The notification message to be sent.
        @rtype: ApplePushRequest
        @return: The sent request for the given parameters.
        """

        # creates the apple push request with the the notification message
        request = ApplePushRequest(notification_message)

        # retrieves the result value from the request
        result_value = request.get_result()

        # sends the result value
        self.client_connection.send(result_value)

        # returns the request
        return request

    def retrieve_response(self, request, notification_response, response_size = MESSAGE_MAXIMUM_SIZE, response_timeout = None):
        """
        Retrieves the response from the sent request.

        @type request: ApplePushRequest
        @param request: The request that originated the response.
        @type notification_response: NotificationMessage
        @param notification_response: The notification response to be used.
        @type response_size: int
        @param response_size: The size of the response.
        @type response_timeout: int
        @param response_timeout: The timeout for the response retrieval.
        @rtype: ApplePushResponse
        @return: The response from the sent request.
        """

        # creates a response object
        response = ApplePushResponse(request, notification_response)

        # creates a string buffer to hold the data
        data_buffer = colony.libs.string_buffer_util.StringBuffer()

        try:
            # receives the data
            data = self.client_connection.receive(response_timeout, response_size)

            # writes the data to the data buffer
            data_buffer.write(data)
        except:
            # avoids the exception because we should be aware
            # of timeouts in the processing of the data
            pass

        # retrieves the complete data from the data buffer
        complete_data = data_buffer.get_value()

        # processes the (complete) data
        response.process_data(complete_data)

        # returns the response
        return response

    def _generate_client_parameters(self, parameters):
        """
        Retrieves the client parameters map from the base parameters
        map.

        @type parameters: Dictionary
        @param parameters: The base parameters map to be used to build
        the final client parameters map.
        @rtype: Dictionary
        @return: The client service parameters map.
        """

        # creates the default parameters
        default_parameters = {
            "client_plugin" : self.main_client_apple_push.main_client_apple_push_plugin,
            "request_timeout" : REQUEST_TIMEOUT,
            "response_timeout" : RESPONSE_TIMEOUT
        }

        # creates the parameters map, from the default parameters
        parameters = colony.libs.map_util.map_extend(parameters, default_parameters, False)

        # returns the parameters
        return parameters

class ApplePushRequest:
    """
    The apple push request class.
    """

    notification_message = None
    """ The notification message for the request """

    def __init__(self, notification_message):
        """
        Constructor of the class.

        @type notification_message: int
        @param notification_message: The notification message for the request.
        """

        self.notification_message = notification_message

    def get_result(self):
        """
        Retrieves the result string (serialized) value of
        the request.

        @rtype: String
        @return: The result string (serialized) value of
        the request.
        """

        # validates the current request
        self.validate()

        # retrieves the result value
        result_value = self.notification_message.get_value()

        # returns the result value
        return result_value

    def validate(self):
        """
        Validates the current request, raising exception
        in case validation fails.
        """

        pass

class ApplePushResponse:
    """
    The apple push response class.
    """

    request = None
    """ The request that originated the response """

    notification_response = None
    """ The retrieved notification response """

    def __init__(self, request, notification_response = None):
        """
        Constructor of the class.

        @type request: ApplePushRequest
        @param request: The request.
        @type notification_response: NotificationResponse
        @param notification_response: The retrieved notification response
        """

        self.request = request
        self.notification_response = notification_response

    def process_data(self, data):
        # process the value using the notification response
        self.notification_response.process_value(data)
