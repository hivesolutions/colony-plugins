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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import hashlib

import main_authentication_entity_manager_handler_exceptions

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

PASSWORD_HASH_TYPE_VALUE = "password_hash_type"
""" The password hash type value """

class MainAuthenticationEntityManagerHandler:
    """
    The main authentication entity manager handler class.
    """

    main_authentication_entity_manager_handler_plugin = None
    """ The main authentication entity manager handler plugin """

    def __init__(self, main_authentication_entity_manager_handler_plugin):
        """
        Constructor of the class.

        @type main_authentication_entity_manager_handler_plugin: MainAuthenticationEntityManagerHandlerPlugin
        @param main_authentication_entity_manager_handler_plugin: The main authentication entity manager handler plugin.
        """

        self.main_authentication_entity_manager_handler_plugin = main_authentication_entity_manager_handler_plugin

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
            raise main_authentication_entity_manager_handler_exceptions.MissingArgument(ENTITY_MANAGER_VALUE)

        # in case the local entity name value in not defined in arguments
        if not LOGIN_ENTITY_NAME_VALUE in arguments:
            # raises an exception
            raise main_authentication_entity_manager_handler_exceptions.MissingArgument(LOGIN_ENTITY_NAME_VALUE)

        # retrieves the entity manager
        entity_manager = arguments[ENTITY_MANAGER_VALUE]

        # retrieves the login entity name
        login_entity_name = arguments[LOGIN_ENTITY_NAME_VALUE]

        # retrieves the password hash type
        password_hash_type = arguments.get(PASSWORD_HASH_TYPE_VALUE, None)

        # in case the hash type is defined
        if password_hash_type:
            # creates the password hash for the given
            # password hash type
            password_hash = hashlib.new(password_hash_type)

            # updates the password hash
            password_hash.update(password)

            # retrieves the password hash value
            password = password_hash.hexdigest()

        # retrieves the login entity class
        login_entity_class = entity_manager.get_entity_class(login_entity_name)

        # creates the find options
        find_options = {
            "filters" : (
                {
                    "filter_type" : "equals",
                    "filter_fields" : (
                        {
                            "field_name" : "username",
                            "field_value" : username
                        },
                    )
                },
                {
                    "filter_type" : "equals",
                    "filter_fields" : (
                        {
                            "field_name" : "password_hash",
                            "field_value" : password
                        },
                    )
                }
            )
        }

        # finds all options in the entity manager
        user_entities = entity_manager._find_all_options(login_entity_class, find_options)

        # in case there are user entities defined
        if user_entities:
            # creates the return value
            return_value = {
                VALID_VALUE : True,
                USERNAME_VALUE : username
            }
        # otherwise there is no valid username password
        # combination
        else:
            # raises the authentication error
            raise main_authentication_entity_manager_handler_exceptions.AuthenticationError("invalid username password combination")

        # returns the return value
        return return_value
