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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 7125 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-12-21 10:43:24 +0000 (seg, 21 Dez 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system_exceptions

class EntityManagerException(colony.plugins.plugin_system_exceptions.ColonyException):
    """
    The entity manager exception class.
    """

    message = None
    """ The exception's message """

class EntityManagerEngineNotFound(EntityManagerException):
    """
    The entity manager engine not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        EntityManagerException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Entity Manager engine not found: %s" % self.message

class EntityManagerEngineDuplicateEntry(EntityManagerException):
    """
    The entity manager engine duplicate entry class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        EntityManagerException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Duplicate entry: %s" % self.message

class EntityManagerEngineEntryNotFound(EntityManagerException):
    """
    The entity manager engine entry not found class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        @type message: String
        @param message: The message to be printed.
        """

        EntityManagerException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        @rtype: String
        @return: The string representation of the class.
        """

        return "Entry not found: %s" % self.message
