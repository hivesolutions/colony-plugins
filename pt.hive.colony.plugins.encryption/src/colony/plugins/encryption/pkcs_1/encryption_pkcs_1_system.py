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

import re
import base64
import hashlib

import encryption_pkcs_1_exceptions

TYPE_VALUE = "type"
""" The type value """

VALUE_VALUE = "value"
""" The value value """

TYPE_CONSTRUCTED_VALUE = "type_constructed"
""" The type constructed value """

TYPE_NUMBER_VALUE = "type_number"
""" The type number value """

TYPE_CLASS_VALUE = "type_class"
""" The type class value """

BEGIN_RSA_PRIVATE_VALUE = "-----BEGIN RSA PRIVATE KEY-----"
""" The begin rsa private value """

END_RSA_PRIVATE_VALUE = "-----END RSA PRIVATE KEY-----"
""" The end rsa private value """

BEGIN_PUBLIC_VALUE = "-----BEGIN PUBLIC KEY-----"
""" The begin public value """

END_PUBLIC_VALUE = "-----END PUBLIC KEY-----"
""" The end public value """

PRIVATE_KEY_VALUE_REGEX = re.compile(BEGIN_RSA_PRIVATE_VALUE + "\n(?P<contents>.*)\n" + END_RSA_PRIVATE_VALUE, re.DOTALL)
""" The private key value regex """

PUBLIC_KEY_VALUE_REGEX = re.compile(BEGIN_PUBLIC_VALUE + "\n(?P<contents>.*)\n" + END_PUBLIC_VALUE, re.DOTALL)
""" The public key value regex """

BASE_64_ENCODED_MAXIMUM_SIZE = 64
""" The base 64 encoded maximum size """

INTEGER_TYPE = 0x02
""" The integer type """

BIT_STRING_TYPE = 0x03
""" The bit string type """

NULL_TYPE = 0x05
""" The null type """

OBJECT_IDENTIFIER_TYPE = 0x06
""" The object identifier type """

SEQUENCE_TYPE = 0x10
""" The sequence type """

OBJECT_IDENTIFIERS_TUPLES_MAP = {"pkcs_1" : (1, 2, 840, 113549, 1, 1),
                                 "rsa_encryption" : (1, 2, 840, 113549, 1, 1, 1),
                                 "id_rsaes_oaep" : (1, 2, 840, 113549, 1, 1, 7),
                                 "id_p_specified" : (1, 2, 840, 113549, 1, 1, 9),
                                 "id_rsassa_pss" : (1, 2, 840, 113549, 1, 1, 10),
                                 "md2_with_rsa_encryption" : (1, 2, 840, 113549, 1, 1, 2),
                                 "md5_with_rsa_encryption" : (1, 2, 840, 113549, 1, 1, 4),
                                 "sha1_with_rsa_encryption" : (1, 2, 840, 113549, 1, 1, 5),
                                 "sha256_with_rsa_encryption" : (1, 2, 840, 113549, 1, 1, 11),
                                 "sha384_with_rsa_encryption" : (1, 2, 840, 113549, 1, 1, 12),
                                 "sha512_with_rsa_encryption" : (1, 2, 840, 113549, 1, 1, 13)}
""" The map associating the object identifiers with the tuples """

TUPLES_OBJECT_IDENTIFIERS_MAP = {(1, 2, 840, 113549, 1, 1) : "pkcs_1",
                                 (1, 2, 840, 113549, 1, 1, 1) : "rsa_encryption",
                                 (1, 2, 840, 113549, 1, 1, 7) : "id_rsaes_oaep",
                                 (1, 2, 840, 113549, 1, 1, 9) : "id_p_specified",
                                 (1, 2, 840, 113549, 1, 1, 10) : "id_rsassa_pss",
                                 (1, 2, 840, 113549, 1, 1, 2) : "md2_with_rsa_encryption",
                                 (1, 2, 840, 113549, 1, 1, 4) : "md5_with_rsa_encryption",
                                 (1, 2, 840, 113549, 1, 1, 5) : "sha1_with_rsa_encryption",
                                 (1, 2, 840, 113549, 1, 1, 11) : "sha256_with_rsa_encryption",
                                 (1, 2, 840, 113549, 1, 1, 12) : "sha384_with_rsa_encryption",
                                 (1, 2, 840, 113549, 1, 1, 13) : "sha512_with_rsa_encryption"}
