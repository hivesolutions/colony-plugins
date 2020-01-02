#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import hmac
import base64
import hashlib
import datetime

import colony

from . import parser
from . import exceptions

DEFAULT_CHARSET = "utf-8"
""" The default charset """

DEFAULT_EXPIRES_IN = "3600"
""" The default expires in """

DEFAULT_SIGNED_NAMES = (
    "op_endpoint",
    "return_to",
    "response_nonce",
    "assoc_handle",
    "claimed_id",
    "identity"
)
""" The default signed names """

DEFAULT_SIGNED_ITEMS = (
    "provider_url",
    "return_to",
    "response_nonce",
    "association_handle",
    "claimed_id",
    "identity"
)
""" The default signed items """

TRUE_VALUE = "true"
""" The true value """

FALSE_VALUE = "false"
""" The false value """

GET_METHOD_VALUE = "GET"
""" The get method value """

POST_METHOD_VALUE = "POST"
""" The post method value """

CONTENT_TYPE_CHARSET_VALUE = "content_type_charset"
""" The content type charset value """

HTTP_URI_VALUE = "http://"
""" The HTTP URI value """

HTTPS_URI_VALUE = "https://"
""" The HTTPS URI value """

XRI_URI_VALUE = "xri://="
""" The XRI URI value """

XRI_INITIALIZER_VALUE = "="
""" The XRI initializer value """

OPENID_NAMESPACE_VALUE = "http://specs.openid.net/auth/2.0"
""" The OpenID namespace value """

OPENID_SREG_1_1_EXTENSION_NAMESPACE_VALUE = "http://openid.net/extensions/sreg/1.1"
""" The OpenID SREG 1.1 extension namespace value """

OPENID_AX_1_0_EXTENSION_NAMESPACE_VALUE = "http://openid.net/srv/ax/1.0"
""" The OpenID ax 1.0 extension namespace value """

ASSOCIATE_MODE_VALUE = "associate"
""" The associate mode value """

CHECKID_SETUP_VALUE = "checkid_setup"
""" The checkid setup value """

CHECKID_IMMEDIATE_VALUE = "checkid_immediate"
""" The checkid immediate value """

ID_RES_VALUE = "id_res"
""" The id res value """

HMAC_SHA1_VALUE = "HMAC-SHA1"
""" The hmac SHA1 value """

HMAC_SHA256_VALUE = "HMAC-SHA256"
""" The HMAC SHA256 value """

DH_SHA1_VALUE = "DH-SHA1"
""" The DH SHA1 value """

DH_SHA256_VALUE = "DH-SHA256"
""" The DH SHA256 value """

NO_ENCRYPTION_VALUE = "no-encryption"
""" The no encryption value """

XRDS_LOCATION_VALUE = "X-XRDS-Location"
""" The XRDS location value """

XRDS_LOCATION_LOWER_VALUE = "x-xrds-location"
""" The XRDS location lower value """

DEFAULT_OPENID_ASSOCIATE_TYPE = HMAC_SHA256_VALUE
""" The default OpenID associate type """

DEFAULT_OPENID_SESSION_TYPE = "no-encryption"
""" The default OpenID session type """

NONCE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZUNIQUE"
""" The nonce time format """

MAXIMUM_NONCE_VALUES_LIST_SIZE = 1000
""" The maximum nonce values list size """

HMAC_HASH_MODULES_MAP = {
    HMAC_SHA1_VALUE : hashlib.sha1,
    HMAC_SHA256_VALUE : hashlib.sha256,
    DH_SHA1_VALUE : hashlib.sha1,
    DH_SHA256_VALUE : hashlib.sha1
}
""" The map associating the hmac values with the hashlib
hash function modules """

DIFFIE_HELLMAN_ASSOCIATION_TYPES = (
    DH_SHA1_VALUE,
    DH_SHA256_VALUE
)
""" The diffie hellman association types """

DEFAULT_PRIME_VALUE = colony.legacy.LONG(155172898181473697471232257763715539915724801966915404479707795314057629378541917580651227423698188993727816152646631438561595825688188889951272158842675419950341258706556549803580104870537681476726513255747040765857479291291572334510643245094715007229621094194349783925984760375594985848253359305585439638443)
""" The default prime value to be used in Diffie Hellman """

DEFAULT_BASE_VALUE = 2
""" The default base value to be used in diffie hellman """

