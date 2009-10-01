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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class ParserGeneratorException(Exception):
    """
    The parser generator exception class.
    """

    pass

class InvalidState(ParserGeneratorException):
    """
    The invalid state exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        ParserGeneratorException.__init__(self, message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Invalid State: %s" % self.message

class ParsingConflict(ParserGeneratorException):
    """
    The parsing conflict class.
    """

    item_set = None
    """ The conflict item set """

    def __init__(self, message, item_set = None):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        @type item_set: ItemSet
        @param item_set: The conflict item set.
        """

        ParserGeneratorException.__init__(self)
        self.message = message
        self.item_set = item_set

    def get_item_set(self):
        """
        Retrieves the conflict item set.

        @rtype: ItemSet
        @return: The conflict item set.
        """

        return self.item_set

    def set_item_set(self, item_set):
        """
        Sets the conflict item set.

        @type item_set: ItemSet
        @param item_set: The conflict item set.
        """

        self.item_set = item_set

class ShiftReduceConflict(ParsingConflict):
    """
    The shift reduce conflict class.
    """

    def __init__(self, message, item_set = None):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        @type item_set: ItemSet
        @param item_set: The conflict item set.
        """

        ParsingConflict.__init__(self, message, item_set)

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        # in case there is an item set defined
        if self.item_set:
            # retrieves the item set string
            item_set_string = self.item_set._get_item_set_string()

            return "Shift reduce conflict: %s\nItem set summary:\n%s" % (self.message, item_set_string)
        else:
            return "Shift reduce conflict: %s" % self.message

class ReduceReduceConflict(ParsingConflict):
    """
    The shift reduce conflict class.
    """

    def __init__(self, message, item_set = None):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        @type item_set: ItemSet
        @param item_set: The conflict item set.
        """

        ParsingConflict.__init__(self, message, item_set)

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        # in case there is an item set defined
        if self.item_set:
            # retrieves the item set string
            item_set_string = self.item_set._get_item_set_string()

            return "Reduce reduce conflict: %s\nItem set summary:\n%s" % (self.message, item_set_string)
        else:
            return "Reduce reduce conflict: %s" % self.message
