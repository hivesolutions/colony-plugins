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

import os
import base64

import colony

import crypton

from .base import BaseController

CONSUMER_STATUS_ACTIVE = 1
""" The consumer active status """

DEFAULT_NUMBER_BITS = 1024
""" The default number of bits to be used in the private
key generation process """

models = colony.__import__("models")


class SignatureController(BaseController):
    def encrypt(self, request, api_key, key_name, message):
        # retrieves the SSL plugin and uses it to create
        # the client structure to be used
        ssl_plugin = self.plugin.ssl_plugin
        ssl_structure = ssl_plugin.create_structure({})

        # validates the API key meaning that in case an API
        # key is expected it's validated, raising an exception
        # in case the validation operation fails
        self._validate_api_key(request, api_key)

        # retrieves the public key path for the key name, decodes
        # the message (using base 64) and encrypts the message (decoded)
        # in base 64 returning the encrypted message back to caller
        public_key_path = self._get_key_path(key_name, "public_key")
        message_decoded = base64.b64decode(message)
        message_e = ssl_structure.encrypt_base_64(public_key_path, message_decoded)
        return message_e

    def decrypt(self, request, api_key, key_name, message_e):
        # retrieves the SSL plugin and uses it to create
        # the client structure to be used
        ssl_plugin = self.plugin.ssl_plugin
        ssl_structure = ssl_plugin.create_structure({})

        # validates the API key meaning that in case an API
        # key is expected it's validated, raising an exception
        # in case the validation operation fails
        self._validate_api_key(request, api_key)

        # retrieves the private key path for the key name, decodes
        # the message (using base 64) and  decrypts the encrypted
        # message (decoded) in base 64, then returns the result
        # back to the caller method
        private_key_path = self._get_key_path(key_name, "private_key")
        message_e_decoded = base64.b64decode(message_e)
        message = ssl_structure.encrypt_base_64(private_key_path, message_e_decoded)
        return message

    def sign(self, request, api_key, key_name, message, algorithm_name):
        # retrieves the SSL plugin and uses it to create
        # the client structure to be used
        ssl_plugin = self.plugin.ssl_plugin
        ssl_structure = ssl_plugin.create_structure({})

        # validates the API key meaning that in case an API
        # key is expected it's validated, raising an exception
        # in case the validation operation fails
        self._validate_api_key(request, api_key)

        # retrieves the private key path for the key name,
        # decodes the message (using base 64) and signs the
        # message (decoded) in base 64 and returns the signature
        # back to the caller method
        private_key_path = self._get_key_path(key_name, "private_key")
        message_decoded = base64.b64decode(message)
        signature = ssl_structure.sign_base_64(
            private_key_path, algorithm_name, message_decoded
        )
        return signature

    def verify(self, request, api_key, key_name, signature, message):
        # retrieves the SSL plugin and uses it to create
        # the client structure to be used
        ssl_plugin = self.plugin.ssl_plugin
        ssl_structure = ssl_plugin.create_structure({})

        # validates the API key meaning that in case an API
        # key is expected it's validated, raising an exception
        # in case the validation operation fails
        self._validate_api_key(request, api_key)

        # retrieves the public key path for the key name, decodes
        # the message (using base 64), then verifies the signature in
        # base 64 and returns a simple string based boolean value,
        # indicating if the validation was successful or not
        public_key_path = self._get_key_path(key_name, "public_key")
        message_decoded = base64.b64decode(message)
        return_value = ssl_structure.verify_base_64(
            public_key_path, signature, message_decoded
        )
        return_value_string = return_value and "1" or "0"
        return return_value_string

    def _validate_api_key(self, request, api_key):
        # retrieves the security map
        security_map = self.system.security_map

        # retrieves the validate API key value and
        # returns immediately in case no API key
        # for validation is defined, meaning that
        # no validation is expected
        validate_api_key = security_map.get("validate_api_key", True)
        if not validate_api_key:
            return

        # creates the filter to retrieve the consumer with
        # the provided API, only existing clients should
        # be considered valid according to specification
        filter = dict(
            filters=(dict(api_key=api_key), dict(status=CONSUMER_STATUS_ACTIVE))
        )

        # retrieves the consumer (entity) with the API key
        consumer = models.Consumer.find_one(filter)

        # raises an exception in case no consumer was found
        # this is the expected behavior for such problem
        if not consumer:
            raise crypton.AccessDeniedException("invalid API key")

    def _get_key_path(self, key_name, key_type):
        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the key path
        keys_map = self.system.keys_map
        key = keys_map.get(key_name, {})
        key_path = key.get(key_type, None)
        key_path = plugin_manager.resolve_file_path(key_path, True, True)

        # generates the key files in case they don't exist
        not os.path.exists(key_path) and self._generate_key_files(key)

        # returns the key path
        return key_path

    def _generate_key_files(self, key, number_bits=DEFAULT_NUMBER_BITS):
        # retrieves the plugin manager and the required plugins for
        # the operation that is going to be performed
        plugin_manager = self.plugin.manager
        ssl_plugin = self.plugin.ssl_plugin

        # retrieves the key path values and uses then in the resolution
        # of the complete path to both of the key values
        private_key_path = key.get("private_key", None)
        public_key_path = key.get("public_key", None)
        private_key_path = plugin_manager.resolve_file_path(
            private_key_path, True, True
        )
        public_key_path = plugin_manager.resolve_file_path(public_key_path, True, True)

        # creates the SSL structure and then generates the public and
        # private keys (should update the generated structure)
        ssl_structure = ssl_plugin.create_structure({})
        ssl_structure.generate_keys(
            private_key_path, public_key_path, number_bits=DEFAULT_NUMBER_BITS
        )
