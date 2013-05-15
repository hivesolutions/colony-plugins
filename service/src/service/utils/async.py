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

import sys
import time
import errno
import types
import heapq
import select
import socket
import threading
import traceback

import colony.libs.map_util

import colony.base.exceptions

import threads
import exceptions

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

PENDING_TIMEOUT = 5.0
""" The timeout to be used to cancel connection in the
handshake pending state (not possible to accept) """

class AbstractService:

    service_utils = None
    """ The service utils """

    service_utils_plugin = None
    """ The service utils plugin """

    stop_flag = False
    """ The flag that controls the execution of the main loop """

    service_sockets = []
    """ The service sockets """

    service_socket_end_point_map = {}
    """ The service socket end point map """

    service_connection_active = False
    """ The service connection active flag """

    time_events = []
    """ The list of pending events to be handled in a time based
    fashion, the process that handles these events is considered a timer
    and this time is part of the main event loop """

    handlers_map = {}
    """ The map that contains the association between the socket fd and
    operation type tuple and the list containing the various handler functions
    to be called upon the kind of event registered is triggered for the
    socked fd in the tuple """

    socket_fd_map = {}
    """ Contains the association between the various file descriptors
    defined in the current pool and the appropriate socket objects that
    represent these connections """

    address_fd_map = {}
    """ Table of associations between the various file descriptor values
    and the address tuples of the connections they represent (the tuple
    contain first the address and then the port """

    pending_fd_map = {}
    """ The map containing the associating between the file
    descriptors and the sockets for the sockets pending handshake """





    client_connection_map = {}

    service_execution_thread = None



    service_connection_close_end_event = None



    def __init__(self, service_utils, service_utils_plugin, parameters = {}):
        """
        Constructor of the class.

        @type service_utils: ServiceUtils
        @param service_utils: The service utils.
        @type service_utils_plugin: ServiceUtilsPlugin
        @param service_utils_plugin: The service utils plugin.
        @type parameters: Dictionary
        @param parameters: The parameters
        """

        self.service_utils = service_utils
        self.service_utils_plugin = service_utils_plugin

        self.service_plugin = parameters.get("service_plugin", None)
        self.service_handling_task_class = parameters.get("service_handling_task_class", None)
        self.end_points = parameters.get("end_points", [])
        self.socket_provider = parameters.get("socket_provider", None)
        self.bind_host = parameters.get("bind_host", BIND_HOST)
        self.port = parameters.get("port", PORT)
        self.socket_parameters = parameters.get("socket_parameters", {})

        self.time_events = []


        #self.chunk_size = parameters.get("chunk_size", CHUNK_SIZE)

        self.service_configuration = parameters.get("service_configuration", {})
        self.extra_parameters = parameters.get("extra_parameters", {})

        #self.client_connection_timeout = parameters.get("client_connection_timeout", CLIENT_CONNECTION_TIMEOUT)
        #self.connection_timeout = parameters.get("connection_timeout", CONNECTION_TIMEOUT)
        #self.request_timeout = parameters.get("request_timeout", REQUEST_TIMEOUT)
        #self.response_timeout = parameters.get("response_timeout", RESPONSE_TIMEOUT)

        self.service_sockets = []
        self.service_socket_end_point_map = {}



        self.handlers_map = {}

        self.socket_fd_map = {}
        self.address_fd_map = {}
        self.pending_fd_map = {}


        self.client_connection_map = {}



        self.service_connection_close_end_event = threading.Event()


        # TER CUIDADO COM ESTE NONE VER SE O POSSO REMOVER DOS SERVICOS !!!!!

        self.client_service = self.service_handling_task_class(self.service_plugin, None, self.service_configuration, exceptions.ServiceUtilsException, self.extra_parameters)
        self.service_execution_thread = threads.ServiceExecutionThread(self)

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
                socket_provider_plugins_map = self.service_utils.socket_provider_plugins_map

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
                    raise exceptions.SocketProviderNotFound("socket provider %s not found" % socket_provider)
            else:
                # creates the service socket
                service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # sets the service socket to non blocking and sets the blocking
            # options in the socket to false so that new sockets are are
            # created automatically in non blocking mode
            service_socket.setblocking(0)
            hasattr(service_socket, "set_option") and service_socket.set_option("blocking", False)

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

            service_connection = ServiceConnection(self, service_socket, bind_host, port)

            socket_fd = service_socket.fileno()

            self.socket_fd_map[socket_fd] = service_socket
            self.address_fd_map[socket_fd] = (bind_host, port)
            self.poll_instance.register(socket_fd, READ | ERROR)

            self.add_handler(socket_fd, service_connection.read_handler, READ)


    # ---- ESTES SAO METODOS DA ABSTRACAO SERVICE------


    def add_socket(self, client_socket, client_address, service_port):
        client_socket_fd = client_socket.fileno()

        self.socket_fd_map[client_socket_fd] = client_socket
        self.address_fd_map[client_socket_fd] = (client_address, service_port)
        self.poll_instance.register(client_socket_fd, READ | ERROR)

        client_connection = ClientConnection(self, client_socket, client_address, service_port)
        client_connection.service_execution_thread = self.service_execution_thread
        self.client_connection_map[client_socket] = client_connection

        self.add_handler(client_socket_fd, client_connection.read_handler, READ)
        self.add_handler(client_socket_fd, client_connection.write_handler, WRITE)
        self.add_handler(client_socket_fd, client_connection.error_handler, ERROR)

    def remove_socket(self, client_socket):
        client_socket_fd = client_socket.fileno()

        del self.socket_fd_map[client_socket_fd]
        del self.address_fd_map[client_socket_fd]
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

        if not tuple in self.handlers_map:
            self.handlers_map[tuple] = []

        lista = self.handlers_map[tuple]
        lista.append(callback_method)

    def remove_handler(self, socket_fd, callback_method, operation):
        tuple = (socket_fd, operation)

        lista = self.handlers_map[tuple]
        lista.remove(callback_method)

        if not lista: del self.handlers_map[tuple]

    def call_handlers(self, socket_fd, operation):
        tuple = (socket_fd, operation)

        self.call_handlers_tuple(tuple)

    def call_handlers_tuple(self, tuple):
        # retrieves the list of handlers for the tuple
        # to be handled, in case there are no handlers
        # registered for the tuple, returns immediately
        handlers = self.handlers_map.get(tuple, [])
        if not handlers: return

        # retrieves the socket fd and then retrieves
        # the socket from the socket fd map
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
                print "-" * 60
                traceback.print_exc(file = sys.stdout)
                print "-" * 60

                # retrieves the client connection from the client
                # connection map using the socket and closes it, at
                # this point the client connection may not exist in
                # the client connection map, in such case no client
                # connection is closed
                client_connection = self.client_connection_map.get(socket, None)
                client_connection and client_connection.close()

    def add_time_handler(self, time, callback_method):
        heapq.heappush(self.time_events, (time, callback_method))

    def start_service(self):
        """
        Starts the service.
        """

        try:
            # starts the background threads
            self._start_threads()

            # creates the base infra-structure for the service
            self._create_base()

            # creates and sets the service sockets
            self._create_service_sockets()

            # activates and listens the service sockets
            self._activate_service_sockets()

            # runs the main loop
            self._loop()
        except BaseException, exception:
            print "Critical exception in user code:"
            print "-" * 60
            traceback.print_exc(file = sys.stdout)
            print "-" * 60

            # prints a warning message message
            self.service_plugin.warning("Runtime problem: %s, while starting the service" % unicode(exception))

            # sets the service connection active flag as false
            self.service_connection_active = False
        finally:
            # disables the service sockets
            self._disable_service_sockets()

            # removes the client sockets
            self._remove_client_sockets()

            # sets the service connection close end event
            self.service_connection_close_end_event.set()

            # unsets the stop flag
            self.stop_flag = False

    def stop_service(self):
        """
        Stops the service.
        """

        # sets the service connection active flag as false
        self.service_connection_active = False

        # sets the stop flag
        self.stop_flag = True

        # waits for the service connection close end event
        self.service_connection_close_end_event.wait()

        # clears the service connection close end event
        self.service_connection_close_end_event.clear()

        # stops the background threads
        self._stop_threads()

    def _create_base(self):
        """
        Creates the base infra-structure for the running og the
        service.
        """

        # sets the initial poll instance
        self.poll_instance = SelectPolling()

        # sets the service connection active flag as true
        self.service_connection_active = True

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

                # "unpacks" the various operation flags, so
                # that the current operation may be discovered
                read = operation_flag & READ
                write = operation_flag & WRITE
                error = operation_flag & ERROR

                read and self.call_handlers_tuple((socket_fd, read))
                write and self.call_handlers_tuple((socket_fd, write))
                error and self.call_handlers_tuple((socket_fd, error))

            # retrieves the current time, to be able to use
            # it for comparison against the target times
            # and then starts the counter that controls the
            # amount of expired time events
            current_time = time.time()
            expired_count = 0

            # iterates over all the time events to handle the
            # ones that have "expired"
            for time_event in self.time_events:
                # unpacks the time part of the event and tests it,
                # in case the time for execution has not been
                # yet reached (finished callback execution)
                _time = time_event[0]
                if _time > current_time: break

                # retrieves the callback part of the event
                # and calls it (event handling)
                callback = time_event[1]
                callback()

                # increments the counter that controls the
                # events that have expired (deferred popping)
                expired_count += 1

            # pops the processes elements from the time events
            # list (deferred popping, avoids list corruption)
            for _index in xrange(expired_count): heapq.heappop(self.time_events)

    def _disable_service_sockets(self):
        """
        Disables the service sockets.
        """

        # iterates over all the service sockets
        for service_socket in self.service_sockets:
            # closes the service socket
            service_socket.close()

    def _remove_client_sockets(self):
        """
        Removes all the "remaining" client sockets.
        """

        # the list to hold the client sockets
        # to be removed
        removal_list = []

        # iterates over all the client sockets in the
        # client connection map
        for client_socket in self.client_connection_map:
            # adds the client socket or the
            # removal list (for later removal)
            removal_list.append(client_socket)

        # iterates over all the client sockets
        # to be removed
        for client_socket in removal_list:
            # removes the client socket from
            # internal structures
            self.remove_socket(client_socket)

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

    connection_address = None
    """ The address for the connection """

    connection_port = None
    """ The port for the connection """

    connection_status = True

    request_data = {}

    delegates = []
    """ The list of delegate object that are notified
    about the changes to the connection """

    def __init__(self, service, socket, connection_address, connection_port):
        self.service = service
        self.socket = socket
        self.connection_address = connection_address
        self.connection_port = connection_port

        self.socket_fd = socket.fileno()

        self.request_data = {}
        self.delegates = []

    def __repr__(self):
        return "(%s, %s)" % (self.connection_address, self.connection_port)

    def call_delegate(self, name, *args, **kwargs):
        for delegate in self.delegates:
            if not hasattr(delegate, name): continue
            method = getattr(delegate, name)
            method(*args, **kwargs)

    def add_delegate(self, delegate):
        if delegate in self.delegates: return
        self.delegates.append(delegate)

    def remove_delegate(self, delegate):
        if not delegate in self.delegates: return
        self.delegates.remove(delegate)

    def is_secure(self):
        """
        Verifies if the current connection is of type secure,
        this analysis uses a specific heuristic.

        If the connection is secure the underlying level should
        be using an encrypted channel for communication.

        @rtype: bool
        @return: If the current connection is being transmitted
        using a secure and encrypted channel.
        """

        return hasattr(self.socket, "_secure")

