#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import xml.dom

import colony

from . import exceptions

DEFAULT_CHARSET = "utf-8"
""" The default charset """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

REQUEST_TIMEOUT_VALUE = "request_timeout"
""" The request timeout value """

ERROR_STATUS = "err"
""" The error status """

DEFAULT_API_VERSION = "1.0"
""" The default Easypay API version """

BASE_REST_URL = "http://www.easypay.pt/_s/"
""" The base REST URL to be used """

BASE_REST_SECURE_URL = "https://www.easypay.pt/_s/"
""" The base REST secure URL to be used """

TEST_BASE_REST_URL = "http://test.easypay.pt/_s/"
""" The base REST URL to be used """

TEST_BASE_REST_SECURE_URL = "http://test.easypay.pt/_s/"
""" The base REST secure URL to be used """

DEFAULT_REQUEST_TIMEOUT = 60
""" The default request timeout """

DEFAULT_COUNTRY = "PT"
""" The default country """

DEFAULT_LANGUAGE = "PT"
""" The default language """


class APIEasypay(colony.System):
    """
    The API Easypay class.
    """

    def create_client(self, api_attributes, open_client=True):
        """
        Creates a client, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :type open_client: bool
        :param open_client: If the client should be opened.
        :rtype: EasypayClient
        :return: The created client.
        """

        # retrieves the client HTTP plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the Easypay structure and test mode (if available)
        easypay_structure = api_attributes.get("easypay_structure", None)
        test_mode = api_attributes.get("test_mode", False)

        # creates a new client with the given options, opens
        # it in case it's required and returns the generated
        # client to the caller method
        easypay_client = EasypayClient(client_http_plugin, easypay_structure, test_mode)
        if open_client:
            easypay_client.open()
        return easypay_client


