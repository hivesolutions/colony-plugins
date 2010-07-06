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

__revision__ = "$LastChangedRevision: 2688 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-16 12:24:34 +0100 (qui, 16 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class CommunicationPushPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Communication Push plugin.
    """

    id = "pt.hive.colony.plugins.communication.push"
    name = "Communication Push Plugin"
    short_name = "Communication Push"
    description = "A plugin to manager the push notifications communication"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.JYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/communication_push/push/resources/baf.xml"}
    capabilities = ["communication.push", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["communication_push.push.communication_push_system"]

    communication_push = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global communication_push
        import communication_push.push.communication_push_system
        self.communication_push = communication_push.push.communication_push_system.CommunicationPush(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def add_communication_handler(self, communication_name, communication_handler_name, communication_handler_method):
        """
        Adds a communication handler to the communication push system.

        @type communication_name: String
        @param communication_name: The name of the communication "channel" to be used.
        @type communication_handler_name: String
        @param communication_handler_name: The name of the handler being added.
        @type communication_handler_method: Method
        @param communication_handler_method: The method to be called on communication notification.
        """

        return self.communication_push.add_communication_handler(communication_name, communication_handler_name, communication_handler_method)

    def remove_communication_handler(self, communication_name, communication_handler_name, communication_handler_method):
        """
        Removes a communication handler from the communication push system.

        @type communication_name: String
        @param communication_name: The name of the communication "channel" to be used.
        @type communication_handler_name: String
        @param communication_handler_name: The name of the handler being removed.
        @type communication_handler_method: Method
        @param communication_handler_method: The method to be called on communication notification.
        """

        return self.communication_push.remove_communication_handler(communication_name, communication_handler_name, communication_handler_method)

    def remove_all_communication_handler(self, communication_handler_name):
        """
        Removes the communication handler from all the communication "channels".

        @type communication_handler_name: String
        @param communication_handler_name: The name of the handler to have the
        communications removed.
        """

        return self.communication_push.remove_all_communication_handler(communication_handler_name)

    def send_broadcast_notification(self, communication_name, notification):
        """
        Sends a broadcast notification to all the communication handler activated.

        @type communication_name: String
        @param communication_name: The name of the communication "channel" to be used.
        @type push_notification: String
        @param push_notification: The push notification to be broadcasted.
        """

        return self.communication_push.send_broadcast_notification(communication_name, notification)

    def generate_notification(self, message, sender_id):
        """
        Generates a push notification for the given message and
        sender id.

        @type message: String
        @param message: The message to be used in the notification.
        @type sender_id: String
        @param sender_id: The id of the notification sender.
        @rtype: PushNotification
        @return: The generated push notification reference.
        """

        return self.communication_push.generate_notification(message, sender_id)
