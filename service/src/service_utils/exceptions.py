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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony


class ServiceUtilsException(colony.ColonyException):
    """
    The service utils exception class.
    """

    message = None
    """ The exception's message """


class SocketProviderNotFound(ServiceUtilsException):
    """
    The socket provider not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Socket provider not found - %s" % self.message


class SocketUpgraderNotFound(ServiceUtilsException):
    """
    The socket upgrader not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Socket upgrader not found - %s" % self.message


class ServerRequestTimeout(ServiceUtilsException):
    """
    The server request timeout class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Server request timeout - %s" % self.message


class ClientRequestTimeout(ServiceUtilsException):
    """
    The client request timeout class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Client request timeout - %s" % self.message


class ServerResponseTimeout(ServiceUtilsException):
    """
    The server response timeout class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Server response timeout - %s" % self.message


class ClientResponseTimeout(ServiceUtilsException):
    """
    The client response timeout class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Client response timeout - %s" % self.message


class RequestClosed(ServiceUtilsException):
    """
    The request closed class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Request closed - %s" % self.message


class PortStarvationReached(ServiceUtilsException):
    """
    The port starvation reached class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Port starvation reached - %s" % self.message


class ConnectionChangeFailure(ServiceUtilsException):
    """
    The connection change failure class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Connection change failure - %s" % self.message
