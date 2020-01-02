#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from . import exceptions

HANDLER_NAME = "main"
""" The handler name """

AUTHENTICATION_HANDLER_VALUE = "authentication_handler"
""" The authentication handler value """

ARGUMENTS_VALUE = "arguments"
""" The arguments value """

class ServiceHTTPAuthentication(colony.System):
    """
    The service HTTP authentication (handler) class.
    """

    def get_handler_name(self):
        """
        Retrieves the handler name.

        :rtype: String
        :return: The handler name.
        """

        return HANDLER_NAME

    def handle_authentication(self, username, password, properties):
        """
        Handles the given HTTP authentication.

        :type username: String
        :param username: The username to be used in the authentication.
        :type password: String
        :param password: The password to be used in the authentication.
        :type properties: Dictionary
        :param properties: The properties used in the authentication process.
        :rtype: Dictionary
        :return: The authentication result.
        """

        # in case the authentication handler property is not defined
        if not AUTHENTICATION_HANDLER_VALUE in properties:
            # raises the missing property exception
            raise exceptions.MissingProperty(AUTHENTICATION_HANDLER_VALUE)

        # in case the arguments property is not defined
        if not ARGUMENTS_VALUE in properties:
            # raises the missing property exception
            raise exceptions.MissingProperty(ARGUMENTS_VALUE)

        # retrieves the authentication handler
        authentication_handler = properties[AUTHENTICATION_HANDLER_VALUE]

        # retrieves the arguments
        arguments = properties[ARGUMENTS_VALUE]

        # retrieves the authentication plugin
        authentication_plugin = self.plugin.authentication_plugin

        # authenticates the user with the authentication plugin retrieving the result
        authentication_result = authentication_plugin.authenticate_user(username, password, authentication_handler, arguments)

        # returns the authentication result
        return authentication_result
