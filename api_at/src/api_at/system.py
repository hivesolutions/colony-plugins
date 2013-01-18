#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

import colony.base.system

import exceptions

DEFAULT_CHARSET = "utf-8"
""" The default charset """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

BASE_URL = "http:/servicos.portaldasfinancas.gov.pt:400/fews/faturas"
""" The base url to be used """

BASE_TEST_URL = "http:/servicos.portaldasfinancas.gov.pt:700/fews/faturas"
""" The base test url to be used """

class ApiAt(colony.base.system.System):
    """
    The api at class.
    """

    def create_client(self, api_attributes, open_client = True):
        """
        Creates a client, with the given api attributes.

        @type api_attributes: Dictionary
        @param api_attributes: The api attributes to be used.
        @type open_client: bool
        @param open_client: If the client should be opened.
        @rtype: OpenidClient
        @return: The created client.
        """

        # retrieves the client http plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the at structure and test mode (if available)
        at_structure = api_attributes.get("at_structure", None)
        test_mode = api_attributes.get("test_mode", False)

        # creates a new at client with the given options and
        # returns it to the caller method
        at_client = AtClient(client_http_plugin, at_structure, test_mode)
        return at_client

class AtClient:
    """
    The class that represents a at client connection.
    Will be used to encapsulate the http request
    around a locally usable api.
    """

    client_http_plugin = None
    """ The client http plugin """

    at_structure = None
    """ The at structure """

    test_mode = None
    """ Flag indicating the client is supposed to
    run in test mode (uses different api urls) """

    http_client = None
    """ The http client for the connection """

    def __init__(self, client_http_plugin = None, at_structure = None, test_mode = False):
        """
        Constructor of the class.

        @type client_http_plugin: ClientHttpPlugin
        @param client_http_plugin: The client http plugin.
        @type at_structure: AtStructure
        @param at_structure: The at structure.
        @type test_mode: bool
        @param test_mode: Flag indicating if the client is to
        be run in test mode.
        """

        self.client_http_plugin = client_http_plugin
        self.at_structure = at_structure
        self.test_mode = test_mode

    def open(self):
        """
        Opens the at client.
        """

        pass

    def close(self):
        """
        Closes the at client.
        """

        # in case an http client is defined closes it
        # (flushing its internal structures
        if self.http_client: self.http_client.close({})
        
    def submit_invoice(self, soap_payload):
        # tenho de criar o client o nonce, etc
        pass

    def generate_at_structure(self, username, password, set_structure = True):
        """
        Generates the at structure for the given arguments.

        @type username: String
        @param username: The username.
        @type password: String
        @param passwird: The password.
        @type set_structure: bool
        @param set_structure: If the structure should be
        set in the at client.
        @rtype: AtStructure
        @return: The generated at structure.
        """

        # creates a new at structure
        at_structure = AtStructure(username, password)

        # in case the structure is meant to be set
        # sets it accordingly (in the current object)
        if set_structure: self.set_at_structure(at_structure)

        # returns the at structure
        return at_structure

    def validate_credentials(self):
        """
        Validates that the credentials are valid, returning a flag
        indicating the result.
        
        This operation is considered a mock for the at client as
        it returns valid, provides api compatibility.

        @rtype: bool
        @return: Flag indicating if the credentials are valid.
        """

        # returns valid for every request for validation received
        # as no validation is currently possible
        return True

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

        # build the url from the base url
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)

        # returns the url
        return url

    def _check_at_errors(self, data):
        """
        Checks the given data for at errors.

        This method raises an exception in case an error
        exists in the data to be verified.

        @type data: Dictionary
        @param data: The data to be checked for at errors.
        """
        
        #@TODO: implement this correctly

        # retrieves the message value and returns immediately
        # in case it's not defined (no error in request)
        message = data.get("L_SHORTMESSAGE0", None)
        if not message: return

        # tries to retrieve the long message to be used for more
        # in depth diagnostics of the problem
        long_message = data.get("L_LONGMESSAGE0", None)

        # raises the at api error
        raise exceptions.AtApiError("error in request: " + message, long_message)

    def _get_http_client(self):
        """
        Retrieves the http client currently in use (in case it's created)
        if not created creates the http client.

        @rtype: HttpClient
        @return: The retrieved http client.
        """

        # in case no http client exists one must be created
        # for the interaction with the api service
        if not self.http_client:
            # defines the client parameters to be used in the
            # creation of the http client
            client_parameters = {
                CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET
            }

            # creates the http client to be used for the api
            # operation and opens it with the default configuration
            self.http_client = self.client_http_plugin.create_client(client_parameters)
            self.http_client.open()

        # returns the created/existing http client
        return self.http_client

class AtStructure:
    """
    The at structure class used to store
    the various at dependent attributes
    placed there over the course of a session.
    """

    username = None
    """ The username """

    password = None
    """ The password """

    def __init__(self, username, password):
        """
        Constructor of the class.

        @type username: String
        @param username: The username.
        @type password: String
        @param password: The password.
        """

        self.username = username
        self.password = password

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

    def get_password(self):
        """
        Retrieves the password.

        @rtype: String
        @return: The password.
        """

        return self.password

    def set_password(self, password):
        """
        Sets the password.

        @type password: String
        @param password: The password.
        """

        self.password = password
