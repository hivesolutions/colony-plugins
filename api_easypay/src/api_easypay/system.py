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

import xml.dom

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

REQUEST_TIMEOUT_VALUE = "request_timeout"
""" The request timeout value """

ERROR_STATUS = "err"
""" The error status """

DEFAULT_API_VERSION = "1.0"
""" The default easypay api version """

BASE_REST_URL = "http://www.easypay.pt/_s/"
""" The base rest url to be used """

BASE_REST_SECURE_URL = "https://www.easypay.pt/_s/"
""" The base rest secure url to be used """

TEST_BASE_REST_URL = "http://test.easypay.pt/_s/"
""" The base rest url to be used """

TEST_BASE_REST_SECURE_URL = "http://test.easypay.pt/_s/"
""" The base rest secure url to be used """

DEFAULT_REQUEST_TIMEOUT = 60
""" The default request timeout """

DEFAULT_COUNTRY = "PT"
""" The default country """

DEFAULT_LANGUAGE = "PT"
""" The default language """

class ApiEasypay(colony.base.system.System):
    """
    The api easypay class.
    """

    def create_client(self, api_attributes, open_client = True):
        """
        Creates a client, with the given api attributes.

        @type api_attributes: Dictionary
        @param api_attributes: The api attributes to be used.
        @type open_client: bool
        @param open_client: If the client should be opened.
        @rtype: EasypayClient
        @return: The created client.
        """

        # retrieves the client http plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the easypay structure and test mode (if available)
        easypay_structure = api_attributes.get("easypay_structure", None)
        test_mode = api_attributes.get("test_mode", False)

        # creates a new client with the given options, opens
        # it in case it's required and returns the generated
        # client to the caller method
        easypay_client = EasypayClient(client_http_plugin, easypay_structure, test_mode)
        open_client and easypay_client.open()
        return easypay_client

