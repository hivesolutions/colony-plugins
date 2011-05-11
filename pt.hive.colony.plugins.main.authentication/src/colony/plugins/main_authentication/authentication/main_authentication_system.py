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

import sys
import traceback

import colony.libs.string_util

VALID_VALUE = "valid"
""" The valid value """

EXCEPTION_VALUE = "exception"
""" The exception value """

EXCEPTION_REFERENCE_VALUE = "exception_reference"
""" The exception reference value """

EXCEPTION_NAME_VALUE = "exception_name"
""" The exception name value """

MESSAGE_VALUE = "message"
""" The message value """

TRACEBACK_VALUE = "traceback"
""" The traceback value """

NO_AUTHENTICATION_METHOD_MESSAGE = "no authentication method found"
""" The no authentication method found message """

class MainAuthentication:
    """
    The main authentication class.
    """

    main_authentication_plugin = None
    """ The main authentication plugin """

    def __init__(self, main_authentication_plugin):
        """
        Constructor of the class.

        @type main_authentication_plugin: MainAuthenticationPlugin
        @param main_authentication_plugin: The main authentication plugin.
        """

        self.main_authentication_plugin = main_authentication_plugin

    def authenticate_user(self, username, password, authentication_handler, arguments):
        """
        Authenticates a user in the general service.

        @type username: String
        @param username: The username to be used in the authentication.
        @type password: String
        @param password: The password to be used in the authentication.
        @type authentication_handler: String
        @param authentication_handler: The authentication handler to be used in the authentication.
        @type arguments: Dictionary
        @param arguments: The arguments to be used in the authentication.
        @rtype: Dictionary
        @return: The authentication return value.
        """

        # creates the authentication request object
        authentication_request = AuthenticationRequest()

        # sets the username in the authentication request
        authentication_request.set_username(username)

        # sets the password in the authentication request
        authentication_request.set_password(password)

        # sets the authentication handler in the authentication request
        authentication_request.set_authentication_handler(authentication_handler)

        # sets the arguments in the authentication request
        authentication_request.set_arguments(arguments)

        # iterates over all the authentication handler plugins
        for authentication_handler_plugin in self.main_authentication_plugin.authentication_handler_plugins:
            # retrieves the authentication handler plugin handler name
            authentication_handler_plugin_handler_name = authentication_handler_plugin.get_handler_name()

            # in case the handler name is not the same as the authentication
            # handler value
            if not authentication_handler_plugin_handler_name == authentication_handler:
                # continues the loop
                continue

            try:
                # handles the authentication request retrieving the return value
                return_value = authentication_handler_plugin.handle_request(authentication_request)
            except BaseException, exception:
                # retrieves the exception map for the exception
                exception_map = self.get_exception_map(exception)

                # sets the return value to invalid
                return_value = {
                    VALID_VALUE : False,
                    EXCEPTION_VALUE : exception_map
                }

            # returns the return value
            return return_value

        # creates the return value for the no authentication
        # method situation
        return_value = {
            VALID_VALUE : False,
            EXCEPTION_VALUE : {
                MESSAGE_VALUE : NO_AUTHENTICATION_METHOD_MESSAGE
            }
        }

        # returns return value
        return return_value

    def process_authentication_string(self, authentication_string):
        """
        Processes the given authentication string.

        @type authentication_string: String
        @param authentication_string: The string to be used for authentication.
        @rtype: Dictionary
        @return: The authentication return value.
        """

        pass

    def get_exception_map(self, exception):
        """
        Retrieves the exception map (describing the exception)
        for the given exception.

        @type exception: Exception
        @param exception: The exception to retrieve the
        exception map.
        @rtype: Dicitonary
        @return: The exception map describing the exception.
        """

        # retrieves the execution information
        _type, _value, traceback_list = sys.exc_info()

        # starts the formatted traceback (with the default value)
        formatted_traceback = None

        # in case the traceback list is valid
        if traceback_list:
            # creates the (initial) formated traceback
            formatted_traceback = traceback.format_tb(traceback_list)

            # retrieves the file system encoding
            file_system_encoding = sys.getfilesystemencoding()

            # decodes the traceback values using the file system encoding
            formatted_traceback = [value.decode(file_system_encoding) for value in formatted_traceback]

        # retrieves the exception class
        exception_class = exception.__class__

        # retrieves the exception class name
        exception_class_name = exception_class.__name__

        # retrieves the exception message
        exception_message = exception.message

        # creates the exception map
        exception_map = {
            EXCEPTION_REFERENCE_VALUE : exception,
            EXCEPTION_NAME_VALUE : exception_class_name,
            MESSAGE_VALUE : exception_message,
            TRACEBACK_VALUE : formatted_traceback
        }

        # converts the exception class name to underscore notation
        exception_class_name_underscore = colony.libs.string_util.convert_underscore(exception_class_name)

        # creates the exception class process method name
        exception_class_process_method_name = "process_map_" + exception_class_name_underscore

        # in case the instance contains the process handler
        # for the exception class
        if hasattr(self, exception_class_process_method_name):
            # retrieves the exception class process method
            exception_class_process_method = getattr(self, exception_class_process_method_name)

            # calls the exception class process method with
            # the exception map and the exception
            exception_class_process_method(exception_map, exception)

        # returns the exception map
        return exception_map

class AuthenticationRequest:
    """
    The authentication request class.
    """

    username = "none"
    """ The username """

    password = "none"
    """ The password """

    authentication_string = "none"
    """ The authentication string """

    authentication_handler = "none"
    """ The authentication handler """

    arguments = None
    """ The request arguments """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def get_username(self):
        """
        Retrieves the username.

        @rtype: String
        @return: The username.
        """

        return self.username

    def set_username(self, username):
        """
        Sets the username.

        @type username: String
        @rtype: The username.
        """

        self.username = username

    def get_password(self):
        """
        Retrieves the password.

        @rtype: String
        @return: The password.
        """

        return self.password

    def set_password(self, password):
        """
        Sets the password.

        @type password: String
        @param password: The password.
        """

        self.password = password

    def get_authentication_string(self):
        """
        Retrieves the authentication string.

        @rtype: String
        @return: The authentication string.
        """

        return self.authentication_string

    def set_authentication_string(self, authentication_string):
        """
        Sets the authentication string.

        @type authentication_string: String
        @param authentication_string: The authentication string.
        """

        self.authentication_string = authentication_string

    def get_authentication_handler(self):
        """
        Retrieves the authentication handler.

        @rtype: String
        @return: The authentication handler.
        """

        return self.authentication_handler

    def set_authentication_handler(self, authentication_handler):
        """
        Sets the authentication handler.

        @type authentication_handler: String
        @param authentication_handler: The authentication handler.
        """

        self.authentication_handler = authentication_handler

    def set_arguments(self, arguments):
        """
        Sets the arguments.

        @type arguments: Dictionary
        @param arguments: The arguments.
        """

        self.arguments = arguments

    def get_arguments(self):
        """
        Retrieves the arguments.

        @rtype: Dictionary
        @return: The arguments.
        """

        return self.arguments
