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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import apple_push_notification_service_client

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

COMMUNICATION_NAME_VALUE = "communication_name"
""" The communication name value """

COMMUNICATION_HANDLER_NAME_VALUE = "communication_handler_name"
""" The communication handler name value """

COMMUNICATION_PROFILE_NAME_VALUE = "communication_profile_name"
""" The communication profile name value """

MESSAGE_CONTENTS_VALUE = "message_contents"
""" The message contents value """

GUID_VALUE = "guid"
""" The guid value """

DEVICE_ID_VALUE = "device_id"
""" The device id value """

class WebMvcCommunicationPushAppleController:
    """
    The web mvc communication push apple controller.
    """

    web_mvc_communication_push_apple_plugin = None
    """ The web mvc communication push apple plugin """

    web_mvc_communication_push_apple = None
    """ The web mvc communication push apple """

    service_connection_name_communication_handler_map = {}
    """ The map associating the service connection name with the communication handler """

    service_connection_profile_name_communication_handler_map = {}
    """ The map associating the service connection profile name with the communication handler """

    def __init__(self, web_mvc_communication_push_apple_plugin, web_mvc_communication_push_apple):
        """
        Constructor of the class.

        @type web_mvc_communication_push_apple_plugin: WebMvcCommunicationPushApplePlugin
        @param web_mvc_communication_push_apple_plugin: The web mvc communication push apple plugin.
        @type web_mvc_communication_push_apple: WebMvcCommunicationPushApple
        @param web_mvc_communication_push_apple: The web mvc communication push apple.
        """

        self.web_mvc_communication_push_apple_plugin = web_mvc_communication_push_apple_plugin
        self.web_mvc_communication_push_apple = web_mvc_communication_push_apple

        self.service_connection_name_communication_handler_map = {}
        self.service_connection_profile_name_communication_handler_map = {}

    def handle_show(self, rest_request, parameters = {}):
        """
        Handles the given show rest request.

        @type rest_request: RestRequest
        @param rest_request: The header rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # sets the result for the rest request
        rest_request.set_result_translated(str(self.service_connection_name_communication_handler_map))

        # flushes the rest request
        rest_request.flush()

        # returns true
        return True

    def handle_register(self, rest_request, parameters = {}):
        """
        Handles the given register rest request.

        @type rest_request: RestRequest
        @param rest_request: The header rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # registers for the given request
        self._register(rest_request)

        # returns true
        return True

    def handle_unregister(self, rest_request, parameters = {}):
        """
        Handles the given unregister rest request.

        @type rest_request: RestRequest
        @param rest_request: The header rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # unregisters for the given request
        self._unregister(rest_request)

        # returns true
        return True

    def handle_load_profile(self, rest_request, parameters = {}):
        """
        Handles the given load profile rest request.

        @type rest_request: RestRequest
        @param rest_request: The header rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # loads the profile for the given request
        self._load_profile(rest_request)

        # returns true
        return True

    def handle_unload_profile(self, rest_request, parameters = {}):
        """
        Handles the given unload profile rest request.

        @type rest_request: RestRequest
        @param rest_request: The header rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # unloads the profile for the given request
        self._unload_profile(rest_request)

        # returns true
        return True

#    def generate_handler(self, return_url, method):
#        """
#        Generates a communication handler for the
#        given request.
#
#        @type return_url: String
#        @param return_url: The url to be used in the returning
#        of the generated handler.
#        @type method: String
#        @param method: The http method to be used to retrieve
#        the return url.
#        @rtype: Function
#        @return: The generated communication handler
#        """
#
#        def communication_handler(notification, communication_name):
#            """
#            The "base" communication handler function.
#            to be used in the generation of the communication handler.
#
#            @type notification: PushNotification
#            @param notification: The push notification to be sent.
#            @type communication_name: String
#            @param communication_name: The name of the communication to be used.
#            """
#
#            # retrieves the main client http plugin
#            main_client_http_plugin = self.web_mvc_communication_push_plugin.main_client_http_plugin
#
#            # creates the http client
#            http_client = main_client_http_plugin.create_client({CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET})
#
#            # opens the http client
#            http_client.open({})
#
#            # retrieves the notification attributes
#            message = notification.get_message()
#            sender_id = notification.get_sender_id()
#            guid = notification.get_guid()
#
#            # creates the parameters map
#            parameters = {COMMUNICATION_NAME_VALUE : communication_name,
#                          COMMUNICATION_HANDLER_NAME_VALUE : sender_id,
#                          GUID_VALUE : guid,
#                          MESSAGE_CONTENTS_VALUE : message}
#
#            # fetches the url, retrieving the contents
#            http_client.fetch_url(return_url, method, parameters, content_type_charset = DEFAULT_CHARSET)
#
#            # closes the http client
#            http_client.close({})
#
#        # returns the communication handler
#        return communication_handler

    def generate_handler(self, device_id):
        """
        Generates a communication handler for the
        given request.

        @type device_id: String
        @param device_id: The id of the device to be notified.
        @rtype: Function
        @return: The generated communication handler
        """

        def communication_handler(notification, communication_name):
            """
            The "base" communication handler function.
            to be used in the generation of the communication handler.

            @type notification: PushNotification
            @param notification: The push notification to be sent.
            @type communication_name: String
            @param communication_name: The name of the communication to be used.
            """

            # retrieves the json plugin
            json_plugin = self.web_mvc_communication_push_apple_plugin.json_plugin()

            # retrieves the notification attributes
            message = notification.get_message()
            sender_id = notification.get_sender_id()
            guid = notification.get_guid()

            # creates the parameters map
            parameters = {COMMUNICATION_NAME_VALUE : communication_name,
                          COMMUNICATION_HANDLER_NAME_VALUE : sender_id,
                          GUID_VALUE : guid,
                          MESSAGE_CONTENTS_VALUE : message}

            # retrieves the aps values
            alert, badge, sound = escolinhas_handler(notification)

            # creates the aps map
            aps = {"alert" : alert, "badge" : badge, "sound" : sound}

            # creates the payload map
            payload = {}

            # populates the payload map
            payload["aps"] = aps
            payload["parameters"] = parameters

            # serializes the payload into json
            payload_serialized = json_plugin.dumps(payload)

            # creates a new apple push notification service client
            _apple_push_notification_service_client = apple_push_notification_service_client.ApplePushNotificationServiceClient()

            # sends the payload
            _apple_push_notification_service_client.send_payload(device_id, payload_serialized)

            # retrieves the feedback
            _apple_push_notification_service_client.get_feedback()

        def escolinhas_handler(notification):
            # retrieves the notification message
            message = notification.get_message()

            # sets the push notification values
            alert = message
            badge = 1
            sound = "default"

            # creates the apple push notification tuple with
            # the alert the badge and the sound
            apple_push_notification_tuple = (alert, badge, sound)

            # returns the apple push notification tuple
            return apple_push_notification_tuple

        # returns the communication handler
        return communication_handler

    def _register(self, rest_request):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        communication_handler_name = form_data_map[COMMUNICATION_HANDLER_NAME_VALUE]
        communication_name = form_data_map[COMMUNICATION_NAME_VALUE]
        device_id = form_data_map[DEVICE_ID_VALUE]

        # generates a communication handler for the given device id
        generated_communication_handler = self.generate_handler(device_id)

        # creates the service connection name tuple
        service_connection_name_tuple = (communication_handler_name, device_id, communication_name)

        # sets the generated communication handler in the service connection name communication handler map
        self.service_connection_name_communication_handler_map[service_connection_name_tuple] = generated_communication_handler

        # adds a new communication handler
        communication_push_plugin.add_communication_handler(communication_name, communication_handler_name, generated_communication_handler)

    def _load_profile(self, rest_request):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        communication_handler_name = form_data_map[COMMUNICATION_HANDLER_NAME_VALUE]
        communication_profile_name = form_data_map[COMMUNICATION_PROFILE_NAME_VALUE]
        device_id = form_data_map[DEVICE_ID_VALUE]

        # generates a communication handler for the given device id
        generated_communication_handler = self.generate_handler(device_id)

        # creates the service connection profile name tuple
        service_connection_profile_name_tuple = (communication_handler_name, device_id, generated_communication_handler)

        # sets the generated communication handler in the service connection profile name communication handler map
        self.service_connection_profile_name_communication_handler_map[service_connection_profile_name_tuple] = generated_communication_handler

        # loads the communication profile
        communication_push_plugin.load_communication_profile(communication_handler_name, communication_profile_name, generated_communication_handler)

    def _unload_profile(self, rest_request):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        communication_handler_name = form_data_map[COMMUNICATION_HANDLER_NAME_VALUE]
        communication_profile_name = form_data_map[COMMUNICATION_PROFILE_NAME_VALUE]
        device_id = form_data_map[DEVICE_ID_VALUE]

        # creates the service connection profile name tuple
        service_connection_profile_name_tuple = (communication_handler_name, device_id, communication_profile_name)

        # retrieves the generated communication handler for the service connection and communication profile name
        generated_communication_handler = self.service_connection_profile_name_communication_handler_map[service_connection_profile_name_tuple]

        # unloads the communication profile
        communication_push_plugin.unload_communication_profile(communication_handler_name, communication_profile_name, generated_communication_handler)

        # removes the service connection profile name from the service connection profile name communication handler map
        del self.service_connection_profile_name_communication_handler_map[service_connection_profile_name_tuple]
