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

import web_mvc_exceptions

DEFAULT_UPDATE_WAIT_TIMEOUT = 5.0
""" The default update wait timeout """

class WebMvcCommunicationHandler:
    """
    The web mvc communication handler class.
    """

    web_mvc_plugin = None
    """ The web mvc plugin """

    connection_name_connections_map = {}
    """ The map associating the connection name with the connections """

    service_connection_connections_map = {}
    """ The map associating the service connection with the connections """

    connection_complete_information_connection_map = {}
    """ The map associating the connection complete information with the connection """

    def __init__(self, web_mvc_plugin):
        """
        Constructor of the class.

        @type web_mvc_plugin: WebMvcPlugin
        @param web_mvc_plugin: The web mvc plugin
        """

        self.web_mvc_plugin = web_mvc_plugin

        self.connection_name_connections_map = {}
        self.service_connection_connections_map = {}
        self.connection_complete_information_connection_map = {}

    def handle_request(self, request, data_handler_method, connection_changed_handler_method, connection_name):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        @type data_handler_method: Method
        @param data_handler_method: The method for data handling.
        @type connection_changed_handler_method: Method
        @param connection_changed_handler_method: The method for connection changed handling.
        @type connection_name: String
        @param connection_name: The name of the connection.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the request command
        command = request.get_attribute("command")

        # in case the command is not defined
        if not command:
            # raises the invalid communication command exception
            raise web_mvc_exceptions.InvalidCommunicationCommandException(None, 406)

        # creates the process method name
        process_method_name = "process_" + command

        # in case the process method does not exists
        if not hasattr(self, process_method_name):
            # raises the invalid communication command exception
            raise web_mvc_exceptions.InvalidCommunicationCommandException(command, 406)

        # retrieves the process method for the given method
        process_method = getattr(self, process_method_name)

        return process_method(request, data_handler_method, connection_changed_handler_method, connection_name)

    def process_connect(self, request, data_handler_method, connection_changed_handler_method, connection_name):
        # retrieves the random plugin
        random_plugin = self.web_mvc_plugin.random_plugin

        # retrieves the service connection
        service_connection = request.get_service_connection()

        # generates a new connection id
        connection_id = random_plugin.generate_random_md5_string()

        # creates a new communication connection from the service connection
        communication_connection = CommunicationConnection(connection_id, connection_name, service_connection)

        # adds the communication connection
        self._add_communication_connection(communication_connection)

        # writes the success message
        self._write_message(request, communication_connection, "success")

        # returns true (valid)
        return True

    def process_disconnect(self, request, data_handler_method, connection_changed_handler_method, connection_name):
        # returns true (valid)
        return True

    def process_update(self, request, data_handler_method, connection_changed_handler_method, connection_name):
        # tries to retrieve the communication connection
        communication_connection = self._get_connection(request, connection_name)

        # in case no communication connection is available
        if not communication_connection:
            # raises the communication command exception
            raise web_mvc_exceptions.CommunicationCommandException("no communication connection available")

        # iterates continuously
        while True:
            # retrieves the message queue
            message_queue = communication_connection.pop_message_queue()

            # in case the message queue is valid
            # and not empty
            if message_queue:
                # breaks the loop
                break
            # otherwise should wait for a
            # message to become available
            else:
                # retrieves the message queue event
                message_queue_event = communication_connection.message_queue_event

                # waits for the message queue event
                communication_connection.message_queue_event.wait(DEFAULT_UPDATE_WAIT_TIMEOUT)

                # in case the message queue event is not set
                if not message_queue_event.isSet():
                    # breaks the loop
                    break

        # writes the message queue into the message
        self._write_message(request, communication_connection, message_queue)

        # returns true (valid)
        return True

    def process_data(self, request, data_handler_method, connection_changed_handler_method, connection_name):
        # returns true (valid)
        return True

    def get_connections_by_connection_name(self, connection_name):
        """
        Retrieves the connections for the given connection
        name.

        @type connection_name: String
        @param connection_name: The connection name to retrieve
        the connections.
        @rtype: List
        @return: The connections for the given connection name.
        """

        return self.connection_name_connections_map.get(connection_name, [])

    def send_broadcast_communication_message(self, connection_name, message):
        """
        Sends a broadcast message to all the clients in the connection
        with the given name.

        @type connection_name: String
        @param connection_name: The name of the connection to be used
        to send the message.
        @type message: String
        @param message: The message to be sent in broadcast mode.
        """

        # retrieves the communication connections
        communication_connections = self.get_connections_by_connection_name(connection_name)

        # iterates over all the communication connections
        for communication_connection in communication_connections:
            # adds the message to the communication connection queue
            communication_connection.add_message_queue(message)

    def _write_message(self, request, communication_connection, result_message):
        # retrieves the json plugin
        json_plugin = self.web_mvc_plugin.json_plugin

        # serializes the result message
        serialized_result_message = communication_connection.serialize_message(result_message, json_plugin)

        # writes the serialized result message to the request
        request.write(serialized_result_message)

    def _get_connection(self, request, connection_name):
        # retrieves the request connection id
        connection_id = request.get_attribute("id")

        # creates the connection complete information tuple
        connection_complete_information = (connection_id, connection_name)

        # tries to retrieve the communication connection from the connection complete
        # information connection map
        communication_connection = self.connection_complete_information_connection_map.get(connection_complete_information, None)

        # returns the communication connection
        return communication_connection

    def _add_communication_connection(self, communication_connection):
        self.__add_communication_connection_name_map(communication_connection)
        self.__add_communication_service_connection_map(communication_connection)
        self.__set_communication_connection_complete_information_map(communication_connection)

    def _remove_communication_connection(self, communication_connection):
        pass

    def __add_communication_connection_name_map(self, communication_connection):
        # retrieves the connection name
        connection_name = communication_connection.get_connection_name()

        if not connection_name in self.connection_name_connections_map:
            self.connection_name_connections_map[connection_name] = []

        # retrieves the connection list from the connection name connections map
        connections_list = self.connection_name_connections_map[connection_name]

        # adds the communication connection to the connections list
        connections_list.append(communication_connection)

    def __add_communication_service_connection_map(self, communication_connection):
        # retrieves the service connection
        service_connection = communication_connection.get_service_connection()

        if not service_connection in self.service_connection_connections_map:
            self.service_connection_connections_map[service_connection] = []

        # retrieves the connection list from the service connection connections map
        connections_list = self.service_connection_connections_map[service_connection]

        # adds the communication connection to the connections list
        connections_list.append(communication_connection)

    def __set_communication_connection_complete_information_map(self, communication_connection):
        # retrieves the connection complete information
        connection_complete_information = communication_connection.get_connection_complete_information()

        # set the communication connection in the connection complete information connection map
        self.connection_complete_information_connection_map[connection_complete_information] = communication_connection

