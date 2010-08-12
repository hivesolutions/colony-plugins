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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

class ServiceException(Exception):
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

        @type message: String
        @param message: The message to be printed.
        """

        BadServiceRequest.__init__(self)
        self.message = message

    def __repr__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Invalid token value: %s" % self.message

class MvcRequestNotHandled(BadServiceRequest):
    """
    The mvc request not handled class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        BadServiceRequest.__init__(self)
        self.message = message

    def __repr__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Mvc Request Not handled: %s" % self.message

class FileNotFoundException(MvcRequestNotHandled):
    """
    The file not found exception class.
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

        MvcRequestNotHandled.__init__(self, message)
        self.status_code = status_code

    def __repr__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "File not found: %s" % self.message

class InvalidCommunicationCommandException(MvcRequestNotHandled):
    """
    The invalid communication command exception class.
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

        MvcRequestNotHandled.__init__(self, message)
        self.status_code = status_code

    def __repr__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Invalid communication command: %s" % self.message

class CommunicationCommandException(MvcRequestNotHandled):
    """
    The communication command exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        MvcRequestNotHandled.__init__(self, message)

    def __repr__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Communication command exception: %s" % self.message
