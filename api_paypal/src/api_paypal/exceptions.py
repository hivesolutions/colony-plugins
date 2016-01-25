#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class ApiPaypalException(colony.ColonyException):
    """
    The api paypal exception class.
    """

    message = None
    """ The exception's message """

class PaypalApiError(ApiPaypalException):
    """
    The paypal api error class.
    """

    long_message = None
    """ The longer version of the error message present
    by the paypal api """

    def __init__(self, message, long_message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        @type long_message: String
        @param long_message: The longer version of the
        error message present by the paypal api.
        """

        ApiPaypalException.__init__(self)
        self.message = message
        self.long_message = long_message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Paypal api error - %s" % self.message
