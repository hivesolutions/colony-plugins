#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2019 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import hashlib

import colony

from . import exceptions

DEFAULT_CHARSET = "utf-8"
""" The default charset """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

JSON_FORMAT_VALUE = "json"
""" The JSON format value """

DEFAULT_FORMAT_VALUE = JSON_FORMAT_VALUE
""" The default format value """

DEFAULT_API_VERSION = "1.0"
""" The default Facebook API version """

DEFAULT_CONSUMER_ID = None
""" The default consumer id """

DEFAULT_SCOPE = ""
""" The default scope """

BASE_REST_URL = "http://api.facebook.com/restserver.php"
""" The base rest URL to be used """

BASE_REST_SECURE_URL = "https://api.facebook.com/restserver.php"
""" The base rest secure URL to be used """

BASE_HOME_URL = "http://www.facebook.com/"
""" The base home URL """

BASE_HOME_SECURE_URL = "https://www.facebook.com/"
""" The base home secure URL """

BASE_REST_OAUTH_URL = "http://www.facebook.com/"
""" The base rest oauth URL """

BASE_REST_OAUTH_SECURE_URL = "https://www.facebook.com/"
""" The base rest oauth secure URL """

BASE_REST_GRAPH_URL = "http://graph.facebook.com/"
""" The base rest graph URL """

BASE_REST_GRAPH_SECURE_URL = "https://graph.facebook.com/"
""" The base rest graph secure URL """

FACEBOOK_CLIENT_TYPE_REST = "rest"
""" The rest Facebook client type """

FACEBOOK_CLIENT_TYPE_OAUTH = "oauth"
""" The oauth Facebook client type """

DEFAULT_FACEBOOK_CLIENT_TYPE = FACEBOOK_CLIENT_TYPE_REST
""" The default Facebook client type is rest """

class ApiFacebook(colony.System):
    """
    The API Facebook class.
    """

    facebook_client_map = {}
    """ The map associating the client type with the client class """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)

        self.facebook_client_map = {
            FACEBOOK_CLIENT_TYPE_REST : FacebookClient,
            FACEBOOK_CLIENT_TYPE_OAUTH : FacebookClientOauth
        }

    def create_client(self, api_attributes, open_client = True):
        """
        Creates a client, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :type open_client: bool
        :param open_client: If the client should be opened.
        :rtype: FacebookClient
        :return: The created client.
        """

        # retrieves the client HTTP plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the JSON plugin
        json_plugin = self.plugin.json_plugin

        # retrieves the various attributes to be used in the
        # construction of the Facebook client
        facebook_structure = api_attributes.get("facebook_structure", None)
        facebook_client_type = api_attributes.get("facebook_client_type", DEFAULT_FACEBOOK_CLIENT_TYPE)

        # retrieves the Facebook client (class) for the "requested" type
        facebook_client_class = self.facebook_client_map.get(facebook_client_type, FacebookClient)

        # creates a new client with the given options, opens
        # it in case it's required and returns the generated
        # client to the caller method
        facebook_client = facebook_client_class(json_plugin, client_http_plugin, facebook_structure)
        open_client and facebook_client.open()
        return facebook_client

