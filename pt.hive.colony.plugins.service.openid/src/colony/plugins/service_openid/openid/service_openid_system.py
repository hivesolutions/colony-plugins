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

import hmac
import base64
import hashlib

import colony.libs.string_buffer_util

import service_openid_parser
import service_openid_exceptions

DEFAULT_CHARSET = "utf-8"
""" The default charset """

DEFAULT_EXPIRES_IN = "1000"
""" The default expires in """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

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

OPENID_SREG_1_1_EXTENSION_NAMESPACE_VALUE = "http://openid.net/extensions/sreg/1.1"
""" The openid sreg 1.1 extension namespace value """

OPENID_AX_1_0_EXTENSION_NAMESPACE_VALUE = "http://openid.net/srv/ax/1.0"
""" The openid ax 1.0 extension namespace value """

ASSOCIATE_MODE_VALUE = "associate"
""" The associate mode value """

CHECKID_SETUP_VALUE = "checkid_setup"
""" The checkid setup value """

CHECKID_IMMEDIATE_VALUE = "checkid_immediate"
""" The checkid immediate value """

HMAC_SHA1_VALUE = "HMAC-SHA1"
""" The hmac sha1 value """

HMAC_SHA256_VALUE = "HMAC-SHA256"
""" The hmac sha256 value """

XRDS_LOCATION_VALUE = "X-XRDS-Location"
""" The xrds location value """

XRDS_LOCATION_LOWER_VALUE = "x-xrds-location"
""" The xrds location lower value """

DEFAULT_OPENID_ASSOCIATE_TYPE = HMAC_SHA256_VALUE
""" The default openid associate type """

DEFAULT_OPENID_SESSION_TYPE = "no-encryption"
""" The default openid session type """

MAXIMUM_NONCE_VALUES_LIST_SIZE = 1000
""" The maximum nonce values list size """

HMAC_HASH_MODULES_MAP = {HMAC_SHA1_VALUE : hashlib.sha1,
                         HMAC_SHA256_VALUE : hashlib.sha256}
""" The map associating the hmac values with the hashlib hash function modules """

