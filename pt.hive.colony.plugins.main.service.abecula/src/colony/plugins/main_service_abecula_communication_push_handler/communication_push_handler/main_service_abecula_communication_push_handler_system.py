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

import types
import base64
import threading

import colony.libs.map_util

import main_service_abecula_communication_push_handler_exceptions

HANDLER_NAME = "communication_push"
""" The handler name """

RESULT_VALUE = "result"
""" The result value """

SUCCESS_VALUE = "success"
""" The success value """

MESSAGE_CONTENTS_VALUE = "message_contents"
""" The message contents value """

MESSAGE_VALUE = "MESSAGE"
""" The message value """

COMMUNICATION_CLIENT_ID_VALUE = "communication_client_id"
""" The communication client id value """

COMMUNICATION_NAME_VALUE = "communication_name"
""" The communication name value """

COMMUNICATION_NAMES_VALUE = "communication_names"
""" The communication names value """

COMMUNICATION_PROFILE_NAMES_VALUE = "communication_profile_names"
""" The communication profile names value """

COUNT_VALUE = "count"
""" The count value """

NOTIFICATIONS_VALUE = "notifications"
""" The notifications value """

INFORMATION_VALUE = "information"
""" The information value """

INFORMATION_ITEM_VALUE = "information_item"
""" The information item value """

INFORMATION_KEY_VALUE = "information_key"
""" The information key value """

COMMUNICATION_PROFILE_NAME_VALUE = "communication_profile_name"
""" The communication profile name value """

COMMUNICATION_VALUE = "communication"
""" The communication value """

COMMUNICATION_HANDLER_VALUE = "communication_handler"
""" The communication handler value """

COMMUNICATION_PROFILE_VALUE = "communication_profile"
""" The communication profile value """

PROPERTY_NAME_VALUE = "property_name"
""" The property name value """

PROPERTY_VALUE_VALUE = "property_value"
""" The property value value """

AUTHENTICATED_OPERATIONS_VALUE = "authenticated_operations"
""" The authenticated operation value """

AUTHENTICATION_PROPERTIES_VALUE = "authentication_properties"
""" The authentication properties value """

AUTHENTICATION_HANDLER_VALUE = "authentication_handler"
""" The authentication handler value """

GUID_VALUE = "guid"
""" The guid value """

SEQUENCE_ID_VALUE = "sequence_id"
""" The squence id value """

ARGUMENTS_VALUE = "arguments"
""" The arguments value """

VALID_VALUE = "valid"
""" The valid value """

AUTHORIZATION_VALUE = "Authorization"
""" The authorization value """

