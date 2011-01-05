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

import base64

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_ENCRYPTION_RESOURCES_PATH = "web_mvc_encryption/encryption/resources"
""" The web mvc encryption resources path """

TEMPLATES_PATH = WEB_MVC_ENCRYPTION_RESOURCES_PATH + "/templates"
""" The templates path """

EXTRAS_PATH = WEB_MVC_ENCRYPTION_RESOURCES_PATH + "/extras"
""" The extras path """

class WebMvcEncryption:
    """
    The web mvc encryption class.
    """

    web_mvc_encryption_plugin = None
    """ The web mvc encryption plugin """

    web_mvc_encryption_main_controller = None
    """ The web mvc encryption main controller """

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

        # creates the web mvc encryption main controller
        self.web_mvc_encryption_main_controller = web_mvc_utils_plugin.create_controller(WebMvcEncryptionMainController, [self.web_mvc_encryption_plugin, self], {})

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
                (r"^web_mvc_encryption/verify$", self.web_mvc_encryption_main_controller.handle_web_mvc_encryption_verify))

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

        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.web_mvc_encryption_plugin.encryption_ssl_plugin

        # retrieves the keys map
        keys_map = self.web_mvc_encryption.keys_map

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the key name from the form data map
        key_name = form_data_map["key_name"]

        # retrieves the message from the form data map
        message = form_data_map["message"]

        # retrieves the algorithm name from the form data map
        algorithm_name = form_data_map.get("algorithm_name", "sha1")

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # retrieves the key for the key name
        key = keys_map.get(key_name, {})

        # retrieves the private key path
        private_key_path = key.get("private_key", None)

        # decodes the message (using base 64)
        message_decoded = base64.b64decode(message)

        # signs the message (decoded) in base 64
        signature = ssl_structure.sign_base_64(private_key_path, algorithm_name, message_decoded)

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

        # retrieves the encryption ssl plugin
        encryption_ssl_plugin = self.web_mvc_encryption_plugin.encryption_ssl_plugin

        # retrieves the keys map
        keys_map = self.web_mvc_encryption.keys_map

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the key name from the form data map
        key_name = form_data_map["key_name"]

        # retrieves the signature from the form data map
        signature = form_data_map["signature"]

        # retrieves the message from the form data map
        message = form_data_map["message"]

        # creates the ssl structure
        ssl_structure = encryption_ssl_plugin.create_structure({})

        # retrieves the key for the key name
        key = keys_map.get(key_name, {})

        # retrieves the public key path
        piublic_key_path = key.get("public_key", None)

        # decodes the message (using base 64)
        message_decoded = base64.b64decode(message)

        # verifies the signature in base 64
        return_value = ssl_structure.verify_base_64(piublic_key_path, signature, message_decoded)

        # retrieves the return value in (simple) string mode
        return_value_string = return_value and "0" or "1"

        # sets the return value string as the contents
        self.set_contents(rest_request, return_value_string, "text/plain")

        # returns true
        return True
