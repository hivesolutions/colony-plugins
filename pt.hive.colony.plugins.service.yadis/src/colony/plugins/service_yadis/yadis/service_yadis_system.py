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

import service_yadis_exceptions

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

class ServiceYadis:
    """
    The service yadis class.
    """

    service_yadis_plugin = None
    """ The service yadis plugin """

    def __init__(self, service_yadis_plugin):
        """
        Constructor of the class.

        @type service_yadis_plugin: ServiceYadisPlugin
        @param service_yadis_plugin: The service yadis plugin.
        """

        self.service_yadis_plugin = service_yadis_plugin

    def create_remote_client(self, service_attributes):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: YadisClient
        @return: The created remote client.
        """

        # retrieves the yadis structure (if available)
        yadis_structure = service_attributes.get("yadis_structure", None)

        # creates a new yadis client with the given options
        yadis_client = YadisClient(urllib2, yadis_structure)

        # returns the yadis client
        return yadis_client

class YadisClient:
    """
    The class that represents a yadis client connection.
    """

    http_client_plugin = None
    """ The http client plugin """

    yadis_structure = None
    """ The yadis structure """

    def __init__(self, http_client_plugin = None, yadis_structure = None):
        """
        Constructor of the class.

        @type http_client_plugin: HttpClientPlugin
        @param http_client_plugin: The http client plugin.
        @type yadis_structure: YadisStructure
        @param yadis_structure: The yadis structure.
        """

        self.http_client_plugin = http_client_plugin
        self.yadis_structure = yadis_structure

    def generate_yadis_structure(self, provider_url, set_structure = True):
        """
        Generates a new yadis structure, for the given parameters.

        @type provider_url: String
        @param provider_url: The url of the yadis provider.
        """

        # constructs a new yadis structure
        yadis_structure = YadisStructure(provider_url)

        # in case the structure is meant to be set
        if set_structure:
            # sets the yadis structure
            self.set_yadis_structure(yadis_structure)

        # returns the yadis structure
        return yadis_structure

    def get_resource_descriptor(self):
        """
        Retrieves the yadis resource descriptor for the current
        provider url.

        @rtype: YadisResourceDescriptor
        @return: The yadis resource descriptor for the current
        provider url.
        """

        # sets the retrieval url
        retrieval_url = self.yadis_structure.provider_url

        # start the parameters map
        parameters = {}

        # fetches the retrieval url with the given parameters retrieving the xml response
        result = self._fetch_url(retrieval_url, parameters)

        print result

        # retrieves the values from the request
#        values = result.split("&")
#
#        # retrieves the values list
#        values_list = [value.split("=", 1) for value in values]
#
#        # converts the values list into a map
#        values_map = dict(values_list)
#
#        # retrieves the yadis token from the values map
#        self.yadis_structure.yadis_token = values_map["yadis_token"]
#
#        # retrieves the yadis token secret from the values map
#        self.yadis_structure.yadis_token_secret = values_map["yadis_token_secret"]

        # returns the yadis structure
        return self.yadis_structure

    def get_yadis_structure(self):
        """
        Retrieves the yadis structure.

        @rtype: YadisStructure
        @return: The yadis structure.
        """

        return self.yadis_structure

    def set_yadis_structure(self, yadis_structure):
        """
        Sets the yadis structure.

        @type yadis_structure: YadisStructure
        @param yadis_structure: The yadis structure.
        """

        self.yadis_structure = yadis_structure

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

class YadisStructure:
    """
    The yadis structure class.
    """

    provider_url = None
    """ The url of the openid provider """

    def __init__(self, provider_url):
        """
        Constructor of the class.

        @type provider_url: String
        @param provider_url: The url of the yadis provider.
        """

        self.provider_url = provider_url

    def get_provider_url(self):
        """
        Retrieves the provider url.

        @rtype: String
        @return: The provider url.
        """

        return self.provider_url

    def set_provider_url(self, provider_url):
        """
        Sets the provider url.

        @type provider_url: String
        @param provider_url: The provider url.
        """

        self.provider_url = provider_url
