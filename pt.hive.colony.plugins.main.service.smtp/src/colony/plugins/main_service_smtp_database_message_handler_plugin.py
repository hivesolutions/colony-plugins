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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class MainServiceSmtpDatabaseMessageHandlerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Smtp Service Main Database Message Handler plugin.
    """

    id = "pt.hive.colony.plugins.main.service.smtp.database_message_handler"
    name = "Smtp Service Main Database Message Handler Plugin"
    short_name = "Smtp Service Main Database Message Handler"
    description = "The plugin that offers the smtp service database message handler"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_service_smtp_database_message_handler/database_message_handler/resources/baf.xml"
    }
    capabilities = [
        "smtp_service_message_handler",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.mail.storage.database", "1.0.0")
    ]
    main_modules = [
        "main_service_smtp_database_message_handler.database_message_handler.main_service_smtp_database_message_handler_exceptions",
        "main_service_smtp_database_message_handler.database_message_handler.main_service_smtp_database_message_handler_system"
    ]

    main_service_smtp_database_message_handler = None
    """ The main service smtp database message handler """

    mail_storage_database_plugin = None
    """ The mail storage database plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_service_smtp_database_message_handler.database_message_handler.main_service_smtp_database_message_handler_system
        self.main_service_smtp_database_message_handler = main_service_smtp_database_message_handler.database_message_handler.main_service_smtp_database_message_handler_system.MainServiceSmtpDatabaseMessageHandler(self)

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

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.main_service_smtp_database_message_handler.get_handler_name()

    def handle_message(self, message, arguments):
        """
        Handles the given smtp message.

        @type message: SmtpMessage
        @param message: The smtp message to handled.
        @type arguments: Dictionary
        @param arguments: The arguments to the message handling.
        """

        return self.main_service_smtp_database_message_handler.handle_message(message, arguments)

    def get_mail_storage_database_plugin(self):
        return self.mail_storage_database_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.mail.storage.database")
    def set_mail_storage_database_plugin(self, mail_storage_database_plugin):
        self.mail_storage_database_plugin = mail_storage_database_plugin
