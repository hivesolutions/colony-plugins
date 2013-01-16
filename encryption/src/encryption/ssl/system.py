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

import base64

import colony.base.system

BASE_64_ENCODED_MAXIMUM_SIZE = 64
""" The base 64 encoded maximum size """

DEFAULT_NUMBER_BITS = 1024
""" The default number of bits """

class Ssl(colony.base.system.System):
    """
    The ssl class.
    """

    def create_structure(self, parameters):
        # retrieves the rsa plugin
        rsa_plugin = self.plugin.rsa_plugin

        # retrieves the pkcs 1 plugin
        pkcs_1_plugin = self.plugin.pkcs_1_plugin

        # creates the ssl structure
        ssl_structure = SslStructure(rsa_plugin, pkcs_1_plugin)

        # returns the ssl structure
        return ssl_structure

class SslStructure:
    """
    Class representing the ssl, cryptographic
    protocol structure.

    Should provide a top level interface for the
    cryptographic operation used in the ssl protocol.
    """

    rsa_plugin = None
    """ The rsa plugin """

    pkcs_1_plugin = None
    """ The pkcs 1 plugin """

    def __init__(self, rsa_plugin, pkcs_1_plugin):
        """
        Constructor of the class.

        @type rsa_plugin: RsaPlugin
        @param rsa_plugin: The rsa plugin.
        @type pkcs_1_plugin: Pkcs1Plugin
        @param pkcs_1_plugin: The pkkc 1 plugin.
        """

        self.rsa_plugin = rsa_plugin
        self.pkcs_1_plugin = pkcs_1_plugin

    def generate_keys(self, private_key_path, public_key_path, number_bits = DEFAULT_NUMBER_BITS):
        # creates the rsa structure
        rsa_structure = self.rsa_plugin.create_structure({})

        # creates the pkcs 1 structure
        pkcs_1_structure = self.pkcs_1_plugin.create_structure({})

        # generates the keys in the rsa structure
        rsa_structure.generate_keys(number_bits)

        # retrieves the keys from the rsa structure
        keys = rsa_structure.get_keys()

        # writes the keys in pem format
        pkcs_1_structure.generate_write_keys_pem(keys, private_key_path, public_key_path)

    def sign_base_64(self, private_key_path, hash_algorithm_name, base_string_value):
        # signs the base string value using the hash algorithm
        # with the given name and retrieving the signature
        signature = self.sign(private_key_path, hash_algorithm_name, base_string_value)

        # encodes the signature into base 64 and splits
        # the various components from it
        signature_base_64 = base64.b64encode(signature)
        signature_base_64 = self._split_base_64(signature_base_64)

        # returns the signature base 64
        return signature_base_64

    def verify_base_64(self, public_key_path, signature_base_64, base_string_value):
        # joins the base 64 value back, removing any extra newline
        # characters and then decodes the signature from base 64
        # back to plain text
        signature_base_64 = self._join_base_64(signature_base_64)
        signature = base64.b64decode(signature_base_64)

        # verifies the signature against the base string value,
        # and returns the return value
        return_value = self.verify(public_key_path, signature, base_string_value)

        # returns the return value
        return return_value

    def encrypt(self, public_key_path, message):
        # creates the rsa structure
        rsa_structure = self.rsa_plugin.create_structure({})

        # creates the pkcs 1 structure then loads the public key,
        # retrieving the keys tuple and sets the keys in the rsa structure
        pkcs_1_structure = self.pkcs_1_plugin.create_structure({})
        keys = pkcs_1_structure.load_read_public_key_pem(public_key_path)
        rsa_structure.set_keys(keys)

        # runs the encryption process over the message and returns
        # the resulting encrypted message to the caller method
        encrypted_message = rsa_structure.encrypt(message)
        return encrypted_message

    def decrypt(self, private_key_path, encrypted_message):
        # creates the rsa structure
        rsa_structure = self.rsa_plugin.create_structure({})

        # creates the pkcs 1 structure then loads the private key,
        # retrieving the keys tuple and the version value and sets
        # them in the rsa structure
        pkcs_1_structure = self.pkcs_1_plugin.create_structure({})
        keys, _version = pkcs_1_structure.load_read_private_key_pem(private_key_path)
        rsa_structure.set_keys(keys)

        # runs the decryption process over the message and returns
        # the resulting message to the caller method
        message = rsa_structure.decypt(encrypted_message)
        return message

    def sign(self, private_key_path, hash_algorithm_name, base_string_value):
        # creates the rsa structure
        rsa_structure = self.rsa_plugin.create_structure({})

        # creates the pkcs 1 structure then loads the private key,
        # retrieving the keys tuple and the version value and sets
        # them in the rsa structure
        pkcs_1_structure = self.pkcs_1_plugin.create_structure({})
        keys, _version = pkcs_1_structure.load_read_private_key_pem(private_key_path)
        rsa_structure.set_keys(keys)

        # signs the base string value using the given hash
        # algorithm name and then used the resulting string
        # value to sign (encrypt) it under rsa using the
        # private key
        signature_verified = pkcs_1_structure.sign(keys, hash_algorithm_name, base_string_value)
        signature = rsa_structure.sign(signature_verified)

        # returns the resulting signature value as a plain
        # byte sequence string
        return signature

    def verify(self, public_key_path, signature, base_string_value):
        # creates the rsa structure
        rsa_structure = self.rsa_plugin.create_structure({})

        # creates the pkcs 1 structure then loads the public key,
        # retrieving the keys tuple and sets the keys in the rsa structure
        pkcs_1_structure = self.pkcs_1_plugin.create_structure({})
        keys = pkcs_1_structure.load_read_public_key_pem(public_key_path)
        rsa_structure.set_keys(keys)

        # verifies the signature (using the public key) and
        # retrieves the signature verified (decrypted message),
        # then uses it to run the final pkcs1 verification
        # process that will compare the the verified signature
        # value against the hash value of the provided base string
        signature_verified = rsa_structure.verify(signature)
        return_value = pkcs_1_structure.verify(signature_verified, base_string_value)

        # returns the return value
        return return_value

    def _split_base_64(self, string_value):
        # retrieves the string value length
        string_value_length = len(string_value)

        # starts the base index
        base_index = 0

        # creates the list
        string_value_list = []

        # iterates continuously
        while True:
            # in case the base index is greater or equal
            # to the private key der encoded length must
            # break the loop (end of iteration)
            if base_index >= string_value_length: break

            # calculates the end index from the base index
            end_index = base_index + BASE_64_ENCODED_MAXIMUM_SIZE

            # retrieves the string value token
            string_value_token = string_value[base_index:end_index]

            # creates the string value from the string value token
            # and a newline character then adds the string value
            # line to the string value list
            string_value_line = string_value_token + "\n"
            string_value_list.append(string_value_line)

            # sets the base index as the end index
            base_index = end_index

        # joins the string value list retrieving the
        # string value splitted
        string_value_splitted = "".join(string_value_list)

        # returns the string value splitted
        return string_value_splitted

    def _join_base_64(self, string_value):
        # removes the newline characters to obtain
        # the plain base 64 value
        string_value_joined = string_value.replace("\n", "")

        # returns the string value joined
        return string_value_joined
