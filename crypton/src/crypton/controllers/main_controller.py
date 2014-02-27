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

import colony.libs.import_util

DEFAULT_ALGORITHM_NAME = "sha1"
""" The default algorithm name """

models = colony.libs.import_util.__import__("models")
controllers = colony.libs.import_util.__import__("controllers")
mvc_utils = colony.libs.import_util.__import__("mvc_utils")

class MainController(controllers.Controller):
    """
    The crypton main controller.
    """

    def handle_encrypt(self, request, parameters = {}):
        """
        Handles the given crypton encrypt request.

        @type request: Request
        @param request: The crypton encrypt request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the required controllers
        signature_controller = self.system.signature_controller

        # processes the form data and retrieves its attributes
        form_data_map = self.process_form_data(request)
        api_key = form_data_map.get("api_key", None)
        key_name = form_data_map["key_name"]
        message = form_data_map["message"]

        # encrypts the message and retrieves the encrypted message
        message_e = signature_controller.encrypt(request, api_key, key_name, message)

        # sets the encrypted message as the contents
        self.set_contents(request, message_e, "text/plain")

    def handle_decrypt(self, request, parameters = {}):
        """
        Handles the given crypton decrypt request.

        @type request: Request
        @param request: The crypton decrypt request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the required controllers
        signature_controller = self.system.signature_controller

        # processes the form data and retrieves its attributes
        form_data_map = self.process_form_data(request)
        api_key = form_data_map.get("api_key", None)
        key_name = form_data_map["key_name"]
        message_e = form_data_map["message_e"]

        # decrypts the encrypted message, retrieving the original message
        message = signature_controller.decrypt(request, api_key, key_name, message_e)

        # sets the message as the contents
        self.set_contents(request, message, "text/plain")

    def handle_sign(self, request, parameters = {}):
        """
        Handles the given crypton sign request.

        @type request: Request
        @param request: The crypton sign request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the required controllers
        signature_controller = self.system.signature_controller

        # processes the form data and retrieves its attributes
        form_data_map = self.process_form_data(request)
        api_key = form_data_map.get("api_key", None)
        key_name = form_data_map["key_name"]
        message = form_data_map["message"]
        algorithm_name = form_data_map.get("algorithm_name", DEFAULT_ALGORITHM_NAME)

        # signs the message and retrieves the signature
        signature = signature_controller.sign(request, api_key, key_name, message, algorithm_name)

        # sets the signature as the contents
        self.set_contents(request, signature, "text/plain")

    def handle_verify(self, request, parameters = {}):
        """
        Handles the given crypton verify request.

        @type request: Request
        @param request: The crypton verify request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the required controllers
        signature_controller = self.system.signature_controller

        # processes the form data and retrieves its attributes
        form_data_map = self.process_form_data(request)
        api_key = form_data_map.get("api_key", None)
        key_name = form_data_map["key_name"]
        signature = form_data_map["signature"]
        message = form_data_map["message"]

        # verifies the signature and retrieves the return value string
        return_value_string = signature_controller.verify(request, api_key, key_name, signature, message)

        # sets the return value string as the contents
        self.set_contents(request, return_value_string, "text/plain")
