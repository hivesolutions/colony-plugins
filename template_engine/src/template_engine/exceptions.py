#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2018 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class TemplateEngineException(colony.ColonyException):
    """
    The template engine exception class. This is
    the top level exception class from which all
    other exceptions/errors must inherit.
    """

    message = None
    """ The exception's message """

class RuntimeError(TemplateEngineException):
    """
    The runtime error class.
    Should be used for general exceptions resulting from
    the runtime execution of the template engine.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        TemplateEngineException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Runtime error - %s" % self.message

class UndefinedVariable(TemplateEngineException):
    """
    The undefined variable class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        TemplateEngineException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Undefined variable - %s" % self.message

class UndefinedReference(TemplateEngineException):
    """
    The undefined reference class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        TemplateEngineException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Undefined reference - %s" % self.message

class VariableNotIterable(TemplateEngineException):
    """
    The variable not iterable class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        TemplateEngineException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Variable not iterable - %s" % self.message

class InvalidNumberAttributes(TemplateEngineException):
    """
    The invalid number attributes class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        TemplateEngineException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Invalid number attributes - %s" % self.message

class InvalidBooleanValue(TemplateEngineException):
    """
    The invalid boolean value class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        TemplateEngineException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Invalid boolean value - %s" % self.message

class InvalidSerializer(TemplateEngineException):
    """
    The invalid serializer class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        TemplateEngineException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Invalid serializer - %s" % self.message