class APIOpenid(colony.System):
    """
    The API OpenID class.
    """

    nonce_values_map = {}
    """ The map associating the provider URL with the nonce values """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.nonce_values_map = {}

    def create_server(self, api_attributes, open_server = True):
        """
        Creates a server, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :type open_server: bool
        :param open_server: If the server should be opened.
        :rtype: OpenidServer
        :return: The created server.
        """

        # retrieves the Diffie Hellman plugin
        diffie_hellman_plugin = self.plugin.diffie_hellman_plugin

        # retrieves the random plugin
        random_plugin = self.plugin.random_plugin

        # retrieves the OpenID structure (if available) and uses it
        # to create the "new" OpenID server
        openid_structure = api_attributes.get("openid_structure", None)
        openid_server = OpenidServer(
            self.plugin,
            diffie_hellman_plugin,
            random_plugin,
            self,
            openid_structure
        )

        # in case the server is meant to be open
        # opens the server
        open_server and openid_server.open()

        # returns the OpenID server
        return openid_server

    def create_client(self, api_attributes, open_client = True):
        """
        Creates a client, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :type open_client: bool
        :param open_client: If the client should be opened.
        :rtype: OpenidClient
        :return: The created client.
        """

        # retrieves the client HTTP plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the API Yadis plugin
        api_yadis_plugin = self.plugin.api_yadis_plugin

        # retrieves the OpenID structure (if available)
        openid_structure = api_attributes.get("openid_structure", None)

        # creates a new client with the given options, opens
        # it in case it's required and returns the generated
        # client to the caller method
        openid_client = OpenidClient(self.plugin, client_http_plugin, api_yadis_plugin, self, openid_structure)
        open_client and openid_client.open()
        return openid_client

    def _verify_nonce(self, nonce_value, provider_url):
        """
        Verifies if the nonce value does not exists in the current
        nonce values database. The validation is made in accordance
        with the OpenID specification.

        :type nonce_value: String
        :param nonce_value: The nonce value to be verified.
        :type provider_url: String
        :param provider_url: The provider URL to be used in
        the verification.
        :rtype: bool
        :return: The result of the verification.
        """

        # in case the provider URL does not exists in the
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
        to it, using the provider URL.

        :type nonce_value: String
        :param nonce_value: The nonce value to be added.
        :type provider_url: String
        :param provider_url: The provider URL to be used in
        the addition.
        """

        # in case the provider URL is not defined
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

    def _btwoc(self, long_value):
        """
        Given some kind of integer (generally a long), this function
        returns the big-endian two's complement as a binary string.

        :type value: int
        :param value: The value to be converted.
        :rtype: String
        :return: The big-endian two's complement as a binary string.
        """

        # encodes the long value into string value
        long_value_encoded = colony.encode_two_complement_string(long_value)

        # converts the long value to a list value
        list_value = list(long_value_encoded)

        # reverses the list
        list_value.reverse()

        # joins the list to retrieve the result
        result = "".join(list_value)

        # returns the result
        return result

    def _mklong(self, btwoc):
        """
        Given a big-endian two's complement string, return the
        long int it represents.

        :type btwoc: String
        :param btwoc: A big-endian two's complement string
        :rtype: int
        :return: The decoded int value.
        """

        # converts the string value to string
        list_value = list(btwoc)

        # reverses the string value
        list_value.reverse()

        # joins the list value to retrieve the string value
        string_value = "".join(list_value)

        # decodes the string value into long
        result = colony.decode_two_complement_string(string_value)

        # returns the result
        return result

class OpenidServer(object):
    """
    The class that represents an OpenID server connection.
    """

    api_openid_plugin = None
    """ The API OpenID plugin """

    diffie_hellman_plugin = None
    """ The Diffie Hellman plugin """

    random_plugin = None
    """ The random plugin """

    api_openid = None
    """ The API OpenID """

    openid_structure = None
    """ The OpenID structure """

    diffie_hellman = None
    """ the Diffie Hellman management structure """

    def __init__(
        self,
        api_openid_plugin = None,
        diffie_hellman_plugin = None,
        random_plugin = None,
        api_openid = None,
        openid_structure = None,
        diffie_hellman = None
    ):
        """
        Constructor of the class.

        :type api_openid_plugin: APIOpenidPlugin
        :param api_openid_plugin: The API OpenID plugin.
        :type diffie_hellman_plugin: DiffieHellmanPlugin
        :param diffie_hellman_plugin: The Diffie Hellman plugin.
        :type random_plugin: RandomPlugin
        :param random_plugin: The random plugin.
        :type api_openid: ServiceOpenid
        :param api_openid: The API OpenID.
        :type openid_structure: OpenidStructure
        :param openid_structure: The OpenID structure.
        :type diffie_hellman: DiffieHellman
        :param diffie_hellman: The Diffie Hellman management structure.
        """

        self.api_openid_plugin = api_openid_plugin
        self.diffie_hellman_plugin = diffie_hellman_plugin
        self.random_plugin = random_plugin
        self.api_openid = api_openid
        self.openid_structure = openid_structure
        self.diffie_hellman = diffie_hellman

    def open(self):
        """
        Opens the OpenID server.
        """

        pass

    def close(self):
        """
        Closes the OpenID server.
        """

        pass

    def generate_openid_structure(
        self,
        provider_url = None,
        association_type = HMAC_SHA256_VALUE,
        session_type = NO_ENCRYPTION_VALUE,
        prime_value = None,
        base_value = None,
        consumer_public = None,
        set_structure = True
    ):
        # creates a new OpenID structure
        openid_structure = OpenidStructure(
            provider_url,
            association_type = association_type,
            session_type = session_type
        )

        # in case the structure is meant to be set
        # sets the OpenID structure
        if set_structure: self.set_openid_structure(openid_structure)

        # decodes the Diffie Hellman values in case they exist
        prime_value = prime_value and self.api_openid._mklong(base64.b64decode(prime_value)) or None
        base_value = base_value and self.api_openid._mklong(base64.b64decode(base_value)) or None
        consumer_public = consumer_public and self.api_openid._mklong(base64.b64decode(consumer_public)) or None

        # sets the default Diffie Hellman values
        prime_value = prime_value or DEFAULT_PRIME_VALUE
        base_value = base_value or DEFAULT_BASE_VALUE

        # creates the parameters to send to be used in the Diffie Hellman
        # structure creation
        parameters = dict(
            prime_value = prime_value,
            base_value = base_value
        )

        # creates the Diffie Hellman management structure with the prime
        # and base values given
        self.diffie_hellman = self.diffie_hellman_plugin.create_structure(parameters)

        # sets the a value in the Diffie Hellman structure
        self.diffie_hellman.set_A_value(consumer_public)

        # returns the OpenID structure
        return openid_structure

    def openid_associate(self):
        """
        Requests an association (associate mode) according to the
        OpenID specification.

        :rtype: OpenidStructure
        :return: The current OpenID structure.
        """

        # generates an association handle
        association_handle = self._generate_handle()

        # retrieves the MAC key type to be used
        mac_key_type = self._get_mac_key_type()

        # generates the MAC key
        mac_key = self._generate_mac_key(mac_key_type)

        # sets the association handle in the OpenID structure
        self.openid_structure.association_handle = association_handle

        # sets the expires in in the OpenID structure
        self.openid_structure.expires_in = DEFAULT_EXPIRES_IN

        # sets the MAC key in the OpenID structure
        self.openid_structure.mac_key = mac_key

        # in case the current session type is of type diffie hellman
        if self.openid_structure.session_type in DIFFIE_HELLMAN_ASSOCIATION_TYPES:
            # generates a private key for the diffie hellman "b" value
            private_key = self._generate_private_key()

            # sets the "b" value in the diffie hellman management structure
            self.diffie_hellman.set_b_value(private_key)

        # returns the OpenID structure
        return self.openid_structure

    def openid_request(self):
        # generates an invalidate handle if necessary
        invalidate_handle = self.openid_structure.invalidate_handle or self._generate_handle()

        # retrieves the current date time
        current_date_time = datetime.datetime.utcnow()

        # converts the current date time to string
        current_date_time_string = current_date_time.strftime(NONCE_TIME_FORMAT)

        # generates a random handle
        random_handle = self._generate_handle()

        # creates the response nonce appending the current date time string
        # to the random handle
        response_nonce = current_date_time_string + random_handle

        # sets the mode in the OpenID structure
        self.openid_structure.mode = ID_RES_VALUE

        # sets the invalidate handle in the OpenID structure
        self.openid_structure.invalidate_handle = invalidate_handle

        # sets the response nonce in the OpenID structure
        self.openid_structure.response_nonce = response_nonce

        # sets the signed in the OpenID structure
        self.openid_structure.signed = ",".join(DEFAULT_SIGNED_NAMES)

        # generates the signature
        signature = self._generate_signature()

        # sets the signature in the OpenID structure
        self.openid_structure.signature = signature

    def openid_check_authentication(self, return_openid_structure, strict = True):
        """
        Verifies the given return OpenID structure (verification)
        according to the OpenID specification.

        :type return_openid_structure: OpenidStructure
        :param return_openid_structure: The return OpenID structure
        to be verified.
        :type strict: bool
        :param strict: Flag to control if the verification should be strict.
        :rtype: OpenidStructure
        :return: The current OpenID structure.
        """

        # in case the verification is strict and any of the base information items mismatches
        if strict and not (self.openid_structure.return_to == return_openid_structure.return_to and\
            self.openid_structure.claimed_id == return_openid_structure.claimed_id and\
            self.openid_structure.identity == return_openid_structure.identity and\
            self.openid_structure.provider_url == return_openid_structure.provider_url and\
            self.openid_structure.response_nonce == return_openid_structure.response_nonce and\
            self.openid_structure.signed == return_openid_structure.signed and\
            self.openid_structure.signature == return_openid_structure.signature and\
            return_openid_structure.ns == OPENID_NAMESPACE_VALUE):

            # raises a verification failed exception
            raise exceptions.VerificationFailed("invalid discovered information")

        # returns the OpenID structure
        return self.openid_structure

    def get_response_parameters(self):
        # start the parameters map
        parameters = {}

        # sets the namespace
        parameters["ns"] = self.openid_structure.ns

        # sets the association handle
        parameters["assoc_handle"] = self.openid_structure.association_handle

        # sets the session type
        parameters["session_type"] = self.openid_structure.session_type

        # sets the association type
        parameters["assoc_type"] = self.openid_structure.association_type

        # sets the expires in
        parameters["expires_in"] = self.openid_structure.expires_in

        # in case the current session type is of type diffie hellman
        if self.openid_structure.session_type in DIFFIE_HELLMAN_ASSOCIATION_TYPES:
            # retrieves the MAC key type to be used
            mac_key_type = self._get_mac_key_type()

            # generates the "B" value
            B_value = self.diffie_hellman.generate_B()

            # calculates the shared key value
            key_value = self.diffie_hellman.calculate_Kb()

            # decodes the MAC key using Base64
            decoded_mac_key = base64.b64decode(self.openid_structure.mac_key)

            # retrieves the hash module from the hmac hash modules map
            hash_module = HMAC_HASH_MODULES_MAP.get(mac_key_type, None)

            # encodes the key value in order to be used in the xor operation
            encoded_key_value = hash_module(self.api_openid._btwoc(key_value)).digest()

            # calculates the encoded MAC key value and retrieves the digest
            encoded_mac_key = colony.xor_string_value(decoded_mac_key, encoded_key_value)

            # encodes the encoded MAC key into Base64
            encoded_mac_key = base64.b64encode(encoded_mac_key)

            # sets the DH server public
            parameters["dh_server_public"] = base64.b64encode(self.api_openid._btwoc(B_value))

            # sets the encoded MAC key
            parameters["enc_mac_key"] = encoded_mac_key
        else:
            # sets the MAC key
            parameters["mac_key"] = self.openid_structure.mac_key

        # returns the parameters
        return parameters

    def get_encoded_response_parameters(self):
        # retrieves the response parameters
        response_parameters = self.get_response_parameters()

        # encodes the response parameters
        encoded_response_parameters = self._encode_key_value(response_parameters)

        # returns the encoded response parameters
        return encoded_response_parameters

    def get_check_authentication_parameters(self):
        # start the parameters map
        parameters = {}

        # sets the namespace
        parameters["ns"] = self.openid_structure.ns

        # sets the is valid
        parameters["is_valid"] = TRUE_VALUE

        # sets the invalidate handle
        parameters["invalidate_handle"] = self.openid_structure.association_handle

        # returns the parameters
        return parameters

    def get_encoded_check_authentication_parameters(self):
        # retrieves the check authentication parameters
        check_authentication_parameters = self.get_check_authentication_parameters()

        # encodes the check authentication parameters
        encoded_check_authentication_parameters = self._encode_key_value(check_authentication_parameters)

        # returns the encoded check authentication parameters
        return encoded_check_authentication_parameters

    def get_return_url(self):
        # sets the retrieval URL
        retrieval_url = self.openid_structure.return_to

        # start the parameters map and sets the complete set of
        # parameters associated with the return URL, these values
        # are taken from the current structure instance
        parameters = {}
        parameters["openid.ns"] = self.openid_structure.ns
        parameters["openid.mode"] = self.openid_structure.mode
        parameters["openid.op_endpoint"] = self.openid_structure.provider_url
        parameters["openid.claimed_id"] = self.openid_structure.claimed_id
        parameters["openid.identity"] = self.openid_structure.identity
        parameters["openid.return_to"] = self.openid_structure.return_to
        parameters["openid.response_nonce"] = self.openid_structure.response_nonce
        parameters["openid.invalidate_handle"] = self.openid_structure.invalidate_handle
        parameters["openid.assoc_handle"] = self.openid_structure.association_handle
        parameters["openid.signed"] = self.openid_structure.signed
        parameters["openid.sig"] = self.openid_structure.signature

        # creates the request (get) URL from the parameters and returns
        # the value to the caller method
        request_url = self._build_get_url(retrieval_url, parameters)
        return request_url

    def get_openid_structure(self):
        """
        Retrieves the OpenID structure.

        :rtype: OpenidStructure
        :return: The OpenID structure.
        """

        return self.openid_structure

    def set_openid_structure(self, openid_structure):
        """
        Sets the OpenID structure.

        :type openid_structure: OpenidStructure
        :param openid_structure: The OpenID structure.
        """

        self.openid_structure = openid_structure

    def _get_mac_key_type(self):
        """
        Retrieves the type of hashing to be used in the
        MAC key.

        :rtype: String
        :return: The type of hashing to be used in the MAC key.
        """

        # in case the current session is of type no encryption
        if self.openid_structure.session_type == NO_ENCRYPTION_VALUE:
            # returns the current association type
            return self.openid_structure.association_type
        # in case the current session is of type DH SHA1
        elif self.openid_structure.session_type == DH_SHA1_VALUE:
            # returns the hmac SHA1 value
            return HMAC_SHA1_VALUE
        # in case the current session is of type DH sha256
        elif self.openid_structure.session_type == DH_SHA256_VALUE:
            # returns the hmac sha256 value
            return HMAC_SHA256_VALUE

    def _generate_signature(self):
        # sets the signature items list
        signed_items_list = DEFAULT_SIGNED_ITEMS

        # sets the signature names list
        signed_names_list = DEFAULT_SIGNED_NAMES

        # creates the string buffer for the message
        message_string_buffer = colony.StringBuffer()

        # starts the index counter
        index = 0

        # iterates over all the signed items
        for signed_item_name in signed_items_list:
            # retrieves the signed item value from the return OpenID structure
            signed_item_value = getattr(self.openid_structure, signed_item_name)

            # retrieves the signed item real name
            signed_item_real_name = signed_names_list[index]

            # adds the key value pair to the message string buffer
            message_string_buffer.write(signed_item_real_name.encode(DEFAULT_CHARSET) + ":" + signed_item_value.encode(DEFAULT_CHARSET) + "\n")

            # increments the index
            index += 1

        # retrieves the value from the message string buffer
        message = message_string_buffer.get_value()

        # decodes the signature MAC key from Base64
        signature_mac_key = base64.b64decode(self.openid_structure.mac_key)

        # retrieves the hash module from the hmac hash modules map
        hash_module = HMAC_HASH_MODULES_MAP.get(self.openid_structure.association_type, None)

        # in case no hash module is set
        if not hash_module:
            # raises the invalid hash function exception
            raise exceptions.InvalidHashFunction("the hash function is not available: " + self.openid_structure.association_type)

        # calculates the signature value and retrieves the digest
        signature = hmac.new(signature_mac_key, message, hash_module).digest()

        # encodes the signature into Base64
        signature = base64.b64encode(signature)

        # returns the signature
        return signature

    def _generate_handle(self):
        # generates a random SHA1
        random_sha1 = self.random_plugin.generate_random_sha1()

        # retrieves the random SHA1 value
        random_sha1_value = random_sha1.digest()

        # encodes the random SHA1 value into Base64
        handle = base64.b64encode(random_sha1_value)

        # returns the handle
        return handle

    def _generate_mac_key(self, mac_key_type = HMAC_SHA1_VALUE):
        # in case the key type is SHA1
        if mac_key_type == HMAC_SHA1_VALUE:
            # generates a MAC key with the SHA1 random value
            mac_key = self.random_plugin.generate_random_sha1()
        # in case the key type is sha256
        elif mac_key_type == HMAC_SHA256_VALUE:
            # generates a MAC key with the sha256 random value
            mac_key = self.random_plugin.generate_random_sha256()

        # retrieves the MAC key value
        mac_key_value = mac_key.digest()

        # encodes the MAC key into Base64
        mac_key_value_encoded = base64.b64encode(mac_key_value)

        # returns the encoded MAC key value
        return mac_key_value_encoded

    def _generate_private_key(self):
        """
        Generates a private key long number, based in the current
        diffie hellman "p" value.
        """

        # retrieves the diffie hellman "p" value
        diffie_hellman_p_value = self.diffie_hellman.get_p_value()

        # generates a "pure" random value
        random_value = self.random_plugin.generate_random_value()

        # normalizes the random value, creating the private key value
        private_key_value = int(random_value * diffie_hellman_p_value - 1)

        # returns the private key value
        return private_key_value

    def _build_get_url(self, base_url, parameters):
        """
        Builds the URL for the given URL and parameters.
        The URL is valid only for a get request.

        :type base_url: String
        :param base_url: The base URL to be used.
        :type parameters: Dictionary
        :param parameters: The parameters to be used for URL construction.
        :rtype: String
        :return: The built URL for the given parameters.
        """

        # encodes the parameters with the URL encode
        parameters_encoded = colony.url_encode(parameters)

        # in case the base URL does not contain any parameters
        if base_url.find("?") == -1:
            # creates the URL value by appending the base URL with
            # the parameters encoded (new parameters)
            url = base_url + "?" + parameters_encoded
        # otherwise
        else:
            # creates the URL value by appending the base URL with
            # the parameters encoded (existing parameters)
            url = base_url + "&" + parameters_encoded

        # returns the built URL
        return url

    def _encode_key_value(self, values_map):
        """
        Encodes the given values map into the key value
        encoding.

        :type values_map: Dictionary
        :param values_map: The map containing the values to be
        encoded.
        :rtype: String
        :return: The key value encoded string.
        """

        return "\n".join([key + ":" + value for key, value in colony.legacy.items(values_map)])

class OpenidClient(object):
    """
    The class that represents an OpenID client connection.
    """

    api_openid_plugin = None
    """ The API OpenID plugin """

    client_http_plugin = None
    """ The client HTTP plugin """

    api_yadis_plugin = None
    """ The API Yadis plugin """

    api_openid = None
    """ The API OpenID """

    openid_structure = None
    """ The OpenID structure """

    http_client = None
    """ The HTTP client for the connection """

    yadis_client = None
    """ The Yadis (remote) client for the connection """

    def __init__(
        self,
        api_openid_plugin = None,
        client_http_plugin = None,
        api_yadis_plugin = None,
        api_openid = None,
        openid_structure = None
    ):
        """
        Constructor of the class.

        :type api_openid_plugin: APIOpenidPlugin
        :param api_openid_plugin: The API OpenID plugin.
        :type client_http_plugin: ClientHTTPPlugin
        :param client_http_plugin: The client HTTP plugin.
        :type api_yadis_plugin: APIYadisPlugin
        :param api_yadis_plugin: The API Yadis plugin.
        :type api_openid: ServiceOpenid
        :param api_openid: The API OpenID.
        :type openid_structure: OpenidStructure
        :param openid_structure: The OpenID structure.
        """

        self.api_openid_plugin = api_openid_plugin
        self.client_http_plugin = client_http_plugin
        self.api_yadis_plugin = api_yadis_plugin
        self.api_openid = api_openid
        self.openid_structure = openid_structure

    def open(self):
        """
        Opens the OpenID client.
        """

        pass

    def close(self):
        """
        Closes the OpenID client.
        """

        # in case an HTTP client is defined, must close
        # it to avoid any leak in HTTP associated resources
        if self.http_client: self.http_client.close({})

        # in case an Yadis (remote) client is defined, must
        # close it to avoid any leak in resources
        if self.yadis_client: self.yadis_client.close()

    def generate_openid_structure(
        self,
        provider_url,
        claimed_id,
        identity,
        return_to,
        realm,
        association_type = DEFAULT_OPENID_ASSOCIATE_TYPE,
        session_type = DEFAULT_OPENID_SESSION_TYPE,
        set_structure = True
    ):
        # creates a new OpenID structure
        openid_structure = OpenidStructure(provider_url, claimed_id, identity, return_to, realm, association_type, session_type)

        # in case the structure is meant to be set
        if set_structure:
            # sets the OpenID structure
            self.set_openid_structure(openid_structure)

        # returns the OpenID structure
        return openid_structure

    def normalize_claimed_id(self, claimed_id):
        """
        Normalizes the claimed id according to the
        OpenID specification.

        :type claimed_id: String
        :param claimed_id: The claimed id to be normalized.
        :rtype: String
        :return: The normalized claimed id.
        """

        # strips the claimed id from trailing spaces
        claimed_id = claimed_id.strip()

        # in case the claimed id is of type xri
        if claimed_id.startswith(XRI_URI_VALUE) or claimed_id.startswith(XRI_INITIALIZER_VALUE):
            # in case the claimed id starts with the xri uri value
            if claimed_id.startswith(XRI_URI_VALUE):
                # removes the xri uri from the claimed id
                claimed_id = claimed_id[6:]
        # in case the claimed id is of type URL
        else:
            # in case the clamed id (URL) does not start with the correct uri value
            if not claimed_id.startswith(HTTP_URI_VALUE) and not claimed_id.startswith(HTTPS_URI_VALUE):
                # adds the HTTP uri to the claimed id
                claimed_id = HTTP_URI_VALUE + claimed_id

            # in case the claimed id (URL) is missing
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
        OpenID specification.

        :rtype: OpenidStructure
        :return: The current OpenID structure.
        """

        # retrieves the Yadis provider URL
        yadis_provider_url = self._get_yadis_provider_url()

        # retrieves the Yadis (remote) client and then used it to
        # generate the proper structure and retrieves the resource
        # descriptor using it as the basis
        yadis_client = self._get_yadis_client()
        yadis_client.generate_yadis_structure(yadis_provider_url)
        resource_descriptor = yadis_client.get_resource_descriptor()

        # retrieves the resources list
        resources_list = resource_descriptor.get_resources_list()

        # retrieves the first service from the resources list
        first_service = resources_list[0].services_list[0]

        # retrieves the provider URL
        provider_url = first_service.get_attribute("URI")

        # retrieves the local id
        local_id = first_service.get_attribute("LocalID")

        # retrieves the types list
        types_list = first_service.types_list

        # sets the provider URL in the OpenID structure
        self.openid_structure.provider_url = provider_url

        # sets the local id in the OpenID structure
        self.openid_structure.local_id = local_id

        # sets the types list in the OpenID structure
        self.openid_structure.types_list = types_list

        # prints a debug message
        self.api_openid_plugin.debug("Found OpenID provider URL '%s'" % provider_url)

        # returns the OpenID structure
        return self.openid_structure

    def openid_associate(self):
        """
        Requests an association (associate mode) according to the
        OpenID specification.

        :rtype: OpenidStructure
        :return: The current OpenID structure.
        """

        # sets the retrieval URL
        retrieval_url = self.openid_structure.provider_url

        # start the parameters map
        parameters = {}

        # sets the namespace as the OpenID default namespace
        parameters["openid.ns"] = OPENID_NAMESPACE_VALUE

        # sets the mode as associate
        parameters["openid.mode"] = ASSOCIATE_MODE_VALUE

        # sets the association type
        parameters["openid.assoc_type"] = self.openid_structure.association_type

        # sets the session type
        parameters["openid.session_type"] = self.openid_structure.session_type

        # fetches the retrieval URL with the given parameters retrieving the result
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
            raise exceptions.ProviderError("problem in provider: " + error)

        # retrieves the expiration from the values map
        self.openid_structure.expires_in = values_map.get("expires_in", None)

        # retrieves the association handle from the values map
        self.openid_structure.association_handle = values_map.get("assoc_handle", None)

        # retrieves the MAC key from the values map
        self.openid_structure.mac_key = values_map.get("mac_key", None)

        # returns the OpenID structure
        return self.openid_structure

    def openid_verify(self, return_openid_structure, strict = True):
        """
        Verifies the given return OpenID structure (verification)
        according to the OpenID specification.

        :type return_openid_structure: OpenidStructure
        :param return_openid_structure: The return OpenID structure
        to be verified.
        :type strict: bool
        :param strict: Flag to control if the verification should be strict.
        :rtype: OpenidStructure
        :return: The current OpenID structure.
        """

        # in case the verification is strict and any of the base information items mismatches
        if strict and not (self.openid_structure.return_to == return_openid_structure.return_to and\
            self.openid_structure.claimed_id == return_openid_structure.claimed_id and\
            self.openid_structure.identity == return_openid_structure.identity and\
            self.openid_structure.provider_url == return_openid_structure.provider_url and\
            return_openid_structure.ns == OPENID_NAMESPACE_VALUE):

            # raises a verification failed exception
            raise exceptions.VerificationFailed("invalid discovered information")

        # verifies the nonce value retrieving the result
        nonce_verification_result = self.api_openid._verify_nonce(return_openid_structure.response_nonce, return_openid_structure.provider_url)

        # in case the nonce verification is not successful
        if not nonce_verification_result:
            # raises a verification failed exception
            raise exceptions.VerificationFailed("invalid return nonce value")

        # retrieves the list of signed items by spliting the list
        signed_items_list = return_openid_structure.signed.split(",")

        # creates the string buffer for the message
        message_string_buffer = colony.StringBuffer()

        # iterates over all the signed items
        for signed_item_name in signed_items_list:
            # retrieves the signed item value from the return OpenID structure
            signed_item_value = getattr(return_openid_structure, signed_item_name)

            # adds the key value pair to the message string buffer
            message_string_buffer.write(signed_item_name.encode(DEFAULT_CHARSET) + ":" + signed_item_value.encode(DEFAULT_CHARSET) + "\n")

        # retrieves the value from the message string buffer
        message = message_string_buffer.get_value()

        # decodes the signature MAC key from Base64
        signature_mac_key = base64.b64decode(self.openid_structure.mac_key)

        # retrieves the hash module from the hmac hash modules map
        hash_module = HMAC_HASH_MODULES_MAP.get(self.openid_structure.association_type, None)

        # in case no hash module is set
        if not hash_module:
            # raises the invalid hash function exception
            raise exceptions.InvalidHashFunction("the hash function is not available: " + self.openid_structure.association_type)

        # calculates the signature value and retrieves the digest
        signature = hmac.new(signature_mac_key, message, hash_module).digest()

        # encodes the signature into Base64
        signature = base64.b64encode(signature)

        # in case there is a signature mismatch
        if not return_openid_structure.signature == signature:
            # raises a verification failed exception
            raise exceptions.VerificationFailed("invalid message signature")

        # updates the nonce value
        self.api_openid._update_nonce(return_openid_structure.response_nonce, return_openid_structure.provider_url)

        # returns the OpenID structure
        return self.openid_structure

    def get_request_url(self):
        """
        Retrieves the request (authentication) URL according to the
        OpenID specification.

        :rtype: String
        :return: The request URL.
        """

        # sets the retrieval URL
        retrieval_url = self.openid_structure.provider_url

        # start the parameters map
        parameters = {}

        # sets the namespace as the OpenID default namespace
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

        # creates the request URL from the parameters
        request_url = self._build_url(retrieval_url, parameters)

        # returns the request URL
        return request_url

    def process_extensions(self, parameters):
        """
        Processes the extensions part of the OpenID
        get request method.

        :type parameters: Dictionary
        :param parameters: The parameters to be processed.
        """

        # in case the sreg 1.1 extension exists in the current OpenID
        # context information
        if OPENID_SREG_1_1_EXTENSION_NAMESPACE_VALUE in self.openid_structure.types_list:
            parameters["openid.ns.sreg"] = OPENID_SREG_1_1_EXTENSION_NAMESPACE_VALUE
            parameters["openid.sreg.required"] = ""
            parameters["openid.sreg.optional"] = "nickname,email,fullname,dob,gender"

        # in case the ax 1.0 extension exists in the current OpenID
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
        for the current OpenID structure.

        :rtype: String
        :return: The preferred claimed id value.
        """

        return self.openid_structure.get_preferred_claimed_id()

    def get_openid_structure(self):
        """
        Retrieves the OpenID structure.

        :rtype: OpenidStructure
        :return: The OpenID structure.
        """

        return self.openid_structure

    def set_openid_structure(self, openid_structure):
        """
        Sets the OpenID structure.

        :type openid_structure: OpenidStructure
        :param openid_structure: The OpenID structure.
        """

        self.openid_structure = openid_structure

    def _get_yadis_provider_url(self):
        """
        Retrieves the "Yadis" provider URL, using the two base strategies
        (the header and the HTML header strategies).

        :rtype: String
        :return: The "Yadis" provider URL.
        """

        # sets the retrieval URL
        retrieval_url = self.openid_structure.claimed_id

        # start the parameters map
        parameters = {}

        # fetches the retrieval URL with the given parameters retrieving the result
        result, headers_map = self._fetch_url(retrieval_url, parameters, headers = True)

        # tries to retrieve the Yadis provider URL
        yadis_provider_url = headers_map.get(XRDS_LOCATION_VALUE, headers_map.get(XRDS_LOCATION_LOWER_VALUE, None))

        # in case a valid Yadis provider
        # URL was discovered
        if yadis_provider_url:
            # returns the Yadis provider URL
            return yadis_provider_url

        # creates a new Yadis HTML parser
        yadis_html_parser = parser.YadisHTMLParser()

        try:
            # feeds the result to the Yadis HTML parser
            yadis_html_parser.feed(result)
        except Exception as exception:
            # prints an info message
            self.api_openid_plugin.info(
                "There was a problem parsing Yadis HTML: %s" %\
                colony.legacy.UNICODE(exception)
            )

        # retrieves the Yadis provider URL
        yadis_provider_url = yadis_html_parser.yadis_provider_url

        # in case a valid Yadis provider
        # URL was discovered
        if yadis_provider_url:
            # returns the Yadis provider URL
            return yadis_provider_url

        # in case no valid Yadis provider URL is set
        if not yadis_provider_url:
            # raises the invalid data exception
            raise exceptions.InvalidData("no valid Yadis provider URL found")

    def _build_url(self, base_url, parameters):
        """
        Builds the URL for the given URL and parameters.

        :type base_url: String
        :param base_url: The base URL to be used.
        :type parameters: Dictionary
        :param parameters: The parameters to be used for URL construction.
        :rtype: String
        :return: The built URL for the given parameters.
        """

        # retrieves the HTTP client
        http_client = self._get_http_client()

        # build the URL from the base URL
        url = http_client.build_url(base_url, GET_METHOD_VALUE, parameters)

        # returns the built URL
        return url

    def _fetch_url(self, url, parameters = None, method = GET_METHOD_VALUE, headers = False):
        """
        Fetches the given URL for the given parameters and using the given method.

        :type url: String
        :param url: The URL to be fetched.
        :type parameters: Dictionary
        :param parameters: The parameters to be used the fetch.
        :type method: String
        :param method: The method to be used in the fetch.
        :type headers: bool
        :param headers: If the headers should be returned.
        :rtype: String
        :return: The fetched data.
        """

        # in case parameters is not defined
        if not parameters:
            # creates a new parameters map
            parameters = {}

        # retrieves the HTTP client
        http_client = self._get_http_client()

        # fetches the URL retrieving the HTTP response
        http_response = http_client.fetch_url(url, method, parameters, content_type_charset = DEFAULT_CHARSET)

        # retrieves the contents from the HTTP response
        contents = http_response.received_message

        # retrieves the headers map from the HTTP response
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
        Retrieves the HTTP client currently in use (in case it's created)
        if not created creates the HTTP client.

        :rtype: HTTPClient
        :return: The retrieved HTTP client.
        """

        # in case no HTTP client exists
        if not self.http_client:
            # defines the client parameters
            client_parameters = {
                CONTENT_TYPE_CHARSET_VALUE : DEFAULT_CHARSET
            }

            # creates the HTTP client
            self.http_client = self.client_http_plugin.create_client(client_parameters)

            # opens the HTTP client
            self.http_client.open({})

        # returns the HTTP client
        return self.http_client

    def _get_yadis_client(self):
        """
        Retrieves the Yadis (remote) client currently in use (in case it's created)
        if not created creates the Yadis (remote) client.

        :rtype: YadisClient
        :return: The retrieved Yadis (remote) client.
        """

        # in case no Yadis client exists, creates the Yadis
        # (remote) client, this is a singleton operation
        if not self.yadis_client:
            self.yadis_client = self.api_yadis_plugin.create_client({})

        # returns the Yadis remote client
        return self.yadis_client

