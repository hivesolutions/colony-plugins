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

import handlers.apn

import exceptions

DEFAULT_UPDATE_POLL_TIMEOUT = 0.5
""" The default update poll timeout, this value if
going to be used in the connection loop to update
the connection states (eg: return default value if
the wait timeout was reached) """

DEFAULT_UPDATE_WAIT_TIMEOUT = 5.0
""" The default update wait timeout, this value is
going to be used as the maximum time a connection
stays "waiting" for a response for the server """

VALID_STATUS_CODE = 200
""" The valid status code """

class MvcCommunicationHandler:
    """
    The mvc communication (handler) class.

    The concept of communication in the mvc context is expressed
    through long polling. Other systems may exist on top of the
    infra-structure using the modular approach.

    The connection name (abstract value) is a value that defined
    a domain for which messages are diffused (diffusion scope).

    A communication connection is a virtual connection created
    between peers through various http requests or any other proxy
    communication infra-structure. The communication connection may
    be identified by the connection name and the id of the connection,
    this value is considered the connection information.

    A communication element is a three element tuple for connection,
    request and (target) timestamp for timeout (maximum wait time).
    This communication element represents a request from the client
    and the (rest request) associated must be flushed or the else the
    client will remain waiting indefinitely.

    There are two types of queues in the communication sub-system, the
    message queue (for each connection) that contains the various messages
    pending to be sent for the connection and the connection queue (global
    wide) that contains the various connections with messages pending to
    be sent.
    """

    mvc_plugin = None
    """ The mvc plugin """

    connections_map = {}
    """ The map associating the connection name with
    the list of connections belonging to the domain """

    service_connections_map = {}
    """ The map associating the service connection
    (http connection) with the connections belonging
    to the it (multiplexing may exist) """

    connection_informations_map = {}
    """ The map associating the connection
    complete information with the connection """

    channels_map = {}
    """ The map associating the (complete) channel name with
    a list containing the various connection registered for
    them (useful for fast channel member accessing) """

    channels_map_i = {}
    """ The inverted map associating the various connections
    with lists containing the various channels for which they
    are registered (useful for unregistering connections) """

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

        self.connections_map = {}
        self.service_connections_map = {}
        self.connection_informations_map = {}
        self.channels_map = {}
        self.channels_map_i = {}

        self.connection_queue = []
        self.connection_queue_lock = threading.RLock()
        self.connection_queue_event = threading.Event()

        self.connection_processing_thread = ConnectionProcessingThread(self)

    def new_connection(self, connection_name, channels = ()):
        # retrieves the random plugin
        random_plugin = self.mvc_plugin.random_plugin

        # generates a new connection id, then uses it to create the
        # (communication) connection structure
        connection_id = random_plugin.generate_random_md5_string()
        connection = CommunicationConnection(
            self,
            connection_id,
            connection_name
        )

        # opens the connection, this should update the internal
        # structures and event handlers (connection start)
        connection.open()

        # adds the connection to the current internal structures
        # should include the multiple maps and lists
        self._add_connection(connection)

        # in case the complete set of channels has been successful
        # verified (authentication/validation process) can now
        # safely register the channels for the connection
        self._register_channels(connection, channels)

        # returns the connection that was just created, this means
        # that it was created successfully
        return connection

    def delete_connection(self, connection):
        # in case the connection is already closed returns immediately
        # avoids duplicated close operations
        if not connection.is_open(): return

        # closes the connection, this should update the internal
        # structures and event handlers (connection stop)
        connection.close()

        # removes the provided connection from the current internal
        # structure, this operation should "revert" the system to its
        # original state (without the connection)
        self._remove_connection(connection)

    def send(self, connection_name, message, channels = ("public",)):
        """
        Sends a unicast message to the clients that are registered
        for the channels in the connection with the given name.

        The usage of this method implies that a security layer secures
        the assigning of the various channels to the connections (private
        message).

        @type connection_name: String
        @param connection_name: The name of the connection to be used
        to send the message.
        @type message: String
        @param message: The message to be sent to the various defined
        channels (provided by argument)
        @type channels: Tuple
        @param channels: The various channels to be used for sending
        the message.
        """

        # iterates over all the channels to send the message and
        # retrieves the connection to be used to send the message
        for channel in channels:
            # creates the fully qualified name for the channel
            # by prepending the connection name to it and then
            # retrieves the complete set of connections registered
            # for the channel
            channel_fqn = connection_name + "/" + channel
            connections = self.channels_map.get(channel_fqn, [])

            # iterates over all the (communication) connections to send
            # the message into their queues (for the channel)
            for connection in connections: self.send_message(connection, message)

    def send_broadcast(self, connection_name, message):
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

        # retrieves the complete set of (communication) connections for
        # the current connection name
        connections = self.get_connections(connection_name)

        # iterates over all the (communication) connections to send
        # the message into their queues (for the channel)
        for connection in connections: self.send_message(connection, message)

    def send_message(self, connection, message):
        """
        Sends a message described as a string of characters into
        the provided connection.

        This methods should be able to abstract the caller method
        from the technical details of sending a message to a certain
        connection. The connection may assume different forms
        (eg: websockets, long polling, apn, etc.).

        @type connection: CommunicationConnection
        @param connection: The communication connection to be used
        for sending the provided message.
        @type message: String
        @param message: The message to be sent to the target connection
        it must be correctly serialized.
        """

        connection.send_message(message)

    def handle_request(self, request, delegate, connection_name):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        @type delegate: Object
        @param delegate: The object to be used to delegate
        operations associated with the communication changes.
        @type connection_name: String
        @param connection_name: The name of the connection.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the request command, this value should
        # identify the operation to be executed
        command = request.get_attribute("command")

        # in case the command is not defined raises the
        # invalid communication command exception
        if not command:
            raise exceptions.InvalidCommunicationCommandException(None, 406)

        # creates the process method name by appending the command name
        # to the base prefix process name
        process_method_name = "process_" + command

        # in case the process method does not exists raises
        # the invalid communication command exception
        if not hasattr(self, process_method_name):
            raise exceptions.InvalidCommunicationCommandException(command, 406)

        # retrieves the process method for the given method and calls it
        # with the request to be handled, the data handler method
        process_method = getattr(self, process_method_name)
        process_method(
            request,
            delegate,
            connection_name
        )
        return True

    def process_connect(self, request, delegate, connection_name):
        # retrieves the random plugin
        random_plugin = self.mvc_plugin.random_plugin

        # retrieves the service connection
        service_connection = request.get_service_connection()

        # generates a new connection id, then uses it to create the
        # (communication) connection structure
        connection_id = random_plugin.generate_random_md5_string()
        connection = CommunicationConnection(
            self,
            connection_id,
            connection_name,
            service_connection,
            delegate = delegate
        )

        # opens the connection, this should update the internal
        # structures and event handlers (connection start)
        connection.open()

        # adds the connection to the current internal structures
        # should include the multiple maps and lists
        self._add_connection(connection)

        # retrieves the complete sets of channels for which the
        # connection is going to be initially registered and
        # verifies them against the associated controller method
        channels = request.get_attribute("channels") or None
        channels = channels and channels.split(",") or ()
        for channel in channels:
            parameters = {
                "communication_handler" : self,
                "operation" : "channel",
                "channel" : channel
            }
            delegate.handle_changed(request, parameters)

        # in case the complete set of channels has been successful
        # verified (authentication/validation process) can now
        # safely register the channels for the connection
        self._register_channels(connection, channels)

        # writes the success message to the client end point to
        # notify it about the success
        self._write_message(request, connection, "success")

    def process_disconnect(self, request, delegate, connection_name):
        pass

    def process_update(self, request, delegate, connection_name):
        # tries to retrieve the (communication) connection
        # using the current request for it
        connection = self._get_connection(request, connection_name)

        # in case no (communication) connection is available raises
        # the communication command exception
        if not connection:
            raise exceptions.CommunicationCommandException("no communication connection available")

        # sets the request as delayed (for latter writing)
        # and sets the status code as valid
        request.set_delayed(True)
        request.set_status_code(VALID_STATUS_CODE)

        # calculates the target time for timeout of the connection
        # element message
        current_time = time.time()
        target_time = current_time + DEFAULT_UPDATE_WAIT_TIMEOUT

        # creates the communication element tuple and adds it
        # to the connection elements queue
        element = (connection, request, target_time)
        self.connection_processing_thread.add_queue(element)

    def process_data(self, request, delegate, connection_name):
        # tries to retrieve the (communication) connection
        # using the current request for it
        connection = self._get_connection(request, connection_name)

        # retrieves the data attribute, containing the data to be
        # handled and constructs the parameters map with it sending
        # it for data handling in the correct method
        data = request.get_attribute("data")
        parameters = {
            "communication_handler" : self,
            "operation" : "data",
            "data" : data
        }
        delegate.handle_data(request, parameters)

        # writes the success message to the client end point to
        # notify it about the success of the channel registration
        self._write_message(request, connection, "success")

    def process_channel(self, request, delegate, connection_name):
        # tries to retrieve the (communication) connection
        # using the current request for it
        connection = self._get_connection(request, connection_name)

        # retrieves the request channel attribute, the
        # one that the client want's to connect and verifies
        # the security of the registration by calling the changed
        # method with the appropriate parameters
        channel = request.get_attribute("channel")
        parameters = {
            "communication_handler" : self,
            "operation" : "channel",
            "channel" : channel
        }
        delegate.handle_changed(request, parameters)

        # in case the the  channel has been successful
        # verified (authentication/validation process) can now
        # safely register the channel for the connection
        self._register_channels(connection, (channel,))

        # writes the success message to the client end point to
        # notify it about the success of the channel registration
        self._write_message(request, connection, "success")

    def get_connections(self, connection_name):
        """
        Retrieves the connections for the given connection
        name.

        In case no connections exists or no connection is
        defined an empty structure is returned.

        @type connection_name: String
        @param connection_name: The connection name to retrieve
        the connections.
        @rtype: List
        @return: The connections for the given connection name.
        """

        return self.connections_map.get(connection_name, [])

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
            # adds the connection to the connection queue and
            # sets the connection queue event
            self.connection_queue.append(connection)
            self.connection_queue_event.set()
        finally:
            # releases the connection queue lock
            self.connection_queue_lock.release()

    def pop_connection_queue(self):
        # acquires the connection queue lock
        self.connection_queue_lock.acquire()

        try:
            # saves the queue in the pop queue, clears the
            # current connection queue and clears the
            # connection queue event
            pop_queue = self.connection_queue
            self.connection_queue = []
            self.connection_queue_event.clear()
        finally:
            # releases the connection queue lock
            self.connection_queue_lock.release()

        # returns the pop queue
        return pop_queue

    def _write_message(self, request, connection, message):
        """
        Serializes and writes a message using the appropriate
        structures available in the connection.

        The message to be serialized is in fact a sequence
        of messages pending to be sent to the client.

        This method should be used to avoid inappropriate
        serialization of messages.

        @type request: HttpRequest
        @param request: The http request to be used in the
        writing operation to be performed.
        @type connection: CommunicationConnection
        @param connection: The communication connection to used
        in the serialization of the message.
        @type message: String
        @param message: The message to be serialized and written
        through the request.
        """

        # retrieves the json plugin
        json_plugin = self.mvc_plugin.json_plugin

        # serializes the message and writes the serialized
        # message to the request
        serialized_message = connection.serialize_message(message, json_plugin)
        request.write(serialized_message)

    def _get_connection(self, request, connection_name):
        """
        Retrieves the communication connection for the
        given request (using the id value from it) and
        connection name.

        @type request: HttpRequest
        @param request: The http request to be used to retrieve
        the id.
        @type connection_name: String
        @param connection_name: The name of the connection to be
        retrieved.
        @rtype: CommunicationConnection
        @return: The communication connection to be retrieved.
        """

        # retrieves the request connection identifier value to be
        # used in the creation of the connection information
        connection_id = request.get_attribute("id")

        # creates the connection information tuple and then
        # tries to retrieve the communication connection from the
        # connection information connection map
        connection_information = (connection_id, connection_name)
        connection = self.connection_informations_map.get(connection_information, None)

        # returns the (communication) connection
        return connection

    def _add_connection(self, connection):
        """
        Adds a (communication) connection to the internal structures
        of the communication handler, this should update all of the
        structures and activate the connection immediately.

        @type connection: CommunicationConnection
        @param connection: The communication connection to be added
        to the communication handler.
        """

        self.__add_connection_name_map(connection)
        self.__add_service_connections_map(connection)
        self.__set_connection_information_map(connection)

    def _remove_connection(self, connection):
        """
        Removes a (communication) connection from the internal structures
        of the communication handlers, this should update all of the
        structures and deactivate the connection immediately.

        @type connection: CommunicationConnection
        @param connection: The communication connection to be removed
        from the communication handler.
        """

        self.__remove_connection_name_map(connection)
        self.__remove_service_connections_map(connection)
        self.__unset_connection_information_map(connection)
        self._unregister_channels(connection)

    def _register_channels(self, connection, channels):
        # retrieves the connection name, to be used to determine
        # the diffusion domain of the connection and uses it to
        # creates the fully qualified names for the various channels
        # that were sent for registration
        connection_name = connection.get_connection_name()
        channels_fqn = [connection_name + "/" + channel for channel in channels]

        # iterates over the complete set of channels provided to register
        # the provided connection for them
        for channel_fqn in channels_fqn:
            # in case the channel is not currently present in
            # the channels map must create a new list to hold
            # the various connections in it
            if not channel_fqn in self.channels_map:
                self.channels_map[channel_fqn] = []

            # retrieves the connections list for the current channel
            # and adds the current connection into it
            connections_list = self.channels_map[channel_fqn]
            connections_list.append(connection)

            # notifies the connection about the changing in the channel
            # state (it has been registered)
            connection.on_channel(channel_fqn, unregister = False)

        # retrieves the complete set of channels registered for the
        # current connection and adds the list of channels current
        # in registration
        channels_list = self.channels_map_i.get(connection, [])
        self.channels_map_i[connection] = channels_list + list(channels_fqn)

    def _unregister_channels(self, connection, channels = None):
        # retrieves the connection name, to be used to determine
        # the diffusion domain of the connection and uses it to
        # creates the fully qualified names for the various channels
        # that were sent for registration
        connection_name = connection.get_connection_name()

        # in case the list of channels to be unregistered from
        # the connection is not defined defaults to the complete
        # set of channels (unregistering from all) otherwise runs
        # the resolution of the fully qualified names for the set
        # of channels provided (channel resolution process)
        if channels == None: channels_fqn = self.channels_map_i.get(connection, [])
        else: channels_fqn = [connection_name + "/" + channel for channel in channels]

        # iterates over the complete set of channels provided to unregister
        # the provided connection from them
        for channel_fqn in channels_fqn:
            # retrieves the connections list for the current channel
            # and removes the current connection from it
            connections_list = self.channels_map.get(channel_fqn, [])
            if connection in connections_list: connections_list.remove(connection)

            # notifies the connection about the changing in the channel
            # state (it has been unregistered)
            connection.on_channel(channel_fqn, unregister = True)

        # retrieves the complete set of channels registered for the
        # current connection and removes the channels current
        # for unregistration from it
        channels_list = self.channels_map_i.get(connection, [])
        for channel_fqn in channels_fqn:
            if channel_fqn in channels_list: channels_list.remove(channel_fqn)

        # in case the list of channels is currently empty and
        # the connection exists in the channels map inverted
        # must run the garbage collector
        if not channels_list and connection in self.channels_map_i:
            del self.channels_map_i[connection]

    def __add_connection_name_map(self, connection):
        # retrieves the connection name, to be used to determine
        # the diffusion domain of the connection
        connection_name = connection.get_connection_name()

        # in case the connection name does nor already exists
        # in the connections map must create a new sequence to
        # hold the various connections
        if not connection_name in self.connections_map:
            self.connections_map[connection_name] = []

        # retrieves the connection list from the connection map and
        # adds the (communication) connection to the connections list
        connections_list = self.connections_map[connection_name]
        connections_list.append(connection)

    def __add_service_connections_map(self, connection):
        # retrieves the service connection (low level socket connection)
        # for the (communication) connection
        service_connection = connection.get_service_connection()

        # in case the service connection does nor already exists
        # in the service connections map must create a new sequence to
        # hold the various connections
        if not service_connection in self.service_connections_map:
            self.service_connections_map[service_connection] = []

        # retrieves the connection list from the service connections map
        # and adds the (communication) connection to the connections list
        connections_list = self.service_connections_map[service_connection]
        connections_list.append(connection)

    def __set_connection_information_map(self, connection):
        # retrieves the connection information and uses it to associate
        # the (communication) connection in the connection informations map
        connection_information = connection.get_connection_information()
        self.connection_informations_map[connection_information] = connection

    def __remove_connection_name_map(self, connection):
        # retrieves the connection name, to be used to determine
        # the diffusion domain of the connection
        connection_name = connection.get_connection_name()

        # retrieves the connection list from the connections  map
        # and removes the (communication) connection from the connections list
        connections_list = self.connections_map[connection_name]
        connections_list.remove(connection)

        # in case the connections list is empty, removes the
        # connection list from the connections map (performs
        # garbage collection operation)
        if not connections_list: del self.connections_map[connection_name]

    def __remove_service_connections_map(self, connection):
        # retrieves the service connection (low level socket connection)
        # for the (communication) connection
        service_connection = connection.get_service_connection()

        # retrieves the connection list from the service connections map
        # and removes the (communication) connection from the connections list
        connections_list = self.service_connections_map[service_connection]
        connections_list.remove(connection)

        # in case the connections list is empty, removes the
        # connection list from the service connections map
        # (performs garbage collection operation)
        if not connections_list: del self.service_connections_map[service_connection]

    def __unset_connection_information_map(self, connection):
        # retrieves the connection information and uses it to remove
        # the (communication) connection from the connection informations map
        connection_information = connection.get_connection_information()
        del self.connection_informations_map[connection_information]

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
    """ The processing queue to be used to store the
    various communication elements that contain the
    request associated with the connection to be sent """

    processing_map = []
    """ The processing map """

    timestamp_list = []
    """ The list with the ordered timestamps (for timeout)
    of the various elements in the processing """

    timestamp_map = {}
    """ The map associating the timestamp (for timeout)
    with the connection element """

    processing_queue_lock = None
    """ The processing queue lock, that ensures only one
    access to the queue at a time """

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

        # iterates continuously to process the various elements
        # as they become ready to be processed (data ready) or
        # as they timeout (overflow) the maximum time
        while True:
            # in case the stop flag is set must break
            # the loop (end of iteration)
            if self.stop_flag: break

            # acquires the processing queue lock
            self.processing_queue_lock.acquire()

            # pops the "current" connection queue from the communication handler
            # and then released the processing queue lock
            try: connection_queue = self.communication_handler.pop_connection_queue()
            finally: self.processing_queue_lock.release()

            # iterates over the connection queue "connections" to process
            # its communication elements (are ready to be sent)
            for connection in connection_queue:
                # retrieves the communication elements from the processing
                # map using the connection and then processes them
                elements = self.processing_map.get(connection, [])
                self.process_elements(elements)

            # retrieves the "overflown" communication elements
            # and processes them
            elements = self.get_overflown_elements()
            self.process_elements(elements)

            # waits for the connection queue event
            connection_queue_event.wait(DEFAULT_UPDATE_POLL_TIMEOUT)

        # processes the complete processing queue to "flush"
        # the pending connections avoiding client connection
        # to remain open indefinitely
        elements = self.processing_queue
        self.process_elements(elements)

    def process_elements(self, elements):
        # starts the removal list (for communication
        # element removal)
        removal_list = []

        # iterates over all the communication elements in
        # the communication elements list
        for element in elements:
            # processes the communication element and adds
            # the communication element to the removal
            # list for later removal
            self._process_element(element)
            removal_list.append(element)

        # iterates over all the communication elements
        # in the removal list
        for element in removal_list:
            # removes the communication element from the queue
            self.remove_queue(element)

    def get_all_elements(self):
        # starts the overflown (communication) elements list
        overflown_elements = []

        # iterates over all the timestamps in
        # timestamp list
        for timestamp in self.timestamp_list:
            # retrieves the communication element for the
            # timestamp in iteration
            elements = self.timestamp_map[timestamp]

            # iterates over all the communication elements
            # to add them to the overflown communication
            # elements (list extension)
            for element in elements: overflown_elements.append(element)

        # returns the overflown (communication) elements
        return overflown_elements

    def get_overflown_elements(self):
        """
        Calculates and retrieves the complete set of communication
        elements that have overflow their wait time and that so
        a default message should be returned to the client.

        @rtype: List
        @return: The list of communication elements that represent
        the overflow connections.
        """

        # retrieves the current timestamp
        current_timestamp = time.time()

        # starts the overflown (communication) elements list
        overflown_elements = []

        # iterates over all the timestamps in
        # timestamp list
        for timestamp in self.timestamp_list:
            # in case the current timestamp is smaller than
            # the timestamp in iteration the communication
            # element is not to be processed yet (end of
            # communication elements, must break loop)
            if current_timestamp < timestamp: break

            # retrieves the communication element for the
            # timestamp in iteration
            elements = self.timestamp_map[timestamp]

            # iterates over all the communication elements
            # to add them to the overflown communication
            # elements (list extension)
            for element in elements: overflown_elements.append(element)

        # returns the overflown (communication) elements
        return overflown_elements

    def add_queue(self, element):
        # acquires the processing queue lock
        self.processing_queue_lock.acquire()

        try:
            # unpacks the communication element into the various components
            # of it to be for the adding operation
            connection, _request, target_timestamp = element

            # in case the target timestamp is not yet present
            # in the timestamp list
            if not target_timestamp in self.timestamp_list:
                # adds the target timestamp to the timestamp
                # list and re-sorts the list
                self.timestamp_list.append(target_timestamp)
                self.timestamp_list.sort()

            # retrieves the communication elements list for the target
            # timestamp (if any) and adds the communication element to the list
            elements = self.timestamp_map.get(target_timestamp, [])
            elements.append(element)
            self.timestamp_map[target_timestamp] = elements

            # retrieves the communication elements list for the communication
            # connection (if any) and adds the communication element to the list
            elements = self.processing_map.get(connection, [])
            elements.append(element)
            self.processing_map[connection] = elements

            # adds the communication element to the processing queue
            self.processing_queue.append(element)

            # in case the (communication) connection message queue is not empty
            # processes the communication elements (flushes queue)
            not connection.is_empty() and self.process_elements(elements)
        finally:
            # releases the processing queue lock
            self.processing_queue_lock.release()

    def remove_queue(self, element):
        # acquires the processing queue lock
        self.processing_queue_lock.acquire()

        try:
            # in case the communication element is not present
            # in the processing queue (possible add and remove)
            # must return immediately
            if not element in self.processing_queue: return

            # unpacks the communication element into the various components
            # of it to be for the removing operation
            connection, _request, target_timestamp = element

            # retrieves the communication elements associated with the
            # target timestamp and removes the current communication
            # element from the communication elements
            elements = self.timestamp_map[target_timestamp]
            elements.remove(element)

            # in case the communication elements list is empty
            # it should be removed (house-keeping)
            if not elements:
                # removes the communication elements list
                # reference from the timestamp map (it's empty)
                del self.timestamp_map[target_timestamp]

                # removes the target timestamp from the timestamp
                # list (no more elements for the target timestamp)
                self.timestamp_list.remove(target_timestamp)

            # retrieves the communication elements associated with the
            # (communication) connection and removes the current communication
            # element from the communication elements
            elements = self.processing_map[connection]
            elements.remove(element)

            # in case the communication elements list is empty
            # it should be removed (house-keeping)
            if not elements:
                # removes the communication elements list
                # reference from the processing map (it's empty)
                del self.processing_map[connection]

            # removes the communication element from the "main"
            # processing queue
            self.processing_queue.remove(element)
        finally:
            # releases the processing queue lock
            self.processing_queue_lock.release()

    def _process_element(self, element):
        # unpacks the element into the (communication) connection the request
        # and the target timestamp
        connection, request, _target_timestamp = element

        # retrieves the service connection so that it's possible
        # to check if it's still open (bandwidth optimization)
        service_connection = request.get_service_connection()

        # checks if the service connection (data connection) is still open
        # and in case the service connection is not open anymore returns
        # immediately (no need to write in a closed connection)
        service_connection_is_open = service_connection.is_open()
        if not service_connection_is_open: return

        # retrieves the current message queue for the connection by "popping"
        # the message queue (retrieves the latest)
        message_queue = connection.pop_message_queue()

        # writes the message queue into the message and processes
        # the request in the service (this represents the final part
        # of the delayed processing of the request) flushing the data
        # to the client side
        self.communication_handler._write_message(request, connection, message_queue)
        request.process()

