#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import os
import base64

import colony.libs.import_util

import crypton.exceptions

CONSUMER_STATUS_ACTIVE = 1
""" The consumer active status """

DEFAULT_NUMBER_BITS = 256
""" The default number of bits """

models = colony.libs.import_util.__import__("models")
controllers = colony.libs.import_util.__import__("controllers")
mvc_utils = colony.libs.import_util.__import__("mvc_utils")

class SignatureController(controllers.Controller):
    """
    The crypton signature controller.
    """

    def encrypt(self, request, api_key, key_name, message):
        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.plugin.encryption_ssl_plugin

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # validates the api key
        self._validate_api_key(request, api_key)

        # retrieves the public key path for the key name
        public_key_path = self._get_key_path(key_name, "public_key")

        # decodes the message (using base 64)
        message_decoded = base64.b64decode(message)

        # encrypts the message (decoded) in base 64
        message_e = ssl_structure.encrypt_base_64(public_key_path, message_decoded)

        # returns the encrypted message
        return message_e

    def decrypt(self, request, api_key, key_name, message_e):
        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.plugin.encryption_ssl_plugin

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # validates the api key
        self._validate_api_key(request, api_key)

        # retrieves the private key path for the key name
        private_key_path = self._get_key_path(key_name, "private_key")

        # decodes the message (using base 64)
        message_e_decoded = base64.b64decode(message_e)

        # decrypts the encrypted message (decoded) in base 64
        message = ssl_structure.encrypt_base_64(private_key_path, message_e_decoded)

        # returns the original message
        return message

    def sign(self, request, api_key, key_name, message, algorithm_name):
        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.plugin.encryption_ssl_plugin

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # validates the api key
        self._validate_api_key(request, api_key)

        # retrieves the private key path for the key name
        private_key_path = self._get_key_path(key_name, "private_key")

        # decodes the message (using base 64)
        message_decoded = base64.b64decode(message)

        # signs the message (decoded) in base 64
        signature = ssl_structure.sign_base_64(private_key_path, algorithm_name, message_decoded)

        # returns the signature
        return signature

    def verify(self, request, api_key, key_name, signature, message):
        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.plugin.encryption_ssl_plugin

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # validates the api key
        self._validate_api_key(request, api_key)

        # retrieves the public key path for the key name
        public_key_path = self._get_key_path(key_name, "public_key")

        # decodes the message (using base 64)
        message_decoded = base64.b64decode(message)

        # verifies the signature in base 64
        return_value = ssl_structure.verify_base_64(public_key_path, signature, message_decoded)

        # retrieves the return value in (simple) string mode
        return_value_string = return_value and "1" or "0"

        # returns the return value string
        return return_value_string

    def _validate_api_key(self, request, api_key):
        # retrieves the security map
        security_map = self.system.security_map

        # retrieves the validate api key value
        validate_api_key = security_map.get("validate_api_key", True)

        # returns in case no api key validation is required
        if not validate_api_key:
            # returns
            return

        # creates the filter to retrieve the consumer with
        # the provided api, only existing clients should
        # be considered valid according to specification
        filter = {
            "filters" : (
                {
                    "api_key" : api_key
                },
                {
                    "status" : CONSUMER_STATUS_ACTIVE
                }
            )
        }

        # retrieves the consumer entity with the api key
        consumer_entity = models.Consumer.find_one(filter)

        # raises an exception in case no consumer was found
        if not consumer_entity:
            # raises the access denied exception
            raise crypton.exceptions.AccessDeniedException("invalid api key")

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

    def _generate_key_files(self, key):
        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.plugin.encryption_ssl_plugin

        # retrieves the key paths
        private_key_path = key.get("private_key", None)
        public_key_path = key.get("public_key", None)

        # resolves the key file paths
        private_key_path = plugin_manager.resolve_file_path(private_key_path, True, True)
        public_key_path = plugin_manager.resolve_file_path(public_key_path, True, True)

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # generates the public and private keys
        ssl_structure.generate_keys(private_key_path, public_key_path, DEFAULT_NUMBER_BITS)
