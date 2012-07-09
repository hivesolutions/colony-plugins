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

__date__ = "$LastChangedDate: 2011-01-15 17:29:58 +0000 (sÃ¡b, 15 Jan 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import exceptions

AUTHENTICATION_HANDLER_VALUE = "authentication_handler"
""" The authentication handler value """

ARGUMENTS_VALUE = "arguments"
""" the arguments value """

class ConsoleAuthentication:
    """
    The console authentication class.
    """

    console_plugin = None
    """ The console plugin """

    def __init__(self, console_plugin):
        """
        Constructor of the class.

        @type console_plugin: ConsolePlugin
        @param console_plugin: The console plugin.
        """

        self.console_plugin = console_plugin

    def handle_authentication(self, username, password, properties = {}):
        """
        Handles the given console authentication.

        @type username: String
        @param username: The username to be used in the authentication.
        @type password: String
        @param password: The password to be used in the authentication.
        @type properties: Dictionary
        @param properties: The properties used in the authentication process.
        @rtype: Dictionary
        @return: The authentication result.
        """

        # in case the authentication handler property is not defined
        # must raise the missing property exception
        if not AUTHENTICATION_HANDLER_VALUE in properties:
            raise exceptions.MissingProperty(AUTHENTICATION_HANDLER_VALUE)

        # in case the arguments property is not defined must raise the
        # missing property exception
        if not ARGUMENTS_VALUE in properties:
            raise exceptions.MissingProperty(ARGUMENTS_VALUE)

        # retrieves the various property elements from the provided
        # map of properties, this should include the authentication
        # handler and the arguments for authentication
        authentication_handler = properties[AUTHENTICATION_HANDLER_VALUE]
        arguments = properties[ARGUMENTS_VALUE]

        # retrieves the authentication plugin and uses it to try
        # to authenticate the current user retrieving the result
        authentication_plugin = self.console_plugin.authentication_plugin
        authentication_result = authentication_plugin.authenticate_user(username, password, authentication_handler, arguments)

        # returns the authentication result
        return authentication_result