class MainServiceAbeculaCommunicationPushHandler:
    """
    The main service abecula communication push handler class.
    """

    main_service_abecula_communication_push_handler_plugin = None
    """ The main service abecula communication push handler plugin """

    service_connection_name_communication_handler_map = {}
    """ The map associating a service connection and communication name tuple with the communication handler """

    service_connection_profile_name_communication_handler_map = {}
    """ The map associating a service connection and communication profile name tuple with the communication handler """

    service_connection_communication_client_id_map = {}
    """ The map associating a service connection with the communication client id """

    operation_id = 0
    """ The operation id """

    operation_id_lock = None
    """ The lock to control operation id creation """

    communication_client_id = 0
    """ The communication client id """

    communication_client_id_lock = None
    """ The lock to control communication client id creation """

    handler_configuration = {}
    """ The handler configuration """

    def __init__(self, main_service_abecula_communication_push_handler_plugin):
        """
        Constructor of the class.

        @type main_service_abecula_communication_push_handler_plugin: MainServiceAbeculaCommunicationPushHandlerPlugin
        @param main_service_abecula_communication_push_handler_plugin: The main service abecula communication push handler plugin.
        """

        self.main_service_abecula_communication_push_handler_plugin = main_service_abecula_communication_push_handler_plugin

        self.service_connection_name_communication_handler_map = {}
        self.service_connection_profile_name_communication_handler_map = {}
        self.service_connection_communication_client_id_map = {}
        self.handler_configuration = {}

        self.operation_id_lock = threading.RLock()
        self.communication_client_id_lock = threading.RLock()

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: AbeculaRequest
        @param request: The abecula request to be handled.
        """

        # retrieves the communication push plugin
        communication_push_plugin = self.main_service_abecula_communication_push_handler_plugin.communication_push_plugin

        # retrieves the operation type
        operation_type = request.get_operation_type()

        # lower cases the operation type
        operation_type = operation_type.lower()

        # creates the operation handler name
        operation_handler_name = "handle_" + operation_type

        # in case the current object does not contains
        # the operation handler
        if not hasattr(self, operation_handler_name):
            # raises the operation not permitted exception
            raise main_service_abecula_communication_push_handler_exceptions.OperationNotPermitted(operation_type)

        # retrieves the operation handler method
        operation_handler_method = getattr(self, operation_handler_name)

        # retrieves the authenticated operations
        authenticated_operations = self.handler_configuration.get(AUTHENTICATED_OPERATIONS_VALUE, [])

        # in case the operation type is set in the authenticated
        # operations list
        if operation_type in authenticated_operations:
            # requires authentication in the request
            self._require_authentication(request)

        # handles the operation
        operation_handler_method(request, communication_push_plugin)

    def print_diagnostics(self):
        """
        Prints diagnostic information about the plugin instance.
        """

        print "service_connection_name_communication_handler_map:" + str(self.service_connection_name_communication_handler_map)
        print "service_connection_profile_name_communication_handler_map:" + str(self.service_connection_profile_name_communication_handler_map)
        print "service_connection_communication_client_id_map:" + str(self.service_connection_communication_client_id_map)

    def set_handler_configuration_property(self, handler_configuration_property):
        # retrieves the handler configuration
        handler_configuration = handler_configuration_property.get_data()

        # cleans the handler configuration
        colony.libs.map_util.map_clean(self.handler_configuration)

        # copies the handler configuration to the handler configuration
        colony.libs.map_util.map_copy(handler_configuration, self.handler_configuration)

    def unset_handler_configuration_property(self):
        # cleans the handler configuration
        colony.libs.map_util.map_clean(self.handler_configuration)

    def handle_connect(self, request, communication_push_plugin):
        """
        Handles the abecula connect command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the service connection
        service_connection = request.get_service_connection()

        # generates a new communication client id
        communication_client_id = self._generate_communication_client_id()

        # sets the communication client id for the service connection
        self.service_connection_communication_client_id_map[service_connection] = communication_client_id

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE,
            COMMUNICATION_CLIENT_ID_VALUE : communication_client_id
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

        # adds the handle connection closed to the connection closed handlers
        service_connection.connection_closed_handlers.append(self.handle_connection_closed)

    def handle_disconnect(self, request, communication_push_plugin):
        """
        Handles the abecula disconnect command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the communication push plugin
        communication_push_plugin = self.main_service_abecula_communication_push_handler_plugin.communication_push_plugin

        # retrieves the service connection
        service_connection = request.get_service_connection()

        # retrieves the communication client id for the service connection
        communication_client_id = self.service_connection_communication_client_id_map[service_connection]

        # removes the service connection structure (using the communication client id)
        self._remove_service_connection_structures(service_connection)

        # removes all the communication handlers for the communication client id
        communication_push_plugin.remove_all_communication_handler(communication_client_id)

        # unloads all the communication profiles for the communication client id
        communication_push_plugin.unload_all_communication_profile(communication_client_id)

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_register(self, request, communication_push_plugin):
        """
        Handles the abecula register command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the service handler
        service_handler = request.get_service_handler()

        # retrieves the service connection
        service_connection = request.get_service_connection()

        # retrieves the decoded request contents from the request
        decoded_request_contents = self._get_decoded_request_contents(request)

        # tries to retrieve the communication client id
        communication_client_id = decoded_request_contents.get(COMMUNICATION_CLIENT_ID_VALUE, None)

        # tries to retrieve the communication name
        communication_name = decoded_request_contents.get(COMMUNICATION_NAME_VALUE, None)

        # retrieves the communication names for the communication name
        communication_names = self._get_values(communication_name)

        # generates a communication handler for the given service handler and service connection
        generated_communication_handler = self.generate_handler(service_handler, service_connection)

        # iterates over all the communication names to register
        # them in the communication push plugin
        for communication_name in communication_names:
            # creates the service connection name tuple
            service_connection_name_tuple = (service_connection, communication_name)

            # sets the generated communication handler in the service connection name communication handler map
            self.service_connection_name_communication_handler_map[service_connection_name_tuple] = generated_communication_handler

            # adds a new communication handler
            communication_push_plugin.add_communication_handler(communication_name, communication_client_id, generated_communication_handler)

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE,
            COMMUNICATION_NAME_VALUE : communication_name
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_unregister(self, request, communication_push_plugin):
        """
        Handles the abecula register command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the service connection
        service_connection = request.get_service_connection()

        # retrieves the decoded request contents from the request
        decoded_request_contents = self._get_decoded_request_contents(request)

        # tries to retrieve the communication client id
        communication_client_id = decoded_request_contents.get(COMMUNICATION_CLIENT_ID_VALUE, None)

        # tries to retrieve the communication name
        communication_name = decoded_request_contents.get(COMMUNICATION_NAME_VALUE, None)

        # retrieves the communication names for the communication name
        communication_names = self._get_values(communication_name)

        # iterates over all the communication names to unregister
        # them in the communication push plugin
        for communication_name in communication_names:
            # creates the service connection name tuple
            service_connection_name_tuple = (service_connection, communication_name)

            # retrieves the generated communication handler for the service connection and communication name
            generated_communication_handler = self.service_connection_name_communication_handler_map[service_connection_name_tuple]

            # removes the communication handler
            communication_push_plugin.remove_communication_handler(communication_name, communication_client_id, generated_communication_handler)

            # removes the service connection name from the service connection name communication handler map
            del self.service_connection_name_communication_handler_map[service_connection_name_tuple]

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE,
            COMMUNICATION_NAME_VALUE : communication_name
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_message(self, request, communication_push_plugin):
        """
        Handles the abecula message command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the decoded request contents from the request
        decoded_request_contents = self._get_decoded_request_contents(request)

        # tries to retrieve the communication client id
        communication_client_id = decoded_request_contents.get(COMMUNICATION_CLIENT_ID_VALUE, None)

        # tries to retrieve the communication name
        communication_name = decoded_request_contents.get(COMMUNICATION_NAME_VALUE, None)

        # tries to retrieve the message contents
        message_contents = decoded_request_contents.get(MESSAGE_CONTENTS_VALUE, None)

        # generates a new notification for the message contents and the communication client id
        notification = communication_push_plugin.generate_notification(message_contents, communication_client_id)

        # sends the notification in broadcast mode
        communication_push_plugin.send_broadcast_notification(communication_name, notification)

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_stat(self, request, communication_push_plugin):
        """
        Handles the abecula stat command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the decoded request contents from the request
        decoded_request_contents = self._get_decoded_request_contents(request)

        # tries to retrieve the information item
        information_item = decoded_request_contents.get(INFORMATION_ITEM_VALUE, None)

        # tries to retrieve the information key
        information_key = decoded_request_contents.get(INFORMATION_KEY_VALUE, None)

        # retrieves the information keys for the information key
        information_keys = self._get_values(information_key)

        # in case the requested information is of type communication
        if information_item == COMMUNICATION_VALUE:
            # sets the information method as the communication information retriever
            information_method = communication_push_plugin.get_communication_information
        # in case the requested information is of type communication handler
        elif information_item == COMMUNICATION_HANDLER_VALUE:
            # sets the information method as the communication handler information retriever
            information_method = communication_push_plugin.get_communication_handler_information
        # in case the requested information is of type communication profile
        elif information_item == COMMUNICATION_PROFILE_VALUE:
            # sets the information method as the communication profile information retriever
            information_method = communication_push_plugin.get_communication_profile_information
        # in case the requested information is not valid
        else:
            # raises the invalid information item exception
            raise main_service_abecula_communication_push_handler_exceptions.InvalidInformationItem(information_item)

        # creates the list to hold the information values
        information_values_list = []

        # iterates over all the information keys to retrieve
        # the various information values
        for information_key in information_keys:
            # retrieves the information value for the information key
            # using the selected information method
            information_value = information_method(information_key)

            # adds the information value to the information values list
            information_values_list.append(information_value)

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE,
            INFORMATION_VALUE : information_values_list
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_prop(self, request, communication_push_plugin):
        """
        Handles the abecula prop command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the decoded request contents from the request
        decoded_request_contents = self._get_decoded_request_contents(request)

        # tries to retrieve the communication client id
        communication_client_id = decoded_request_contents.get(COMMUNICATION_CLIENT_ID_VALUE, None)

        # tries to retrieve the property name
        property_name = decoded_request_contents.get(PROPERTY_NAME_VALUE, None)

        # tries to retrieve the property value
        property_value = decoded_request_contents.get(PROPERTY_VALUE_VALUE, None)

        # sets the communication handler property
        communication_push_plugin.set_communication_handler_property(communication_client_id, property_name, property_value)

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_load(self, request, communication_push_plugin):
        """
        Handles the abecula load command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the service handler
        service_handler = request.get_service_handler()

        # retrieves the service connection
        service_connection = request.get_service_connection()

        # retrieves the decoded request contents from the request
        decoded_request_contents = self._get_decoded_request_contents(request)

        # tries to retrieve the communication client id
        communication_client_id = decoded_request_contents.get(COMMUNICATION_CLIENT_ID_VALUE, None)

        # tries to retrieve the communication profile name
        communication_profile_name = decoded_request_contents.get(COMMUNICATION_PROFILE_NAME_VALUE, None)

        # retrieves the communication profile names for the communication profile name
        communication_profile_names = self._get_values(communication_profile_name)

        # generates a communication handler for the given service handler and service connection
        generated_communication_handler = self.generate_handler(service_handler, service_connection)

        # iterates over all the communication profile names to load them
        for communication_profile_name in communication_profile_names:
            # creates the service communication profile name tuple
            service_connection_profile_name_tuple = (service_connection, communication_profile_name)

            # sets the generated communication handler in the service connection profile name communication handler map
            self.service_connection_profile_name_communication_handler_map[service_connection_profile_name_tuple] = generated_communication_handler

            # loads the communication profile
            communication_push_plugin.load_communication_profile(communication_client_id, communication_profile_name, generated_communication_handler)

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_unload(self, request, communication_push_plugin):
        """
        Handles the abecula unload command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the service connection
        service_connection = request.get_service_connection()

        # retrieves the decoded request contents from the request
        decoded_request_contents = self._get_decoded_request_contents(request)

        # tries to retrieve the communication client id
        communication_client_id = decoded_request_contents.get(COMMUNICATION_CLIENT_ID_VALUE, None)

        # tries to retrieve the communication profile name
        communication_profile_name = decoded_request_contents.get(COMMUNICATION_PROFILE_NAME_VALUE, None)

        # retrieves the communication profile names for the communication name
        communication_profile_names = self._get_values(communication_profile_name)

        # iterates over all the communication profile names to unregister
        # them in the communication push plugin
        for communication_profile_name in communication_profile_names:
            # creates the service communication profile name tuple
            service_connection_profile_name_tuple = (service_connection, communication_profile_name)

            # retrieves the generated communication handler for the service connection and communication profile name
            generated_communication_handler = self.service_connection_profile_name_communication_handler_map[service_connection_profile_name_tuple]

            # unloads the communication profile
            communication_push_plugin.unload_communication_profile(communication_client_id, communication_profile_name, generated_communication_handler)

            # removes the service connection profile name from the service connection profile name communication handler map
            del self.service_connection_profile_name_communication_handler_map[service_connection_profile_name_tuple]

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_set(self, request, communication_push_plugin):
        """
        Handles the abecula set command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the decoded request contents from the request
        decoded_request_contents = self._get_decoded_request_contents(request)

        # tries to retrieve the communication profile name
        communication_profile_name = decoded_request_contents.get(COMMUNICATION_PROFILE_NAME_VALUE, None)

        # tries to retrieve the communication name
        communication_name = decoded_request_contents.get(COMMUNICATION_NAME_VALUE, None)

        # retrieves the communication names for the communication name
        communication_names = self._get_values(communication_name)

        # iterates over all the communication names to set them
        for communication_name in communication_names:
            # sets the communication profile
            communication_push_plugin.set_communication_profile(communication_profile_name, communication_name)

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_unset(self, request, communication_push_plugin):
        """
        Handles the abecula unset command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the decoded request contents from the request
        decoded_request_contents = self._get_decoded_request_contents(request)

        # tries to retrieve the communication profile name
        communication_profile_name = decoded_request_contents.get(COMMUNICATION_PROFILE_NAME_VALUE, None)

        # tries to retrieve the communication name
        communication_name = decoded_request_contents.get(COMMUNICATION_NAME_VALUE, None)

        # retrieves the communication names for the communication name
        communication_names = self._get_values(communication_name)

        # iterates over all the communication names to set them
        for communication_name in communication_names:
            # unsets the communication profile
            communication_push_plugin.unset_communication_profile(communication_profile_name, communication_name)

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_get(self, request, communication_push_plugin):
        """
        Handles the abecula get command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # retrieves the decoded request contents from the request
        decoded_request_contents = self._get_decoded_request_contents(request)

        # tries to retrieve the communication name
        communication_name = decoded_request_contents.get(COMMUNICATION_NAME_VALUE, None)

        # tries to retrieve the count
        count = decoded_request_contents.get(COUNT_VALUE, None)

        # tries to retrieve the guid
        guid = decoded_request_contents.get(GUID_VALUE, None)

        # in case the guid is set
        if guid:
            # retrieves the notification from the notifications buffer of the communication
            notifications = communication_push_plugin.get_notifications_buffer_guid(communication_name, guid)
        # otherwise the count should be used
        else:
            # retrieves the notification from the notifications buffer of the communication
            notifications = communication_push_plugin.get_notifications_buffer(communication_name, count)

        # creates the list for the structured notifications
        structured_notifications = []

        # iterates over all the notifications
        for notification in notifications:
            # structures the notification retrieving the structured notification
            structured_notification = self._structure_notification(notification, communication_name)

            # adds the structured notification to the structured notifications
            structured_notifications.append(structured_notification)

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE,
            NOTIFICATIONS_VALUE : structured_notifications
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_ping(self, request, communication_push_plugin):
        """
        Handles the abecula ping command.

        @type request: AbeculaRequest
        @param request: The abecula request for the command.
        @type communication_push_plugin: Plugin
        @param communication_push_plugin: The communication push plugin.
        """

        # defines the request contents
        request_contents = {
            RESULT_VALUE : SUCCESS_VALUE
        }

        # sets the encoded request contents
        self._set_encoded_request_contents(request, request_contents)

    def handle_connection_closed(self, service_connection):
        """
        The connection closed handler.
        The handler is called upon the closing of the
        connection.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection
        that is being closed.
        """

        # retrieves the communication push plugin
        communication_push_plugin = self.main_service_abecula_communication_push_handler_plugin.communication_push_plugin

        # retrieves the communication client id for the service connection
        communication_client_id = self.service_connection_communication_client_id_map[service_connection]

        # removes the service connection structure (using the communication client id)
        self._remove_service_connection_structures(service_connection)

        # removes all the communication handlers for the communication client id
        communication_push_plugin.remove_all_communication_handler(communication_client_id)

        # unloads all the communication profiles for the communication client id
        communication_push_plugin.unload_all_communication_profile(communication_client_id)

    def generate_handler(self, service_handler, service_connection):
        """
        Generates a communication handler for the
        given request.

        @type service_handler: ServiceHandler
        @param service_handler: The service handler to generate
        a communication handler.
        @type service_connection: ServiceConnection
        @param service_connection: The service connection to generate
        a communication handler.
        @rtype: Function
        @return: The generated communication handler
        """

        def communication_handler(notification, communication_name):
            """
            The "base" communication handler function.
            to be used in the generation of the communication handler.

            @type notification: PushNotification
            @param notification: The push notification to be sent.
            @type communication_name: String
            @param communication_name: The name of the communication to be used.
            """

            # creates a new response
            response = service_handler.create_response()

            # generates a new operation id
            operation_id = self._generate_operation_id()

            # encodes the notification, retrieving the encoded notification
            encoded_notification = self._encode_notification(notification, communication_name)

            # sets the response properties
            response.set_operation_id("S" + str(operation_id))
            response.set_operation_type(MESSAGE_VALUE)
            response.set_target(HANDLER_NAME)

            # writes the encoded notification message to the response
            response.write(encoded_notification)

            # sends the response to the service connection
            service_handler.send_response(service_connection, response)

        # returns the communication handler
        return communication_handler

    def _require_authentication(self, request):
        """
        Requires authentication on the given request.
        In case no valid authentication is set an exception
        is raised.

        @type request: AbeculaRequest
        @param request: The abecula request to be used in
        the request for authentication.
        """

        # retrieves the main authentication plugin
        main_authentication_plugin = self.main_service_abecula_communication_push_handler_plugin.main_authentication_plugin

        # retrieves the authentication token from the request headers
        authentication_token = request.headers_map.get(AUTHORIZATION_VALUE, None)

        # in case no authentication token is set
        if not authentication_token:
            # raises the authentication error
            raise main_service_abecula_communication_push_handler_exceptions.AuthenticationError("no authentication token defined in the request")

        # decodes the authentication token using the base 64 decoder
        # in order to retrieve the decoded authentication token
        decoded_authentication_token = base64.b64decode(authentication_token)

        # splits the decoded authentication token to retrieve
        # the username and the password
        username, password = decoded_authentication_token.split(":", 1)

        # retrieves the authentication properties
        authentication_properties = self.handler_configuration.get(AUTHENTICATION_PROPERTIES_VALUE, {})

        # retrieves the authentication handler
        authentication_handler = authentication_properties.get(AUTHENTICATION_HANDLER_VALUE, None)

        # retrieves the authentication arguments
        authentication_arguments = authentication_properties.get(ARGUMENTS_VALUE, None)

        # authenticates the user
        return_value = main_authentication_plugin.authenticate_user(username, password, authentication_handler, authentication_arguments)

        # in case no return value is received
        if not return_value:
            # raises the authentication error
            raise main_service_abecula_communication_push_handler_exceptions.AuthenticationError("invalid authentication credentials")

        # tries to retrieve the valid value from the return value
        valid_value = return_value.get(VALID_VALUE, False)

        # in case no valid value is set
        if not valid_value:
            # raises the authentication error
            raise main_service_abecula_communication_push_handler_exceptions.AuthenticationError("invalid authentication credentials")

    def _generate_operation_id(self):
        """
        Generates a new operation id.

        @rtype: int
        @return: The generated operation id.
        """

        # acquires the operation id lock
        self.operation_id_lock.acquire()

        # retrieves the current operation id
        operation_id = self.operation_id

        # increment the operation id
        self.operation_id += 1

        # releases the operation id lock
        self.operation_id_lock.release()

        # returns the operation id
        return operation_id

    def _generate_communication_client_id(self):
        """
        Generates a new communication client id.

        @rtype: String
        @return: The generated communication client id.
        """

        # acquires the communication client id lock
        self.communication_client_id_lock.acquire()

        # retrieves the current communication client id
        communication_client_id = self.communication_client_id

        # converts the communication client id to string
        communication_client_id_string = str(communication_client_id)

        # increment the communication client id
        self.communication_client_id += 1

        # releases the communication client id lock
        self.communication_client_id_lock.release()

        # returns the communication client id string
        return communication_client_id_string

    def _get_decoded_request_contents(self, request):
        """
        Retrieves the decoded request contents from the original
        request.

        @type request: AbeculaRequest
        @param request: The request to be used in the decoding.
        @rtype: String
        @return: The decoded request contents.
        """

        # reads the contents of the request
        request_contents = request.read()

        # decodes the request contents, retrieving the decoded
        # request contents
        decoded_request_contents = self._decode(request_contents)

        # returns the decoded request contents
        return decoded_request_contents

    def _set_encoded_request_contents(self, request, request_contents, status_code = 200):
        """
        Sets the encoded request contents into the request.

        @type request: AbeculaRequest
        @param request: The request to be used in the encoding.
        @type request_contents: String
        @param request_contents: The decoded request contents.
        @type status_code: int
        @param status_code: The status code to be set in the request.
        """

        # encodes the request contents, retrieving the encoded
        # request contents
        encoded_request_contents = self._encode(request_contents)

        # sets the status code
        request.status_code = status_code

        # writes the response
        request.write(encoded_request_contents)

    def _get_values(self, base_value):
        """
        Retrieves a list of values for the given value.
        It takes into account if the current value is
        a list or a single value.

        @type base_value: Object
        @param base_value: The base value to be used to retrieve
        the list of values.
        @rtype: List
        @return: The list of values, retrieved from the base value.
        """

        # retrieves the base value type
        base_value_type = type(base_value)

        # in case the base value is of type list
        if base_value_type == types.ListType:
            # sets the values as the base value
            values = base_value
        else:
            # sets the values as a list with the
            # base value being the only element
            values = [base_value]

        # returns the values
        return values

    def _remove_service_connection_structures(self, service_connection):
        """
        Removes the internal structures referring the
        given service connection.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection to be used
        in the "removal".
        """

        # retrieves the communication push plugin
        communication_push_plugin = self.main_service_abecula_communication_push_handler_plugin.communication_push_plugin

        # retrieves the communication client id for the service connection
        communication_client_id = self.service_connection_communication_client_id_map[service_connection]

        # retrieves the communication handler information
        communication_handler_information = communication_push_plugin.get_communication_handler_information(communication_client_id)

        # retrieves the communication names from the communication handler information
        communication_names = communication_handler_information[COMMUNICATION_NAMES_VALUE]

        # iterates over all the communication names to remove
        # the service connection information
        for communication_name in communication_names:
            # creates the service connection name tuple
            service_connection_name_tuple = (service_connection, communication_name)

            # in case the service connection name tuple exists in the service connection
            # name communication handler map
            if service_connection_name_tuple in self.service_connection_name_communication_handler_map:
                # removes the service connection name from the service connection name communication handler map
                del self.service_connection_name_communication_handler_map[service_connection_name_tuple]

        # retrieves the communication profile names from the communication handler information
        communication_profile_names = communication_handler_information[COMMUNICATION_PROFILE_NAMES_VALUE]

        # iterates over all the communication profile names to unload
        # the service connection information
        for communication_profile_name in communication_profile_names:
            # creates the service connection profile name tuple
            service_connection_profile_name_tuple = (service_connection, communication_profile_name)

            # removes the service connection name from the service connection profile name communication handler map
            del self.service_connection_profile_name_communication_handler_map[service_connection_profile_name_tuple]

        # removes the service connection from the service connection communication client id map
        del self.service_connection_communication_client_id_map[service_connection]

    def _structure_notification(self, notification, communication_name):
        """
        Structures the notification into a map.

        @type notification: PushNotification
        @param notification: The push notification to be structured.
        @type communication_name: String
        @param communication_name: The communication name.
        @rtype: Dictionary
        @return: The structured notification in map format.
        """

        # retrieves the notification attributes
        message = notification.get_message()
        sender_id = notification.get_sender_id()
        guid = notification.get_guid()
        sequence_id = notification.get_sequence_id()

        # creates the complete message contents from the original message contents
        message_contents = {
            COMMUNICATION_NAME_VALUE : communication_name,
            COMMUNICATION_CLIENT_ID_VALUE : sender_id,
            GUID_VALUE : guid,
            SEQUENCE_ID_VALUE : sequence_id,
            MESSAGE_CONTENTS_VALUE : message
        }

        # returns the message contents
        return message_contents

    def _encode_notification(self, notification, communication_name):
        """
        Encodes the given notification into the required
        output format.

        @type notification: PushNotification
        @param notification: The push notification to be encoded.
        @type communication_name: String
        @param communication_name: The communication name.
        @rtype: String
        @return: The encoded notification in string format.
        """

        # structures the notification retrieving the message contents
        message_contents = self._structure_notification(notification, communication_name)

        # encodes the message contents
        message_contents_encoded = self._encode(message_contents)

        # returns the message contents encoded
        return message_contents_encoded

    def _encode(self, value):
        """
        Encodes the given value into json notation.

        @type value: Object
        @param value: The value to be encoded into json notation.
        @rtype: String
        @return: The value encoded in json notation.
        """

        # retrieves the json plugin
        json_plugin = self.main_service_abecula_communication_push_handler_plugin.json_plugin

        # dumps the json from the value contents, retrieving
        # the encoded value
        encoded_value = json_plugin.dumps(value)

        # returns the encoded value
        return encoded_value

    def _decode(self, value):
        """
        Decodes the given json value into an object.

        @type value: String
        @param value: The value to be decoded from json notation.
        @rtype: Object
        @return: The decoded object value.
        """

        # retrieves the json plugin
        json_plugin = self.main_service_abecula_communication_push_handler_plugin.json_plugin

        # loads the json from the value, retrieving
        # the decoded value
        decoded_value = json_plugin.loads(value)

        # returns the decoded value
        return decoded_value