class ServiceConnection(Connection):

    handlers_association = {}
    """ The map associating the socket fd with the respective
    close handler method or function """

    def __init__(self, service, socket, connection_address, connection_port):
        Connection.__init__(self, service, socket, connection_address, connection_port)

        self.handlers_association = {}

    def read_handler(self, _socket):
        # iterates continuously to accept the various
        # sockets pending to be accepted in the buffer
        while True:
            try:
                # accepts the connection retrieving the service connection object and the address
                service_connection, service_address = _socket.accept()
            except colony.base.exceptions.OperationNotComplete, error:
                # unpacks the various components of the error, so
                # that is possible to retrieve the connection and
                # the address of the (still) pending connection
                # then uses the service connection to retrieve the
                # socket file descriptor
                service_connection = error.connection
                service_address = error.address
                socket_fd = service_connection.fileno()

                # tries to retrieve the handle not complete options,
                # in case this option is set a non complete accept
                # operation should be retried for a certain timeout
                # until it's finally discarded
                handle_not_complete = self.service.socket_parameters.get("handle_not_complete", True)

                # in case the handle not complete flag is set the pending
                # mode is enabled for the current socket (tries the handshake
                # latter) otherwise the service connection is discarded
                if handle_not_complete: self._enable_pending(service_connection, service_address, socket_fd)
                else: service_connection.close()
                return

            except socket.error, exception:
                # in case the exception is normal, the operation did not
                # complete or the socket would block nothing should be done
                # and the read operation must be deferred to the next data
                # sending "event"
                if exception.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EPERM, errno.ENOENT, WSAEWOULDBLOCK):
                    # returns immediately (no error)
                    return
                # otherwise the exception is more severe
                else:
                    # re-raises the exception
                    raise

            # sets the service connection to non blocking mode
            # and then adds the service connection in the service
            service_connection.setblocking(0)
            self.service.add_socket(service_connection, service_address, self.connection_port)

    def get_handshake_handler(self, service_connection, service_address, socket_fd):

        def handshake_handler(_socket):
            try:
                # tries to run the handshake in the service connection
                # on more time (see if it's already possible to do it)
                service_connection.handshake()
            except socket.error, error:
                # in case the exception is normal, the operation did not
                # complete or the socket would block nothing should be done
                # and the read operation must be deferred to the next data
                # receiving "event"
                if error.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EPERM, errno.ENOENT, WSAEWOULDBLOCK):
                    # returns immediately (no error)
                    return
                # otherwise it's a major error and the connection is considered
                # to be in an erroneous state (meant to be discarded)
                else:
                    # disables the pending connection, no more need to listen
                    # to the changes on it for enabling
                    self._disable_pending(service_connection, service_address, socket_fd); return
            except:
                # disables the pending connection, no more need to listen
                # to the changes on it for enabling (meant to be discarded)
                self._disable_pending(service_connection, service_address, socket_fd); return
            else:
                try:
                    # disables the pending connection, no more need to listen
                    # to the changes on it for enabling (in this case the connection
                    # is not meant to be closed)
                    self._disable_pending(service_connection, service_address, socket_fd, close_connection = False)

                    # sets the service connection to non blocking mode and
                    # adds service connection in the service
                    service_connection.setblocking(0)
                    self.service.add_socket(service_connection, service_address, self.connection_port)
                except:
                    # closes the service connection, because there was an
                    # "extraordinary" exception (unexpected) the re-raises
                    # the exception to the upper levels
                    service_connection.close()
                    raise

        # returns the "generated" handshake handler through
        # context closure
        return handshake_handler

    def get_close_handler(self, service_connection, service_address, socket_fd):

        def close_handler():
            # in case the socket fd is no longer present in the pending
            # fd map there's no need to proceed with the disable of the
            # pending operations (normal situation)
            if not socket_fd in self.service.pending_fd_map: return

            # verifies if the socket of the service that is going to be
            # closed as the same that is currently set for the socket
            # descriptor, in case it's not returns immediately as the
            # socket fd must have been re-used
            _service_connection = self.service.socket_fd_map[socket_fd]
            if not _service_connection == service_connection: return

            # disables the pending connection, this operation should close
            # the socket and release all the allocated structures inside the
            # service structures for the socket/connection
            self._disable_pending(service_connection, service_address, socket_fd)

        # returns the "generated" close handler through
        # context closure
        return close_handler

    def _enable_pending(self, service_connection, service_address, socket_fd):
        handshake_handler = self.get_handshake_handler(service_connection, service_address, socket_fd)
        close_handler = self.get_close_handler(service_connection, service_address, socket_fd)

        self.handlers_association[socket_fd] = handshake_handler
        self.service.socket_fd_map[socket_fd] = service_connection
        self.service.address_fd_map[socket_fd] = service_address
        self.service.pending_fd_map[socket_fd] = service_connection
        self.service.poll_instance.register(socket_fd, READ | ERROR)
        self.service.add_handler(socket_fd, handshake_handler, READ)

        self.service.add_time_handler(time.time() + PENDING_TIMEOUT, close_handler)

    def _disable_pending(self, service_connection, service_address, socket_fd, close_connection = True):
        handshake_handler = self.handlers_association[socket_fd]
        del self.service.socket_fd_map[socket_fd]
        del self.service.address_fd_map[socket_fd]
        del self.service.pending_fd_map[socket_fd]
        self.service.poll_instance.unregister(socket_fd, READ | ERROR)
        self.service.remove_handler(socket_fd, handshake_handler, READ)
        close_connection and service_connection.close()

