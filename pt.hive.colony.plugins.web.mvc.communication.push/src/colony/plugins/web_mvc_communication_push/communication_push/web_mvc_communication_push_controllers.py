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

import colony.libs.importer_util

import web_mvc_communication_push_exceptions

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

GET_METHOD_VALUE = "GET"
""" The get method value """

SERIALIZER_VALUE = "serializer"
""" The serializer value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

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

INFORMATION_ITEM_VALUE = "information_item"
""" The information item value """

INFORMATION_KEYS_VALUE = "information_keys"
""" The information keys value """

GUID_VALUE = "guid"
""" The guid value """

RETURN_URL_VALUE = "return_url"
""" The return url value """

METHOD_VALUE = "method"
""" The method value """

PROPERTY_NAME_VALUE = "property_name"
""" The property name value """

PROPERTY_VALUE_VALUE = "property_value"
""" The property value value """

COMMUNICATION_VALUE = "communication"
""" The communication value """

COMMUNICATION_HANDLER_VALUE = "communication_handler"
""" The communication handler value """

COMMUNICATION_PROFILE_VALUE = "communication_profile"
""" The communication profile value """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

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

    service_connection_profile_name_communication_handler_map = {}
    """ The map associating the service connection profile name with the communication handler """

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
        self.service_connection_profile_name_communication_handler_map = {}

    @web_mvc_utils.serialize_exceptions("all")
    def handle_show_serialized(self, rest_request, parameters = {}):
        """
        Handles the given show serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The show serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the string representation of the connection name handler map
        serialized_service_connection_name_communication_handler_map = serializer.dumps(self.service_connection_name_communication_handler_map)

        # sets the request contents
        self.set_contents(rest_request, serialized_service_connection_name_communication_handler_map)

    def handle_show_json(self, rest_request, parameters = {}):
        """
        Handles the given show json rest request.

        @type rest_request: RestRequest
        @param rest_request: The show json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.web_mvc_communication_push_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle show serialized method
        self.handle_show_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    def handle_register_serialized(self, rest_request, parameters = {}):
        """
        Handles the given register serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The register serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication handler name
        communication_handler_name = form_data_map[COMMUNICATION_HANDLER_NAME_VALUE]

        # retrieves the communication name
        communication_name = form_data_map[COMMUNICATION_NAME_VALUE]

        # retrieves the return url
        return_url = form_data_map[RETURN_URL_VALUE]

        # retrieves the method
        method = form_data_map.get(METHOD_VALUE, GET_METHOD_VALUE)

        # registers for the given request
        register_result = self._register(rest_request, communication_handler_name, communication_name, return_url, method)

        # serializes the register result
        serialized_register_result = serializer.dumps(register_result)

        # sets the request contents
        self.set_contents(rest_request, serialized_register_result)

    def handle_register_json(self, rest_request, parameters = {}):
        """
        Handles the given register json rest request.

        @type rest_request: RestRequest
        @param rest_request: The register json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.web_mvc_communication_push_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle register serialized method
        self.handle_register_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    def handle_unregister_serialized(self, rest_request, parameters = {}):
        """
        Handles the given unregister serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The unregister serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication handler name
        communication_handler_name = form_data_map[COMMUNICATION_HANDLER_NAME_VALUE]

        # retrieves the communication name
        communication_name = form_data_map[COMMUNICATION_NAME_VALUE]

        # retrieves the return url
        return_url = form_data_map[RETURN_URL_VALUE]

        # unregisters for the given request
        unregister_result = self._unregister(rest_request, communication_handler_name, communication_name, return_url)

        # serializes the unregister result
        serialized_unregister_result = serializer.dumps(unregister_result)

        # sets the request contents
        self.set_contents(rest_request, serialized_unregister_result)

    def handle_unregister_json(self, rest_request, parameters = {}):
        """
        Handles the given unregister json rest request.

        @type rest_request: RestRequest
        @param rest_request: The unregister json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.web_mvc_communication_push_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle unregister serialized method
        self.handle_unregister_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    def handle_message_serialized(self, rest_request, parameters = {}):
        """
        Handles the given message serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The message serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer value
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication handler name
        communication_handler_name = form_data_map[COMMUNICATION_HANDLER_NAME_VALUE]

        # retrieves the communication name
        communication_name = form_data_map[COMMUNICATION_NAME_VALUE]

        # retrieves the message
        message = form_data_map[MESSAGE_VALUE]

        # sends the message for the given request
        message_result = self._message(rest_request, communication_handler_name, communication_name, message)

        # serializes the message result
        serialized_message_result = serializer.dumps(message_result)

        # sets the request contents
        self.set_contents(rest_request, serialized_message_result)

    def handle_message_json(self, rest_request, parameters = {}):
        """
        Handles the given message json rest request.

        @type rest_request: RestRequest
        @param rest_request: The message json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.web_mvc_communication_push_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle message serialized method
        self.handle_message_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    def handle_set_property_serialized(self, rest_request, parameters = {}):
        """
        Handles the given set property serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The set property serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication handler name
        communication_handler_name = form_data_map[COMMUNICATION_HANDLER_NAME_VALUE]

        # retrieves the property name
        property_name = form_data_map[PROPERTY_NAME_VALUE]

        # retrieves the property value
        property_value = form_data_map[PROPERTY_VALUE_VALUE]

        # sets the property for the given request
        set_property_result = self._set_property(rest_request, communication_handler_name, property_name, property_value)

        # serializes the set property result
        serialized_set_property_result = serializer.dumps(set_property_result)

        # sets the request contents
        self.set_contents(rest_request, serialized_set_property_result)

    def handle_set_property_json(self, rest_request, parameters = {}):
        """
        Handles the given set property json rest request.

        @type rest_request: RestRequest
        @param rest_request: The set property json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        json_plugin = self.web_mvc_communication_push_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle set property serialized method
        self.handle_set_property_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    def handle_stat_serialized(self, rest_request, parameters = {}):
        """
        Handles the given stat serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The stat serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the information item
        information_item = form_data_map[INFORMATION_ITEM_VALUE]

        # retrieves the information keys
        information_keys = form_data_map[INFORMATION_KEYS_VALUE]

        # performs the stat for the given request
        stat_result = self._stat(rest_request, information_item, information_keys)

        # serializes the stat result
        serialized_stat_result = serializer.dumps(stat_result)

        # sets the request contents
        self.set_contents(rest_request, serialized_stat_result)

    def handle_stat_json(self, rest_request, parameters = {}):
        """
        Handles the given stat json rest request.

        @type rest_request: RestRequest
        @param rest_request: The stat json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.web_mvc_communication_push_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle stat serialized method
        self.handle_stat_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    def handle_load_profile_serialized(self, rest_request, parameters = {}):
        """
        Handles the given load profile serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The load profile serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication handler name
        communication_handler_name = form_data_map[COMMUNICATION_HANDLER_NAME_VALUE]

        # retrieves the communication profile name
        communication_profile_name = form_data_map[COMMUNICATION_PROFILE_NAME_VALUE]

        # retrieves the return url
        return_url = form_data_map[RETURN_URL_VALUE]

        # retrieves the method
        method = form_data_map.get(METHOD_VALUE, GET_METHOD_VALUE)

        # loads the profile for the given request
        load_profile_result = self._load_profile(rest_request, communication_handler_name, communication_profile_name, return_url, method)

        # serializes the load profile result
        serialized_load_profile_result = serializer.dumps(load_profile_result)

        # sets the request contents
        self.set_contents(rest_request, serialized_load_profile_result)

    def handle_load_profile_json(self, rest_request, parameters = {}):
        """
        Handles the given load profile json rest request.

        @type rest_request: RestRequest
        @param rest_request: The load profile json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.web_mvc_communication_push_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle load profile serialized method
        self.handle_load_profile_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    def handle_unload_profile_serialized(self, rest_request, parameters = {}):
        """
        Handles the given unload profile serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The unload profile serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication handler name
        communication_handler_name = form_data_map[COMMUNICATION_HANDLER_NAME_VALUE]

        # retrieves the communication profile name
        communication_profile_name = form_data_map[COMMUNICATION_PROFILE_NAME_VALUE]

        # retrieves the return url
        return_url = form_data_map[RETURN_URL_VALUE]

        # unloads the profile for the given request
        unload_profile_result = self._unload_profile(rest_request, communication_handler_name, communication_profile_name, return_url)

        # serializes the load profile result
        serialized_unload_profile_result = serializer.dumps(unload_profile_result)

        # sets the request contents
        self.set_contents(rest_request, serialized_unload_profile_result)

    def handle_unload_profile_json(self, rest_request, parameters = {}):
        """
        Handles the given unload profile json rest request.

        @type rest_request: RestRequest
        @param rest_request: The unload profile json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.web_mvc_communication_push_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle unload profile serialized method
        self.handle_unload_profile_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    def handle_set_profile_serialized(self, rest_request, parameters = {}):
        """
        Handles the given set profile serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The set profile serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication profile name
        communication_profile_name = form_data_map[COMMUNICATION_PROFILE_NAME_VALUE]

        # retrieves the communication name
        communication_name = form_data_map[COMMUNICATION_NAME_VALUE]

        # sets the profile for the given request
        set_profile_result = self._set_profile(rest_request, communication_profile_name, communication_name)

        # serializes the set profile result
        serialized_set_profile_result = serializer.dumps(set_profile_result)

        # sets the request contents
        self.set_contents(rest_request, serialized_set_profile_result)

    def handle_set_profile_json(self, rest_request, parameters = {}):
        """
        Handles the given set profile json rest request.

        @type rest_request: RestRequest
        @param rest_request: The set profile json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.web_mvc_communication_push_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle set profile serialized method
        self.handle_set_profile_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    def handle_unset_profile_serialized(self, rest_request, parameters = {}):
        """
        Handles the given unset profile serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The unset profile serialized rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication profile name
        communication_profile_name = form_data_map[COMMUNICATION_PROFILE_NAME_VALUE]

        # retrieves the communication name
        communication_name = form_data_map[COMMUNICATION_NAME_VALUE]

        # unsets the profile for the given request
        unset_profile_result = self._unset_profile(rest_request, communication_profile_name, communication_name)

        # serializes the unset profile result
        serialized_unset_profile_result = serializer.dumps(unset_profile_result)

        # sets the request contents
        self.set_contents(rest_request, serialized_unset_profile_result)

    def handle_unset_profile_json(self, rest_request, parameters = {}):
        """
        Handles the given unset profile json rest request.

        @type rest_request: RestRequest
        @param rest_request: The unset profile json rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the json plugin
        json_plugin = self.web_mvc_communication_push_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle unset profile serialized method
        self.handle_unset_profile_serialized(rest_request, parameters)

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

            # defines the client parameters
            client_parameters = {
                CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET
            }

            # creates the http client
            http_client = main_client_http_plugin.create_client(client_parameters)

            # opens the http client
            http_client.open({})

            # retrieves the notification attributes
            message = notification.get_message()
            sender_id = notification.get_sender_id()
            guid = notification.get_guid()

            # creates the parameters map
            parameters = {
                COMMUNICATION_NAME_VALUE : communication_name,
                COMMUNICATION_HANDLER_NAME_VALUE : sender_id,
                GUID_VALUE : guid,
                MESSAGE_CONTENTS_VALUE : message
            }

            # fetches the url, retrieving the contents
            http_client.fetch_url(return_url, method, parameters, content_type_charset = DEFAULT_CHARSET)

            # closes the http client
            http_client.close({})

        # returns the communication handler
        return communication_handler

    def _register(self, rest_request, communication_handler_name, communication_name, return_url, method):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # generates a communication handler for the given return url and method
        generated_communication_handler = self.generate_handler(return_url, method)

        # creates the service connection name tuple
        service_connection_name_tuple = (
            communication_handler_name,
            return_url,
            communication_name
        )

        # sets the generated communication handler in the service connection name communication handler map
        self.service_connection_name_communication_handler_map[service_connection_name_tuple] = generated_communication_handler

        # adds a new communication handler
        communication_push_plugin.add_communication_handler(communication_name, communication_handler_name, generated_communication_handler)

    def _unregister(self, rest_request, communication_handler_name, communication_name, return_url):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # creates the service connection name tuple
        service_connection_name_tuple = (
            communication_handler_name,
            return_url,
            communication_name
        )

        # retrieves the generated communication handler for the service connection and communication name
        generated_communication_handler = self.service_connection_name_communication_handler_map[service_connection_name_tuple]

        # removes the communication handler
        communication_push_plugin.remove_communication_handler(communication_name, communication_handler_name, generated_communication_handler)

        # removes the service connection name from the service connection name communication handler map
        del self.service_connection_name_communication_handler_map[service_connection_name_tuple]

    def _message(self, rest_request, communication_handler_name, communication_name, message):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # generates the notification
        notification = communication_push_plugin.generate_notification(message, communication_handler_name)

        # sends the broadcast notification, for the communication name
        # and notification
        communication_push_plugin.send_broadcast_notification(communication_name, notification)

    def _set_property(self, rest_request, communication_handler_name, property_name, property_value):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # sets the communication handler property
        communication_push_plugin.set_communication_handler_property(communication_handler_name, property_name, property_value)

    def _stat(self, rest_request, information_item, information_keys):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # in case the requested information is of type communication
        if information_item == COMMUNICATION_VALUE:
            # sets the information method as the communication information retriever
            information_method = communication_push_plugin.get_communication_information
        # in case the requested information is of type communication handler
        elif information_item == COMMUNICATION_HANDLER_VALUE:
            # sets the information method as the communication handler information retriever
            information_method = communication_push_plugin.get_communication_handler_information
        # in case the requested information is of type communication profile
        elif information_item == COMMUNICATION_PROFILE_VALUE:
            # sets the information method as the communication profile information retriever
            information_method = communication_push_plugin.get_communication_profile_information
        # in case the requested information is not valid
        else:
            # raises the invalid information item exception
            raise web_mvc_communication_push_exceptions.InvalidInformationItem(information_item)

        # creates the list to hold the information values
        information_values_list = []

        # iterates over all the information keys to retrieve
        # the various information values
        for information_key in information_keys:
            # retrieves the information value for the information key
            # using the selected information method
            information_value = information_method(information_key)

            # adds the information value to the information values list
            information_values_list.append(information_value)

        # returns the information values list, containing
        # the set of information for the request items
        return information_values_list

    def _load_profile(self, rest_request, communication_handler_name, communication_profile_name, return_url, method):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # generates a communication handler for the given return url and method
        generated_communication_handler = self.generate_handler(return_url, method)

        # creates the service connection profile name tuple
        service_connection_profile_name_tuple = (
            communication_handler_name,
            return_url,
            communication_profile_name
        )

        # sets the generated communication handler in the service connection profile name communication handler map
        self.service_connection_profile_name_communication_handler_map[service_connection_profile_name_tuple] = generated_communication_handler

        # loads the communication profile
        communication_push_plugin.load_communication_profile(communication_handler_name, communication_profile_name, generated_communication_handler)

    def _unload_profile(self, rest_request, communication_handler_name, communication_profile_name, return_url):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # creates the service connection profile name tuple
        service_connection_profile_name_tuple = (
            communication_handler_name,
            return_url,
            communication_profile_name
        )

        # retrieves the generated communication handler for the service connection and communication profile name
        generated_communication_handler = self.service_connection_profile_name_communication_handler_map[service_connection_profile_name_tuple]

        # unloads the communication profile
        communication_push_plugin.unload_communication_profile(communication_handler_name, communication_profile_name, generated_communication_handler)

        # removes the service connection profile name from the service connection profile name communication handler map
        del self.service_connection_profile_name_communication_handler_map[service_connection_profile_name_tuple]

    def _set_profile(self, rest_request, communication_profile_name, communication_name):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # sets the communication profile
        communication_push_plugin.set_communication_profile(communication_profile_name, communication_name)

    def _unset_profile(self, rest_request, communication_profile_name, communication_name):
        # retrieves the communication push plugin
        communication_push_plugin = self.web_mvc_communication_push_plugin.communication_push_plugin

        # unsets the communication profile
        communication_push_plugin.unset_communication_profile(communication_profile_name, communication_name)
