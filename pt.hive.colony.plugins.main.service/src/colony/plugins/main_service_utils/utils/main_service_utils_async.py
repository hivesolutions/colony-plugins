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

import sys
import errno
import select
import socket
import threading
import traceback

import colony.libs.map_util

import main_service_utils_threads
import main_service_utils_exceptions

BIND_HOST = ""
""" The bind host """

PORT = 0
""" The bind host """

SERVER_SIDE_VALUE = "server_side"
""" The server side value """

DO_HANDSHAKE_ON_CONNECT_VALUE = "do_handshake_on_connect"
""" The do handshake on connect value """


_EPOLLIN = 0x001
_EPOLLPRI = 0x002
_EPOLLOUT = 0x004
_EPOLLERR = 0x008
_EPOLLHUP = 0x010
_EPOLLRDHUP = 0x2000
_EPOLLONESHOT = (1 << 30)
_EPOLLET = (1 << 31)



WSAEWOULDBLOCK = 10035




READ = _EPOLLIN

WRITE = _EPOLLPRI

ERROR = _EPOLLERR | _EPOLLHUP | _EPOLLRDHUP

ALL = READ | WRITE | ERROR





POLL_TIMEOUT = 0.2


class AbstractService:

    main_service_utils = None
    """ The main service utils """

    main_service_utils_plugin = None
    """ The main service utils plugin """

    stop_flag = False
    """ The flag that controls the execution of the main loop """

    service_sockets = []
    """ The service sockets """

    service_socket_end_point_map = {}
    """ The service socket end point map """




    handers_map = {}



    socket_fd_map = {}


    client_connection_map = {}

    service_execution_thread = None



    service_connection_close_end_event = None



    def __init__(self, main_service_utils, main_service_utils_plugin, parameters = {}):
        """
        Constructor of the class.

        @type main_service_utils: MainServiceUtils
        @param main_service_utils: The main service utils.
        @type main_service_utils_plugin: MainServiceUtilsPlugin
        @param main_service_utils_plugin: The main service utils plugin.
        @type parameters: Dictionary
        @param parameters: The parameters
        """

        self.main_service_utils = main_service_utils
        self.main_service_utils_plugin = main_service_utils_plugin

        self.service_plugin = parameters.get("service_plugin", None)
        self.service_handling_task_class = parameters.get("service_handling_task_class", None)
        self.end_points = parameters.get("end_points", [])
        self.socket_provider = parameters.get("socket_provider", None)
        self.bind_host = parameters.get("bind_host", BIND_HOST)
        self.port = parameters.get("port", PORT)
        self.socket_parameters = parameters.get("socket_parameters", {})




        #self.chunk_size = parameters.get("chunk_size", CHUNK_SIZE)

        self.service_configuration = parameters.get("service_configuration", {})
        self.extra_parameters = parameters.get("extra_parameters", {})

        #self.client_connection_timeout = parameters.get("client_connection_timeout", CLIENT_CONNECTION_TIMEOUT)
        #self.connection_timeout = parameters.get("connection_timeout", CONNECTION_TIMEOUT)
        #self.request_timeout = parameters.get("request_timeout", REQUEST_TIMEOUT)
        #self.response_timeout = parameters.get("response_timeout", RESPONSE_TIMEOUT)

        self.service_sockets = []
        self.service_socket_end_point_map = {}



        self.handers_map = {}

        self.socket_fd_map = {}


        self.client_connection_map = {}



        self.service_connection_close_end_event = threading.Event()


        # TER CUIDADO COM ESTE NONE VER SE O POSSO REMOVER DOS SERVICOS !!!!!

        self.client_service = self.service_handling_task_class(self.service_plugin, None, self.service_configuration, main_service_utils_exceptions.MainServiceUtilsException, self.extra_parameters)
        self.service_execution_thread = main_service_utils_threads.ServiceExecutionThread(self)

        # in case no end points are defined and there is a socket provider
        # a default end point is created with those values
        if not self.end_points and self.socket_provider:
            # defines the end point tuple
            end_point_tuple = (
                self.socket_provider,
                self.bind_host,
                self.port,
                self.socket_parameters
            )

            # adds the end point
            self.end_points.append(end_point_tuple)







    def _create_service_sockets(self):
        """
        Creates the service sockets according to the
        service configuration.
        """

        # iterates over all the end points
        for end_point in self.end_points:
            # unpacks the end point
            socket_provider, _bind_host, _port, socket_parameters = end_point

            # in case the socket provider is defined
            if socket_provider:
                # retrieves the socket provider plugins map
                socket_provider_plugins_map = self.main_service_utils.socket_provider_plugins_map

                # in case the socket provider is available in the socket
                # provider plugins map
                if socket_provider in socket_provider_plugins_map:
                    # retrieves the socket provider plugin from the socket provider plugins map
                    socket_provider_plugin = socket_provider_plugins_map[socket_provider]

                    # the parameters for the socket provider
                    parameters = {
                        SERVER_SIDE_VALUE : True,
                        DO_HANDSHAKE_ON_CONNECT_VALUE : False
                    }

                    # copies the socket parameters to the parameters map
                    colony.libs.map_util.map_copy(socket_parameters, parameters)

                    # creates a new service socket with the socket provider plugin
                    service_socket = socket_provider_plugin.provide_socket_parameters(parameters)
                else:
                    # raises the socket provider not found exception
                    raise main_service_utils_exceptions.SocketProviderNotFound("socket provider %s not found" % socket_provider)
            else:
                # creates the service socket
                service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # sets the service socket to non blocking
            service_socket.setblocking(0)

            # adds the service socket to the service sockets
            self.service_sockets.append(service_socket)

            # sets the end point in the service socket end point map
            self.service_socket_end_point_map[service_socket] = end_point






    def _activate_service_sockets(self):
        """
        Activates the service socket.
        """

        # iterates over the service sockets and the end points
        for service_socket, end_point in zip(self.service_sockets, self.end_points):
            # unpacks the end point
            _socket_provider, bind_host, port, _socket_parameters = end_point

            # sets the socket to be able to reuse the socket
            service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # defines the bind parameters
            bind_parameters = (
                bind_host,
                port
            )

            # binds the service socket
            service_socket.bind(bind_parameters)

            # in case the service type is connection

            #TENHO DE PENSAR MUITO BEM SOBRE ESTE ASSUNTO

            #if self.service_type == CONNECTION_TYPE_VALUE:

            # start listening in the service socket
            service_socket.listen(30)

            service_connection = ServiceConnection(self, service_socket)

            socket_fd = service_socket.fileno()

            self.socket_fd_map[socket_fd] = service_socket
            self.poll_instance.register(socket_fd, READ | ERROR)

            self.add_handler(socket_fd, service_connection.read_handler, READ)


    # ---- ESTES SAO METODOS DA ABSTRACAO SERVICE------


    def add_socket(self, client_socket, client_address):
        client_socket_fd = client_socket.fileno()

        self.socket_fd_map[client_socket_fd] = client_socket
        self.poll_instance.register(client_socket_fd, READ | ERROR)

        client_connection = ClientConnection(self, client_socket, client_address)
        client_connection.service_execution_thread = self.service_execution_thread
        self.client_connection_map[client_socket] = client_connection

        self.add_handler(client_socket_fd, client_connection.read_handler, READ)
        self.add_handler(client_socket_fd, client_connection.write_handler, WRITE)
        self.add_handler(client_socket_fd, client_connection.error_handler, ERROR)

    def remove_socket(self, client_socket):
        client_socket_fd = client_socket.fileno()

        del self.socket_fd_map[client_socket_fd]
        self.poll_instance.unregister(client_socket_fd)

        client_connection = self.client_connection_map[client_socket]
        del self.client_connection_map[client_socket]

        self.remove_handler(client_socket_fd, client_connection.read_handler, READ)
        self.remove_handler(client_socket_fd, client_connection.write_handler, WRITE)
        self.remove_handler(client_socket_fd, client_connection.error_handler, ERROR)

        # closes the client socket
        client_socket.close()

    # ---- AKI ACABAM OS METODOS DA ABSTRACAO SERVICE------




    def add_handler(self, socket_fd, callback_method, operation):
        tuple = (socket_fd, operation)

        if not tuple in self.handers_map:
            self.handers_map[tuple] = []

        lista = self.handers_map[tuple]
        lista.append(callback_method)

    def remove_handler(self, socket_fd, callback_method, operation):
        tuple = (socket_fd, operation)

        lista = self.handers_map[tuple]
        lista.remove(callback_method)

        if not lista:
            del self.handers_map[tuple]

    def call_handlers(self, socket_fd, operation):
        tuple = (socket_fd, operation)

        self.call_handlers_tuple(tuple)

    def call_handlers_tuple(self, tuple):
        handlers = self.handers_map.get(tuple, [])

        if not handlers:
            # returns immediately
            return

        # retrieves the socket fd and then
        # retrieves the socket from the socket fd map
        socket_fd = tuple[0]
        socket = self.socket_fd_map[socket_fd]

        # iterates over all the handlers for the
        # tuple (to call them)
        for handler in handlers:
            try:
                # calls the handler with the socket
                handler(socket)
            except BaseException:
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file = sys.stdout)
                print '-'*60

                # retrieves the client connection from the client
                # connection map using the socket and closes it
                client_connection = self.client_connection_map[socket]
                client_connection.close()

    def start_service(self):
        """
        Starts the service.
        """

        # clears the service connection close end event
        self.service_connection_close_end_event.clear()

        # unsets the stop flag
        self.stop_flag = False

        self.poll_instance = SelectPolling()

        # starts the background threads
        self._start_threads()

        # creates and sets the service sockets
        self._create_service_sockets()

        # activates and listens the service sockets
        self._activate_service_sockets()

        try:
            # runs the main loop
            self._loop()
        finally:
            # disables the service sockets
            self._disable_service_sockets()

            # sets the service connection close end event
            self.service_connection_close_end_event.set()

    def stop_service(self):
        """
        Stops the service.
        """

        # stops the background threads
        self._stop_threads()

        # sets the stop flag
        self.stop_flag = True

        # waits for the service connection close end event
        self.service_connection_close_end_event.wait()

    def _loop(self):
        """
        Method representing the main loop for
        request and connection handling.
        """

        # iterates continuously
        while True:
            # in case the stop flag is set
            if self.stop_flag:
                # breaks the loop
                break

            # pools the poll instance to retrieve the
            # current loop events
            events = self.poll_instance.poll(POLL_TIMEOUT)

            # iterates over all the events to
            # call the proper handlers
            for event in events:
                # unpacks the event into the socket fd
                # and the operation flag
                socket_fd, operation_flag = event

                # "unpacks" the various operation flags
                read = operation_flag & READ
                write = operation_flag & WRITE
                error = operation_flag & ERROR

                read and self.call_handlers_tuple((socket_fd, read))
                write and self.call_handlers_tuple((socket_fd, write))
                error and self.call_handlers_tuple((socket_fd, error))

    def _disable_service_sockets(self):
        """
        Disables the service sockets.
        """

        # iterates over all the service sockets
        for service_socket in self.service_sockets:
            # closes the service socket
            service_socket.close()

        for tobias in  self.client_connection_map:
            self.remove_socket(tobias)

    def _start_threads(self):
        """
        Stars the base threads for background execution.
        """

        # starts the service execution (background) thread
        self.service_execution_thread.start()

    def _stop_threads(self):
        """
        Stars the base threads for background execution.
        """

        # stops the service execution (background) thread
        self.service_execution_thread.stop()

        # joins (waits for) the service execution
        # (background) thread
        self.service_execution_thread.join()

