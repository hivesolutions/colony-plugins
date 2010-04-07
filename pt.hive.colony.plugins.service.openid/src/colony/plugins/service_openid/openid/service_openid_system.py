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

import urllib
import urllib2

import service_openid_parser
import service_openid_exceptions

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

HTTP_URI_VALUE = "http://"
""" The http uri value """

HTTPS_URI_VALUE = "https://"
""" The https uri value """

XRI_URI_VALUE = "xri://="
""" The xri uri value """

XRI_INITIALIZER_VALUE = "="
""" The xri initializer value """

OPENID_NAMESPACE_VALUE = "http://specs.openid.net/auth/2.0"
""" The openid namespace value """

ASSOCIATE_MODE_VALUE = "associate"
""" The associate mode value """

CHECKID_SETUP_VALUE = "checkid_setup"
""" The checkid setup value """

CHECKID_IMMEDIATE_VALUE = "checkid_immediate"
""" The checkid immediate value """

XRDS_LOCATION_VALUE = "x-xrds-location"
""" The xrds location value """

DEFAULT_OPENID_ASSOCIATE_TYPE = "HMAC-SHA1"
""" The default openid associate type """

DEFAULT_OPENID_SESSION_TYPE = "no-encryption"
""" The default openid session type """

class ServiceOpenid:
    """
    The service openid class.
    """

    service_openid_plugin = None
    """ The service openid plugin """

    def __init__(self, service_openid_plugin):
        """
        Constructor of the class.

        @type service_openid_plugin: ServiceOpenidPlugin
        @param service_openid_plugin: The service openid plugin.
        """

        self.service_openid_plugin = service_openid_plugin

    def create_remote_client(self, service_attributes):
        """
        Creates a remote client, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @rtype: OpenidClient
        @return: The created remote client.
        """

        # retrieves the service yadis plugin
        service_yadis_plugin = self.service_openid_plugin.service_yadis_plugin

        # retrieves the openid structure (if available)
        openid_structure = service_attributes.get("openid_structure", None)

        # creates the openid client
        openid_client = OpenidClient(self.service_openid_plugin, service_yadis_plugin, urllib2, openid_structure)

        # returns the openid client
        return openid_client