class OpenidStructure(object):
    """
    The OpenID structure class.
    """

    provider_url = None
    """ The URL of the OpenID provider """

    claimed_id = None
    """ The id being claimed """

    identity = None
    """ The identity of the authentication """

    return_to = None
    """ The return to URL to be used after authentication """

    realm = None
    """ The realm to be used during the authentication """

    association_type = None
    """ The association type """

    session_type = None
    """ The session type """

    ns = OPENID_NAMESPACE_VALUE
    """ The namespace """

    mode = None
    """ The mode """

    expires_in = None
    """ The expires in """

    association_handle = None
    """ The association handle """

    invalidate_handle = None
    """ The invalidate handle """

    mac_key = None
    """ The MAC key """

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

    def __init__(
        self,
        provider_url = None,
        claimed_id = None,
        identity = None,
        return_to = None,
        realm = None,
        association_type = DEFAULT_OPENID_ASSOCIATE_TYPE,
        session_type = DEFAULT_OPENID_SESSION_TYPE
    ):
        """
        Constructor of the class.

        :type provider_url: String
        :param provider_url: The URL of the OpenID provider.
        :type claimed_id: String
        :param claimed_id: The id being claimed.
        :type identity: String
        :param identity: The identity of the authentication.
        :type return_to: String
        :param return_to: The return to URL to be used after authentication.
        :type realm: String
        :param realm: The realm to be used during the authentication.
        :type association_type: String
        :param association_type: The association type.
        :param session_type: String
        :param session_type: The session type.
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
        for the current OpenID structure.

        :rtype: String
        :return: The preferred claimed id value.
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
            raise exceptions.InvalidClaimedId("no claimed id available")

    def get_username_claimed_id(self):
        """
        Retrieves the username from the current claimed id
        value, converted accordingly.

        :rtype: String
        :return: The username from the current claimed id
        value, converted accordingly.
        """

        # retrieves the claimed id
        claimed_id = self.get_preferred_claimed_id()

        # strips the claimed id
        claimed_id = claimed_id.rstrip("/")

        # splits the claimed id into base claimed id
        # and username
        _base_claimed_id, username = claimed_id.rsplit("/", 1)

        # returns the username
        return username

    def get_provider_url(self):
        """
        Retrieves the provider URL.

        :rtype: String
        :return: The provider URL.
        """

        return self.provider_url

    def set_provider_url(self, provider_url):
        """
        Sets the provider URL.

        :type provider_url: String
        :param provider_url: The provider URL.
        """

        self.provider_url = provider_url

    def get_claimed_id(self):
        """
        Retrieves the claimed id.

        :rtype: String
        :return: The claimed id.
        """

        return self.claimed_id

    def set_claimed_id(self, claimed_id):
        """
        Sets the claimed id.

        :type claimed_id: String
        :param claimed_id: The claimed id.
        """

        self.claimed_id = claimed_id

    def get_identity(self):
        """
        Retrieves the identity.

        :rtype: String
        :return: The identity.
        """

        return self.identity

    def set_identity(self, identity):
        """
        Sets the identity.

        :type identity: String
        :param identity: The identity.
        """

        self.identity = identity

    def get_return_to(self):
        """
        Retrieves the return to.

        :rtype: String
        :return: The return to.
        """

        return self.return_to

    def set_return_to(self, return_to):
        """
        Sets the return to.

        :type return_to: String
        :param return_to: The return to.
        """

        self.return_to = return_to

    def get_realm(self):
        """
        Retrieves the realm.

        :rtype: String
        :return: The realm.
        """

        return self.realm

    def set_realm(self, realm):
        """
        Sets the realm.

        :type realm: String
        :param realm: The realm.
        """

        self.realm = realm

    def get_association_type(self):
        """
        Retrieves the association type.

        :rtype: String
        :return: The association type.
        """

        return self.association_type

    def set_association_type(self, association_type):
        """
        Sets the association type.

        :type association_type: String
        :param association_type: The association type.
        """

        self.association_type = association_type

    def get_session_type(self):
        """
        Retrieves the session type.

        :rtype: String
        :return: The session type.
        """

        return self.session_type

    def set_session_type(self, session_type):
        """
        Sets the session type.

        :type session_type: String
        :param session_type: The session type.
        """

        self.session_type = session_type

    def get_ns(self):
        """
        Retrieves the namespace.

        :rtype: String
        :return: The namespace.
        """

        return self.ns

    def set_ns(self, ns):
        """
        Sets the namespace.

        :type ns: String
        :param ns: The namespace.
        """

        self.ns = ns

    def get_mode(self):
        """
        Retrieves the mode.

        :rtype: String
        :return: The mode.
        """

        return self.mode

    def set_mode(self, mode):
        """
        Sets the mode.

        :type mode: String
        :param mode: The mode.
        """

        self.mode = mode

    def get_expires_in(self):
        """
        Retrieves the expires in.

        :rtype: String
        :return: The expires in.
        """

        return self.expires_in

    def set_expires_in(self, expires_in):
        """
        Sets the expires in.

        :type expires_in: String
        :param expires_in: The expires in.
        """

        self.expires_in = expires_in

    def get_association_handle(self):
        """
        Retrieves the association handle.

        :rtype: String
        :return: The association handle.
        """

        return self.association_handle

    def set_association_handle(self, association_handle):
        """
        Sets the association handle.

        :type association_handle: String
        :param association_handle: The association handle.
        """

        self.association_handle = association_handle

    def get_invalidate_handle(self):
        """
        Retrieves the invalidate handle.

        :rtype: String
        :return: The invalidate handle.
        """

        return self.invalidate_handle

    def set_invalidate_handle(self, invalidate_handle):
        """
        Sets the invalidate handle.

        :type invalidate_handle: String
        :param invalidate_handle: The invalidate handle.
        """

        self.invalidate_handle = invalidate_handle

    def get_mac_key(self):
        """
        Retrieves the MAC key.

        :rtype: String
        :return: The MAC key.
        """

        return self.mac_key

    def set_mac_key(self, mac_key):
        """
        Sets the MAC key.

        :type mac_key: String
        :param mac_key: The MAC key.
        """

        self.mac_key = mac_key

    def get_signed(self):
        """
        Retrieves the signed

        :rtype: String
        :return: The signed.
        """

        return self.signed

    def set_signed(self, signed):
        """
        Sets the signed.

        :type signed: String
        :param signed: The signed.
        """

        self.signed = signed

    def get_signature(self):
        """
        Retrieves the signature

        :rtype: String
        :return: The signature.
        """

        return self.signature

    def set_signature(self, signature):
        """
        Sets the signature.

        :type signed: String
        :param signed: The signature.
        """

        self.signature = signature

    def get_response_nonce(self):
        """
        Retrieves the response nonce

        :rtype: String
        :return: The response nonce.
        """

        return self.response_nonce

    def set_response_nonce(self, response_nonce):
        """
        Sets the response nonce.

        :type signed: String
        :param signed: The response nonce.
        """

        self.response_nonce = response_nonce

    def get_local_id(self):
        """
        Retrieves the local id.

        :rtype: String
        :return: The local id.
        """

        return self.local_id

    def set_local_id(self, local_id):
        """
        Sets the local id.

        :type local_id: String
        :param local_id: The local id.
        """

        self.local_id = local_id

    def get_types_list(self):
        """
        Retrieves the types list.

        :rtype: List
        :return: The types list.
        """

        return self.types_list

    def set_types_list(self, types_list):
        """
        Sets the types list.

        :type types_list: List
        :param types_list: The types list.
        """

        self.types_list = types_list
