#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class ServiceHTTPException(colony.ColonyException):
    """
    The service HTTP exception class.
    """

    message = None
    """ The exception's message """

class EncodingNotFound(ServiceHTTPException):
    """
    The encoding not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceHTTPException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Encoding not found - %s" % self.message

class ClientRequestSecurityViolation(ServiceHTTPException):
    """
    The client request security violation request timeout class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceHTTPException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Client request security violation - %s" % self.message

class HTTPRuntimeException(ServiceHTTPException):
    """
    The HTTP runtime exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        ServiceHTTPException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "HTTP runtime exception - %s" % self.message

class HTTPInvalidDataException(HTTPRuntimeException):
    """
    The HTTP invalid data exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        HTTPRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "HTTP invalid data exception - %s" % self.message

class HTTPNoHandlerException(HTTPRuntimeException):
    """
    The HTTP no handler exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        HTTPRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "HTTP no handler exception - %s" % self.message

class HTTPHandlerNotFoundException(HTTPRuntimeException):
    """
    The HTTP handler not found exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        HTTPRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "HTTP handler not found exception - %s" % self.message

class HTTPAuthenticationHandlerNotFoundException(HTTPRuntimeException):
    """
    The HTTP authentication handler not found exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        HTTPRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "HTTP authentication handler not found exception - %s" % self.message

class HTTPInvalidMultipartRequestException(HTTPRuntimeException):
    """
    The HTTP invalid multipart request exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        HTTPRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "HTTP invalid multipart request exception - %s" % self.message

class HTTPDataRetrievalException(HTTPRuntimeException):
    """
    The HTTP data retrieval exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        HTTPRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "HTTP data retrieval exception - %s" % self.message

class HTTPDataSendingException(HTTPRuntimeException):
    """
    The HTTP data sending exception.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        HTTPRuntimeException.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "HTTP data sending exception - %s" % self.message

class UnauthorizedException(HTTPRuntimeException):
    """
    The unauthorized exception class.
    """

    status_code = None
    """ The exceptions's status code """

    def __init__(self, message, status_code):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        :type status_code: int
        :param status_code: The HTTP status code.
        """

        HTTPRuntimeException.__init__(self, message)
        self.status_code = status_code

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Unauthorized - %s" % self.message
