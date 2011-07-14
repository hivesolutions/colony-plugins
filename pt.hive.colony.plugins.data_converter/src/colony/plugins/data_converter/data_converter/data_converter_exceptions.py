#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2300 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:10:15 +0100 (Wed, 01 Apr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system_exceptions

class DataConverterException(colony.base.plugin_system_exceptions.ColonyException):
    """
    The data converter exception class.
    """

    message = None
    """ The exception's message """

class DataConverterConfigurationPluginNotFound(DataConverterException):
    """
    The data converter configuration plugin not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data Converter configuration plugin not found: %s" % self.message

class DataConverterConfigurationNotFound(DataConverterException):
    """
    The data converter configuration not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data Converter configuration not found: %s" % self.message

class DataConverterConfigurationOptionNotFound(DataConverterException):
    """
    The data converter configuration option not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data Converter configuration option not found: %s" % self.message

class DataConverterOperationNotImplemented(DataConverterException):
    """
    The data converter operation not implemented class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        DataConverterException.__init__(self)

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data Converter operation not implemented"

class DataConverterMandatoryOptionNotFound(DataConverterException):
    """
    The data converter option not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data Converter mandatory option not found: %s" % self.message

class DataConverterIoAdapterPluginNotFound(DataConverterException):
    """
    The data converter io adapter plugin not found option class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data Converter input output adapter plugin not found: %s" % self.message

class DataConverterIndexElementTypeUnknown(DataConverterException):
    """
    The data converter index element type unknown class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data Converter index element type is unknown: %s" % self.message

class DataConverterEntityNotFound(DataConverterException):
    """
    The data converter entity not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data Converter entity not found: %s" % self.message

class DataConverterCreatorInputEntityNotFound(DataConverterException):
    """
    The data converter creator input entity not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data Converter creator input entity not found: %s" % self.message

class DataConverterUnexpectedNumberInputEntitiesException(DataConverterException):
    """
    The data converter unexpected number of input entities exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data Converter number of retrieved input entities was unexpected: %s" % self.message

class IntermediateStructureEntityNotFound(DataConverterException):
    """
    The intermediate structure entity not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Intermediate Structure entity not found: %s" % self.message

class IntermediateStructureEntityNameAlreadyAllocated(DataConverterException):
    """
    The intermediate structure entity name already allocated class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Intermediate Structure entity name already allocated: %s" % self.message

class IntermediateStructureEntityNotAllowed(DataConverterException):
    """
    The intermediate structure entity not allowed class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Intermediate Structure entity not allowed: %s" % self.message

class IntermediateStructureEntityAttributeNotFound(DataConverterException):
    """
    The intermediate structure entity attribute not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Intermediate Structure entity attribute was not found: %s" % self.message

class IntermediateStructureEntityAttributeNotAllowed(DataConverterException):
    """
    The intermediate structure entity attribute not allowed class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Intermediate Structure entity attribute is not allowed: %s" % self.message

class IntermediateStructureEntityAttributeDataTypeNotAllowed(DataConverterException):
    """
    The intermediate structure entity attribute data type is not allowed class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Intermediate Structure entity attribute data type is not allowed: %s" % self.message

class IntermediateStructureIndexOccupied(DataConverterException):
    """
    The intermediate structure index occupied class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Intermediate Structure index is occupied: %s" % self.message

class IntermediateStructureIndexNotTuple(DataConverterException):
    """
    The intermediate structure index not tuple class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Intermediate Structure index is not a tuple: %s" % self.message

class DataConverterConfigurationOutputEntityNotDefined(DataConverterException):
    """
    The data converter configuration output entity not defined exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration output entity is not defined: %s" % self.message

class DataConverterConfigurationOutputAttributeNameAlreadyDefined(DataConverterException):
    """
    The data converter configuration output attribute name already defined exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration output attribute name is already defined: %s" % self.message

class DataConverterConfigurationIoAdapterOptionAlreadyDefined(DataConverterException):
    """
    The data converter configuration io adapter option already defined exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration io adapter option is already defined: %s" % self.message

class DataConverterConfigurationInputEntityNotDefined(DataConverterException):
    """
    The data converter configuration input entity not defined exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration input entity was not defined: %s" % self.message

class DataConverterConfigurationOutputAttributeNotDefined(DataConverterException):
    """
    The data converter configuration output attribute not defined exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration output attribute was not defined: %s" % self.message

class DataConverterConfigurationDefaultValueAlreadyDefined(DataConverterException):
    """
    The data converter configuration default value already defined exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration default value was already defined: %s" % self.message

class DataConverterConfigurationInputAttributeNameAlreadyDefined(DataConverterException):
    """
    The data converter configuration input attribute name already defined exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration input attribute name was already defined: %s" % self.message

class DataConverterConfigurationConfigurationItemTypeNotDefined(DataConverterException):
    """
    The data converter configuration configuration item type not defined exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration configuration item type was not defined: %s" % self.message

class DataConverterConfigurationConfigurationItemNotDefined(DataConverterException):
    """
    The data converter configuration configuration item not defined exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration configuration item was not defined: %s" % self.message

class DataConverterConfigurationConfigurationItemAlreadyEnabled(DataConverterException):
    """
    The data converter configuration item already enabled exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration configuration item was already enabled: %s" % self.message

class DataConverterConfigurationConfigurationItemAlreadyDisabled(DataConverterException):
    """
    The data converter configuration item already disabled exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration configuration item was already disabled: %s" % self.message

class DataConverterConfigurationConfigurationItemTypeNotRecognized(DataConverterException):
    """
    The data converter configuration item type not recognized exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        DataConverterException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Data converter configuration configuration item type was not recognized: %s" % self.message
