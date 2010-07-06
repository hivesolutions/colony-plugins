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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 5731 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-10-21 19:04:42 +0100 (qua, 21 Out 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import copy

class CommunicationPush:
    """
    The communication push plugin.
    """

    comnunication_push_plugin = None
    """ The communication push plugin """

    communication_name_communication_handlers_map = {}
    """ The map associating a communication with a list of communication handlers """

    communication_handler_communication_names = {}
    """ The map associating a communication handler with the communication names it handles """

    communication_handler_name_communication_handler_method = {}
    """ The map associating a communication handler and name tuple with the communication handler method """

    communication_handler_name_push_notifications = {}
    """ The map associating the communication handler name with the list of pending push notifications """

    def __init__(self, comnunication_push_plugin):
        """
        Constructor of the class.

        @type comnunication_push_plugin: CommunicationPushPlugin
        @param comnunication_push_plugin: The communication push plugin.
        """

        self.comnunication_push_plugin = comnunication_push_plugin

        self.communication_name_communication_handlers_map = {}
        self.communication_handler_communication_names = {}
        self.communication_handler_name_communication_handler_method = {}
        self.communication_handler_name_push_notifications = {}

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

        # creates the communication handler tuple with the handler name
        # and the handler method
        communication_handler_tuple = (communication_handler_name, communication_handler_method)

        # in case the communication name is not defined in the communication name
        # communication handlers map
        if not communication_name in self.communication_name_communication_handlers_map:
            # sets the value of the communication name in the communication name communication
            # handlers map to a new empty list
            self.communication_name_communication_handlers_map[communication_name] = []

        # retrieves the communication handlers list for the communication name
        communication_handlers_list = self.communication_name_communication_handlers_map[communication_name]

        # adds the communication handler tuple to the communication handlers list
        communication_handlers_list.append(communication_handler_tuple)

        # in case the communication handler name is not defined in the communication handler
        # communication names map
        if not communication_handler_name in self.communication_handler_communication_names:
            # sets the value of the communication handler name in the communication handler
            # communication names map to a new empty list
            self.communication_handler_communication_names[communication_handler_name] = []

        # retrieves the communication names list for the communication handler name
        communication_names_list = self.communication_handler_communication_names[communication_handler_name]

        # adds the communication name to the communication names list
        communication_names_list.append(communication_name)

        # creates the communication handler name tuple with the communication name
        # and the communication handler name
        communication_handler_name_tuple = (communication_name, communication_handler_name)

        # sets the communication handler name tuple for the communication handler method
        # in the communication handler name communication handler method map
        self.communication_handler_name_communication_handler_method[communication_handler_name_tuple] = communication_handler_method

        # in case the communication handler is not defined in the communication handler name
        # push notification map
        if not communication_handler_name in self.communication_handler_name_push_notifications:
            # creates a new list to hold the push notification for the communication handler name
            self.communication_handler_name_push_notifications[communication_handler_name] = []

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

        # creates the communication handler tuple with the handler name
        # and the handler method
        communication_handler_tuple = (communication_handler_name, communication_handler_method)

        # retrieves the communication handlers list for the communication name
        communication_handlers_list = self.communication_name_communication_handlers_map[communication_name]

        # removes the communication handler tuple from the communication handlers list
        communication_handlers_list.remove(communication_handler_tuple)

        # retrieves the communication names list for the communication handler name
        communication_names_list = self.communication_handler_communication_names[communication_handler_name]

        # removes the communication name from the communication names list
        communication_names_list.remove(communication_name)

        # creates the communication handler name tuple with the communication name
        # and the communication handler name
        communication_handler_name_tuple = (communication_name, communication_handler_name)

        # removes the communication handler name tuple for the communication handler method
        # in the communication handler name communication handler method map
        del self.communication_handler_name_communication_handler_method[communication_handler_name_tuple]

    def remove_all_communication_handler(self, communication_handler_name):
        """
        Removes the communication handler from all the communication "channels".

        @type communication_handler_name: String
        @param communication_handler_name: The name of the handler to have the
        communications removed.
        """

        # retrieves the communication names list for the communication handler name
        communication_names_list = self.communication_handler_communication_names.get(communication_handler_name, [])

        # creates a copy of the communication names list, in order to avoid
        # possible list corruption during iteration
        communication_names_list_copy = copy.copy(communication_names_list)

        # iterates over all the communication names
        for communication_name in communication_names_list_copy:
            # creates the communication handler name tuple with the communication name
            # and the communication handler name
            communication_handler_name_tuple = (communication_name, communication_handler_name)

            # retrieves the communication handler method for the communication handler name tuple
            communication_handler_method = self.communication_handler_name_communication_handler_method[communication_handler_name_tuple]

            # removes the communication handler for the communication name, communication handler name
            # and communication handler method
            self.remove_communication_handler(communication_name, communication_handler_name, communication_handler_method)

    def send_broadcast_notification(self, communication_name, push_notification):
        """
        Sends a broadcast notification to all the communication handler activated.

        @type communication_name: String
        @param communication_name: The name of the communication "channel" to be used.
        @type push_notification: PushNotification
        @param push_notification: The push notification to be broadcasted.
        """

        # in case the communication name is not defined in the communication name
        # communication handlers map, there is no need to continue
        if not communication_name in self.communication_name_communication_handlers_map:
            # returns immediately
            return

        # retrieves the push notification sender id
        push_notification_sender_id = push_notification.get_sender_id()

        # retrieves the communication handlers list for the communication name
        communication_handlers_list = self.communication_name_communication_handlers_map[communication_name]

        # iterates over all the communication handlers
        for communication_handler in communication_handlers_list:
            # retrieves the communication handler name and method, unpacking
            # the communication handler tuple
            communication_handler_name, communication_handler_method = communication_handler

            # in case the communication handler is the push notification sender id
            # (no message is sent) this avoid notification of the sender
            if communication_handler_name == push_notification_sender_id:
                # passes the iteration
                continue

            # in case there is a communication handler method
            # defined use it
            if communication_handler_method:
                # calls the communication handler method, with the push notification
                communication_handler_method(push_notification)
            # otherwise puts the message into the "mail box"
            else:
                self.communication_handler_name_push_notifications[communication_handler_name].append(push_notification)

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

        # returns the generated notification
        return PushNotification(message, sender_id)

class PushNotification:
    """
    The push notification class.
    Represents a simple push notification.
    """

    message = None
    """ The message for the push notification """

    sender_id = None
    """ The identification of the sender """

    def __init__(self, message, sender_id = None):
        """
        Constructor of the class.

        @type message: String
        @param message: The message for the push notification.
        @type sender_id: String
        @param sender_id: The identification of the sender.
        """

        self.message = message
        self.sender_id = sender_id

    def get_message(self):
        """
        Retrieves the message.

        @rtype: String
        @return: The message.
        """

        return self.message

    def set_message(self, message):
        """
        Sets the message.

        @type message: String
        @param message: The message.
        """

        self.message = message

    def get_sender_id(self):
        """
        Retrieves the sender id.

        @rtype: String
        @return: The sender id.
        """

        return self.sender_id

    def set_sender_id(self, sender_id):
        """
        Sets the sender id

        @type sender_id: String
        @param sender_id: The sender id.
        """

        self.sender_id = sender_id
