#!/usr/bin/python
# -*- coding: utf-8 -*-

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

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

BASE_REST_URL = "http://bargania.com/"
""" The base rest url to be used """

BASE_REST_SECURE_URL = "https://bargania.com/"
""" The base rest secure url to be used """

class ServiceBargania:
    """
    The service bargania class.
    """

    service_bargania_plugin = None
    """ The service bargania plugin """

    def __init__(self, service_bargania_plugin):
        """
        Constructor of the class.

        @type service_bargania_plugin: ServiceBarganiaPlugin
        @param service_bargania_plugin: The service bargania plugin.
        """

        self.service_bargania_plugin = service_bargania_plugin

    def create_remote_client(self, service_attributes, open_client = True):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @type open_client: bool
        @param open_client: If the client should be opened.
        @rtype: BarganiaClient
        @return: The created remote client.
        """

        # retrieves the main client http plugin
        main_client_http_plugin = self.service_bargania_plugin.main_client_http_plugin

        # retrieves the json plugin
        json_plugin = self.service_bargania_plugin.json_plugin

        # creates a new bargania client with the given options
        bargania_client = BarganiaClient(json_plugin, main_client_http_plugin)

        # in case the client is meant to be open
        # open the client
        open_client and bargania_client.open()

        # returns the bargania client
        return bargania_client

class BarganiaClient:
    """
    The class that represents a bargania client connection.
    """

    json_plugin = None
    """ The json plugin """

    main_client_http_plugin = None
    """ The main client http plugin """

    http_client = None
    """ The http client for the connection """

    def __init__(self, json_plugin = None, main_client_http_plugin = None):
        """
        Constructor of the class.

        @type json_plugin: JsonPlugin
        @param json_plugin: The json plugin.
        @type main_client_http_plugin: MainClientHttpPlugin
        @param main_client_http_plugin: The main client http plugin.
        """

        self.json_plugin = json_plugin
        self.main_client_http_plugin = main_client_http_plugin

        self.request_header = {}

    def open(self):
        """
        Opens the bargania client.
        """

        pass

    def close(self):
        """
        Closes the bargania client.
        """

        # in case an http client is defined
        if self.http_client:
            # closes the http client
            self.http_client.close({})

    def get_status(self, start_date, end_date = None, steps = 7):
        """
        Retrieves the status of the bargania system from the start
        data until the end date.
        The interval of the status is defined by the number of steps.

        @type start_date: int
        @type start_date: The start date timestamp (in seconds).
        @type end_date: int
        @type end_date: The end date timestamp (in seconds).
        @type steps: int
        @param steps: The number of steps to be used in the status
        retrieval.
        @rtype: Dictionary
        @return: A map describing the status in the given interval
        for the bargania environment.
        """

        # start the parameters map
        parameters = {
            "start_date" : start_date,
            "end_date" : end_date,
            "steps" : steps
        }

        # sets the retrieval
        retrieval_url = BASE_REST_URL + "status.json"

        # fetches the retrieval url with the given parameters retrieving the json
        json = self._fetch_url(retrieval_url, parameters)

        # loads json retrieving the data
        data = self.json_plugin.loads(json)

        # checks for bargania errors
        self._check_bargania_errors(data)

        # returns the data
        return data

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


    def _check_bargania_errors(self, data):
        """
        Checks the given data for bargania errors.

        @type data: String
        @param data: The data to be checked for bargania errors.
        @rtype: bool
        @return: The result of the data error check.
        """

        pass

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
