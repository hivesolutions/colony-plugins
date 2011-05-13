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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 1070 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-01-21 19:19:20 +0000 (qua, 21 Jan 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.importer_util

ENTITY_MANAGER_VALUE = "entity_manager"
""" The entity manager value """

VALID_VALUE = "valid"
""" The valid value """

ENTITY_MANAGER_VALUE = "entity_manager"
""" The entity manager value """

LOGIN_ENTITY_NAME_VALUE = "login_entity_name"
""" The login entity name value """

USER_VALUE = "User"
""" The user value """

MAIN_AUTHENTICATION_PLUGIN_ID = "pt.hive.colony.plugins.main.authentication"
""" The main authentication plugin id """

MAIN_AUTHENTICATION_LOGIC_EXCEPTIONS_VALUE = "main_authentication_logic_exceptions"
""" The main authentication logic exceptions value """

# imports the main authentication logic exceptions decorator
main_authentication_logic_exceptions = colony.libs.importer_util.__importer__(MAIN_AUTHENTICATION_LOGIC_EXCEPTIONS_VALUE)

class AuthenticationLogic:

    def authenticate_user(self, username, password, arguments):
        # retrieves the main authentication plugin
        main_authentication_plugin = self.plugin_manager.get_plugin_by_id(MAIN_AUTHENTICATION_PLUGIN_ID)

        # raises an exception in case the plugin was not found
        if not main_authentication_plugin:
            # raises the main authentication logic exception
            raise main_authentication_logic_exceptions.MainAuthenticationLogicException("Main authentication plugin not found")

        # creates the arguments map in case it is not defined
        if not arguments:
            arguments = {}

        # sets the entity manager in the arguments map
        arguments[ENTITY_MANAGER_VALUE] = self.entity_manager

        # sets the login entity name in the arguments map
        arguments[LOGIN_ENTITY_NAME_VALUE] = USER_VALUE

        # authenticates the user retrieving the authentication result
        authentication_result = main_authentication_plugin.authenticate_user(username, password, ENTITY_MANAGER_VALUE, arguments)

        # retrieves the authentication result valid
        authentication_result_valid = authentication_result.get(VALID_VALUE, False)

        # in case the authentication result is valid
        if authentication_result_valid:
            # sets the authentication result in the session
            self._set_session_information(authentication_result)

        # returns the authentication result
        return authentication_result

    def process_authentication_string(self, authentication_string):
        # retrieves the main authentication plugin
        main_authentication_plugin = self.plugin_manager.get_plugin_by_id(MAIN_AUTHENTICATION_PLUGIN_ID)

        # raises an exception in case the plugin was not found
        if not main_authentication_plugin:
            # raises the main authentication logic exception
            raise main_authentication_logic_exceptions.MainAuthenticationLogicException("Main authentication plugin not found")

        # authenticates the user retrieving the authentication result
        authentication_result = main_authentication_plugin.process_authentication_string(authentication_string)

        # retrieves the authentication result valid
        authentication_result_valid = authentication_result.get(VALID_VALUE, False)

        # in case the authentication result is valid
        if authentication_result_valid:
            # sets the authentication result in the session
            self._set_session_information(authentication_result)

        # returns the authentication result
        return authentication_result

    def _set_session_information(self, authentication_result):
        # retrieves the current session information
        current_session_information = self.session_manager.get_current_session_information()

        # sets the authentication value of the session information as the authentication result
        current_session_information.set_session_property("authentication_value", authentication_result)

BUSINESS_LOGIC_CLASSES = [
    AuthenticationLogic
]
""" The business logic classes """