class ClientConnection(Connection):

    pending_data_buffer = []
    """ The buffer that holds the pending data """

    write_data_buffer = []
    """ The buffer to hold the data pending to be sent """

    service_execution_thread = None
    """ The service execution thread """

    def __init__(self, service, socket, connection_address, connection_port):
        Connection.__init__(self, service, socket, connection_address, connection_port)

        self.pending_data_buffer = []
        self.write_data_buffer = []

        # TODO IMPLMENTAR DE MODO REAL
        self.connection_request_timeout = 10

    def open(self):
        # in case the current connection is already open
        # must return immediately (no duplicate open)
        if self.is_open(): return

        # sets the connection status to open
        self.connection_status = True

        # handles the open (event) using the client service and
        # then calls the appropriate delegate method
        self.service.client_service.handle_opened(self)
        self.call_delegate("on_open", self)

    def close(self):
        # in case the current connection is already closed
        # must return immediately (no duplicate close)
        if not self.is_open(): return

        # removes the socket from the service, this should
        # properly close the socket
        self.service.remove_socket(self.socket)

        # sets the connection status to closed
        self.connection_status = False

        # handles the close (event) using the client service and
        # then calls the appropriate delegate method
        self.service.client_service.handle_closed(self)
        self.call_delegate("on_close", self)

    def read_handler(self, _socket):
        # iterates continuously
        while True:
            try:
                # receives the data from the socket
                data = _socket.recv(1024)
            except socket.error, exception:
                # in case the exception is normal, the operation did not
                # complete or the socket would block nothing should be done
                # and the read operation must be deferred to the next data
                # receiving "event"
                if exception.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EPERM, errno.ENOENT, WSAEWOULDBLOCK):
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
            # otherwise a try for parsing should be made
            else:
                # iterates while there is data available to
                # be processed
                while data:
                    # tries to retrieve the request from the given data (only a successful
                    # parse is valid for request handling)
                    request = self.service.client_service.retrieve_request_data(self, data)

                    # handles the request using the client service (in case the request is valid)
                    request and self.service.client_service.handle_request(self, request)

                    # pops the pending data from the client service and sets it
                    # as the current data
                    data = self.pop_pending_data()

    def write_handler(self, _socket):
        # iterates over the write data buffer
        while self.write_data_buffer:
            # retrieves the data (last element) from the write
            # data buffer and checks the type of it
            data = self.write_data_buffer[-1]
            data_type = type(data)

            # in case the type is a tuple (callback
            # exists)
            if data_type == types.TupleType:
                # unpacks the data into data and
                # callback information
                data, callback = data
            # otherwise no callback exists
            else:
                # unsets the callback value
                callback = None

            try:
                # retrieves the data bytes (length)
                data_bytes = len(data)

                # tries to send the data through the socket
                sent_bytes = _socket.send(data)
            except socket.error, exception:
                # in case the exception is normal, the operation did not
                # complete or the socket would block nothing should be done
                # and the read operation must be deferred to the next data
                # sending "event"
                if exception.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EPERM, errno.ENOENT, WSAEWOULDBLOCK):
                    # returns immediately (no error)
                    return
                # otherwise the exception is more severe
                # and it shall be handled properly
                else:
                    # calls the callback, with the
                    # error flag set (in case it's defined)
                    callback and callback(True)

                    # re-raises the exception
                    raise

            # pops the element from the write data buffer
            self.write_data_buffer.pop()

            # in case the data was not completely
            # sent (sent bytes not complete)
            if sent_bytes < data_bytes:
                # retrieves the "pending" data (including callback) and
                # inserts it in first place in the write
                # data buffer (queue)
                pending_data = (data[sent_bytes:], callback)
                self.write_data_buffer.append(pending_data)
            # otherwise in case there is a callback to be called
            else:
                # calls the callback, with the
                # error flag unset (in case it's defined)
                callback and callback(False)

        # unregisters the socket fd for the write event
        self.unregister(self.socket_fd, WRITE)

    def error_handler(self, socket):
        # closes the client connection
        self.close()

    def write(self, data, write_front = False):
        # in case the connection status is closed
        if not self.connection_status:
            raise Exception("Trying to write in a closed socket")

        # in case the write front flag is set
        if write_front:
            # adds the data to the write buffer
            # in the front part of the buffer
            self.write_data_buffer.append(data)
        # otherwise the write front is disabled
        # the data shall be inserted to the back
        else:
            # adds the data to the write buffer
            # in the back part of the buffer
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

    def execute_background(self, callable, retries = 0, timeout = 0.0, timestamp = None):
        """
        Executes the given callable object in a background
        thread.
        This method is useful for avoid blocking the request
        handling method in non critic tasks.

        @type callable: Callable
        @param callable: The callable to be called in background.
        @type retries: int
        @param retries: The number of times to retry executing the
        callable in case exception is raised.
        @type timeout: float
        @param timeout: The time to be set in between calls of the
        callable, used together with the retry value.
        @type timestamp: float
        @param timestamp: The unix second based timestamp for the
        first execution of the callable.
        """

        # adds the callable to the service execution thread
        self.service_execution_thread.add_callable(
            callable,
            retries = retries,
            timeout = timeout,
            timestamp = timestamp
        )

    def send(self, message, response_timeout = None, retries = None, write_front = False):
        self.write(message, write_front)

    def send_callback(self, message, callback, response_timeout = None, retries = None, write_front = False):
        message_tuple = (message, callback)
        self.write(message_tuple, write_front)

    def is_open(self):
        return self.connection_status

    def is_async(self):
        """
        Checks if the connection is of type asynchronous
        or synchronous.
        Useful to provide conditional execution in the premises
        of the connection type.

        @rtype: bool
        @return: If the connection is of type asynchronous.
        """

        return True

    def add_pending_data(self, pending_data):
        """
        Adds a chunk of pending data to the pending
        data buffer.

        @type pending_data: String
        @param pending_data: The pending data to be
        added to the pending data buffer.
        """

        # in case the pending data is not valid
        if not pending_data:
            # returns immediately
            return

        # adds the pending data to the pending data
        # buffer (list)
        self.pending_data_buffer.append(pending_data)

    def pop_pending_data(self):
        """
        "Pops" the current pending data from the
        service connection.

        @rtype: String
        @return: The current pending data from the
        service connection (in case there is one).
        """

        # in case the pending data buffer is
        # not valid
        if not self.pending_data_buffer:
            # returns none (invalid)
            return None

        # returns the result of a "pop" in the
        # pending data buffer
        return self.pending_data_buffer.pop(0)

    def pending_data(self):
        """
        Checks if there is pending data to be "read"
        or interpreted by the client service.

        @rtype: bool
        @return: If there is pending data to be "read"
        or interpreted by the client service.
        """

        # returns the boolean value base on the status
        # of the pending data buffer
        return self.pending_data_buffer and True or False
