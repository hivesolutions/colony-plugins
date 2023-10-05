#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import errno
import socket

import colony

PROVIDER_NAME = "raw"
""" The provider name """

WSAEWOULDBLOCK = 10035
""" Windows based value for the error raised when a non
blocking connection is not able to read/write more, this
error should be raised constantly in no blocking connections """

class RawSocket(colony.System):
    """
    The raw socket (provider) class.
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

        # creates the raw socket
        raw_socket = self.provide_socket_parameters()

        # returns the raw socket
        return raw_socket

    def provide_socket_parameters(self, parameters = {}):
        """
        Provides a new socket, configured with
        the given parameters.

        :type parameters: Dictionary
        :param parameters: The parameters for socket configuration.
        :rtype: Socket
        :return: The provided socket.
        """

        # prints a debug message
        self.plugin.debug("Providing a raw socket")

        # tries to retrieve the socket family
        socket_family = parameters.get("family", socket.AF_INET)

        # creates the raw socket
        raw_socket = socket.socket(socket_family, socket.SOCK_RAW)

        # returns the raw socket
        return raw_socket

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

def process_exception(self, exception):
    # in case the exception is of type socket error and the error
    # value is inside the list of valid error the exception is considered
    # valid and a valid value is returned
    if isinstance(exception, socket.error) and\
        exception.args[0] in (
            errno.EWOULDBLOCK,
            errno.EAGAIN,
            errno.EPERM,
            errno.ENOENT,
            WSAEWOULDBLOCK
        ):
        return True

    # return false (exception must be processed) as no graceful
    # approach is possible for such exception
    return False
