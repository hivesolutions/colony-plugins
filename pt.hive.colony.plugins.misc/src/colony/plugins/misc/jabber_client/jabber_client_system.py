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

import xmpp
import threading

CONSOLE_EXTENSION_NAME = "jabber_client"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### JABBER CLIENT HELP ###\n\
jabber_connect <jabber_id> <password>                         - connects to a XAMPP server\n\
jabber_disconnect <jabber_id>                                 - disconnects from the XAMPP server\n\
jabber_send <sender_jabber_id> <receiver_jabber_id> <message> - sends a message to a user in the server one is connected to\n\
jabber_list_clients                                           - retrieves a list of the currently connected clients"
""" The help text """

#@todo: comment this class
class JabberClient:

    commands = ["jabber_connect", "jabber_disconnect", "jabber_send", "jabber_list_clients"]

    loop = None
    connect_jabber_id = None
    connect_password = None
    disconnect_jabber_id = None
    send_sender_jabber_id = None
    send_receiver_jabber_id = None
    send_message = None
    register_message_handler_jabber_id = None
    register_message_handler_handler = None
    list_clients_output_method = None
    start_semaphore = None
    event_semaphore = None
    clients = {}
    message_handlers = {}
    unloading = False

    def __init__(self, parent_plugin):
        self.parent_plugin = parent_plugin
        self.clients = {}
        self.start_semaphore = threading.Semaphore(0)
        self.event_semaphore = threading.Semaphore()
        self.send_sender_jabber_id = []
        self.send_receiver_jabber_id = []
        self.send_message = []

    def load(self):
        self.start_semaphore.acquire()
        if not self.unloading:
            self.loop = True
            self.run_loop()

    def unload(self):
        self.unloading = True
        if not self.loop:
            self.start_semaphore.release()
        self.loop = False
        for jabber_id in self.clients:
            self.clients[jabber_id].disconnect()

    def register_message_handler(self, jabber_id, handler):
        if not jabber_id in self.message_handlers:
            self.message_handlers[jabber_id] = MessageHandler()
        self.message_handlers[jabber_id].register_message_handler(handler)

    def set_list_clients_parameters(self, output_method):
        self.list_clients_output_method = output_method

    def set_connect_parameters(self, jabber_id, password):
        self.connect_jabber_id = jabber_id
        self.connect_password = password

    def set_send_parameters(self, sender_jabber_id, receiver_jabber_id, send_message):
        self.send_sender_jabber_id.append(sender_jabber_id)
        self.send_receiver_jabber_id.append(receiver_jabber_id)
        self.send_message.append(send_message)

    def set_disconnect_parameters(self, jabber_id):
        self.disconnect_jabber_id = jabber_id

    def set_register_message_handler_parameters(self, id, handler):
        self.register_message_handler_jabber_id = id
        self.register_message_handler_handler = handler

    def clear_register_message_handler_parameters(self):
        self.register_message_handler_jabber_id = None
        self.register_message_handler_handler = None

    def clear_connect_parameters(self):
        self.connect_jabber_id = None
        self.connect_password = None

    def clear_send_parameters(self):
        del self.send_sender_jabber_id[0]
        del self.send_receiver_jabber_id[0]
        del self.send_message[0]

    def clear_disconnect_parameters(self):
        self.disconnect_jabber_id = None

    def is_connect_pending(self):
        return self.connect_jabber_id and self.connect_password

    def is_send_pending(self):
        return len(self.send_sender_jabber_id) > 0

    def is_disconnect_pending(self):
        return self.disconnect_jabber_id

    def is_register_message_handler_pending(self):
        return self.register_message_handler_jabber_id

    def run_loop(self):
        while self.loop:
            if self.is_connect_pending():
                self.connect(self.connect_jabber_id, self.connect_password)
                self.clear_connect_parameters()
                self.event_semaphore.release()
            if self.is_register_message_handler_pending():
                self.register_message_handler(self.register_message_handler_jabber_id, self.register_message_handler_handler)
                self.clear_register_message_handler_parameters()
                self.event_semaphore.release()
            if self.is_disconnect_pending():
                self.disconnect(self.disconnect_jabber_id)
                self.clear_disconnect_parameters()
                self.event_semaphore.release()
            if self.is_send_pending():
                sender_jabber_id = self.send_sender_jabber_id[0]
                receiver_jabber_id = self.send_receiver_jabber_id[0]
                message = self.send_message[0]
                self.send(sender_jabber_id, receiver_jabber_id, message)
                self.clear_send_parameters()
            for jabber_id in self.clients:
                self.clients[jabber_id].Process(1)

    def get_jabber_id(self, username, password, hostname, resource):
        jabber_id = username + "@" + hostname
        if (not resource == None and not resource == ""):
            jabber_id += "/" + resource
        return jabber_id

    def connect(self, jabber_id, password):
        if not jabber_id in self.clients:
            jid = xmpp.protocol.JID(jabber_id)
            client = xmpp.Client(jid.getDomain(), debug = [])
            connection = client.connect()
            if connection:
                authentication = client.auth(jid.getNode(), password, resource = jid.getResource())
                if authentication:
                    if not jabber_id in self.message_handlers:
                        self.message_handlers[jabber_id] = MessageHandler()
                    client.RegisterHandler('message', self.message_handlers[jabber_id].handle_incoming_message)
                    client.sendInitPresence()
                    self.clients[jabber_id] = client
                    return True
        return False

    def disconnect(self, jabber_id):
        if jabber_id in self.clients:
            self.clients[jabber_id].disconnect()
            del self.clients[jabber_id]
            del self.message_handlers[jabber_id]

    def send(self, sender_jabber_id, receiver_jabber_id, message):
        if sender_jabber_id in self.clients:
            client = self.clients[sender_jabber_id]
            client.send(xmpp.protocol.Message(receiver_jabber_id, message))

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_jabber_connect(self, args, output_method):
        if len(args) >= 2:
            jabber_id = args[0]
            password = args[1]
            self.parent_plugin.connect(jabber_id, password)
        else:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)

    def process_jabber_send(self, args, output_method):
        if len(args) >= 3:
            sender_jabber_id = args[0]
            receiver_jabber_id = args[1]
            message = args[2]
            self.parent_plugin.send(sender_jabber_id, receiver_jabber_id, message)
        else:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)

    def process_jabber_disconnect(self, args, output_method):
        if len(args) >= 1:
            jabber_id = args[0]
            self.parent_plugin.disconnect(jabber_id)
        else:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)

    def process_jabber_list_clients(self, args, output_method):
        output_method("List of connected jabber clients:")
        for jabber_id in self.clients:
            output_method("* " + jabber_id)

class MessageHandler:

    handler = None

    def handle_incoming_message(self, connection, event):
        type = event.getType()
        sender_id = event.getFrom().getStripped()
        body = event.getBody()
        print "message received from %s: %s" % (sender_id, body)
        if self.handler:
            self.handler(sender_id, body)
        else:
            print "message received from %s: %s" % (sender_id, body)

    def register_message_handler(self, handler):
        print "Registering message handler"
        self.handler = handler