class SelectPolling:

    readable_socket_list = None
    writeable_socket_list = None
    errors_socket_list = None

    def __init__(self):
        self.readable_socket_list = set()
        self.writeable_socket_list = set()
        self.errors_socket_list = set()

    def register(self, socket_fd, operations):
        if operations & READ:
            self.readable_socket_list.add(socket_fd)

        if operations & WRITE:
            self.writeable_socket_list.add(socket_fd)

        if operations & ERROR:
            self.errors_socket_list.add(socket_fd)

            # adds the socket to the readable socket list
            # as closed connections are reported as read in select
            self.readable_socket_list.add(socket_fd)

    def unregister(self, socket_fd, operations = ALL):
        if operations & READ:
            self.readable_socket_list.discard(socket_fd)

        if operations & WRITE:
            self.writeable_socket_list.discard(socket_fd)

        if operations & ERROR:
            self.errors_socket_list.discard(socket_fd)

    def modify(self, socket_fd, operations):
        self.unregister(socket_fd)
        self.register(socket_fd, operations)

    def poll(self, timeout):
        # selects the values
        readable, writeable, errors = select.select(self.readable_socket_list, self.writeable_socket_list, self.errors_socket_list, timeout)

        #print "recebeu '%s', '%s', '%s'" % (readable, writeable, errors)

        # creates the events map to hold the socket fd's
        events_map = {}

        for socket_fd in readable:
            events_map[socket_fd] = events_map.get(socket_fd, 0) | READ

        for socket_fd in writeable:
            events_map[socket_fd] = events_map.get(socket_fd, 0) | WRITE

        for socket_fd in errors:
            events_map[socket_fd] = events_map.get(socket_fd, 0) | ERROR

        # retrieves the list of event tuples
        events_list = events_map.items()

        # returns the events list
        return events_list

