#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import ssl
import errno
import types
import socket

import colony

PROVIDER_NAME = "ssl"
""" The provider name """

SSL_ERROR_WANT_READ = 2
""" The SSL error want read value """

SSL_ERROR_WANT_WRITE = 3
""" The SSL error want write value """

WSAEWOULDBLOCK = 10035
""" Windows based value for the error raised when a non
blocking connection is not able to read/write more, this
error should be raised constantly in no blocking connections """

SSL_VERSIONS = {
    "ssl2": ssl.PROTOCOL_SSLv2 if hasattr(ssl, "PROTOCOL_SSLv2") else -1,
    "ssl3": ssl.PROTOCOL_SSLv3 if hasattr(ssl, "PROTOCOL_SSLv3") else -1,
    "ssl23": ssl.PROTOCOL_SSLv23 if hasattr(ssl, "PROTOCOL_SSLv23") else -1,
    "tls1": ssl.PROTOCOL_TLSv1 if hasattr(ssl, "PROTOCOL_TLSv1") else -1,
    "tls11": ssl.PROTOCOL_TLSv1_1 if hasattr(ssl, "PROTOCOL_TLSv1_1") else -1,
    "tls12": ssl.PROTOCOL_TLSv1_2 if hasattr(ssl, "PROTOCOL_TLSv1_2") else -1,
    "tls13": ssl.PROTOCOL_TLSv1_3 if hasattr(ssl, "PROTOCOL_TLSv1_3") else -1,
    "tls": (
        ssl.PROTOCOL_TLS
        if hasattr(ssl, "PROTOCOL_TLS")
        else (ssl.PROTOCOL_SSLv23 if hasattr(ssl, "PROTOCOL_SSLv23") else -1)
    ),
    "tls_client": (
        ssl.PROTOCOL_TLS_CLIENT
        if hasattr(ssl, "PROTOCOL_TLS_CLIENT")
        else ssl.PROTOCOL_TLSv1
    ),
    "tls_server": (
        ssl.PROTOCOL_TLS_SERVER
        if hasattr(ssl, "PROTOCOL_TLS_SERVER")
        else ssl.PROTOCOL_TLSv1
    ),
}
""" The map associating the string based description
values for the various SSL protocols with the corresponding
constants in the SSL infra-structure, note that the map
is constructed taking into account the existence of the
constants in the SSL module defaulting to invalid otherwise """


