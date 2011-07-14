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

__revision__ = "$LastChangedRevision: 2688 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-16 12:24:34 +0100 (qui, 16 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class CommunicationPushPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Communication Push plugin.
    """

    id = "pt.hive.colony.plugins.communication.push"
    name = "Communication Push Plugin"
    short_name = "Communication Push"
    description = "A plugin to manager the push notifications communication"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/communication_push/push/resources/baf.xml"
    }
    capabilities = [
        "communication.push",
        "diagnostics",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "communication.push_persistence"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.work.work_pool_manager", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.guid", "1.0.0")
    ]
    main_modules = [
        "communication_push.push.communication_push_system"
    ]

    communication_push = None
    """ The communication push """

    communication_push_persistence_plugins = []
    """ The communication push persistence plugins """

    work_pool_manager_plugin = None
    """ The work pool manager plugin """

    guid_plugin = None
    """ The guid plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import communication_push.push.communication_push_system
        self.communication_push = communication_push.push.communication_push_system.CommunicationPush(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

        # starts the pool
        self.communication_push.start_pool()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

        # stops the pool
        self.communication_push.stop_pool()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

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
        It also removes the extra meta information associated with the
        communication handler.

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

    def get_communication_information(self, communication_handler_name):
        """
        Retrieves an information structure on the communication
        with the given name.

        @type communication_name: String
        @param communication_name: The name of the communication
        to retrieve the information structure.
        @rtype: Dictionary
        @return: The information structure on the communication.
        """

        return self.communication_push.get_communication_information(communication_handler_name)

    def get_communication_handler_information(self, communication_handler_name):
        """
        Retrieves an information structure on the communication
        handler with the given name.

        @type communication_handler_name: String
        @param communication_handler_name: The name of the communication
        handler to retrieve the information structure.
        @rtype: Dictionary
        @return: The information structure on the communication
        handler.
        """

        return self.communication_push.get_communication_handler_information(communication_handler_name)

    def get_communication_profile_information(self, communication_profile_name):
        """
        Retrieves an information structure on the communication
        profile with the given name.

        @type communication_profile_name: String
        @param communication_profile_name: The name of the communication
        profile to retrieve the information structure.
        @rtype: Dictionary
        @return: The information structure on the communication
        profile.
        """

        return self.communication_push.get_communication_profile_information(communication_profile_name)

    def get_communication_handler_property(self, communication_handler_name, property_name):
        """
        Retrieves a communication handler property for the
        given communication handler name and property name.

        @type communication_handler_name: String
        @param communication_handler_name: The name of the communication
        handler to retrieve the property.
        @type property_name: String
        @param property_name: The name of the property to retrieve.
        @rtype: Object
        @return: The retrieved property.
        """

        return self.communication_push.get_communication_handler_property(communication_handler_name, property_name)

    def set_communication_handler_property(self, communication_handler_name, property_name, property_value):
        """
        Sets a communication handler property for the given
        communication handler name, property name and property value.

        @type communication_handler_name: String
        @param communication_handler_name: The name of the communication
        handler to set the property.
        @type property_name: String
        @param property_name: The name of the property to set.
        @type property_value: Object
        @param property_value: The value of the property to set.
        """

        return self.communication_push.set_communication_handler_property(communication_handler_name, property_name, property_value)

    def load_communication_profile(self, communication_handler_name, communication_profile_name, communication_handler_method):
        """
        Loads a communication profile into a communication handler.
        The loading of the communication profile implies the registration of all the
        communication "channels" associated with the profile.

        @type communication_handler_name: String
        @param communication_handler_name: The name of the communication handler
        to be loaded with the profile.
        @type communication_profile_name: String
        @param communication_profile_name: The name of the profile to be used in the
        profile loading.
        @type communication_handler_method: Method
        @param communication_handler_method: The method to be called on communication notification.
        """

        return self.communication_push.load_communication_profile(communication_handler_name, communication_profile_name, communication_handler_method)

    def unload_communication_profile(self, communication_handler_name, communication_profile_name, communication_handler_method):
        """
        Unloads a communication profile from a communication handler.
        The loading of the communication profile implies the unregistration from all the
        communication "channels" associated with the profile.

        @type communication_handler_name: String
        @param communication_handler_name: The name of the communication handler
        to be unloaded from the profile.
        @type communication_profile_name: String
        @param communication_profile_name: The name of the profile to be used in the
        profile unloading.
        @type communication_handler_method: Method
        @param communication_handler_method: The method to be called on communication notification.
        """

        return self.communication_push.unload_communication_profile(communication_handler_name, communication_profile_name, communication_handler_method)

    def unload_all_communication_profile(self, communication_handler_name):
        """
        Removes the communication handler from all the communication profiles.

        @type communication_handler_name: String
        @param communication_handler_name: The name of the handler to have the
        communication profiles removed.
        """

        return self.communication_push.unload_all_communication_profile(communication_handler_name)

    def set_communication_profile(self, communication_profile_name, communication_name):
        """
        Sets (adds) a communication to the given communication profile.

        @type communication_profile_name: String
        @param communication_profile_name: The name of the communication profile
        to add the communication.
        @type communication_name: String
        @param communication_name: The name of the communication to be added.
        """

        return self.communication_push.set_communication_profile(communication_profile_name, communication_name)

    def unset_communication_profile(self, communication_profile_name, communication_name):
        """
        Unsets (removes) a communication from the given communication profile.

        @type communication_profile_name: String
        @param communication_profile_name: The name of the communication profile
        to remove the communication.
        @type communication_name: String
        @param communication_name: The name of the communication to be removed.
        """

        return self.communication_push.unset_communication_profile(communication_profile_name, communication_name)

    def insert_notification_buffer(self, communication_name, push_notification):
        """
        Inserts a notification into the notification buffer of the given
        communication name.

        @type communication_name: String
        @param communication_name: The name of the communication to
        insert the push notification.
        @type push_notification: PushNotification
        @param push_notification: The push notification to be inserted.
        """

        return self.communication_push.insert_notification_buffer(communication_name, push_notification)

    def get_notifications_buffer(self, communication_name, count):
        """
        Retrieves the notifications from the notification buffer, for the given
        communication and respecting the given count value.

        @type communication_name: String
        @param communication_name: The name of the communication to
        retrieve the notifications.
        @type count: int
        @param count: The maximum number of notifications to be retrieved.
        @rtype: List
        @return: The list of retrieved notifications.
        """

        return self.communication_push.get_notifications_buffer(communication_name, count)

    def get_notifications_buffer_guid(self, communication_name, guid):
        """
        Retrieves the notifications from the notification buffer, for the given
        communication and respecting the given count value.
        This method uses the guid as a filter for notification retrieval.

        @type communication_name: String
        @param communication_name: The name of the communication to
        retrieve the notifications.
        @type guid: String
        @param guid: The guid to be used as filter to the retrieval
        of the notifications.
        @rtype: List
        @return: The list of retrieved notifications.
        """

        return self.communication_push.get_notifications_buffer_guid(communication_name, guid)

    def clear_notifications_buffer(self, communication_name):
        """
        Clears the notifications notification buffer for the given
        communication name.

        @type communication_name: String
        @param communication_name: The communication name of the
        notification buffer to cleared.
        """

        return self.communication_push.clear_notifications_buffer(communication_name)

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

    def print_diagnostics(self):
        """
        Prints diagnostic information about the plugin instance.
        """

        return self.communication_push.print_diagnostics()

    @colony.base.decorators.load_allowed_capability("communication.push_persistence")
    def communication_push_persistence_load_allowed(self, plugin, capability):
        self.communication_push_persistence_plugins.append(plugin)
        self.communication_push.communication_push_persistence_load(plugin)

    @colony.base.decorators.unload_allowed_capability("communication.push_persistence")
    def communication_push_persistence_unload_allowed(self, plugin, capability):
        self.communication_push_persistence_plugins.remove(plugin)
        self.communication_push.communication_push_persistence_unload(plugin)

    def get_work_pool_manager_plugin(self):
        return self.work_pool_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.work.work_pool_manager")
    def set_work_pool_manager_plugin(self, work_pool_manager_plugin):
        self.work_pool_manager_plugin = work_pool_manager_plugin

    def get_guid_plugin(self):
        return self.guid_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.guid")
    def set_guid_plugin(self, guid_plugin):
        self.guid_plugin = guid_plugin
