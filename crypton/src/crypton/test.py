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
__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
__license__ = "Apache License, Version 2.0"

import base64

import colony

from . import system
from . import exceptions
from . import mocks


class CryptonTest(colony.Test):
    """
    The crypton infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            CryptonBaseTestCase,
            CryptonEncryptionTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class CryptonBaseTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Crypton Base test case"

    def test_initialization(self):
        mock_plugin = mocks.MockPlugin()
        crypton = system.Crypton(mock_plugin)

        self.assertEqual(crypton.keys_map, {})
        self.assertEqual(crypton.security_map, {})

    def test_set_configuration_property(self):
        mock_plugin = mocks.MockPlugin()
        crypton = system.Crypton(mock_plugin)

        config_property = mocks.MockConfigurationProperty(
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
        mock_plugin = mocks.MockPlugin()
        crypton = system.Crypton(mock_plugin)

        config_property = mocks.MockConfigurationProperty(
            {
                "keys": {"test_key": {"private_key": "/path/to/key"}},
                "security": {"validate_api_key": True},
            }
        )
        crypton.set_configuration_property(config_property)

        self.assertNotEqual(crypton.keys_map, {})
        self.assertNotEqual(crypton.security_map, {})

        crypton.unset_configuration_property()

        self.assertEqual(crypton.keys_map, {})
        self.assertEqual(crypton.security_map, {})

    def test_set_configuration_multiple_keys(self):
        mock_plugin = mocks.MockPlugin()
        crypton = system.Crypton(mock_plugin)

        config_property = mocks.MockConfigurationProperty(
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
        mock_plugin = mocks.MockPlugin()
        crypton = system.Crypton(mock_plugin)

        mock_main_controller = mocks.MockController("main")
        mock_signature_controller = mocks.MockController("signature")
        crypton.controllers = {
            "main": mock_main_controller,
            "signature": mock_signature_controller,
        }

        main = crypton.get_controller("main")
        signature = crypton.get_controller("signature")

        self.assertEqual(main.name, "main")
        self.assertEqual(signature.name, "signature")

    def test_get_patterns(self):
        mock_plugin = mocks.MockPlugin()
        crypton = system.Crypton(mock_plugin)

        mock_main = mocks.MockController("main")
        mock_main.encrypt = lambda r: None
        mock_main.decrypt = lambda r: None
        mock_main.sign = lambda r: None
        mock_main.verify = lambda r: None

        mock_consumer = mocks.MockController("consumer")
        mock_consumer.create = lambda r: None

        crypton.main_controller = mock_main
        crypton.consumer_controller = mock_consumer

        patterns = crypton.get_patterns()

        self.assertEqual(len(patterns), 5)
        for pattern in patterns:
            self.assertEqual(len(pattern), 3)

        routes = [p[0] for p in patterns]
        self.assertIn("crypton/encrypt", routes)
        self.assertIn("crypton/decrypt", routes)
        self.assertIn("crypton/sign", routes)
        self.assertIn("crypton/verify", routes)
        self.assertIn("crypton/consumers", routes)

    def test_crypton_exception(self):
        exception = exceptions.CryptonException()
        self.assertEqual(exception.message, None)

    def test_access_denied_exception(self):
        exception = exceptions.AccessDeniedException("invalid API key")

        self.assertEqual(exception.message, "invalid API key")
        self.assertEqual(str(exception), "Access denied exception - invalid API key")

    def test_access_denied_exception_unicode(self):
        exception = exceptions.AccessDeniedException(colony.legacy.u("访问被拒绝"))

        self.assertEqual(exception.message, colony.legacy.u("访问被拒绝"))

    def test_access_denied_exception_inheritance(self):
        exception = exceptions.AccessDeniedException("test")

        self.assertTrue(isinstance(exception, exceptions.CryptonException))
        self.assertTrue(isinstance(exception, colony.ColonyException))


class CryptonEncryptionTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Crypton Encryption test case"

    def test_encrypt_base_64(self):
        ssl = mocks.MockSSLStructure()

        message = b"Hello World"
        result = ssl.encrypt_base_64("/path/to/public.key", message)

        self.assertNotEqual(result, None)
        self.assertTrue(len(result) > 0)
        decoded = base64.b64decode(result)
        self.assertTrue(decoded.startswith(b"encrypted:"))

    def test_decrypt_base_64(self):
        ssl = mocks.MockSSLStructure()

        message = b"Secret Message"
        encrypted = ssl.encrypt_base_64("/path/to/public.key", message)
        decrypted = ssl.decrypt_base_64("/path/to/private.key", encrypted)

        self.assertEqual(decrypted, message)

    def test_sign_base_64(self):
        ssl = mocks.MockSSLStructure()

        message = b"Message to sign"
        signature = ssl.sign_base_64("/path/to/private.key", "sha256", message)

        self.assertNotEqual(signature, None)
        self.assertTrue(len(signature) > 0)

    def test_sign_multiple_algorithms(self):
        ssl = mocks.MockSSLStructure()

        message = b"Test message"
        for algorithm in ("md5", "sha1", "sha256"):
            signature = ssl.sign_base_64("/path/to/private.key", algorithm, message)
            self.assertNotEqual(signature, None)
            self.assertTrue(len(signature) > 0)
            decoded = base64.b64decode(signature)
            self.assertIn(algorithm.encode(), decoded)

    def test_verify_base_64(self):
        ssl = mocks.MockSSLStructure()

        message = b"Signed message"
        signature = ssl.sign_base_64("/path/to/private.key", "sha256", message)

        result = ssl.verify_base_64("/path/to/public.key", signature, message)
        self.assertEqual(result, True)

    def test_encrypt_decrypt_roundtrip(self):
        ssl = mocks.MockSSLStructure()

        messages = [b"Hello World", b"Test 123", b"Special chars: @#$%"]
        for original in messages:
            encrypted = ssl.encrypt_base_64("/path/to/public.key", original)
            decrypted = ssl.decrypt_base_64("/path/to/private.key", encrypted)
            self.assertEqual(decrypted, original)

    def test_sign_verify_roundtrip(self):
        ssl = mocks.MockSSLStructure()

        messages = [b"Message 1", b"Message 2", b"Message 3"]
        for message in messages:
            signature = ssl.sign_base_64("/path/to/private.key", "sha256", message)
            result = ssl.verify_base_64("/path/to/public.key", signature, message)
            self.assertEqual(result, True)

    def test_encrypt_empty_message(self):
        ssl = mocks.MockSSLStructure()

        encrypted = ssl.encrypt_base_64("/path/to/public.key", b"")
        decrypted = ssl.decrypt_base_64("/path/to/private.key", encrypted)
        self.assertEqual(decrypted, b"")

    def test_encrypt_unicode_message(self):
        ssl = mocks.MockSSLStructure()

        message = colony.legacy.u("你好世界").encode("utf-8")
        encrypted = ssl.encrypt_base_64("/path/to/public.key", message)
        decrypted = ssl.decrypt_base_64("/path/to/private.key", encrypted)
        self.assertEqual(decrypted, message)

    def test_base64_message_encoding(self):
        original = b"Hello World"
        encoded = base64.b64encode(original)
        decoded = base64.b64decode(encoded)

        self.assertEqual(decoded, original)
        self.assertEqual(encoded, b"SGVsbG8gV29ybGQ=")
