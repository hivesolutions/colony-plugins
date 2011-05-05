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
import datetime

import colony.libs.encode_util
import colony.libs.string_util
import colony.libs.string_buffer_util

import service_openid_parser
import service_openid_exceptions

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

ID_RES_VALUE = "id_res"
""" The id res value """

HMAC_SHA1_VALUE = "HMAC-SHA1"
""" The hmac sha1 value """

HMAC_SHA256_VALUE = "HMAC-SHA256"
""" The hmac sha256 value """

DH_SHA1_VALUE = "DH-SHA1"
""" The dh sha1 value """

DH_SHA256_VALUE = "DH-SHA256"
""" The dh sha256 value """

NO_ENCRYPTION_VALUE = "no-encryption"
""" The no encryption value """

XRDS_LOCATION_VALUE = "X-XRDS-Location"
""" The xrds location value """

XRDS_LOCATION_LOWER_VALUE = "x-xrds-location"
""" The xrds location lower value """

DEFAULT_OPENID_ASSOCIATE_TYPE = HMAC_SHA256_VALUE
""" The default openid associate type """

DEFAULT_OPENID_SESSION_TYPE = "no-encryption"
""" The default openid session type """

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
""" The map associating the hmac values with the hashlib hash function modules """

DIFFIE_HELLMAN_ASSOCIATION_TYPES = (
    DH_SHA1_VALUE,
    DH_SHA256_VALUE
)
""" The diffie hellman association types """

DEFAULT_PRIME_VALUE = 155172898181473697471232257763715539915724801966915404479707795314057629378541917580651227423698188993727816152646631438561595825688188889951272158842675419950341258706556549803580104870537681476726513255747040765857479291291572334510643245094715007229621094194349783925984760375594985848253359305585439638443L
""" The default prime value to be used in diffie hellman """