class EpollPolling:

    def __init__(self):
        pass

    def register(self, socket):
        pass

    def unregister(self, socket):
        pass

    def poll(self):
        pass

class KqueuePolling:

    def __init__(self):
        pass

    def register(self, socket):
        pass

    def unregister(self, socket):
        pass

    def poll(self):
        pass


class Connection:

    service = None
    """ The reference to the service implementation """

    socket = None

    socket_fd = None

    connection_status = True

    request_data = {}

    def __init__(self, service, socket):
        self.service = service
        self.socket = socket

        self.socket_fd = socket.fileno()

        self.request_data = {}

class ServiceConnection(Connection):

    def __init__(self, service, socket):
        Connection.__init__(self, service, socket)

    def read_handler(self, _socket):
        # iterates continuously
        while True:
            try:
                # accepts the connection retrieving the service connection object and the address
                service_connection, service_address = _socket.accept()
            except socket.error, exception:
                # in case the exception is normal
                if exception.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN, WSAEWOULDBLOCK):
                    # returns immediately (no error)
                    return
                # otherwise the exception is more severe
                else:
                    # re-raises the exception
                    raise

            # sets the service connection to non blocking mode
            service_connection.setblocking(0)

            # adds service connection in the service
            self.service.add_socket(service_connection, service_address)