class EasypayClient(object):
    """
    The class that represents a Easypay client connection.
    """

    client_http_plugin = None
    """ The client HTTP plugin """

    easypay_structure = None
    """ The Easypay structure """

    test_mode = None
    """ Flag indicating the client is supposed to
    run in test mode (uses different API urls) """

    http_client = None
    """ The HTTP client for the connection """

    def __init__(
        self, client_http_plugin=None, easypay_structure=None, test_mode=False
    ):
        """
        Constructor of the class.

        :type client_http_plugin: ClientHTTPPlugin
        :param client_http_plugin: The client HTTP plugin.
        :type easypay_structure: EasypayStructure
        :param easypay_structure: The Easypay structure.
        :type test_mode: bool
        :param test_mode: Flag indicating if the client is to
        be run in test mode.
        """

        self.client_http_plugin = client_http_plugin
        self.easypay_structure = easypay_structure
        self.test_mode = test_mode

    def open(self):
        """
        Opens the Easypay client.
        """

        pass

    def close(self):
        """
        Closes the Easypay client.
        """

        # closes the HTTP client in case it is defined
        if self.http_client:
            self.http_client.close({})

    def generate_easypay_structure(
        self,
        username,
        cin,
        country=DEFAULT_COUNTRY,
        language=DEFAULT_LANGUAGE,
        api_version=DEFAULT_API_VERSION,
        set_structure=True,
    ):
        """
        Generates the Easypay structure for the given arguments.

        :type username: String
        :param username: The username.
        :type cin: String
        :param cin: The cin.
        :type country: String
        :param country: The two letter string representing the
        country to be used.
        :type language: String
        :param language: The two letter string representing the
        language to be used.
        :type api_version: String
        :param api_version: The version of the API being used.
        :type set_structure: bool
        :param set_structure: If the structure should be
        set in the Easypay client.
        :rtype: EasypayStructure
        :return: The generated Easypay structure.
        """

        # creates a new Easypay structure then sets the
        # Easypay structure in case it is to be set and
        # returns it to the caller
        easypay_structure = EasypayStructure(
            username, cin, country, language, api_version
        )
        if set_structure:
            self.set_easypay_structure(easypay_structure)
        return easypay_structure

    def generate_reference(
        self,
        amount,
        transaction_key,
        entity,
        reference_type="auto",
        name=None,
        description=None,
        mobile=None,
        email=None,
    ):
        # sets the retrieval URL, using the test URL
        # in case the client is running in test mode
        retrieval_url = (
            TEST_BASE_REST_SECURE_URL if self.test_mode else BASE_REST_SECURE_URL
        ) + "api_easypay_01BG.php"

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # sets the amount, reference key, entity, reference
        # type, country and language in the parameters
        parameters["t_value"] = amount
        parameters["t_key"] = transaction_key
        parameters["ep_entity"] = entity
        parameters["ep_ref_type"] = reference_type
        parameters["ep_country"] = self.easypay_structure.country
        parameters["ep_language"] = self.easypay_structure.language

        # sets the name, description, mobile an email
        # in the parameters in case they were specified
        if name:
            parameters["o_name"] = name
        if description:
            parameters["o_description"] = description
        if mobile:
            parameters["o_mobile"] = mobile
        if email:
            parameters["o_email"] = email

        # fetches the retrieval URL with the given parameters retrieving the XML
        result = self._fetch_url(retrieval_url, parameters)

        # parses the result (response) and retrieves the root node
        response_document = xml.dom.minidom.parseString(result)
        get_reference_root_nodes = response_document.getElementsByTagName("getautoMB")
        get_reference_root_node = get_reference_root_nodes[0]

        # retrieves the reference values
        get_reference_status = self.get_xml_node_text(
            get_reference_root_node, "ep_status"
        )
        get_reference_message = self.get_xml_node_text(
            get_reference_root_node, "ep_message"
        )
        get_reference_cin = self.get_xml_node_text(get_reference_root_node, "ep_cin")
        get_reference_user = self.get_xml_node_text(get_reference_root_node, "ep_user")
        get_reference_entity = self.get_xml_node_text(
            get_reference_root_node, "ep_entity"
        )
        get_reference_reference = self.get_xml_node_text(
            get_reference_root_node, "ep_reference"
        )
        get_reference_value = self.get_xml_node_text(
            get_reference_root_node, "ep_value"
        )
        get_reference_key = self.get_xml_node_text(get_reference_root_node, "t_key")
        get_reference_link = self.get_xml_node_text(get_reference_root_node, "ep_link")

        # processes the casting of the values
        get_reference_value = float(get_reference_value)

        # initializes the data (map)
        data = {
            "status": get_reference_status,
            "message": get_reference_message,
            "cin": get_reference_cin,
            "user": get_reference_user,
            "entity": get_reference_entity,
            "reference": get_reference_reference,
            "value": get_reference_value,
            "key": get_reference_key,
            "link": get_reference_link,
        }

        # checks for Easypay errors
        self._check_easypay_errors(data)

        # returns the data
        return data

    def cancel_reference(self, entity, reference):
        # sets the retrieval URL, using the test URL
        # in case the client is running in test mode
        retrieval_url = (
            TEST_BASE_REST_SECURE_URL if self.test_mode else BASE_REST_SECURE_URL
        ) + "api_easypay_00BG.php"

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # sets the entity, reference and delete flag in the parameters
        parameters["ep_entity"] = entity
        parameters["ep_ref"] = reference
        parameters["ep_delete"] = "yes"

        # fetches the retrieval URL with the given parameters retrieving the XML
        result = self._fetch_url(retrieval_url, parameters)

        # parses the result (response) and retrieves the root node
        response_document = xml.dom.minidom.parseString(result)
        get_reference_root_nodes = response_document.getElementsByTagName("getautoMB")
        get_reference_root_node = get_reference_root_nodes[0]

        # retrieves the reference values
        get_reference_status = self.get_xml_node_text(
            get_reference_root_node, "ep_status"
        )
        get_reference_message = self.get_xml_node_text(
            get_reference_root_node, "ep_message"
        )
        get_reference_cin = self.get_xml_node_text(get_reference_root_node, "ep_cin")
        get_reference_user = self.get_xml_node_text(get_reference_root_node, "ep_user")
        get_reference_entity = self.get_xml_node_text(
            get_reference_root_node, "ep_entity"
        )
        get_reference_reference = self.get_xml_node_text(
            get_reference_root_node, "ep_reference"
        )
        get_reference_value = self.get_xml_node_text(
            get_reference_root_node, "ep_value"
        )
        get_reference_key = self.get_xml_node_text(get_reference_root_node, "t_key")

        # processes the casting of the values
        get_reference_value = float(get_reference_value)

        # initializes the data (map)
        data = {
            "status": get_reference_status,
            "message": get_reference_message,
            "cin": get_reference_cin,
            "user": get_reference_user,
            "entity": get_reference_entity,
            "reference": get_reference_reference,
            "value": get_reference_value,
            "key": get_reference_key,
        }

        # checks for Easypay errors
        self._check_easypay_errors(data)

        # returns the data
        return data

    def get_payment_details(self, document_identifier, reference_key):
        # sets the retrieval URL, using the test URL
        # in case the client is running in test mode
        retrieval_url = (
            TEST_BASE_REST_SECURE_URL if self.test_mode else BASE_REST_SECURE_URL
        ) + "api_easypay_03AG.php"

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # sets the document identifier and reference key in the parameters
        parameters["ep_doc"] = document_identifier
        parameters["ep_key"] = reference_key

        # fetches the retrieval URL with the given parameters retrieving the XML
        result = self._fetch_url(retrieval_url, parameters)

        # parses the result (response) and retrieves the root node
        response_document = xml.dom.minidom.parseString(result)
        get_payment_details_root_nodes = response_document.getElementsByTagName(
            "getautoMB_detail"
        )
        get_payment_details_root_node = get_payment_details_root_nodes[0]

        # retrieves the basic payment details
        get_payment_details_status = self.get_xml_node_text(
            get_payment_details_root_node, "ep_status"
        )
        get_payment_details_message = self.get_xml_node_text(
            get_payment_details_root_node, "ep_message"
        )
        get_payment_details_cin = self.get_xml_node_text(
            get_payment_details_root_node, "ep_cin"
        )
        get_payment_details_user = self.get_xml_node_text(
            get_payment_details_root_node, "ep_user"
        )
        get_payment_details_key = self.get_xml_node_text(
            get_payment_details_root_node, "ep_key"
        )
        get_payment_details_transaction_key = self.get_xml_node_text(
            get_payment_details_root_node, "t_key"
        )
        get_payment_details_doc = self.get_xml_node_text(
            get_payment_details_root_node, "ep_doc"
        )

        # initializes the data (map)
        data = {
            "status": get_payment_details_status,
            "message": get_payment_details_message,
            "cin": get_payment_details_cin,
            "user": get_payment_details_user,
            "key": get_payment_details_key,
            "transaction_key": get_payment_details_transaction_key,
            "document": get_payment_details_doc,
        }

        # checks for Easypay errors
        self._check_easypay_errors(data)

        # retrieves the remaining payment details
        get_payment_details_entity = self.get_xml_node_text(
            get_payment_details_root_node, "ep_entity"
        )
        get_payment_details_reference = self.get_xml_node_text(
            get_payment_details_root_node, "ep_reference"
        )
        get_payment_details_value = self.get_xml_node_text(
            get_payment_details_root_node, "ep_value"
        )
        get_payment_details_payment_type = self.get_xml_node_text(
            get_payment_details_root_node, "ep_payment_type"
        )
        get_payment_details_value_fixed = self.get_xml_node_text(
            get_payment_details_root_node, "ep_value_fixed"
        )
        get_payment_details_value_var = self.get_xml_node_text(
            get_payment_details_root_node, "ep_value_var"
        )
        get_payment_details_value_tax = self.get_xml_node_text(
            get_payment_details_root_node, "ep_value_tax"
        )
        get_payment_details_value_transf = self.get_xml_node_text(
            get_payment_details_root_node, "ep_value_transf"
        )
        get_payment_details_date_transf = self.get_xml_node_text(
            get_payment_details_root_node, "ep_date_transf"
        )
        get_payment_details_date_read = self.get_xml_node_text(
            get_payment_details_root_node, "ep_date_read"
        )
        get_payment_details_status_read = self.get_xml_node_text(
            get_payment_details_root_node, "ep_status_read"
        )

        # converts the numeric payment details
        get_payment_details_value = float(get_payment_details_value)
        get_payment_details_value_fixed = float(get_payment_details_value_fixed)
        get_payment_details_value_var = float(get_payment_details_value_var)
        get_payment_details_value_tax = float(get_payment_details_value_tax)
        get_payment_details_value_transf = float(get_payment_details_value_transf)

        # sets the values in the data (map)
        data["entity"] = get_payment_details_entity
        data["reference"] = get_payment_details_reference
        data["value"] = get_payment_details_value
        data["payment_type"] = get_payment_details_payment_type
        data["value_fixed"] = get_payment_details_value_fixed
        data["value_variable"] = get_payment_details_value_var
        data["value_tax"] = get_payment_details_value_tax
        data["value_transfer"] = get_payment_details_value_transf
        data["date_transfer"] = get_payment_details_date_transf
        data["date_read"] = get_payment_details_date_read
        data["status_read"] = get_payment_details_status_read

        # checks for Easypay errors
        self._check_easypay_errors(data)

        # returns the data
        return data

    def validate_credentials(self):
        """
        Validates that the credentials are valid, returning a flag
        indicating the result.

        This operation will perform the get payment details operation
        with invalid arguments as a no-op, in order to check its exception
        message for the presence of a statement that the credentials are invalid.

        :rtype: bool
        :return: Flag indicating if the credentials are valid.
        """

        # initializes the valid flag
        valid = True

        # attempts to retrieve the payment details
        # with invalid arguments (no-op) and checks
        # if a credential failure is in the exception message,
        # to determine if the credentials are valid
        try:
            self.get_payment_details(None, None)
        except Exception as exception:
            valid = not "ep_cin not ok" in exception.message

        # returns the valid flag
        return valid

    def get_easypay_structure(self):
        """
        Retrieves the Easypay structure.

        :rtype: EasypayStructure
        :return: The Easypay structure.
        """

        return self.easypay_structure

    def set_easypay_structure(self, easypay_structure):
        """
        Sets the Easypay structure.

        :type easypay_structure: EasypayStructure
        :param easypay_structure: The Easypay structure.
        """

        self.easypay_structure = easypay_structure

    def _set_base_parameters(self, parameters):
        """
        Sets the base Easypay REST request parameters
        in the parameters map.

        :type parameters: Dictionary
        :param parameters: The parameters map to be used in setting
        the base parameters.
        """

        # sets the username and cin in the parameters
        parameters["ep_user"] = self.easypay_structure.username
        parameters["ep_cin"] = self.easypay_structure.cin

    def _fetch_url(self, url, parameters=None, method=GET_METHOD_VALUE):
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

        # creates the parameters map in case it is not defined
        if not parameters:
            parameters = {}

        # retrieves the HTTP client, fetches the URL retrieving the
        # HTTP response and retrieves the contents from the response
        http_client = self._get_http_client()
        http_response = http_client.fetch_url(
            url, method, parameters, content_type_charset=DEFAULT_CHARSET
        )
        contents = http_response.received_message

        # returns the contents
        return contents

    def _build_url(self, base_url, parameters):
        """
        Builds the URL for the given URL and parameters.

        :type url: String
        :param url: The base URL to be used.
        :type parameters: Dictionary
        :param parameters: The parameters to be used for URL construction.
        :rtype: String
        :return: The built URL for the given parameters.
        """

        # retrieves the HTTP client, then builds the URL from the
        # base URL and returns it to the caller method
        http_client = self._get_http_client()
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)
        return url

    def _check_easypay_errors(self, data):
        """
        Checks the given data for Easypay errors.

        This method raises an exception in case an error
        exists in the data to be verified.

        :type data: Dictionary
        :param data: The data to be checked for Easypay errors.
        """

        # retrieves the status and
        # message from the data
        status = data["status"]
        message = data["message"]

        # returns immediately in case the
        # status does not start with an error
        if not status.startswith(ERROR_STATUS):
            return

        # raises the Easypay API error
        raise exceptions.EasypayAPIError("error in request: " + message)

    def _get_http_client(self):
        """
        Retrieves the HTTP client currently in use (in case it's created)
        if not created creates the HTTP client.

        :rtype: HTTPClient
        :return: The retrieved HTTP client.
        """

        # in case an HTTP client already exists then returns it
        if self.http_client:
            return self.http_client

        # defines the client parameters
        client_parameters = {CONTENT_TYPE_CHARSET_VALUE: DEFAULT_CHARSET}

        # creates the HTTP client
        self.http_client = self.client_http_plugin.create_client(client_parameters)

        # defines the open parameters
        open_parameters = {REQUEST_TIMEOUT_VALUE: DEFAULT_REQUEST_TIMEOUT}

        # opens the HTTP client
        self.http_client.open(open_parameters)

        # returns the HTTP client
        return self.http_client

    def get_xml_node_text(self, xml_document, xml_tag_name):
        # retrieves the XML nodes, returning none
        # in case the retrieved nodes are empty
        xml_nodes = xml_document.getElementsByTagName(xml_tag_name)
        if not xml_nodes:
            return None

        # retrieves the XML node (first), and its text
        xml_node = xml_nodes[0]
        xml_node_text = self._get_xml_node_text(xml_node)

        # returns the XML node text
        return xml_node_text

    def _get_xml_node_text(self, xml_node):
        # retrieves the child nodes
        child_nodes = xml_node.childNodes

        # collects the child text nodes
        child_node_data_list = [
            child_node.data
            for child_node in child_nodes
            if child_node.nodeType == xml.dom.minidom.Node.TEXT_NODE
        ]

        # converts the child text nodes to a string
        xml_node_text = "".join(child_node_data_list)

        # returns the XML node text
        return xml_node_text


