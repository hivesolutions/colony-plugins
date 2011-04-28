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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

import service_yadis_parser

DEFAULT_CHARSET = "utf-8"
""" The default charset """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

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

    def create_remote_client(self, service_attributes, open_client = True):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @type open_client: bool
        @param open_client: If the client should be opened.
        @rtype: YadisClient
        @return: The created remote client.
        """

        # retrieves the main client http plugin
        main_client_http_plugin = self.service_yadis_plugin.main_client_http_plugin

        # retrieves the yadis structure (if available)
        yadis_structure = service_attributes.get("yadis_structure", None)

        # creates a new yadis client with the given options
        yadis_client = YadisClient(main_client_http_plugin, yadis_structure)

        # in case the client is meant to be open
        # open the client
        open_client and yadis_client.open()

        # returns the yadis client
        return yadis_client

class YadisClient:
    """
    The class that represents a yadis client connection.
    """

    main_client_http_plugin = None
    """ The main client http plugin """

    yadis_structure = None
    """ The yadis structure """

    http_client = None
    """ The http client for the connection """

    def __init__(self, main_client_http_plugin = None, yadis_structure = None):
        """
        Constructor of the class.

        @type main_client_http_plugin: MainClientHttpPlugin
        @param main_client_http_plugin: The main client http plugin.
        @type yadis_structure: YadisStructure
        @param yadis_structure: The yadis structure.
        """

        self.main_client_http_plugin = main_client_http_plugin
        self.yadis_structure = yadis_structure

    def open(self):
        """
        Opens the yadis client.
        """

        pass

    def close(self):
        """
        Closes the yadis client.
        """

        # in case an http client is defined
        if self.http_client:
            # closes the http client
            self.http_client.close({})

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

        # creates a new resource descriptor parser
        resource_descriptor_parser = service_yadis_parser.ResourceDescriptorParser()

        # loads the yadis contents
        resource_descriptor_parser.load_yadis_contents(result)

        # retrieves the resources list
        resources_list = resource_descriptor_parser.get_value()

        # creates the yadis resource descriptor
        resource_descriptor = YadisResourceDescriptor(resources_list)

        # returns the yadis resource descriptor
        return resource_descriptor

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

    def _build_url(self, base_url, parameters):
        """
        Builds the url for the given url and parameters.

        @type base_url: String
        @param base_url: The base url to be used.
        @type parameters: Dictionary
        @param parameters: The parameters to be used for url construction.
        @rtype: String
        @return: The built url for the given parameters.
        """

        # retrieves the http client
        http_client = self._get_http_client()

        # build the url from the base urtl
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)

        # returns the built url
        return url

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

    def _get_http_client(self):
        """
        Retrieves the http client currently in use (in case it's created)
        if not created creates the http client.

        @rtype: HttpClient
        @return: The retrieved http client.
        """

        # in case no http client exists
        if not self.http_client:
            # defines the client parameters
            client_parameters = {
                CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET
            }

            # creates the http client
            self.http_client = self.main_client_http_plugin.create_client(client_parameters)

            # opens the http client
            self.http_client.open({})

        # returns the http client
        return self.http_client

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

class YadisResourceDescriptor:
    """
    The yadis resource descriptor class.
    """

    resources_list = []
    """ The list of yadis resources """

    def __init__(self, resources_list):
        """
        Constructor of the class.

        @type resources_list: List
        @param resources_list: The list of yadis resources.
        """

        self.resources_list = resources_list

    def get_resources_list(self):
        """
        Retrieves the list of yadis resources.

        @rtype: List
        @return: The list of yadis resources.
        """

        return self.resources_list

    def set_resources_list(self, resources_list):
        """
        Sets the list of yadis resources.

        @type resources_list: List
        @param resources_list: The list of yadis resources.
        """

        self.resources_list = resources_list
