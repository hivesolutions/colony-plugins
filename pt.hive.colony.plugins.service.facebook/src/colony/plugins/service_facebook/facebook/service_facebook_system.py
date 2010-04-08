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

        # creates a new facebook client with the given options
        facebook_client = FacebookClient(json_plugin, urllib2)

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


    def __init__(self, json_plugin = None, http_client_plugin = None, username = None, password = None, encoding = None, oauth_structure = None):
        """
        Constructor of the class.

        @type json_plugin: JsonPlugin
        @param json_plugin: The json plugin.
        @type http_client_plugin: HttpClientPlugin
        @param http_client_plugin: The http client plugin.
        """

        self.json_plugin = json_plugin
        self.http_client_plugin = http_client_plugin
