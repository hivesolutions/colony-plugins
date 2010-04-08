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

import urllib
import urllib2
import hashlib

import colony.libs.string_buffer_util

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

API_VERSION = "1.0"
""" The facebook api version """

BASE_REST_URL = "http://api.facebook.com/restserver.php"
""" The base rest url to be used """

BASE_REST_SECURE_URL = "https://api.facebook.com/restserver.php"
""" The base rest secure url to be used """

BASE_HOME_URL = "http://www.facebook.com/"
""" The base home url """

BASE_HOME_SECURE_URL = "https://www.facebook.com/"
""" The base home secure url """

API_KEY = "b42e59dee7e7b07258dfc82913648e43"
""" The api key """

API_SECRET = "6fddb2bbaade579798f45b1134865f01"
""" The api secret """

class ServiceFacebook:
    """
    The service facebook class.
    """

    service_facebbok_plugin = None
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

        # retrieves the json plugin
        json_plugin = self.service_facebook_plugin.json_plugin

        # retrieves the facebook structure (if available)
        facebook_structure = service_attributes.get("facebook_structure", None)

        # creates a new facebook client with the given options
        facebook_client = FacebookClient(json_plugin, urllib2, facebook_structure)

        # returns the facebook client
        return facebook_client

class FacebookClient:
    """
    The class that represents a facebook client connection.
    """

    json_plugin = None
    """ The json plugin """

    http_client_plugin = None
    """ The http client plugin """

    facebook_structure = None
    """ The facebook structure """

    def __init__(self, json_plugin = None, http_client_plugin = None, facebook_structure = None):
        """
        Constructor of the class.

        @type json_plugin: JsonPlugin
        @param json_plugin: The json plugin.
        @type http_client_plugin: HttpClientPlugin
        @param http_client_plugin: The http client plugin.
        @type facebook_structure: FacebookStructure
        @param facebook_structure: The facebook structure.
        """

        self.json_plugin = json_plugin
        self.http_client_plugin = http_client_plugin
        self.facebook_structure = facebook_structure

    def generate_facebook_structure(self, set_structure = True):
        # creates a new facebook structure
        facebook_structure = FacebookStructure()

        # in case the structure is meant to be set
        if set_structure:
            # sets the facebook structure
            self.set_facebook_structure(facebook_structure)

        # returns the facebook structure
        return facebook_structure

    def auth_create_token(self):
        # sets the retrieval url
        retrieval_url = BASE_REST_SECURE_URL

        # start the parameters map
        parameters = {}

        # sets the method
        parameters["method"] = "Auth.createToken"

        # sets the api key
        parameters["api_key"] = API_KEY

        # sets the version (v)
        parameters["v"] = API_VERSION

        parameters["format"] = "json"

        parameters["sig"] = self._get_signature(parameters)

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters, method = POST_METHOD_VALUE)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # sets the token in the facebook structure
        self.facebook_structure.token = data

    def auth_get_session(self):
        # sets the retrieval url
        retrieval_url = BASE_REST_SECURE_URL

        # start the parameters map
        parameters = {}

        # sets the method
        parameters["method"] = "Auth.getSession"

        # sets the api key
        parameters["api_key"] = API_KEY

        # sets the version (v)
        parameters["v"] = API_VERSION

        parameters["auth_token"] = self.facebook_structure.token

        parameters["format"] = "json"

        parameters["sig"] = self._get_signature(parameters)

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters, method = POST_METHOD_VALUE)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

    def get_login_url(self):
        # sets the retrieval url
        retrieval_url = BASE_HOME_SECURE_URL + "login.php"

        # start the parameters map
        parameters = {}

        # sets the api key
        parameters["api_key"] = API_KEY

        # sets the version (v)
        parameters["v"] = API_VERSION

        # sets the next web site to redirect
        parameters["next"] = "http://localhost:8080/take_the_bill/facebook"

        # creates the login url from the parameters
        login_url = self._build_url(retrieval_url, parameters)

        # returns the login url
        return login_url

    def _get_signature(self, parameters):
        # creates the message string buffer
        message_string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # retrieves the parameters keys
        parameters_keys = parameters.keys()

        # sorts the parameters keys
        parameters_keys.sort()

        for parameter_key in parameters_keys:
            parameter_value = parameters[parameter_key]

            message_string_buffer.write(parameter_key + "=" + str(parameter_value))

        message_string_buffer.write(API_SECRET)

        message = message_string_buffer.get_value()

        return hashlib.md5(message).hexdigest()

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

    def _get_opener(self, url):
        """
        Retrieves the opener to the connection.

        @type url: String
        @param url: The url to create the opener.
        @rtype: Opener
        @return: The opener to the connection.
        """

        # builds the opener
        opener = urllib2.build_opener()

        # returns the opener
        return opener

    def _fetch_url(self, url, parameters = None, post_data = None, method = GET_METHOD_VALUE, headers = False):
        """
        Fetches the given url for the given parameters, post data and using the given method.

        @type url: String
        @param url: The url to be fetched.
        @type parameters: Dictionary
        @param parameters: The parameters to be used the fetch.
        @type post_data: Dictionary
        @param post_data: The post data to be used the fetch.
        @type method: String
        @param method: The method to be used in the fetch.
        @type headers: bool
        @param headers: If the headers should be returned.
        @rtype: String
        @return: The fetched data.
        """

        # in case parameters is not defined
        if not parameters:
            # creates a new parameters map
            parameters = {}

        # in case post data is not defined
        if not post_data:
            # creates a new post data map
            post_data = {}

        if method == GET_METHOD_VALUE:
            pass
        elif method == POST_METHOD_VALUE:
            post_data = parameters

        # builds the url
        url = self._build_url(url, parameters)

        # encodes the post data
        encoded_post_data = self._encode_post_data(post_data)

        # retrieves the opener for the given url
        opener = self._get_opener(url)

        # opens the url with the given encoded post data
        url_structure = opener.open(url, encoded_post_data)

        # reads the contents from the url structure
        contents = url_structure.read()

        # in case the headers flag is set
        if headers:
            # creates the headers map
            headers_map = dict(url_structure.info().items())

            # returns the contents and the headers map
            return contents, headers_map
        else:
            # returns the contents
            return contents

    def _build_url(self, url, parameters):
        """
        Builds the url for the given url and parameters.

        @type url: String
        @param url: The base url to be used.
        @type parameters: Dictionary
        @param parameters: The parameters to be used for url construction.
        @rtype: String
        @return: The built url for the given parameters.
        """

        # in case the parameters are valid and the length
        # of them is greater than zero
        if parameters and len(parameters) > 0:
            # retrieves the extra query
            extra_query = self._encode_parameters(parameters)

            # adds it to the url
            url += "?" + extra_query

        # returns the url
        return url

    def _encode_parameters(self, parameters):
        """
        Encodes the given parameters into url encoding.

        @type parameters: Dictionary
        @param parameters: The parameters map to be encoded.
        @rtype: String
        @return: The encoded parameters.
        """

        # in case the parameters are defined
        if parameters:
            # returns the encoded parameters
            return urllib.urlencode(dict([(parameter_key, self._encode(parameter_value)) for parameter_key, parameter_value in parameters.items() if parameter_value is not None]))
        else:
            # returns none
            return None

    def _encode_post_data(self, post_data):
        """
        Encodes the post data into url encoding.

        @type post_data: Dictionary
        @param post_data: The post data map to be encoded.
        @rtype: String
        @return: The encoded post data.
        """

        # in case the post data is defined
        if post_data:
            # returns the encoded post data
            return urllib.urlencode(dict([(post_data_key, self._encode(post_data_value)) for post_data_key, post_data_value in post_data.items()]))
        else:
            # returns none
            return None

    def _encode(self, string_value):
        """
        Encodes the given string value to the current encoding.

        @type string_value: String
        @param string_value: The string value to be encoded.
        @rtype: String
        @return: The given string value encoded in the current encoding.
        """

        return unicode(string_value).encode("utf-8")

class FacebookStructure:
    """
    The facebook structure class.
    """

    token = None
    """ The authentication token used """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def get_token(self):
        """
        Retrieves the token.

        @rtype: String
        @return: The token
        """

        return self.token

    def set_token(self, token):
        """
        Sets the token.

        @type token: String
        @param token: The token
        """

        self.token = token
