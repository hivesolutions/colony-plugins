#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pecway Payment Gateway
# Copyright (C) 2010 Hive Solutions Lda.
#
# This file is part of Pecway Payment Gateway.
#
# Pecway Payment Gateway is confidential and property of Hive Solutions Lda.,
# its usage is constrained by the terms of the Hive Solutions
# Confidential Usage License.
#
# Pecway Payment Gateway should not be distributed under any circumstances,
# violation of this may imply legal action.
#
# If you have any questions regarding the terms of this license please
# refer to <http://www.hive.pt/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2010 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony.base.exceptions

class CryptonException(colony.base.exceptions.ColonyException):
    """
    The wen mvc encryption exception class.
    """

    message = None
    """ The exception's message """

class AccessDeniedException(CryptonException):
    """
    The access denied exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        CryptonException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Access denied exception - %s" % self.message
