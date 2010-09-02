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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class EmailPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Email plugin.
    """

    id = "pt.hive.colony.plugins.misc.email"
    name = "Email Plugin"
    short_name = "Email"
    description = "Email Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/misc/email/resources/baf.xml"}
    capabilities = ["email", "console_command_extension", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []

    email = None
    console_email = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.email.email_system
        import misc.email.console_email
        self.email = misc.email.email_system.Email(self)
        self.console_email = misc.email.console_email.ConsoleEmail(self)

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

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_console_extension_name(self):
        return self.console_email.get_console_extension_name()

    def get_all_commands(self):
        return self.console_email.get_all_commands()

    def get_handler_command(self, command):
        return self.console_email.get_handler_command(command)

    def get_help(self):
        return self.console_email.get_help()

    def send_email(self, email_sender, email_receiver, name_sender, name_receiver, subject, contents, smtp_server, smtp_login, smtp_password):
        """
        Sends an email for the given configuration.

        @type email_sender: String
        @param email_sender: The sender of the email.
        @type email_receiver: String
        @param email_receiver: The receiver of the email.
        @type name_sender: String
        @param name_sender: The name of the sender.
        @type name_receiver: String
        @param name_receiver: The name of the receiver.
        @type subject: String
        @param subject: The subject of the email.
        @type contents: String
        @param contents: The contents of the email.
        @type smtp_server: String
        @param smtp_server: The smtp server to be used when sending the email.
        @type smtp_login: String
        @param smtp_login: The login to be used in the server authentication.
        @type smtp_password: String
        @param smtp_password: The password to be used in the server authentication.
        """

        self.email.send_email(email_sender, email_receiver, name_sender, name_receiver, subject, contents, smtp_server, smtp_login, smtp_password)
