#!/usr/bin/python
# -*- coding: utf-8 -*-

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

models = colony.libs.import_util.__import__("models")
mvc_utils = colony.libs.import_util.__import__("mvc_utils")

class ConsumerController:
    """
    The crypton consumer controller.
    """

    crypton_plugin = None
    """ The crypton plugin """

    crypton = None
    """ The crypton """

    def __init__(self, crypton_plugin, crypton):
        """
        Constructor of the class.

        @type crypton_plugin: CryptonPlugin
        @param crypton_plugin: The crypton plugin.
        @type crypton: Crypton
        @param crypton: The crypton.
        """

        self.crypton_plugin = crypton_plugin
        self.crypton = crypton

    def handle_create(self, rest_request, parameters = {}):
        """
        Handles the new consumer rest request.

        @type rest_request: RestRequest
        @param rest_request: The crypton new rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the consumer from the rest request
        # and applies it to the consumer entity
        consumer = self.get_field(rest_request, "consumer", {})
        consumer_entity = models.Consumer.new(consumer)

        # generates the consumer api key
        consumer_entity.generate_api_key()

        # stores the consumer in the data source
        consumer_entity.store(mvc_utils.PERSIST_SAVE_TYPE)