class ServiceOpenid:
    """
    The service openid class.
    """

    service_openid_plugin = None
    """ The service openid plugin """

    nonce_values_map = {}
    """ The map associating the provider url with the nonce values """

    def __init__(self, service_openid_plugin):
        """
        Constructor of the class.

        @type service_openid_plugin: ServiceOpenidPlugin
        @param service_openid_plugin: The service openid plugin.
        """

        self.service_openid_plugin = service_openid_plugin

        self.nonce_values_map = {}

    def create_remote_server(self, service_attributes, open_server = True):
        """
        Creates a remote server, with the given service attributes.

        @type service_attributes: Dictionary
        @param service_attributes: The service attributes to be used.
        @type open_server: bool
        @param open_server: If the server should be opened.
        @rtype: OpenidServer
        @return: The created remote server.
        """

        # retrieves the random plugin
        random_plugin = self.service_openid_plugin.random_plugin

        # retrieves the openid structure (if available)
        openid_structure = service_attributes.get("openid_structure", None)

        # creates the openid server
        openid_server = OpenidServer(self.service_openid_plugin, random_plugin, self, openid_structure)

        # in case the server is meant to be open
        # opens the server
        open_server and openid_server.open()

        # returns the openid server
        return openid_server

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
        main_client_http_plugin = self.service_openid_plugin.main_client_http_plugin

        # retrieves the service yadis plugin
        service_yadis_plugin = self.service_openid_plugin.service_yadis_plugin

        # retrieves the openid structure (if available)
        openid_structure = service_attributes.get("openid_structure", None)

        # creates the openid client
        openid_client = OpenidClient(self.service_openid_plugin, main_client_http_plugin, service_yadis_plugin, self, openid_structure)

        # in case the client is meant to be open
        # opens the client
        open_client and openid_client.open()

        # returns the openid client
        return openid_client

    def _verify_nonce(self, nonce_value, provider_url):
        """
        Verifies if the nonce value does not exists in the current
        nonce values database. The validation is made in accordance
        with the openid specification.

        @type nonce_value: String
        @param nonce_value: The nonce value to be verified.
        @type provider_url: String
        @param provider_url: The provider url to be used in
        the verification.
        @rtype: bool
        @return: The result of the verification.
        """

        # in case the provider url does not exists in the
        # global nonce values map
        if not provider_url in self.nonce_values_map:
            return True

        # retrieves the nonce values map
        nonce_values_map = self.nonce_values_map[provider_url][2]

        # in case the nonce value exists in the
        # nonce values map (collision)
        if nonce_value in nonce_values_map:
            # returns false
            return False

        # returns true
        return True

    def _update_nonce(self, nonce_value, provider_url):
        """
        Updates the nonce database by adding the nonce value
        to it, using the provider url.

        @type nonce_value: String
        @param nonce_value: The nonce value to be added.
        @type provider_url: String
        @param provider_url: The provider url to be used in
        the addition.
        """

        # in case the provider url is not defined
        # in the nonce values map
        if not provider_url in self.nonce_values_map:
            # sets the nonce values map
            self.nonce_values_map[provider_url] = {}

            # sets the nonce values list and map
            self.nonce_values_map[provider_url][1] = []
            self.nonce_values_map[provider_url][2] = {}

        # retrieves the nonce values list and map
        nonce_values_list = self.nonce_values_map[provider_url][1]
        nonce_values_map = self.nonce_values_map[provider_url][2]

        # retrieves the nonce values list length
        nonce_values_list_length = len(nonce_values_list)

        # in case the list is full (it's a circular list)
        # the list needs to be kept at the same size (last item is removed)
        if nonce_values_list_length == MAXIMUM_NONCE_VALUES_LIST_SIZE:
            # retrieves the last element from the
            # nonce values list (the oldest)
            last_element = nonce_values_list[-1]

            # removes the last element from the nonce values map
            del nonce_values_map[last_element]

            # pops the last element from the nonce values list
            nonce_values_list.pop()

        # inserts the item at the beginning of the list
        # and sets the item in the map
        nonce_values_list.insert(0, nonce_value)
        nonce_values_map[nonce_value] = True

class OpenidServer:
    """
    The class that represents an openid server connection.
    """

    service_openid_plugin = None
    """ The service openid plugin """

    random_plugin = None
    """ The random plugin """

    service_openid = None
    """ The service openid """

    openid_structure = None
    """ The openid structure """

    def __init__(self, service_openid_plugin = None, random_plugin = None, service_openid = None, openid_structure = None):
        """
        Constructor of the class.

        @type service_openid_plugin: ServiceOpenidPlugin
        @param service_openid_plugin: The service openid plugin.
        @type random_plugin: RandomPlugin
        @param random_plugin: The random plugin.
        @type service_openid: ServiceOpenid
        @param service_openid: The service openid.
        @type openid_structure: OpenidStructure
        @param openid_structure: The openid structure.
        """

        self.service_openid_plugin = service_openid_plugin
        self.random_plugin = random_plugin
        self.service_openid = service_openid
        self.openid_structure = openid_structure

    def open(self):
        """
        Opens the openid server.
        """

        pass

    def close(self):
        """
        Closes the openid server.
        """

        pass

    def generate_openid_structure(self, association_type, session_type, set_structure = True):
        # creates a new openid structure
        openid_structure = OpenidStructure(association_type = association_type, session_type = session_type)

        # in case the structure is meant to be set
        if set_structure:
            # sets the openid structure
            self.set_openid_structure(openid_structure)

        # returns the openid structure
        return openid_structure

    def openid_associate(self):
        """
        Requests an association (associate mode) according to the
        openid specification.

        @rtype: OpenidStructure
        @return: The current openid structure.
        """

        # generates an association handle
        association_handle = self._generate_association_handle()

        # retrieves the association type as the key type
        key_type = self.openid_structure.get_association_type()

        # generates the mac key
        mac_key = self._generate_mac_key(key_type)

        # sets the association handle in the openid structure
        self.openid_structure.association_handle = association_handle

        # sets the expires in in the openid structure
        self.openid_structure.expires_in = DEFAULT_EXPIRES_IN

        # sets the mac key in the openid structure
        self.openid_structure.mac_key = mac_key

        # returns the openid structure
        return self.openid_structure

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

    def _generate_association_handle(self, key_type = HMAC_SHA1_VALUE):
        # generates a random sha1
        random_sha1 = self.random_plugin.generate_random_sha1()

        # retrieves the random sha1 value
        random_sha1_value = random_sha1.digest()

        # encodes the random sha1 value into base64
        association_handle = base64.b64encode(random_sha1_value)

        # returns the association handle
        return association_handle

    def _generate_mac_key(self, key_type = HMAC_SHA1_VALUE):
        # in case the key type is sha1
        if key_type == HMAC_SHA1_VALUE:
            # generates a mac key with the sha1 random value
            mac_key = self.random_plugin.generate_random_sha1()
        # in case the key type is sha256
        elif key_type == HMAC_SHA256_VALUE:
            # generates a mac key with the sha256 random value
            mac_key = self.random_plugin.generate_random_sha256()

        # retrieves the mac key value
        mac_key_value = mac_key.digest()

        # encodes the mac key into base64
        mac_key_value_encoded = base64.b64encode(mac_key_value)

        # returns the encoded mac key value
        return mac_key_value_encoded