DEFAULT_BASE_VALUE = 2
""" The default base value to be used in diffie hellman """

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

        # retrieves the encryption diffie hellman plugin
        encryption_diffie_hellman_plugin = self.service_openid_plugin.encryption_diffie_hellman_plugin

        # retrieves the random plugin
        random_plugin = self.service_openid_plugin.random_plugin

        # retrieves the openid structure (if available)
        openid_structure = service_attributes.get("openid_structure", None)

        # creates the openid server
        openid_server = OpenidServer(self.service_openid_plugin, encryption_diffie_hellman_plugin, random_plugin, self, openid_structure)

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

    def _btwoc(self, long_value):
        """
        Given some kind of integer (generally a long), this function
        returns the big-endian two's complement as a binary string.

        @type value: int
        @param value: The value to be converted.
        @rtype: String
        @return: The big-endian two's complement as a binary string.
        """

        # encodes the long value into string value
        long_value_encoded = colony.libs.encode_util.encode_two_complement_string(long_value)

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

        @type btwoc: String
        @param btwoc: A big-endian two's complement string
        @rtype: int
        @return: The decoded int value.
        """

        # converts the string value to string
        list_value = list(btwoc)

        # reverses the string value
        list_value.reverse()

        # joins the list value to retrieve the string value
        string_value = "".join(list_value)

        # decodes the string value into long
        result = colony.libs.encode_util.decode_two_complement_string(string_value)

        # returns the result
        return result

class OpenidServer:
    """
    The class that represents an openid server connection.
    """

    service_openid_plugin = None
    """ The service openid plugin """

    encryption_diffie_hellman_plugin = None
    """ The encryption diffie hellman plugin """

    random_plugin = None
    """ The random plugin """

    service_openid = None
    """ The service openid """

    openid_structure = None
    """ The openid structure """

    diffie_hellman = None
    """ the diffie hellman management structure """

    def __init__(self, service_openid_plugin = None, encryption_diffie_hellman_plugin = None, random_plugin = None, service_openid = None, openid_structure = None, diffie_hellman = None):
        """
        Constructor of the class.

        @type service_openid_plugin: ServiceOpenidPlugin
        @param service_openid_plugin: The service openid plugin.
        @type encryption_diffie_hellman_plugin: EncryptionDiffieHellmanPlugin
        @param encryption_diffie_hellman_plugin: The encryption diffie hellman plugin.
        @type random_plugin: RandomPlugin
        @param random_plugin: The random plugin.
        @type service_openid: ServiceOpenid
        @param service_openid: The service openid.
        @type openid_structure: OpenidStructure
        @param openid_structure: The openid structure.
        @type diffie_hellman: DiffieHellman
        @param diffie_hellman: The diffie hellman management structure.
        """

        self.service_openid_plugin = service_openid_plugin
        self.encryption_diffie_hellman_plugin = encryption_diffie_hellman_plugin
        self.random_plugin = random_plugin
        self.service_openid = service_openid
        self.openid_structure = openid_structure
        self.diffie_hellman = diffie_hellman

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

    def generate_openid_structure(self, provider_url = None, association_type = HMAC_SHA256_VALUE, session_type = NO_ENCRYPTION_VALUE, prime_value = None, base_value = None, consumer_public = None, set_structure = True):
        # creates a new openid structure
        openid_structure = OpenidStructure(provider_url, association_type = association_type, session_type = session_type)

        # in case the structure is meant to be set
        if set_structure:
            # sets the openid structure
            self.set_openid_structure(openid_structure)

        # decodes the diffie hellman values in case they exist
        prime_value = prime_value and self.service_openid._mklong(base64.b64decode(prime_value)) or  None
        base_value = base_value and self.service_openid._mklong(base64.b64decode(base_value)) or None
        consumer_public = consumer_public and self.service_openid._mklong(base64.b64decode(consumer_public)) or None

        # sets the default diffie hellman values
        prime_value = prime_value or DEFAULT_PRIME_VALUE
        base_value = base_value or DEFAULT_BASE_VALUE

        # creates the parameters to send to be used in the diffie hellman
        # structure creation
        parameters = {
            "prime_value" : prime_value,
            "base_value" : base_value
        }

        # creates the diffie hellman management structure with the prime
        # and base values given
        self.diffie_hellman = self.encryption_diffie_hellman_plugin.create_structure(parameters)

        # sets the a value in the diffie hellman structure
        self.diffie_hellman.set_A_value(consumer_public)

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
        association_handle = self._generate_handle()

        # retrieves the mac key type to be used
        mac_key_type = self._get_mac_key_type()

        # generates the mac key
        mac_key = self._generate_mac_key(mac_key_type)

        # sets the association handle in the openid structure
        self.openid_structure.association_handle = association_handle

        # sets the expires in in the openid structure
        self.openid_structure.expires_in = DEFAULT_EXPIRES_IN

        # sets the mac key in the openid structure
        self.openid_structure.mac_key = mac_key

        # in case the current session type is of type diffie hellman
        if self.openid_structure.session_type in DIFFIE_HELLMAN_ASSOCIATION_TYPES:
            # generates a private key for the diffie hellman "b" value
            private_key = self._generate_private_key()

            # sets the "b" value in the diffie hellman management structure
            self.diffie_hellman.set_b_value(private_key)

        # returns the openid structure
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

        # sets the mode in the openid structure
        self.openid_structure.mode = ID_RES_VALUE

        # sets the invalidate handle in the openid structure
        self.openid_structure.invalidate_handle = invalidate_handle

        # sets the response nonce in the openid structure
        self.openid_structure.response_nonce = response_nonce

        # sets the signed in the openid structure
        self.openid_structure.signed = ",".join(DEFAULT_SIGNED_NAMES)

        # generates the signature
        signature = self._generate_signature()

        # sets the signature in the openid structure
        self.openid_structure.signature = signature

    def openid_check_authentication(self, return_openid_structure, strict = True):
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
                           self.openid_structure.response_nonce == return_openid_structure.response_nonce and\
                           self.openid_structure.signed == return_openid_structure.signed and\
                           self.openid_structure.signature == return_openid_structure.signature and\
                           return_openid_structure.ns == OPENID_NAMESPACE_VALUE):
            # raises a verification failed exception
            raise service_openid_exceptions.VerificationFailed("invalid discovered information")

        # returns the openid structure
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
            # retrieves the mac key type to be used
            mac_key_type = self._get_mac_key_type()

            # generates the "B" value
            B_value = self.diffie_hellman.generate_B()

            # calculates the shared key value
            key_value = self.diffie_hellman.calculate_Kb()

            # decodes the mac key using base64
            decoded_mac_key = base64.b64decode(self.openid_structure.mac_key)

            # retrieves the hash module from the hmac hash modules map
            hash_module = HMAC_HASH_MODULES_MAP.get(mac_key_type, None)

            # encodes the key value in order to be used in the xor operation
            encoded_key_value = hash_module(self.service_openid._btwoc(key_value)).digest()

            # calculates the encoded mac key value and retrieves the digest
            encoded_mac_key = colony.libs.string_util.xor_string_value(decoded_mac_key, encoded_key_value)

            # encodes the encoded mac key into base64
            encoded_mac_key = base64.b64encode(encoded_mac_key)

            # sets the dh server public
            parameters["dh_server_public"] = base64.b64encode(self.service_openid._btwoc(B_value))

            # sets the encoded mac key
            parameters["enc_mac_key"] = encoded_mac_key
        else:
            # sets the mac key
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
        # sets the retrieval url
        retrieval_url = self.openid_structure.return_to

        # start the parameters map
        parameters = {}

        # sets the namespace
        parameters["openid.ns"] = self.openid_structure.ns

        # sets the mode
        parameters["openid.mode"] = self.openid_structure.mode

        # sets the provider url
        parameters["openid.op_endpoint"] = self.openid_structure.provider_url

        # sets the claimed id
        parameters["openid.claimed_id"] = self.openid_structure.claimed_id

        # sets the identity
        parameters["openid.identity"] = self.openid_structure.identity

        # sets the return to
        parameters["openid.return_to"] = self.openid_structure.return_to

        # sets the response nonce
        parameters["openid.response_nonce"] = self.openid_structure.response_nonce

        # sets the invalidate handle
        parameters["openid.invalidate_handle"] = self.openid_structure.invalidate_handle

        # sets the association handle
        parameters["openid.assoc_handle"] = self.openid_structure.association_handle

        # sets the signed
        parameters["openid.signed"] = self.openid_structure.signed

        # sets the signature
        parameters["openid.sig"] = self.openid_structure.signature

        # creates the request (get) url from the parameters
        request_url = self._build_get_url(retrieval_url, parameters)

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

    def _get_mac_key_type(self):
        """
        Retrieves the type of hashing to be used in the
        mac key.

        @rtype: String
        @return: The type of hashing to be used in the mac key.
        """

        # in case the current session is of type no encryption
        if self.openid_structure.session_type == NO_ENCRYPTION_VALUE:
            # returns the current association type
            return self.openid_structure.association_type
        # in case the current session is of type dh sha1
        elif self.openid_structure.session_type == DH_SHA1_VALUE:
            # returns the hmac sha1 value
            return HMAC_SHA1_VALUE
        # in case the current session is of type dh sha256
        elif self.openid_structure.session_type == DH_SHA256_VALUE:
            # returns the hmac sha256 value
            return HMAC_SHA256_VALUE

    def _generate_signature(self):
        # sets the signature items list
        signed_items_list = DEFAULT_SIGNED_ITEMS

        # sets the signature names list
        signed_names_list = DEFAULT_SIGNED_NAMES

        # creates the string buffer for the message
        message_string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # starts the index counter
        index = 0

        # iterates over all the signed items
        for signed_item_name in signed_items_list:
            # retrieves the signed item value from the return openid structure
            signed_item_value = getattr(self.openid_structure, signed_item_name)

            # retrieves the signed item real name
            signed_item_real_name = signed_names_list[index]

            # adds the key value pair to the message string buffer
            message_string_buffer.write(signed_item_real_name.encode(DEFAULT_CHARSET) + ":" + signed_item_value.encode(DEFAULT_CHARSET) + "\n")

            # increments the index
            index += 1

        # retrieves the value from the message string buffer
        message = message_string_buffer.get_value()

        # decodes the signature mac key from base64
        signature_mac_key = base64.b64decode(self.openid_structure.mac_key)

        # retrieves the hash module from the hmac hash modules map
        hash_module = HMAC_HASH_MODULES_MAP.get(self.openid_structure.association_type, None)

        # in case no hash module is set
        if not hash_module:
            # raises the invalid hash function exception
            raise service_openid_exceptions.InvalidHashFunction("the hash function is not available: " + self.openid_structure.association_type)

        # calculates the signature value and retrieves the digest
        signature = hmac.new(signature_mac_key, message, hash_module).digest()

        # encodes the signature into base64
        signature = base64.b64encode(signature)

        # returns the signature
        return signature

    def _generate_handle(self):
        # generates a random sha1
        random_sha1 = self.random_plugin.generate_random_sha1()

        # retrieves the random sha1 value
        random_sha1_value = random_sha1.digest()

        # encodes the random sha1 value into base64
        handle = base64.b64encode(random_sha1_value)

        # returns the handle
        return handle

    def _generate_mac_key(self, mac_key_type = HMAC_SHA1_VALUE):
        # in case the key type is sha1
        if mac_key_type == HMAC_SHA1_VALUE:
            # generates a mac key with the sha1 random value
            mac_key = self.random_plugin.generate_random_sha1()
        # in case the key type is sha256
        elif mac_key_type == HMAC_SHA256_VALUE:
            # generates a mac key with the sha256 random value
            mac_key = self.random_plugin.generate_random_sha256()

        # retrieves the mac key value
        mac_key_value = mac_key.digest()

        # encodes the mac key into base64
        mac_key_value_encoded = base64.b64encode(mac_key_value)

        # returns the encoded mac key value
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
        Builds the url for the given url and parameters.
        The url is valid only for a get request.

        @type base_url: String
        @param base_url: The base url to be used.
        @type parameters: Dictionary
        @param parameters: The parameters to be used for url construction.
        @rtype: String
        @return: The built url for the given parameters.
        """

        # encodes the parameters with the url encode
        parameters_encoded = colony.libs.quote_util.url_encode(parameters)

        # in case the base url does not contain any parameters
        if base_url.find("?") == -1:
            # creates the url value by appending the base url with
            # the parameters encoded (new parameters)
            url = base_url + "?" + parameters_encoded
        # otherwise
        else:
            # creates the url value by appending the base url with
            # the parameters encoded (existing parameters)
            url = base_url + "&" + parameters_encoded

        # returns the built url
        return url

    def _encode_key_value(self, values_map):
        """
        Encodes the given values map into the key value
        encoding.

        @type values_map: Dictionary
        @param values_map: The map containing the values to be
        encoded.
        @rtype: String
        @return: The key value encoded string.
        """

        return "\n".join([key + ":" + value for key, value in values_map.items()])

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
            message_string_buffer.write(signed_item_name.encode(DEFAULT_CHARSET) + ":" + signed_item_value.encode(DEFAULT_CHARSET) + "\n")

        # retrieves the value from the message string buffer
        message = message_string_buffer.get_value()

        # decodes the signature mac key from base64
        signature_mac_key = base64.b64decode(self.openid_structure.mac_key)

        # retrieves the hash module from the hmac hash modules map
        hash_module = HMAC_HASH_MODULES_MAP.get(self.openid_structure.association_type, None)

        # in case no hash module is set
        if not hash_module:
            # raises the invalid hash function exception
            raise service_openid_exceptions.InvalidHashFunction("the hash function is not available: " + self.openid_structure.association_type)

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

        # returns the openid structure
        return self.openid_structure

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

    mode = None
    """ The mode """

    expires_in = None
    """ The expires in """

    association_handle = None
    """ The association handle """

    invalidate_handle = None
    """ The invalidate handle """

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
        Sets the identity.

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
        Sets the return to.

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
        Sets the realm.

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
        Sets the association type.

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
        Sets the session type.

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
        Sets the namespace.

        @type ns: String
        @param ns: The namespace.
        """

        self.ns = ns

    def get_mode(self):
        """
        Retrieves the mode.

        @rtype: String
        @return: The mode.
        """

        return self.mode

    def set_mode(self, mode):
        """
        Sets the mode.

        @type mode: String
        @param mode: The mode.
        """

        self.mode = mode

    def get_expires_in(self):
        """
        Retrieves the expires in.

        @rtype: String
        @return: The expires in.
        """

        return self.expires_in

    def set_expires_in(self, expires_in):
        """
        Sets the expires in.

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
        Sets the association handle.

        @type association_handle: String
        @param association_handle: The association handle.
        """

        self.association_handle = association_handle

    def get_invalidate_handle(self):
        """
        Retrieves the invalidate handle.

        @rtype: String
        @return: The invalidate handle.
        """

        return self.invalidate_handle

    def set_invalidate_handle(self, invalidate_handle):
        """
        Sets the invalidate handle.

        @type invalidate_handle: String
        @param invalidate_handle: The invalidate handle.
        """

        self.invalidate_handle = invalidate_handle

    def get_mac_key(self):
        """
        Retrieves the mac key.

        @rtype: String
        @return: The mac key.
        """

        return self.mac_key

    def set_mac_key(self, mac_key):
        """
        Sets the mac key.

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
        Sets the signed.

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
        Sets the signature.

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
        Sets the response nonce.

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
        Sets the local id.

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
        Sets the types list.

        @type types_list: List
        @param types_list: The types list.
        """

        self.types_list = types_list
