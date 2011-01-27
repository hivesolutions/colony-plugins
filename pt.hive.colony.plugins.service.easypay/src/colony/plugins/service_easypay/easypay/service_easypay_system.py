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

import xml.dom

import service_easypay_exceptions

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

DEFAULT_REQUEST_TIMEOUT = 60
""" The default request timeout """

class ServiceEasypay:
    """
    The service easypay class.
    """

    service_facebbok_plugin = None
    """ The service easypay plugin """

    def __init__(self, service_easypay_plugin):
        """
        Constructor of the class.

        @type service_easypay_plugin: ServiceEasypayPlugin
        @param service_easypay_plugin: The service easypay plugin.
        """

        self.service_easypay_plugin = service_easypay_plugin

    def create_remote_client(self, service_attributes):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: easypayClient
        @return: The created remote client.
        """

        # retrieves the main client http plugin
        main_client_http_plugin = self.service_easypay_plugin.main_client_http_plugin

        # retrieves the easypay structure (if available)
        easypay_structure = service_attributes.get("easypay_structure", None)

        # creates a new easypay client with the given options
        easypay_client = EasypayClient(main_client_http_plugin, easypay_structure)

        # returns the easypay client
        return easypay_client

class EasypayClient:
    """
    The class that represents a easypay client connection.
    """

    main_client_http_plugin = None
    """ The main client http plugin """

    easypay_structure = None
    """ The easypay structure """

    http_client = None
    """ The http client for the connection """

    def __init__(self, main_client_http_plugin = None, easypay_structure = None):
        """
        Constructor of the class.

        @type main_client_http_plugin: MainClientHttpPlugin
        @param main_client_http_plugin: The main client http plugin.
        @type easypay_structure: EasypayStructure
        @param easypay_structure: The easypay structure.
        """

        self.main_client_http_plugin = main_client_http_plugin
        self.easypay_structure = easypay_structure

    def open(self):
        """
        Opens the easypay client.
        """

        pass

    def close(self):
        """
        Closes the easypay client.
        """

        # in case an http client is defined
        if self.http_client:
            # closes the http client
            self.http_client.close({})

    def generate_easypay_structure(self, username, cin, country, language, api_version = DEFAULT_API_VERSION, set_structure = True):
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

        # in case the structure is meant to be set
        if set_structure:
            # sets the easypay structure
            self.set_easypay_structure(easypay_structure)

        # returns the easypay structure
        return easypay_structure

    def generate_reference(self, amount, reference_key, entity, reference_type = "auto", name = None, description = None, mobile = None, email = None):
        # sets the retrieval url
        retrieval_url = BASE_REST_SECURE_URL + "api_easypay_01BG.php"

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # sets the amount
        parameters["t_value"] = amount

        # sets the reference key
        parameters["t_key"] = reference_key

        # sets the entity
        parameters["ep_entity"] = entity

        # sets the reference type
        parameters["ep_ref_type"] = reference_type

        # sets the country
        parameters["ep_country"] = self.easypay_structure.country

        # sets the language
        parameters["ep_language"] = self.easypay_structure.language

        # in case the name is set
        if name:
            # sets the name
            parameters["o_name"] = name

        # in case the description is set
        if description:
            # sets the description
            parameters["o_description"] = description

        # in case the mobile is set
        if mobile:
            # sets the mobile
            parameters["o_mobile"] = mobile

        # in case the email is set
        if email:
            # sets the email
            parameters["o_email"] = email

        # fetches the retrieval url with the given parameters retrieving the xml
        result = self._fetch_url(retrieval_url, parameters)

        # parses the result (response)
        response_document = xml.dom.minidom.parseString(result)

        # retrieves the response document value
        get_reference_root_nodes = response_document.getElementsByTagName("getautoMB")

        # retrieves the get reference root node
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
        data = {}

        # sets the values in the data (map)
        data["status"] = get_reference_status
        data["message"] = get_reference_message
        data["cin"] = get_reference_cin
        data["user"] = get_reference_user
        data["entity"] = get_reference_entity
        data["reference"] = get_reference_reference
        data["value"] = get_reference_value
        data["key"] = get_reference_key
        data["link"] = get_reference_link

        # checks for easypay errors
        self._check_easypay_errors(data)

        # returns the data
        return data

    def get_payment_details(self, document_identifier, reference_key):
        # sets the retrieval url
        retrieval_url = BASE_REST_SECURE_URL + "api_easypay_03AG.php"

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # sets the document identifier
        parameters["ep_doc"] = document_identifier

        # sets the reference key
        parameters["ep_key"] = reference_key

        # fetches the retrieval url with the given parameters retrieving the xml
        result = self._fetch_url(retrieval_url, parameters)

        # parses the result (response)
        response_document = xml.dom.minidom.parseString(result)

        # retrieves the get payment details root nodes
        get_payment_details_root_nodes = response_document.getElementsByTagName("getautoMB_detail")

        # retrieves the get payment details root node
        get_payment_details_root_node = get_payment_details_root_nodes[0]

        # initializes the data (map)
        data = {}

        # retrieves the basic payment details
        get_payment_details_status = self.get_xml_node_text(get_payment_details_root_node, "ep_status")
        get_payment_details_message = self.get_xml_node_text(get_payment_details_root_node, "ep_message")
        get_payment_details_cin = self.get_xml_node_text(get_payment_details_root_node, "ep_cin")
        get_payment_details_user = self.get_xml_node_text(get_payment_details_root_node, "ep_user")
        get_payment_details_key = self.get_xml_node_text(get_payment_details_root_node, "ep_key")
        get_payment_details_transaction_key = self.get_xml_node_text(get_payment_details_root_node, "t_key")
        get_payment_details_doc = self.get_xml_node_text(get_payment_details_root_node, "ep_doc")

        # sets the values in the data (map)
        data["status"] = get_payment_details_status
        data["message"] = get_payment_details_message
        data["cin"] = get_payment_details_cin
        data["user"] = get_payment_details_user
        data["key"] = get_payment_details_key
        data["transaction_key"] = get_payment_details_transaction_key
        data["document"] = get_payment_details_doc

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

        # sets the username
        parameters["ep_user"] = self.easypay_structure.username

        # sets the cin
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

    def _check_easypay_errors(self, data):
        """
        Checks the given data for easypay errors.

        @type data: String
        @param data: The data to be checked for easypay errors.
        @rtype: bool
        @return: The result of the data error check.
        """

        # retrieves the status value
        status = data["status"]

        # retrieves the message value
        message = data["message"]

        # in case the status does not start with error
        if not status.startswith(ERROR_STATUS):
            # returns immediately
            return

        # raises the easypay api error
        raise service_easypay_exceptions.EasypayApiError("error in request: " + message)

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
            self.http_client = self.main_client_http_plugin.create_client({CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET})

            # opens the http client
            self.http_client.open({REQUEST_TIMEOUT_VALUE : DEFAULT_REQUEST_TIMEOUT})

        # returns the http client
        return self.http_client

    def get_xml_node_text(self, xml_document, xml_tag_name):
        # retrieves the xml nodes
        xml_nodes = xml_document.getElementsByTagName(xml_tag_name)

        # in case the retrieved xml
        # nodes are empty
        if not xml_nodes:
            # returns invalid
            return None

        # retrieves the xml node (first)
        xml_node = xml_nodes[0]

        # retrieves the xml node text
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
