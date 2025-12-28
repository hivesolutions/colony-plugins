#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from .system import Authentication
from .system import AuthenticationRequest


class AuthenticationTest(colony.Test):
    """
    The authentication infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            AuthenticationRequestTestCase,
            AuthenticationSystemTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class AuthenticationRequestTestCase(colony.ColonyTestCase):
    """
    Test case for the AuthenticationRequest class.
    Tests all getter and setter methods.
    """

    @staticmethod
    def get_description():
        return "Authentication Request test case"

    def test_default_values(self):
        """
        Tests that AuthenticationRequest initializes with default values.
        """
        request = AuthenticationRequest()

        self.assertEqual(request.get_username(), "none")
        self.assertEqual(request.get_password(), "none")
        self.assertEqual(request.get_authentication_string(), "none")
        self.assertEqual(request.get_authentication_handler(), "none")
        self.assertEqual(request.get_arguments(), None)

    def test_set_username(self):
        """
        Tests setting and getting username.
        """
        request = AuthenticationRequest()
        request.set_username("testuser")

        self.assertEqual(request.get_username(), "testuser")

    def test_set_password(self):
        """
        Tests setting and getting password.
        """
        request = AuthenticationRequest()
        request.set_password("testpassword")

        self.assertEqual(request.get_password(), "testpassword")

    def test_set_authentication_string(self):
        """
        Tests setting and getting authentication string.
        """
        request = AuthenticationRequest()
        request.set_authentication_string("auth_string_value")

        self.assertEqual(request.get_authentication_string(), "auth_string_value")

    def test_set_authentication_handler(self):
        """
        Tests setting and getting authentication handler.
        """
        request = AuthenticationRequest()
        request.set_authentication_handler("python")

        self.assertEqual(request.get_authentication_handler(), "python")

    def test_set_arguments(self):
        """
        Tests setting and getting arguments dictionary.
        """
        request = AuthenticationRequest()
        arguments = {"key1": "value1", "key2": "value2"}
        request.set_arguments(arguments)

        self.assertEqual(request.get_arguments(), arguments)
        self.assertEqual(request.get_arguments()["key1"], "value1")

    def test_set_empty_arguments(self):
        """
        Tests setting empty arguments dictionary.
        """
        request = AuthenticationRequest()
        request.set_arguments({})

        self.assertEqual(request.get_arguments(), {})

    def test_unicode_username(self):
        """
        Tests that unicode usernames are handled correctly.
        """
        request = AuthenticationRequest()
        request.set_username(colony.legacy.u("用户名"))

        self.assertEqual(request.get_username(), colony.legacy.u("用户名"))

    def test_unicode_password(self):
        """
        Tests that unicode passwords are handled correctly.
        """
        request = AuthenticationRequest()
        request.set_password(colony.legacy.u("密码"))

        self.assertEqual(request.get_password(), colony.legacy.u("密码"))

    def test_special_characters_in_credentials(self):
        """
        Tests that special characters in credentials are handled correctly.
        """
        request = AuthenticationRequest()
        request.set_username("user@domain.com")
        request.set_password("p@ss!w0rd#$%^&*()")

        self.assertEqual(request.get_username(), "user@domain.com")
        self.assertEqual(request.get_password(), "p@ss!w0rd#$%^&*()")


class AuthenticationSystemTestCase(colony.ColonyTestCase):
    """
    Test case for the Authentication system class.
    Tests the main authentication flow and exception handling.
    """

    @staticmethod
    def get_description():
        return "Authentication System test case"

    def test_authenticate_user_no_handler(self):
        """
        Tests authentication when no matching handler is found.
        Returns an error indicating no authentication method found.
        """
        # creates a mock plugin with no authentication handler plugins
        mock_plugin = MockPlugin()
        mock_plugin.authentication_handler_plugins = []

        # creates the authentication system
        authentication = Authentication(mock_plugin)

        # attempts to authenticate
        result = authentication.authenticate_user(
            "testuser", "testpass", "nonexistent_handler", {}
        )

        # verifies the result indicates failure with proper message
        self.assertEqual(result["valid"], False)
        self.assertEqual(
            result["exception"]["message"], "no authentication method found"
        )

    def test_authenticate_user_handler_mismatch(self):
        """
        Tests authentication when handler name doesn't match.
        """
        # creates a mock handler plugin with a different name
        mock_handler = MockAuthHandler("different_handler")

        # creates a mock plugin with the handler
        mock_plugin = MockPlugin()
        mock_plugin.authentication_handler_plugins = [mock_handler]

        # creates the authentication system
        authentication = Authentication(mock_plugin)

        # attempts to authenticate with a different handler name
        result = authentication.authenticate_user(
            "testuser", "testpass", "python", {}
        )

        # verifies the result indicates failure
        self.assertEqual(result["valid"], False)
        self.assertEqual(
            result["exception"]["message"], "no authentication method found"
        )

    def test_authenticate_user_successful(self):
        """
        Tests successful authentication flow.
        """
        # creates a mock handler that returns success
        mock_handler = MockAuthHandler("python")
        mock_handler.return_value = {"valid": True, "username": "testuser"}

        # creates a mock plugin with the handler
        mock_plugin = MockPlugin()
        mock_plugin.authentication_handler_plugins = [mock_handler]

        # creates the authentication system
        authentication = Authentication(mock_plugin)

        # attempts to authenticate
        result = authentication.authenticate_user(
            "testuser", "testpass", "python", {"file_path": "/path/to/config"}
        )

        # verifies successful authentication
        self.assertEqual(result["valid"], True)
        self.assertEqual(result["username"], "testuser")

    def test_authenticate_user_handler_exception(self):
        """
        Tests authentication when handler raises an exception.
        """
        # creates a mock handler that raises an exception
        mock_handler = MockAuthHandler("python")
        mock_handler.raise_exception = True
        mock_handler.exception = MockAuthException("authentication failed")

        # creates a mock plugin with the handler
        mock_plugin = MockPlugin()
        mock_plugin.authentication_handler_plugins = [mock_handler]

        # creates the authentication system
        authentication = Authentication(mock_plugin)

        # attempts to authenticate
        result = authentication.authenticate_user(
            "testuser", "testpass", "python", {}
        )

        # verifies that exception was caught and wrapped
        self.assertEqual(result["valid"], False)
        self.assertNotEqual(result.get("exception"), None)

    def test_authenticate_user_multiple_handlers(self):
        """
        Tests that correct handler is selected from multiple handlers.
        """
        # creates multiple mock handlers
        mock_handler_ldap = MockAuthHandler("ldap")
        mock_handler_ldap.return_value = {"valid": True, "username": "ldap_user"}

        mock_handler_python = MockAuthHandler("python")
        mock_handler_python.return_value = {"valid": True, "username": "python_user"}

        # creates a mock plugin with multiple handlers
        mock_plugin = MockPlugin()
        mock_plugin.authentication_handler_plugins = [
            mock_handler_ldap,
            mock_handler_python,
        ]

        # creates the authentication system
        authentication = Authentication(mock_plugin)

        # authenticates using python handler
        result = authentication.authenticate_user(
            "testuser", "testpass", "python", {}
        )

        # verifies python handler was used
        self.assertEqual(result["valid"], True)
        self.assertEqual(result["username"], "python_user")

    def test_get_exception_map_basic(self):
        """
        Tests basic exception map generation.
        """
        mock_plugin = MockPlugin()
        authentication = Authentication(mock_plugin)

        # creates a test exception
        exception = MockAuthException("test error message")

        # gets the exception map
        try:
            raise exception
        except MockAuthException as e:
            exception_map = authentication.get_exception_map(e)

        # verifies the exception map contents
        self.assertEqual(exception_map["message"], "test error message")
        self.assertEqual(exception_map["exception_name"], "MockAuthException")
        self.assertEqual(exception_map["exception_reference"], exception)

    def test_get_exception_map_with_traceback(self):
        """
        Tests exception map includes traceback information.
        """
        mock_plugin = MockPlugin()
        authentication = Authentication(mock_plugin)

        # creates and raises an exception to generate traceback
        try:
            raise MockAuthException("traceback test")
        except MockAuthException as e:
            exception_map = authentication.get_exception_map(e)

        # verifies traceback is included
        self.assertNotEqual(exception_map.get("traceback"), None)


class MockPlugin:
    """
    Mock plugin for testing authentication system.
    """

    def __init__(self):
        self.authentication_handler_plugins = []


class MockAuthHandler:
    """
    Mock authentication handler for testing.
    """

    def __init__(self, handler_name):
        self.handler_name = handler_name
        self.return_value = {"valid": False}
        self.raise_exception = False
        self.exception = None

    def get_handler_name(self):
        return self.handler_name

    def handle_request(self, request):
        if self.raise_exception:
            raise self.exception
        return self.return_value


class MockAuthException(Exception):
    """
    Mock exception for testing exception handling.
    """

    def __init__(self, message):
        self.message = message
        super(MockAuthException, self).__init__(message)
