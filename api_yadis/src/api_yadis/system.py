#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from . import parser

DEFAULT_CHARSET = "utf-8"
""" The default charset """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

class APIYadis(colony.System):
    """
    The API Yadis class.
    """

    def create_client(self, api_attributes, open_client = True):
        """
        Creates a client, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :type open_client: bool
        :param open_client: If the client should be opened.
        :rtype: YadisClient
        :return: The created client.
        """

        # retrieves the client HTTP plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the Yadis structure (if available)
        yadis_structure = api_attributes.get("yadis_structure", None)

        # creates a new client with the given options, opens
        # it in case it's required and returns the generated
        # client to the caller method
        yadis_client = YadisClient(client_http_plugin, yadis_structure)
        if open_client: yadis_client.open()
        return yadis_client

class YadisClient(object):
    """
    The class that represents a Yadis client connection.
    """

    client_http_plugin = None
    """ The client HTTP plugin """

    yadis_structure = None
    """ The Yadis structure """

    http_client = None
    """ The HTTP client for the connection """

    def __init__(self, client_http_plugin = None, yadis_structure = None):
        """
        Constructor of the class.

        :type client_http_plugin: ClientHTTPPlugin
        :param client_http_plugin: The client HTTP plugin.
        :type yadis_structure: YadisStructure
        :param yadis_structure: The Yadis structure.
        """

        self.client_http_plugin = client_http_plugin
        self.yadis_structure = yadis_structure

    def open(self):
        """
        Opens the Yadis client.
        """

        pass

    def close(self):
        """
        Closes the Yadis client.
        """

        # in case an HTTP client is defined
        if self.http_client:
            # closes the HTTP client
            self.http_client.close({})

    def generate_yadis_structure(self, provider_url, set_structure = True):
        """
        Generates a new Yadis structure, for the given parameters.

        :type provider_url: String
        :param provider_url: The URL of the Yadis provider.
        """

        # constructs a new Yadis structure
        yadis_structure = YadisStructure(provider_url)

        # in case the structure is meant to be set
        # sets the structure in the current instance
        if set_structure: self.set_yadis_structure(yadis_structure)

        # returns the Yadis structure
        return yadis_structure

    def get_resource_descriptor(self):
        """
        Retrieves the Yadis resource descriptor for the current
        provider URL.

        :rtype: YadisResourceDescriptor
        :return: The Yadis resource descriptor for the current
        provider URL.
        """

        # sets the retrieval URL
        retrieval_url = self.yadis_structure.provider_url

        # start the parameters map
        parameters = {}

        # fetches the retrieval URL with the given parameters retrieving the XML response
        result = self._fetch_url(retrieval_url, parameters)

        # creates a new resource descriptor parser
        resource_descriptor_parser = parser.ResourceDescriptorParser()

        # loads the Yadis contents
        resource_descriptor_parser.load_yadis_contents(result)

        # retrieves the resources list
        resources_list = resource_descriptor_parser.get_value()

        # creates the Yadis resource descriptor
        resource_descriptor = YadisResourceDescriptor(resources_list)

        # returns the Yadis resource descriptor
        return resource_descriptor

    def get_yadis_structure(self):
        """
        Retrieves the Yadis structure.

        :rtype: YadisStructure
        :return: The Yadis structure.
        """

        return self.yadis_structure

    def set_yadis_structure(self, yadis_structure):
        """
        Sets the Yadis structure.

        :type yadis_structure: YadisStructure
        :param yadis_structure: The Yadis structure.
        """

        self.yadis_structure = yadis_structure

    def _build_url(self, base_url, parameters):
        """
        Builds the URL for the given URL and parameters.

        :type base_url: String
        :param base_url: The base URL to be used.
        :type parameters: Dictionary
        :param parameters: The parameters to be used for URL construction.
        :rtype: String
        :return: The built URL for the given parameters.
        """

        # retrieves the HTTP client
        http_client = self._get_http_client()

        # build the URL from the base URL
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)

        # returns the built URL
        return url

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

    def _get_http_client(self):
        """
        Retrieves the HTTP client currently in use (in case it's created)
        if not created creates the HTTP client.

        :rtype: HTTPClient
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

class YadisStructure(object):
    """
    The Yadis structure class.
    """

    provider_url = None
    """ The URL of the OpenID provider """

    def __init__(self, provider_url):
        """
        Constructor of the class.

        :type provider_url: String
        :param provider_url: The URL of the Yadis provider.
        """

        self.provider_url = provider_url

    def get_provider_url(self):
        """
        Retrieves the provider URL.

        :rtype: String
        :return: The provider URL.
        """

        return self.provider_url

    def set_provider_url(self, provider_url):
        """
        Sets the provider URL.

        :type provider_url: String
        :param provider_url: The provider URL.
        """

        self.provider_url = provider_url

class YadisResourceDescriptor(object):
    """
    The Yadis resource descriptor class.
    """

    resources_list = []
    """ The list of Yadis resources """

    def __init__(self, resources_list):
        """
        Constructor of the class.

        :type resources_list: List
        :param resources_list: The list of Yadis resources.
        """

        self.resources_list = resources_list

    def get_resources_list(self):
        """
        Retrieves the list of Yadis resources.

        :rtype: List
        :return: The list of Yadis resources.
        """

        return self.resources_list

    def set_resources_list(self, resources_list):
        """
        Sets the list of Yadis resources.

        :type resources_list: List
        :param resources_list: The list of Yadis resources.
        """

        self.resources_list = resources_list
