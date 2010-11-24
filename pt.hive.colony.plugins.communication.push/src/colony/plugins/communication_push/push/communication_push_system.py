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
import threading

COMMUNICATION_NAMES_VALUE = "communication_names"
""" The communication names value """

COMMUNICATION_PROFILE_NAMES_VALUE = "communication_profile_names"
""" The communication profile names value """

COMMUNICATION_HANDLER_COUNT_VALUE = "communication_handler_count"
""" The communication handler count value """

COMMUNICATION_HANDLER_NAMES_VALUE = "communication_handler_names"
""" The communication handler names value """

COMMUNICATION_HANDLER_TUPLES_VALUE = "communication_handler_tuples"
""" The communication handler tuples value """

PROPERTIES_VALUE = "properties"
""" The properties value """

NUMBER_THREADS = 3
""" The number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

MAXIMUM_NUMBER_THREADS = 5
""" The maximum number of threads """

MAXIMUM_NUMBER_WORKER_THREADS = 5
""" The maximum number of workers per thread """

WORK_SCHEDULING_ALGORITHM = 1
""" The work scheduling algorithm """

MAXIMUM_NOTIFICATION_BUFFER_SIZE = 50
""" The maximum size of the notification buffer """

INITIAL_SEQUENCE_ID = 0
""" The initial sequence id """

PUSH_SERVICE_NOTIFICATION_TOKEN = "%{PUSH}%"
""" The push service notification token """

REMOVED_VALUE = "REMOVED"
""" The removed value """

class CommunicationPush:
    """
    The communication push plugin.
    """

    communication_push_plugin = None
    """ The communication push plugin """

    communication_push_persistence_plugins_map = {}
    """ The communication push persistence plugins map """

    communication_name_push_notifications_map = {}
    """ The map associating a communication with the list of push notifications (notification buffer) """

    communication_name_communication_handlers_map = {}
    """ The map associating a communication with a list of communication handlers """

    communication_handler_communication_names_map = {}
    """ The map associating a communication handler with the communication names it handles """

    communication_handler_name_communication_handler_method_map = {}
    """ The map associating a communication handler and name tuple with the communication handler method """

    communication_handler_name_properties_map = {}
    """ The map associating a communication handler name with the map of properties """

    communication_profile_name_communication_handler_tuples_map = {}
    """ The map associating a communication profile name with the communication handler tuples """

    communication_profile_name_communication_names_map = {}
    """ The map associating a communication profile name with the communication names """

    communication_handler_profile_communication_handler_method = {}
    """ The map associating a communication handler and profile tuple with the communication handler method """

    communication_name_sequence_id_map = {}
    """ The map associating a commmunication with the current sequence id """

    process_notification_lock = None
    """ The lock to control the access to the process notification method """

    work_pool = None
    """ The work pool associated with the processing of the push notifications """

    def __init__(self, communication_push_plugin):
        """
        Constructor of the class.

        @type communication_push_plugin: CommunicationPushPlugin
        @param communication_push_plugin: The communication push plugin.
        """

        self.communication_push_plugin = communication_push_plugin

        self.communication_push_persistence_plugins_map = {}
        self.communication_name_push_notifications_map = {}
        self.communication_name_communication_handlers_map = {}
        self.communication_handler_communication_names_map = {}
        self.communication_handler_name_communication_handler_method_map = {}
        self.communication_handler_name_properties_map = {}
        self.communication_profile_name_communication_handler_tuples_map = {}
        self.communication_profile_name_communication_names_map = {}
        self.communication_handler_communication_profile_names_map = {}
        self.communication_handler_profile_communication_handler_method = {}
        self.communication_name_sequence_id_map = {}

        self.process_notification_lock = threading.RLock()

    def start_pool(self):
        """
        Starts the work pool.
        """

        # retrieves the work pool manager pool
        work_pool_manager_plugin = self.communication_push_plugin.work_pool_manager_plugin

        # creates the work pool
        self.work_pool = work_pool_manager_plugin.create_new_work_pool("communication push system pool", "communication push system work pool", CommunicationPushProcessingTask, [self, self.communication_push_plugin], NUMBER_THREADS, SCHEDULING_ALGORITHM, MAXIMUM_NUMBER_THREADS, MAXIMUM_NUMBER_WORKER_THREADS, WORK_SCHEDULING_ALGORITHM)

        # starts the pool
        self.work_pool.start_pool()

    def stop_pool(self):
        """
        Stops the work pool.
        """

        # stops the pool tasks
        self.work_pool.stop_pool_tasks()

        # stops the pool
        self.work_pool.stop_pool()

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
        if not communication_handler_name in self.communication_handler_communication_names_map:
            # sets the value of the communication handler name in the communication handler
            # communication names map to a new empty list
            self.communication_handler_communication_names_map[communication_handler_name] = []

        # retrieves the communication names list for the communication handler name
        communication_names_list = self.communication_handler_communication_names_map[communication_handler_name]

        # adds the communication name to the communication names list
        communication_names_list.append(communication_name)

        # creates the communication handler name tuple with the communication name
        # and the communication handler name
        communication_handler_name_tuple = (communication_name, communication_handler_name)

        # sets the communication handler name tuple for the communication handler method
        # in the communication handler name communication handler method map
        self.communication_handler_name_communication_handler_method_map[communication_handler_name_tuple] = communication_handler_method

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

        # sends the removed service notificaiton to communication handler
        self._send_service_notification(REMOVED_VALUE, [communication_name], communication_name, communication_handler_method)

        # creates the communication handler tuple with the handler name
        # and the handler method
        communication_handler_tuple = (communication_handler_name, communication_handler_method)

        # retrieves the communication handlers list for the communication name
        communication_handlers_list = self.communication_name_communication_handlers_map[communication_name]

        # removes the communication handler tuple from the communication handlers list
        communication_handlers_list.remove(communication_handler_tuple)

        # retrieves the communication names list for the communication handler name
        communication_names_list = self.communication_handler_communication_names_map[communication_handler_name]

        # removes the communication name from the communication names list
        communication_names_list.remove(communication_name)

        # in case the communication names list is empty (no more communication names associated)
        if not communication_names_list:
            # removes the communication handler name from the communication handler communication names map
            del self.communication_handler_communication_names_map[communication_handler_name]

        # creates the communication handler name tuple with the communication name
        # and the communication handler name
        communication_handler_name_tuple = (communication_name, communication_handler_name)

        # removes the communication handler name tuple for the communication handler method
        # in the communication handler name communication handler method map
        del self.communication_handler_name_communication_handler_method_map[communication_handler_name_tuple]

    def remove_all_communication_handler(self, communication_handler_name):
        """
        Removes the communication handler from all the communication "channels".
        It also removes the extra meta information associated with the
        communication handler.

        @type communication_handler_name: String
        @param communication_handler_name: The name of the handler to have the
        communications removed.
        """

        # retrieves the communication names list for the communication handler name
        communication_names_list = self.communication_handler_communication_names_map.get(communication_handler_name, [])

        # creates a copy of the communication names list, in order to avoid
        # possible list corruption during iteration
        communication_names_list_copy = copy.copy(communication_names_list)

        # iterates over all the communication names
        for communication_name in communication_names_list_copy:
            # creates the communication handler name tuple with the communication name
            # and the communication handler name
            communication_handler_name_tuple = (communication_name, communication_handler_name)

            # retrieves the communication handler method for the communication handler name tuple
            communication_handler_method = self.communication_handler_name_communication_handler_method_map[communication_handler_name_tuple]

            # removes the communication handler for the communication name, communication handler name
            # and communication handler method
            self.remove_communication_handler(communication_name, communication_handler_name, communication_handler_method)

        # in case the communication handler name exists in the communication handler
        # name properties map
        if communication_handler_name in self.communication_handler_name_properties_map:
            # removes the communication handler name from the communication handler name
            # properties map
            del self.communication_handler_name_properties_map[communication_handler_name]

    def send_broadcast_notification(self, communication_name, push_notification):
        """
        Sends a broadcast notification to all the communication handler activated.

        @type communication_name: String
        @param communication_name: The name of the communication "channel" to be used.
        @type push_notification: PushNotification
        @param push_notification: The push notification to be broadcasted.
        """

        # processes the notification, updating some of its values
        self._process_notification(push_notification, communication_name)

        # inserts the notification in the notification buffer
        self.insert_notification_buffer(communication_name, push_notification)

        # in case the communication name is not defined in the communication name
        # communication handlers map, there is no need to continue
        if not communication_name in self.communication_name_communication_handlers_map:
            # returns immediately
            return

        # retrieves the communication handlers list for the communication name
        communication_handlers_list = self.communication_name_communication_handlers_map[communication_name]

        # iterates over all the communication handlers
        for communication_handler in communication_handlers_list:
            # retrieves the communication handler name and method, unpacking
            # the communication handler tuple
            _communication_handler_name, communication_handler_method = communication_handler

            # creates a new push notification work
            push_notification_work = PushNotificationWork(push_notification, communication_name, communication_handler_method)

            # inserts a push notification work into the work pool (in order to be processed)
            self.work_pool.insert_work(push_notification_work)

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

        # creates the communication handler names list
        communication_handler_names_list = []

        # retrieves the communication handlers list from the communication name communication handlers map
        communication_handlers_list = self.communication_name_communication_handlers_map.get(communication_handler_name, [])

        # iterates over all the communication handler in the communication
        # handlers list
        for communication_handler in communication_handlers_list:
            # retrieves the communication handler name and method, unpacking
            # the communication handler tuple
            communication_handler_name, _communication_handler_method = communication_handler

            # adds the communication handler name to the list of communication handler names
            communication_handler_names_list.append(communication_handler_name)

        # retrieves the communication handler names list length
        communication_handler_names_list_length = len(communication_handler_names_list)

        # creates the communication information
        communication_information = {COMMUNICATION_HANDLER_COUNT_VALUE : communication_handler_names_list_length,
                                     COMMUNICATION_HANDLER_NAMES_VALUE : communication_handler_names_list}

        # returns the communication information
        return communication_information

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

        # retrieves the communication names list for the communication handler name
        communication_names_list = self.communication_handler_communication_names_map.get(communication_handler_name, [])

        # retrieves the communication profile names list for the communication handler name
        communication_profile_names_list = self.communication_handler_communication_profile_names_map.get(communication_handler_name, [])

        # retrieves the properties map for the communication handler
        properties_map = self._get_communication_handler_properties(communication_handler_name)

        # creates the communication handler information
        communication_handler_information = {COMMUNICATION_NAMES_VALUE : communication_names_list,
                                             COMMUNICATION_PROFILE_NAMES_VALUE : communication_profile_names_list,
                                             PROPERTIES_VALUE : properties_map}

        # returns the communication handler information
        return communication_handler_information

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

        # retrieves the communication names list for the communication profile name
        communication_names_list = self.communication_profile_name_communication_names_map.get(communication_profile_name, [])

        # retrieves the communication handler tuples list for the communication profile name
        communication_handler_tuples_list = self.communication_profile_name_communication_handler_tuples_map.get(communication_profile_name, [])

        # retrieves the communication handler tuples list length
        communication_handler_tuples_list_length = len(communication_handler_tuples_list)

        # creates the communication profile information
        communication_profile_information = {COMMUNICATION_NAMES_VALUE : communication_names_list,
                                             COMMUNICATION_HANDLER_COUNT_VALUE : communication_handler_tuples_list_length,
                                             COMMUNICATION_HANDLER_TUPLES_VALUE : communication_handler_tuples_list}

        # returns the communication profile information
        return communication_profile_information

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

        # in case the communication handler name is not defined in the communication
        # handler name properties map
        if not communication_handler_name in self.communication_handler_name_properties_map:
            # returns none (invalid)
            return None

        # retrieves the properties map for the communication handler name
        properties_map = self.communication_handler_name_properties_map[communication_handler_name]

        # tries to retrieve the property value from the properties map
        property_value = properties_map.get(property_name, None)

        # returns the property value
        return property_value

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

        # in case the communication handler name is not defined in the communication
        # handler name properties map
        if not communication_handler_name in self.communication_handler_name_properties_map:
            # creates the properties map for the communication handler name
            self.communication_handler_name_properties_map[communication_handler_name] = {}

        # retrieves the properties map for the communication handler name
        properties_map = self.communication_handler_name_properties_map[communication_handler_name]

        # set the property value in the properties map
        properties_map[property_name] = property_value

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

        # creates the communication handler tuple
        communication_handler_tuple = (communication_handler_name, communication_handler_method)

        # creates the communication handler profile tuple
        communication_handler_profile_tuple = (communication_handler_name, communication_profile_name)

        # in case the communication profile name is not defined in the communication
        # profile name communication handler tuples map
        if not communication_profile_name in self.communication_profile_name_communication_handler_tuples_map:
            # creates the list for the communication profile name
            self.communication_profile_name_communication_handler_tuples_map[communication_profile_name] = []

        # retrieves the communication handler tuples list
        communication_handler_tuples_list = self.communication_profile_name_communication_handler_tuples_map[communication_profile_name]

        # adds the communication handler tuple to the communication handler names list
        communication_handler_tuples_list.append(communication_handler_tuple)

        # in case the communication handler name is not defined in the communication handler communication
        # profile names map
        if not communication_handler_name in self.communication_handler_communication_profile_names_map:
            # creates the list for the communication handler
            self.communication_handler_communication_profile_names_map[communication_handler_name] = []

        # retrieves the communication profile names list
        communication_profile_names_list = self.communication_handler_communication_profile_names_map[communication_handler_name]

        # adds the communication profile name to the communication profile names list
        communication_profile_names_list.append(communication_profile_name)

        # sets the communication handler method for the communication handler profile tuple
        self.communication_handler_name_communication_handler_method_map[communication_handler_profile_tuple] = communication_handler_method

        # loads the communication profile (internal structures) in the communication handler
        self._load_communication_profile(communication_handler_name, communication_profile_name, communication_handler_method)

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

        # creates the communication handler tuple
        communication_handler_tuple = (communication_handler_name, communication_handler_method)

        # creates the communication handler profile tuple
        communication_handler_profile_tuple = (communication_handler_name, communication_profile_name)

        # retrieves the communication handler tuples list
        communication_handler_tuples_list = self.communication_profile_name_communication_handler_tuples_map[communication_profile_name]

        # removes the communication handler name from the communication handler tuples list
        communication_handler_tuples_list.remove(communication_handler_tuple)

        # retrieves the communication profile names list
        communication_profile_names_list = self.communication_handler_communication_profile_names_map[communication_handler_name]

        # removes the communication profile name from the communication profile names list
        communication_profile_names_list.remove(communication_profile_name)

        # removes the communication handler profile tuple from the communication
        # handler name communication handler method map
        del self.communication_handler_name_communication_handler_method_map[communication_handler_profile_tuple]

        # unloads the communication profile (internal structures) from communication handler
        self._unload_communication_profile(communication_handler_name, communication_profile_name, communication_handler_method)

    def unload_all_communication_profile(self, communication_handler_name):
        """
        Removes the communication handler from all the communication profiles.

        @type communication_handler_name: String
        @param communication_handler_name: The name of the handler to have the
        communication profiles removed.
        """

        # retrieves the communication profile names list for the communication handler name
        communication_profile_names_list = self.communication_handler_communication_profile_names_map.get(communication_handler_name, [])

        # iterates over all the communication profile names list
        for communication_profile_name in communication_profile_names_list:
            # creates the communication handler profile tuple
            communication_handler_profile_tuple = (communication_handler_name, communication_profile_name)

            # retrieves the communication handler method fo the communication handler profile tuple
            communication_handler_method = self.communication_handler_name_communication_handler_method_map[communication_handler_profile_tuple]

            # unloads the communication profile for the handler name, profile name and handler method
            self.unload_communication_profile(communication_handler_name, communication_profile_name, communication_handler_method)

    def set_communication_profile(self, communication_profile_name, communication_name):
        """
        Sets (adds) a communication to the given communication profile.

        @type communication_profile_name: String
        @param communication_profile_name: The name of the communication profile
        to add the communication.
        @type communication_name: String
        @param communication_name: The name of the communication to be added.
        """

        # in case the communication profile name is not defined in the communication
        # profile name communication names map
        if not communication_profile_name in self.communication_profile_name_communication_names_map:
            # creates the list for the communication profile name
            self.communication_profile_name_communication_names_map[communication_profile_name] = []

        # retrieves the communication names list
        communication_names_list = self.communication_profile_name_communication_names_map[communication_profile_name]

        # adds the communication name to the communication names list
        communication_names_list.append(communication_name)

        # registers the new communication name in the communication profile
        self._register_communication_profile(communication_profile_name, communication_name)

    def unset_communication_profile(self, communication_profile_name, communication_name):
        """
        Unsets (removes) a communication from the given communication profile.

        @type communication_profile_name: String
        @param communication_profile_name: The name of the communication profile
        to remove the communication.
        @type communication_name: String
        @param communication_name: The name of the communication to be removed.
        """

        # retrieves the communication names list
        communication_names_list = self.communication_profile_name_communication_names_map[communication_profile_name]

        # removes the communication name from the communication names list
        communication_names_list.remove(communication_name)

        # unregisters the new communication name in the communication profile
        self._unregister_communication_profile(communication_profile_name, communication_name)

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

        # in case the communication name is not defined in the communication name
        # push notifications map
        if not communication_name in self.communication_name_push_notifications_map:
            # creates a list for the communication name in the communication
            # name push notifications map
            self.communication_name_push_notifications_map[communication_name] = []

        # retrieves the push notifications list from the communication name push
        # notifications map
        push_notifications_list = self.communication_name_push_notifications_map[communication_name]

        # adds (to the front) the push notification to the push notifications list
        push_notifications_list.insert(0, push_notification)

        # retrieves the push notifications list length
        push_notifications_list_length = len(push_notifications_list)

        # in case the maximum size of the push notifications list
        # is reached (overflow)
        if push_notifications_list_length > MAXIMUM_NOTIFICATION_BUFFER_SIZE:
            # pops the last (oldest) element
            push_notifications_list.pop()

    def get_notifications_buffer(self, communication_name, count = None):
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

        # retrieves the push notifications list from the communication name push
        # notifications map
        push_notifications_list = self.communication_name_push_notifications_map.get(communication_name, [])

        # retrieves the push notifications list length
        push_notifications_list_length = len(push_notifications_list)

        # sets the count value
        count = count or push_notifications_list_length

        # retrieves the sub set of required push notifications
        required_push_notifications_list = push_notifications_list[:count]

        # returns the sub set of required push notifications
        return required_push_notifications_list

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

        # retrieves the push notifications list from the communication name push
        # notifications map
        push_notifications_list = self.communication_name_push_notifications_map.get(communication_name, [])

        # starts the index value
        index = 0

        # iterates over all the push notification in the
        # push notifications list
        for push_notification in push_notifications_list:
            # retrieves the current guid
            current_guid = push_notification.get_guid()

            # in case the target guid is found
            if current_guid == guid:
                # breaks the cycle
                break

            # increments the index value
            index += 1

        # retrieves the sub set of required push notifications
        required_push_notifications_list = push_notifications_list[:index]

        # returns the sub set of required push notifications
        return required_push_notifications_list

    def clear_notifications_buffer(self, communication_name):
        """
        Clears the notifications notification buffer for the given
        communication name.

        @type communication_name: String
        @param communication_name: The communication name of the
        notification buffer to cleared.
        """

        # creates a new list for the communication name in the communication
        # name push notifications map
        self.communication_name_push_notifications_map[communication_name] = []

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

    def print_diagnostics(self):
        """
        Prints diagnostic information about the plugin instance.
        """

        print "communication_name_push_notifications_map: " + str(self.communication_name_push_notifications_map)
        print "communication_name_communication_handlers_map:" + str(self.communication_name_communication_handlers_map)
        print "communication_handler_communication_names_map:" + str(self.communication_handler_communication_names_map)
        print "communication_handler_name_communication_handler_method_map:" + str(self.communication_handler_name_communication_handler_method_map)
        print "communication_handler_name_properties_map:" + str(self.communication_handler_name_properties_map)
        print "communication_profile_name_communication_handler_tuples_map:" + str(self.communication_profile_name_communication_handler_tuples_map)
        print "communication_profile_name_communication_names_map:" + str(self.communication_profile_name_communication_names_map)
        print "communication_handler_profile_communication_handler_method:" + str(self.communication_handler_profile_communication_handler_method)

    def communication_push_persistence_load(self, communication_push_persistence_plugin):
        # retrieves the plugin persistence name
        persistence_name = communication_push_persistence_plugin.get_persistence_name()

        self.communication_push_persistence_plugins_map[persistence_name] = communication_push_persistence_plugin

    def communication_push_persistence_unload(self, communication_push_persistence_plugin):
        # retrieves the plugin persistence name
        persistence_name = communication_push_persistence_plugin.get_persistence_name()

        del self.communication_push_persistence_plugins_map[persistence_name]

    def _get_communication_handler_properties(self, communication_handler_name):
        """
        Retrieves a map containing the communication handler properties
        for the given communication handler name.

        @type communication_handler_name: String
        @param communication_handler_name: The name of the communication
        handler to retrieve the map of properties.
        @rtype: Dictionary
        @return: The map containing the properties of the communication
        handler.
        """

        return self.communication_handler_name_properties_map.get(communication_handler_name, {})

    def _load_communication_profile(self, communication_handler_name, communication_profile_name, communication_handler_method):
        # retrieves the communication names list
        communication_names_list = self.communication_profile_name_communication_names_map.get(communication_profile_name, [])

        # iterates over all the communication names to
        # add the communication handler to the communication name
        for communication_name in communication_names_list:
            # adds the communication handler to the communication name
            self.add_communication_handler(communication_name, communication_handler_name, communication_handler_method)

    def _unload_communication_profile(self, communication_handler_name, communication_profile_name, communication_handler_method):
        # retrieves the communication names list
        communication_names_list = self.communication_profile_name_communication_names_map.get(communication_profile_name, [])

        # iterates over all the communication names to remove
        # the communication handler from the communication name
        for communication_name in communication_names_list:
            try:
                # removes the communication handler from the communication name
                self.remove_communication_handler(communication_name, communication_handler_name, communication_handler_method)
            except Exception, exception:
                # prints an information message about the exception
                self.communication_push_plugin.info("Unable to remove communication '%s' for handler '%s', probably due to double removal (%s)" % (communication_name , communication_handler_name, unicode(exception)))

    def _register_communication_profile(self, communication_profile_name, communication_name):
        # retrieves the communication handler tuples list
        communication_handler_tuples_list = self.communication_profile_name_communication_handler_tuples_map.get(communication_profile_name, [])

        # iterates over all the communication handler tuples to add the communication
        # handlers for the communication name
        for communication_handler_tuple in communication_handler_tuples_list:
            # retrieves the communication handler name and method from the communication handler tuple
            communication_handler_name, communication_handler_method = communication_handler_tuple

            # adds the communication handler to the communication name
            self.add_communication_handler(communication_name, communication_handler_name, communication_handler_method)

    def _unregister_communication_profile(self, communication_profile_name, communication_name):
        # retrieves the communication handler tuples list
        communication_handler_tuples_list = self.communication_profile_name_communication_handler_tuples_map.get(communication_profile_name, [])

        # iterates over all the communication handler tuples to remove the communication
        # handlers for the communication name
        for communication_handler_tuple in communication_handler_tuples_list:
            # retrieves the communication handler name and method from the communication handler tuple
            communication_handler_name, communication_handler_method = communication_handler_tuple

            # removes the communication handler from the communication name
            self.remove_communication_handler(communication_name, communication_handler_name, communication_handler_method)

    def _send_notification(self, notification_message, communication_name, communication_handler_method, allow_failure = True):
        """
        Sends the given notification message using the given communication handler method
        and for the given communication name.
        The allow failire flag controls the tolerance to the failure.

        @type notification_message: String
        @param notification_message: The notification message to be sent.
        @type communication_name: String
        @param communication_name: The name of the communication to be used.
        @type communication_handler_method: Method
        @param communication_handler_method: The communication handler method to be used.
        @type allow_failure: bool
        @param allow_failure: The tolerance to failure.
        """

        # creates a new push notificaiton for the notification message
        push_notification = PushNotification(notification_message)

        try:
            # calls the communication handler method
            communication_handler_method(push_notification, communication_name)
        except Exception, exception:
            # in case no failure is tolerated
            if not allow_failure:
                # prints an information message about the exception
                self.communication_push_plugin.debug("Problem sending notification: %s" % unicode(exception))

    def _send_service_notification(self, command, arguments, communication_name, communication_handler_method):
        """
        Sends a service notification using the given communication handler method
        and for the given communication name.

        @type command: String
        @param command: The command to be sent.
        @type arguments: List
        @param arguments: The list of arguments for the command.
        @type communication_name: String
        @param communication_name: The name of the communication to be used.
        @type communication_handler_method: Method
        @param communication_handler_method: The communication handler method to be used.
        """

        # serializes the arguments
        arguments_serialized = " ".join([str(argument) for argument in arguments])

        # creates the notification message appending the push notification token with the command
        # and the arguments serialized
        notification_message = PUSH_SERVICE_NOTIFICATION_TOKEN + " " + command + " " + arguments_serialized

        # sends the notification to the communication name (on failure no verbosity)
        self._send_notification(notification_message, communication_name, communication_handler_method)

    def _process_notification(self, push_notification, communication_name):
        """
        Processes the given notification.

        @type communication_name: String
        @param communication_name: The name of the communication.
        @type push_notification: PushNotification
        @param push_notification: The push notification to be processed.
        """

        # acquires the process notification lock
        self.process_notification_lock.acquire()

        # retrieves the plugin manager
        plugin_manager = self.communication_push_plugin.manager

        # retrieves the guid plugin
        guid_plugin = self.communication_push_plugin.guid_plugin

        # generates a new guid for the push notification
        generated_guid = guid_plugin.generate_guid()

        # retrieves the plugin manager uid
        plugin_manager_uid = plugin_manager.uid

        # creates the composite guid as the concatenation of the plugin
        # manager guid and the generated guid
        composite_guid = plugin_manager_uid + "-" + generated_guid

        # retrieves the sequence id for the communication name
        sequence_id = self._get_sequence_id_communication_name(communication_name)

        # sets the composite guid in the push notification
        push_notification.set_guid(composite_guid)

        # sets the sequence id in the push notification
        push_notification.set_sequence_id(sequence_id)

        # releases the process notification lock
        self.process_notification_lock.release()

    def _get_sequence_id_communication_name(self, communication_name):
        """
        Retrieves the next sequence id for the
        communication with the given name.

        @type communication_name: String
        @param communication_name: The name of the communication
        to retrieve the sequence id.
        @rtype: int
        @return: The sequence id for the given communication name.
        """

        # retrieves the sequence id for the communication name
        sequence_id = self.communication_name_sequence_id_map.get(communication_name, 0)

        # sets the increments sequence id in the communication name sequence id map
        self.communication_name_sequence_id_map[communication_name] = sequence_id + 1

        # returns the sequence id
        return sequence_id

class CommunicationPushProcessingTask:
    """
    The communication push processing task.
    """

    communication_push = None
    """ The communication push """

    communication_push_plugin = None
    """ The communication push plugin """

    work_list = []
    """ The list of work to do """

    def __init__(self, communication_push, communication_push_plugin):
        """
        Constructor of the class.

        @type communication_push: CommunicationPush
        @param communication_push: The communication push.
        @type communication_push_plugin: CommunicationPushPlugin
        @param communication_push_plugin: The communication push plugin.
        """

        self.communication_push = communication_push
        self.communication_push_plugin = communication_push_plugin

        self.work_list = []

    def start(self):
        """
        Starts the communication push
        processing task.
        """

        pass

    def stop(self):
        """
        Stops the communication push
        processing task.
        """

        pass

    def process(self):
        """
        Processes an iteration of the communication push processing task.
        """

        # iterates over all the work in the
        # work list
        for work in self.work_list:
            try:
                # retrieves the push notification from the work
                push_notification = work.get_push_notification()

                # retrieves the communication name from the work
                communication_name = work.get_communication_name()

                # retrieves the communication handler method from the work
                communication_handler_method = work.get_communication_handler_method()

                # calls the communication handler method with
                # the push notification and the communication name
                communication_handler_method(push_notification, communication_name)
            except Exception, exception:
                # prints an information message
                self.communication_push_plugin.info("Problem calling the communication handler method for push notification: %s" % unicode(exception))

                # removes the work
                self.remove_work(work)
            else:
                # removes the work
                self.remove_work(work)

    def wake(self):
        """
        "Wakes" the communication push
        processing task.
        """

        pass

    def busy(self):
        """
        Retrieves the current busy status.

        @rtype: bool
        @return: The current busy status.
        """

        return False

    def work_added(self, work_reference):
        """
        Adds a work to the work list.

        @type work_reference: Object
        @param work_reference: The work to be added
        to the work list.
        """

        self.work_list.append(work_reference)

    def work_removed(self, work_reference):
        """
        Removes a work from the work list.

        @type work_reference: Object
        @param work_reference: The work to be removed
        from the work list.
        """

        self.work_list.remove(work_reference)

class PushNotification:
    """
    The push notification class.
    Represents a simple push notification.
    """

    message = None
    """ The message for the push notification """

    sender_id = None
    """ The identification of the sender """

    guid = None
    """ The global unique identifier """

    sequence_id = None
    """ The sequence id associated """

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
        Sets the sender id.

        @type sender_id: String
        @param sender_id: The sender id.
        """

        self.sender_id = sender_id

    def get_guid(self):
        """
        Retrieves the guid.

        @rtype: String
        @return: The guid.
        """

        return self.guid

    def set_guid(self, guid):
        """
        Sets the guid.

        @type guid: String
        @param guid: The guid.
        """

        self.guid = guid

    def get_sequence_id(self):
        """
        Retrieves the sequence id.

        @rtype: int
        @return: The sequence id.
        """

        return self.sequence_id

    def set_sequence_id(self, sequence_id):
        """
        Sets the sequence id.

        @type sequence_id: int
        @param sequence_id: The sequence id.
        """

        self.sequence_id = sequence_id

