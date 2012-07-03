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

import re

import url_parser_exceptions

URL_REGEX_VALUE = "(?P<protocol>\w+\:\/\/)?((?P<authentication>\w+\:\w+)@)?(?P<base_name>[^\:\/\?#]+)(\:(?P<port>\d+))?(?P<resource_reference>(\/[^\?#]+)*)\/?(\?(?P<options>([^#])*))?(?P<location>#(.*))?"
""" The url regex value """

URL_REGEX = re.compile(URL_REGEX_VALUE)
""" The url regex """

DEFAULT_PROTOCOL_VALUE = "http://"
""" The default protocol value """

DEFAULT_PORT_VALUE = None
""" The default port value """

class UrlParser:
    """
    The url parser class.
    """

    url_parser_plugin = None
    """ The url parser plugin """

    def __init__(self, url_parser_plugin):
        """
        Constructor of the class.

        @type url_parser_plugin: UrlParserPlugin
        @param url_parser_plugin: The url parser plugin.
        """

        self.url_parser_plugin = url_parser_plugin

    def parse_url(self, url):
        """
        Parses the given url retrieving the url object.

        @type url: String
        @param url:  The url to be parsed.
        @rtype: Url
        @return: The url object representing the url
        """

        # saves the url reference
        url_reference = url

        # creates the url object
        url = Url()

        # parses the url (reference)
        url.parse_url(url_reference)

        # generates the resource reference list
        url._generate_resource_reference_list()

        # generates the options map
        url._generate_options_map()

        # returns the url
        return url

