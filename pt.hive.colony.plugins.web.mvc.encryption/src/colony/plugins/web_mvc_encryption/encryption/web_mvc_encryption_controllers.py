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

import colony.libs.importer_util

import web_mvc_encryption_exceptions

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

VALID_STATUS_VALUE = 1
""" The valid status value """

INVALID_STATUS_VALUE = 1
""" The invalid status value """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

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

    def handle_new(self, rest_request, parameters = {}):
        """
        Handles the new consumer rest request.

        @type rest_request: RestRequest
        @param rest_request: The web mvc encryption new rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # returns false in case this is not post request
        if not rest_request.is_post():
            return False

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
        consumer_create = {"status" : INVALID_STATUS_VALUE,
                           "api_key" : self._generate_api_key()}

        # retrieves the consumer entity
        consumer_entity = self.get_entity_model(web_mvc_encryption_entity_models.entity_manager, web_mvc_encryption_entity_models.Consumer, consumer, consumer_create)

        # validates the consumer entity
        self.validate_model_exception(consumer_entity, "consumer validation failed")

        # saves the consumer entity
        consumer_entity.save_update()

        # returns the consumer entity
        return consumer_entity

    def _validate_api_key(self, rest_request, api_key):
        # retrieves the web mvc encryption entity models
        web_mvc_encryption_entity_models = self.web_mvc_encryption.web_mvc_encryption_entity_models

        # retrieves the entity manager
        entity_manager = web_mvc_encryption_entity_models.entity_manager

        # retrieves the consumer entities with the specified api key
        consumer_entities = entity_manager._find_all_options(web_mvc_encryption_entity_models.Consumer, {"filters" : [{"filter_type" : "equals",
                                                                                                                       "filter_fields" : [{"field_name" : "api_key",
                                                                                                                                           "field_value" : api_key}]},
                                                                                                                       {"filter_type" : "equals",
                                                                                                                       "filter_fields" : [{"field_name" : "status",
                                                                                                                                           "field_value" : VALID_STATUS_VALUE}]}]})

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
