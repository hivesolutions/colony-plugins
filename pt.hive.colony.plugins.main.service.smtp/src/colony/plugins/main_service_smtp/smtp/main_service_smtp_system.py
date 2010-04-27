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
import socket
import select
import threading
import traceback

import colony.libs.string_buffer_util

import main_service_smtp_exceptions

BIND_HOST_VALUE = ""
""" The host value """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 60
""" The request timeout """

CHUNK_SIZE = 4096
""" The chunk size """

NUMBER_THREADS = 15
""" The number of threads """

MAX_NUMBER_THREADS = 30
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

DEFAULT_PORT = 25
""" The default port """

class MainServiceSmtp:
    """
    The main service smtp class.
    """

    main_service_smtp_plugin = None
    """ The main service smtp plugin """

    smtp_service_handler_plugins_map = {}
    """ The smtp service handler plugin map """

    smtp_socket = None
    """ The smtp socket """

    smtp_connection_active = False
    """ The smtp connection active flag """

    smtp_client_thread_pool = None
    """ The smtp client thread pool """

    smtp_connection_close_event = None
    """ The smtp connection close event """

    smtp_connection_close_end_event = None
    """ The smtp connection close end event """

    def __init__(self, main_service_smtp_plugin):
        """
        Constructor of the class.

        @type main_service_smtp_plugin: MainServiceSmtpPlugin
        @param main_service_smtp_plugin: The main service smtp plugin.
        """

        self.main_service_smtp_plugin = main_service_smtp_plugin

        self.smtp_service_handler_plugins_map = {}
        self.smtp_connection_close_event = threading.Event()
        self.smtp_connection_close_end_event = threading.Event()

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # retrieves the socket provider value
        socket_provider = parameters.get("socket_provider", None)

        # retrieves the port value
        port = parameters.get("port", DEFAULT_PORT)

        # retrieves the service configuration
        service_configuration_property = self.main_service_smtp_plugin.get_configuration_property("server_configuration")

        # in case the service configuration property is defined
        if service_configuration_property:
            # retrieves the service configuration
            service_configuration = service_configuration_property.get_data()
        else:
            # sets the service configuration as an empty map
            service_configuration = {}

        # retrieves the socket provider configuration value
        socket_provider = service_configuration.get("default_socket_provider", socket_provider)

        # retrieves the port configuration value
        port = service_configuration.get("default_port", port)

        # start the server for the given socket provider, port and encoding
        self.start_server(socket_provider, port, service_configuration)

        # clears the smtp connection close event
        self.smtp_connection_close_event.clear()

        # sets the smtp connection close end event
        self.smtp_connection_close_end_event.set()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # sets the smtp connection active flag as false
        self.smtp_connection_active = False

        # sets the smtp connection close event
        self.smtp_connection_close_event.set()

        # waits for the smtp connection close end event
        self.smtp_connection_close_end_event.wait()

        # clears the smtp connection close end event
        self.smtp_connection_close_end_event.clear()

        # stops all the pool tasks
        self.smtp_client_thread_pool.stop_pool_tasks()

        # stops the pool
        self.smtp_client_thread_pool.stop_pool()

    def start_server(self, socket_provider, port, service_configuration):
        """
        Starts the server in the given port.

        @type socket_provider: String
        @param socket_provider: The name of the socket provider to be used.
        @type port: int
        @param port: The port to start the server.
        @type service_configuration: Dictionary
        @param service_configuration: The service configuration map.
        """

        # retrieves the thread pool manager plugin
        thread_pool_manager_plugin = self.main_service_smtp_plugin.thread_pool_manager_plugin

        # retrieves the task descriptor class
        task_descriptor_class = thread_pool_manager_plugin.get_thread_task_descriptor_class()

        # creates the smtp client thread pool
        self.smtp_client_thread_pool = thread_pool_manager_plugin.create_new_thread_pool("smtp pool",
                                                                                         "pool to support smtp client connections",
                                                                                         NUMBER_THREADS, SCHEDULING_ALGORITHM, MAX_NUMBER_THREADS)

        # starts the smtp client thread pool
        self.smtp_client_thread_pool.start_pool()

        # sets the smtp connection active flag as true
        self.smtp_connection_active = True

        # in case the socket provider is defined
        if socket_provider:
            # retrieves the socket provider plugins
            socket_provider_plugins = self.main_service_smtp_plugin.socket_provider_plugins

            # iterates over all the socket provider plugins
            for socket_provider_plugin in socket_provider_plugins:
                # retrieves the provider name from the socket provider plugin
                socket_provider_plugin_provider_name = socket_provider_plugin.get_provider_name()

                # in case the names are the same
                if socket_provider_plugin_provider_name == socket_provider:
                    # creates a new smtp socket with the socket provider plugin
                    self.smtp_socket = socket_provider_plugin.provide_socket()

            # in case the socket was not created, no socket provider found
            if not self.smtp_socket:
                raise main_service_smtp_exceptions.SocketProviderNotFound("socket provider %s not found" % socket_provider)
        else:
            # creates the smtp socket
            self.smtp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # sets the socket to be able to reuse the socket
        self.smtp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binds the smtp socket
        self.smtp_socket.bind((BIND_HOST_VALUE, port))

        # start listening in the smtp socket
        self.smtp_socket.listen(5)

        # loops while the smtp connection is active
        while not self.smtp_connection_close_event.isSet():
            try:
                # sets the socket to non blocking mode
                self.smtp_socket.setblocking(0)

                # starts the select values
                selected_values = ([], [], [])

                # iterates while there is no selected values
                while selected_values == ([], [], []):
                    # in case the connection is closed
                    if self.smtp_connection_close_event.isSet():
                        # closes the smtp socket
                        self.smtp_socket.close()

                        return

                    # selects the values
                    selected_values = select.select([self.smtp_socket], [], [], CLIENT_CONNECTION_TIMEOUT)

                # sets the socket to blocking mode
                self.smtp_socket.setblocking(1)
            except:
                # prints debug message about connection
                self.main_service_smtp_plugin.info("The socket is not valid for selection of the pool")

                return

            # in case the connection is closed
            if self.smtp_connection_close_event.isSet():
                # closes the smtp socket
                self.smtp_socket.close()

                return

            try:
                # accepts the connection retrieving the smtp connection object and the address
                smtp_connection, smtp_address = self.smtp_socket.accept()

                # creates a new smtp client service task, with the given smtp connection, address, encoding and encoding handler
                smtp_client_service_task = SmtpClientServiceTask(self.main_service_smtp_plugin, smtp_connection, smtp_address, service_configuration)

                # creates a new task descriptor
                task_descriptor = task_descriptor_class(start_method = smtp_client_service_task.start,
                                                        stop_method = smtp_client_service_task.stop,
                                                        pause_method = smtp_client_service_task.pause,
                                                        resume_method = smtp_client_service_task.resume)

                # inserts the new task descriptor into the smtp client thread pool
                self.smtp_client_thread_pool.insert_task(task_descriptor)

                self.main_service_smtp_plugin.debug("Number of threads in pool: %d" % self.smtp_client_thread_pool.current_number_threads)
            except Exception, exception:
                print exception
                self.main_service_smtp_plugin.error("Error accepting connection")

        # closes the smtp socket
        self.smtp_socket.close()

    def smtp_service_handler_load(self, smtp_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = smtp_service_handler_plugin.get_handler_name()

        self.smtp_service_handler_plugins_map[handler_name] = smtp_service_handler_plugin

    def smtp_service_handler_unload(self, smtp_service_handler_plugin):
        # retrieves the plugin handler name
        handler_name = smtp_service_handler_plugin.get_handler_name()

        del self.smtp_service_handler_plugins_map[handler_name]

class SmtpClientServiceTask:
    """
    The smtp client service task class.
    """

    main_service_smtp_plugin = None
    """ The main service smtp plugin """

    smtp_connection = None
    """ The smtp connection """

    smtp_address = None
    """ The smtp address """

    service_configuration = None
    """ The service configuration """

    encoding_handler = None
    """ The encoding handler """

    def __init__(self, main_service_smtp_plugin, smtp_connection, smtp_address, service_configuration):
        self.main_service_smtp_plugin = main_service_smtp_plugin
        self.smtp_connection = smtp_connection
        self.smtp_address = smtp_address
        self.service_configuration = service_configuration

    def start(self):
        # prints debug message about connection
        self.main_service_smtp_plugin.debug("Connected to: %s" % str(self.smtp_address))

        # sets the request timeout
        request_timeout = REQUEST_TIMEOUT

        # creates the session object
        session = SmtpSession()

        # retrieves the initial request
        request = self.retrieve_initial_request(session, request_timeout)

        # retrieves the real service configuration,
        # taking the request information into account
        service_configuration = self._get_service_configuration(request)

        # retrieves the default handler name
        handler_name = service_configuration.get("default_handler", None)

        # in case no handler name is defined (request not handled)
        if not handler_name:
            # raises an smtp no handler exception
            raise main_service_smtp_exceptions.SmtpNoHandlerException("no handler defined for current request")

        # retrieves the smtp service handler plugins map
        smtp_service_handler_plugins_map = self.main_service_smtp_plugin.main_service_smtp.smtp_service_handler_plugins_map

        # in case the handler is not found in the handler plugins map
        if not handler_name in smtp_service_handler_plugins_map:
            # raises an smtp handler not found exception
            raise main_service_smtp_exceptions.SmtpHandlerNotFoundException("no handler found for current request: " + handler_name)

        # retrieves the smtp service handler plugin
        smtp_service_handler_plugin = smtp_service_handler_plugins_map[handler_name]

        # handles the initial request by the request handler
        smtp_service_handler_plugin.handle_initial_request(request)

        # sends the initial request to the client (initial response)
        self.send_request(request)

        while True:
            try:
                # retrieves the request
                request = self.retrieve_request(session, request_timeout)
            except main_service_smtp_exceptions.MainServiceSmtpException:
                self.main_service_smtp_plugin.debug("Connection: %s closed" % str(self.smtp_address))
                return

            try:
                # prints debug message about request
                self.main_service_smtp_plugin.debug("Handling request: %s" % str(request))

                # handles the request by the request handler
                smtp_service_handler_plugins_map[handler_name].handle_request(request)

                # handles the request by the request handler
                smtp_service_handler_plugin.handle_request(request)

                # sends the request to the client (response)
                self.send_request(request)

                # in case the session is closed
                if session.get_closed():
                    # prints debug message about session
                    self.main_service_smtp_plugin.debug("Session closed: %s" % str(session))

                    break;

            except Exception, exception:
                self.send_exception(request, exception)

        # closes the smtp connection
        self.smtp_connection.close()

    def stop(self):
        # closes the smtp connection
        self.smtp_connection.close()

    def pause(self):
        pass

    def resume(self):
        pass

    def retrieve_initial_request(self, session, request_timeout = REQUEST_TIMEOUT):
        """
        Retrieves the initial request from the received message.

        @type session: SmtpSession
        @param session: The current smtp session.
        @type request_timeout: int
        @param request_timeout: The timeout for the request retrieval.
        @rtype: SmtpRequest
        @return: The request from the received message.
        """

        # creates the initial request object
        request = SmtpRequest()

        # sets the session object in the request
        request.set_session(session)

        # returns the initial request
        return request

    def retrieve_request(self, session, request_timeout = REQUEST_TIMEOUT):
        """
        Retrieves the request from the received message.

        @type session: SmtpSession
        @param session: The current smtp session.
        @type request_timeout: int
        @param request_timeout: The timeout for the request retrieval.
        @rtype: SmtpRequest
        @return: The request from the received message.
        """

        # creates the string buffer for the message
        message = colony.libs.string_buffer_util.StringBuffer()

        # creates a request object
        request = SmtpRequest()

        # continuous loop
        while True:
            # retrieves the data
            data = self.retrieve_data(request_timeout)

            # in case no valid data was received
            if data == "":
                raise main_service_smtp_exceptions.SmtpInvalidDataException("empty data received")

            # writes the data to the string buffer
            message.write(data)

            # retrieves the message value from the string buffer
            message_value = message.get_value()

            # in case the session is in data transmission mode
            if session.data_transmission:
                end_token = ".\r\n"
            else:
                end_token = "\r\n"

            # finds the first end token value
            end_token_index = message_value.find(end_token)

            # in case there is an end token found
            if not end_token_index == -1:
                # retrieves the smtp message
                smtp_message = message_value[:end_token_index]

                # in case the session is not in data transmission mode
                if not session.data_transmission:
                    # splits the smtp message
                    smtp_message_splitted = smtp_message.split(" ")

                    # retrieves the smtp command
                    smtp_command = smtp_message_splitted[0].lower()

                    # retrieves the smpt arguments
                    smtp_arguments = smtp_message_splitted[1:]

                    # sets the smtp command in the request
                    request.set_command(smtp_command)

                    # sets the smtp arguments in the request
                    request.set_arguments(smtp_arguments)

                # sets the smtp message in the request
                request.set_message(smtp_message)

                # sets the session object in the request
                request.set_session(session)

                # returns the request
                return request

    def retrieve_data(self, request_timeout = REQUEST_TIMEOUT, chunk_size = CHUNK_SIZE):
        try:
            # sets the connection to non blocking mode
            self.smtp_connection.setblocking(0)

            # runs the select in the smtp connection, with timeout
            selected_values = select.select([self.smtp_connection], [], [], request_timeout)

            # sets the connection to blocking mode
            self.smtp_connection.setblocking(1)
        except:
            raise main_service_smtp_exceptions.RequestClosed("invalid socket")

        if selected_values == ([], [], []):
            self.smtp_connection.close()
            raise main_service_smtp_exceptions.ServerRequestTimeout("%is timeout" % request_timeout)
        try:
            # receives the data in chunks
            data = self.smtp_connection.recv(chunk_size)
        except:
            raise main_service_smtp_exceptions.ClientRequestTimeout("timeout")

        return data

    def send_exception(self, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type request: SmtpRequest
        @param request: The request to send the exception.
        @type exception: Exception
        @param exception: The exception to be sent.
        """

        # sets the request response code
        request.set_response_code(554)

        # sets the request response message
        request.set_response_message("Exception occurred")

        # writes the exception message
        request.write("error: '" + str(exception) + "'\n")

        # writes the traceback message in the request
        request.write("traceback:\n")

        # retrieves the execution information
        _type, _value, traceback_list = sys.exc_info()

        # in case the traceback list is valid
        if traceback_list:
            formated_traceback = traceback.format_tb(traceback_list)
        else:
            formated_traceback = ()

        # iterates over the traceback lines
        for formated_traceback_line in formated_traceback:
            request.write(formated_traceback_line)

        # sends the request to the client (response)
        self.send_request(request)

    def send_request(self, request):
        self.send_request_simple(request)

    def send_request_simple(self, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            self.smtp_connection.send(result_value)
        except:
            # error in the client side
            return

    def _get_service_configuration(self, request):
        """
        Retrieves the service configuration for the given request.
        This retrieval takes into account the request target and characteristics
        to merge the virtual servers configurations.

        @type request: SmtpRequest
        @param request: The request to be used in the resolution
        of the service configuration.
        @rtype: Dictionary
        @return: The resolved service configuration.
        """

        # retrieves the base service configuration
        service_configuration = self.service_configuration

        # returns the service configuration
        return service_configuration

class SmtpRequest:
    """
    The smtp request class.
    """

    message = "none"
    """ The received message """

    command = "none"
    """ The received command """

    arguments = "none"
    """ The received arguments """

    response_message = "none"
    """ The response message """

    response_messages = []
    """ The response messages """

    response_code = None
    """ The response code """

    session = None
    """ The session """

    message_stream = None
    """ The message stream """

    properties = {}
    """ The properties """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.response_messages = []
        self.message_stream = colony.libs.string_buffer_util.StringBuffer()
        self.properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.command, self.message)

    def read(self):
        return self.message

    def write(self, message):
        self.message_stream.write(message)

    def get_result(self):
        """
        Retrieves the result value, processing
        the current request structure.

        @rtype: String
        @return: The result value for the current
        request structure.
        """

        # retrieves the result string value
        message = self.message_stream.get_value()

        # in case the response messages
        # are defined
        if self.response_messages:
            # initializes the return message
            return_message_buffer = colony.libs.string_buffer_util.StringBuffer()

            # starts the counter value
            counter = len(self.response_messages)

            # iterates over all the response messages
            for response_message in self.response_messages:
                # in case the counter is one (last response message)
                if counter == 1:
                    # adds the response code with the response message
                    return_message_buffer.write(str(self.response_code) + " " + response_message + "\r\n")
                else:
                    # adds the response code with the response message (separated with a dash)
                    return_message_buffer.write(str(self.response_code) + "-" + response_message + "\r\n")

                # decrements the counter
                counter -= 1

            # retrieves the return message from the return message buffer
            return_message = return_message_buffer.get_value()
        else:
            # creates the return message
            return_message = str(self.response_code) + " " + self.response_message + "\r\n"

            # in case the message is not empty
            if not message == "":
                return_message += message + "\r\n"

        # returns the return message
        return return_message

    def get_message(self):
        """
        Retrieves the message.

        @rtype: String
        @return: The message.
        """

        return self.message

    def set_message(self, message):
        """
        Sets the message.

        @type message: String
        @param message: The message.
        """

        self.message = message

    def get_command(self):
        """
        Retrieves the command.

        @rtype: String
        @return: The command.
        """

        return self.command

    def set_command(self, command):
        """
        Sets the command.

        @type command: String
        @param command: The command.
        """

        self.command = command

    def get_arguments(self):
        """
        Retrieves the arguments.

        @rtype: List
        @return: The arguments.
        """

        return self.arguments

    def set_arguments(self, arguments):
        """
        Sets the arguments.

        @type arguments: List
        @param arguments: The arguments.
        """

        self.arguments = arguments

    def get_response_message(self):
        """
        Retrieves the response message.

        @rtype: String
        @return: The response message.
        """

        return self.response_message

    def set_response_message(self, response_message):
        """
        Sets the response message.

        @type response_message: String
        @param response_message: The response message.
        """

        self.response_message = response_message

    def get_response_messages(self):
        """
        Retrieves the response messages.

        @rtype: List
        @return: The response messages.
        """

        return self.response_messages

    def set_response_messages(self, response_messages):
        """
        Sets the response messages.

        @type response_messages: List
        @param response_messages: The response messages.
        """

        self.response_messages = response_messages

    def get_response_code(self):
        """
        Retrieves the response code.

        @rtype: int
        @return: The response code.
        """

        return self.response_code

    def set_response_code(self, response_code):
        """
        Sets the response code.

        @type response_code: int
        @param response_code: The response code.
        """

        self.response_code = response_code

    def get_session(self):
        """
        Retrieves the session.

        @rtype: Session
        @return: The session.
        """

        return self.session

    def set_session(self, session):
        """
        Sets the session.

        @type session: Session
        @param session: The session.
        """

        self.session = session

class SmtpSession:
    """
    The smtp session class.
    """

    client_hostname = "none"
    """ The client hostname """

    extensions_active = False
    """ The extensions active flag """

    data_transmission = False
    """ The data transmission flag """

    closed = False
    """ The closed flag """

    current_message = None
    """ The current message being processed """

    messages = []
    """ The messages associated with the session """

    properties = {}
    """ The properties of the current session """

    def __init__(self):
        self.messages = []
        self.properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.client_hostname, self.properties)

    def generate_message(self, set_current_message = True):
        # creates the new message
        message = SmtpMessage()

        # adds the message to the messages list
        self.add_message(message)

        # in case the set current message flag
        # is active
        if set_current_message:
            # sets the message as the current message
            self.set_current_message(message)

    def add_message(self, message):
        """
        Adds a message to the list of messages
        of the current session.

        @type message: SmtpMessage
        @param message: The message to be added
        to the session.
        """

        self.messages.append(message)

    def get_client_hostname(self):
        """
        Retrieves the client hostname.

        @rtype: String
        @return: The client hostname.
        """

        return self.client_hostname

    def set_client_hostname(self, client_hostname):
        """
        Sets the client hostname.

        @type client_hostname: String
        @param client_hostname: The client hostname.
        """

        self.client_hostname = client_hostname

    def get_extensions_active(self):
        """
        Retrieves the extensions active.

        @rtype: bool
        @return: The extensions active.
        """

        return self.extensions_active

    def set_extensions_active(self, extensions_active):
        """
        Sets the extensions active.

        @type extensions_active: bool
        @param extensions_active: The extensions active.
        """

        self.extensions_active = extensions_active

    def get_data_transmission(self):
        """
        Retrieves the data transmission.

        @rtype: bool
        @return: The data transmission.
        """

        return self.data_transmission

    def set_data_transmission(self, data_transmission):
        """
        Sets the data transmission.

        @type data_transmission: bool
        @param data_transmission: The data transmission.
        """

        self.data_transmission = data_transmission

    def get_closed(self):
        """
        Retrieves the closed.

        @rtype: bool
        @return: The closed.
        """

        return self.closed

    def set_closed(self, closed):
        """
        Sets the closed.

        @type closed: bool
        @param closed: The closed.
        """

        self.closed = closed

    def get_current_message(self):
        """
        Retrieves the current message.

        @rtype: SmtpMessage
        @return: The current message.
        """

        return self.current_message

    def set_current_message(self, current_message):
        """
        Sets the current message.

        @type current_message: SmtpMessage
        @param current_message: The current message.
        """

        self.current_message = current_message

    def get_messages(self):
        """
        Retrieves the messages.

        @rtype: List
        @return: The messages.
        """

        return self.messages

    def set_messages(self, messages):
        """
        Sets the messages.

        @type messages: List
        @param messages: The messages.
        """

        self.messages = messages

    def get_properties(self):
        """
        Retrieves the properties.

        @rtype: Dictionary
        @return: The properties.
        """

        return self.properties

    def set_properties(self, properties):
        """
        Sets the properties.

        @type properties: Dictionary
        @param properties: The properties.
        """

        self.properties = properties

class SmtpMessage:
    """
    The smtp message class that represents
    a message to be sent through smtp.
    """

    contents = "none"
    """ The contents of the message """

    sender = "none"
    """ The sender of the message """

    recipients_list = []
    """ The list of recipients for the message """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.recipients_list = []

    def add_recipient(self, recipient):
        """
        Adds a recipient to the recipients list

        @type recipient: String
        @param recipient: The recipient to be added.
        """

        self.recipients_list.append(recipient)

    def get_contents(self):
        """
        Retrieves the contents.

        @rtype: String
        @return: The contents.
        """

        return self.contents

    def set_contents(self, contents):
        """
        Sets the contents.

        @type contents: String
        @param contents: The contents.
        """

        self.contents = contents

    def get_sender(self):
        """
        Retrieves the .

        @rtype: String
        @return: The sender.
        """

        return self.sender

    def set_sender(self, sender):
        """
        Sets the sender.

        @type sender: String
        @param sender: The sender.
        """

        self.sender = sender

    def get_recipients_list(self):
        """
        Retrieves the recipients list.

        @rtype: List
        @return: The recipients list.
        """

        return self.recipients_list

    def set_recipients_list(self, recipients_list):
        """
        Sets the recipients list.

        @type recipients_list: List
        @param recipients_list: The recipients list.
        """

        self.recipients_list = recipients_list
