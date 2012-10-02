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

import time
import threading

import exceptions

DEFAULT_UPDATE_POLL_TIMEOUT = 0.5
""" The default update poll timeout """

DEFAULT_UPDATE_WAIT_TIMEOUT = 5.0
""" The default update wait timeout """

VALID_STATUS_CODE = 200
""" The valid status code """

class MvcCommunicationHandler:
    """
    The mvc communication handler class.
    The concept of communication in the mvc context is expressed
    through long polling.
    A communication connection is the virtual connection created
    between peers through various http request.
    A communication element is the three element tuple for connection,
    request and timestamp.
    """

    mvc_plugin = None
    """ The mvc plugin """

    connection_name_connections_map = {}
    """ The map associating the connection
    name with the connections """

    service_connection_connections_map = {}
    """ The map associating the service
    connection with the connections """

    connection_complete_information_connection_map = {}
    """ The map associating the connection
    complete information with the connection """

    connection_queue = []
    """ The queue that holds the connections
    with messages ready to be processed """

    connection_queue_lock = None
    """ The lock that controls the access to
    the connection (messages) queue """

    connection_queue_event = None
    """ The event that controls the existence
    of new messages in the connection queue """

    connection_processing_thread = None
    """ The thread that controls the processing
    of the messages """

    def __init__(self, mvc_plugin):
        """
        Constructor of the class.

        @type mvc_plugin: MvcPlugin
        @param mvc_plugin: The mvc plugin
        """

        self.mvc_plugin = mvc_plugin

        self.connection_name_connections_map = {}
        self.service_connection_connections_map = {}
        self.connection_complete_information_connection_map = {}

        self.connection_queue = []
        self.connection_queue_lock = threading.RLock()
        self.connection_queue_event = threading.Event()

        self.connection_processing_thread = ConnectionProcessingThread(self)

    def handle_request(self, request, data_handler_method, connection_changed_handler_method, connection_name):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        @type data_handler_method: Method
        @param data_handler_method: The method for data handling.
        @type connection_changed_handler_method: Method
        @param connection_changed_handler_method: The method for
        connection changed handling.
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
            raise exceptions.InvalidCommunicationCommandException(None, 406)

        # creates the process method name
        process_method_name = "process_" + command

        # in case the process method does not exists
        if not hasattr(self, process_method_name):
            # raises the invalid communication command exception
            raise exceptions.InvalidCommunicationCommandException(command, 406)

        # retrieves the process method for the given method
        process_method = getattr(self, process_method_name)

        return process_method(request, data_handler_method, connection_changed_handler_method, connection_name)

    def process_connect(self, request, data_handler_method, connection_changed_handler_method, connection_name):
        # retrieves the random plugin
        random_plugin = self.mvc_plugin.random_plugin

        # retrieves the service connection
        service_connection = request.get_service_connection()

        # generates a new connection id
        connection_id = random_plugin.generate_random_md5_string()

        # creates a new communication connection from the service connection
        communication_connection = CommunicationConnection(self, connection_id, connection_name, service_connection)

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
            raise exceptions.CommunicationCommandException("no communication connection available")

        # sets the request as delayed (for latter writing)
        # and sets the status code as valid
        request.delayed = True
        request.status_code = VALID_STATUS_CODE

        # calculates the target time for timeout of the connection
        # element message
        current_time = time.time()
        target_time = current_time + DEFAULT_UPDATE_WAIT_TIMEOUT

        # creates the communication element tuple and adds it
        # to the connection elements queue
        communication_element = (communication_connection, request, target_time)
        self.connection_processing_thread.add_queue(communication_element)

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

    def send_broadcast_message(self, connection_name, message):
        """
        Sends a broadcast message to all the clients in the connection
        with the given name.

        The usage of this method implies that no security measured will
        be applied to the message (public message).

        @type connection_name: String
        @param connection_name: The name of the connection to be used
        to send the message.
        @type message: String
        @param message: The message to be sent in broadcast mode.
        """

        # retrieves the communication connections
        communication_connections = self.get_connections_by_connection_name(connection_name)

        # iterates over all the communication connections to send
        # the message into their queues (all queues allowed)
        for communication_connection in communication_connections:
            # adds the message to the communication connection queue
            communication_connection.add_message_queue(message)

    def start_processing(self):
        """
        Starts processing the various communication
        connection messages.
        This method launches the thread for message processing.
        """

        # starts the connection processing thread
        self.connection_processing_thread.start()

    def stop_processing(self):
        """
        Stops processing the various communication
        connection messages.
        This method stops the thread for message processing.
        """

        # sets the stop flag in the connection processing thread
        self.connection_processing_thread.stop_flag = True

        # sets the connection queue event
        self.connection_queue_event.set()

    def add_connection_queue(self, connection):
        # acquires the connection queue lock
        self.connection_queue_lock.acquire()

        try:
            # adds the connection to the connection queue
            self.connection_queue.append(connection)

            # sets the connection queue event
            self.connection_queue_event.set()
        finally:
            # releases the connection queue lock
            self.connection_queue_lock.release()

    def pop_connection_queue(self):
        # acquires the connection queue lock
        self.connection_queue_lock.acquire()

        try:
            # saves the queue in the pop queue
            pop_queue = self.connection_queue

            # clears the current connection queue
            self.connection_queue = []

            # clears the connection queue event
            self.connection_queue_event.clear()
        finally:
            # releases the connection queue lock
            self.connection_queue_lock.release()

        # returns the pop queue
        return pop_queue

    def _write_message(self, request, communication_connection, result_message):
        # retrieves the json plugin
        json_plugin = self.mvc_plugin.json_plugin

        # serializes the result message
        serialized_result_message = communication_connection.serialize_message(result_message, json_plugin)

        # writes the serialized result message to the request
        request.write(serialized_result_message)

    def _get_connection(self, request, connection_name):
        """
        Retrieves the communication connection for the
        given request (to use the id of it) and connection
        name.

        @type request: HttpRequest
        @param request: The http request to be used to retrieve
        the id.
        @type connection_name: Srring
        @param connection_name: The name of the connection to be
        retrieved.
        @rtype: CommunicationConnection
        @return: The communication connection to be retrieved.
        """

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
        self.__remove_communication_connection_name_map(communication_connection)
        self.__remove_communication_service_connection_map(communication_connection)
        self.__unset_communication_connection_complete_information_map(communication_connection)

    def __add_communication_connection_name_map(self, communication_connection):
        # retrieves the connection name
        connection_name = communication_connection.get_connection_name()

        if not connection_name in self.connection_name_connections_map:
            self.connection_name_connections_map[connection_name] = []

        # retrieves the connection list from the connection name connections map
        # and adds the communication connection to the connections list
        connections_list = self.connection_name_connections_map[connection_name]
        connections_list.append(communication_connection)

    def __add_communication_service_connection_map(self, communication_connection):
        # retrieves the service connection
        service_connection = communication_connection.get_service_connection()

        if not service_connection in self.service_connection_connections_map:
            self.service_connection_connections_map[service_connection] = []

        # retrieves the connection list from the service connection connections map
        # and adds the communication connection to the connections list
        connections_list = self.service_connection_connections_map[service_connection]
        connections_list.append(communication_connection)

    def __set_communication_connection_complete_information_map(self, communication_connection):
        # retrieves the connection complete information
        connection_complete_information = communication_connection.get_connection_complete_information()

        # set the communication connection in the connection complete information connection map
        self.connection_complete_information_connection_map[connection_complete_information] = communication_connection

    def __remove_communication_connection_name_map(self, communication_connection):
        # retrieves the connection name
        connection_name = communication_connection.get_connection_name()

        # retrieves the connection list from the connection name connections map
        # and removes the communication connection from the connections list
        connections_list = self.connection_name_connections_map[connection_name]
        connections_list.remove(communication_connection)

        # in case the connections list is empty
        if not connections_list:
            # removes the connection from the connection name connections map
            del self.connection_name_connections_map[connection_name]

    def __remove_communication_service_connection_map(self, communication_connection):
        # retrieves the service connection
        service_connection = communication_connection.get_service_connection()

        # retrieves the connection list from the service connection connections map
        # and remove the communication connection from the connections list
        connections_list = self.service_connection_connections_map[service_connection]
        connections_list.remove(communication_connection)

        # in case the connections list is empty
        if not connections_list:
            # removes the connection from the service connection connections map
            del self.service_connection_connections_map[service_connection]

    def __unset_communication_connection_complete_information_map(self, communication_connection):
        # retrieves the connection complete information
        connection_complete_information = communication_connection.get_connection_complete_information()

        # unsets the communication connection in the connection complete information connection map
        del self.connection_complete_information_connection_map[connection_complete_information]

