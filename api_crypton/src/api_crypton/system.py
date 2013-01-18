#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import base64

import colony.base.system

DEFAULT_CHARSET = "utf-8"
""" The default charset """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

class ApiCrypton(colony.base.system.System):
    """
    The api crypton class.
    """

    def create_client(self, api_attributes, open_client = True):
        """
        Creates a client, with the given api attributes.

        @type api_attributes: Dictionary
        @param api_attributes: The api attributes to be used.
        @type open_client: bool
        @param open_client: If the client should be opened.
        @rtype: CryptonClient
        @return: The created client.
        """

        # retrieves the client http plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the crypton structure (if available)
        crypton_structure = api_attributes.get("crypton_structure", None)

        # creates the crypton client
        crypton_client = CryptonClient(client_http_plugin, crypton_structure)

        # in case the client is meant to be open
        # opens the client
        crypton_client and crypton_client.open()

        # returns the crypton client
        return crypton_client

class CryptonClient:
    """
    The class that represents a crypton client connection.
    """

    client_http_plugin = None
    """ The client http plugin """

    crypton_structure = None
    """ The crypton structure """

    http_client = None
    """ The http client for the connection """

    def __init__(self, client_http_plugin = None, crypton_structure = None):
        """
        Constructor of the class.

        @type client_http_plugin: ClientHttpPlugin
        @param client_http_plugin: The client http plugin.
        @type crypton_structure: CryptonStructure
        @param crypton_structure: The crypton structure.
        """

        self.client_http_plugin = client_http_plugin
        self.crypton_structure = crypton_structure

    def open(self):
        """
        Opens the crypton client.
        """

        pass

    def close(self):
        """
        Closes the crypton client.
        """

        # in case an http client is defined
        if self.http_client:
            # closes the http client
            self.http_client.close({})

    def generate_crypton_structure(self, base_url, api_key, key_name, set_structure = True):
        """
        Generates the crypton structure for the given arguments.

        @type base_url: String
        @param base_url: The base url of the crypton provider.
        @type api_key: String
        @param api_key: The key to be used to access the remote api.
        @type key_name: String
        @param key_name: The name of the key to be used.
        @type set_structure: bool
        @param set_structure: If the structure should be
        set in the crypton client.
        @rtype: CryptonStructure
        @return: The generated crypton structure.
        """

        # creates a new crypton structure
        crypton_structure = CryptonStructure(base_url, api_key, key_name)

        # in case the structure is meant to be set
        if set_structure:
            # sets the crypton structure
            self.set_crypton_structure(crypton_structure)

        # returns the crypton structure
        return crypton_structure
    
    def encrypt(self, message):
        # retrieves the base url
        base_url = self.crypton_structure.base_url

        # sets the retrieval url
        retrieval_url = base_url + "encrypt"

        # encodes the message in base 64
        message_base_64 = base64.b64encode(message)

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # sets the message
        parameters["message"] = message_base_64

        # fetches the retrieval url with the given parameters
        # retrieving the (encrypted) message
        message_e = self._fetch_url(retrieval_url, parameters)

        # returns the (encrypted) message
        return message_e

    def decrypt(self, message_e):
        # retrieves the base url
        base_url = self.crypton_structure.base_url

        # sets the retrieval url
        retrieval_url = base_url + "decrypt"

        # encodes the message in base 64
        message_base_64 = base64.b64encode(message_e)

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # sets the message
        parameters["message_e"] = message_base_64

        # fetches the retrieval url with the given parameters
        # retrieving the (decrypted) message
        message = self._fetch_url(retrieval_url, parameters)

        # returns the (decrypted) message
        return message
    
    def sign(self, message, algorithm_name = None):
        # retrieves the base url
        base_url = self.crypton_structure.base_url

        # sets the retrieval url
        retrieval_url = base_url + "sign"

        # encodes the message in base 64
        message_base_64 = base64.b64encode(message)

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # sets the message
        parameters["message"] = message_base_64

        # in case the algorithm name is defined
        if algorithm_name:
            # sets the algorithm name
            parameters["algorithm_name"] = algorithm_name

        # fetches the retrieval url with the given parameters retrieving the signature
        signature = self._fetch_url(retrieval_url, parameters)

        # returns the signature
        return signature
    
    def verify(self, signature, message):
        # retrieves the base url
        base_url = self.crypton_structure.base_url

        # sets the retrieval url
        retrieval_url = base_url + "verify"

        # encodes the message in base 64
        message_base_64 = base64.b64encode(message)

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # sets the signature
        parameters["signature"] = signature

        # sets the message
        parameters["message"] = message_base_64

        # fetches the retrieval url with the given parameters retrieving the signature
        return_value = self._fetch_url(retrieval_url, parameters)

        # returns the return value
        return return_value

    def get_crypton_structure(self):
        """
        Retrieves the crypton structure.

        @rtype: CryptonStructure
        @return: The crypton structure.
        """

        return self.crypton_structure

    def set_crypton_structure(self, crypton_structure):
        """
        Sets the crypton structure.

        @type crypton_structure: CryptonStructure
        @param crypton_structure: The crypton structure.
        """

        self.crypton_structure = crypton_structure

    def _set_base_parameters(self, parameters):
        """
        Sets the base crypton rest request parameters
        in the parameters map.

        @type parameters: Dictionary
        @param parameters: The parameters map to be used in setting
        the base parameters.
        """

        # sets the api key
        parameters["api_key"] = self.crypton_structure.api_key

        # sets the key name
        parameters["key_name"] = self.crypton_structure.key_name

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
            self.http_client = self.client_http_plugin.create_client({})

            # opens the http client
            self.http_client.open({})

        # returns the http client
        return self.http_client

class CryptonStructure:
    """
    The crypton structure class.
    """

    base_url = None
    """ The base url of the crypton provider """

    api_key = None
    """ The key to be used to access the remote api """

    key_name = None
    """ The name of the key to be used """

    def __init__(self, base_url, api_key, key_name):
        """
        Constructor of the class.

        @type base_url: String
        @param base_url: The base url of the crypton provider.
        @type api_key: String
        @param api_key: The key to be used to access the remote api.
        @type key_name: String
        @param key_name: The name of the key to be used.
        """

        self.base_url = base_url
        self.api_key = api_key
        self.key_name = key_name

    def get_base_url(self):
        """
        Retrieves the base url.

        @rtype: String
        @return: The base url.
        """

        return self.base_url

    def set_base_url(self, base_url):
        """
        Sets the base url.

        @type base_url: String
        @param base_url: The base url.
        """

        self.base_url = base_url

    def get_api_key(self):
        """
        Retrieves the api key.

        @rtype: String
        @return: The api key.
        """

        return self.api_key

    def set_api_key(self, api_key):
        """
        Sets the api key.

        @type api_key: String
        @param api_key: The api key.
        """

        self.api_key = api_key

    def get_key_name(self):
        """
        Retrieves the key name.

        @rtype: String
        @return: The key name.
        """

        return self.key_name

    def set_key_name(self, key_name):
        """
        Sets the key name.

        @type key_name: String
        @param key_name: The key name.
        """

        self.key_name = key_name
