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

class EntityManagerException(colony.ColonyException):
    """
    The entity manager exception class.
    """

    message = None
    """ The exception's message """

class RuntimeError(EntityManagerException):
    """
    The entity manager runtime error class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        EntityManagerException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Runtime error - %s" % self.message

class EntityManagerEngineNotFound(EntityManagerException):
    """
    The entity manager engine not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        EntityManagerException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Engine not found - %s" % self.message

class MissingRelationMethod(EntityManagerException):
    """
    The entity manager missing relation method class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        EntityManagerException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Missing relation method - %s" % self.message

class ValidationError(EntityManagerException):
    """
    The entity manager validation error class.
    """

    context = None
    """ The context in which the validation issue has been
    generated, provides extra debug support """

    def __init__(self, message, context = None):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        :type context: Object
        :param context: The context (object) for the validation
        issue, this will provide extra information for debug
        purposes allowing for fast context
        """

        EntityManagerException.__init__(self)
        self.message = message
        self.context = context

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Validation error - %s" % self._get_message()

    def _get_message(self):
        if not self.message: return self.message
        if not self.context: return self.message
        return "(%s) %s" % (self.context, self.message)

class RelationValidationError(ValidationError):
    """
    The entity manager relation validation error class.
    """

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Relation validation error - %s" % self._get_message()

class InvalidSerializerError(ValidationError):
    """
    The invalid serializer error class.
    """

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Invalid serializer error - %s" % self._get_message()