""" The map associating the tuples with the object identifiers """

TUPLES_HASH_OBJECT_IDENTIFIERS_MAP = {(1, 2, 840, 113549, 2, 2) : "md2",
                                      (1, 2, 840, 113549, 2, 5) : "md5",
                                      (1, 3, 14, 3, 2, 26) : "sha1",
                                      (2, 16, 840, 1, 101, 3, 4, 2, 1) : "sha256",
                                      (2, 16, 840, 1, 101, 3, 4, 2, 2) : "sha384",
                                      (2, 16, 840, 1, 101, 3, 4, 2, 3) : "sha512"}
""" The map associating the tuples with the hash object identifiers """

class EncryptionPkcs1:
    """
    The encryption pkcs 1 class.
    """

    encryption_pkcs_1_plugin = None
    """ The encryption pkcs 1 plugin """

    def __init__(self, encryption_pkcs_1_plugin):
        """
        Constructor of the class.

        @type encryption_pkcs_1_plugin: EncryptionPkcs1Plugin
        @param encryption_pkcs_1_plugin: The encryption pkcs 1 plugin.
        """

        self.encryption_pkcs_1_plugin = encryption_pkcs_1_plugin

    def create_structure(self, parameters):
        # retrieves the format ber plugin
        format_ber_plugin = self.encryption_pkcs_1_plugin.format_ber_plugin

        # creates the pkcs 1 structure
        pkcs_1_structure = Pkcs1Structure(format_ber_plugin)

        # returns the pkcs 1 structure
        return pkcs_1_structure

