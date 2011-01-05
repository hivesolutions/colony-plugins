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

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class ConsumerController:
    """
    The web mvc encryption consumer controller.
    """

    pecway_main_plugin = None
    """ The pecway main plugin """

    pecway_main = None
    """ The pecway main """

    def __init__(self, pecway_main_plugin, pecway_main):
        """
        Constructor of the class.

        @type pecway_main_plugin: PecwayMainPlugin
        @param pecway_main_plugin: The pecway main plugin.
        @type pecway_main: PecwayMain
        @param pecway_main: The pecway main.
        """

        self.pecway_main_plugin = pecway_main_plugin
        self.pecway_main = pecway_main

    def start(self):
        """
        Method called upon structure initialization.
        """

        pass

    @web_mvc_utils.transaction_method("pecway_main.pecway_main_entity_models.entity_manager")
    def _save_consumer(self, rest_request, consumer):
        # retrieves the web mvc encryption entity models
        web_mvc_encryption_entity_models = self.pecway_main.pecway_main_entity_models

        # retrieves the consumer entity
        consumer_entity = self.get_entity_model(web_mvc_encryption_entity_models.entity_manager, web_mvc_encryption_entity_models.Consumer, consumer)

        # validates the consumer entity
        self.validate_model_exception(consumer_entity, "consumer validation failed")

        # saves the consumer entity
        consumer_entity.save_update()

        # returns the consumer entity
        return consumer_entity
