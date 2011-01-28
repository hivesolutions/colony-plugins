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

import time
import datetime

import xml.dom.minidom

DEFAULT_CHARSET = "utf-8"
""" The default charset """

GET_METHOD_VALUE = "GET"
""" The get method value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

REQUEST_TIMEOUT_VALUE = "request_timeout"
""" The request timeout value """

DEFAULT_API_VERSION = "1.0"
""" The default bargnia rss api version """

DEFAULT_REQUEST_TIMEOUT = 60
""" The default request timeout """

XML_TEXT_NODES = (xml.dom.minidom.Node.TEXT_NODE, xml.dom.minidom.Node.CDATA_SECTION_NODE)
""" The xml text nodes """

class ServiceBarganiaRss:
    """
    The service bargania rss class.
    """

    service_bargania_rss_plugin = None
    """ The service bargania rss plugin """

    def __init__(self, service_bargania_rss_plugin):
        """
        Constructor of the class.

        @type service_bargania_rss_plugin: ServiceBarganiaRssPlugin
        @param service_bargania_rss_plugin: The service bargania rss plugin.
        """

        self.service_bargania_rss_plugin = service_bargania_rss_plugin

    def create_remote_client(self, service_attributes):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: easypayClient
        @return: The created remote client.
        """

        # retrieves the main client http plugin
        main_client_http_plugin = self.service_bargania_rss_plugin.main_client_http_plugin

        # retrieves the bargania rss structure (if available)
        bargania_rss_structure = service_attributes.get("bargania_rss_structure", None)

        # creates a new bargania rss client with the given options
        bargania_rss_client = BarganiaRssClient(main_client_http_plugin, bargania_rss_structure)

        # returns the bargania rss client
        return bargania_rss_client

