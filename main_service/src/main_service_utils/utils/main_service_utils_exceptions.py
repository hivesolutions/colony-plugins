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

import colony.base.exceptions

class MainServiceUtilsException(colony.base.exceptions.ColonyException):
    """
    The main service utils exception class.
    """

    message = None
    """ The exception's message """

class SocketProviderNotFound(MainServiceUtilsException):
    """
    The socket provider not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Socket provider not found - %s" % self.message

class SocketUpgraderNotFound(MainServiceUtilsException):
    """
    The socket upgrader not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Socket upgrader not found - %s" % self.message

class ServerRequestTimeout(MainServiceUtilsException):
    """
    The server request timeout class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Server request timeout - %s" % self.message

class ClientRequestTimeout(MainServiceUtilsException):
    """
    The client request timeout class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Client request timeout - %s" % self.message

class ServerResponseTimeout(MainServiceUtilsException):
    """
    The server response timeout class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Server response timeout - %s" % self.message

class ClientResponseTimeout(MainServiceUtilsException):
    """
    The client response timeout class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Client response timeout - %s" % self.message

class RequestClosed(MainServiceUtilsException):
    """
    The request closed class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Request closed - %s" % self.message

class PortStarvationReached(MainServiceUtilsException):
    """
    The port starvation reached class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Port starvation reached - %s" % self.message

class ConnectionChangeFailure(MainServiceUtilsException):
    """
    The connection change failure class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceUtilsException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Connection change failure - %s" % self.message
