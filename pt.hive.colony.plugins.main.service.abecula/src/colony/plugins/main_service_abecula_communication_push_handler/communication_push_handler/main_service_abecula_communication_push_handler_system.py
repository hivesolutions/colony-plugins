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

import main_service_abecula_communication_push_handler_exceptions

HANDLER_NAME = "communication_push"
""" The handler name """

class MainServiceAbeculaCommunicationPushHandler:
    """
    The main service abecula communication push handler class.
    """

    main_service_abecula_communication_push_handler_plugin = None
    """ The main service abecula communication push handler plugin """

    service_connection_communication_handler_map = {}
    """ The map associating a service connection with the communication handler """

    def __init__(self, main_service_abecula_communication_push_handler_plugin):
        """
        Constructor of the class.

        @type main_service_abecula_communication_push_handler_plugin: MainServiceAbeculaCommunicationPushHandlerPlugin
        @param main_service_abecula_communication_push_handler_plugin: The main service abecula communication push handler plugin.
        """

        self.main_service_abecula_communication_push_handler_plugin = main_service_abecula_communication_push_handler_plugin

        self.service_connection_communication_handler_map = {}

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
        # retrieves the service connection
        service_connection = request.get_service_connection()

        # generates a communication handler for the given service connection
        generated_communication_handler = self.generate_handler(service_connection)

        # sets the generated communication handler in the service connection communication handler map
        self.service_connection_communication_handler_map[service_connection] = generated_communication_handler

        # adds a new communication handler
        communication_push_plugin.add_communication_handler("tobias", "nome_da_conexao", generated_communication_handler)

        # sets the status code
        request.status_code = 200

        # writes the response
        request.write("success")



        service_connection.connection_closed_handlers.append(self.handle_connection_closed)

    def handle_message(self, request, communication_push_plugin):
        pass

    def handle_disconnect(self, request, communication_push_plugin):
        # retrieves the service connection
        service_connection = request.get_service_connection()

        # retrieves the generated communication handler for the service connection
        generated_communication_handler = self.service_connection_communication_handler_map[service_connection]

        # removes the communication handler
        communication_push_plugin.remove_communication_handler("tobias", "nome_da_conexao", generated_communication_handler)

        # sets the status code
        request.status_code = 200

        # writes the response
        request.write("success")

    def handle_connection_closed(self, service_connection):
        # retrieves the communication push plugin
        communication_push_plugin = self.main_service_abecula_communication_push_handler_plugin.communication_push_plugin

        # retrieves the generated communication handler for the service connection
        generated_communication_handler = self.service_connection_communication_handler_map[service_connection]

        # removes the communication handler
        communication_push_plugin.remove_communication_handler("tobias", "nome_da_conexao", generated_communication_handler)

    def generate_handler(self, service_connection):
        """
        Generates a communication handler for the
        given request.

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
            response = service_connection.create_response()

            # sets the response properties
            response.set_operation_id("C12")
            response.set_operation_type("MESSAGE")
            response.set_target(HANDLER_NAME)

            # retrieves the notification message
            notification_message = notification.get_message()

            # writes the notification message to the response
            response.write(notification_message)

            # sends the response to the service connection
            service_connection.send_response(response)

        # returns the communication handler
        return communication_handler