class CommunicationConnection:
    """
    The communication connection class.
    """

    communication_handler = None
    """ The communication handler """

    connection_id = None
    """ The connection id, should be a randomly and non
    colliding value """

    connection_name = None
    """ The connection name, abstract name of the diffusion
    scope associated with the connection """

    service_connection = None
    """ The service connection for the connection, this
    is the lower level socket connection (data connection) """

    delegate = None
    """ The delegate object to be used to redirect
    event calls for connection actions, the events to
    be issued include connection and channel changes """

    status = False
    """ The current (open) status for the connection
    in case the current connection is open the value
    should be true otherwise it should be false """

    handlers = []
    """ The list of (message) handler functions to be used
    for the sending of the message to external notification
    system, these calls should not block the flow control """

    message_queue = []
    """ The queue of messages pending to be sent, may contain
    both unicode and string based messages """

    message_queue_lock = None
    """ The lock for the access to the message queue,
    avoids collision under simultaneous access """

    message_queue_event = None
    """ The event about the new message operation
    in the message queue """

    def __init__(self, communication_handler, connection_id, connection_name, service_connection = None, delegate = None):
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
        @type delegate: Object
        @param delegate: The delegate object to be used to redirect
        event calls for connection actions.
        """

        self.communication_handler = communication_handler
        self.connection_id = connection_id
        self.connection_name = connection_name
        self.service_connection = service_connection
        self.delegate = delegate

        self.handlers = []
        self.message_queue = []
        self.message_queue_lock = threading.RLock()
        self.message_queue_event = threading.Event()

    def open(self):
        """
        Opens the current connection, should start all the
        current internal structures.

        The event handlers should also be triggered in case
        a delegate is registered.
        """

        self.status = True
        self.service_connection.add_delegate(self)

        if self.delegate and hasattr(self.delegate, "on_open"):
            self.delegate.on_open(self)

    def close(self):
        """
        Closes the current connection, should stop all the
        current internal structures.

        The event handlers should also be triggered in case
        a delegate is registered.
        """

        self.status = False

        if self.delegate and hasattr(self.delegate, "on_close"):
            self.delegate.on_close(self)

    def serialize_message(self, message, serializer):
        """
        Serializes the given message, using the given
        serializer method.

        The serialization takes into account the current
        connection information (exposed in the message).

        @type message: String
        @param message: The message to be serialized, this
        value will be marked as return.
        @type serializer: Method
        @param serializer: The serializer method to be used
        in the serialization.
        """

        # creates the map for the message
        message_map = {}

        # sets the message map values
        message_map["id"] = self.connection_id
        message_map["name"] = self.connection_name
        message_map["result"] = message

        # serializes the message map
        serialized_message_map = serializer.dumps(message_map)

        # returns the serialized message map
        return serialized_message_map

    def send_message(self, message):
        """
        Sends the provided message using the complete set of
        registered handlers for the current connection.

        This method is considered the main abstraction for the
        interaction with the connection.
        """

        if self.service_connection: self.add_message_queue(message)
        for handler in self.handlers: handler(message)

    def add_handler(self, handler):
        """
        Adds a new message handler to the current connection so
        that every time a new message is sent for the current
        connection the handler is "notified" about it.

        @type handler: Function
        @param handler: The handler function to be called for
        every message received in the connection.
        """

        self.handlers.append(handler)

    def remove_handler(self, handler):
        """
        Removes an handler function currently registered in the
        current connection, avoiding any further handling of
        messages from it.

        @type handler: Function
        @param handler: The handler function to be removed from
        the current connection, no further messages handled.
        """

        if not handler in self.handlers: return
        self.handlers.remove(handler)

    def add_print_handler(self):
        """
        Adds a "simple" printer handler to the current connection
        so that any message received will be printed to the standard
        output of the current executing process.
        """

        self.add_handler(self.print_handler)

    def add_apn_handler(self, token_string, key_file = None, cert_file = None, sandbox = True):
        """
        Adds an apn (apple push notifications) handler to the current
        connection to be able to handle communication with ios/osx
        devices using the apn protocol.

        @type token_string: String
        @param token_string: The hexadecimal based string containing the
        token that identifies the device/app uniquely.
        @type key_file: String
        @param key_file: The path to the (private) key file to be used in
        the connection to the apn service.
        @type cert_file: String
        @param cert_file: The path to the certificate file to be used in
        the connection to the apn service.
        @type sandbox: bool
        @param sandbox: If the connection with the apn service should be done
        using the secure sandboxed approach (default) or the production model.
        """

        apn_handler = handlers.apn.ApnHandler(
            token_string,
            key_file = key_file,
            cert_file = cert_file,
            sandbox = sandbox
        )
        self.add_handler(apn_handler.handle)

    def print_handler(self, message):
        """
        The print handler method, responsible for printing a message
        to the standard output.

        This method is mainly used for easy debugging purposes.
        """

        print message

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
            # adds the message to the message queue, sets the
            # message queue event and adds the current connection
            # to the connection queue
            self.message_queue.append(message)
            self.message_queue_event.set()
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
            # saves the queue in the pop queue clears the
            # current message queue and clears the message
            # queue event
            pop_queue = self.message_queue
            self.message_queue = []
            self.message_queue_event.clear()
        finally:
            # releases the message queue lock
            self.message_queue_lock.release()

        # returns the pop queue
        return pop_queue

    def on_close(self, connection):
        self.communication_handler.delete_connection(self)

    def on_channel(self, fqn, unregister = False):
        connection_name_l = len(self.connection_name)
        name = fqn[connection_name_l + 1:]
        if self.delegate and hasattr(self.delegate, "on_channel"):
            self.delegate.on_channel(self, name, unregister = unregister)

    def is_open(self):
        """
        Checks if the current connection status is open
        and returns the value.

        @rtype: bool
        @return: If the status for the current connection
        is open (connection available).
        """

        return self.status

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

    def get_connection_information(self):
        """
        Retrieves the connection information, containing
        both the identifier of the connection and the name
        (domain) of it.

        @rtype: Tuple
        @return: The connection information.
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