class Pkcs1Structure:
    """
    Class representing the pkcs 1,
    cryptographic standards structure.
    """

    format_ber_plugin = None
    """ the format ber plugin """

    def __init__(self, format_ber_plugin):
        """
        Constructor of the class.

        @type format_ber_plugin: Plugin
        @param format_ber_plugin: The format ber plugin.
        """

        self.format_ber_plugin = format_ber_plugin

    def generate_write_keys_pem(self, keys, private_key_file_path, public_key_file_path, version = 1):
        # generates the public and private key pem values
        private_key_pem, public_key_pem = self.generate_keys_pem(keys, version)

        # writes the private and public key files
        self._write_file(private_key_file_path, private_key_pem)
        self._write_file(public_key_file_path, public_key_pem)

    def generate_keys_pem(self, keys, version = 1):
        # generates the private key pem
        private_key_pem = self.generate_private_key_pem(keys)

        # generates the public key pem
        public_key_pem = self.generate_public_key_pem(keys)

        # creates a tuple with the private key and public key pem
        keys_pem = (private_key_pem, public_key_pem)

        # returns the keys pem
        return keys_pem

    def load_read_private_key_pem(self, private_key_file_path):
        # reads the file, retrieving the private key pem
        private_key_pem = self._read_file(private_key_file_path)

        # loads the private key pem, retrieving the return tuple
        return_tuple = self.load_private_key_pem(private_key_pem)

        # returns the return tuple
        return return_tuple

    def load_read_public_key_pem(self, public_key_file_path):
        # reads the file, retrieving the public key pem
        public_key_pem = self._read_file(public_key_file_path)

        # loads the public key pem, retrieving the keys tuple
        keys = self.load_public_key_pem(public_key_pem)

        # returns the keys tuple
        return keys

    def verify_test(self, keys, signature_verified, string_value):
        # verifies the keys and the signature verified, retrieving
        # the hash algorithm name and the digest value
        hash_algorithm_name, digest_value = self.verify(keys, signature_verified)

        # creates a new hash using the given hash algorithm name
        hash = hashlib.new(hash_algorithm_name)

        # updates the hash with the string value
        hash.update(string_value)

        # retrieves the hash digest
        hash_digest = hash.digest()

        # in case the hash digest value is
        # the same as the digest value
        if hash_digest == digest_value:
            # returns true (valid)
            return True
        # otherwise
        else:
            # returns false (invalid)
            return False

    def verify(self, keys, signature_verified):
        # retrieves the first character
        first_character = signature_verified[0]

        # converts the first character to ordinal
        first_character_ordinal = ord(first_character)

        # in case the first character ordinal is not one
        if not first_character_ordinal == 0x01:
            # raises the invalid format exception
            raise encryption_pkcs_1_exceptions.InvalidFormatException("invalid signature format")

        # creates the ber structure
        ber_structure = self.format_ber_plugin.create_structure({})

        # retrieves the signature verified length
        signature_verified_length = len(signature_verified)

        # iterates over the range of the signature verified length
        # starting in the one value
        for index in range(1, signature_verified_length):
            # retrieves the current character
            current_character = signature_verified[index]

            # converts the current character to ordinal
            current_character_ordinal = ord(current_character)

            # in case the current character ordinal is zero
            # (end of padding part)
            if current_character_ordinal == 0x00:
                # breaks the loop
                break

        # retrieves the signature value
        signature_value = signature_verified[index + 1:]

        # unpacks the signature value
        signature_value_unpacked = ber_structure.unpack(signature_value)

        signature_value_value = signature_value_unpacked[VALUE_VALUE]

        # retrieves the digest algorithm and the digest algorithm value
        digest_algorithm = signature_value_value[0]
        digest_algorithm_value = digest_algorithm[VALUE_VALUE]

        # retrieves the algorithm and the algorithm value
        algorithm = digest_algorithm_value[0]
        algorithm_value = algorithm[VALUE_VALUE]

        # retrieves the arguments and the arguments value
        arguments = digest_algorithm_value[1]
        arguments_value = arguments[VALUE_VALUE]

        # retrieves the digest and the digest value
        digest = signature_value_value[1]
        digest_value = digest[VALUE_VALUE]

        # in case the arguments value is not none
        if not arguments_value == None:
            # raises the invalid format exception
            raise encryption_pkcs_1_exceptions.InvalidFormatException("invalid arguments value: " + str(arguments_value))

        # retrieves the hash algorithm name
        hash_algorithm_name = TUPLES_HASH_OBJECT_IDENTIFIERS_MAP[algorithm_value]

        # creates the return tuple with the hash algorithm name
        # and the digest value
        return_tuple = (hash_algorithm_name, digest_value)

        # returns the return value
        return return_tuple

    def generate_private_key_pem(self, keys, version = 1):
        """
        Generates the a private key in pem format, using
        the given keys value.

        @type keys: Tuple
        @param keys: A tuple containing the public, private
        and extra key values.
        @type version: int
        @param version: The version of the keys to be generated.
        @rtype: String
        @return: The generated private key in pem format.
        """

        # retrieves the private key in der format
        private_key_der = self.generate_private_key_der(keys, version)

        # encodes the private key der in base 64
        private_key_der_encoded = base64.b64encode(private_key_der)

        # creates the string value list
        string_value_list = []

        # adds the begin rsa private value to the string value list
        string_value_list.append(BEGIN_RSA_PRIVATE_VALUE + "\n")

        # splits the private key der encoded value
        private_key_der_splitted = self._split_base_64(private_key_der_encoded)

        # adds the private key der splitted to the string value list
        string_value_list.append(private_key_der_splitted)

        # adds the end rsa private value to the string value list
        string_value_list.append(END_RSA_PRIVATE_VALUE + "\n")

        # joins the string value list retrieving the
        # private key pem value
        private_key_pem = "".join(string_value_list)

        # returns the private key pem value
        return private_key_pem

    def generate_public_key_pem(self, keys):
        """
        Generates the a public key in pem format, using
        the given keys value.

        @type keys: Tuple
        @param keys: A tuple containing the public, private
        and extra key values.
        @rtype: String
        @return: The generated public key in pem format.
        """

        # retrieves the public key in der format
        public_key_der = self.generate_public_key_der(keys)

        # encodes the public key der in base 64
        public_key_der_encoded = base64.b64encode(public_key_der)

        # creates the string value list
        string_value_list = []

        # adds the begin rsa public value to the string value list
        string_value_list.append(BEGIN_PUBLIC_VALUE + "\n")

        # splits the public key der encoded value
        public_key_der_splitted = self._split_base_64(public_key_der_encoded)

        # adds the public key der splitted to the string value list
        string_value_list.append(public_key_der_splitted)

        # adds the end rsa public value to the string value list
        string_value_list.append(END_PUBLIC_VALUE + "\n")

        # joins the string value list retrieving the
        # public key pem value
        public_key_pem = "".join(string_value_list)

        # returns the public key pem value
        return public_key_pem

    def load_private_key_pem(self, private_key_pem):
        # matches the private key pem
        private_key_pem_match = PRIVATE_KEY_VALUE_REGEX.match(private_key_pem)

        # retrieves the private key pem contents
        private_key_pem_contents = private_key_pem_match.group("contents")

        # joins the base 64 value back together
        private_key_pem_contents_joined = self._join_base_64(private_key_pem_contents)

        # decodes the private key pem from base 64, obtaining
        # private key der
        private_key_der = base64.b64decode(private_key_pem_contents_joined)

        # loads the private key der, retrieving the return tuple
        return_tuple = self.load_private_key_der(private_key_der)

        # returns the return tuple
        return return_tuple

    def load_public_key_pem(self, public_key_pem):
        # matches the public key pem
        public_key_pem_match = PUBLIC_KEY_VALUE_REGEX.match(public_key_pem)

        # retrieves the public key pem contents
        public_key_pem_match_contents = public_key_pem_match.group("contents")

        # joins the base 64 value back together
        public_key_pem_match_contents_joined = self._join_base_64(public_key_pem_match_contents)

        # decodes the public key pem from base 64, obtaining
        # public key der
        public_key_der = base64.b64decode(public_key_pem_match_contents_joined)

        # loads the public key der, retrieving the keys tuple
        keys = self.load_public_key_der(public_key_der)

        # returns the keys tuple
        return keys

    def generate_private_key_der(self, keys, version = 1):
        """
        Generates the a private key in der format, using
        the given keys value.

        @type keys: Tuple
        @param keys: A tuple containing the public, private
        and extra key values.
        @type version: int
        @param version: The version of the keys to be generated.
        @rtype: String
        @return: The generated private key in der format.
        """

        # unpacks the keys value
        public_key, private_key, extras = keys

        # retrieves the public key values
        modulus = public_key["n"]
        public_exponent = public_key["e"]

        # retrieves the private key values
        private_exponent = private_key["d"]
        prime_1 = private_key["p"]
        prime_2 = private_key["q"]

        # retrieves the extras values
        exponent_1 = extras["fe"]
        exponent_2 = extras["se"]
        coefficient  = extras["c"]

        # creates the ber structure
        ber_structure = self.format_ber_plugin.create_structure({})

        # creates the various integer values
        version_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : version}
        modulus_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : modulus}
        public_exponent_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : public_exponent}
        private_exponent_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : private_exponent}
        prime_1_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : prime_1}
        prime_2_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : prime_2}
        exponent_1_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : exponent_1}
        exponent_2_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : exponent_2}
        coefficient_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : coefficient}

        # creates the rsa private key contents (list)
        rsa_private_key_contents = [version_value, modulus_value, public_exponent_value, private_exponent_value, prime_1_value, prime_2_value, exponent_1_value, exponent_2_value, coefficient_value]

        # creates the rsa private key
        rsa_private_key = {TYPE_VALUE : {TYPE_CONSTRUCTED_VALUE : 1, TYPE_NUMBER_VALUE : SEQUENCE_TYPE, TYPE_CLASS_VALUE : 0}, VALUE_VALUE : rsa_private_key_contents}

        # packs the rsa private key
        rsa_private_key_packed = ber_structure.pack(rsa_private_key)

        # returns the rsa private key packed
        return rsa_private_key_packed

    def generate_public_key_der(self, keys):
        """
        Generates the a public key in der format, using
        the given keys value.

        @type keys: Tuple
        @param keys: A tuple containing the public, private
        and extra key values.
        @rtype: String
        @return: The generated public key in der format.
        """

        # unpacks the keys value
        public_key, _private_key, _extras = keys

        # retrieves the pubic key values
        modulus = public_key["n"]
        public_exponent = public_key["e"]

        # retrieves the rsa encryption object identifier
        rsa_encryption_object_identifier = OBJECT_IDENTIFIERS_TUPLES_MAP["rsa_encryption"]

        # creates the ber structure
        ber_structure = self.format_ber_plugin.create_structure({})

        # creates the various integer values
        modulus_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : modulus}
        public_exponent_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : public_exponent}

        # creates the rsa public key contents (list)
        rsa_public_key_contents = [modulus_value, public_exponent_value]

        # creates the rsa public key
        rsa_public_key = {TYPE_VALUE : {TYPE_CONSTRUCTED_VALUE : 1, TYPE_NUMBER_VALUE : SEQUENCE_TYPE, TYPE_CLASS_VALUE : 0}, VALUE_VALUE : rsa_public_key_contents}

        # packs the rsa public key
        rsa_public_key_packed = ber_structure.pack(rsa_public_key)

        # creates the algorithm identifier values
        algorithm_value = {TYPE_VALUE : OBJECT_IDENTIFIER_TYPE, VALUE_VALUE : rsa_encryption_object_identifier}
        arguments_value = {TYPE_VALUE : NULL_TYPE, VALUE_VALUE : None}

        # creates the algorithm identifier contents (list)
        algorithm_identifier_contents = [algorithm_value, arguments_value]

        # creates the algorithm identifier
        algorithm_identifier = {TYPE_VALUE : {TYPE_CONSTRUCTED_VALUE : 1, TYPE_NUMBER_VALUE : SEQUENCE_TYPE, TYPE_CLASS_VALUE : 0}, VALUE_VALUE : algorithm_identifier_contents}

        # creates the rsa public key packed but value
        rsa_public_key_packed_bit_value = {TYPE_VALUE : BIT_STRING_TYPE, VALUE_VALUE : rsa_public_key_packed}

        # creates the subject public key info contents (list)
        subject_plubic_key_info_contents = [algorithm_identifier, rsa_public_key_packed_bit_value]

        # creates the subject public key info
        subject_plubic_key_info = {TYPE_VALUE : {TYPE_CONSTRUCTED_VALUE : 1, TYPE_NUMBER_VALUE : SEQUENCE_TYPE, TYPE_CLASS_VALUE : 0}, VALUE_VALUE : subject_plubic_key_info_contents}

        # packs the subject public key info
        subject_plubic_key_info_packed = ber_structure.pack(subject_plubic_key_info)

        # returns the subject public key info
        return subject_plubic_key_info_packed

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
            # to the private key der encoded length
            if base_index >= string_value_length:
                # breaks the loop
                break

            # calculates the end index from the base index
            end_index = base_index + BASE_64_ENCODED_MAXIMUM_SIZE

            # retrieves the string value token
            string_value_token = string_value[base_index:end_index]

            # creates the string value from the string value token
            # and a newline character
            string_value_line = string_value_token + "\n"

            # adds the string value line to the string value list
            string_value_list.append(string_value_line)

            # sets the base index as the end index
            base_index = end_index

        # joins the string value list retrieving the
        # string value splitted
        string_value_splitted = "".join(string_value_list)

        # returns the string value splitted
        return string_value_splitted

    def load_private_key_der(self, private_key_der):
        # creates the ber structure
        ber_structure = self.format_ber_plugin.create_structure({})

        # unpacks the rsa private key
        rsa_private_key_unpacked = ber_structure.unpack(private_key_der)

        # retrieves the rsa private key value
        rsa_private_key_value = rsa_private_key_unpacked[VALUE_VALUE]

        # retrieves the version and the version value
        version = rsa_private_key_value[0]
        version_value = version[VALUE_VALUE]

        # retrieves the modulus and the modulus value
        modulus = rsa_private_key_value[1]
        modulus_value = modulus[VALUE_VALUE]

        # retrieves the public exponent and the public exponent value
        public_exponent = rsa_private_key_value[2]
        public_exponent_value = public_exponent[VALUE_VALUE]

        # retrieves the private exponent and the private exponent value
        private_exponent = rsa_private_key_value[3]
        private_exponent_value = private_exponent[VALUE_VALUE]

        # retrieves the prime 1 and the prime 1 value
        prime_1 = rsa_private_key_value[4]
        prime_1_value = prime_1[VALUE_VALUE]

        # retrieves the prime 2 and the prime 2 value
        prime_2 = rsa_private_key_value[5]
        prime_2_value = prime_2[VALUE_VALUE]

        # retrieves the exponent 1 and the exponent 1 value
        exponent_1 = rsa_private_key_value[6]
        exponent_1_value = exponent_1[VALUE_VALUE]

        # retrieves the exponent 2 and the exponent 2 value
        exponent_2 = rsa_private_key_value[7]
        exponent_2_value = exponent_2[VALUE_VALUE]

        # retrieves the coefficient and the coefficient value
        coefficient = rsa_private_key_value[8]
        coefficient_value = coefficient[VALUE_VALUE]

        # creates the public key map
        public_key = {"n" : modulus_value, "e" : public_exponent_value}

        # creates the private key map
        private_key = {"d" : private_exponent_value, "p" : prime_1_value, "q" : prime_2_value}

        # creates the extras map
        extras = {"fe" : exponent_1_value, "se" : exponent_2_value, "c" : coefficient_value}

        # creates the keys tuple
        keys = (public_key, private_key, extras)

        # creates the return tuple
        return_tuple = (keys, version_value)

        # returns the return tuple
        return return_tuple

    def load_public_key_der(self, private_key_der):
        # creates the ber structure
        ber_structure = self.format_ber_plugin.create_structure({})

        # unpacks the rsa public key
        rsa_public_key_unpacked = ber_structure.unpack(private_key_der)

        # retrieves the rsa public key value
        rsa_public_key_value = rsa_public_key_unpacked[VALUE_VALUE]

        # retrieves the algorithm identifier and the algorithm identifier value
        algorithm_identifier = rsa_public_key_value[0]
        algorithm_identifier_value = algorithm_identifier[VALUE_VALUE]

        # retrieves the algorithm and the algorithm value
        algorithm = algorithm_identifier_value[0]
        algorithm_value = algorithm[VALUE_VALUE]

        # retrieves the arguments and the arguments value
        arguments = algorithm_identifier_value[1]
        arguments_value = arguments[VALUE_VALUE]

        # retrieves the rsa public key packed bit value and the rsa public key packed bit value value
        rsa_public_key_packed_bit = rsa_public_key_value[1]
        rsa_public_key_packed_bit_value_value = rsa_public_key_packed_bit[VALUE_VALUE]

        # unpacks the rsa public key packed bit value value
        rsa_public_key = ber_structure.unpack(rsa_public_key_packed_bit_value_value)

        # retrieves the rsa public key value value
        rsa_public_key_value_value = rsa_public_key[VALUE_VALUE]

        # retrieves the modulus and the modulus value
        modulus = rsa_public_key_value_value[0]
        modulus_value = modulus[VALUE_VALUE]

        # retrieves the public exponent and the public exponent value
        public_exponent = rsa_public_key_value_value[1]
        public_exponent_value = public_exponent[VALUE_VALUE]

        # in case the object identifier is not rsa encryption
        if not algorithm_value == OBJECT_IDENTIFIERS_TUPLES_MAP["rsa_encryption"]:
            # raises the invalid format exception
            raise encryption_pkcs_1_exceptions.InvalidFormatException("invalid algorithm value: " + str(algorithm_value))

        # in case the arguments value is not none
        if not arguments_value == None:
            # raises the invalid format exception
            raise encryption_pkcs_1_exceptions.InvalidFormatException("invalid arguments value: " + str(arguments_value))

        # creates the public key map
        public_key = {"n" : modulus_value, "e" : public_exponent_value}

        # creates the private key map
        private_key = {}

        # creates the extras map
        extras = {}

        # creates the keys tuple
        keys = (private_key, public_key, extras)

        # returns the keys tuple
        return keys

    def _join_base_64(self, string_value):
        # removes the newline characters to obtain
        # the plain base 64 value
        string_value_joined = string_value.replace("\n", "")

        # returns the string value joined
        return string_value_joined

    def _write_file(self, file_path, string_value):
        """
        Writes the given string value to the file
        in the given file path.

        @type file_path: String
        @param file_path: The path to the file to write.
        @type string_value: String
        @param string_value: The string value to be written
        in the file.
        """

        # opens the file
        file = open(file_path, "wb")

        try:
            # writes the string value
            file.write(string_value)
        finally:
            # closes the file
            file.close()

    def _read_file(self, file_path):
        """
        Reads the contents of the file in the
        given file path.

        @type file_path: String
        @param file_path: The path to the file to read.
        @rtype: String
        @return: The string value read from the file.
        """

        # opens the file
        file = open(file_path, "rb")

        try:
            # reads the string value
            string_value = file.read()
        finally:
            # closes the file
            file.close()

        # returns the string value
        return string_value
