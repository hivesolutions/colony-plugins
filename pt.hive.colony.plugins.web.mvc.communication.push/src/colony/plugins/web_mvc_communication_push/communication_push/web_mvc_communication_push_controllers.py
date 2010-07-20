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

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

GET_METHOD_VALUE = "GET"
""" The get method value """

COMMUNICATION_NAME_VALUE = "communication_name"
""" The communication name value """

COMMUNICATION_HANDLER_NAME_VALUE = "communication_handler_name"
""" The communication handler name value """

COMMUNICATION_PROFILE_NAME_VALUE = "communication_profile_name"
""" The communication profile name value """

MESSAGE_VALUE = "message"
""" The message value """

MESSAGE_CONTENTS_VALUE = "message_contents"
""" The message contents value """

RETURN_URL_VALUE = "return_url"
""" The return url value """

METHOD_VALUE = "method"
""" The method value """

class WebMvcCommunicationPushController:
    """
    The web mvc communication push controller.
    """

    web_mvc_communication_push_plugin = None
    """ The web mvc communication push plugin """

    web_mvc_communication_push = None
    """ The web mvc communication push """

    service_connection_name_communication_handler_map = {}
    """ The map associating the service connection name with the communication handler """

    def __init__(self, web_mvc_communication_push_plugin, web_mvc_communication_push):
        """
        Constructor of the class.

        @type web_mvc_communication_push_plugin: WebMvcCommunicationPushPlugin
        @param web_mvc_communication_push_plugin: The web mvc communication push plugin.
        @type web_mvc_communication_push: WebMvcCommunicationPush
        @param web_mvc_communication_push: The web mvc communication push.
        """

        self.web_mvc_communication_push_plugin = web_mvc_communication_push_plugin
        self.web_mvc_communication_push = web_mvc_communication_push

        self.service_connection_name_communication_handler_map = {}

    def handle_show(self, rest_request, parameters = {}):
        return True

    def handle_register(self, rest_request, parameters = {}):
        # registers for the given request
        self._register(rest_request)

        # returns true
        return True

    def handle_unregister(self, rest_request, parameters = {}):
        # unregisters for the given request
        self._unregister(rest_request)

        # returns true
        return True

    def handle_message(self, rest_request, parameters = {}):
        # sends the message for the given request
        self._message(rest_request)

        # returns true
        return True

    def handle_set_profile(self, rest_request, parameters = {}):
        # sets the profile for the given request
        self._set_profile(rest_request)

        # returns true
        return True

    def handle_unset_profile(self, rest_request, parameters = {}):
        # unsets the profile for the given request
        self._unset_profile(rest_request)

        # returns true
        return True

    def generate_handler(self, return_url, method):
        """
        Generates a communication handler for the
        given request.

        @type return_url: String
        @param return_url: The url to be used in the returning
        of the generated handler.
        @type method: String
        @param method: The http method to be used to retrieve
        the return url.
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

            # retrieves the main client http plugin
            main_client_http_plugin = self.web_mvc_communication_push_plugin.main_client_http_plugin

            # creates the http client
            http_client = main_client_http_plugin.create_client({})

            # opens the http client
            http_client.open({})

            # retrieves the notification attributes
            message = notification.get_message()
            sender_id = notification.get_sender_id()

            parameters = {COMMUNICATION_NAME_VALUE : communication_name,
                          COMMUNICATION_HANDLER_NAME_VALUE : sender_id,
                          MESSAGE_CONTENTS_VALUE : message}

            contents = http_client.fetch_url(return_url, method, parameters)

            # closes the http client
            http_client.close({})

            print contents.received_message

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
        return_url = form_data_map[RETURN_URL_VALUE]
        method = form_data_map.get(METHOD_VALUE, GET_METHOD_VALUE)

        # generates a communication handler for the given return url and method
        generated_communication_handler = self.generate_handler(return_url, method)

        # creates the service connection name tuple
        service_connection_name_tuple = (communication_handler_name, return_url, communication_name)

        # sets the generated communication handler in the service connection name communication handler map
        self.service_connection_name_communication_handler_map[service_connection_name_tuple] = generated_communication_handler

        # adds a new communication handler
        communication_push_plugin.add_communication_handler(communication_name, communication_handler_name, generated_communication_handler)

    def _unregister(self, rest_request):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        communication_handler_name = form_data_map[COMMUNICATION_HANDLER_NAME_VALUE]
        communication_name = form_data_map[COMMUNICATION_NAME_VALUE]
        return_url = form_data_map[RETURN_URL_VALUE]

        # creates the service connection name tuple
        service_connection_name_tuple = (communication_handler_name, return_url, communication_name)

        # retrieves the generated communication handler for the service connection and communication name
        generated_communication_handler = self.service_connection_name_communication_handler_map[service_connection_name_tuple]

        # removes the communication handler
        communication_push_plugin.remove_communication_handler(communication_name, communication_handler_name, generated_communication_handler)

        # removes the service connection name from the service connection name communication handler map
        del self.service_connection_name_communication_handler_map[service_connection_name_tuple]

    def _message(self, rest_request):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        communication_handler_name = form_data_map[COMMUNICATION_HANDLER_NAME_VALUE]
        communication_name = form_data_map[COMMUNICATION_NAME_VALUE]
        message = form_data_map[MESSAGE_VALUE]

        # generates the notification
        notification = communication_push_plugin.generate_notification(message, communication_handler_name)

        # sends the broadcast notification, for the communication name
        # and notification
        communication_push_plugin.send_broadcast_notification(communication_name, notification)

    def _set_profile(self, rest_request):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        communication_profile_name = form_data_map[COMMUNICATION_PROFILE_NAME_VALUE]
        communication_name = form_data_map[COMMUNICATION_NAME_VALUE]

        # sets the communication profile
        communication_push_plugin.set_communication_profile(communication_profile_name, communication_name)

    def _unset_profile(self, rest_request):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        communication_profile_name = form_data_map[COMMUNICATION_PROFILE_NAME_VALUE]
        communication_name = form_data_map[COMMUNICATION_NAME_VALUE]

        # unsets the communication profile
        communication_push_plugin.unset_communication_profile(communication_profile_name, communication_name)