class OpenidClient:
    """
    The class that represents an openid client connection.
    """

    service_openid_plugin = None
    """ The service openid plugin """

    main_client_http_plugin = None
    """ The main client http plugin """

    service_yadis_plugin = None
    """ The service yadis plugin """

    service_openid = None
    """ The service openid """

    openid_structure = None
    """ The openid structure """

    http_client = None
    """ The http client for the connection """

    yadis_remote_client = None
    """ The yadis remote client for the connection """

    def __init__(self, service_openid_plugin = None, main_client_http_plugin = None, service_yadis_plugin = None, service_openid = None, openid_structure = None):
        """
        Constructor of the class.

        @type service_openid_plugin: ServiceOpenidPlugin
        @param service_openid_plugin: The service openid plugin.
        @type main_client_http_plugin: MainClientHttpPlugin
        @param main_client_http_plugin: The main client http plugin.
        @type service_yadis_plugin: ServiceYadisPlugin
        @param service_yadis_plugin: The service yadis plugin.
        @type service_openid: ServiceOpenid
        @param service_openid: The service openid.
        @type openid_structure: OpenidStructure
        @param openid_structure: The openid structure.
        """

        self.service_openid_plugin = service_openid_plugin
        self.main_client_http_plugin = main_client_http_plugin
        self.service_yadis_plugin = service_yadis_plugin
        self.service_openid = service_openid
        self.openid_structure = openid_structure

    def open(self):
        """
        Opens the openid client.
        """

        pass

    def close(self):
        """
        Closes the openid client.
        """

        # in case an http client is defined
        if self.http_client:
            # closes the http client
            self.http_client.close({})

        # in case an yadis remote client is defined
        if self.yadis_remote_client:
            # closes the yadis remote client
            self.yadis_remote_client.close()

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
        @return: The normalized claimed id.
        """

        # strips the claimed id from trailing spaces
        claimed_id = claimed_id.strip()

        # in case the claimed id is of type xri
        if claimed_id.startswith(XRI_URI_VALUE) or claimed_id.startswith(XRI_INITIALIZER_VALUE):
            # in case the claimed id starts with the xri uri value
            if claimed_id.startswith(XRI_URI_VALUE):
                # removes the xri uri from the claimed id
                claimed_id = claimed_id[6:]
        # in case the claimed id is of type url
        else:
            # in case the clamed id (url) does not start with the correct uri value
            if not claimed_id.startswith(HTTP_URI_VALUE) and not claimed_id.startswith(HTTPS_URI_VALUE):
                # adds the http uri to the claimed id
                claimed_id = HTTP_URI_VALUE + claimed_id

            # in case the claimed id (url) is missing
            # the trailing slash
            if not claimed_id[-1] == "/":
                # in case the claimed id is an empty
                # path (eg: http://example.com)
                if claimed_id.count("/") < 3:
                    # adds the trailing slash
                    claimed_id += "/"

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

        # retrieves the yadis remote client
        yadis_remote_client = self._get_yadis_remote_client()

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

        # retrieves the local id
        local_id = first_service.get_attribute("LocalID")

        # retrieves the types list
        types_list = first_service.types_list

        # sets the provider url in the openid structure
        self.openid_structure.provider_url = provider_url

        # sets the local id in the openid structure
        self.openid_structure.local_id = local_id

        # sets the types list in the openid structure
        self.openid_structure.types_list = types_list

        # prints a debug message
        self.service_openid_plugin.debug("Found openid provider url '%s'" % provider_url)

        # returns the openid structure
        return self.openid_structure

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

        # retrieves the error from the values map
        error = values_map.get("error", None)

        # in case the error value is set
        if error:
            # raises a provider error exception
            raise service_openid_exceptions.ProviderError("problem in provider: " + error)

        # retrieves the expiration from the values map
        self.openid_structure.expires_in = values_map.get("expires_in", None)

        # retrieves the association handle from the values map
        self.openid_structure.association_handle = values_map.get("assoc_handle", None)

        # retrieves the mac key from the values map
        self.openid_structure.mac_key = values_map.get("mac_key", None)

        # returns the openid structure
        return self.openid_structure

    def openid_verify(self, return_openid_structure, strict = True):
        """
        Verifies the given return openid structure (verification)
        according to the openid specification.

        @type return_openid_structure: OpenidStructure
        @param return_openid_structure: The return openid structure
        to be verified.
        @type strict: bool
        @param strict: Flag to control if the verification should be strict.
        @rtype: OpenidStructure
        @return: The current openid structure.
        """

        # in case the verification is strict and any of the base information items mismatches
        if strict and not (self.openid_structure.return_to == return_openid_structure.return_to and\
                           self.openid_structure.claimed_id == return_openid_structure.claimed_id and\
                           self.openid_structure.identity == return_openid_structure.identity and\
                           self.openid_structure.provider_url == return_openid_structure.provider_url and\
                           return_openid_structure.ns == OPENID_NAMESPACE_VALUE):
            # raises a verification failed exception
            raise service_openid_exceptions.VerificationFailed("invalid discovered information")

        # verifies the nonce value retrieving the result
        nonce_verification_result = self.service_openid._verify_nonce(return_openid_structure.response_nonce, return_openid_structure.provider_url)

        # in case the nonce verification is not successful
        if not nonce_verification_result:
            # raises a verification failed exception
            raise service_openid_exceptions.VerificationFailed("invalid return nonce value")

        # retrieves the list of signed items by spliting the list
        signed_items_list = return_openid_structure.signed.split(",")

        # creates the string buffer for the message
        message_string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # iterates over all the signed items
        for signed_item_name in signed_items_list:
            # retrieves the signed item value from the return openid structure
            signed_item_value = getattr(return_openid_structure, signed_item_name)

            # adds the key value pair to the message string buffer
            message_string_buffer.write(signed_item_name.encode("utf-8") + ":" + signed_item_value.encode("utf-8") + "\n")

        # retrieves the value from the message string buffer
        message = message_string_buffer.get_value()

        # decodes the signature mac key from base64
        signature_mac_key = base64.b64decode(self.openid_structure.mac_key)

        # retrieves the hash module from the hmac hash modules map
        hash_module = HMAC_HASH_MODULES_MAP.get(self.openid_structure.association_type, None)

        # in case no hash module is set
        if not hash_module:
            # raises the invalid hash function exception
            raise service_openid_exceptions.InvalidHashFunction("the hash functionn is not available: " + self.openid_structure.association_type)

        # calculates the signature value and retrieves the digest
        signature = hmac.new(signature_mac_key, message, hash_module).digest()

        # encodes the signature into base64
        signature = base64.b64encode(signature)

        # in case there is a signature mismatch
        if not return_openid_structure.signature == signature:
            # raises a verification failed exception
            raise service_openid_exceptions.VerificationFailed("invalid message signature")

        # updates the nonce value
        self.service_openid._update_nonce(return_openid_structure.response_nonce, return_openid_structure.provider_url)

    def get_request_url(self):
        """
        Retrieves the request (authentication) url according to the
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

        # processes the extensions
        self.process_extensions(parameters)

        # creates the request url from the parameters
        request_url = self._build_url(retrieval_url, parameters)

        # returns the request url
        return request_url

    def process_extensions(self, parameters):
        """
        Processes the extensions part of the openid
        get request method.

        @type parameters: Dictionary
        @param parameters: The parameters to be processed.
        """

        # in case the sreg 1.1 extension exists in the current openid
        # context information
        if OPENID_SREG_1_1_EXTENSION_NAMESPACE_VALUE in self.openid_structure.types_list:
            parameters["openid.ns.sreg"] = OPENID_SREG_1_1_EXTENSION_NAMESPACE_VALUE
            parameters["openid.sreg.required"] = ""
            parameters["openid.sreg.optional"] = "nickname,email,fullname,dob,gender"

        # in case the ax 1.0 extension exists in the current openid
        # context information
        if OPENID_AX_1_0_EXTENSION_NAMESPACE_VALUE in self.openid_structure.types_list:
            parameters["openid.ns.ax"] = OPENID_AX_1_0_EXTENSION_NAMESPACE_VALUE
            parameters["openid.ax.mode"] = "fetch_request"
            parameters["openid.ax.type.nickname"] = "http://axschema.org/namePerson/friendly"
            parameters["openid.ax.type.email"] = "http://axschema.org/contact/email"
            parameters["openid.ax.type.fullname"] = "http://axschema.org/namePerson"
            parameters["openid.ax.type.dob"] = "http://axschema.org/birthDate"
            parameters["openid.ax.type.gender"] = "http://axschema.org/person/gender"
            parameters["openid.ax.required"] = "nickname,email,fullname,dob,gender"
            parameters["openid.ax.optional"] = ""

    def get_preferred_claimed_id(self):
        """
        Retrieves the preferred claimed id
        for the current openid structure.

        @rtype: String
        @return: The preferred claimed id value.
        """

        return self.openid_structure.get_preferred_claimed_id()

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
        yadis_provider_url = headers_map.get(XRDS_LOCATION_VALUE, headers_map.get(XRDS_LOCATION_LOWER_VALUE, None))

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
            self.service_openid_plugin.info("There was a problem parsing yadis html: %s" % unicode(exception))

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

    def _build_url(self, base_url, parameters):
        """
        Builds the url for the given url and parameters.

        @type base_url: String
        @param base_url: The base url to be used.
        @type parameters: Dictionary
        @param parameters: The parameters to be used for url construction.
        @rtype: String
        @return: The built url for the given parameters.
        """

        # retrieves the http client
        http_client = self._get_http_client()

        # build the url from the base urtl
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)

        # returns the built url
        return url

    def _fetch_url(self, url, parameters = None, method = GET_METHOD_VALUE, headers = False):
        """
        Fetches the given url for the given parameters and using the given method.

        @type url: String
        @param url: The url to be fetched.
        @type parameters: Dictionary
        @param parameters: The parameters to be used the fetch.
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

        # retrieves the http client
        http_client = self._get_http_client()

        # fetches the url retrieving the http response
        http_response = http_client.fetch_url(url, method, parameters, content_type_charset = DEFAULT_CHARSET)

        # retrieves the contents from the http response
        contents = http_response.received_message

        # retrieves the headers map from the http response
        headers_map = http_response.headers_map

        # in case the headers flag is set
        if headers:
            # returns the contents and the headers map
            return contents, headers_map
        else:
            # returns the contents
            return contents

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
            self.http_client.open({})

        # returns the http client
        return self.http_client

    def _get_yadis_remote_client(self):
        """
        Retrieves the yadis remote client currently in use (in case it's created)
        if not created creates the yadis remote client.

        @rtype: YadisClient
        @return: The retrieved yadis remote client.
        """

        # in case no yadis remote client exists
        if not self.yadis_remote_client:
            # creates the yadis remote client
            self.yadis_remote_client = self.service_yadis_plugin.create_remote_client({})

        # returns the yadis remote client
        return self.yadis_remote_client

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

    ns = OPENID_NAMESPACE_VALUE
    """ The namespace """

    expires_in = None
    """ The expires in """

    association_handle = None
    """ The association handle """

    mac_key = None
    """ The mac key """

    signed = None
    """ The current type of signature being used """

    signature = None
    """ The signature value of the current message """

    response_nonce = None
    """ The response nonce of the message """

    local_id = None
    """ The local id """

    types_list = []
    """ the list of extension types accepted by the provider """

    def __init__(self, provider_url = None, claimed_id = None, identity = None, return_to = None, realm = None, association_type = DEFAULT_OPENID_ASSOCIATE_TYPE, session_type = DEFAULT_OPENID_SESSION_TYPE):
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

        self.types_list = []

    def get_preferred_claimed_id(self):
        """
        Retrieves the preferred claimed id
        for the current openid structure.

        @rtype: String
        @return: The preferred claimed id value.
        """

        # in case there is a local id defined
        if self.local_id:
            # returns the local id
            return self.local_id
        # in case there is a claimed id defined
        elif self.claimed_id:
            # returns the claimed id
            return self.claimed_id
        # in case none is defined
        else:
            # raises the invalid claimed id exception
            raise service_openid_exceptions.InvalidClaimedId("no claimed id available")

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

    def get_ns(self):
        """
        Retrieves the namespace.

        @rtype: String
        @return: The namespace.
        """

        return self.ns

    def set_ns(self, ns):
        """
        Retrieves the namespace.

        @type ns: String
        @param ns: The namespace.
        """

        self.ns = ns

    def get_expires_in(self):
        """
        Retrieves the expires in.

        @rtype: String
        @return: The expires in.
        """

        return self.expires_in

    def set_expires_in(self, expires_in):
        """
        Retrieves the expires in.

        @type expires_in: String
        @param expires_in: The expires in.
        """

        self.expires_in = expires_in

    def get_association_handle(self):
        """
        Retrieves the association handle.

        @rtype: String
        @return: The association handle.
        """

        return self.association_handle

    def set_association_handle(self, association_handle):
        """
        Retrieves the association handle.

        @type association_handle: String
        @param association_handle: The association handle.
        """

        self.association_handle = association_handle

    def get_mac_key(self):
        """
        Retrieves the mac key.

        @rtype: String
        @return: The mac key.
        """

        return self.mac_key

    def set_mac_key(self, mac_key):
        """
        Retrieves the mac key.

        @type mac_key: String
        @param mac_key: The mac key.
        """

        self.mac_key = mac_key

    def get_signed(self):
        """
        Retrieves the signed

        @rtype: String
        @return: The signed.
        """

        return self.signed

    def set_signed(self, signed):
        """
        Retrieves the signed.

        @type signed: String
        @param signed: The signed.
        """

        self.signed = signed

    def get_signature(self):
        """
        Retrieves the signature

        @rtype: String
        @return: The signature.
        """

        return self.signature

    def set_signature(self, signature):
        """
        Retrieves the signature.

        @type signed: String
        @param signed: The signature.
        """

        self.signature = signature

    def get_response_nonce(self):
        """
        Retrieves the response nonce

        @rtype: String
        @return: The response nonce.
        """

        return self.response_nonce

    def set_response_nonce(self, response_nonce):
        """
        Retrieves the response nonce.

        @type signed: String
        @param signed: The response nonce.
        """

        self.response_nonce = response_nonce

    def get_local_id(self):
        """
        Retrieves the local id.

        @rtype: String
        @return: The local id.
        """

        return self.local_id

    def set_local_id(self, local_id):
        """
        Retrieves the local id.

        @type local_id: String
        @param local_id: The local id.
        """

        self.local_id = local_id

    def get_types_list(self):
        """
        Retrieves the types list.

        @rtype: List
        @return: The types list.
        """

        return self.types_list

    def set_types_list(self, types_list):
        """
        Retrieves the types list.

        @type types_list: List
        @param types_list: The types list.
        """

        self.types_list = types_list
