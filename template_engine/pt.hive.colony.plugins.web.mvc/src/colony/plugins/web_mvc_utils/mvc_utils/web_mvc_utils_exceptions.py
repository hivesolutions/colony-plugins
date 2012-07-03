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

import colony.base.plugin_system_exceptions

class WebMvcUtilsExceptionException(colony.base.plugin_system_exceptions.ColonyException):
    """
    The web mvc utils exception class.
    """

    message = None
    """ The exception's message """

class InvalidValidationMethod(WebMvcUtilsExceptionException):
    """
    The invalid validation method class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        WebMvcUtilsExceptionException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Invalid validation method - %s" % self.message

class InvalidAttributeName(WebMvcUtilsExceptionException):
    """
    The invalid attribute name class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        WebMvcUtilsExceptionException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Invalid attribute name - %s" % self.message

class InsufficientHttpInformation(WebMvcUtilsExceptionException):
    """
    The insufficient http information error class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        WebMvcUtilsExceptionException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Insufficient http information - %s" % self.message

class ModelValidationError(WebMvcUtilsExceptionException):
    """
    The model validation error class.
    """

    model = None
    """ The model that failed the validation """

    def __init__(self, message, model = None):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        @type model: Model
        @param model: The model that failed the validation.
        """

        WebMvcUtilsExceptionException.__init__(self)
        self.message = message
        self.model = model

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Model validation error - %s" % self.message

class ControllerValidationError(WebMvcUtilsExceptionException):
    """
    The controller validation error class.
    """

    controller = None
    """ The controller that failed the validation """

    def __init__(self, message, controller = None):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        @type controller: Controller
        @param controller: The controller that failed the validation.
        """

        WebMvcUtilsExceptionException.__init__(self)
        self.message = message
        self.controller = controller

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Controller validation error - %s" % self.message

class ControllerValidationReasonFailed(ControllerValidationError):
    """
    The controller validation reason failed class.
    """

    reasons_list = []
    """ The list of reasons for validation failure """

    def __init__(self, message, controller = None, reasons_list = []):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        @type controller: Controller
        @param controller: The controller that failed the validation.
        @type reasons_list: String
        @param reasons_list: The list of reasons for validation failure.
        """

        ControllerValidationError.__init__(self, message, controller)
        self.reasons_list = reasons_list

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Controller validation reason error - %s" % self.message

class ValidationMethodError(WebMvcUtilsExceptionException):
    """
    The validation method error class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        WebMvcUtilsExceptionException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Validation method error - %s" % self.message

class ModelApplyException(WebMvcUtilsExceptionException):
    """
    The model apply exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        WebMvcUtilsExceptionException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Model apply exception - %s" % self.message
