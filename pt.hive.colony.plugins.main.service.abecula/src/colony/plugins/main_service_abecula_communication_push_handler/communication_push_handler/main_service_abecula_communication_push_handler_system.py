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
import threading

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

INFORMATION_VALUE = "information"
""" The information value """

INFORMATION_ITEM_VALUE = "information_item"
""" The information item value """

INFORMATION_KEY_VALUE = "information_key"
""" The information key value """

COMMUNICATION_VALUE = "communication"
""" The communication value """

COMMUNICATION_HANDLER_VALUE = "communication_handler"
""" The communication handler value """

class MainServiceAbeculaCommunicationPushHandler:
    """
    The main service abecula communication push handler class.
    """

    main_service_abecula_communication_push_handler_plugin = None
    """ The main service abecula communication push handler plugin """

    service_connection_name_communication_handler_map = {}
    """ The map associating a service connection and communication name tuple with the communication handler """

    service_connection_communication_client_id_map = {}
    """ The map associating a service connection with the communication client id """

    communication_client_id = 0
    """ The communication client id """

    communication_client_id_lock = None
    """ The lock to control communication client id creation """

    def __init__(self, main_service_abecula_communication_push_handler_plugin):
        """
        Constructor of the class.

        @type main_service_abecula_communication_push_handler_plugin: MainServiceAbeculaCommunicationPushHandlerPlugin
        @param main_service_abecula_communication_push_handler_plugin: The main service abecula communication push handler plugin.
        """

        self.main_service_abecula_communication_push_handler_plugin = main_service_abecula_communication_push_handler_plugin

        self.service_connection_name_communication_handler_map = {}
        self.service_connection_communication_client_id_map = {}

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

        # handles the operation
        operation_handler_method(request, communication_push_plugin)

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

        # sets the encoded request contents
        self._set_encoded_request_contents(request, {RESULT_VALUE : SUCCESS_VALUE, COMMUNICATION_CLIENT_ID_VALUE : communication_client_id})

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

        # sets the encoded request contents
        self._set_encoded_request_contents(request, {RESULT_VALUE : SUCCESS_VALUE})

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
        communication_names = self._get_communication_names(communication_name)

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

        # sets the encoded request contents
        self._set_encoded_request_contents(request, {RESULT_VALUE : SUCCESS_VALUE})

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
        communication_names = self._get_communication_names(communication_name)

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

        # sets the encoded request contents
        self._set_encoded_request_contents(request, {RESULT_VALUE : SUCCESS_VALUE})

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

        # creates the complete message contents from the original message contents
        complete_message_contents = {COMMUNICATION_NAME_VALUE : communication_name,
                                     COMMUNICATION_CLIENT_ID_VALUE : communication_client_id,
                                     MESSAGE_CONTENTS_VALUE : message_contents}

        # encodes the complete message contents
        complete_message_contents_encoded = self._encode(complete_message_contents)

        # generates a new notification for the message contents and the communication client id
        notification = communication_push_plugin.generate_notification(complete_message_contents_encoded, communication_client_id)

        # sends the notification in broadcast mode
        communication_push_plugin.send_broadcast_notification(communication_name, notification)

        # sets the encoded request contents
        self._set_encoded_request_contents(request, {RESULT_VALUE : SUCCESS_VALUE})

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

        # in case the requested information is of type communication
        if information_item == COMMUNICATION_VALUE:
            information = communication_push_plugin.get_communication_information(information_key)
        # in case the requested information is of type communication handler
        elif information_item == COMMUNICATION_HANDLER_VALUE:
            information = communication_push_plugin.get_communication_handler_information(information_key)
        # in case the requested information is not valid
        else:
            # raises the invalid information item exception
            raise main_service_abecula_communication_push_handler_exceptions.InvalidInformationItem(information_item)

        # sets the encoded request contents
        self._set_encoded_request_contents(request, {RESULT_VALUE : SUCCESS_VALUE, INFORMATION_VALUE : information})

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

        def communication_handler(notification):
            """
            The "base" communication handler function.
            to be used in the generation of the communication handler.

            @type notification: PushNotification
            @param notification: The push notification to be sent.
            """

            # creates a new response
            response = service_handler.create_response()

            # sets the response properties
            response.set_operation_id("C124")
            response.set_operation_type(MESSAGE_VALUE)
            response.set_target(HANDLER_NAME)

            # retrieves the notification message
            notification_message = notification.get_message()

            # writes the notification message to the response
            response.write(notification_message)

            # sends the response to the service connection
            service_handler.send_response(service_connection, response)

        # returns the communication handler
        return communication_handler

    def _generate_communication_client_id(self):
        """
        Generates a new communication client id.

        @rtype: int
        @return: The generated communication client id.
        """

        # acquires the communication client id lock
        self.communication_client_id_lock.acquire()

        # retrieves the current communication client id
        communication_client_id = self.communication_client_id

        # increment the communication client id
        self.communication_client_id += 1

        # releases the communication client id lock
        self.communication_client_id_lock.release()

        # returns the communication client id
        return communication_client_id

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

    def _get_communication_names(self, communication_name):
        """
        Retrieves a list of communication names for the
        given communication name.

        @type communication_name: String
        @param communication_name: The name of the communication.
        @rtype: List
        @return: The list of communication names for the given
        communication name.
        """

        # retrieves the communication name type
        communication_name_type = type(communication_name)

        # in case the communication name is of type list
        if communication_name_type == types.ListType:
            # sets the communication names as the
            # communication names
            communication_names = communication_name
        else:
            # sets the communication names as a list
            # with the communication name item
            communication_names = [communication_name]

        # returns the communication names
        return communication_names

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

            # removes the service connection name from the service connection name communication handler map
            del self.service_connection_name_communication_handler_map[service_connection_name_tuple]

        # removes the service connection from the service connection communication client id map
        del self.service_connection_communication_client_id_map[service_connection]

    def _encode(self, value):
        # retrieves the json plugin
        json_plugin = self.main_service_abecula_communication_push_handler_plugin.json_plugin

        # dumps the json from the value contents, retrieving
        # the encoded value
        encoded_value = json_plugin.dumps(value)

        # returns the encoded value
        return encoded_value

    def _decode(self, value):
        # retrieves the json plugin
        json_plugin = self.main_service_abecula_communication_push_handler_plugin.json_plugin

        # loads the json from the value, retrieving
        # the decoded value
        decoded_value = json_plugin.loads(value)

        # returns the decoded value
        return decoded_value