class ClientConnection(Connection):

    connection_address = None
    """ The address for the connection """

    write_data_buffer = []
    """ The buffer to hold the data pending to be sent """

    service_execution_thread = None
    """ The service execution thread """

    def __init__(self, service, socket, connection_address):
        Connection.__init__(self, service, socket)

        self.connection_address = connection_address

        self.write_data_buffer = []

        # TODO IMPLMENTAR DE MODO REAL
        self.connection_request_timeout = 10

    def open(self):
        # sets the connection status to open
        self.connection_status = True

    def close(self):
        # removes the socket from the service
        self.service.remove_socket(self.socket)

        # sets the connection status to closed
        self.connection_status = False

    def read_handler(self, _socket):
        # iterates continuously
        while True:
            try:
                data = _socket.recv(1024)
            except socket.error, exception:
                # in case the exception is normal
                if exception.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN, WSAEWOULDBLOCK):
                    # returns immediately (no error)
                    return
                # otherwise the exception is more severe
                else:
                    # re-raises the exception
                    raise

            # in case the data is empty (connection closed)
            if data == "":
                # closes the client connection
                self.close()

                # returns immediately (no more
                # data to be processed)
                return
            else:
                request = self.service.client_service.retrieve_request_data(self, data)

                # handles the request using the client service (in case the request is valid)
                request and self.service.client_service.handle_request(self, request)

    def write_handler(self, _socket):
        # iterates over the write data buffer
        while self.write_data_buffer:
            # retrieves the data (last element) from the write
            # data buffer
            data = self.write_data_buffer[-1]

            try:
                # retrieves the data bytes (length)
                data_bytes = len(data)

                # tries to send the data through the socket
                sent_bytes = _socket.send(data)
            except socket.error, exception:
                # in case the exception is normal
                if exception.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN, WSAEWOULDBLOCK):
                    # returns immediately (no error)
                    return
                # otherwise the exception is more severe
                else:
                    # re-raises the exception
                    raise

            # pops the element from the write data buffer
            self.write_data_buffer.pop()

            # in case the data was not completely
            # sent (sent bytes not complete)
            if sent_bytes < data_bytes:
                # retrieves the "pending" data and
                # inserts it in first place in the write
                # data buffer (queue)
                pending_data = data[sent_bytes:]
                self.write_data_buffer.append(pending_data)

        # unregisters the socket fd for the write event
        self.unregister(self.socket_fd, WRITE)

    def error_handler(self, socket):
        # closes the client connection
        self.close()

    def write(self, data):
        if not self.connection_status:
            raise Exception("Trying to write in a closed socket")

        # adds the data to the write buffer
        self.write_data_buffer.insert(0, data)

        # registers the socket fd for the write event (in
        # case it's not already registered)
        self.register(self.socket_fd, WRITE)

    def register(self, socket_fd, operations):
        if not self.connection_status:
            raise Exception("Trying to register in a closed socket")

        self.service.poll_instance.register(socket_fd, operations)

    def unregister(self, socket_fd, operations):
        if not self.connection_status:
            raise Exception("Trying to unregister in a closed socket")

        self.service.poll_instance.unregister(socket_fd, operations)

    def execute_background(self, callable):
        """
        Executes the given callable object in a background
        thread.
        This method is useful for avoid blocking the request
        handling method in non critic tasks.

        @type callable: Callable
        @param callable: The callable to be called in background.
        """

        # adds the callable to the service execution thread
        self.service_execution_thread.add_callable(callable)

    def send(self, message, response_timeout = None, retries = None):
        self.write(message)

    def is_open(self):
        return self.connection_status
