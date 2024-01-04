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


class APIPaypalException(colony.ColonyException):
    """
    The API PayPal exception class.
    """

    message = None
    """ The exception's message """


class PaypalAPIError(APIPaypalException):
    """
    The PayPal API error class.
    """

    long_message = None
    """ The longer version of the error message present
    by the PayPal API """

    def __init__(self, message, long_message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        :type long_message: String
        :param long_message: The longer version of the
        error message present by the PayPal API.
        """

        APIPaypalException.__init__(self)
        self.message = message
        self.long_message = long_message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "PayPal API error - %s" % self.message
