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

import colony

class APIATException(colony.ColonyException):
    """
    The API AT exception class.
    """

    message = None
    """ The exception's message """

class ATAPIError(APIATException):
    """
    The AT API error class representing an error
    coming from the AT server.
    """

    error_code = None
    """ The code associated with the message contained
    in this API error """

    details = None
    """ An optional details value that will better
    describe the issue in detail, the data type of this
    attribute is dynamic and can be a dictionary or a string """

    def __init__(self, message, error_code = None, details = None):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        :type error_code: String
        :param error_code: The code associated with
        the message contained in this API error.
        :type details: String/Dictionary
        :param details: The details that describe this
        error for possible debugging.
        """

        APIATException.__init__(self)
        self.message = message
        self.error_code = error_code
        self.details = details

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "AT API error (%d) - %s" % (self.error_code, self.message) if\
            self.error_code else "AT API error - %s" % self.message

class ATVersionError(APIATException):

    def __init__(self, version = None):
        """
        Constructor of the class.

        :type version: int
        :param version: The version that is considered
        to be in error under the context.
        """

        APIATException.__init__(self)
        self.version = version

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "AT Version error - %d" % self.version if\
            self.version else "AT Version error"
