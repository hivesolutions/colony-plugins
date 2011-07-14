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

import colony.base.plugin_system
import colony.base.decorators

class EmailMessagingExtensionPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Email Messaging Extension plugin.
    """

    id = "pt.hive.colony.plugins.messaging.extensions.email"
    name = "Stdout Messaging Extension Plugin"
    short_name = "Stdout Messaging Extension"
    description = "A plugin to manage stdout messaging extension"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/messaging_extensions/email/resources/baf.xml"
    }
    capabilities = [
        "messaging_extension",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.email", "1.0.0")
    ]
    main_modules = [
        "messaging_extensions.email.email_messaging_extension_system"
    ]

    email_messaging_extension = None
    """ The email messaging extension """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import messaging_extensions.email.email_messaging_extension_system
        self.email_messaging_extension = messaging_extensions.email.email_messaging_extension_system.EmailMessagingExtension(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_messaging_service_id(self):
        """
        Retrieves the messaging service id.

        @rtype: String
        @return: The messaging service id.
        """

        return self.email_messaging_extension.get_messaging_service_id()

    def send_message(self, message_attributes):
        """
        Sends a message using the given message attributes.

        @type message_attributes: Dictionary
        @param message_attributes: The attributes of the message to
        be sent.
        """

        return self.email_messaging_extension.send_message(message_attributes)

    def get_email_plugin(self):
        return self.email_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.email")
    def set_email_plugin(self, email_plugin):
        self.email_plugin = email_plugin
