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

import hmac
import time
import base64
import random
import urllib
import urllib2
import hashlib
import urlparse

import service_twitter_exceptions

TWITTER_API_REALM_VALUE = "Twitter API"
""" The twitter api realm value """

TWITTER_CHARACTER_LIMIT_VALUE = 140
""" The twitter character limit value """

OAUTH_AUTHENTICATION_TYPE = 1
""" The oauth authentication type """

BASIC_AUTHENTICATION_TYPE = 2
""" The basic authentication type """

DEFAULT_OAUTH_SIGNATURE_METHOD = "HMAC-SHA1"
""" The default oauth signature method """

DEFAULT_OAUTH_VERSION = "1.0"
""" The default oauth version """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

PIN_BASED_CALLBACK_VALUE = "oob"
""" The pin based callback value """

class ServiceTwitter:
    """
    The service twitter class.
    """

    service_twitter_plugin = None
    """ The service twitter plugin """

    def __init__(self, service_twitter_plugin):
        """
        Constructor of the class.

        @type service_twitter_plugin: ServiceTwitterPlugin
        @param service_twitter_plugin: The service twitter plugin.
        """

        self.service_twitter_plugin = service_twitter_plugin

    def create_remote_client(self, service_attributes):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: TwitterClient
        @return: The created remote client.
        """

        # retrieves the json plugin
        json_plugin = self.service_twitter_plugin.json_plugin

        # retrieves the username (if available)
        username = service_attributes.get("username", None)

        # retrieves the password (if available)
        password = service_attributes.get("password", None)

        # retrieves the encoding (if available)
        encoding = service_attributes.get("encoding", None)

        # retrieves the oauth structure (if available)
        oauth_structure = service_attributes.get("oauth_structure", None)

        # creates a new twitter client with the given options
        twitter_client = TwitterClient(json_plugin, urllib2, username, password, encoding, oauth_structure)

        # returns the twitter client
        return twitter_client

class TwitterClient:
    """
    The class that represent a twitter client connection.
    """

    json_plugin = None
    """ The json plugin """

    http_client_plugin = None
    """ The http client plugin """

    username = None
    """ The username """

    password = None
    """ The password """

    encoding = None
    """ The encoding used """

    request_headers = {}
    """ The request headers """

    oauth_structure = None
    """ The oauth structure """

    def __init__(self, json_plugin = None, http_client_plugin = None, username = None, password = None, encoding = None, oauth_structure = None):
        """
        Constructor of the class.

        @type json_plugin: JsonPlugin
        @param json_plugin: The json plugin.
        @type http_client_plugin: HttpClientPlugin
        @param http_client_plugin: The http client plugin.
        @type username: String
        @param username: The username.
        @type password: String
        @param password: The password.
        @type encoding: String
        @param encoding: The encoding used.
        @type oauth_structure: OauthStructure
        @param oauth_structure: The oauth structure
        """

        self.json_plugin = json_plugin
        self.http_client_plugin = http_client_plugin
        self.username = username
        self.password = password
        self.encoding = encoding
        self.oauth_structure = oauth_structure

        self.request_header = {}

    def generate_oauth_structure(self, oauth_consumer_key, oauth_consumer_secret, oauth_signature_method = DEFAULT_OAUTH_SIGNATURE_METHOD, oauth_signature = None, oauth_timestamp = None, oauth_nonce = None, oauth_version = DEFAULT_OAUTH_VERSION, oauth_callback = PIN_BASED_CALLBACK_VALUE, set_structure = True):
        """
        Generates a new oauth structure, for the given parameters.

        @type oauth_consumer_key: String
        @param oauth_consumer_key: The consumer key.
        @type oauth_consumer_secret: String
        @param oauth_consumer_secret: The consumer secret.
        @type oauth_signature_method: String
        @param oauth_signature_method: The signature method.
        @type oauth_signature: String
        @param oauth_signature: The signature.
        @type oauth_timestamp: float
        @param oauth_timestamp: The timestamp.
        @type oauth_nonce: int
        @param oauth_nonce: The nonce.
        @type oauth_version: String
        @param oauth_version: The version.
        @type oauth_callback: Method
        @param oauth_callback: The callback.
        @type set_structure: bool
        @param set_structure: The set structure flag (if the structure should be set in the client).
        @rtype: OauthStructure
        @return: The generated oauth structure.
        """

        # constructs a new oauth structure
        oauth_structure = OauthStructure(oauth_consumer_key, oauth_consumer_secret, oauth_signature_method, oauth_signature, oauth_timestamp, oauth_nonce, oauth_version, oauth_callback)

        # in case the structure is meant to be set
        if set_structure:
            # sets the oauth structure
            self.set_oauth_structure(oauth_structure)

        # returns the oauth structure
        return oauth_structure

    def open_oauth_request_token(self):
        """
        Opens the oauth request token.

        @rtype: OauthStructure
        @return: The current oauth structure.
        """

        # sets the retrieval url
        retrieval_url = "https://twitter.com/oauth/request_token"

        # retrieves the timestamp
        oauth_timestamp = self._get_oauth_timestamp()

        # retrieves the nonce
        oauth_nonce = self._get_oauth_nonce()

        # start the parameters map
        parameters = {}

        # sets the consumer key
        parameters["oauth_consumer_key"] = self.oauth_structure.oauth_consumer_key

        # sets the signature method
        parameters["oauth_signature_method"] = self.oauth_structure.oauth_signature_method

        # sets the timestamp
        parameters["oauth_timestamp"] = oauth_timestamp

        # sets the nonce
        parameters["oauth_nonce"] = oauth_nonce

        # sets the version
        parameters["oauth_version"] = self.oauth_structure.oauth_version

        # in case callback is defined
        if self.oauth_structure.oauth_callback:
            # sets the callback
            parameters["oauth_callback"] = self.oauth_structure.oauth_callback

        if self.oauth_structure.oauth_signature:
            # sets the signature
            parameters["oauth_signature"] = self.oauth_structure.oauth_signature
        else:
            # escapes the consumer secret
            oauth_consumer_secret_escaped = "%s&" % self._escape_url(self.oauth_structure.oauth_consumer_secret)

            # creates the parameters tuple
            parameters_tuple = ["%s=%s" % (self._escape_url(key), self._escape_url(parameters[key])) for key in sorted(parameters)]

            # creates the message
            message = "&".join(map(self._escape_url, [GET_METHOD_VALUE, retrieval_url, "&".join(parameters_tuple)]))

            # sets the signature
            parameters["oauth_signature"] = hmac.new(oauth_consumer_secret_escaped, message, hashlib.sha1).digest().encode("base64")[:-1]

        # fetches the retrieval url with the given parameters retrieving the json
        result = self._fetch_url(retrieval_url, parameters)

        # retrieves the values from the request
        values = result.split("&")

        # retrieves the values list
        values_list = [value.split("=") for value in values]

        # converts the values list into a map
        values_map = dict(values_list)

        # retrieves the oauth token from the values map
        self.oauth_structure.oauth_token = values_map["oauth_token"]

        # retrieves the oauth token secret from the values map
        self.oauth_structure.oauth_token_secret = values_map["oauth_token_secret"]

        # returns the oauth structure
        return self.oauth_structure

    def open_oauth_access_token(self):
        """
        Opens the oauth access token.

        @rtype: OauthStructure
        @return: The current oauth structure.
        """

        # sets the retrieval url
        retrieval_url = "https://twitter.com/oauth/access_token"

        # retrieves the timestamp
        oauth_timestamp = self._get_oauth_timestamp()

        # retrieves the nonce
        oauth_nonce = self._get_oauth_nonce()

        # start the parameters map
        parameters = {}

        # sets the token
        parameters["oauth_token"] = self.oauth_structure.oauth_token

        # sets the consumer key
        parameters["oauth_consumer_key"] = self.oauth_structure.oauth_consumer_key

        # sets the signature method
        parameters["oauth_signature_method"] = self.oauth_structure.oauth_signature_method

        # sets the timestamp
        parameters["oauth_timestamp"] = oauth_timestamp

        # sets the nonce
        parameters["oauth_nonce"] = oauth_nonce

        # sets the version
        parameters["oauth_version"] = self.oauth_structure.oauth_version

        # in case the verifier is defined
        if self.oauth_structure.oauth_verifier:
            # sets the verifier
            parameters["oauth_verifier"] = self.oauth_structure.oauth_verifier

        if self.oauth_structure.oauth_signature:
            # sets the signature
            parameters["oauth_signature"] = self.oauth_structure.oauth_signature
        else:
            # escapes the consumer secret
            oauth_consumer_secret_escaped = "%s&%s" % (self._escape_url(self.oauth_structure.oauth_consumer_secret), self._escape_url(self.oauth_structure.oauth_token_secret))

            # creates the parameters tuple
            parameters_tuple = ["%s=%s" % (self._escape_url(key), self._escape_url(parameters[key])) for key in sorted(parameters)]

            # creates the message
            message = "&".join(map(self._escape_url, [GET_METHOD_VALUE, retrieval_url, "&".join(parameters_tuple)]))

            # sets the signature
            parameters["oauth_signature"] = hmac.new(oauth_consumer_secret_escaped, message, hashlib.sha1).digest().encode("base64")[:-1]

        # fetches the retrieval url with the given parameters retrieving the json
        result = self._fetch_url(retrieval_url, parameters)

        # retrieves the values from the request
        values = result.split("&")

        # retrieves the values list
        values_list = [value.split("=") for value in values]

        # converts the values list into a map
        values_map = dict(values_list)

        # retrieves the oauth access token from the values map
        self.oauth_structure.oauth_access_token = values_map["oauth_token"]

        # retrieves the oauth token secret from the values map
        self.oauth_structure.oauth_token_secret = values_map["oauth_token_secret"]

        # retrieves the user id from the values map
        self.oauth_structure.user_id = values_map["user_id"]

        # retrieves the screen name from the values map
        self.oauth_structure.screen_name = values_map["screen_name"]

        # returns the oauth structure
        return self.oauth_structure

    def get_oauth_authorize_url(self):
        """
        Retrieves the oauth authorize url.

        @rtype: String
        @return: The oauth authorize url.
        """

        # sets the retrieval url
        retrieval_url = "https://twitter.com/oauth/authorize"

        # creates the authentication parameters
        authentication_parameters = {"oauth_token" : self.oauth_structure.oauth_token}

        # creates the authentication url from the authentication token
        authentication_url = self._build_url(retrieval_url, authentication_parameters)

        # returns the authentication url
        return authentication_url

    def get_oauth_authenticate_url(self):
        """
        Retrieves the oauth authenticate url.

        @rtype: String
        @return: The oauth authenticate url.
        """

        # sets the retrieval url
        retrieval_url = "https://twitter.com/oauth/authenticate"

        # creates the authentication parameters
        authentication_parameters = {"oauth_token" : self.oauth_structure.oauth_token}

        # creates the authentication url from the authentication token
        authentication_url = self._build_url(retrieval_url, authentication_parameters)

        # returns the authentication url
        return authentication_url

    def get_public_timeline(self, since_id = None):
        """
        Retrieves the public timeline, since the given date id.

        @type since_id: String
        @param since_id: The date id from wich the timeline should be retrieved.
        @rtype: Dictionary
        @return: The public timeline, since the given date id.
        """

        # start the parameters map
        parameters = {}

        if since_id:
            parameters["since_id"] = since_id

        retrieval_url = "http://twitter.com/statuses/public_timeline.json"

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for twitter errors
        self._check_twitter_errors(data)

        # returns the data
        return data

    def get_home_timeline(self, since_id = None, max_id = None, count = None, page = None):
        """
        Retrieves the home timeline, since the given id, for the given maximum id, with the given count
        and the given page.

        @type since_id: String
        @param since_id: The date id from wich the timeline should be retrieved.
        @type max_id: String
        @param max_id: The maximum date if from wich the timeline should be retrieved.
        @type count: int
        @param count: The number of records to be retrieved.
        @type page: int
        @param page: The page to be retrieved.
        @rtype: Dictionary
        @return: The home timeline, for the given arguments.
        """

        # requires authentication
        self.require_authentication()

        # start the parameters map
        parameters = {}

        if since_id:
            parameters["since_id"] = since_id

        if max_id:
            parameters["max_id"] = max_id

        if count:
            parameters["count"] = count

        if page:
            parameters["page"] = page

        retrieval_url = "http://twitter.com/statuses/home_timeline.json"

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for twitter errors
        self._check_twitter_errors(data)

        # returns the data
        return data

    def get_friends_timeline(self, since_id = None, max_id = None, count = None, page = None):
        """
        Retrieves the friends timeline, since the given id, for the given maximum id, with the given count
        and the given page.

        @type since_id: String
        @param since_id: The date id from wich the timeline should be retrieved.
        @type max_id: String
        @param max_id: The maximum date if from wich the timeline should be retrieved.
        @type count: int
        @param count: The number of records to be retrieved.
        @type page: int
        @param page: The page to be retrieved.
        @rtype: Dictionary
        @return: The friends timeline, for the given arguments.
        """

        # requires authentication
        self.require_authentication()

        # start the parameters map
        parameters = {}

        if since_id:
            parameters["since_id"] = since_id

        if max_id:
            parameters["max_id"] = max_id

        if count:
            parameters["count"] = count

        if page:
            parameters["page"] = page

        retrieval_url = "http://twitter.com/statuses/friends_timeline.json"

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for twitter errors
        self._check_twitter_errors(data)

        # returns the data
        return data

    def get_user_timeline(self, user = None, since = None, since_id = None, count = None, page = None):
        """
        Retrieves the user timeline, since the given id, for the given maximum id, with the given count
        and the given page.

        @type since_id: String
        @param since_id: The date id from wich the timeline should be retrieved.
        @type max_id: String
        @param max_id: The maximum date if from wich the timeline should be retrieved.
        @type count: int
        @param count: The number of records to be retrieved.
        @type page: int
        @param page: The page to be retrieved.
        @rtype: Dictionary
        @return: The user timeline, for the given arguments.
        """

        # start the parameters map
        parameters = {}

        if since:
            parameters["since"] = since

        if since_id:
            parameters["since_id"] = since_id

        if count:
            parameters["count"] = count

        if page:
            parameters["page"] = count

        if user:
            retrieval_url = "http://twitter.com/statuses/user_timeline/%s.json" % user
        else:
            # requires authentication
            self.require_authentication()

            retrieval_url = "http://twitter.com/statuses/user_timeline.json"

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for twitter errors
        self._check_twitter_errors(data)

        # returns the data
        return data

    def get_friends(self, user = None, cursor = None, user_id = None, screen_name = None):
        """
        Retrieves the user friends, for the given user, with the given cursor,
        for the given user id and screen name.

        @type user: String
        @param user: The user for wich the friends should be retrieved.
        @type cursor: int
        @param cursor: The current cursor for retrieval.
        @type user_id: String
        @param user_id: The user id for wich the friends should be retrieved.
        @type screen_name: String
        @param screen_name: The screen name for wich the friends should be retrieved.
        @rtype: Dictionary
        @return: The user friends, for the given arguments.
        """

        # requires authentication
        self.require_authentication()

        # start the parameters map
        parameters = {}

        if cursor:
            parameters["cursor"] = cursor

        if user_id:
            parameters["user_id"] = user_id

        if screen_name:
            parameters["screen_name"] = screen_name

        # in case the user is defined
        if user:
            retrieval_url = "http://twitter.com/statuses/friends/%s.json" % user
        else:
            retrieval_url = "http://twitter.com/statuses/friends.json"

        # fetches the retrieval url retrieving the json
        json = self._fetch_url(retrieval_url, parameters)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for twitter errors
        self._check_twitter_errors(data)

        # returns the data
        return data

    def get_followers(self, user = None, cursor = None, user_id = None, screen_name = None):
        """
        Retrieves the user followers, for the given user, with the given cursor,
        for the given user id and screen name.

        @type user: String
        @param user: The user for wich the followers should be retrieved.
        @type cursor: int
        @param cursor: The current cursor for retrieval.
        @type user_id: String
        @param user_id: The user id for wich the followers should be retrieved.
        @type screen_name: String
        @param screen_name: The screen name for wich the followers should be retrieved.
        @rtype: Dictionary
        @return: The user followers, for the given arguments.
        """

        # requires authentication
        self.require_authentication()

        # start the parameters map
        parameters = {}

        if cursor:
            parameters["cursor"] = cursor

        if user_id:
            parameters["user_id"] = user_id

        if screen_name:
            parameters["screen_name"] = screen_name

        # in case the user is defined
        if user:
            retrieval_url = "http://twitter.com/statuses/followers/%s.json" % user
        else:
            retrieval_url = "http://twitter.com/statuses/followers.json"

        # fetches the retrieval url retrieving the json
        json = self._fetch_url(retrieval_url, parameters)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for twitter errors
        self._check_twitter_errors(data)

        # returns the data
        return data

    def get_user(self, user = None):
        """
        Retrieves the user information for the given user.

        @type user: String
        @param user: The user for wich the information should be retrieved.
        @rtype: Dictionary
        @return: The user information for the given user.
        """

        # in case the user is not defined
        if not user:
            # sets the user as the current user
            user = self._get_current_user()

        # sets the retrieval url
        retrieval_url = "http://twitter.com/users/show/%s.json" % user

        # fetches the retrieval url retrieving the json
        json = self._fetch_url(retrieval_url)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for twitter errors
        self._check_twitter_errors(data)

        # returns the data
        return data

    def post_update(self, status, in_reply_to_status_id = None, lat = None, long = None):
        """
        Posts an update message, with the given arguments.

        @type status: String
        @param status: The status message to be sent.
        @type in_reply_to_status_id: bool
        @param in_reply_to_status_id: If the update is a reply.
        @type lat: String
        @param lat: The latitude value to be appended to the status udapte.
        @type long: String
        @param long: The longitude value to be appended to the status udapte.
        @rtype: Dictionary
        @return: The update result value.
        """

        # requires authentication
        self.require_authentication()

        # in case the length of the status message is greater than the twitter
        # character limit value
        if len(status) > TWITTER_CHARACTER_LIMIT_VALUE:
            raise service_twitter_exceptions.StatusUpdateProblem("text must be less than or equal to %d characters" % TWITTER_CHARACTER_LIMIT_VALUE)

        # sets the status in the post data
        post_data = {"status" : status}

        if in_reply_to_status_id:
            post_data["in_reply_to_status_id"] = in_reply_to_status_id

        # sets the retrieval url
        retrieval_url = "http://twitter.com/statuses/update.json"

        # fetches the retrieval url retrieving the json
        json = self._fetch_url(retrieval_url, post_data = post_data, method = POST_METHOD_VALUE)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for twitter errors
        self._check_twitter_errors(data)

        # returns the data
        return data

    def require_authentication(self):
        """
        Tests if authentication is enabled.
        """

        if (not self.username or not self.password) and not self.oauth_structure.oauth_access_token:
            raise service_twitter_exceptions.InvalidAuthentication("user not authenticated")

    def get_oauth_structure(self):
        """
        Retrieves the oauth structure.

        @rtype: OauthStructure
        @return: The oauth structure.
        """

        return self.oauth_structure

    def set_oauth_structure(self, oauth_structure):
        """
        Sets the oauth structure.

        @type oauth_structure: OauthStructure
        @param: The oauth structure.
        """

        self.oauth_structure = oauth_structure

    def _add_authorization_header(self):
        """
        Adds the authorization handler to the request headers.
        """

        if self.username and self.password:
            # constructs the basic authentication string
            basic_authentication = base64.encodestring("%s:%s" % (self.username, self.password))[:-1]

            # sets the request header authorization
            self.request_headers["Authorization"] = "Basic %s" % basic_authentication

    def _get_opener(self, url):
        """
        Retrieves the opener to the connection.

        @type url: String
        @param url: The url to create the opener.
        @rtype: Opener
        @return: The opener to the connection.
        """

        # in case the username and the password are defined
        if self.username and self.password:
            # adds the authorization header
            self._add_authorization_header()

            # creates the http basic auth handler
            authentication_handler = urllib2.HTTPBasicAuthHandler()

            # parses the url
            _scheme, net_localization, _path, _parameters, _query, _fragment = urlparse.urlparse(url)

            # adds the password to the url structure
            authentication_handler.add_password(TWITTER_API_REALM_VALUE, net_localization, self.username, self.password)

            # builds the opener with the authentication handler
            opener = urllib2.build_opener(authentication_handler)
        else:
            # builds the opener
            opener = urllib2.build_opener()

        # adds the request header to the opener
        opener.addheaders = self.request_headers.items()

        # returns the opener
        return opener

    def _fetch_url(self, url, parameters = None, post_data = None, method = GET_METHOD_VALUE):
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

        # retrieves the current authentication type
        authentication_type = self._get_authentication_type()

        # in case oauth is in use
        if authentication_type == OAUTH_AUTHENTICATION_TYPE:
            if method == GET_METHOD_VALUE:
                self._build_oauth_arguments(url, parameters, method)
            elif method == POST_METHOD_VALUE:
                self._build_oauth_arguments(url, post_data, method)

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

    def _build_oauth_arguments(self, url, parameters, method = GET_METHOD_VALUE):
        """
        Builds the oauth arguments encoding them into the oauth message specification.

        @type url: String
        @param url: The url to be used for the oauth encoding.
        @type parameters: Dictionary
        @param parameters: The parameters to be used for the oauth encoding.
        @type method: String
        @param method: The method to be used for the oauth encoding.
        @rtype: String
        @return: The oauth arguments encoded in oauth message specification.
        """

        # retrieves the timestamp
        oauth_timestamp = self._get_oauth_timestamp()

        # retrieves the nonce
        oauth_nonce = self._get_oauth_nonce()

        # sets the token
        parameters["oauth_token"] = self.oauth_structure.oauth_access_token

        # sets the consumer key
        parameters["oauth_consumer_key"] = self.oauth_structure.oauth_consumer_key

        # sets the signature method
        parameters["oauth_signature_method"] = self.oauth_structure.oauth_signature_method

        # sets the timestamp
        parameters["oauth_timestamp"] = oauth_timestamp

        # sets the nonce
        parameters["oauth_nonce"] = oauth_nonce

        # sets the version
        parameters["oauth_version"] = self.oauth_structure.oauth_version

        if self.oauth_structure.oauth_signature:
            # sets the signature
            parameters["oauth_signature"] = self.oauth_structure.oauth_signature
        else:
            # escapes the consumer secret
            oauth_consumer_secret_escaped = "%s&%s" % (self._escape_url(self.oauth_structure.oauth_consumer_secret), self._escape_url(self.oauth_structure.oauth_token_secret))

            # creates the parameters tuple
            parameters_tuple = ["%s=%s" % (self._escape_url(key), self._escape_url(parameters[key])) for key in sorted(parameters)]

            # creates the message
            message = "&".join(map(self._escape_url, [method, url, "&".join(parameters_tuple)]))

            # sets the signature
            parameters["oauth_signature"] = hmac.new(oauth_consumer_secret_escaped, message, hashlib.sha1).digest().encode("base64")[:-1]

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

    def _escape_url(self, url_text):
        """
        Escapes the given url text into a valid http get request string.

        @rtype: String
        @return: the given url text in a valid http get request string.
        """

        return urllib.quote(str(url_text), "")

    def _check_twitter_errors(self, data):
        """
        Checks the given data for twitter errors.

        @type data: String
        @param data: The data to be checked for twitter errors.
        @rtype: bool
        @return: The result of the data error check.
        """

        pass

    def _get_authentication_type(self):
        """
        Retrieves the current authentication type being used.

        @rtype: int
        @return: The current authentication type being used.
        """

        if self.oauth_structure and self.oauth_structure.oauth_access_token:
            return OAUTH_AUTHENTICATION_TYPE
        elif self.username and self.password:
            return BASIC_AUTHENTICATION_TYPE

        return None

    def _get_oauth_timestamp(self):
        """
        Retrieves the real value for the oauth timestamp.

        @rtype: float
        @return: The real value for the oauth timestamp.
        """

        if self.oauth_structure.oauth_timestamp:
            oauth_timestamp = self.oauth_structure.oauth_token
        else:
            oauth_timestamp = int(time.time())

        return oauth_timestamp

    def _get_oauth_nonce(self):
        """
        Retrieves the real value for the oauth nonce.

        @rtype: int
        @return: the real value for the oauth nonce.
        """

        if self.oauth_structure.oauth_nonce:
            oauth_nonce = self.oauth_structure.oauth_nonce
        else:
            oauth_nonce = random.getrandbits(64)

        return oauth_nonce

    def _get_current_user(self):
        """
        Retrieves the current user.

        @rtype: String
        @return: The current user.
        """

        # retrieves the current authentication type
        authentication_type = self._get_authentication_type()

        # in case oauth is in use
        if authentication_type == OAUTH_AUTHENTICATION_TYPE:
            # returns the oauth structure screen name
            return self.oauth_structure.screen_name
        # in case basic authentication is in use
        elif authentication_type == BASIC_AUTHENTICATION_TYPE:
            # returns the username
            return self.username

class OauthStructure:
    """
    The oauth structure class.
    """

    oauth_consumer_key = None
    """ The consumer key """

    oauth_consumer_secret = None
    """ The consumer secret """

    oauth_signature_method = DEFAULT_OAUTH_SIGNATURE_METHOD
    """ The signature method """

    oauth_signature = None
    """ The signature """

    oauth_timestamp = None
    """ The timestamp """

    oauth_nonce = None
    """ The nonce """

    oauth_version = DEFAULT_OAUTH_VERSION
    """ The version """

    oauth_callback = PIN_BASED_CALLBACK_VALUE
    """ The callback """

    oauth_token = None
    """ The oauth token """

    oauth_token_secret = None
    """ The token secret """

    oauth_verifier = None
    """ The verififer """

    oauth_access_token = None
    """ The oauth access token """

    user_id = None
    """ The user id """

    screen_name = None
    """ The screen name """

    def __init__(self, oauth_consumer_key, oauth_consumer_secret, oauth_signature_method = DEFAULT_OAUTH_SIGNATURE_METHOD, oauth_signature = None, oauth_timestamp = None, oauth_nonce = None, oauth_version = DEFAULT_OAUTH_VERSION, oauth_callback = PIN_BASED_CALLBACK_VALUE):
        """
        Constructor of the class.

        @type oauth_consumer_key: String
        @param oauth_consumer_key: The consumer key.
        @type oauth_consumer_secret: String
        @param oauth_consumer_secret: The consumer secret.
        @type oauth_signature_method: String
        @param oauth_signature_method: The signature method.
        @type oauth_signature: String
        @param oauth_signature: The signature.
        @type oauth_timestamp: float
        @param oauth_timestamp: The timestamp.
        @type oauth_nonce: int
        @param oauth_nonce: The nonce.
        @type oauth_version: String
        @param oauth_version: The version.
        @type oauth_callback: Method
        @param oauth_callback: The callback.
        """

        self.oauth_consumer_key = oauth_consumer_key
        self.oauth_consumer_secret = oauth_consumer_secret
        self.oauth_signature_method = oauth_signature_method
        self.oauth_signature = oauth_signature
        self.oauth_timestamp = oauth_timestamp
        self.oauth_nonce = oauth_nonce
        self.oauth_version = oauth_version
        self.oauth_callback = oauth_callback

    def get_oauth_consumer_key(self):
        """
        Retrieves the consumer key.

        @rtype: String
        @return: The consumer key.
        """

        return self.oauth_consumer_key

    def set_oauth_consumer_key(self, oauth_consumer_key):
        """
        Sets the consumer key.

        @type oauth_consumer_key: String
        @param oauth_consumer_key: The consumer key.
        """

        self.oauth_consumer_key = oauth_consumer_key

    def get_oauth_consumer_secret(self):
        """
        Retrieves the consumer secret.

        @rtype: String
        @return: The consumer secret.
        """

        return self.oauth_consumer_secret

    def set_consumer_secret(self, oauth_consumer_secret):
        """
        Sets the consumer secret.

        @type: String
        @param: The consumer secret.
        """

        self.oauth_consumer_secret = oauth_consumer_secret

    def get_oauth_signature_method(self):
        """
        Retrieves the signature method.

        @rtype: String
        @return: The signature method.
        """

        return self.oauth_signature_method

    def set_oauth_signature_method(self, oauth_signature_method):
        """
        Sets the signature method.

        @type oauth_signature_method: String
        @param oauth_signature_method: The signature method.
        """

        self.oauth_signature_method = oauth_signature_method

    def get_oauth_signature(self):
        """
        Retrieves the signature.

        @rtype: String
        @return: The signature.
        """

        return self.oauth_signature

    def set_oauth_signature(self, oauth_signature):
        """
        Sets the signature.

        @type oauth_signature: String
        @param oauth_signature: The signature.
        """

        self.oauth_signature = oauth_signature

    def get_oauth_timestamp(self):
        """
        Retrieves the timestamp.

        @rtype: float
        @return: The timestamp.
        """

        return self.oauth_timestamp

    def set_oauth_timestamp(self, oauth_timestamp):
        """
        Sets the timestamp.

        @type oauth_timestamp: float
        @param oauth_timestamp: The timestamp
        """

        self.oauth_timestamp = oauth_timestamp

    def get_oauth_nonce(self):
        """
        Retrieves the nonce.

        @rtype: int
        @return: The nonce.
        """

        return self.oauth_nonce

    def set_oauth_nonce(self, oauth_nonce):
        """
        Sets the nonce.

        @type oauth_nonce: int
        @param oauth_nonce: The nonce.
        """

        self.oauth_nonce = oauth_nonce

    def get_oauth_version(self):
        """
        Retrieves the version.

        @rtype: String
        @return: The version.
        """

        return self.oauth_version

    def set_oauth_version(self, oauth_version):
        """
        Sets the version.

        @type oauth_version: String
        @param oauth_version: The version.
        """

        self.oauth_version = oauth_version

    def get_oauth_callback(self):
        """
        Retrieves the callback.

        @rtype: String
        @return: The callback.
        """

        return self.oauth_callback

    def set_oauth_callback(self, oauth_callback):
        """
        Sets the callback.

        @type oauth_callback: String
        @param oauth_callback: The callback.
        """

        self.oauth_callback = oauth_callback

    def get_oauth_token(self):
        """
        Retrieves the token.

        @rtype: String
        @return: The token.
        """

        return self.oauth_token

    def set_oauth_token(self, oauth_token):
        """
        Sets the token.

        @type oauth_token: String
        @param oauth_token: The token.
        """

        self.oauth_token = oauth_token

    def get_oauth_token_secret(self):
        """
        Retrieves the token secret.

        @rtype: String
        @return: The token secret.
        """

        return self.oauth_token_secret

    def set_oauth_token_secret(self, oauth_token_secret):
        """
        Sets the token secret.

        @type oauth_token_secret: String
        @param oauth_token_secret: The token secret.
        """

        self.oauth_token_secret = oauth_token_secret

    def get_oauth_verifier(self):
        """
        Retrieves the verifier.

        @rtype: String
        @return: The verifier.
        """

        return self.oauth_verifier

    def set_oauth_verifier(self, oauth_verifier):
        """
        Sets the verifier.

        @type oauth_verifier: String
        @param oauth_verifier: The verifier.
        """

        self.oauth_verifier = oauth_verifier

    def get_oauth_access_token(self):
        """
        Retrieves the access token.

        @rtype: String
        @return: The access token.
        """

        return self.oauth_access_token

    def set_oauth_access_token(self, oauth_access_token):
        """
        Sets the access token.

        @type oauth_access_token: String
        @param oauth_access_token: The access token.
        """

        self.oauth_access_token = oauth_access_token

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

    def get_screen_name(self):
        """
        Retrieves the screen name.

        @rtype: String
        @return: The screen name.
        """

        return self.screen_name

    def set_screen_name(self, screen_name):
        """
        Sets the screen name.

        @type screen_name: String
        @param screen_name: The screen name.
        """

        self.screen_name = screen_name
