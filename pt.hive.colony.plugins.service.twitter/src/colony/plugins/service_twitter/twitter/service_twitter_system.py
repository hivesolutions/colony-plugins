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

import base64
import urllib
import urllib2
import urlparse

import service_twitter_exceptions

TWITTER_API_REALM_VALUE = "Twitter API"
""" The twitter api realm value """

TWITTER_CHARACTER_LIMIT_VALUE = 140
""" The twitter character limit value """

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

        # creates a new twitter client with the given options
        twitter_client = TwitterClient(json_plugin, urllib2, username, password, encoding)

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

    def __init__(self, json_plugin = None, http_client_plugin = None, username = None, password = None, encoding = None):
        self.json_plugin = json_plugin
        self.http_client_plugin = http_client_plugin
        self.username = username
        self.password = password
        self.encoding = encoding

        self.request_header = {}

    def get_public_timeline(self, since_id = None):
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

        retrieval_url = "http://twitter.com/statuses/friends_timeline.format"

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for twitter errors
        self._check_twitter_errors(data)

        # returns the data
        return data

    def get_user_timeline(self, user = None, since = None, since_id = None, count = None, page = None):
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

    def get_user(self, user):
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
        # requires authentication
        self.require_authentication()

        # in case the length of the status message is greater than the twitter
        # character limit value
        if len(status) > TWITTER_CHARACTER_LIMIT_VALUE:
            raise Exception("text must be less than or equal to %d characters" % TWITTER_CHARACTER_LIMIT_VALUE)

        # sets the status in the post data
        post_data = {"status" : status}

        if in_reply_to_status_id:
            post_data["in_reply_to_status_id"] = in_reply_to_status_id

        # sets the retrieval url
        retrieval_url = "http://twitter.com/statuses/update.json"

        # fetches the retrieval url retrieving the json
        json = self._fetch_url(retrieval_url, post_data = post_data)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for twitter errors
        self._check_twitter_errors(data)

        # returns the data
        return data

    def require_authentication(self):
        if not self.username or not self.password:
            raise service_twitter_exceptions.InvalidAuthentication("user not authenticated")

    def _add_authorization_header(self):
        if self.username and self.password:
            # constructs the basic authentication string
            basic_authentication = base64.encodestring("%s:%s" % (self.username, self.password))[:-1]

            # sets the request header authorization
            self.request_headers["Authorization"] = "Basic %s" % basic_authentication

    def _get_opener(self, url):
        # in case the username and the password are defined
        if self.username and self.password:
            # adds the authorization header
            self._add_authorization_header()

            # creates the http basic auth handler
            authentication_handler = urllib2.HTTPBasicAuthHandler()

            # parses the url
            scheme, net_localization, path, parameters, query, fragment = urlparse.urlparse(url)

            # adds the password to the url structure
            authentication_handler.add_password(TWITTER_API_REALM_VALUE, net_localization, self.username, self.password)

            opener = urllib2.build_opener(authentication_handler)
        else:
            opener = urllib2.build_opener()

        opener.addheaders = self.request_headers.items()

        return opener

    def _fetch_url(self, url, parameters = {}, post_data = {}):
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
        if parameters and len(parameters) > 0:
            # retrieves the extra query
            extra_query = self._encode_parameters(parameters)

            # adds it to the url
            url += "?" + extra_query

        return url

    def _encode_parameters(self, parameters):
        if parameters is None:
            return None
        else:
            return urllib.urlencode(dict([(parameter_key, self._encode(parameter_value)) for parameter_key, parameter_value in parameters.items() if parameter_value is not None]))

    def _encode_post_data(self, post_data):
        if post_data is None:
            return None
        else:
            return urllib.urlencode(dict([(post_data_key, self._encode(post_data_value)) for post_data_key, post_data_value in post_data.items()]))

    def _encode(self, string_value):
        return unicode(string_value).encode("utf-8")

    def _check_twitter_errors(self, data):
        pass
