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

class ServiceException(colony.ColonyException):
    """
    The service exception class.
    """

    message = None
    """ The exception's message """

class ServiceRequestNotTranslatable(ServiceException):
    """
    The service request not translatable class.
    """

    pass

class BadServiceRequest(ServiceException):
    """
    The bad service request class.
    """

    pass

class InvalidTokenValue(BadServiceRequest):
    """
    The invalid token value class.
    """

    def __init__(self, message, status_code):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        BadServiceRequest.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Invalid token value - %s" % self.message

class RuntimeRequestException(BadServiceRequest):
    """
    The runtime request exception class, meant to be
    used for problems occurring during the runtime of
    the handling of the request.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        BadServiceRequest.__init__(self, message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Runtime request exception - %s" % self.message

class MVCRequestNotHandled(BadServiceRequest):
    """
    The MVC request not handled class.
    """

    def __init__(self, message, status_code = 404):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        :type status_code: int
        :param status_code: The integer describing the status
        code that is going to be returned in the request.
        """

        BadServiceRequest.__init__(self)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "MVC Request Not handled - %s" % self.message

class FileNotFoundException(MVCRequestNotHandled):
    """
    The file not found exception class.
    """

    status_code = None
    """ The exceptions's status code """

    def __init__(self, message, status_code = 404):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        :type status_code: int
        :param status_code: The http status code.
        """

        MVCRequestNotHandled.__init__(self, message)
        self.status_code = status_code

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "File not found - %s" % self.message

class InvalidCommunicationCommandException(MVCRequestNotHandled):
    """
    The invalid communication command exception class.
    """

    status_code = None
    """ The exceptions's status code """

    def __init__(self, message, status_code):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        :type status_code: int
        :param status_code: The http status code.
        """

        MVCRequestNotHandled.__init__(self, message)
        self.status_code = status_code

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Invalid communication command - %s" % self.message

class CommunicationCommandException(MVCRequestNotHandled):
    """
    The communication command exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        MVCRequestNotHandled.__init__(self, message)

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Communication command exception - %s" % self.message