class EasypayClient:
    """
    The class that represents a easypay client connection.
    """

    client_http_plugin = None
    """ The client http plugin """

    easypay_structure = None
    """ The easypay structure """

    test_mode = None
    """ Flag indicating the client is supposed to
    run in test mode (uses different api urls) """

    http_client = None
    """ The http client for the connection """

    def __init__(self, client_http_plugin = None, easypay_structure = None, test_mode = False):
        """
        Constructor of the class.

        @type client_http_plugin: ClientHttpPlugin
        @param client_http_plugin: The client http plugin.
        @type easypay_structure: EasypayStructure
        @param easypay_structure: The easypay structure.
        @type test_mode: bool
        @param test_mode: Flag indicating if the client is to
        be run in test mode.
        """

        self.client_http_plugin = client_http_plugin
        self.easypay_structure = easypay_structure
        self.test_mode = test_mode

    def open(self):
        """
        Opens the easypay client.
        """

        pass

    def close(self):
        """
        Closes the easypay client.
        """

        # closes the http client in case it is defined
        if self.http_client: self.http_client.close({})

    def generate_easypay_structure(self, username, cin, country = DEFAULT_COUNTRY, language = DEFAULT_LANGUAGE, api_version = DEFAULT_API_VERSION, set_structure = True):
        """
        Generates the easypay structure for the given arguments.

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
        set in the easypay client.
        @rtype: EasypayStructure
        @return: The generated easypay structure.
        """

        # creates a new easypay structure
        easypay_structure = EasypayStructure(username, cin, country, language, api_version)

        # sets the easypay structure in case it is to be set
        if set_structure: self.set_easypay_structure(easypay_structure)

        # returns the easypay structure
        return easypay_structure

    def generate_reference(self, amount, transaction_key, entity, reference_type = "auto", name = None, description = None, mobile = None, email = None):
        # sets the retrieval url, using the test url
        # in case the client is running in test mode
        retrieval_url = (self.test_mode and TEST_BASE_REST_SECURE_URL or BASE_REST_SECURE_URL) + "api_easypay_01BG.php"

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
        if name: parameters["o_name"] = name
        if description: parameters["o_description"] = description
        if mobile: parameters["o_mobile"] = mobile
        if email: parameters["o_email"] = email

        # fetches the retrieval url with the given parameters retrieving the xml
        result = self._fetch_url(retrieval_url, parameters)

        # parses the result (response) and retrieves the root node
        response_document = xml.dom.minidom.parseString(result)
        get_reference_root_nodes = response_document.getElementsByTagName("getautoMB")
        get_reference_root_node = get_reference_root_nodes[0]

        # retrieves the reference values
        get_reference_status = self.get_xml_node_text(get_reference_root_node, "ep_status")
        get_reference_message = self.get_xml_node_text(get_reference_root_node, "ep_message")
        get_reference_cin = self.get_xml_node_text(get_reference_root_node, "ep_cin")
        get_reference_user = self.get_xml_node_text(get_reference_root_node, "ep_user")
        get_reference_entity = self.get_xml_node_text(get_reference_root_node, "ep_entity")
        get_reference_reference = self.get_xml_node_text(get_reference_root_node, "ep_reference")
        get_reference_value = self.get_xml_node_text(get_reference_root_node, "ep_value")
        get_reference_key = self.get_xml_node_text(get_reference_root_node, "t_key")
        get_reference_link = self.get_xml_node_text(get_reference_root_node, "ep_link")

        # processes the casting of the values
        get_reference_value = float(get_reference_value)

        # initializes the data (map)
        data = {
            "status" : get_reference_status,
            "message" : get_reference_message,
            "cin" : get_reference_cin,
            "user" : get_reference_user,
            "entity" : get_reference_entity,
            "reference" : get_reference_reference,
            "value" : get_reference_value,
            "key" : get_reference_key,
            "link" : get_reference_link
        }

        # checks for easypay errors
        self._check_easypay_errors(data)

        # returns the data
        return data

    def cancel_reference(self, entity, reference):
        # sets the retrieval url, using the test url
        # in case the client is running in test mode
        retrieval_url = (self.test_mode and TEST_BASE_REST_SECURE_URL or BASE_REST_SECURE_URL) + "api_easypay_00BG.php"

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # sets the entity, reference and delete flag in the parameters
        parameters["ep_entity"] = entity
        parameters["ep_ref"] = reference
        parameters["ep_delete"] = "yes"

        # fetches the retrieval url with the given parameters retrieving the xml
        result = self._fetch_url(retrieval_url, parameters)

        # parses the result (response) and retrieves the root node
        response_document = xml.dom.minidom.parseString(result)
        get_reference_root_nodes = response_document.getElementsByTagName("getautoMB")
        get_reference_root_node = get_reference_root_nodes[0]

        # retrieves the reference values
        get_reference_status = self.get_xml_node_text(get_reference_root_node, "ep_status")
        get_reference_message = self.get_xml_node_text(get_reference_root_node, "ep_message")
        get_reference_cin = self.get_xml_node_text(get_reference_root_node, "ep_cin")
        get_reference_user = self.get_xml_node_text(get_reference_root_node, "ep_user")
        get_reference_entity = self.get_xml_node_text(get_reference_root_node, "ep_entity")
        get_reference_reference = self.get_xml_node_text(get_reference_root_node, "ep_reference")
        get_reference_value = self.get_xml_node_text(get_reference_root_node, "ep_value")
        get_reference_key = self.get_xml_node_text(get_reference_root_node, "t_key")

        # processes the casting of the values
        get_reference_value = float(get_reference_value)

        # initializes the data (map)
        data = {
            "status" : get_reference_status,
            "message" : get_reference_message,
            "cin" : get_reference_cin,
            "user" : get_reference_user,
            "entity" : get_reference_entity,
            "reference" : get_reference_reference,
            "value" : get_reference_value,
            "key" : get_reference_key
        }

        # checks for easypay errors
        self._check_easypay_errors(data)

        # returns the data
        return data

    def get_payment_details(self, document_identifier, reference_key):
        # sets the retrieval url, using the test url
        # in case the client is running in test mode
        retrieval_url = (self.test_mode and TEST_BASE_REST_SECURE_URL or BASE_REST_SECURE_URL) + "api_easypay_03AG.php"

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # sets the document identifier and reference key in the parameters
        parameters["ep_doc"] = document_identifier
        parameters["ep_key"] = reference_key

        # fetches the retrieval url with the given parameters retrieving the xml
        result = self._fetch_url(retrieval_url, parameters)

        # parses the result (response) and retrieves the root node
        response_document = xml.dom.minidom.parseString(result)
        get_payment_details_root_nodes = response_document.getElementsByTagName("getautoMB_detail")
        get_payment_details_root_node = get_payment_details_root_nodes[0]

        # retrieves the basic payment details
        get_payment_details_status = self.get_xml_node_text(get_payment_details_root_node, "ep_status")
        get_payment_details_message = self.get_xml_node_text(get_payment_details_root_node, "ep_message")
        get_payment_details_cin = self.get_xml_node_text(get_payment_details_root_node, "ep_cin")
        get_payment_details_user = self.get_xml_node_text(get_payment_details_root_node, "ep_user")
        get_payment_details_key = self.get_xml_node_text(get_payment_details_root_node, "ep_key")
        get_payment_details_transaction_key = self.get_xml_node_text(get_payment_details_root_node, "t_key")
        get_payment_details_doc = self.get_xml_node_text(get_payment_details_root_node, "ep_doc")

        # initializes the data (map)
        data = {
            "status" : get_payment_details_status,
            "message" : get_payment_details_message,
            "cin" : get_payment_details_cin,
            "user" : get_payment_details_user,
            "key" : get_payment_details_key,
            "transaction_key" : get_payment_details_transaction_key,
            "document" : get_payment_details_doc
        }

        # checks for easypay errors
        self._check_easypay_errors(data)

        # retrieves the remaining payment details
        get_payment_details_entity = self.get_xml_node_text(get_payment_details_root_node, "ep_entity")
        get_payment_details_reference = self.get_xml_node_text(get_payment_details_root_node, "ep_reference")
        get_payment_details_value = self.get_xml_node_text(get_payment_details_root_node, "ep_value")
        get_payment_details_payment_type = self.get_xml_node_text(get_payment_details_root_node, "ep_payment_type")
        get_payment_details_value_fixed = self.get_xml_node_text(get_payment_details_root_node, "ep_value_fixed")
        get_payment_details_value_var = self.get_xml_node_text(get_payment_details_root_node, "ep_value_var")
        get_payment_details_value_tax = self.get_xml_node_text(get_payment_details_root_node, "ep_value_tax")
        get_payment_details_value_transf = self.get_xml_node_text(get_payment_details_root_node, "ep_value_transf")
        get_payment_details_date_transf = self.get_xml_node_text(get_payment_details_root_node, "ep_date_transf")
        get_payment_details_date_read = self.get_xml_node_text(get_payment_details_root_node, "ep_date_read")
        get_payment_details_status_read = self.get_xml_node_text(get_payment_details_root_node, "ep_status_read")

        # converst the numeric payment details
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

        # checks for easypay errors
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

        @rtype: bool
        @return: Flag indicating if the credentials are valid.
        """

        # initializes the valid flag
        valid = True

        # attempts to retrieve the payment details
        # with invalid arguments (no-op) and checks
        # if a credential failure is in the exception message,
        # to determine if the credentials are valid
        try: self.get_payment_details(None, None)
        except Exception, exception: valid = not "ep_cin not ok" in exception.message

        # returns the valid flag
        return valid

    def get_easypay_structure(self):
        """
        Retrieves the easypay structure.

        @rtype: EasypayStructure
        @return: The easypay structure.
        """

        return self.easypay_structure

    def set_easypay_structure(self, easypay_structure):
        """
        Sets the easypay structure.

        @type easypay_structure: EasypayStructure
        @param easypay_structure: The easypay structure.
        """

        self.easypay_structure = easypay_structure

    def _set_base_parameters(self, parameters):
        """
        Sets the base easypay rest request parameters
        in the parameters map.

        @type parameters: Dictionary
        @param parameters: The parameters map to be used in setting
        the base parameters.
        """

        # sets the username and cin in the parameters
        parameters["ep_user"] = self.easypay_structure.username
        parameters["ep_cin"] = self.easypay_structure.cin

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

        # creates the parameters map in case it is not defined
        if not parameters: parameters = {}

        # retrieves the http client, fethes the url retrieving the
        # http response and retrieves the contents from the response
        http_client = self._get_http_client()
        http_response = http_client.fetch_url(
            url,
            method,
            parameters,
            content_type_charset = DEFAULT_CHARSET
        )
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

        # build the url from the base url
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)

        # returns the url
        return url

    def _check_easypay_errors(self, data):
        """
        Checks the given data for easypay errors.

        This method raises an exception in case an error
        exists in the data to be verified.

        @type data: Dictionary
        @param data: The data to be checked for easypay errors.
        """

        # retrieves the status and
        # message from the data
        status = data["status"]
        message = data["message"]

        # returns immediately in case the
        # status does not start with an error
        if not status.startswith(ERROR_STATUS): return

        # raises the easypay api error
        raise exceptions.EasypayApiError("error in request: " + message)

    def _get_http_client(self):
        """
        Retrieves the http client currently in use (in case it's created)
        if not created creates the http client.

        @rtype: HttpClient
        @return: The retrieved http client.
        """

        # in case an http client already exists then returns it
        if self.http_client: return self.http_client

        # defines the client parameters
        client_parameters = {
            CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET
        }

        # creates the http client
        self.http_client = self.client_http_plugin.create_client(client_parameters)

        # defines the open parameters
        open_parameters = {
            REQUEST_TIMEOUT_VALUE : DEFAULT_REQUEST_TIMEOUT
        }

        # opens the http client
        self.http_client.open(open_parameters)

        # returns the http client
        return self.http_client

    def get_xml_node_text(self, xml_document, xml_tag_name):
        # retrieves the xml nodes, returning none
        # in case the retrieved nodes are empty
        xml_nodes = xml_document.getElementsByTagName(xml_tag_name)
        if not xml_nodes: return None

        # retrieves the xml node (first), and its text
        xml_node = xml_nodes[0]
        xml_node_text = self._get_xml_node_text(xml_node)

        # returns the xml node text
        return xml_node_text

    def _get_xml_node_text(self, xml_node):
        # retrieves the child nodes
        child_nodes = xml_node.childNodes

        # collects the child text nodes
        child_node_data_list = [child_node.data for child_node in child_nodes if child_node.nodeType == xml.dom.minidom.Node.TEXT_NODE]

        # converts the child text nodes to a string
        xml_node_text = "".join(child_node_data_list)

        # returns the xml node text
        return xml_node_text

class EasypayStructure:
    """
    The easypay structure class.
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