class ConnectionProcessingThread(threading.Thread):
    """
    Thread that controls the processing of "new"
    messages in the communication connections.
    """

    communication_handler = None
    """ The communication handler """

    stop_flag = False
    """ Flag controlling the execution of the thread """

    processing_queue = []
    """ The processing queue """

    processing_map = []
    """ The processing map """

    timestamp_list = []
    """ The map with the ordered timestamps """

    timestamp_map = {}
    """ The map associating the timestamp with the connection element """

    processing_queue_lock = None
    """ the processing queue lock """

    def __init__(self, communication_handler):
        """
        Constructor of the class.

        @type communication_handler: MvcCommunicationHandler
        @param communication_handler: The communication handler reference.
        """

        threading.Thread.__init__(self)

        self.communication_handler = communication_handler

        self.processing_queue = []
        self.processing_map = {}
        self.timestamp_list = []
        self.timestamp_map = {}

        self.processing_queue_lock = threading.RLock()

    def run(self):
        # retrieves the connection queue event
        connection_queue_event = self.communication_handler.connection_queue_event

        # unsets the stop flag
        self.stop_flag = False

        # iterates continuously
        while True:
            # in case the stop flag is set
            if self.stop_flag:
                # breaks the loop
                break

            # acquires the processing queue lock
            self.processing_queue_lock.acquire()

            try:
                # pops the "current" connection queue from the communication handler
                connection_queue = self.communication_handler.pop_connection_queue()
            finally:
                # releases the processing queue lock
                self.processing_queue_lock.release()

            # iterates over the connection queue "connections"
            for communication_connection in connection_queue:
                # retrieves the communication element from the processing
                # map using the connection and processes them
                communication_elements = self.processing_map.get(communication_connection, [])
                self.process_communication_elements(communication_elements)

            # retrieves the "overflown" communication elements
            # and processes them
            communication_elements = self.get_overflown_communication_elements()
            self.process_communication_elements(communication_elements)

            # waits for the connection queue event
            connection_queue_event.wait(DEFAULT_UPDATE_POLL_TIMEOUT)

    def process_communication_elements(self, communication_elements):
        # starts the removal list (for communication
        # element removal)
        removal_list = []

        # iterates over all the communication element in
        # the communication elements list
        for communication_element in communication_elements:
            # processes the communication element
            self._process_element(communication_element)

            # adds the communication element to the removal
            # list for later removal
            removal_list.append(communication_element)

        # iterates over all the communication elements
        # in the removal list
        for communication_element in removal_list:
            # removes the communication element from the queue
            self.remove_queue(communication_element)

    def get_overflown_communication_elements(self):
        # retrieves the current timestamp
        current_timestamp = time.time()

        # starts the overflown communication elements list
        overflown_communication_elements = []

        # iterates over all the timestamps in
        # timestamp list
        for timestamp in self.timestamp_list:
            # in case the current timestamp is
            # smaller than the timestamp in iteration
            if current_timestamp < timestamp:
                # breaks the loop
                break

            # retrieves the communication element for the
            # timestamp in iteration
            communication_elements = self.timestamp_map[timestamp]

            # iterates over all the communication elements
            # to add them to the overflown communication
            # elements
            for communication_element in communication_elements:
                # adds the communication element to the overflown
                # communication elements
                overflown_communication_elements.append(communication_element)

        # returns the overflown communication elements
        return overflown_communication_elements

    def add_queue(self, communication_element):
        # acquires the processing queue lock
        self.processing_queue_lock.acquire()

        try:
            # unpacks the communication element
            communication_connection, _request, target_timestamp = communication_element

            # in case the target timestamp is not yet present
            # in the timestamp list
            if not target_timestamp in self.timestamp_list:
                # adds the target timestamp to the timestamp
                # list and re-sorts the list
                self.timestamp_list.append(target_timestamp)
                self.timestamp_list.sort()

            # retrieves the communication elements list for the target
            # timestamp (if any) and adds the communication element to the list
            communication_elements = self.timestamp_map.get(target_timestamp, [])
            communication_elements.append(communication_element)
            self.timestamp_map[target_timestamp] = communication_elements

            # retrieves the communication elements list for the communication
            # connection (if any) and adds the communication element to the list
            communication_elements = self.processing_map.get(communication_connection, [])
            communication_elements.append(communication_element)
            self.processing_map[communication_connection] = communication_elements

            # adds the communication element to the processing queue
            self.processing_queue.append(communication_element)

            # in case the communication connection message queue is not empty
            # processes the communication elements (flushes queue)
            not communication_connection.is_empty() and self.process_communication_elements(communication_elements)
        finally:
            # releases the processing queue lock
            self.processing_queue_lock.release()

    def remove_queue(self, communication_element):
        # acquires the processing queue lock
        self.processing_queue_lock.acquire()

        try:
            # in case the communication element is not present
            # in the processing queue (possible add and remove)
            if not communication_element in self.processing_queue:
                # returns immediately
                return

            # unpacks the communication element
            communication_connection, request, target_timestamp = communication_element

            # retrieves the service connection from the request and
            # checks if the service connection (data connection) is still open
            service_connection = request.service_connection
            service_connection_is_open = service_connection.is_open()

            # retrieves the communication elements associated with the
            # target timestamp and removes the current communication
            # element from the communication elements
            communication_elements = self.timestamp_map[target_timestamp]
            communication_elements.remove(communication_element)

            # in case the communication elements list is empty
            # it should be removed (house-keeping)
            if not communication_elements:
                # removes the communication elements list
                # reference from the timestamp map (it's empty)
                del self.timestamp_map[target_timestamp]

                # removes the target timestamp from the timestmap
                # list (no more elements for the target timestamp)
                self.timestamp_list.remove(target_timestamp)

            # retrieves the communication elements associated with the
            # communication connection and removes the current communication
            # element from the communication elements
            communication_elements = self.processing_map[communication_connection]
            communication_elements.remove(communication_element)

            # in case the communication elements list is empty
            # it should be removed (house-keeping)
            if not communication_elements:
                # removes the communication elements list
                # reference from the processing map (it's empty)
                del self.processing_map[communication_connection]

                # in case the service connection is
                # not open anymore
                if not service_connection_is_open:
                    # removes the communication connection (no more communication elements)
                    self.communication_handler._remove_communication_connection(communication_connection)

            # removes the communication element from the "main"
            # processing queue
            self.processing_queue.remove(communication_element)
        finally:
            # releases the processing queue lock
            self.processing_queue_lock.release()

    def _process_element(self, element):
        # unpacks the element into the communication connection the request
        # and the target timestamp
        communication_connection, request, _target_timestamp = element

        # retrieves the request elements
        http_client_service_handler = request.http_client_service_handler
        service_connection = request.service_connection

        # checks if the service connection (data connection) is still open
        service_connection_is_open = service_connection.is_open()

        # in case the service connection is
        # not open anymore
        if not service_connection_is_open:
            # returns immediately (no need to write
            # in a closed connection)
            return True

        # retrieves the message queue
        message_queue = communication_connection.pop_message_queue()

        # writes the message queue into the message and processes
        # the request in the http client service handler (this represents
        # the final part of the delayed processing of the request)
        self.communication_handler._write_message(request, communication_connection, message_queue)
        http_client_service_handler.process_request(request, service_connection)

        # returns true (the element should be removed)
        return True

