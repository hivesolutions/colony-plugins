#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class ServiceHttpProxyException(colony.ColonyException):
    """
    The service http proxy exception class.
    """

    message = None
    """ The exception's message """

class HttpProxyRuntimeException(ServiceHttpProxyException):
    """
    The http proxy runtime exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        ServiceHttpProxyException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Http proxy runtime - %s" % self.message

class HttpClientUnavailableException(ServiceHttpProxyException):
    """
    The http client unavailable exception class.
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

        ServiceHttpProxyException.__init__(self)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Http client unavailable - %s" % self.message
