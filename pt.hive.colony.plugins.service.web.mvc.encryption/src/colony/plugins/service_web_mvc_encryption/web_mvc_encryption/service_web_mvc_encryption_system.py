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

DEFAULT_CHARSET = "utf-8"
""" The default charset """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

DEFAULT_API_VERSION = "1.0"
""" The default web mvc encryption api version """

class ServiceWebMvcEncryption:
    """
    The service web mvc encryption class.
    """

    service_web_mvc_encryption_plugin = None
    """ The service web mvc encryption plugin """

    def __init__(self, service_web_mvc_encryption_plugin):
        """
        Constructor of the class.

        @type service_web_mvc_encryption_plugin: ServiceWebMvcEncryptionPlugin
        @param service_web_mvc_encryption_plugin: The service web mvc encryption plugin.
        """

        self.service_web_mvc_encryption_plugin = service_web_mvc_encryption_plugin

    def create_remote_client(self, service_attributes, open_client = True):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @type open_client: bool
        @param open_client: If the client should be opened.
        @rtype: OpenidClient
        @return: The created remote client.
        """

        # retrieves the main client http plugin
        main_client_http_plugin = self.service_web_mvc_encryption_plugin.main_client_http_plugin

        # retrieves the web mvc encryption structure (if available)
        web_mvc_encryption_structure = service_attributes.get("web_mvc_encryption_structure", None)

        # creates the web mvc encryption client
        web_mvc_encryption_client = WebMvcEncryptionClient(main_client_http_plugin, web_mvc_encryption_structure)

        # in case the client is meant to be open
        # opens the client
        web_mvc_encryption_client and web_mvc_encryption_client.open()

        # returns the web mvc encryption client
        return web_mvc_encryption_client

class WebMvcEncryptionClient:
    """
    The class that represents a web mvc encryption client connection.
    """

    main_client_http_plugin = None
    """ The main client http plugin """

    web_mvc_encryption_structure = None
    """ The web mvc encryption structure """

    http_client = None
    """ The http client for the connection """

    def __init__(self, main_client_http_plugin = None, web_mvc_encryption_structure = None):
        """
        Constructor of the class.

        @type main_client_http_plugin: MainClientHttpPlugin
        @param main_client_http_plugin: The main client http plugin.
        @type web_mvc_encryption_structure: WebMvcEncryptionStructure
        @param web_mvc_encryption_structure: The web mvc encryption structure.
        """

        self.main_client_http_plugin = main_client_http_plugin
        self.web_mvc_encryption_structure = web_mvc_encryption_structure

    def open(self):
        """
        Opens the web mvc encryption client.
        """

        pass

    def close(self):
        """
        Closes the web mvc encryption client.
        """

        # in case an http client is defined
        if self.http_client:
            # closes the http client
            self.http_client.close({})

    def generate_web_mvc_encryption_structure(self, username, cin, country, language, api_version = DEFAULT_API_VERSION, set_structure = True):
        """
        Generates the web mvc encryption structure for the given arguments.

        @type username: String
        @param username: The username.
        @type cin: String
        @param cin: The cin.
        @type country: String
        @param country: The two letter string representing the
        country to be used.
        @type language: String
        @param language: The two letter string representing the
        language to be used.
        @type api_version: String
        @param api_version: The version of the api being used.
        @type set_structure: bool
        @param set_structure: If the structure should be
        set in the web mvc encryption client.
        @rtype: WebMvcEncryptionStructure
        @return: The generated web mvc encryption structure.
        """

        # creates a new web mvc encryption structure
        web_mvc_encryption_structure = WebMvcEncryptionStructure(username, cin, country, language, api_version)

        # in case the structure is meant to be set
        if set_structure:
            # sets the web mvc encryption structure
            self.set_web_mvc_encryption_structure(web_mvc_encryption_structure)

        # returns the web mvc encryption structure
        return web_mvc_encryption_structure

    def get_web_mvc_encryption_structure(self):
        """
        Retrieves the web mvc encryption structure.

        @rtype: WebMvcEncryptionStructure
        @return: The web mvc encryption structure.
        """

        return self.web_mvc_encryption_structure

    def set_web_mvc_encryption_structure(self, web_mvc_encryption_structure):
        """
        Sets the web mvc encryption structure.

        @type web_mvc_encryption_structure: WebMvcEncryptionStructure
        @param web_mvc_encryption_structure: The web mvc encryption structure.
        """

        self.web_mvc_encryption_structure = web_mvc_encryption_structure

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
            self.http_client = self.main_client_http_plugin.create_client({})

            # opens the http client
            self.http_client.open({})

        # returns the http client
        return self.http_client

class WebMvcEncryptionStructure:
    """
    The web mvc encryption structure class.
    """

    username = None
    """ The username """

    cin = None
    """ The cin value """

    country = None
    """ The two letter string representing the country to be used """

    language = None
    """ The two letter string representing the language to be used """

    api_version = None
    """ The version of the api being used """

    def __init__(self, username, cin, country, language, api_version = DEFAULT_API_VERSION):
        """
        Constructor of the class.

        @type username: String
        @param username: The username.
        @type cin: String
        @param cin: The cin value.
        @type country: String
        @param country: The two letter string representing the
        country to be used.
        @type language: String
        @param language: The two letter string representing the
        language to be used.
        @type api_version: String
        @param api_version: The version of the api being used.
        """

        self.username = username
        self.cin = cin
        self.country = country
        self.language = language
        self.api_version = api_version

    def get_username(self):
        """
        Retrieves the username.

        @rtype: String
        @return: The username.
        """

        return self.username

    def set_username(self, username):
        """
        Sets the username.

        @type username: String
        @param username: The username.
        """

        self.username = username

    def get_cin(self):
        """
        Retrieves the cin.

        @rtype: String
        @return: The cin.
        """

        return self.cin

    def set_cin(self, cin):
        """
        Sets the cin.

        @type cin: String
        @param cin: The cin.
        """

        self.cin = cin

    def get_country(self):
        """
        Retrieves the country.

        @rtype: String
        @return: The country.
        """

        return self.country

    def set_country(self, country):
        """
        Sets the country.

        @type country: String
        @param country: The country.
        """

        self.country = country

    def get_language(self):
        """
        Retrieves the language.

        @rtype: String
        @return: The language.
        """

        return self.language

    def set_language(self, language):
        """
        Sets the language.

        @type language: String
        @param language: The language.
        """

        self.language = language

    def get_api_version(self):
        """
        Retrieves the api version.

        @rtype: String
        @return: The api version.
        """

        return self.api_version

    def set_api_version(self, api_version):
        """
        Sets the api version.

        @type api_version: String
        @param api_version: The api version.
        """

        self.api_version = api_version
