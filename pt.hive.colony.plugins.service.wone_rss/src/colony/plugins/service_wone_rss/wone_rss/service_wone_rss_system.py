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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
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
import types
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
""" The default wone rss api version """

DEFAULT_REQUEST_TIMEOUT = 60
""" The default request timeout """

XML_TEXT_NODES = (
    xml.dom.minidom.Node.TEXT_NODE,
    xml.dom.minidom.Node.CDATA_SECTION_NODE
)
""" The xml text nodes """

class ServiceWoneRss:
    """
    The service wone rss class.
    """

    service_wone_rss_plugin = None
    """ The service wone rss plugin """

    def __init__(self, service_wone_rss_plugin):
        """
        Constructor of the class.

        @type service_wone_rss_plugin: ServiceWoneRssPlugin
        @param service_wone_rss_plugin: The service wone rss plugin.
        """

        self.service_wone_rss_plugin = service_wone_rss_plugin

    def create_remote_client(self, service_attributes):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: RssClient
        @return: The created remote client.
        """

        # retrieves the main client http plugin
        main_client_http_plugin = self.service_wone_rss_plugin.main_client_http_plugin

        # retrieves the wone rss structure (if available)
        wone_rss_structure = service_attributes.get("wone_rss_structure", None)

        # creates a new wone rss client with the given options
        wone_rss_client = WoneRssClient(main_client_http_plugin, wone_rss_structure)

        # returns the wone rss client
        return wone_rss_client

class WoneRssClient:
    """
    The class that represents a wone rss client connection.
    """

    main_client_http_plugin = None
    """ The main client http plugin """

    wone_rss_structure = None
    """ The wone rss structure """

    http_client = None
    """ The http client for the connection """

    def __init__(self, main_client_http_plugin = None, wone_rss_structure = None):
        """
        Constructor of the class.

        @type main_client_http_plugin: MainClientHttpPlugin
        @param main_client_http_plugin: The main client http plugin.
        @type wone_rss_structure: WoneRssStructure
        @param wone_rss_structure: The wone rss structure.
        """

        self.main_client_http_plugin = main_client_http_plugin
        self.wone_rss_structure = wone_rss_structure

    def open(self):
        """
        Opens the wone rss client.
        """

        pass

    def close(self):
        """
        Closes the wone rss client.
        """

        # in case an http client is defined
        if self.http_client:
            # closes the http client
            self.http_client.close({})

    def generate_wone_rss_structure(self, base_url, api_version = DEFAULT_API_VERSION, set_structure = True):
        """
        Generates the wone rss structure for the given arguments.

        @type base_url: String
        @param base_url: The username.
        @type api_version: String
        @param api_version: The version of the api being used.
        @type set_structure: bool
        @param set_structure: If the structure should be
        set in the wone rss client.
        @rtype: WoneRssStructure
        @return: The generated wone rss structure.
        """

        # creates a new wone rss structure
        wone_rss_structure = WoneRssStructure(base_url, api_version)

        # in case the structure is meant to be set
        if set_structure:
            # sets the wone rss structure
            self.set_wone_rss_structure(wone_rss_structure)

        # returns the wone rss structure structure
        return wone_rss_structure

    def get_wone_items(self):
        # sets the retrieval url
        retrieval_url = self.wone_rss_structure.base_url

        # start the parameters map
        parameters = {}

        # sets the base parameters
        self._set_base_parameters(parameters)

        # fetches the retrieval url with the given parameters retrieving the xml
        result = self._fetch_url(retrieval_url, parameters)

        # retrieves the result type
        result_type = type(result)

        # encodes the result into the default encoding in case the result is unicode
        result = result_type == types.UnicodeType and result.encode(DEFAULT_CHARSET) or result

        # parses the result (response)
        response_document = xml.dom.minidom.parseString(result)

        # retrieves the item nodes
        item_nodes = response_document.getElementsByTagName("item")

        # creates the data list
        data = []

        # iterates over all the item nodes
        for item_node in item_nodes:
            # initializes the wone deal (map)
            wone_deal = {}

            # retrieves the basic wone deal details
            wone_deal_title = self.get_xml_node_text(item_node, "title")
            wone_deal_description = self.get_xml_node_text(item_node, "description")
            wone_deal_link = self.get_xml_node_text(item_node, "link")
            wone_deal_retail_price = self.get_xml_node_text(item_node, "retail_price")
            wone_deal_discounted_price = self.get_xml_node_text(item_node, "discounted_price")
            wone_deal_expiration_date = self.get_xml_node_text(item_node, "expiration_date")
            wone_deal_image_url = self.get_xml_node_text(item_node, "image_url")
            wone_deal_category = self.get_xml_node_text(item_node, "category")
            wone_deal_city = self.get_xml_node_text(item_node, "city")
            wone_deal_latitude = self.get_xml_node_text(item_node, "latitude")
            wone_deal_longitude = self.get_xml_node_text(item_node, "longitude")

            # converts the time values
            wone_deal_expiration_date = self.__convert_date_string_timestamp(wone_deal_expiration_date)

            # sets the values in the wone deal (map)
            wone_deal["title"] = wone_deal_title
            wone_deal["description"] = wone_deal_description
            wone_deal["link"] = wone_deal_link
            wone_deal["retail_price"] = wone_deal_retail_price
            wone_deal["discounted_price"] = wone_deal_discounted_price
            wone_deal["expiration_date"] = wone_deal_expiration_date
            wone_deal["image_url"] = wone_deal_image_url
            wone_deal["category"] = wone_deal_category
            wone_deal["city"] = wone_deal_city
            wone_deal["latitude"] = wone_deal_latitude
            wone_deal["longitude"] = wone_deal_longitude

            # adds the wone deal to the data
            data.append(wone_deal)

        # checks for wone rss errors
        self._check_wone_rss_errors(data)

        # returns the data
        return data

    def get_wone_rss_structure(self):
        """
        Retrieves the wone rss structure.

        @rtype: WoneRssStructure
        @return: The wone rss structure.
        """

        return self.wone_rss_structure

    def set_wone_rss_structure(self, wone_rss_structure):
        """
        Sets the wone rss structure.

        @type wone_rss_structure: WoneRssStructure
        @param wone_rss_structure: The wone rss structure.
        """

        self.wone_rss_structure = wone_rss_structure

    def _set_base_parameters(self, parameters):
        """
        Sets the base wone rss rest request parameters
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

    def _check_wone_rss_errors(self, data):
        """
        Checks the given data for wone rss errors.

        @type data: String
        @param data: The data to be checked for wone rss errors.
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

            # defines the open parameters
            open_parameters = {
                REQUEST_TIMEOUT_VALUE : DEFAULT_REQUEST_TIMEOUT
            }

            # opens the http client
            self.http_client.open(open_parameters)

        # returns the http client
        return self.http_client

    def get_xml_node_text(self, xml_document, xml_tag_name, default_value = None):
        # retrieves the xml nodes
        xml_nodes = xml_document.getElementsByTagName(xml_tag_name)

        # in case the retrieved xml
        # nodes are empty
        if not xml_nodes:
            # returns the default value
            return default_value

        # retrieves the xml node (first)
        xml_node = xml_nodes and xml_nodes[0] or None

        # retrieves the xml node text
        xml_node_text = xml_node and self._get_xml_node_text(xml_node) or default_value

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
        signal = signal_string == "+" and -1 or 1

        # re-calculates the utc offset values
        utc_offset_hours = utc_offset_hours * signal
        utc_offset_minutes = utc_offset_minutes * signal

        # retrieves the date string partial (without utc offset)
        date_string_partial = date_string[:-6]

        # tries to convert the date using two formats
        try:
            # convert the date string partial to date time value
            date_time_value = datetime.datetime.strptime(date_string_partial, "%a, %d %b %y %H:%M:%S")
        # in case the first format conversion raises a value error
        except ValueError:
            # tries the alternative date format
            date_time_value = datetime.datetime.strptime(date_string_partial, "%a, %d %b %Y %H:%M:%S")

        try:
            # calculates the date time delta according to the offset values
            date_time_delta = datetime.timedelta(hours = utc_offset_hours, minutes = utc_offset_minutes)

            # re-calculates the date time value with the date time delta
            date_time_value = date_time_value + date_time_delta

            # retrieves the date time value tuple
            date_time_value_tuple = date_time_value.utctimetuple()

            # converts the date time value tuple to timestamp
            date_time_timestamp = time.mktime(date_time_value_tuple)
        except:
            # sets the date time timestamp to invalid
            date_time_timestamp = 0

        # returns the date time timestamp
        return date_time_timestamp

class WoneRssStructure:
    """
    The wone rss structure class.
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
