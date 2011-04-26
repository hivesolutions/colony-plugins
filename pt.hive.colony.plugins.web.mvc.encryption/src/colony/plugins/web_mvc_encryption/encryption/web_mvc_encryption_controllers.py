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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import base64

import colony.libs.importer_util

import web_mvc_encryption_exceptions

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

WEB_MVC_ENCRYPTION_RESOURCES_PATH = "web_mvc_encryption/encryption/resources"
""" The web mvc encryption resources path """

TEMPLATES_PATH = WEB_MVC_ENCRYPTION_RESOURCES_PATH + "/templates"
""" The templates path """

DEFAULT_NUMBER_BITS = 256
""" The default number of bits """

VALID_STATUS_VALUE = 1
""" The valid status value """

INVALID_STATUS_VALUE = 2
""" The invalid status value """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

DEFAULT_ALGORITHM_NAME = "sha1"
""" The default algorithm name """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class WebMvcEncryptionMainController:
    """
    The web mvc encryption main controller.
    """

    web_mvc_encryption_plugin = None
    """ The web mvc encryption plugin """

    web_mvc_encryption = None
    """ The web mvc encryption """

    def __init__(self, web_mvc_encryption_plugin, web_mvc_encryption):
        """
        Constructor of the class.

        @type web_mvc_encryption_plugin: WebMvcEncryptionPlugin
        @param web_mvc_encryption_plugin: The web mvc encryption plugin.
        @type web_mvc_encryption: WebMvcEncryption
        @param web_mvc_encryption: The web mvc encryption.
        """

        self.web_mvc_encryption_plugin = web_mvc_encryption_plugin
        self.web_mvc_encryption = web_mvc_encryption

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_encryption_plugin.manager

        # retrieves the web mvc encryption plugin path
        web_mvc_encryption_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_encryption_plugin.id)

        # creates the templates path
        templates_path = web_mvc_encryption_plugin_path + "/" + TEMPLATES_PATH

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_web_mvc_encryption_sign(self, rest_request, parameters = {}):
        """
        Handles the given web mvc encryption sign rest request.

        @type rest_request: RestRequest
        @param rest_request: The web mvc encryption sign rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the api key from the form data map
        api_key = form_data_map.get("api_key", None)

        # retrieves the key name from the form data map
        key_name = form_data_map["key_name"]

        # retrieves the message from the form data map
        message = form_data_map["message"]

        # retrieves the algorithm name from the form data map
        algorithm_name = form_data_map.get("algorithm_name", DEFAULT_ALGORITHM_NAME)

        # signs the message and retrieves the signature
        signature = self._sign(rest_request, api_key, key_name, message, algorithm_name)

        # sets the signature as the contents
        self.set_contents(rest_request, signature, "text/plain")

        # returns true
        return True

    def handle_web_mvc_encryption_verify(self, rest_request, parameters = {}):
        """
        Handles the given web mvc encryption verify rest request.

        @type rest_request: RestRequest
        @param rest_request: The web mvc encryption verify rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the api key from the form data map
        api_key = form_data_map.get("api_key", None)

        # retrieves the key name from the form data map
        key_name = form_data_map["key_name"]

        # retrieves the signature from the form data map
        signature = form_data_map["signature"]

        # retrieves the message from the form data map
        message = form_data_map["message"]

        # verifies the signature and retrieves the return value string
        return_value_string = self._verify(rest_request, api_key, key_name, signature, message)

        # sets the return value string as the contents
        self.set_contents(rest_request, return_value_string, "text/plain")

        # returns true
        return True

    def _sign(self, rest_request, api_key, key_name, message, algorithm_name):
        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.web_mvc_encryption_plugin.encryption_ssl_plugin

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # validates the api key
        self._validate_api_key(rest_request, api_key)

        # retrieves the private key path for the key name
        private_key_path = self._get_key_path(key_name, "private_key")

        # decodes the message (using base 64)
        message_decoded = base64.b64decode(message)

        # signs the message (decoded) in base 64
        signature = ssl_structure.sign_base_64(private_key_path, algorithm_name, message_decoded)

        # returns the signature
        return signature

    def _verify(self, rest_request, api_key, key_name, signature, message):
        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.web_mvc_encryption_plugin.encryption_ssl_plugin

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # validates the api key
        self._validate_api_key(rest_request, api_key)

        # retrieves the public key path for the key name
        public_key_path = self._get_key_path(key_name, "public_key")

        # decodes the message (using base 64)
        message_decoded = base64.b64decode(message)

        # verifies the signature in base 64
        return_value = ssl_structure.verify_base_64(public_key_path, signature, message_decoded)

        # retrieves the return value in (simple) string mode
        return_value_string = return_value and "0" or "1"

        # returns the return value string
        return return_value_string

    def _validate_api_key(self, rest_request, api_key):
        # retrieves the web mvc encryption consumer controller
        web_mvc_encryption_consumer_controller = self.web_mvc_encryption.web_mvc_encryption_consumer_controller

        # retrieves the security map
        security_map = self.web_mvc_encryption.security_map

        # retrieves the valida pi key value
        validate_api_key = security_map.get("validate_api_key", True)

        # validates the api key
        validate_api_key and  web_mvc_encryption_consumer_controller._validate_api_key(rest_request, api_key)

    def _get_key_path(self, key_name, key_type):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_encryption_plugin.manager

        # retrieves the keys map
        keys_map = self.web_mvc_encryption.keys_map

        # retrieves the key for the key name
        key = keys_map.get(key_name, {})

        # retrieves the key path
        key_path = key.get(key_type, None)

        # resolves the key file path
        key_path = plugin_manager.resolve_file_path(key_path, True, True)

        # in case the key file path does not exists
        if not os.path.exists(key_path):
            # generates the key files
            self._generate_key_files(key)

        # returns the key path
        return key_path

    def _generate_key_files(self, key):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_encryption_plugin.manager

        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.web_mvc_encryption_plugin.encryption_ssl_plugin

        # retrieves the private key path
        private_key_path = key.get("private_key", None)

        # retrieves the public key path
        public_key_path = key.get("public_key", None)

        # resolves the private key file path
        private_key_path = plugin_manager.resolve_file_path(private_key_path, True, True)

        # resolves the public key file path
        public_key_path = plugin_manager.resolve_file_path(public_key_path, True, True)

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # generates the public and private keys
        ssl_structure.generate_keys(private_key_path, public_key_path, DEFAULT_NUMBER_BITS)

