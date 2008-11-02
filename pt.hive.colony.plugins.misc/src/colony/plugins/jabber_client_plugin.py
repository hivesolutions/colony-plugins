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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

#@todo: comment this class
class JabberClientPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Jabber Client plugin
    """

    id = "pt.hive.colony.plugins.misc.jabber_client"
    name = "Jabber Client Plugin"
    short_name = "Jabber Client"
    description = "Jabber Client Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    #"bot_output",
    capabilities = ["main", "jabber_client", "bot_input", "bot_output", "console_command_extension"]
    capabilities_allowed = ["jabber_client"]
    dependencies = [colony.plugins.plugin_system.PackageDependency(
                    "xmpppy", "xmpp", "0.4.x", "http://xmpppy.sourceforge.net"),
                    colony.plugins.plugin_system.PackageDependency(
                    "dnspython", "dns", "1.6.x", "http://www.dnspython.org")]
    events_handled = ["jabber_client_connect", "jabber_client_send", "jabber_client_disconnect", "jabber_register_message_handler"]
    events_registrable = ["jabber_client_connect", "jabber_client_send", "jabber_client_disconnect", "jabber_register_message_handler"]

    jabber_client = None
    
    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.jabber_client.jabber_client_system
        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.jabber_client = misc.jabber_client.jabber_client_system.JabberClient(self)
        # notifies the ready semaphore
        self.release_ready_semaphore()
        self.jabber_client.load()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.jabber_client.unload()
        self.jabber_client = None

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.event_handler("pt.hive.colony.plugins.misc.jabber_client", "1.0.0")
    def event_handler(self, event_name, *event_args):
        try:
            colony.plugins.plugin_system.Plugin.event_handler(self, event_name, *event_args)
        except Exception, exception:
            colony.plugins.plugin_system.Plugin.treat_exception(self, exception)

    def register_message_handler(self, id, handler):
        self.generate_event("jabber_register_message_handler", [id, handler])

    def connect(self, jabber_id, password):
        self.generate_event("jabber_client_connect", [jabber_id, password])

    def disconnect(self, jabber_id):
        self.generate_event("jabber_client_disconnect", [jabber_id])

    def send(self, sender_jabber_id, receiver_jabber_id, message):
        self.generate_event("jabber_client_send", [sender_jabber_id, receiver_jabber_id, message])

    def get_console_extension_name(self):
        return self.jabber_client.get_console_extension_name()

    def get_all_commands(self):
        return self.jabber_client.get_all_commands()

    def get_handler_command(self, command):
        return self.jabber_client.get_handler_command(command)

    def get_help(self):
        return self.jabber_client.get_help()

    @colony.plugins.decorators.event_handler_method("jabber_client_connect")
    def jabber_client_connect_handler(self, event_name, jabber_id, password, *event_args):
        if self.is_loaded():
            if not self.jabber_client.loop:
                self.jabber_client.start_semaphore.release()
            self.jabber_client.event_semaphore.acquire()
            self.jabber_client.set_connect_parameters(jabber_id, password)

    @colony.plugins.decorators.event_handler_method("jabber_client_send")
    def jabber_client_send_handler(self, event_name, sender_jabber_id, receiver_jabber_id, message, *event_args):
        if self.is_loaded():
            self.jabber_client.set_send_parameters(sender_jabber_id, receiver_jabber_id, message)

    @colony.plugins.decorators.event_handler_method("jabber_client_disconnect")
    def jabber_client_disconnect_handler(self, event_name, jabber_id, *event_args):
        if self.is_loaded():
            self.jabber_client.event_semaphore.acquire()
            self.jabber_client.set_disconnect_parameters(jabber_id)

    @colony.plugins.decorators.event_handler_method("jabber_register_message_handler")
    def jabber_register_message_handler_handler(self, event_name, id, handler, *event_args):
        if self.is_loaded():
            self.jabber_client.event_semaphore.acquire()
            self.jabber_client.set_register_message_handler_parameters(id, handler)
