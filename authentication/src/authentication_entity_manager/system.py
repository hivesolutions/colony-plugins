#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

from . import exceptions

HANDLER_NAME = "entity_manager"
""" The handler name """

ENTITY_MANAGER_VALUE = "entity_manager"
""" The entity manager value """

LOGIN_ENTITY_NAME_VALUE = "login_entity_name"
""" The login entity name value """

LOGIN_SALT_VALUE = "login_salt"
""" The login salt value """

class AuthenticationEntityManager(colony.System):
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

        # retrieves the complete set of values that are going
        # to be used for the authentication process
        username = request.get_username()
        password = request.get_password()
        arguments = request.get_arguments()

        # in case the entity manager in not defined in arguments
        # raises an exception indicating the miss of the manager
        if not ENTITY_MANAGER_VALUE in arguments:
            raise exceptions.MissingArgument(ENTITY_MANAGER_VALUE)

        # in case the local entity name value in not defined in arguments
        # must raises an exception because that's required
        if not LOGIN_ENTITY_NAME_VALUE in arguments:
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
        # an authentication error must be raised
        if not username or not password:
            raise exceptions.AuthenticationError("an username and a password must be provided")

        # retrieves the users that match the authentication parameters
        # and retrieves the first user as the possible valid one, defaulting
        # to an invalid/unset value in case no entities exist
        users = entity_manager.find(login_entity_class, username = username)
        user = users[0] if users else None

        # in case the user was not found an authentication
        # error must be raised about the issue
        if not user: raise exceptions.AuthenticationError("user not found")

        # checks that the password is valid
        password_valid = colony.password_match(user.password_hash, password, login_salt)

        # in case the password is valid, creates the return
        # value as a map containing some of the user data
        if password_valid: return_value = dict(
            valid = True,
            username = username
        )
        # otherwise there is no valid username password
        # combination and raises an exception
        else:
            raise exceptions.AuthenticationError("invalid username password combination")

        # returns the return value
        return return_value
