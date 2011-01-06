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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types
import hashlib

import colony.libs.string_buffer_util

import service_facebook_exceptions

DEFAULT_CHARSET = "utf-8"
""" The default charset """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

JSON_FORMAT_VALUE = "json"
""" The json format value """

DEFAULT_FORMAT_VALUE = JSON_FORMAT_VALUE
""" The default format value """

DEFAULT_API_VERSION = "1.0"
""" The default facebook api version """

BASE_REST_URL = "http://api.facebook.com/restserver.php"
""" The base rest url to be used """

BASE_REST_SECURE_URL = "https://api.facebook.com/restserver.php"
""" The base rest secure url to be used """

BASE_HOME_URL = "http://www.facebook.com/"
""" The base home url """

BASE_HOME_SECURE_URL = "https://www.facebook.com/"
""" The base home secure url """

class ServiceFacebook:
    """
    The service facebook class.
    """

    service_facebook_plugin = None
    """ The service facebook plugin """

    def __init__(self, service_facebook_plugin):
        """
        Constructor of the class.

        @type service_facebook_plugin: ServiceFacebookPlugin
        @param service_facebook_plugin: The service facebook plugin.
        """

        self.service_facebook_plugin = service_facebook_plugin

    def create_remote_client(self, service_attributes):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: FacebookClient
        @return: The created remote client.
        """

        # retrieves the main client http plugin
        main_client_http_plugin = self.service_facebook_plugin.main_client_http_plugin

        # retrieves the json plugin
        json_plugin = self.service_facebook_plugin.json_plugin

        # retrieves the facebook structure (if available)
        facebook_structure = service_attributes.get("facebook_structure", None)

        # creates a new facebook client with the given options
        facebook_client = FacebookClient(json_plugin, main_client_http_plugin, facebook_structure)

        # returns the facebook client
        return facebook_client

class FacebookClient:
    """
    The class that represents a facebook client connection.
    """

    json_plugin = None
    """ The json plugin """

    main_client_http_plugin = None
    """ The main client http plugin """

    facebook_structure = None
    """ The facebook structure """

    http_client = None
    """ The http client for the connection """

    def __init__(self, json_plugin = None, main_client_http_plugin = None, facebook_structure = None):
        """
        Constructor of the class.

        @type json_plugin: JsonPlugin
        @param json_plugin: The json plugin.
        @type main_client_http_plugin: MainClientHttpPlugin
        @param main_client_http_plugin: The main client http plugin.
        @type facebook_structure: FacebookStructure
        @param facebook_structure: The facebook structure.
        """

        self.json_plugin = json_plugin
        self.main_client_http_plugin = main_client_http_plugin
        self.facebook_structure = facebook_structure

    def open(self):
        """
        Opens the facebook client.
        """

        pass

    def close(self):
        """
        Closes the facebook client.
        """

        # in case an http client is defined
        if self.http_client:
            # closes the http client
            self.http_client.close({})

    def generate_facebook_structure(self, consumer_key, consumer_secret, next, api_version = DEFAULT_API_VERSION, set_structure = True):
        """
        Generates the facebook structure for the given arguments.

        @type consumer_key: String
        @param consumer_key: The consumer key.
        @type consumer_secret: String
        @param consumer_secret: The consumer secret.
        @type next: String
        @param next: The next value from which the facebook request
        will be redirecting.
        @type api_version: String
        @param api_version: The version of the api being used.
        @type set_structure: bool
        @param set_structure: If the structure should be
        set in the facebook client.
        @rtype: FacebookStructure
        @return: The generated facebook structure.
        """

        # creates a new facebook structure
        facebook_structure = FacebookStructure(consumer_key, consumer_secret, next, api_version)

        # in case the structure is meant to be set
        if set_structure:
            # sets the facebook structure
            self.set_facebook_structure(facebook_structure)

        # returns the facebook structure
        return facebook_structure

    def auth_create_token(self):
        """
        Initializes the process of creating an authentication token
        for the facebook session creation.

        @rtype: FacebookStructure
        @return: The current facebook structure.
        """

        # sets the retrieval url
        retrieval_url = BASE_REST_SECURE_URL

        # start the parameters map
        parameters = {}

        # sets the base parameters (including the signature)
        self._set_base_parameters("auth.createToken", parameters)

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters, POST_METHOD_VALUE)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for facebook errors
        self._check_facebook_errors(data)

        # sets the token in the facebook structure
        self.facebook_structure.token = data

        # returns the facebook structure
        return self.facebook_structure

    def auth_get_session(self):
        """
        Retrieves a news session using the created auth token
        obtained from the user login.

        @rtype: FacebookStructure
        @return: The current facebook structure.
        """

        # sets the retrieval url
        retrieval_url = BASE_REST_SECURE_URL

        # start the parameters map
        parameters = {}

        # sets the authentication token
        parameters["auth_token"] = self.facebook_structure.token

        # sets the base parameters (including the signature)
        self._set_base_parameters("auth.getSession", parameters)

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters, POST_METHOD_VALUE)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for facebook errors
        self._check_facebook_errors(data)

        # sets the session key in the facebook structure
        self.facebook_structure.session_key = data["session_key"]

        # sets the user id in the facebook structure
        self.facebook_structure.user_id = data["uid"]

        # returns the facebook structure
        return self.facebook_structure

    def auth_get_info(self):
        # retrieves the user id
        user_id = self.facebook_structure.user_id

        # retrieves the user information
        user_info = self.user_get_user_info([user_id], ["username"])

        # sets the username in the facebook structure
        self.facebook_structure.username = user_info[0]["username"]

        # returns the faceboook structure
        return self.facebook_structure

    def get_login_url(self):
        """
        Retrieves the url used for facebook user login.

        @rtype: String
        @return: The url used for facebook user login.
        """

        # sets the retrieval url
        retrieval_url = BASE_HOME_SECURE_URL + "login.php"

        # start the parameters map
        parameters = {}

        # sets the api key
        parameters["api_key"] = self.facebook_structure.consumer_key

        # sets the version (v)
        parameters["v"] = self.facebook_structure.api_version

        # sets the next web site to redirect
        parameters["next"] = self.facebook_structure.next

        # creates the login url from the parameters
        login_url = self._build_url(retrieval_url, parameters)

        # returns the login url
        return login_url

    def user_get_user_info(self, user_id_list, fields):
        """
        Retrieves the user information for the given user identifiers
        and field.

        @type user_id_list: List
        @param user_id_list: The user id to retrieve the information.
        @type fields: List
        @param fields: The field to be retrieve as the user information.
        @rtype: Dictionary
        @return: The retrieved user information.
        """

        # sets the retrieval url
        retrieval_url = BASE_REST_SECURE_URL

        # start the parameters map
        parameters = {}

        # sets the user id list in the parameters
        parameters["uids"] = self._list_to_coma_string(user_id_list)

        # sets the fields in the parameters
        parameters["fields"] = self._list_to_coma_string(fields)

        # sets the base parameters (including the signature)
        self._set_base_parameters("users.getInfo", parameters)

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters, POST_METHOD_VALUE)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for facebook errors
        self._check_facebook_errors(data)

        # reeturns the data
        return data

    def _list_to_coma_string(self, list):
        # creates the coma string buffer
        coma_string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # sets the is first flag
        is_first = True

        # iterates over all the list items
        # in the list
        for list_item in list:
            # in case the is first flag is set
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # writes the coma to the coma string buffer
                coma_string_buffer.write(",")

            # converts the list item to string
            list_item_string = str(list_item)

            # writes the list item (in string) to
            # the coma string buffer
            coma_string_buffer.write(list_item_string)

        # retrieves the coma string value from the
        # coma string buffer
        coma_string = coma_string_buffer.get_value()

        # returns the coma string
        return coma_string

    def get_facebook_structure(self):
        """
        Retrieves the facebook structure.

        @rtype: FacebookStructure
        @return: The facebook structure.
        """

        return self.facebook_structure

    def set_facebook_structure(self, facebook_structure):
        """
        Sets the facebook structure.

        @type facebook_structure: FacebookStructure
        @param facebook_structure: The facebook structure.
        """

        self.facebook_structure = facebook_structure

    def _get_signature(self, parameters):
        """
        Calculates and retrieves the message signature
        for the given parameters.

        @type parameters: Dictionary
        @param parameters: The map with the parameters to be used
        to calculate the signature.
        @rtype: String
        @return: The calculated signature.
        """

        # creates the message string buffer
        message_string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # retrieves the parameters keys
        parameters_keys = parameters.keys()

        # sorts the parameters keys
        parameters_keys.sort()

        # iterates over all the parameters keys (ordered)
        for parameter_key in parameters_keys:
            # retrieves the parameter value
            parameter_value = parameters[parameter_key]

            # writes the key value pair in the message string buffer
            message_string_buffer.write(parameter_key + "=" + str(parameter_value))

        # writes the consumer secret to the message string buffer
        message_string_buffer.write(self.facebook_structure.consumer_secret)

        # retrieves the message from the message string buffer
        message = message_string_buffer.get_value()

        # returns the md5 hex digest for the message
        return hashlib.md5(message).hexdigest()

    def _set_base_parameters(self, method_name, parameters):
        """
        Sets the base facebook rest request parameters
        in the parameters map.

        @type method_name: String
        @param method_name: The name of the method to be called.
        @type parameters: Dictionary
        @param parameters: The parameters map to be used in setting
        the authentication parameters.
        """

        # sets the method name
        parameters["method"] = method_name

        # sets the api key
        parameters["api_key"] = self.facebook_structure.consumer_key

        # sets the version (v)
        parameters["v"] = self.facebook_structure.api_version

        # sets the format
        parameters["format"] = DEFAULT_FORMAT_VALUE

        # in case the session key is defined
        if self.facebook_structure.session_key:
            # sets the session key
            parameters["session_key"] = self.facebook_structure.session_key

        # calculates and sets the signature value
        parameters["sig"] = self._get_signature(parameters)

    def _fetch_url(self, url, parameters = None, method = GET_METHOD_VALUE):
        """
        Fetches the given url for the given parameters and using the given method.

        @type url: String
        @param url: The url to be fetched.
        @type parameters: Dictionary
        @param parameters: The parameters to be used the fetch.
        @type method: String
        @param method: The method to be used in the fetch.
        @rtype: String
        @return: The fetched data.
        """

        # in case parameters is not defined
        if not parameters:
            # creates a new parameters map
            parameters = {}

        # retrieves the http client
        http_client = self._get_http_client()

        # fetches the url retrieving the http response
        http_response = http_client.fetch_url(url, method, parameters, content_type_charset = DEFAULT_CHARSET)

        # retrieves the contents from the http response
        contents = http_response.received_message

        # returns the contents
        return contents

    def _build_url(self, base_url, parameters):
        """
        Builds the url for the given url and parameters.

        @type url: String
        @param url: The base url to be used.
        @type parameters: Dictionary
        @param parameters: The parameters to be used for url construction.
        @rtype: String
        @return: The built url for the given parameters.
        """

        # retrieves the http client
        http_client = self._get_http_client()

        # build the url from the base urtl
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)

        # returns the url
        return url

    def _check_facebook_errors(self, data):
        """
        Checks the given data for facebook errors.

        @type data: String
        @param data: The data to be checked for facebook errors.
        @rtype: bool
        @return: The result of the data error check.
        """

        # retrieves the data type
        data_type = type(data)

        # in case the data is not of type dictionary
        if not data_type == types.DictType:
            # returns immediately
            return

        # retrieves the error code
        error_code = data.get("error_code", None)

        # in case the error code is not set
        if not error_code:
            # returns immediately
            return

        # retrieves the error message
        error_message = data.get("error_msg", None)

        # raises the facebook api error
        raise service_facebook_exceptions.FacebookApiError("error in request: " + error_message)

    def _get_http_client(self):
        """
        Retrieves the http client currently in use (in case it's created)
        if not created creates the http client.

        @rtype: HttpClient
        @return: The retrieved http client.
        """

        # in case no http client exists
        if not self.http_client:
            # creates the http client
            self.http_client = self.main_client_http_plugin.create_client({CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET})

            # opens the http client
            self.http_client.open({})

        # returns the http client
        return self.http_client

class FacebookStructure:
    """
    The facebook structure class.
    """

    consumer_key = None
    """ The consumer key """

    consumer_secret = None
    """ The consumer secret """

    next = None
    """ The next value from which the facebook request will be redirecting """

    api_version = None
    """ The version of the api being used """

    token = None
    """ The authentication token used """

    session_key = None
    """ The key used to identify the session """

    user_id = None
    """ The identification of the logged user """

    username = None
    """ The username of the logged user """

    def __init__(self, consumer_key, consumer_secret, next, api_version = DEFAULT_API_VERSION):
        """
        Constructor of the class.

        @type consumer_key: String
        @param consumer_key: The consumer key.
        @type consumer_secret: String
        @param consumer_secret: The consumer secret.
        @type next: String
        @param next: The next value from which the facebook request
        will be redirecting.
        @type api_version: String
        @param api_version: The version of the api being used.
        """

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.next = next
        self.api_version = api_version

    def get_consumer_key(self):
        """
        Retrieves the consumer key.

        @rtype: String
        @return: The consumer key.
        """

        return self.consumer_key

    def set_consumer_key(self, consumer_key):
        """
        Sets the consumer key.

        @type consumer_key: String
        @param consumer_key: The consumer key.
        """

        self.consumer_key = consumer_key

    def get_consumer_secret(self):
        """
        Retrieves the consumer secret.

        @rtype: String
        @return: The consumer secret.
        """

        return self.consumer_secret

    def set_consumer_secret(self, consumer_secret):
        """
        Sets the consumer key.

        @type consumer_secret: String
        @param consumer_secret: The consumer secret.
        """

        self.consumer_secret = consumer_secret

    def get_next(self):
        """
        Retrieves the next.

        @rtype: String
        @return: The next.
        """

        return self.next

    def set_next(self, next):
        """
        Sets the next.

        @type next: String
        @param next: The next.
        """

        self.next = next

    def get_api_version(self):
        """
        Retrieves the api version.

        @rtype: String
        @return: The api version.
        """

        return self.api_version

    def set_api_version(self, api_version):
        """
        Sets the api version.

        @type api_version: String
        @param api_version: The api version.
        """

        self.api_version = api_version

    def get_token(self):
        """
        Retrieves the token.

        @rtype: String
        @return: The token.
        """

        return self.token

    def set_token(self, token):
        """
        Sets the token.

        @type token: String
        @param token: The token.
        """

        self.token = token

    def get_session_key(self):
        """
        Retrieves the session key.

        @rtype: String
        @return: The session key.
        """

        return self.session_key

    def set_session_key(self, session_key):
        """
        Sets the session key.

        @type session_key: String
        @param session_key: The session key.
        """

        self.session_key = session_key

    def get_user_id(self):
        """
        Retrieves the user id.

        @rtype: String
        @return: The user id.
        """

        return self.user_id

    def set_user_id(self, user_id):
        """
        Sets the user id.

        @type user_id: String
        @param user_id: The user id.
        """

        self.user_id = user_id

    def get_username(self):
        """
        Retrieves the username.

        @rtype: String
        @return: The username.
        """

        return self.username

    def set_username(self, username):
        """
        Sets the username.

        @type username: String
        @param username: The username.
        """

        self.username = username