class PushNotificationWork:
    """
    The push notification work class.
    """

    push_notification = None
    """ The push notification associated with the work """

    communication_name = None
    """ The name of the communication used to send push notification """

    communication_handler_method = None
    """ The communication handler method """

    def __init__(self, push_notification, communication_name, communication_handler_method):
        """
        Constructor of the class.

        @type push_notification: PushNotification
        @param push_notification: The push notification associated
        with the work.
        @type communication_name: String
        @param communication_name: The name of the communication used to
        send push notification.
        @type communication_handler_method: Method
        @param communication_handler_method: The communication handler method.
        """

        self.push_notification = push_notification
        self.communication_name = communication_name
        self.communication_handler_method = communication_handler_method

    def get_push_notification(self):
        """
        Retrieves the push notification.

        @rtype: PushNotification
        @return: The push notification.
        """

        return self.push_notification

    def set_push_notification(self, push_notification):
        """
        Sets the push notification.

        @type push_notification: PushNotification
        @param push_notification: The push notification.
        """

        self.push_notification = push_notification

    def get_communication_name(self):
        """
        Retrieves the push notification.

        @rtype: String
        @return: The communication name.
        """

        return self.communication_name

    def set_communication_name(self, communication_name):
        """
        Sets the push notification.

        @type communication_name: String
        @param communication_name: The communication name.
        """

        self.communication_name = communication_name

    def get_communication_handler_method(self):
        """
        Retrieves the communication handler method.

        @rtype: Method
        @return: The communication handler method.
        """

        return self.communication_handler_method

    def set_communication_handler_method(self, communication_handler_method):
        """
        Sets the communication handler method.

        @type communication_handler_method: Method
        @param communication_handler_method: The communication
        handler method.
        """

        self.communication_handler_method = communication_handler_method