class CommunicationConnection:
    """
    The communication connection class.
    """

    communication_handler = None
    """ The communication handler """

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

    def __init__(self, communication_handler, connection_id, connection_name, service_connection):
        """
        Constructor of the class.

        @type communication_handler: MvcCommunicationHandler
        @param communication_handler: The communication handler (manager).
        @type connection_id: String
        @param connection_id: The identifier of the connection.
        @type connection_name: String
        @param connection_name: The name of the connection.
        @type service_connection: ServiceConnection
        @param service_connection: The service connection for the connection.
        """

        self.communication_handler = communication_handler
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

        try:
            # adds the message to the message queue
            self.message_queue.append(message)

            # sets the message queue event
            self.message_queue_event.set()

            # adds the current connection to the connection queue
            self.communication_handler.add_connection_queue(self)
        finally:
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

        try:
            # saves the queue in the pop queue
            pop_queue = self.message_queue

            # clears the current message queue
            self.message_queue = []

            # clears the message queue event
            self.message_queue_event.clear()
        finally:
            # releases the message queue lock
            self.message_queue_lock.release()

        # returns the pop queue
        return pop_queue

    def is_empty(self):
        """
        Checks if the internal message queue is empty.

        @rtype: bool
        @return: The result of the testing of the internal
        message queue.
        """

        # retrieves the message queue length for checking
        # it the message queue is empty
        message_queue_length = len(self.message_queue)
        message_queue_is_empty = message_queue_length == 0

        # return the result of the message queue empty test
        return message_queue_is_empty

    def get_connection_complete_information(self):
        """
        Retrieves the connection complete information.

        @rtype: Tuple
        @return: The connection complete information.
        """

        return (
            self.connection_id,
            self.connection_name
        )

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