class SSLSocket(colony.System):
    """
    The SSL socket (provider) class.
    """

    def get_provider_name(self):
        """
        Retrieves the socket provider name.

        :rtype: String
        :return: The socket provider name.
        """

        return PROVIDER_NAME

    def provide_socket(self):
        """
        Provides a new socket, configured with
        the default parameters.

        :rtype: Socket
        :return: The provided socket.
        """

        # creates the SSL socket
        ssl_socket = self.provide_socket_parameters()

        # returns the SSL socket
        return ssl_socket

    def provide_socket_parameters(self, parameters={}):
        """
        Provides a new socket, configured with
        the given parameters.

        :type parameters: Dictionary
        :param parameters: The parameters for socket configuration.
        :rtype: Socket
        :return: The provided socket.
        """

        # prints a debug message
        self.plugin.debug("Providing an SSL socket")

        # retrieves the plugin manager
        manager = self.plugin.manager

        # retrieves the plugin base path and uses it to retrieve the plugin
        # resources path (relative to the plugin path)
        plugin_path = manager.get_plugin_path_by_id(self.plugin.id)
        plugin_resources_path = plugin_path + "/ssl_socket/resources"

        # tries to retrieve the socket family
        socket_family = parameters.get("family", socket.AF_INET)

        # creates the normal socket
        normal_socket = socket.socket(socket_family, socket.SOCK_STREAM)

        # retrieves the dummy SSL key and certificate paths
        # so that they can be used as the default values
        dummy_ssl_key_path = plugin_resources_path + "/dummy.key"
        dummy_ssl_certificate_path = plugin_resources_path + "/dummy.crt"

        # tries to retrieve the key and certificate file paths,
        # falling back to the dummy certificate values
        key_file_path = parameters.get("key_file_path", dummy_ssl_key_path)
        certificate_file_path = parameters.get(
            "certificate_file_path", dummy_ssl_certificate_path
        )

        # resolves both file paths using the plugin manager, in case
        # their refers logical references their are converted into absolute paths
        key_file_path = manager.resolve_file_path(key_file_path)
        certificate_file_path = manager.resolve_file_path(certificate_file_path)

        # tries to retrieve the server side value
        server_side = parameters.get("server_side", False)

        # tries to retrieve the do handshake on connect value
        do_handshake_on_connect = parameters.get("do_handshake_on_connect", False)

        # tries to retrieve the server side value, that will
        # control the accepted versions of the protocol
        ssl_version = parameters.get("ssl_version", None)
        ssl_version = SSL_VERSIONS.get(ssl_version, ssl.PROTOCOL_SSLv23)

        # warps the normal socket into an SSL socket, providing
        # the extra security layer on top of the normal socket
        ssl_socket = self._wrap_socket(
            normal_socket,
            key_file_path,
            certificate_file_path,
            server_side,
            ssl_version=ssl_version,
            do_handshake_on_connect=do_handshake_on_connect,
        )

        # returns the SSL socket
        return ssl_socket

    def process_exception(self, socket, exception):
        """
        Processes the exception taking into account the severity of it,
        as for some exception a graceful handling is imposed.

        The provided socket object should comply with typical python
        interface for it.

        :type socket: Socket
        :param socket: The socket to be used in the exception processing.
        :type exception: Exception
        :param exception: The exception that is going to be handled/processed.
        :rtype: bool
        :return: The result of the processing, in case it's false a normal
        exception handling should be performed otherwise a graceful one is used.
        """

        return process_exception(socket, exception)

    def _wrap_socket(
        self,
        base_socket,
        key_file_path,
        certificate_file_path,
        server_side=False,
        ssl_version=ssl.PROTOCOL_SSLv23,
        do_handshake_on_connect=False,
        server_hostname="localhost",
    ):
        """
        Wraps the base socket into an SSL socket using the given
        key file, certificate file and attributes.

        Note that the version of the SSL implementation may be
        controlled and in some cases it's required to be controlled
        for security purposes.

        :type base_socket: Socket
        :param base_socket: The base socket to be used for wrapping.
        :type key_file_path: String
        :param key_file_path: The path to the key file.
        :type certificate_file_path: String
        :param certificate_file_path: The path to the certificate file.
        :type server_side: bool
        :param server_side: If the socket should be created for a server.
        :type ssl_version: int
        :param ssl_version: The version  of the SSL protocol stack that
        is allowed to be executed for the socket to wrapped.
        :type do_handshake_on_connect: bool
        :param do_handshake_on_connect: If a handshake should be done on connect.
        :type server_hostname: String
        :param server_hostname: The server hostname to be used in the SSL.
        :rtype: Socket
        :return: The wrapped (SSL) socket.
        """

        # warps the base socket into an SSL socket, then wraps it with
        # new  methods and returns it to the caller method
        ssl_socket = context_wrap(
            base_socket,
            key_file_path,
            certificate_file_path,
            server_side=server_side,
            ssl_version=ssl_version,
            do_handshake_on_connect=do_handshake_on_connect,
            server_hostname=server_hostname,
        )
        wrap_socket(ssl_socket)
        return ssl_socket


