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

import colony.base.system
import colony.libs.crypt_util

import exceptions

HANDLER_NAME = "entity_manager"
""" The handler name """

USERNAME_VALUE = "username"
""" The username value """

VALID_VALUE = "valid"
""" The valid value """

ENTITY_MANAGER_VALUE = "entity_manager"
""" The entity manager value """

LOGIN_ENTITY_NAME_VALUE = "login_entity_name"
""" The login entity name value """

LOGIN_SALT_VALUE = "login_salt"
""" The login salt value """

class AuthenticationEntityManager(colony.base.system.System):
    """
    The authentication entity manager class.
    """

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

        # retrieves the request username
        username = request.get_username()

        # retrieves the request password
        password = request.get_password()

        # retrieves the request arguments
        arguments = request.get_arguments()

        # in case the entity manager in not defined in arguments
        if not ENTITY_MANAGER_VALUE in arguments:
            # raises an exception
            raise exceptions.MissingArgument(ENTITY_MANAGER_VALUE)

        # in case the local entity name value in not defined in arguments
        if not LOGIN_ENTITY_NAME_VALUE in arguments:
            # raises an exception
            raise exceptions.MissingArgument(LOGIN_ENTITY_NAME_VALUE)

        # retrieves the entity manager
        entity_manager = arguments[ENTITY_MANAGER_VALUE]

        # retrieves the login salt
        login_salt = arguments.get(LOGIN_SALT_VALUE, "")

        # retrieves the login entity name
        login_entity_name = arguments[LOGIN_ENTITY_NAME_VALUE]

        # retrieves the login entity class
        login_entity_class = entity_manager.get_entity_class(login_entity_name)

        # in case the username or password are not defined
        if not username or not password:
            # raises an authentication error
            raise exceptions.AuthenticationError("an username and a password must be provided")

        # creates the filter map
        filter = {
            "username" : username
        }

        # retrieves the users that match the authentication parameters
        user_entities = entity_manager.find(login_entity_class, filter)

        # retrieves the user
        user_entity = user_entities and user_entities[0] or None

        # in case the user was not found
        if not user_entity:
            # raises an authentication error
            raise exceptions.AuthenticationError("user not found")

        # checks that the password is valid
        password_valid = colony.libs.crypt_util.password_match(user_entity.password_hash, password, login_salt)

        # in case the password is valid
        if password_valid:
            # creates the return value
            return_value = {
                VALID_VALUE : True,
                USERNAME_VALUE : username
            }
        # otherwise there is no valid username password
        # combination
        else:
            # raises the authentication error
            raise exceptions.AuthenticationError("invalid username password combination")

        # returns the return value
        return return_value
