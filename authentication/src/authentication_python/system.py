#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from . import exceptions

HANDLER_NAME = "python"
""" The handler name """

CONFIGURATION_PATH = "authentication_python/configuration"
""" The configuration path """

FILE_PATH_VALUE = "file_path"
""" The file path value """

USERNAME_VALUE = "username"
""" The username value """

PASSWORD_VALUE = "password"
""" The password value """

VALID_VALUE = "valid"
""" The valid value """

AUTHENTICATION_CONFIGURATION_VALUE = "authentication_configuration"
""" The authentication configuration value """

class AuthenticationPython(colony.System):
    """
    The authentication python class.
    """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.create_default_file()

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request):
        """
        Authenticates a user in the general service.

        @type request: AuthenticationRequest
        @param request: The authentication request to be handled.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the request username
        username = request.get_username()

        # retrieves the request password
        password = request.get_password()

        # retrieves the request arguments
        arguments = request.get_arguments()

        # in case the username or password are not defined
        if not username or not password:
            # raises an authentication error
            raise exceptions.AuthenticationError("an username and a password must be provided")

        # in case the file path in not defined in arguments
        if not FILE_PATH_VALUE in arguments:
            # raises an exception
            raise exceptions.MissingArgument(FILE_PATH_VALUE)

        # retrieves the file path
        file_path = arguments[FILE_PATH_VALUE]

        # resolves the file path
        file_path = plugin_manager.resolve_file_path(file_path)

        # creates the symbols map to be used in the interpretation
        # of the file as the locals and globals map
        symbols_map = {}

        # interprets the python file path with the symbols map
        colony.legacy.execfile(file_path, symbols_map, symbols_map)

        # tries to retrieve the authentication configuration
        authentication_configuration = symbols_map.get(AUTHENTICATION_CONFIGURATION_VALUE, {})

        # retrieves the user authentication configuration
        user_authentication_configuration = authentication_configuration.get(username, None)

        # in case no user authentication configuration is defined
        if not user_authentication_configuration:
            # raises the authentication error
            raise exceptions.AuthenticationError("user not found")

        # retrieves the user password from the user authentication
        # configuration
        user_password = user_authentication_configuration.get(PASSWORD_VALUE, None)

        # in case the user password matches the one
        # in the configuration and is valid
        if not user_password or not user_password == password:
            # raises the authentication error
            raise exceptions.AuthenticationError("password mismatch")

        # creates the return value
        return_value = {
            VALID_VALUE : True,
            USERNAME_VALUE : username
        }

        # returns the return value
        return return_value

    def create_default_file(self):
        """
        Creates the default file in the default configuration
        file in case it's necessary.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the plugin id
        plugin_id = self.plugin.id

        # resolves the configuration file path
        configuration_file_path = plugin_manager.resolve_file_path("%configuration:" + plugin_id + "%/authentication.py", True)

        # retrieves the authentication plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(plugin_id)

        # creates the authentication configuration file path
        authentication_configuration_file_path = plugin_path + "/" + CONFIGURATION_PATH + "/authentication_configuration.py"

        # ensures that the configuration file path exists and contains the default contents
        colony.ensure_file_path(configuration_file_path, authentication_configuration_file_path)