class Url:
    """
    The url class.
    """

    protocol = DEFAULT_PROTOCOL_VALUE
    """ The protocol """

    username = None
    """ The username """

    password = None
    """ The password """

    base_name = None
    """ The base name """

    port = DEFAULT_PORT_VALUE
    """ The port """

    resource_reference = None
    """ The resource reference """

    resource_reference_list = []
    """ The resource reference list """

    options = None
    """ The options """

    options_map = {}
    """ The options map """

    location = None
    """ The location """

    base_url = None
    """ The base url """

    def __init__(self, protocol = DEFAULT_PROTOCOL_VALUE, username = None, password = None, base_name = None, port = DEFAULT_PORT_VALUE, resource_reference = None, options = None, location = None, base_url = None):
        """
        Constructor of the class.

        @type protocol: String
        @param protocol: The protocol.
        @type username: String
        @param username: The username.
        @type password: String
        @param password: The password.
        @type base_name: String
        @param base_name: The base name.
        @type port: int
        @param port: The port.
        @type resource_reference: String
        @param resource_reference: The resource reference.
        @type options: String
        @param options: The options.
        @type location: String
        @param location: The location.
        @type base_url: String
        @param base_url: The base url.
        """

        self.protocol = protocol
        self.username = username
        self.password = password
        self.base_name = base_name
        self.port = port
        self.resource_reference = resource_reference
        self.options = options
        self.location = location
        self.base_url = base_url

        self.resource_reference_list = []
        self.options_map = {}

    def build_url(self):
        """
        Builds the url for the current options.
        """

        # generates the resource reference
        self._generate_resource_reference()

        # generates the options
        self._generate_options()

        # creates the url
        url = self.protocol + self.base_name

        # in case the protocol port is not the default one
        if not self.protocol == DEFAULT_PROTOCOL_VALUE or not self.port == DEFAULT_PORT_VALUE:
            url += ":" + str(self.port)

        # adds the resource reference to the url
        url += self.resource_reference

        # in case options is defined
        if self.options:
            url += "?" + self.options

        # returns the url
        return url

    def parse_url(self, url):
        """
        Parses the given url retrieving setting url object.

        @type url: String
        @param url:  The url to be parsed.
        """

        # matches the url against the url regex
        url_match = URL_REGEX.match(url)

        # in case there was no match
        if not url_match:
            # raises the url parser exception
            raise url_parser_exceptions.UrlParserException("invalid url value: %s" % url)

        # retrieves the protocol
        protocol = url_match.group("protocol")

        # retrieves the authentication
        authentication = url_match.group("authentication")

        # retrieves the base name
        base_name = url_match.group("base_name")

        # retrieves the port
        port = url_match.group("port")

        # retrieves the resource reference
        resource_reference = url_match.group("resource_reference")

        # retrieves the options
        options = url_match.group("options")

        # retrieves the location
        location = url_match.group("location")

        # in case the protocol is valid
        if protocol:
            # sets the protocol
            self.protocol = protocol

        # in case the protocol is valid
        if authentication:
            # retrieves the username and password from the
            # authentication token
            username, password = authentication.split(":", 1)

            # sets the username
            self.username = username

            # sets the password
            self.password = password

        # in case the base name is valid
        if base_name:
            # sets the base name
            self.base_name = base_name

        # in case the port is valid
        if port:
            # sets the port
            self.port = int(port)

        # in case the resource reference is valid
        if resource_reference:
            # sets the resource reference
            self.resource_reference = resource_reference

            # generates the resource reference list
            self._generate_resource_reference_list()

        # in case options is valid
        if options:
            # sets the options
            self.options = options

            # generates the options map
            self._generate_options_map()

        # in case location is valid
        if location:
            # sets the location
            self.location = location

        # creates the base url from the protocol, authentication, base name and port
        self.base_url = (protocol or "") + (authentication and authentication + "@" or "") + (base_name or "") + (port and ":" + port or "")

    def add_resource_reference_item(self, resource_reference_item):
        """
        Adds the given resource reference item to the resource reference list.

        @type resource_reference_item: Object
        @param resource_reference_item: The resource reference to be added.
        """

        # adds the resource reference item to the resource reference list
        self.resource_reference_list.append(resource_reference_item)

    def remove_resource_reference_item(self, resource_reference_item):
        """
        Removes the given resource reference item from the resource reference list.

        @type resource_reference_item: Object
        @param resource_reference_item: The resource reference to be removed.
        """

        # removes the resource reference item to the resource reference list
        self.resource_reference_list.remove(resource_reference_item)

    def add_option(self, option_key, option_value):
        """
        Adds the given option to the options map.

        @type option_key: String
        @param option_key: The option key to be added.
        @type option_value: Object
        @param option_value: The option value to be added.
        """

        # adds the option value to the options map
        self.options_map[option_key] = option_value

    def remove_option(self, option_key):
        """
        Removes the given option from the options map.

        @type option_key: String
        @param option_key: The option key to be removed.
        """

        # deletes the option from the options map
        del self.options_map[option_key]

    def get_protocol(self):
        """
        Retrieves the protocol.

        @rtype: String
        @return: The protocol.
        """

        return self.protocol

    def set_protocol(self, protocol):
        """
        Sets the protocol.

        @type protocol: String
        @param protocol: The protocol.
        """

        self.protocol = protocol

    def get_base_name(self):
        """
        Retrieves the base name.

        @rtype: String
        @return: The base name.
        """

        return self.base_name

    def set_base_name(self, base_name):
        """
        Sets the base name.

        @type base_name: String
        @param base_name: The protocol.
        """

        self.base_name = base_name

    def get_port(self):
        """
        Retrieves the port.

        @rtype: int
        @return: The port.
        """

        return self.port

    def set_port(self, port):
        """
        Sets the port.

        @type port: int
        @param port: The port.
        """

        self.port = port

    def get_resource_reference(self):
        """
        Retrieves the resource reference.

        @rtype: String
        @return: The resource reference.
        """

        return self.resource_reference

    def set_resource_reference(self, resource_reference):
        """
        Sets the resource reference.

        @type resource_reference: String
        @param resource_reference: The resource reference.
        """

        self.resource_reference = resource_reference

    def get_resource_reference_list(self):
        """
        Retrieves the resource reference list.

        @rtype: String
        @return: The resource reference list.
        """

        return self.resource_reference_list

    def set_resource_reference_list(self, resource_reference_list):
        """
        Sets the resource reference list.

        @type resource_reference_list: String
        @param resource_reference_list: The resource reference list.
        """

        self.resource_reference_list = resource_reference_list

    def get_options(self):
        """
        Retrieves the options.

        @rtype: String
        @return: The options.
        """

        return self.options

    def set_options(self, options):
        """
        Sets the options.

        @type options: String
        @param options: The options.
        """

        self.options = options

    def get_options_map(self):
        """
        Retrieves the options map.

        @rtype: Dictionary
        @return: The options map.
        """

        return self.options_map

    def set_options_map(self, options_map):
        """
        Sets the options map.

        @type options_map: Dictionary
        @param options_map: The options map.
        """

        self.options_map = options_map

    def get_location(self):
        """
        Retrieves the location.

        @rtype: String
        @return: The location.
        """

        return self.location

    def set_location(self, location):
        """
        Sets the location.

        @type location: String
        @param location: The location.
        """

        self.location = location

    def _generate_resource_reference(self):
        """
        Generates the resource reference.
        """

        # is case the resource reference list is invalid
        if not self.resource_reference_list:
            # returns immediately
            return

        self.resource_reference = "/" + "/".join(self.resource_reference_list)

    def _generate_options(self):
        """
        Generates the options map.
        """

        # is case the options map is invalid
        if not self.options_map:
            # returns immediately
            return

        self.options = "&".join([key + "=" + value for key, value in self.options_map.items()])

    def _generate_resource_reference_list(self):
        """
        Generates the resource reference list.
        """

        # is case the resource reference is invalid
        if not self.resource_reference:
            # returns immediately
            return

        # strips the resource reference
        resource_reference_stripped = self.resource_reference.strip("/")

        # splits the options around the and operator
        resource_reference_splitted = resource_reference_stripped.split("/")

        # sets the resource reference list as the resource reference splitted
        self.resource_reference_list = resource_reference_splitted

    def _generate_options_map(self):
        """
        Generates the options map.
        """

        # is case the options are invalid
        if not self.options:
            # returns immediately
            return

        # splits the options around the and operator
        options_splitted = self.options.split("&")

        # iterates over all the options splitted
        for option_splitted in options_splitted:
            # retrieves the key and the value from
            # the options splitted
            key, value = option_splitted.split("=")

            # sets the value in the options map
            self.options_map[key] = value
