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

import colony.libs.map_util

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_ENCRYPTION_RESOURCES_PATH = "web_mvc_encryption/encryption/resources"
""" The web mvc encryption resources path """

TEMPLATES_PATH = WEB_MVC_ENCRYPTION_RESOURCES_PATH + "/templates"
""" The templates path """

EXTRAS_PATH = WEB_MVC_ENCRYPTION_RESOURCES_PATH + "/extras"
""" The extras path """

ENTITY_MANAGER_ARGUMENTS = {"engine" : "sqlite",
                            "connection_parameters" : {"autocommit" : False}}
""" The entity manager arguments """

CONNECTION_PARAMETERS_VALUE = "connection_parameters"
""" The connection parameters value """

FILE_PATH_VALUE = "file_path"
""" The file path value """

DEFAULT_DATABASE_SUFFIX = "database.db"
""" The default database suffix """

DEFAULT_DATABASE_PREFIX = "web_mvc_encryption_"
""" The default database prefix """

DEFAULT_NUMBER_BITS = 256
""" The default number of bits """

class WebMvcEncryption:
    """
    The web mvc encryption class.
    """

    web_mvc_encryption_plugin = None
    """ The web mvc encryption plugin """

    web_mvc_encryption_main_controller = None
    """ The web mvc encryption main controller """

    web_mvc_encryption_consumer_controller = None
    """ The web mvc encryption consumer controller """

    web_mvc_encryption_entity_models = None
    """ the web mvc encryption entity models """

    keys_map = {}
    """ The map of keys """

    def __init__(self, web_mvc_encryption_plugin):
        """
        Constructor of the class.

        @type web_mvc_encryption_plugin: WebMvcEncryptionPlugin
        @param web_mvc_encryption_plugin: The web mvc encryption plugin.
        """

        self.web_mvc_encryption_plugin = web_mvc_encryption_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_encryption_plugin.web_mvc_utils_plugin

        # retrieves the entity manager arguments
        entity_manager_arguments = self.get_entity_manager_arguments()

        # retrieves the current directory path
        current_directory_path = os.path.dirname(__file__)

        # loads the mvc utils in the web mvc encryption controllers module
        web_mvc_encryption_controllers = web_mvc_utils_plugin.import_module_mvc_utils("web_mvc_encryption_controllers", "web_mvc_encryption.encryption", current_directory_path)

        # creates the web mvc encryption main controller
        self.web_mvc_encryption_main_controller = web_mvc_utils_plugin.create_controller(WebMvcEncryptionMainController, [self.web_mvc_encryption_plugin, self], {})

        # creates the web mvc encryption consumer controller
        self.web_mvc_encryption_consumer_controller = web_mvc_utils_plugin.create_controller(web_mvc_encryption_controllers.ConsumerController, [self.web_mvc_encryption_plugin, self], {})

        # creates the entity models classes by creating the entity manager and updating the classes
        self.web_mvc_encryption_entity_models = web_mvc_utils_plugin.create_entity_models("web_mvc_encryption_entity_models", entity_manager_arguments, current_directory_path)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the web mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return ((r"^web_mvc_encryption/?$", self.web_mvc_encryption_main_controller.handle_web_mvc_encryption_index),
                (r"^web_mvc_encryption/index$", self.web_mvc_encryption_main_controller.handle_web_mvc_encryption_index),
                (r"^web_mvc_encryption/sign$", self.web_mvc_encryption_main_controller.handle_web_mvc_encryption_sign),
                (r"^web_mvc_encryption/verify$", self.web_mvc_encryption_main_controller.handle_web_mvc_encryption_verify),
                (r"^web_mvc_encryption/consumers/new$", self.web_mvc_encryption_consumer_controller.handle_new))

    def get_communication_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as communication patterns,
        to the web mvc service. The tuple should relate the route with a tuple
        containing the data handler, the connection changed handler and the name
        of the connection.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as communication patterns,
        to the web mvc service.
        """

        return ()

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the web mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_encryption_plugin.manager

        # retrieves the web mvc encryption plugin path
        web_mvc_encryption_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_encryption_plugin.id)

        return ((r"^web_mvc_encryption/resources/.+$", (web_mvc_encryption_plugin_path + "/" + EXTRAS_PATH, "web_mvc_encryption/resources")),)

    def set_configuration_property(self, configuration_property):
        # retrieves the configuration
        configuration = configuration_property.get_data()

        # retrieves the extension map
        keys_map = configuration["keys"]

        # sets the keys map
        self.keys_map = keys_map

    def unset_configuration_property(self):
        # sets the keys map
        self.keys_map = {}

    def get_entity_manager_arguments(self):
        """
        Retrieves the entity manager arguments.

        @rtype: Dictionary
        @return: The entity manager arguments.
        """

        # retrieves the resource manager plugin
        resource_manager_plugin = self.web_mvc_encryption_plugin.resource_manager_plugin

        # creates the entity manager arguments map
        entity_manager_arguments = {}

        # copies the entity manager arguments constant to the new entity manager arguments
        colony.libs.map_util.map_copy_deep(ENTITY_MANAGER_ARGUMENTS, entity_manager_arguments)

        # retrieves the system database file name resource
        system_database_filename_resource = resource_manager_plugin.get_resource("system.database.file_name")

        # in case the system database filename resource
        # is defined
        if system_database_filename_resource:
            # retrieves the system database filename suffix
            system_database_filename_suffix = system_database_filename_resource.data
        # otherwise
        else:
            # sets the system database filename suffix as the default one
            system_database_filename_suffix = DEFAULT_DATABASE_SUFFIX

        # creates the system database file name value using the prefix and suffix values
        system_database_filename = DEFAULT_DATABASE_PREFIX + system_database_filename_suffix

        # retrieves the web mvc encryption plugin id
        web_mvc_encryption_plugin_id = self.web_mvc_encryption_plugin.id

        # creates the database file path using the plugin id and the system database filename
        database_file_path = "%configuration:" + web_mvc_encryption_plugin_id + "%/" + system_database_filename

        # sets the file path in the entity manager arguments
        entity_manager_arguments[CONNECTION_PARAMETERS_VALUE][FILE_PATH_VALUE] = database_file_path

        # returns the entity manager arguments
        return entity_manager_arguments

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

    def handle_web_mvc_encryption_index(self, rest_request, parameters = {}):
        """
        Handles the given web mvc encryption index rest request.

        @type rest_request: RestRequest
        @param rest_request: The web mvc encryption index rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the template file
        template_file = self.retrieve_template_file("general.html.tpl")

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

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

        # signs the message and retrieves the signature
        signature = self._sign(rest_request)

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

        # verifies the signature and retrieves the return value string
        return_value_string = self._verify(rest_request)

        # sets the return value string as the contents
        self.set_contents(rest_request, return_value_string, "text/plain")

        # returns true
        return True

    def _sign(self, rest_request):
        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.web_mvc_encryption_plugin.encryption_ssl_plugin

        # retrieves the web mvc encryption consumer controller
        web_mvc_encryption_consumer_controller = self.web_mvc_encryption.web_mvc_encryption_consumer_controller

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the api key from the form data map
        api_key = form_data_map.get("api_key", None)

        # retrieves the key name from the form data map
        key_name = form_data_map["key_name"]

        # retrieves the message from the form data map
        message = form_data_map["message"]

        # retrieves the algorithm name from the form data map
        algorithm_name = form_data_map.get("algorithm_name", "sha1")

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # validates the api key
        web_mvc_encryption_consumer_controller._validate_api_key(rest_request, api_key)

        # retrieves the private key path for the key name
        private_key_path = self._get_key_path(key_name, "private_key")

        # decodes the message (using base 64)
        message_decoded = base64.b64decode(message)

        # signs the message (decoded) in base 64
        signature = ssl_structure.sign_base_64(private_key_path, algorithm_name, message_decoded)

        # returns the signature
        return signature

    def _verify(self, rest_request):
        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.web_mvc_encryption_plugin.encryption_ssl_plugin

        # retrieves the web mvc encryption consumer controller
        web_mvc_encryption_consumer_controller = self.web_mvc_encryption.web_mvc_encryption_consumer_controller

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the api key from the form data map
        api_key = form_data_map.get("api_key", None)

        # retrieves the key name from the form data map
        key_name = form_data_map["key_name"]

        # retrieves the signature from the form data map
        signature = form_data_map["signature"]

        # retrieves the message from the form data map
        message = form_data_map["message"]

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # validates the api key
        web_mvc_encryption_consumer_controller._validate_api_key(rest_request, api_key)

        # retrieves the public key path for the key name
        piublic_key_path = self._get_key_path(key_name, "public_key")

        # decodes the message (using base 64)
        message_decoded = base64.b64decode(message)

        # verifies the signature in base 64
        return_value = ssl_structure.verify_base_64(piublic_key_path, signature, message_decoded)

        # retrieves the return value in (simple) string mode
        return_value_string = return_value and "0" or "1"

        # returns the return value string
        return return_value_string

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