class CommunicationConnection:
    """
    The communication connection class.
    """

    connection_id = None
    """ The connection id """

    connection_name = None
    """ The connection name """

    service_connection = None
    """ The service connection for the connection """

    message_queue = []
    """ The queue of messages pending to be sent """

    message_queue_lock = None
    """ The lock for the access to the message queue """

    message_queue_event = None
    """ The event about the new message operation in the message queue """

    def __init__(self, connection_id, connection_name, service_connection):
        """
        Constructor of the class.

        @type connection_id: String
        @param connection_id: The identifier of the connection.
        @type connection_name: String
        @param connection_name: The name of the connection.
        @type service_connection: ServiceConnection
        @param service_connection: The service connection for the connection.
        """

        self.connection_id = connection_id
        self.connection_name = connection_name
        self.service_connection = service_connection

        self.message_queue = []
        self.message_queue_lock = threading.RLock()
        self.message_queue_event = threading.Event()

    def serialize_message(self, result_message, serializer):
        """
        Serializes the given message, using the given
        serializer method.
        The serializartion take into account the current connection
        information.

        @type result_message: String
        @param result_message: The message to be serialized.
        @type serializer: Method
        @param serializer: The serializer method to be used
        in the serialization.
        """

        # creates the map for the message
        message_map = {}

        # sets the message map values
        message_map["id"] = self.connection_id
        message_map["name"] = self.connection_name
        message_map["result"] = result_message

        # serializes the message map
        serialized_message_map = serializer.dumps(message_map)

        # returns the serialized message map
        return serialized_message_map

    def add_message_queue(self, message):
        """
        Adds a message to the connection message queue.

        @type message: String
        @param message: The message to be added to the
        connection message queue.
        """

        # acquires the message queue lock
        self.message_queue_lock.acquire()

        # adds the message to the message queue
        self.message_queue.append(message)

        # sets the message queue event
        self.message_queue_event.set()

        # releases the message queue lock
        self.message_queue_lock.release()

    def pop_message_queue(self):
        """
        Pops the message queue, retrieving all the messages
        from the queue and cleaning the queue after.

        @rtype: List
        @return: The popped queue.
        """

        # acquires the message queue lock
        self.message_queue_lock.acquire()

        # saves the queue in the pop queue
        pop_queue = self.message_queue

        # clears the current message queue
        self.message_queue = []

        # clears the message queue event
        self.message_queue_event.clear()

        # releases the message queue lock
        self.message_queue_lock.release()

        # returns the pop queue
        return pop_queue

    def get_connection_complete_information(self):
        """
        Retrieves the connection complete information.

        @rtype: Tuple
        @return: The connection complete information.
        """

        return (self.connection_id, self.connection_name)

    def get_connection_id(self):
        """
        Retrieves the connection id.

        @rtype: String
        @return: The connection id.
        """

        return self.connection_id

    def set_connection_id(self, connection_id):
        """
        Sets the connection name.

        @type connection_id: String
        @param connection_id: The connection id.
        """

        self.connection_id = connection_id

    def get_connection_name(self):
        """
        Retrieves the connection name.

        @rtype: String
        @return: The connection name.
        """

        return self.connection_name

    def set_connection_name(self, connection_name):
        """
        Sets the connection name.

        @type connection_name: String
        @param connection_name: The connection name.
        """

        self.connection_name = connection_name

    def get_service_connection(self):
        """
        Retrieves the service connection.

        @rtype: ServiceConnection
        @return: The service connection.
        """

        return self.service_connection

    def set_service_connection(self, service_connection):
        """
        Sets the service connection.

        @type service_connection: ServiceConnection
        @param service_connection: The service connection.
        """

        self.service_connection = service_connection
