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

from . import system
from . import mocks


class AuthenticationTest(colony.Test):
    """
    The authentication infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            AuthenticationRequestTestCase,
            AuthenticationBaseTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class AuthenticationRequestTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Authentication Request test case"

    def test_default_values(self):
        request = system.AuthenticationRequest()

        self.assertEqual(request.get_username(), "none")
        self.assertEqual(request.get_password(), "none")
        self.assertEqual(request.get_authentication_string(), "none")
        self.assertEqual(request.get_authentication_handler(), "none")
        self.assertEqual(request.get_arguments(), None)

    def test_set_username(self):
        request = system.AuthenticationRequest()
        request.set_username("testuser")

        self.assertEqual(request.get_username(), "testuser")

    def test_set_password(self):
        request = system.AuthenticationRequest()
        request.set_password("testpassword")

        self.assertEqual(request.get_password(), "testpassword")

    def test_set_authentication_string(self):
        request = system.AuthenticationRequest()
        request.set_authentication_string("auth_string_value")

        self.assertEqual(request.get_authentication_string(), "auth_string_value")

    def test_set_authentication_handler(self):
        request = system.AuthenticationRequest()
        request.set_authentication_handler("python")

        self.assertEqual(request.get_authentication_handler(), "python")

    def test_set_arguments(self):
        request = system.AuthenticationRequest()
        arguments = {"key1": "value1", "key2": "value2"}
        request.set_arguments(arguments)

        self.assertEqual(request.get_arguments(), arguments)
        self.assertEqual(request.get_arguments()["key1"], "value1")

    def test_set_arguments_empty(self):
        request = system.AuthenticationRequest()
        request.set_arguments({})

        self.assertEqual(request.get_arguments(), {})

    def test_username_unicode(self):
        request = system.AuthenticationRequest()
        request.set_username(colony.legacy.u("用户名"))

        self.assertEqual(request.get_username(), colony.legacy.u("用户名"))

    def test_password_unicode(self):
        request = system.AuthenticationRequest()
        request.set_password(colony.legacy.u("密码"))

        self.assertEqual(request.get_password(), colony.legacy.u("密码"))

    def test_credentials_special_characters(self):
        request = system.AuthenticationRequest()
        request.set_username("user@domain.com")
        request.set_password("p@ss!w0rd#$%^&*()")

        self.assertEqual(request.get_username(), "user@domain.com")
        self.assertEqual(request.get_password(), "p@ss!w0rd#$%^&*()")


class AuthenticationBaseTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Authentication Base test case"

    def test_authenticate_user_no_handler(self):
        mock_plugin = mocks.MockPlugin()
        mock_plugin.authentication_handler_plugins = []

        authentication = system.Authentication(mock_plugin)
        result = authentication.authenticate_user(
            "testuser", "testpass", "nonexistent_handler", {}
        )

        self.assertEqual(result["valid"], False)
        self.assertEqual(
            result["exception"]["message"], "no authentication method found"
        )

    def test_authenticate_user_handler_mismatch(self):
        mock_handler = mocks.MockAuthHandler("different_handler")

        mock_plugin = mocks.MockPlugin()
        mock_plugin.authentication_handler_plugins = [mock_handler]

        authentication = system.Authentication(mock_plugin)
        result = authentication.authenticate_user("testuser", "testpass", "python", {})

        self.assertEqual(result["valid"], False)
        self.assertEqual(
            result["exception"]["message"], "no authentication method found"
        )

    def test_authenticate_user_success(self):
        mock_handler = mocks.MockAuthHandler("python")
        mock_handler.return_value = {"valid": True, "username": "testuser"}

        mock_plugin = mocks.MockPlugin()
        mock_plugin.authentication_handler_plugins = [mock_handler]

        authentication = system.Authentication(mock_plugin)
        result = authentication.authenticate_user(
            "testuser", "testpass", "python", {"file_path": "/path/to/config"}
        )

        self.assertEqual(result["valid"], True)
        self.assertEqual(result["username"], "testuser")

    def test_authenticate_user_exception(self):
        mock_handler = mocks.MockAuthHandler("python")
        mock_handler.raise_exception = True
        mock_handler.exception = mocks.MockAuthException("authentication failed")

        mock_plugin = mocks.MockPlugin()
        mock_plugin.authentication_handler_plugins = [mock_handler]

        authentication = system.Authentication(mock_plugin)
        result = authentication.authenticate_user("testuser", "testpass", "python", {})

        self.assertEqual(result["valid"], False)
        self.assertNotEqual(result.get("exception"), None)

    def test_authenticate_user_multiple_handlers(self):
        mock_handler_ldap = mocks.MockAuthHandler("ldap")
        mock_handler_ldap.return_value = {"valid": True, "username": "ldap_user"}

        mock_handler_python = mocks.MockAuthHandler("python")
        mock_handler_python.return_value = {"valid": True, "username": "python_user"}

        mock_plugin = mocks.MockPlugin()
        mock_plugin.authentication_handler_plugins = [
            mock_handler_ldap,
            mock_handler_python,
        ]

        authentication = system.Authentication(mock_plugin)
        result = authentication.authenticate_user("testuser", "testpass", "python", {})

        self.assertEqual(result["valid"], True)
        self.assertEqual(result["username"], "python_user")

    def test_get_exception_map(self):
        mock_plugin = mocks.MockPlugin()
        authentication = system.Authentication(mock_plugin)

        exception = mocks.MockAuthException("test error message")
        try:
            raise exception
        except mocks.MockAuthException as e:
            exception_map = authentication.get_exception_map(e)

        self.assertEqual(exception_map["message"], "test error message")
        self.assertEqual(exception_map["exception_name"], "MockAuthException")
        self.assertEqual(exception_map["exception_reference"], exception)

    def test_get_exception_map_traceback(self):
        mock_plugin = mocks.MockPlugin()
        authentication = system.Authentication(mock_plugin)

        try:
            raise mocks.MockAuthException("traceback test")
        except mocks.MockAuthException as e:
            exception_map = authentication.get_exception_map(e)

        self.assertNotEqual(exception_map.get("traceback"), None)
