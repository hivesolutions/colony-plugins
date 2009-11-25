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

import urllib2

import service_twitter_exceptions

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

        # retrieves the request headers (if available)
        request_headers = service_attributes.get("request_headers", None)

        # creates a new twitter client with the given options
        twitter_client = TwitterClient(json_plugin, urllib2, username, password, encoding, request_headers)

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

    request_headers = None
    """ The request headers """

    def __init__(self, json_plugin = None, http_client_plugin = None, username = None, password = None, encoding = None, request_headers = None):
        self.json_plugin = json_plugin
        self.http_client_plugin = http_client_plugin
        self.username = username
        self.password = password
        self.encoding = encoding
        self.request_header = request_headers

    def get_friends(self, user = None, page = None):
        # requires authentication
        self.require_authentication()

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

    def require_authentication(self):
        if not self.username or not self.password:
            raise service_twitter_exceptions.InvalidAuthentication("user not authenticated")

    def _fetch_url(self, url):
        # opens the url
        url_structure = urllib2.urlopen(url)

        # reads the contents from the url structure
        contents = url_structure.read()

        # returns the contents
        return contents

    def _check_twitter_errors(self, data):
        pass
