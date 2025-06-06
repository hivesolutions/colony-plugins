#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import base64

import colony

BASE_64_ENCODED_MAXIMUM_SIZE = 64
""" The base 64 encoded maximum size """

DEFAULT_NUMBER_BITS = 1024
""" The default number of bits to be used in the generation
of the private key """


class SSL(colony.System):
    """
    The SSL class, responsible for the creation of
    the associated structure for manipulation.
    """

    def create_structure(self, parameters):
        # retrieves the required plugins for the creation
        # of the associated (SSL) structure
        rsa_plugin = self.plugin.rsa_plugin
        pkcs1_plugin = self.plugin.pkcs1_plugin

        # creates the SSL structure with the provided plugins
        # and then returns it to the caller method
        ssl_structure = SSLStructure(rsa_plugin, pkcs1_plugin)
        return ssl_structure


class SSLStructure(object):
    """
    Class representing the SSL, cryptographic
    protocol structure.

    Should provide a top level interface for the
    cryptographic operation used in the SSL protocol.
    """

    rsa_plugin = None
    """ The RSA plugin """

    pkcs1_plugin = None
    """ The PKCS1 plugin """

    def __init__(self, rsa_plugin, pkcs1_plugin):
        """
        Constructor of the class.

        :type rsa_plugin: RSAPlugin
        :param rsa_plugin: The RSA plugin.
        :type pkcs1_plugin: PKCS1Plugin
        :param pkcs1_plugin: The PKCS1 plugin.
        """

        self.rsa_plugin = rsa_plugin
        self.pkcs1_plugin = pkcs1_plugin

    def generate_keys(
        self, private_key_path, public_key_path, number_bits=DEFAULT_NUMBER_BITS
    ):
        # creates both structures that are required for
        # the generation of the keys an packing of them
        rsa_structure = self.rsa_plugin.create_structure({})
        pkcs1_structure = self.pkcs1_plugin.create_structure({})

        # generates the keys in the RSA structure and then
        # retrieves them as plain strings, to be encoded
        rsa_structure.generate_keys(number_bits)
        keys = rsa_structure.get_keys()

        # writes the keys in PEM format to the target file
        # paths, so that they may be used latter
        pkcs1_structure.generate_write_keys_pem(keys, private_key_path, public_key_path)

    def encrypt_base_64(self, public_key_path, message):
        # ensures that the provided message is properly encoded as
        # a byte sequence as expected by the encoder
        message = colony.legacy.bytes(message)

        # encrypts the message, creating the encrypted version
        # of the message, according to the RSA and PKCS specification
        message_e = self.encrypt(public_key_path, message)

        # encodes the encrypted message into base 64
        # and splits the various components from it
        message_e = colony.legacy.bytes(message_e)
        message_e_base_64 = base64.b64encode(message_e)
        message_e_base_64 = colony.legacy.str(message_e_base_64)
        message_e_base_64 = self._split_base_64(message_e_base_64)

        # returns the encrypted message in base 64
        return message_e_base_64

    def decrypt_base_64(self, private_key_path, message_e_base_64):
        # decodes the encoded message from the original base 64
        # version so that it may be decrypted correctly
        message_e_base_64 = self._join_base_64(message_e_base_64)
        message_e_base_64 = colony.legacy.bytes(message_e_base_64)
        message_e = base64.b64decode(message_e_base_64)
        message_e = colony.legacy.str(message_e)

        # decrypts the encrypted message, retrieving the original
        # message, according to the RSA and PKCS specification
        message = self.decrypt(private_key_path, message_e)

        # returns the decrypted message as plain text as
        # in the original version of the buffer
        return message

    def sign_base_64(self, private_key_path, hash_algorithm_name, base_string_value):
        # signs the base string value using the hash algorithm
        # with the given name and retrieving the signature
        signature = self.sign(private_key_path, hash_algorithm_name, base_string_value)

        # encodes the signature into base 64 and splits
        # the various components from it
        signature = colony.legacy.bytes(signature)
        signature_base_64 = base64.b64encode(signature)
        signature_base_64 = colony.legacy.str(signature_base_64)
        signature_base_64 = self._split_base_64(signature_base_64)

        # returns the signature base 64
        return signature_base_64

    def verify_base_64(self, public_key_path, signature_base_64, base_string_value):
        # joins the base 64 value back, removing any extra newline
        # characters and then decodes the signature from base 64
        # back to plain text
        signature_base_64 = self._join_base_64(signature_base_64)
        signature_base_64 = colony.legacy.bytes(signature_base_64)
        signature = base64.b64decode(signature_base_64)
        signature = colony.legacy.str(signature)

        # verifies the signature against the base string value,
        # and returns the return value
        return_value = self.verify(public_key_path, signature, base_string_value)

        # returns the return value
        return return_value

    def encrypt(self, public_key_path, message):
        # creates the RSA structure
        rsa_structure = self.rsa_plugin.create_structure({})

        # creates the PKCS1 structure then loads the public key,
        # retrieving the keys tuple and sets the keys in the RSA structure
        pkcs1_structure = self.pkcs1_plugin.create_structure({})
        keys = pkcs1_structure.load_read_public_key_pem(public_key_path)
        rsa_structure.set_keys(keys)

        # runs the encrypt process for the PKCS that should add the
        # proper padding to the message to be encrypted the uses RSA
        # to encrypt the message with the public key
        message_pad = pkcs1_structure.encrypt(keys, message)
        encrypted_message = rsa_structure.encrypt_s(message_pad)

        # returns the resulting encrypted message buffer to be used
        # for cryptographic purposes
        return encrypted_message

    def decrypt(self, private_key_path, encrypted_message):
        # creates the RSA structure
        rsa_structure = self.rsa_plugin.create_structure({})

        # creates the PKCS1 structure then loads the private key,
        # retrieving the keys tuple and the version value and sets
        # them in the RSA structure
        pkcs1_structure = self.pkcs1_plugin.create_structure({})
        keys, _version = pkcs1_structure.load_read_private_key_pem(private_key_path)
        rsa_structure.set_keys(keys)

        # runs the decryption process over the message to be able
        # to retrieve the plain text value and then removes the
        # padding from it according to the PKCS specification
        message_pad = rsa_structure.decrypt_s(encrypted_message)
        message = pkcs1_structure.decrypt(keys, message_pad)

        # returns the original plain message resulting from the
        # standard PKCS decryption process
        return message

    def sign(self, private_key_path, hash_algorithm_name, base_string_value):
        # creates the RSA structure
        rsa_structure = self.rsa_plugin.create_structure({})

        # creates the PKCS1 structure then loads the private key,
        # retrieving the keys tuple and the version value and sets
        # them in the RSA structure
        pkcs1_structure = self.pkcs1_plugin.create_structure({})
        keys, _version = pkcs1_structure.load_read_private_key_pem(private_key_path)
        rsa_structure.set_keys(keys)

        # signs the base string value using the given hash
        # algorithm name and then used the resulting string
        # value to sign (encrypt) it under RSA using the
        # private key
        signature_verified = pkcs1_structure.sign(
            keys, hash_algorithm_name, base_string_value
        )
        signature = rsa_structure.sign(signature_verified)

        # returns the resulting signature value as a plain
        # byte sequence string
        return signature

    def verify(self, public_key_path, signature, base_string_value):
        # creates the RSA structure
        rsa_structure = self.rsa_plugin.create_structure({})

        # creates the PKCS1 structure then loads the public key,
        # retrieving the keys tuple and sets the keys in the RSA structure
        pkcs1_structure = self.pkcs1_plugin.create_structure({})
        keys = pkcs1_structure.load_read_public_key_pem(public_key_path)
        rsa_structure.set_keys(keys)

        # verifies the signature (using the public key) and
        # retrieves the signature verified (decrypted message),
        # then uses it to run the final PKCS1 verification
        # process that will compare the the verified signature
        # value against the hash value of the provided base string
        signature_verified = rsa_structure.verify(signature)
        return_value = pkcs1_structure.verify(signature_verified, base_string_value)

        # returns the return value
        return return_value

    def _split_base_64(self, string_value):
        # retrieves the string value length
        string_value_length = len(string_value)

        # starts the base index
        base_index = 0

        # creates the list
        string_value_list = []

        # iterates continuously, in order to properly split
        # the (long) key into multiple lines
        while True:
            # in case the base index is greater or equal
            # to the private key DER encoded length must
            # break the loop (end of iteration)
            if base_index >= string_value_length:
                break

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
        # the plain base 64 value (one line only)
        string_value_joined = string_value.replace("\n", "")

        # returns the string value joined
        return string_value_joined
