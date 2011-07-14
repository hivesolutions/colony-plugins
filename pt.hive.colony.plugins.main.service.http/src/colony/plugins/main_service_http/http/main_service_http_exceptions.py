#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system_exceptions

class MainServiceHttpException(colony.base.plugin_system_exceptions.ColonyException):
    """
    The main service http exception class.
    """

    message = None
    """ The exception's message """

class EncodingNotFound(MainServiceHttpException):
    """
    The encoding not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceHttpException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Encoding not found: %s" % self.message

class ClientRequestSecurityViolation(MainServiceHttpException):
    """
    The client request security violation request timeout class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceHttpException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Client request security violation: %s" % self.message

class HttpRuntimeException(MainServiceHttpException):
    """
    The http runtime exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MainServiceHttpException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Http runtime exception: %s" % self.message

class HttpInvalidDataException(HttpRuntimeException):
    """
    The http invalid data exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        HttpRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Http invalid data exception: %s" % self.message

class HttpNoHandlerException(HttpRuntimeException):
    """
    The http no handler exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        HttpRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Http no handler exception: %s" % self.message

class HttpHandlerNotFoundException(HttpRuntimeException):
    """
    The http handler not found exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        HttpRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Http handler not found exception: %s" % self.message

class HttpAuthenticationHandlerNotFoundException(HttpRuntimeException):
    """
    The http authentication handler not found exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        HttpRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Http authentication handler not found exception: %s" % self.message

class HttpInvalidMultipartRequestException(HttpRuntimeException):
    """
    The http invalid multipart request exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        HttpRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Http invalid multipart request exception: %s" % self.message

class HttpDataRetrievalException(HttpRuntimeException):
    """
    The http data retrieval exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        HttpRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Http data retrieval exception: %s" % self.message

class HttpDataSendingException(HttpRuntimeException):
    """
    The http data sending exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        HttpRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Http data sending exception: %s" % self.message

class UnauthorizedException(HttpRuntimeException):
    """
    The unauthorized exception class.
    """

    status_code = None
    """ The exceptions's status code """

    def __init__(self, message, status_code):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        @type status_code: int
        @param status_code: The http status code.
        """

        HttpRuntimeException.__init__(self, message)
        self.status_code = status_code

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Unauthorized: %s" % self.message
