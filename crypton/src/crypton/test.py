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

from .system import Crypton
from .exceptions import CryptonException
from .exceptions import AccessDeniedException


class CryptonTest(colony.Test):
    """
    The crypton infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (CryptonBaseTestCase,)

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class CryptonBaseTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Crypton Base test case"

    def test_initialization(self):
        mock_plugin = MockPlugin()
        crypton = Crypton(mock_plugin)

        self.assertEqual(crypton.keys_map, {})
        self.assertEqual(crypton.security_map, {})

    def test_set_configuration_property(self):
        mock_plugin = MockPlugin()
        crypton = Crypton(mock_plugin)

        # creates a mock configuration property with keys and security
        config_property = MockConfigurationProperty(
            {
                "keys": {
                    "test_key": {
                        "private_key": "/path/to/private.key",
                        "public_key": "/path/to/public.key",
                    }
                },
                "security": {"validate_api_key": True, "allowed_origins": ["*"]},
            }
        )

        # sets the configuration property and verifies the maps were updated
        crypton.set_configuration_property(config_property)

        self.assertNotEqual(crypton.keys_map, {})
        self.assertEqual(
            crypton.keys_map["test_key"]["private_key"], "/path/to/private.key"
        )
        self.assertEqual(
            crypton.keys_map["test_key"]["public_key"], "/path/to/public.key"
        )
        self.assertNotEqual(crypton.security_map, {})
        self.assertEqual(crypton.security_map["validate_api_key"], True)

    def test_unset_configuration_property(self):
        mock_plugin = MockPlugin()
        crypton = Crypton(mock_plugin)

        # sets some configuration first
        config_property = MockConfigurationProperty(
            {
                "keys": {"test_key": {"private_key": "/path/to/key"}},
                "security": {"validate_api_key": True},
            }
        )
        crypton.set_configuration_property(config_property)

        # verifies configuration was set
        self.assertNotEqual(crypton.keys_map, {})
        self.assertNotEqual(crypton.security_map, {})

        # unsets the configuration and verifies maps are now empty
        crypton.unset_configuration_property()

        self.assertEqual(crypton.keys_map, {})
        self.assertEqual(crypton.security_map, {})

    def test_set_configuration_multiple_keys(self):
        mock_plugin = MockPlugin()
        crypton = Crypton(mock_plugin)

        # creates configuration with multiple keys
        config_property = MockConfigurationProperty(
            {
                "keys": {
                    "production_key": {
                        "private_key": "/prod/private.key",
                        "public_key": "/prod/public.key",
                    },
                    "staging_key": {
                        "private_key": "/staging/private.key",
                        "public_key": "/staging/public.key",
                    },
                    "development_key": {
                        "private_key": "/dev/private.key",
                        "public_key": "/dev/public.key",
                    },
                },
                "security": {},
            }
        )

        crypton.set_configuration_property(config_property)

        self.assertEqual(len(crypton.keys_map), 3)
        self.assertIn("production_key", crypton.keys_map)
        self.assertIn("staging_key", crypton.keys_map)
        self.assertIn("development_key", crypton.keys_map)

    def test_get_controller(self):
        mock_plugin = MockPlugin()
        crypton = Crypton(mock_plugin)

        # adds mock controllers to the crypton instance
        mock_main_controller = MockController("main")
        mock_signature_controller = MockController("signature")
        crypton.controllers = {
            "main": mock_main_controller,
            "signature": mock_signature_controller,
        }

        # retrieves controllers and verifies they are correct
        main = crypton.get_controller("main")
        signature = crypton.get_controller("signature")

        self.assertEqual(main.name, "main")
        self.assertEqual(signature.name, "signature")

    def test_get_patterns(self):
        mock_plugin = MockPlugin()
        crypton = Crypton(mock_plugin)

        # creates mock controllers with required methods
        mock_main = MockController("main")
        mock_main.encrypt = lambda r: None
        mock_main.decrypt = lambda r: None
        mock_main.sign = lambda r: None
        mock_main.verify = lambda r: None

        mock_consumer = MockController("consumer")
        mock_consumer.create = lambda r: None

        crypton.main_controller = mock_main
        crypton.consumer_controller = mock_consumer

        # retrieves patterns and verifies structure
        patterns = crypton.get_patterns()

        self.assertEqual(len(patterns), 5)
        for pattern in patterns:
            self.assertEqual(len(pattern), 3)

        # verifies all expected routes are present
        routes = [p[0] for p in patterns]
        self.assertIn("crypton/encrypt", routes)
        self.assertIn("crypton/decrypt", routes)
        self.assertIn("crypton/sign", routes)
        self.assertIn("crypton/verify", routes)
        self.assertIn("crypton/consumers", routes)

    def test_crypton_exception(self):
        exception = CryptonException()
        self.assertEqual(exception.message, None)

    def test_access_denied_exception(self):
        exception = AccessDeniedException("invalid API key")

        self.assertEqual(exception.message, "invalid API key")
        self.assertEqual(str(exception), "Access denied exception - invalid API key")

    def test_access_denied_exception_unicode(self):
        exception = AccessDeniedException(colony.legacy.u("访问被拒绝"))

        self.assertEqual(exception.message, colony.legacy.u("访问被拒绝"))

    def test_access_denied_exception_inheritance(self):
        exception = AccessDeniedException("test")

        self.assertTrue(isinstance(exception, CryptonException))
        self.assertTrue(isinstance(exception, colony.ColonyException))


class MockPlugin:
    def __init__(self):
        self.mvc_utils_plugin = None
        self.ssl_plugin = None
        self.manager = None


class MockConfigurationProperty:
    def __init__(self, data):
        self._data = data

    def get_data(self):
        return self._data


class MockController:
    def __init__(self, name):
        self.name = name