class OpenidServer:
    """
    The class that represents an openid server connection.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

class OpenidClient:
    """
    The class that represents an openid client connection.
    """

    service_openid_plugin = None
    """ The service openid plugin """

    service_yadis_plugin = None
    """ The service yadis plugin """

    http_client_plugin = None
    """ The http client plugin """

    openid_structure = None
    """ The openid structure """

    def __init__(self, service_openid_plugin = None, service_yadis_plugin = None, http_client_plugin = None, openid_structure = None):
        """
        Constructor of the class.

        @type service_openid_plugin: ServiceOpenidPlugin
        @param service_openid_plugin: The service openid plugin.
        @type service_yadis_plugin: ServiceYadisPlugin
        @param service_yadis_plugin: The service yadis plugin.
        @type http_client_plugin: HttpClientPlugin
        @param http_client_plugin: The http client plugin.
        @type openid_structure: OpenidStructure
        @param openid_structure: The openid structure.
        """

        self.service_openid_plugin = service_openid_plugin
        self.service_yadis_plugin = service_yadis_plugin
        self.http_client_plugin = http_client_plugin
        self.openid_structure = openid_structure

    def generate_openid_structure(self, provider_url, claimed_id, identity, return_to, realm, association_type = DEFAULT_OPENID_ASSOCIATE_TYPE, session_type = DEFAULT_OPENID_SESSION_TYPE, set_structure = True):
        # creates a new openid structure
        openid_structure = OpenidStructure(provider_url, claimed_id, identity, return_to, realm, association_type, session_type)

        # in case the structure is meant to be set
        if set_structure:
            # sets the openid structure
            self.set_openid_structure(openid_structure)

        # returns the openid structure
        return openid_structure

    def normalize_claimed_id(self, claimed_id):
        """
        Normalizes the claimed id according to the
        openid specification.

        @type claimed_id: String
        @param claimed_id: The claimed id to be normalized.
        @rtype: String
        @return: The normalized claimded id.
        """

        # strips the claimed id from trailing spaces
        claimed_id = claimed_id.strip()

        # in case the claimed id is not xri and starts with the correct uri
        if not claimed_id.startswith(HTTP_URI_VALUE) and not claimed_id.startswith(HTTPS_URI_VALUE) and not claimed_id.startswith(XRI_URI_VALUE) and not claimed_id.startswith(XRI_INITIALIZER_VALUE):
            # adds the http uri to the claimed id
            claimed_id = HTTP_URI_VALUE + claimed_id
        # in case the claimed id is of type xri
        elif claimed_id.startswith(XRI_URI_VALUE):
            # removes the xri uri from the claimed id
            claimed_id = claimed_id[6:]

        # returns the claimed id
        return claimed_id

    def openid_discover(self):
        """
        Initializes the discovery process according to the
        openid specification.

        @rtype: OpenidStructure
        @return: The current openid structure.
        """

        # retrieves the yadis provider url
        yadis_provider_url = self._get_yadis_provider_url()

        # creates a new yadis remote client
        yadis_remote_client = self.service_yadis_plugin.create_remote_client({})

        # generates the yadis structure
        yadis_remote_client.generate_yadis_structure(yadis_provider_url)

        # retrieves the resource descriptor
        resource_descriptor = yadis_remote_client.get_resource_descriptor()

        # retrieves the resources list
        resources_list = resource_descriptor.get_resources_list()

        # retrieves the first service from the resources list
        first_service = resources_list[0].services_list[0]

        # retrieves the provider url
        provider_url = first_service.get_attribute("URI")

        # sets the provider url in the open id structure
        self.openid_structure.provider_url = provider_url

        # prints a debug message
        self.service_openid_plugin.debug("Found openid provider url '%s'" % provider_url)

    def openid_associate(self):
        """
        Requests an association (associate mode) according to the
        openid specification.

        @rtype: OpenidStructure
        @return: The current openid structure.
        """

        # sets the retrieval url
        retrieval_url = self.openid_structure.provider_url

        # start the parameters map
        parameters = {}

        # sets the namespace as the openid default namespace
        parameters["openid.ns"] = OPENID_NAMESPACE_VALUE

        # sets the mode as associate
        parameters["openid.mode"] = ASSOCIATE_MODE_VALUE

        # sets the association type
        parameters["openid.assoc_type"] = self.openid_structure.association_type

        # sets the session type
        parameters["openid.session_type"] = self.openid_structure.session_type

        # fetches the retrieval url with the given parameters retrieving the result
        result = self._fetch_url(retrieval_url, parameters, method = POST_METHOD_VALUE)

        # strips the result value
        result = result.strip()

        # retrieves the values from the request
        values = result.split("\n")

        # retrieves the values list
        values_list = [value.split(":", 1) for value in values]

        # converts the values list into a map
        values_map = dict(values_list)

        # retrieves the expiration from the values map
        self.openid_structure.expires_in = values_map.get("expires_in", None)

        # retrieves the association handle from the values map
        self.openid_structure.association_handle = values_map.get("assoc_handle", None)

        # retrieves the mac key from the values map
        self.openid_structure.mac_key = values_map.get("mac_key", None)

        # returns the openid structure
        return self.openid_structure

    def get_request_url(self):
        """
        Retrieves the request url according to the
        openid specification.

        @rtype: String
        @return: The request url.
        """

        # sets the retrieval url
        retrieval_url = self.openid_structure.provider_url

        # start the parameters map
        parameters = {}

        # sets the namespace as the openid default namespace
        parameters["openid.ns"] = OPENID_NAMESPACE_VALUE

        # sets the mode as checkid setup
        parameters["openid.mode"] = CHECKID_SETUP_VALUE

        # sets the claimed id
        parameters["openid.claimed_id"] = self.openid_structure.claimed_id

        # sets the identity
        parameters["openid.identity"] = self.openid_structure.identity

        # sets the association handle
        parameters["openid.assoc_handle"] = self.openid_structure.association_handle

        # sets the return to
        parameters["openid.return_to"] = self.openid_structure.return_to

        # sets the realm
        parameters["openid.realm"] = self.openid_structure.realm

        # creates the request url from the parameters
        request_url = self._build_url(retrieval_url, parameters)

        # returns the request url
        return request_url

    def get_openid_structure(self):
        """
        Retrieves the openid structure.

        @rtype: OpenidStructure
        @return: The openid structure.
        """

        return self.openid_structure

    def set_openid_structure(self, openid_structure):
        """
        Sets the openid structure.

        @type openid_structure: OpenidStructure
        @param openid_structure: The openid structure.
        """

        self.openid_structure = openid_structure

    def _get_yadis_provider_url(self):
        """
        Retrieves the "yadis" provider url, using the two base strategies
        (the header and the html header strategies).

        @rtype: String
        @return: The "yadis" provider url.
        """

        # sets the retrieval url
        retrieval_url = self.openid_structure.claimed_id

        # start the parameters map
        parameters = {}

        # fetches the retrieval url with the given parameters retrieving the result
        result, headers_map = self._fetch_url(retrieval_url, parameters, headers = True)

        # tries to retrieve the yadis provider url
        yadis_provider_url = headers_map.get(XRDS_LOCATION_VALUE, None)

        # in case a valid yadis provider
        # url was discovered
        if yadis_provider_url:
            # returns the yadis provider url
            return yadis_provider_url

        # creates a new yadis html parser
        yadis_html_parser = service_openid_parser.YadisHtmlParser()

        try:
            # feeds the result to the yadis html parser
            yadis_html_parser.feed(result)
        except Exception, exception:
            # prints an info message
            self.service_openid_plugin.info("There was a problem parsing yadis html: %s" % str(exception))

        # retrieves the yadis provider url
        yadis_provider_url = yadis_html_parser.yadis_provider_url

        # in case a valid yadis provider
        # url was discovered
        if yadis_provider_url:
            # returns the yadis provider url
            return yadis_provider_url

        # in case no valid yadis provider url is set
        if not yadis_provider_url:
            # raises the invalid data exception
            raise service_openid_exceptions.InvalidData("no valid yadis provider url found")

    def _get_opener(self, url):
        """
        Retrieves the opener to the connection.

        @type url: String
        @param url: The url to create the opener.
        @rtype: Opener
        @return: The opener to the connection.
        """

        # builds the opener
        opener = urllib2.build_opener()

        # returns the opener
        return opener

    def _fetch_url(self, url, parameters = None, post_data = None, method = GET_METHOD_VALUE, headers = False):
        """
        Fetches the given url for the given parameters, post data and using the given method.

        @type url: String
        @param url: The url to be fetched.
        @type parameters: Dictionary
        @param parameters: The parameters to be used the fetch.
        @type post_data: Dictionary
        @param post_data: The post data to be used the fetch.
        @type method: String
        @param method: The method to be used in the fetch.
        @type headers: bool
        @param headers: If the headers should be returned.
        @rtype: String
        @return: The fetched data.
        """

        # in case parameters is not defined
        if not parameters:
            # creates a new parameters map
            parameters = {}

        # in case post data is not defined
        if not post_data:
            # creates a new post data map
            post_data = {}

        if method == GET_METHOD_VALUE:
            pass
        elif method == POST_METHOD_VALUE:
            post_data = parameters

        # builds the url
        url = self._build_url(url, parameters)

        # encodes the post data
        encoded_post_data = self._encode_post_data(post_data)

        # retrieves the opener for the given url
        opener = self._get_opener(url)

        # opens the url with the given encoded post data
        url_structure = opener.open(url, encoded_post_data)

        # reads the contents from the url structure
        contents = url_structure.read()

        # in case the headers flag is set
        if headers:
            # creates the headers map
            headers_map = dict(url_structure.info().items())

            # returns the contents and the headers map
            return contents, headers_map
        else:
            # returns the contents
            return contents

    def _build_url(self, url, parameters):
        """
        Builds the url for the given url and parameters.

        @type url: String
        @param url: The base url to be used.
        @type parameters: Dictionary
        @param parameters: The parameters to be used for url construction.
        @rtype: String
        @return: The built url for the given parameters.
        """

        # in case the parameters are valid and the length
        # of them is greater than zero
        if parameters and len(parameters) > 0:
            # retrieves the extra query
            extra_query = self._encode_parameters(parameters)

            # adds it to the url
            url += "?" + extra_query

        # returns the url
        return url

    def _encode_parameters(self, parameters):
        """
        Encodes the given parameters into url encoding.

        @type parameters: Dictionary
        @param parameters: The parameters map to be encoded.
        @rtype: String
        @return: The encoded parameters.
        """

        # in case the parameters are defined
        if parameters:
            # returns the encoded parameters
            return urllib.urlencode(dict([(parameter_key, self._encode(parameter_value)) for parameter_key, parameter_value in parameters.items() if parameter_value is not None]))
        else:
            # returns none
            return None

    def _encode_post_data(self, post_data):
        """
        Encodes the post data into url encoding.

        @type post_data: Dictionary
        @param post_data: The post data map to be encoded.
        @rtype: String
        @return: The encoded post data.
        """

        # in case the post data is defined
        if post_data:
            # returns the encoded post data
            return urllib.urlencode(dict([(post_data_key, self._encode(post_data_value)) for post_data_key, post_data_value in post_data.items()]))
        else:
            # returns none
            return None

    def _encode(self, string_value):
        """
        Encodes the given string value to the current encoding.

        @type string_value: String
        @param string_value: The string value to be encoded.
        @rtype: String
        @return: The given string value encoded in the current encoding.
        """

        return unicode(string_value).encode("utf-8")

class OpenidStructure:
    """
    The openid structure class.
    """

    provider_url = None
    """ The url of the openid provider """

    claimed_id = None
    """ The id being claimed """

    identity = None
    """ The identity of the authentication """

    return_to = None
    """ The return to url to be used after authentication """

    realm = None
    """ The realm to be used during the authentication """

    association_type = None
    """ The association type """

    session_type = None
    """ The session type """

    def __init__(self, provider_url, claimed_id, identity, return_to, realm, association_type = DEFAULT_OPENID_ASSOCIATE_TYPE, session_type = DEFAULT_OPENID_SESSION_TYPE):
        """
        Constructor of the class.

        @type provider_url: String
        @param provider_url: The url of the openid provider.
        @type claimed_id: String
        @param claimed_id: The id being claimed.
        @type identity: String
        @param identity: The identity of the authentication.
        @type return_to: String
        @param return_to: The return to url to be used after authentication.
        @type realm: String
        @param realm: The realm to be used during the authentication.
        @type association_type: String
        @param association_type: The association type.
        @param session_type: String
        @param session_type: The session type.
        """

        self.provider_url = provider_url
        self.claimed_id = claimed_id
        self.identity = identity
        self.return_to = return_to
        self.realm = realm
        self.association_type = association_type
        self.session_type = session_type

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

    def get_claimed_id(self):
        """
        Retrieves the claimed id.

        @rtype: String
        @return: The claimed id.
        """

        return self.claimed_id

    def set_claimed_id(self, claimed_id):
        """
        Sets the claimed id.

        @type claimed_id: String
        @param claimed_id: The claimed id.
        """

        self.claimed_id = claimed_id

    def get_identity(self):
        """
        Retrieves the identity.

        @rtype: String
        @return: The identity.
        """

        return self.identity

    def set_identity(self, identity):
        """
        Retrieves the identity.

        @type identity: String
        @param identity: The identity.
        """

        self.identity = identity

    def get_return_to(self):
        """
        Retrieves the return to.

        @rtype: String
        @return: The return to.
        """

        return self.return_to

    def set_return_to(self, return_to):
        """
        Retrieves the return to.

        @type return_to: String
        @param return_to: The return to.
        """

        self.return_to = return_to

    def get_realm(self):
        """
        Retrieves the realm.

        @rtype: String
        @return: The realm.
        """

        return self.realm

    def set_realm(self, realm):
        """
        Retrieves the realm.

        @type realm: String
        @param realm: The realm.
        """

        self.realm = realm

    def get_association_type(self):
        """
        Retrieves the association type.

        @rtype: String
        @return: The association type.
        """

        return self.association_type

    def set_association_type(self, association_type):
        """
        Retrieves the association type.

        @type association_type: String
        @param association_type: The association type.
        """

        self.association_type = association_type

    def get_session_type(self):
        """
        Retrieves the session type.

        @rtype: String
        @return: The session type.
        """

        return self.session_type

    def set_session_type(self, session_type):
        """
        Retrieves the session type.

        @type session_type: String
        @param session_type: The session type.
        """

        self.session_type = session_type