class BarganiaRssClient:
    """
    The class that represents a bargania rss client connection.
    """

    main_client_http_plugin = None
    """ The main client http plugin """

    bargania_rss_structure = None
    """ The bargania rss structure """

    http_client = None
    """ The http client for the connection """

    def __init__(self, main_client_http_plugin = None, bargania_rss_structure = None):
        """
        Constructor of the class.

        @type main_client_http_plugin: MainClientHttpPlugin
        @param main_client_http_plugin: The main client http plugin.
        @type bargania_rss_structure: BargniaRssStructure
        @param bargania_rss_structure: The bargania rss structure.
        """

        self.main_client_http_plugin = main_client_http_plugin
        self.bargania_rss_structure = bargania_rss_structure

    def open(self):
        """
        Opens the bargnia rss client.
        """

        pass

    def close(self):
        """
        Closes the bargania rss client.
        """

        # in case an http client is defined
        if self.http_client:
            # closes the http client
            self.http_client.close({})

    def generate_bargania_rss_structure(self, base_url, api_version = DEFAULT_API_VERSION, set_structure = True):
        """
        Generates the bargania rss structure for the given arguments.

        @type base_url: String
        @param base_url: The username.
        @type api_version: String
        @param api_version: The version of the api being used.
        @type set_structure: bool
        @param set_structure: If the structure should be
        set in the bargania rss client.
        @rtype: BarganiaRssStructure
        @return: The generated bargania rss structure.
        """

        # creates a new bargania rss structure
        bargania_rss_structure = BarganiaRssStructure(base_url, api_version)

        # in case the structure is meant to be set
        if set_structure:
            # sets the bargania rss structure
            self.set_bargania_rss_structure(bargania_rss_structure)

        # returns the bargania rss structure structure
        return bargania_rss_structure

    def get_bargania_items(self):
        # sets the retrieval url
        retrieval_url = self.bargania_rss_structure.base_url

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # fetches the retrieval url with the given parameters retrieving the xml
        result = self._fetch_url(retrieval_url, parameters)

        # parses the result (response)
        response_document = xml.dom.minidom.parseString(result)

        # retrieves the item nodes
        item_nodes = response_document.getElementsByTagName("item")

        # creates the data list
        data = []

        # iterates over all the item nodes
        for item_node in item_nodes:
            # initializes the bargania deal (map)
            bargania_deal = {}

            # retrieves the bargania deal nodes
            bargania_deal_nodes = item_node.getElementsByTagName("bargania:deal")

            # retrieves the first bargania deal node
            bargania_deal_node = bargania_deal_nodes[0]

            # retrieves the basic bargania deal details
            bargania_deal_object_id = self.get_xml_node_text(bargania_deal_node, "bargania:object_id")
            bargania_deal_provider_id = self.get_xml_node_text(bargania_deal_node, "bargania:provider_id")
            bargania_deal_status = self.get_xml_node_text(bargania_deal_node, "bargania:status")
            bargania_deal_title = self.get_xml_node_text(bargania_deal_node, "bargania:title")
            bargania_deal_description = self.get_xml_node_text(item_node, "bargania:description")
            bargania_deal_details_url = self.get_xml_node_text(item_node, "bargania:details_url")
            bargania_deal_purchase_url = self.get_xml_node_text(item_node, "bargania:purchase_url")
            bargania_deal_retail_price = self.get_xml_node_text(item_node, "bargania:retail_price")
            bargania_deal_discounted_price = self.get_xml_node_text(item_node, "bargania:discounted_price")
            bargania_deal_number_purchases = self.get_xml_node_text(item_node, "bargania:number_purchases")
            bargania_deal_minimum_purchases = self.get_xml_node_text(item_node, "bargania:minimum_purchases")
            bargania_deal_maximum_purchases = self.get_xml_node_text(item_node, "bargania:maximum_purchases")
            bargania_deal_expiration_date = self.get_xml_node_text(item_node, "bargania:expiration_date")

            # retrieves the bargania deal relations
            bargania_deal_advertisement_media = self._get_media(item_node, "bargania:advertisement_media")
            bargania_deal_store = self._get_store(item_node, "bargania:store")
            bargania_deal_primary_address = self._get_address(item_node, "bargania:primary_address")
            bargania_deal_primary_contact_information = self._get_contact_information(item_node, "bargania:primary_contact_information")

            # converts the time values
            bargania_deal_expiration_date = self.__convert_date_string_timestamp(bargania_deal_expiration_date)

            # sets the values in the bargania deal (map)
            bargania_deal["object_id"] = bargania_deal_object_id
            bargania_deal["provider_id"] = bargania_deal_provider_id
            bargania_deal["status"] = bargania_deal_status
            bargania_deal["title"] = bargania_deal_title
            bargania_deal["description"] = bargania_deal_description
            bargania_deal["details_url"] = bargania_deal_details_url
            bargania_deal["purchase_url"] = bargania_deal_purchase_url
            bargania_deal["retail_price"] = bargania_deal_retail_price
            bargania_deal["discounted_price"] = bargania_deal_discounted_price
            bargania_deal["number_purchases"] = bargania_deal_number_purchases
            bargania_deal["minimum_purchases"] = bargania_deal_minimum_purchases
            bargania_deal["maximum_purchases"] = bargania_deal_maximum_purchases
            bargania_deal["expiration_date"] = bargania_deal_expiration_date

            # sets the relations in the bargania deal (map)
            bargania_deal["advertisement_media"] = [bargania_deal_advertisement_media]
            bargania_deal["store"] = bargania_deal_store
            bargania_deal["primary_address"] = bargania_deal_primary_address
            bargania_deal["primary_contact_information"] = bargania_deal_primary_contact_information

            # adds the bargania deal to the data
            data.append(bargania_deal)

        # checks for bargania rss errors
        self._check_bargania_rss_errors(data)

        # returns the data
        return data

    def get_bargania_rss_structure(self):
        """
        Retrieves the bargania rss structure.

        @rtype: BarganiaRssStructure
        @return: The bargania rss structure.
        """

        return self.bargania_rss_structure

    def set_bargania_rss_structure(self, bargania_rss_structure):
        """
        Sets the bargania rss structure.

        @type bargania_rss_structure: BarganiaRssStructure
        @param bargania_rss_structure: The bargania rss structure.
        """

        self.bargania_rss_structure = bargania_rss_structure

    def _set_base_parameters(self, parameters):
        """
        Sets the base bargania rss rest request parameters
        in the parameters map.

        @type parameters: Dictionary
        @param parameters: The parameters map to be used in setting
        the base parameters.
        """

        pass

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

    def _check_bargania_rss_errors(self, data):
        """
        Checks the given data for bargania rss errors.

        @type data: String
        @param data: The data to be checked for bargania rss errors.
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
        child_node_data_list = [child_node.data for child_node in child_nodes if child_node.nodeType in XML_TEXT_NODES]

        # converts the child text nodes to a string
        xml_node_text = "".join(child_node_data_list)

        # returns the xml node text
        return xml_node_text

    def _get_media(self, item_node, advertisement_media_node_name):
        # creates the media map
        media = {}

        # retrieves the media nodes
        media_nodes = item_node.getElementsByTagName(advertisement_media_node_name)

        # in case the media nodes is not valid
        if not media_nodes:
            # returns invalid
            return None

        # retrieves the media node
        media_node = media_nodes[0]

        # retrieves the basic media details
        media_object_id = self.get_xml_node_text(media_node, "bargania:object_id")
        media_url = self.get_xml_node_text(media_node, "bargania:source_url")

        # sets the values in the media (map)
        media["object_id"] = media_object_id
        media["source_url"] = media_url

        # returns the media
        return media

    def _get_store(self, item_node, store_node_name):
        # creates the store map
        store = {}

        # retrieves the store nodes
        store_nodes = item_node.getElementsByTagName(store_node_name)

        # in case the store nodes is not valid
        if not store_nodes:
            # returns invalid
            return None

        # retrieves the store node
        store_node = store_nodes[0]

        # retrieves the basic store details
        store_object_id = self.get_xml_node_text(store_node, "bargania:object_id")
        store_name = self.get_xml_node_text(store_node, "bargania:name")
        store_description = self.get_xml_node_text(store_node, "bargania:description")

        # retrieves the store relations
        store_primary_address = self._get_address(store_node, "bargania:primary_address")
        store_primary_contact_information = self._get_contact_information(store_node, "bargania:primary_contact_information")
        store_logotype_media = self._get_media(store_node, "bargania:logotype_media")

        # sets the values in the store (map)
        store["object_id"] = store_object_id
        store["name"] = store_name
        store["description"] = store_description

        # sets the relations in the store (map)
        store["primary_address"] = store_primary_address
        store["primary_contact_information"] = store_primary_contact_information
        store["logotype_media"] = store_logotype_media

        # returns the store
        return store

    def _get_address(self, item_node, address_node_name):
        # creates the address map
        address = {}

        # retrieves the address nodes
        address_nodes = item_node.getElementsByTagName(address_node_name)

        # in case the address nodes is not valid
        if not address_nodes:
            # returns invalid
            return None

        # retrieves the address node
        address_node = address_nodes[0]

        # retrieves the basic address details
        address_object_id = self.get_xml_node_text(address_node, "bargania:object_id")
        address_street_name = self.get_xml_node_text(address_node, "bargania:street_name")
        address_city = self.get_xml_node_text(address_node, "bargania:city")
        address_postal_code = self.get_xml_node_text(address_node, "bargania:postal_code")
        address_province = self.get_xml_node_text(address_node, "bargania:province")
        address_country = self.get_xml_node_text(address_node, "bargania:country")
        address_latitude = self.get_xml_node_text(address_node, "bargania:latitude")
        address_longitude = self.get_xml_node_text(address_node, "bargania:longitude")

        # sets the values in the address (map)
        address["street_name"] = address_object_id
        address["street_name"] = address_street_name
        address["city"] = address_city
        address["postal_code"] = address_postal_code
        address["province"] = address_province
        address["country"] = address_country
        address["latitude"] = address_latitude
        address["longitude"] = address_longitude

        # returns the address
        return address

    def _get_contact_information(self, item_node, contact_information_node_name):
        # creates the contact information map
        contact_information = {}

        # retrieves the contact information nodes
        contact_information_nodes = item_node.getElementsByTagName(contact_information_node_name)

        # in case the contact information nodes is not valid
        if not contact_information_nodes:
            # returns invalid
            return None

        # retrieves the contact information node
        contact_information_node = contact_information_nodes[0]

        # retrieves the basic contact information details
        contact_information_object_id = self.get_xml_node_text(contact_information_node, "bargania:object_id")
        contact_information_phone_number = self.get_xml_node_text(contact_information_node, "bargania:phone_number")
        contact_information_fax_number = self.get_xml_node_text(contact_information_node, "bargania:fax_number")
        contact_information_email = self.get_xml_node_text(contact_information_node, "bargania:email")
        contact_information_website = self.get_xml_node_text(contact_information_node, "bargania:website")

        # sets the values in the contact information (map)
        contact_information["object_id"] = contact_information_object_id
        contact_information["phone_number"] = contact_information_phone_number
        contact_information["fax_number"] = contact_information_fax_number
        contact_information["email"] = contact_information_email
        contact_information["website"] = contact_information_website

        # returns the contact information
        return contact_information

    def __convert_date_string_timestamp(self, date_string):
        # retrieves the utc offset strings
        utc_offset_hours_string = date_string[-4:-2]
        utc_offset_minutes_string = date_string[-2:]

        # converts the utc offset to integer
        utc_offset_hours = int(utc_offset_hours_string)
        utc_offset_minutes = int(utc_offset_minutes_string)

        # retrieves the signal string
        signal_string = date_string[-5]

        # converts the signal to integer (multiplier)
        signal = signal_string == "-" and -1 or 1

        # re-calculates the utc offset values
        utc_offset_hours = utc_offset_hours * signal
        utc_offset_minutes = utc_offset_minutes * signal

        # retrieves the date string partial (without utc offset)
        date_string_partial = date_string[:-6]

        # convert the date string partial to date time value
        date_time_value = datetime.datetime.strptime(date_string_partial, "%a, %d %b %Y %H:%M:%S")

        try:
            # calculates the date time delta according to the offset values
            date_time_delta = datetime.timedelta(hours = utc_offset_hours, minutes = utc_offset_minutes)

            # re-calculates the date time value with the date time delta
            date_time_value = date_time_value + date_time_delta

            # retrieves the date time value tuple
            date_time_value_tuple = date_time_value.timetuple()

            # converts the date time value tuple to timestamp
            date_time_timestamp = time.mktime(date_time_value_tuple)
        except:
            # sets the date time timestamp to invalid
            date_time_timestamp = 0

        # returns the date time timestamp
        return date_time_timestamp

class BarganiaRssStructure:
    """
    The bargnia rss structure class.
    """

    base_url = None
    """ The base url for retrieval """

    api_version = None
    """ The version of the api being used """

    def __init__(self, base_url, api_version = DEFAULT_API_VERSION):
        """
        Constructor of the class.

        @type base_url: String
        @param base_url: The base url for retrieval.
        @type api_version: String
        @param api_version: The version of the api being used.
        """

        self.base_url = base_url
        self.api_version = api_version

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