class FacebookClient(object):
    """
    The class that represents a Facebook client connection.
    """

    json_plugin = None
    """ The JSON plugin """

    client_http_plugin = None
    """ The client HTTP plugin """

    facebook_structure = None
    """ The Facebook structure """

    http_client = None
    """ The HTTP client for the connection """

    def __init__(self, json_plugin = None, client_http_plugin = None, facebook_structure = None):
        """
        Constructor of the class.

        :type json_plugin: JSONPlugin
        :param json_plugin: The JSON plugin.
        :type client_http_plugin: ClientHttpPlugin
        :param client_http_plugin: The client HTTP plugin.
        :type facebook_structure: FacebookStructure
        :param facebook_structure: The Facebook structure.
        """

        self.json_plugin = json_plugin
        self.client_http_plugin = client_http_plugin
        self.facebook_structure = facebook_structure

    def open(self):
        """
        Opens the Facebook client.
        """

        pass

    def close(self):
        """
        Closes the Facebook client.
        """

        # in case an HTTP client is defined
        if self.http_client:
            # closes the HTTP client
            self.http_client.close({})

    def generate_facebook_structure(
        self,
        consumer_key,
        consumer_secret,
        next,
        api_version = DEFAULT_API_VERSION,
        set_structure = True
    ):
        """
        Generates the Facebook structure for the given arguments.

        :type consumer_key: String
        :param consumer_key: The consumer key.
        :type consumer_secret: String
        :param consumer_secret: The consumer secret.
        :type next: String
        :param next: The next value from which the Facebook request
        will be redirecting.
        :type api_version: String
        :param api_version: The version of the API being used.
        :type set_structure: bool
        :param set_structure: If the structure should be
        set in the Facebook client.
        :rtype: FacebookStructure
        :return: The generated Facebook structure.
        """

        # creates a new Facebook structure
        facebook_structure = FacebookStructure(consumer_key, consumer_secret, next, api_version)

        # in case the structure is meant to be set
        if set_structure:
            # sets the Facebook structure
            self.set_facebook_structure(facebook_structure)

        # returns the Facebook structure
        return facebook_structure

    def auth_create_token(self):
        """
        Initializes the process of creating an authentication token
        for the Facebook session creation.

        :rtype: FacebookStructure
        :return: The current Facebook structure.
        """

        # sets the retrieval URL
        retrieval_url = BASE_REST_SECURE_URL

        # start the parameters map
        parameters = {}

        # sets the base parameters (including the signature)
        self._set_base_parameters("auth.createToken", parameters)

        # fetches the retrieval URL with the given parameters retrieving the JSON
        json = self._fetch_url(retrieval_url, parameters, POST_METHOD_VALUE)

        # loads JSON retrieving the data
        data = self.json_plugin.loads(json)

        # checks for Facebook errors
        self._check_facebook_errors(data)

        # sets the token in the Facebook structure
        self.facebook_structure.token = data

        # returns the Facebook structure
        return self.facebook_structure

    def auth_get_session(self):
        """
        Retrieves a news session using the created auth token
        obtained from the user login.

        :rtype: FacebookStructure
        :return: The current Facebook structure.
        """

        # sets the retrieval URL
        retrieval_url = BASE_REST_SECURE_URL

        # start the parameters map
        parameters = {}

        # sets the authentication token
        parameters["auth_token"] = self.facebook_structure.token

        # sets the base parameters (including the signature)
        self._set_base_parameters("auth.getSession", parameters)

        # fetches the retrieval URL with the given parameters retrieving the JSON
        json = self._fetch_url(retrieval_url, parameters, POST_METHOD_VALUE)

        # loads JSON retrieving the data
        data = self.json_plugin.loads(json)

        # checks for Facebook errors
        self._check_facebook_errors(data)

        # sets the session key in the Facebook structure
        self.facebook_structure.session_key = data["session_key"]

        # sets the user id in the Facebook structure
        self.facebook_structure.user_id = data["uid"]

        # returns the Facebook structure
        return self.facebook_structure

    def auth_get_info(self):
        # retrieves the user id
        user_id = self.facebook_structure.user_id

        # retrieves the user information
        user_info = self.user_get_user_info([user_id], ["username"])

        # sets the username in the Facebook structure
        self.facebook_structure.username = user_info[0]["username"]

        # returns the Facebook structure
        return self.facebook_structure

    def get_login_url(self):
        """
        Retrieves the URL used for Facebook user login.

        :rtype: String
        :return: The URL used for Facebook user login.
        """

        # sets the retrieval URL
        retrieval_url = BASE_HOME_SECURE_URL + "login.php"

        # start the parameters map
        parameters = {}

        # sets the API key
        parameters["api_key"] = self.facebook_structure.consumer_key

        # sets the version (v)
        parameters["v"] = self.facebook_structure.api_version

        # sets the next web site to redirect
        parameters["next"] = self.facebook_structure.next

        # creates the login URL from the parameters
        login_url = self._build_url(retrieval_url, parameters)

        # returns the login URL
        return login_url

    def user_get_user_info(self, user_id_list, fields):
        """
        Retrieves the user information for the given user identifiers
        and field.

        :type user_id_list: List
        :param user_id_list: The user id to retrieve the information.
        :type fields: List
        :param fields: The field to be retrieve as the user information.
        :rtype: Dictionary
        :return: The retrieved user information.
        """

        # sets the retrieval URL
        retrieval_url = BASE_REST_SECURE_URL

        # start the parameters map
        parameters = {}

        # sets the user id list in the parameters
        parameters["uids"] = self._list_to_coma_string(user_id_list)

        # sets the fields in the parameters
        parameters["fields"] = self._list_to_coma_string(fields)

        # sets the base parameters (including the signature)
        self._set_base_parameters("users.getInfo", parameters)

        # fetches the retrieval URL with the given parameters retrieving the JSON
        json = self._fetch_url(retrieval_url, parameters, POST_METHOD_VALUE)

        # loads JSON retrieving the data
        data = self.json_plugin.loads(json)

        # checks for Facebook errors
        self._check_facebook_errors(data)

        # reeturns the data
        return data

    def _list_to_coma_string(self, list):
        # creates the coma string buffer
        coma_string_buffer = colony.StringBuffer()

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
        Retrieves the Facebook structure.

        :rtype: FacebookStructure
        :return: The Facebook structure.
        """

        return self.facebook_structure

    def set_facebook_structure(self, facebook_structure):
        """
        Sets the Facebook structure.

        :type facebook_structure: FacebookStructure
        :param facebook_structure: The Facebook structure.
        """

        self.facebook_structure = facebook_structure

    def _get_signature(self, parameters):
        """
        Calculates and retrieves the message signature
        for the given parameters.

        :type parameters: Dictionary
        :param parameters: The map with the parameters to be used
        to calculate the signature.
        :rtype: String
        :return: The calculated signature.
        """

        # creates the message string buffer
        message_string_buffer = colony.StringBuffer()

        # retrieves the parameters keys and then runs
        # the sorting operation in them
        parameters_keys = colony.legacy.keys(parameters)
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
        Sets the base Facebook rest request parameters
        in the parameters map.

        :type method_name: String
        :param method_name: The name of the method to be called.
        :type parameters: Dictionary
        :param parameters: The parameters map to be used in setting
        the authentication parameters.
        """

        # sets the method name
        parameters["method"] = method_name

        # sets the API key
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
        Fetches the given URL for the given parameters and using the given method.

        :type url: String
        :param url: The URL to be fetched.
        :type parameters: Dictionary
        :param parameters: The parameters to be used the fetch.
        :type method: String
        :param method: The method to be used in the fetch.
        :rtype: String
        :return: The fetched data.
        """

        # in case parameters is not defined
        if not parameters:
            # creates a new parameters map
            parameters = {}

        # retrieves the HTTP client
        http_client = self._get_http_client()

        # fetches the url retrieving the HTTP response
        http_response = http_client.fetch_url(url, method, parameters, content_type_charset = DEFAULT_CHARSET)

        # retrieves the contents from the HTTP response
        contents = http_response.received_message

        # returns the contents
        return contents

    def _build_url(self, base_url, parameters):
        """
        Builds the URL for the given URL and parameters.

        :type url: String
        :param url: The base URL to be used.
        :type parameters: Dictionary
        :param parameters: The parameters to be used for URL construction.
        :rtype: String
        :return: The built URL for the given parameters.
        """

        # retrieves the HTTP client
        http_client = self._get_http_client()

        # build the URL from the base URL
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)

        # returns the URL
        return url

    def _check_facebook_errors(self, data):
        """
        Checks the given data for Facebook errors.

        This method raises an exception in case an error
        exists in the data to be verified.

        :type data: Dictionary/Object
        :param data: The data to be checked for Facebook errors.
        """

        # retrieves the data type and returns immediately
        # in case it is not of type dictionary
        data_type = type(data)
        if not data_type == dict: return

        # retrieves the error code and returns
        # immediately in case the error code is not set
        error_code = data.get("error_code", None)
        if not error_code: return

        # retrieves the error message
        error_message = data.get("error_msg", None)

        # raises the Facebook API error
        raise exceptions.FacebookApiError("error in request: " + error_message)

    def _get_http_client(self):
        """
        Retrieves the HTTP client currently in use (in case it's created)
        if not created creates the HTTP client.

        :rtype: HttpClient
        :return: The retrieved HTTP client.
        """

        # in case no HTTP client exists
        if not self.http_client:
            # defines the client parameters
            client_parameters = {
                CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET
            }

            # creates the HTTP client
            self.http_client = self.client_http_plugin.create_client(client_parameters)

            # opens the HTTP client
            self.http_client.open({})

        # returns the HTTP client
        return self.http_client

class FacebookClientOauth(object):
    """
    The class that represents a Facebook client oauth connection.
    """

    json_plugin = None
    """ The JSON plugin """

    client_http_plugin = None
    """ The client HTTP plugin """

    facebook_structure = None
    """ The Facebook structure """

    http_client = None
    """ The HTTP client for the connection """

    def __init__(self, json_plugin = None, client_http_plugin = None, facebook_structure = None):
        """
        Constructor of the class.

        :type json_plugin: JSONPlugin
        :param json_plugin: The JSON plugin.
        :type client_http_plugin: ClientHttpPlugin
        :param client_http_plugin: The client HTTP plugin.
        :type facebook_structure: FacebookStructure
        :param facebook_structure: The Facebook structure.
        """

        self.json_plugin = json_plugin
        self.client_http_plugin = client_http_plugin
        self.facebook_structure = facebook_structure

    def open(self):
        """
        Opens the Facebook client.
        """

        pass

    def close(self):
        """
        Closes the Facebook client.
        """

        # in case an HTTP client is defined
        if self.http_client:
            # closes the HTTP client
            self.http_client.close({})

    def generate_facebook_structure(self, consumer_key, consumer_secret, next, api_version = DEFAULT_API_VERSION, consumer_id = DEFAULT_CONSUMER_ID, scope = DEFAULT_SCOPE, set_structure = True):
        """
        Generates the Facebook structure for the given arguments.

        :type consumer_key: String
        :param consumer_key: The consumer key.
        :type consumer_secret: String
        :param consumer_secret: The consumer secret.
        :type next: String
        :param next: The next value from which the Facebook request
        will be redirecting.
        :type api_version: String
        :param api_version: The version of the API being used.
        :type consumer_id: String
        :param consumer_id: The consumer id.
        :type scope: String
        :param scope: The authorized scope.
        :type set_structure: bool
        :param set_structure: If the structure should be
        set in the Facebook client.
        :rtype: FacebookStructure
        :return: The generated Facebook structure.
        """

        # creates a new Facebook structure
        facebook_structure = FacebookStructure(consumer_key, consumer_secret, next, api_version, consumer_id, scope)

        # in case the structure is meant to be set
        if set_structure:
            # sets the Facebook structure
            self.set_facebook_structure(facebook_structure)

        # returns the Facebook structure
        return facebook_structure

    def get_login_url(self):
        """
        Retrieves the URL used to redirect the user to Facebook, for user
        authentication and app authorization.

        :rtype: String
        :return: The URL used to redirect the user to Facebook, for login.
        """

        # sets the retrieval URL
        retrieval_url = BASE_REST_OAUTH_SECURE_URL + "dialog/oauth"

        # start the parameters map
        parameters = {}

        # sets the client id
        parameters["client_id"] = self.facebook_structure.consumer_id

        # sets the redirect uri
        parameters["redirect_uri"] = self.facebook_structure.next

        # sets the scope
        parameters["scope"] = self.facebook_structure.scope

        # creates the login URL from the parameters
        login_url = self._build_url(retrieval_url, parameters)

        # returns the login URL
        return login_url

    def authenticate_application(self, authorization_code):
        """
        Performs app authentication with Facebook, using the received
        authorization code available.

        :type authorization_code: String
        :param authorization_code: The authorization code provided by Facebook
        to the application.
        """

        # sets the retrieval URL
        retrieval_url = BASE_REST_GRAPH_SECURE_URL + "oauth/access_token"

        # starts the parameters map
        parameters = {}

        # sets the client id
        parameters["client_id"] = self.facebook_structure.consumer_id

        # sets the redirect uri
        parameters["redirect_uri"] = self.facebook_structure.next

        # sets the client secret
        parameters["client_secret"] = self.facebook_structure.consumer_secret

        # sets the authentication code
        parameters["code"] = authorization_code

        # fetches the token endpoint URL, along with the required parameters
        response_text = self._fetch_url(retrieval_url, parameters, GET_METHOD_VALUE)

        # tries to retrieve the field map from the response
        field_map = self._parse_query_string(response_text)

        # in case the field map was not parsed
        if not field_map:
            # loads JSON retrieving the data
            data = self.json_plugin.loads(response_text)

            # checks for Facebook errors
            self._check_facebook_errors(data)

        # retrieves the access token from the field map
        access_token = field_map["access_token"]

        # sets the access token in the Facebook structure
        self.facebook_structure.session_key = access_token

    def get_user_data(self):
        # sets the retrieval URL
        retrieval_url = BASE_REST_GRAPH_SECURE_URL + "me"

        # starts the parameters map
        parameters = {}

        # sets the client id
        parameters["access_token"] = self.facebook_structure.session_key

        # fetches the user data URL, along with the required parameters
        json = self._fetch_url(retrieval_url, parameters, GET_METHOD_VALUE)

        # loads JSON retrieving the data
        data = self.json_plugin.loads(json)

        # checks for Facebook errors
        self._check_facebook_errors(data)

        # returns the parsed data
        return data

    def get_facebook_structure(self):
        """
        Retrieves the Facebook structure.

        :rtype: FacebookStructure
        :return: The Facebook structure.
        """

        return self.facebook_structure

    def set_facebook_structure(self, facebook_structure):
        """
        Sets the Facebook structure.

        :type facebook_structure: FacebookStructure
        :param facebook_structure: The Facebook structure.
        """

        self.facebook_structure = facebook_structure

    def _fetch_url(self, url, parameters = None, method = GET_METHOD_VALUE):
        """
        Fetches the given URL for the given parameters and using the given method.

        :type url: String
        :param url: The URL to be fetched.
        :type parameters: Dictionary
        :param parameters: The parameters to be used the fetch.
        :type method: String
        :param method: The method to be used in the fetch.
        :rtype: String
        :return: The fetched data.
        """

        # in case parameters is not defined
        if not parameters:
            # creates a new parameters map
            parameters = {}

        # retrieves the HTTP client
        http_client = self._get_http_client()

        # fetches the URL retrieving the HTTP response
        http_response = http_client.fetch_url(url, method, parameters, content_type_charset = DEFAULT_CHARSET)

        # retrieves the contents from the HTTP response
        contents = http_response.received_message

        # returns the contents
        return contents

    def _build_url(self, base_url, parameters):
        """
        Builds the URL for the given URL and parameters.

        :type url: String
        :param url: The base URL to be used.
        :type parameters: Dictionary
        :param parameters: The parameters to be used for URL construction.
        :rtype: String
        :return: The built URL for the given parameters.
        """

        # retrieves the HTTP client
        http_client = self._get_http_client()

        # build the URL from the base URL
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)

        # returns the URL
        return url

    def _check_facebook_errors(self, data):
        """
        Checks the given data for Facebook errors.

        This method raises an exception in case an error
        exists in the data to be verified.

        :type data: Dictionary/Object
        :param data: The data to be checked for Facebook errors.
        """

        # retrieves the data type and returns immediately
        # in case it is not of type dictionary
        data_type = type(data)
        if not data_type == dict: return

        # retrieves the error code and returns
        # immediately in case the error code is not set
        error_code = data.get("error_code", None)
        if not error_code: return

        # retrieves the error message
        error_message = data.get("error_msg", None)

        # raises the Facebook API error
        raise exceptions.FacebookApiError("error in request: " + error_message)

    def _parse_query_string(self, query_string):
        """
        Parses the query string value, creating a map
        containing the various key value pair associations.
        The values are not unquoted and as such they are
        prone to encoding errors.

        :type query_string: String
        :param query_string: The query string value to be
        decoded and parsed into the key values map.
        :rtype: Dictionary
        :return: The map resulting from the parsing of the
        provided query string value.
        """

        # creates the response map
        fields_map = {}

        # splits the field value pairs
        field_value_pairs = query_string.split("&")

        # iterates over each of the field value pairs
        # to create the proper map associations
        for field_value_pair in field_value_pairs:
            # retrieves the field and value from the pair
            field, value = field_value_pair.split("=")

            # sets the field and value in the map
            fields_map[field] = value

        # returns the fields map
        return fields_map

    def _get_http_client(self):
        """
        Retrieves the HTTP client currently in use (in case it's created)
        if not created creates the HTTP client.

        :rtype: HttpClient
        :return: The retrieved HTTP client.
        """

        # in case no HTTP client exists
        if not self.http_client:
            # defines the client parameters
            client_parameters = {
                CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET
            }

            # creates the HTTP client
            self.http_client = self.client_http_plugin.create_client(client_parameters)

            # opens the HTTP client
            self.http_client.open({})

        # returns the HTTP client
        return self.http_client

class FacebookStructure(object):
    """
    The Facebook structure class.
    """

    consumer_key = None
    """ The consumer key """

    consumer_secret = None
    """ The consumer secret """

    next = None
    """ The next value from which the Facebook request will be redirecting """

    api_version = None
    """ The version of the API being used """

    consumer_id = None
    """ The consumer id """

    scope = None
    """ The authorized scope """

    token = None
    """ The authentication token used """

    session_key = None
    """ The key used to identify the session """

    user_id = None
    """ The identification of the logged user """

    username = None
    """ The username of the logged user """

    def __init__(
        self,
        consumer_key,
        consumer_secret,
        next,
        api_version = DEFAULT_API_VERSION,
        consumer_id = DEFAULT_CONSUMER_ID,
        scope = DEFAULT_SCOPE
    ):
        """
        Constructor of the class.

        :type consumer_key: String
        :param consumer_key: The consumer key.
        :type consumer_secret: String
        :param consumer_secret: The consumer secret.
        :type next: String
        :param next: The next value from which the Facebook request
        will be redirecting.
        :type api_version: String
        :param api_version: The version of the API being used.
        :type consumer_id: String
        :param consumer_id: The consumer id.
        :type scope: String
        :param scope: The authorizated scope.
        """

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.next = next
        self.api_version = api_version
        self.consumer_id = consumer_id
        self.scope = scope

    def get_consumer_key(self):
        """
        Retrieves the consumer key.

        :rtype: String
        :return: The consumer key.
        """

        return self.consumer_key

    def set_consumer_key(self, consumer_key):
        """
        Sets the consumer key.

        :type consumer_key: String
        :param consumer_key: The consumer key.
        """

        self.consumer_key = consumer_key

    def get_consumer_secret(self):
        """
        Retrieves the consumer secret.

        :rtype: String
        :return: The consumer secret.
        """

        return self.consumer_secret

    def set_consumer_secret(self, consumer_secret):
        """
        Sets the consumer key.

        :type consumer_secret: String
        :param consumer_secret: The consumer secret.
        """

        self.consumer_secret = consumer_secret

    def get_next(self):
        """
        Retrieves the next.

        :rtype: String
        :return: The next.
        """

        return self.next

    def set_next(self, next):
        """
        Sets the next.

        :type next: String
        :param next: The next.
        """

        self.next = next

    def get_api_version(self):
        """
        Retrieves the API version.

        :rtype: String
        :return: The API version.
        """

        return self.api_version

    def set_api_version(self, api_version):
        """
        Sets the API version.

        :type api_version: String
        :param api_version: The API version.
        """

        self.api_version = api_version

    def get_token(self):
        """
        Retrieves the token.

        :rtype: String
        :return: The token.
        """

        return self.token

    def set_token(self, token):
        """
        Sets the token.

        :type token: String
        :param token: The token.
        """

        self.token = token

    def get_session_key(self):
        """
        Retrieves the session key.

        :rtype: String
        :return: The session key.
        """

        return self.session_key

    def set_session_key(self, session_key):
        """
        Sets the session key.

        :type session_key: String
        :param session_key: The session key.
        """

        self.session_key = session_key

    def get_user_id(self):
        """
        Retrieves the user id.

        :rtype: String
        :return: The user id.
        """

        return self.user_id

    def set_user_id(self, user_id):
        """
        Sets the user id.

        :type user_id: String
        :param user_id: The user id.
        """

        self.user_id = user_id

    def get_username(self):
        """
        Retrieves the username.

        :rtype: String
        :return: The username.
        """

        return self.username

    def set_username(self, username):
        """
        Sets the username.

        :type username: String
        :param username: The username.
        """

        self.username = username

    def get_consumer_id(self):
        """
        Retrieves the consumer id.

        :rtype: String
        :return: The consumer id.
        """

        return self.consumer_id

    def set_consumer_id(self, consumer_id):
        """
        Sets the consumer id.

        :type consumer_id: String
        :param consumer_id: The consumer id.
        """

        self.consumer_id = consumer_id

    def get_scope(self):
        """
        Retrieves the scope.

        :rtype: String
        :return: The scope.
        """

        return self.scope

    def set_scope(self, scope):
        """
        Sets the scope.

        :type scope: String
        :param scope: The scope.
        """

        self.scope = scope
