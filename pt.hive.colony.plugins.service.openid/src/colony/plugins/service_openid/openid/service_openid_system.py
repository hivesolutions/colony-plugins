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

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

OPENID_NAMESPACE_VALUE = "http://specs.openid.net/auth/2.0"
""" The openid namespace value """

class ServiceOpenid:
    """
    The service openid class.
    """

    service_openid_plugin = None
    """ The service openid plugin """

    def __init__(self, service_openid_plugin):
        """
        Constructor of the class.

        @type service_openid_plugin: ServiceOpenidPlugin
        @param service_openid_plugin: The service openid plugin.
        """

        self.service_openid_plugin = service_openid_plugin

    def create_remote_client(self, service_attributes):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: OpenidClient
        @return: The created remote client.
        """

        # @todo: REMOVER ISTO QUE NAO E NECESSARIO !!!
        openid_structure = OpenidStructure()

        # creates the openid client
        openid_client = OpenidClient(openid_structure)

        # returns the openid client
        return openid_client

class OpenidServer:
    """
    The class that represents an openid server connection.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

class OpenidClient:
    """
    The class that represents an openid client connection.
    """

    openid_structure = None
    """ The openid structure """

    def __init__(self, openid_structure):
        """
        Constructor of the class.

        @type openid_structure: OpenidStructure
        @param openid_structure: The openid structure.
        """

        self.openid_structure = openid_structure

    def openid_associate(self):
        """
        Requests an association (associate mode) according to the
        openid specification.

        @rtype: OpenidStructure
        @return: The current openid structure.
        """

        # sets the retrieval url
        retrieval_url = "http://localhost/myid/MyID.config.php"

        # start the parameters map
        parameters = {}

        # sets the namespace
        parameters["openid.ns"] = OPENID_NAMESPACE_VALUE

        # sets the mode as associate
        parameters["openid.mode"] = "associate"

        parameters["openid.assoc_type"] = "HMAC-SHA1"

        parameters["openid.session_type"] = "no-encryption"

        # fetches the retrieval url with the given parameters retrieving the json
        result = self._fetch_url(retrieval_url, parameters, method = POST_METHOD_VALUE)

        # strips the result value
        result = result.strip()

        # retrieves the values from the request
        values = result.split("\n")

        # retrieves the values list
        values_list = [value.split(":") for value in values]

        # converts the values list into a map
        values_map = dict(values_list)

        # retrieves the association type from the values map
        self.openid_structure.assoc_type = values_map["assoc_type"]

        # retrieves the expiration from the values map
        self.openid_structure.expires_in = values_map["expires_in"]

        # retrieves the association handle from the values map
        self.openid_structure.assoc_handle = values_map["assoc_handle"]

        # retrieves the mac key from the values map
        self.openid_structure.mac_key = values_map["mac_key"]

        # returns the openid structure
        return self.openid_structure

    def get_request_url(self):
        """
        Retrieves the request url according to the
        openid specification.

        @rtype: String
        @return: The request url.
        """

        # sets the retrieval url
        retrieval_url = "http://localhost/myid/MyID.config.php"

        # start the parameters map
        parameters = {}

        # sets the namespace
        parameters["openid.ns"] = OPENID_NAMESPACE_VALUE

        # sets the mode as checkid setup
        parameters["openid.mode"] = "checkid_setup"
        #parameters["openid.mode"] = "checkid_immediate"

        parameters["openid.claimed_id"] = self.openid_structure.claimed_id

        parameters["openid.identity"] = self.openid_structure.claimed_id

        parameters["openid.assoc_handle"] = self.openid_structure.assoc_handle

        parameters["openid.return_to"] = "http://localhost:8080/take_the_bill/openid"

        parameters["openid.realm"] = "http://localhost:8080"

        # creates the request url from the parameters
        request_url = self._build_url(retrieval_url, parameters)

        # returns the request url
        return request_url

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

class OpenidStructure:
    pass