def context_wrap(
    socket,
    key_file_path,
    certificate_file_path,
    server_side=False,
    ssl_version=ssl.PROTOCOL_SSLv23,
    do_handshake_on_connect=False,
    server_hostname="localhost",
    verify_mode=ssl.CERT_NONE,
    check_hostname=False,
    context=None,
):
    if hasattr(ssl, "wrap_socket"):
        return ssl.wrap_socket(
            socket,
            key_file_path,
            certificate_file_path,
            server_side,
            ssl_version=ssl_version,
            do_handshake_on_connect=do_handshake_on_connect,
        )

    if not context:
        context = ssl.create_default_context()

    if hasattr(context, "check_hostname"):
        context.check_hostname = check_hostname
    context.verify_mode = verify_mode
    context.load_cert_chain(certfile=certificate_file_path, keyfile=key_file_path)
    return context.wrap_socket(
        socket,
        server_side=server_side,
        do_handshake_on_connect=do_handshake_on_connect,
        server_hostname=server_hostname,
    )


def wrap_socket(ssl_socket):
    # creates the bound accept and handshake methods for
    # the SSL socket
    _accept = types.MethodType(accept, ssl_socket)
    _handshake = types.MethodType(handshake, ssl_socket)
    _set_option = types.MethodType(set_option, ssl_socket)

    # creates the bound process exception method for the SSL socket
    _process_exception = types.MethodType(process_exception, ssl_socket)

    # sets the old accept method in the SSL socket with
    # a different name
    ssl_socket._accept = ssl_socket.accept

    # sets the new accept and handshake bound methods in
    # the SSL socket
    ssl_socket.accept = _accept
    ssl_socket.handshake = _handshake
    ssl_socket.set_option = _set_option

    # sets the extra secure attribute, to indicate
    # that this socket is of type secure
    ssl_socket._secure = True

    # sets the new process exception bound method in the SSL socket
    ssl_socket.process_exception = _process_exception


def accept(self):
    # accepts the connection, retrieving
    # the return value
    return_value = self._accept()

    # unpacks the return value into
    # connection and address
    connection, address = return_value

    try:
        # wraps the (SSL) connection with new methods
        wrap_socket(connection)

        # sets the connection to non blocking mode in case
        # the blocking flag is not set in the current socket
        if hasattr(self, "blocking") and not self.blocking:
            connection.setblocking(0)

        # tries to archive the proper handshake on the SSL
        # connection, asynchronous handshake
        connection.do_handshake()
    except socket.error as error:
        # in case the exception is normal, the operation did not
        # complete or the socket would block nothing should be done
        # and the handshake operation must be deferred to the next data
        # receiving "event"
        error_v = error.args[0] if error.args else None
        if error_v in (
            errno.EWOULDBLOCK,
            errno.EAGAIN,
            errno.EPERM,
            errno.ENOENT,
            WSAEWOULDBLOCK,
        ):
            # creates the error and populates it with the connection and the address
            # then raises it to the upper levels
            error = colony.OperationNotComplete("no handshake was possible")
            error.socket = connection
            error.connection = connection
            error.address = address
            raise error
        # otherwise it's a different kind of error and the connection
        # state is considered to be erroneous (must be closed)
        else:
            # closes the client connection (it's currently in an erroneous
            # state) and then re-raises the exception
            connection.close()
            raise
    except:
        # closes the client connection (it's currently in an erroneous
        # state) and then re-raises the exception
        connection.close()
        raise

    # returns the return value
    return return_value


def handshake(self):
    self.do_handshake()


def set_option(self, name, value):
    setattr(self, name, value)


def process_exception(self, exception):
    # in case the exception is of type socket error and the error
    # value is inside the list of valid error the exception is considered
    # valid and a valid value is returned
    if isinstance(exception, socket.error) and exception.args[0] in (
        errno.EWOULDBLOCK,
        errno.EAGAIN,
        errno.EPERM,
        errno.ENOENT,
        WSAEWOULDBLOCK,
    ):
        return True

    # in case the exception is of type SSL error and the error
    # number is SSL error want read or write, the exception must
    # be ignored as it means that an operation could not be immediately
    # performed and must be delayed
    if isinstance(exception, ssl.SSLError) and exception.errno in (
        SSL_ERROR_WANT_READ,
        SSL_ERROR_WANT_WRITE,
    ):
        return True

    # return false (exception must be processed) as no graceful
    # approach is possible for such exception
    return False