class EasypayStructure(object):
    """
    The Easypay structure class.
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
    """ The version of the API being used """

    def __init__(
        self, username, cin, country, language, api_version=DEFAULT_API_VERSION
    ):
        """
        Constructor of the class.

        :type username: String
        :param username: The username.
        :type cin: String
        :param cin: The cin value.
        :type country: String
        :param country: The two letter string representing the
        country to be used.
        :type language: String
        :param language: The two letter string representing the
        language to be used.
        :type api_version: String
        :param api_version: The version of the API being used.
        """

        self.username = username
        self.cin = cin
        self.country = country
        self.language = language
        self.api_version = api_version

    def get_username(self):
        """
        Retrieves the username.

        :rtype: String
        :return: The username.
        """

        return self.username

    def set_username(self, username):
        """
        Sets the username.

        :type username: String
        :param username: The username.
        """

        self.username = username

    def get_cin(self):
        """
        Retrieves the cin.

        :rtype: String
        :return: The cin.
        """

        return self.cin

    def set_cin(self, cin):
        """
        Sets the cin.

        :type cin: String
        :param cin: The cin.
        """

        self.cin = cin

    def get_country(self):
        """
        Retrieves the country.

        :rtype: String
        :return: The country.
        """

        return self.country

    def set_country(self, country):
        """
        Sets the country.

        :type country: String
        :param country: The country.
        """

        self.country = country

    def get_language(self):
        """
        Retrieves the language.

        :rtype: String
        :return: The language.
        """

        return self.language

    def set_language(self, language):
        """
        Sets the language.

        :type language: String
        :param language: The language.
        """

        self.language = language

    def get_api_version(self):
        """
        Retrieves the API version.

        :rtype: String
        :return: The API version.
        """

        return self.api_version

    def set_api_version(self, api_version):
        """
        Sets the API version.

        :type api_version: String
        :param api_version: The API version.
        """

        self.api_version = api_version