class ConsumerController:
    """
    The web mvc encryption consumer controller.
    """

    web_mvc_encryption_plugin = None
    """ The web mvc encryption plugin """

    web_mvc_encryption = None
    """ The web mvc encryption """

    def __init__(self, web_mvc_encryption_plugin, web_mvc_encryption):
        """
        Constructor of the class.

        @type web_mvc_encryption_plugin: WebMvcEncryptionPlugin
        @param web_mvc_encryption_plugin: The web mvc encryption plugin.
        @type web_mvc_encryption: WebMvcEncryption
        @param web_mvc_encryption: The web mvc encryption.
        """

        self.web_mvc_encryption_plugin = web_mvc_encryption_plugin
        self.web_mvc_encryption = web_mvc_encryption

    def start(self):
        """
        Method called upon structure initialization.
        """

        pass

    def handle_create(self, rest_request, parameters = {}):
        """
        Handles the new consumer rest request.

        @type rest_request: RestRequest
        @param rest_request: The web mvc encryption new rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the consumer
        consumer = form_data_map.get("consumer", {})

        # saves the consumer
        self._save_consumer(rest_request, consumer)

        # returns true
        return True

    @web_mvc_utils.transaction_method("web_mvc_encryption.web_mvc_encryption_entity_models.entity_manager")
    def _save_consumer(self, rest_request, consumer):
        # retrieves the web mvc encryption entity models
        web_mvc_encryption_entity_models = self.web_mvc_encryption.web_mvc_encryption_entity_models

        # creates the consumer create map
        consumer_create = {
            "status" : INVALID_STATUS_VALUE,
            "api_key" : self._generate_api_key()
        }

        # retrieves the consumer entity
        consumer_entity = self.get_entity_model(web_mvc_encryption_entity_models.entity_manager, web_mvc_encryption_entity_models.Consumer, consumer, consumer_create)

        # validates the consumer entity
        self.validate_model_exception(consumer_entity, "consumer validation failed")

        # saves the consumer entity
        consumer_entity.save_update()

        # returns the consumer entity
        return consumer_entity

    def _get_consumers(self, rest_request, filter):
        # retrieves the web mvc encryption entity models
        web_mvc_encryption_entity_models = self.web_mvc_encryption.web_mvc_encryption_entity_models

        # retrieves the entity manager
        entity_manager = web_mvc_encryption_entity_models.entity_manager

        # retrieves the consumer entities with the specified api key
        consumer_entities = entity_manager._find_all_options(web_mvc_encryption_entity_models.Consumer, filter)

        # returns the consumer entities
        return consumer_entities

    def _validate_api_key(self, rest_request, api_key):
        # creates the filter map
        filter = {
            "filters" : [
                {
                    "filter_type" : "equals",
                    "filter_fields" : [
                        {
                            "field_name" : "api_key",
                            "field_value" : api_key
                        }
                    ]
                },
                {
                    "filter_type" : "equals",
                    "filter_fields" : [
                        {
                            "field_name" : "status",
                            "field_value" : VALID_STATUS_VALUE
                        }
                    ]
                }
            ]
        }

        # retrieves the consumer entities with the api key
        consumer_entities = self._get_consumers(rest_request, filter)

        # retrieves the consumer entity
        consumer_entity = consumer_entities and consumer_entities[0] or None

        # raises an exception in case no consumer was found
        if not consumer_entity:
            # raises the access denied exception
            raise web_mvc_encryption_exceptions.AccessDeniedException("invalid api key")

        # returns the consumer entity
        return consumer_entity

    def _generate_api_key(self):
        # retrieves the random plugin
        random_plugin = self.web_mvc_encryption_plugin.random_plugin

        # generates a random string value for
        # the api key
        api_key = random_plugin.generate_random_sha256_string()

        # returns the (generated) api key
        return api_key
