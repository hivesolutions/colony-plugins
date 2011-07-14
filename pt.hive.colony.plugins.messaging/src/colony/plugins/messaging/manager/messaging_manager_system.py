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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import messaging_manager_exceptions

class MessagingManager:
    """
    The messaging manager class.
    """

    messaging_manager_plugin = None
    """ The messaging manager plugin """

    messaging_service_id_messaging_extension_plugin_map = {}
    """ The map with the messaging service id associated with the messaging extension plugin """

    def __init__(self, messaging_manager_plugin):
        """
        Constructor of the class.

        @type messaging_manager_plugin: MessagingManagerPlugin
        @param messaging_manager_plugin: The messaging manager plugin.
        """

        self.messaging_manager_plugin = messaging_manager_plugin

        self.messaging_service_id_messaging_extension_plugin_map = {}

    def send_message(self, messaging_service_id, message_attributes):
        # in case the messaging service id exists in the messaging service id messaging extension plugin map
        if not messaging_service_id in self.messaging_service_id_messaging_extension_plugin_map:
            raise messaging_manager_exceptions.InvalidMessagingServiceIdException("service " + messaging_service_id + " is invalid")

        # retrieves the messaging extension plugin for the given messaging service id
        messaging_extension_plugin = self.messaging_service_id_messaging_extension_plugin_map[messaging_service_id]

        # send the message to the selected messaging extension plugin
        messaging_extension_plugin.send_message(message_attributes)

    def load_messaging_extension_plugin(self, messaging_extension_plugin):
        # retrieves the messaging service id
        messaging_service_id = messaging_extension_plugin.get_messaging_service_id()

        self.messaging_service_id_messaging_extension_plugin_map[messaging_service_id] = messaging_extension_plugin

    def unload_messaging_extension_plugin(self, messaging_extension_plugin):
        # retrieves the messaging service id
        messaging_service_id = messaging_extension_plugin.get_messaging_service_id()

        del self.messaging_service_id_messaging_extension_plugin_map[messaging_service_id]
