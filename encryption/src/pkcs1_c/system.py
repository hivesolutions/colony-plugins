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

import re
import math
import random
import string
import base64
import hashlib

import colony

from . import exceptions

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
""" The begin RSA private value """

END_RSA_PRIVATE_VALUE = "-----END RSA PRIVATE KEY-----"
""" The end RSA private value """

BEGIN_PUBLIC_VALUE = "-----BEGIN PUBLIC KEY-----"
""" The begin public value """

END_PUBLIC_VALUE = "-----END PUBLIC KEY-----"
""" The end public value """

PRIVATE_KEY_VALUE_REGEX = re.compile(
    BEGIN_RSA_PRIVATE_VALUE + "\n(?P<contents>.*)\n" + END_RSA_PRIVATE_VALUE, re.DOTALL
)
""" The private key value regex """

PUBLIC_KEY_VALUE_REGEX = re.compile(
    BEGIN_PUBLIC_VALUE + "\n(?P<contents>.*)\n" + END_PUBLIC_VALUE, re.DOTALL
)
""" The public key value regex """

BASE_64_ENCODED_MAXIMUM_SIZE = 64
""" The base 64 encoded maximum size """

INTEGER_TYPE = 0x02
""" The integer type """

BIT_STRING_TYPE = 0x03
""" The bit string type """

OCTET_STRING_TYPE = 0x04
""" The octet string type """

NULL_TYPE = 0x05
""" The null type """

OBJECT_IDENTIFIER_TYPE = 0x06
""" The object identifier type """

SEQUENCE_TYPE = 0x10
""" The sequence type """

OBJECT_IDENTIFIERS_TUPLES_MAP = {
    "pkcs1": (1, 2, 840, 113549, 1, 1),
    "rsa_encryption": (1, 2, 840, 113549, 1, 1, 1),
    "id_rsaes_oaep": (1, 2, 840, 113549, 1, 1, 7),
    "id_p_specified": (1, 2, 840, 113549, 1, 1, 9),
    "id_rsassa_pss": (1, 2, 840, 113549, 1, 1, 10),
    "md2_with_rsa_encryption": (1, 2, 840, 113549, 1, 1, 2),
    "md5_with_rsa_encryption": (1, 2, 840, 113549, 1, 1, 4),
    "sha1_with_rsa_encryption": (1, 2, 840, 113549, 1, 1, 5),
    "sha256_with_rsa_encryption": (1, 2, 840, 113549, 1, 1, 11),
    "sha384_with_rsa_encryption": (1, 2, 840, 113549, 1, 1, 12),
    "sha512_with_rsa_encryption": (1, 2, 840, 113549, 1, 1, 13),
}
""" The map associating the object identifiers with the tuples """

TUPLES_OBJECT_IDENTIFIERS_MAP = {
    (1, 2, 840, 113549, 1, 1): "pkcs1",
    (1, 2, 840, 113549, 1, 1, 1): "rsa_encryption",
    (1, 2, 840, 113549, 1, 1, 7): "id_rsaes_oaep",
    (1, 2, 840, 113549, 1, 1, 9): "id_p_specified",
    (1, 2, 840, 113549, 1, 1, 10): "id_rsassa_pss",
    (1, 2, 840, 113549, 1, 1, 2): "md2_with_rsa_encryption",
    (1, 2, 840, 113549, 1, 1, 4): "md5_with_rsa_encryption",
    (1, 2, 840, 113549, 1, 1, 5): "sha1_with_rsa_encryption",
    (1, 2, 840, 113549, 1, 1, 11): "sha256_with_rsa_encryption",
    (1, 2, 840, 113549, 1, 1, 12): "sha384_with_rsa_encryption",
    (1, 2, 840, 113549, 1, 1, 13): "sha512_with_rsa_encryption",
}
""" The map associating the tuples with the object identifiers """

HASH_OBJECT_IDENTIFIERS_TUPLES_MAP = {
    "md2": (1, 2, 840, 113549, 2, 2),
    "md5": (1, 2, 840, 113549, 2, 5),
    "sha1": (1, 3, 14, 3, 2, 26),
    "sha256": (2, 16, 840, 1, 101, 3, 4, 2, 1),
    "sha384": (2, 16, 840, 1, 101, 3, 4, 2, 2),
    "sha512": (2, 16, 840, 1, 101, 3, 4, 2, 3),
}
""" The map associating the hash object identifiers with the tuples """

TUPLES_HASH_OBJECT_IDENTIFIERS_MAP = {
    (1, 2, 840, 113549, 2, 2): "md2",
    (1, 2, 840, 113549, 2, 5): "md5",
    (1, 3, 14, 3, 2, 26): "sha1",
    (2, 16, 840, 1, 101, 3, 4, 2, 1): "sha256",
    (2, 16, 840, 1, 101, 3, 4, 2, 2): "sha384",
    (2, 16, 840, 1, 101, 3, 4, 2, 3): "sha512",
}
""" The map associating the tuples with the hash object identifiers """


class PKCS1(colony.System):
    """
    The PKCS1 class.
    """

    def create_structure(self, parameters):
        # retrieves the ber plugin and uses it to create the requested
        # PKCS1 structure that may be then be used for cryptographic
        # based operations on the provided buffers
        ber_plugin = self.plugin.ber_plugin
        pkcs1_structure = PKCS1Structure(ber_plugin)
        return pkcs1_structure


class PKCS1Structure:
    """
    Class representing the PKCS1,
    cryptographic standards structure.
    """

    ber_plugin = None
    """ the ber plugin """

    def __init__(self, ber_plugin):
        """
        Constructor of the class.

        :type ber_plugin: Plugin
        :param ber_plugin: The ber plugin.
        """

        self.ber_plugin = ber_plugin

    def generate_write_keys_pem(
        self, keys, private_key_file_path, public_key_file_path, version=1
    ):
        # generates the public and private key PEM values
        private_key_pem, public_key_pem = self.generate_keys_pem(keys, version)

        # converts both of the keys into a byte compatible stream
        # so that it's possible to properly write them to the files
        private_key_pem = colony.legacy.bytes(private_key_pem)
        public_key_pem = colony.legacy.bytes(public_key_pem)

        # writes the private and public key files
        self._write_file(private_key_file_path, private_key_pem)
        self._write_file(public_key_file_path, public_key_pem)

    def generate_keys_pem(self, keys, version=1):
        # generates the private key PEM
        private_key_pem = self.generate_private_key_pem(keys)

        # generates the public key PEM
        public_key_pem = self.generate_public_key_pem(keys)

        # creates a tuple with the private key and public key PEM
        keys_pem = (private_key_pem, public_key_pem)

        # returns the keys PEM
        return keys_pem

    def load_read_private_key_pem(self, private_key_file_path):
        # reads the file, retrieving the private key PEM
        # and constructs and loads the return tuple
        private_key_pem = self._read_file(private_key_file_path)
        private_key_pem = colony.legacy.str(private_key_pem)
        return_tuple = self.load_private_key_pem(private_key_pem)

        # returns the return tuple
        return return_tuple

    def load_read_public_key_pem(self, public_key_file_path):
        # reads the file, retrieving the public key PEM
        # and constructs and loads the keys tuple
        public_key_pem = self._read_file(public_key_file_path)
        public_key_pem = colony.legacy.str(public_key_pem)
        keys = self.load_public_key_pem(public_key_pem)

        # returns the keys tuple
        return keys

    def encrypt(self, keys, message):
        message_pad = self._encrypt(keys, message)
        return message_pad

    def decrypt(self, keys, message_pad):
        message = self._decrypt(keys, message_pad)
        return message

    def sign(self, keys, hash_algorithm_name, string_value):
        # ensures that the provided string value is encoded
        # as a byte based string (may be a void execution)
        string_value = colony.legacy.bytes(string_value)

        # creates a new hash using the given hash algorithm name
        # updates it with the provided string value and retrieves
        # the digest from it
        hash = hashlib.new(hash_algorithm_name)
        hash.update(string_value)
        digest_value = hash.digest()

        # signs the digest value retrieving the signature verified
        # (final signature) returning it to the caller method
        signature_verified = self._sign(keys, hash_algorithm_name, digest_value)
        return signature_verified

    def verify(self, signature_verified, string_value):
        # verifies the signature verified, retrieving
        # the hash algorithm name and the digest value
        # this is considered the unpack operation and
        # should be compliant with the PKCS1 specification
        hash_algorithm_name, digest_value = self._verify(signature_verified)

        # ensures that the provided string value is encoded
        # as a byte based string (may be a void execution)
        string_value = colony.legacy.bytes(string_value)

        # creates a new hash using the given hash algorithm name
        # updates it with the provided string value to be verified
        # and retrieves its digest
        hash = hashlib.new(hash_algorithm_name)
        hash.update(string_value)
        hash_digest = hash.digest()

        # verifies that the hash digest is the same
        # as the provided signature to be verified
        valid = hash_digest == digest_value
        return valid

    def generate_private_key_pem(self, keys, version=1):
        """
        Generates the a private key in PEM format, using
        the given keys value.

        :type keys: Tuple
        :param keys: A tuple containing the public, private
        and extra key values.
        :type version: int
        :param version: The version of the keys to be generated.
        :rtype: String
        :return: The generated private key in PEM format.
        """

        # retrieves the private key in DER format
        private_key_der = self.generate_private_key_der(keys, version)

        # encodes the private key DER in base 64
        private_key_der = colony.legacy.bytes(private_key_der)
        private_key_der_encoded = base64.b64encode(private_key_der)
        private_key_der_encoded = colony.legacy.str(private_key_der_encoded)

        # creates the string value list
        string_value_list = []

        # adds the begin RSA private value to the string value list
        string_value_list.append(BEGIN_RSA_PRIVATE_VALUE + "\n")

        # splits the private key DER encoded value
        private_key_der_splitted = self._split_base_64(private_key_der_encoded)

        # adds the private key DER splitted to the string value list
        string_value_list.append(private_key_der_splitted)

        # adds the end RSA private value to the string value list
        string_value_list.append(END_RSA_PRIVATE_VALUE + "\n")

        # joins the string value list retrieving the
        # private key PEM value
        private_key_pem = "".join(string_value_list)

        # returns the private key PEM value
        return private_key_pem

    def generate_public_key_pem(self, keys):
        """
        Generates the a public key in PEM format, using
        the given keys value.

        :type keys: Tuple
        :param keys: A tuple containing the public, private
        and extra key values.
        :rtype: String
        :return: The generated public key in PEM format.
        """

        # retrieves the public key in DER format
        public_key_der = self.generate_public_key_der(keys)

        # encodes the public key DER in base 64
        public_key_der = colony.legacy.bytes(public_key_der)
        public_key_der_encoded = base64.b64encode(public_key_der)
        public_key_der_encoded = colony.legacy.str(public_key_der_encoded)

        # creates the string value list
        string_value_list = []

        # adds the begin RSA public value to the string value list
        string_value_list.append(BEGIN_PUBLIC_VALUE + "\n")

        # splits the public key DER encoded value
        public_key_der_splitted = self._split_base_64(public_key_der_encoded)

        # adds the public key DER splitted to the string value list
        string_value_list.append(public_key_der_splitted)

        # adds the end RSA public value to the string value list
        string_value_list.append(END_PUBLIC_VALUE + "\n")

        # joins the string value list retrieving the
        # public key PEM value
        public_key_pem = "".join(string_value_list)

        # returns the public key PEM value
        return public_key_pem

    def load_private_key_pem(self, private_key_pem):
        # matches the public key header/footer token in case no match
        # is done raises an exception indicating the problem
        private_key_pem_match = PRIVATE_KEY_VALUE_REGEX.match(private_key_pem)
        if not private_key_pem_match:
            raise exceptions.InvalidFormatException(
                "private key header/footer not found"
            )

        # retrieves the private key PEM contents (avoid header and footer)
        # and joins the base 64 value back together removing extra newlines
        private_key_pem_contents = private_key_pem_match.group("contents")
        private_key_pem_contents_joined = self._join_base_64(private_key_pem_contents)

        # decodes the private key PEM from base 64, obtaining
        # private key DER in binary format, then loads it retrieving
        # the return tuple to be returned to the caller method
        private_key_pem_contents_joined = colony.legacy.bytes(
            private_key_pem_contents_joined
        )
        private_key_der = base64.b64decode(private_key_pem_contents_joined)
        private_key_der = colony.legacy.str(private_key_der)
        return_tuple = self.load_private_key_der(private_key_der)

        # returns the return tuple
        return return_tuple

    def load_public_key_pem(self, public_key_pem):
        # matches the public key header/footer token in case no match
        # is done raises an exception indicating the problem
        public_key_pem_match = PUBLIC_KEY_VALUE_REGEX.match(public_key_pem)
        if not public_key_pem_match:
            raise exceptions.InvalidFormatException(
                "public key header/footer not found"
            )

        # retrieves the public key PEM contents (avoid header and footer)
        # and joins the base 64 value back together removing extra newlines
        public_key_pem_match_contents = public_key_pem_match.group("contents")
        public_key_pem_match_contents_joined = self._join_base_64(
            public_key_pem_match_contents
        )

        # decodes the public key PEM from base 64, obtaining
        # public key DER in binary format the loads it retrieving
        # the keys tuple to be returned to the caller method
        public_key_pem_match_contents_joined = colony.legacy.bytes(
            public_key_pem_match_contents_joined
        )
        public_key_der = base64.b64decode(public_key_pem_match_contents_joined)
        public_key_der = colony.legacy.str(public_key_der)

        # loads the public key DER, retrieving the keys tuple
        keys = self.load_public_key_der(public_key_der)

        # returns the keys tuple
        return keys

    def generate_private_key_der(self, keys, version=1):
        """
        Generates the a private key in DER format, using
        the given keys value.

        :type keys: Tuple
        :param keys: A tuple containing the public, private
        and extra key values.
        :type version: int
        :param version: The version of the keys to be generated.
        :rtype: String
        :return: The generated private key in DER format.
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
        coefficient = extras["c"]

        # creates the ber structure
        ber_structure = self.ber_plugin.create_structure({})

        # creates the version value
        version_value = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE: version}

        # creates the modulus value
        modulus_value = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE: modulus}

        # creates the public exponent value
        public_exponent_value = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE: public_exponent}

        # creates the private exponent value
        private_exponent_value = {
            TYPE_VALUE: INTEGER_TYPE,
            VALUE_VALUE: private_exponent,
        }

        # creates the prime 1 value
        prime_1_value = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE: prime_1}

        # creates the prime 2 value
        prime_2_value = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE: prime_2}

        # creates the exponent 1 value
        exponent_1_value = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE: exponent_1}

        # creates the exponent 2 value
        exponent_2_value = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE: exponent_2}

        # creates the coefficient value
        coefficient_value = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE: coefficient}

        # creates the RSA private key contents (list)
        rsa_private_key_contents = [
            version_value,
            modulus_value,
            public_exponent_value,
            private_exponent_value,
            prime_1_value,
            prime_2_value,
            exponent_1_value,
            exponent_2_value,
            coefficient_value,
        ]

        # creates the RSA private key
        rsa_private_key = {
            TYPE_VALUE: {
                TYPE_CONSTRUCTED_VALUE: 1,
                TYPE_NUMBER_VALUE: SEQUENCE_TYPE,
                TYPE_CLASS_VALUE: 0,
            },
            VALUE_VALUE: rsa_private_key_contents,
        }

        # packs the RSA private key
        rsa_private_key_packed = ber_structure.pack(rsa_private_key)

        # returns the RSA private key packed
        return rsa_private_key_packed

    def generate_public_key_der(self, keys):
        """
        Generates the a public key in DER format, using
        the given keys value.

        :type keys: Tuple
        :param keys: A tuple containing the public, private
        and extra key values.
        :rtype: String
        :return: The generated public key in DER format.
        """

        # unpacks the keys value
        public_key, _private_key, _extras = keys

        # retrieves the public key values
        modulus = public_key["n"]
        public_exponent = public_key["e"]

        # retrieves the RSA encryption object identifier
        rsa_encryption_object_identifier = OBJECT_IDENTIFIERS_TUPLES_MAP[
            "rsa_encryption"
        ]

        # creates the ber structure
        ber_structure = self.ber_plugin.create_structure({})

        # creates the modulus value
        modulus_value = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE: modulus}

        # creates the public exponent value
        public_exponent_value = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE: public_exponent}

        # creates the RSA public key contents (list)
        rsa_public_key_contents = [modulus_value, public_exponent_value]

        # creates the RSA public key
        rsa_public_key = {
            TYPE_VALUE: {
                TYPE_CONSTRUCTED_VALUE: 1,
                TYPE_NUMBER_VALUE: SEQUENCE_TYPE,
                TYPE_CLASS_VALUE: 0,
            },
            VALUE_VALUE: rsa_public_key_contents,
        }

        # packs the RSA public key
        rsa_public_key_packed = ber_structure.pack(rsa_public_key)

        # creates the algorithm identifier value
        algorithm_value = {
            TYPE_VALUE: OBJECT_IDENTIFIER_TYPE,
            VALUE_VALUE: rsa_encryption_object_identifier,
        }

        # creates the algorithm identifier arguments value
        arguments_value = {TYPE_VALUE: NULL_TYPE, VALUE_VALUE: None}

        # creates the algorithm identifier contents (list)
        algorithm_identifier_contents = [algorithm_value, arguments_value]

        # creates the algorithm identifier
        algorithm_identifier = {
            TYPE_VALUE: {
                TYPE_CONSTRUCTED_VALUE: 1,
                TYPE_NUMBER_VALUE: SEQUENCE_TYPE,
                TYPE_CLASS_VALUE: 0,
            },
            VALUE_VALUE: algorithm_identifier_contents,
        }

        # creates the RSA public key packed but value
        rsa_public_key_packed_bit_value = {
            TYPE_VALUE: BIT_STRING_TYPE,
            VALUE_VALUE: rsa_public_key_packed,
        }

        # creates the subject public key info contents (list)
        subject_public_key_info_contents = [
            algorithm_identifier,
            rsa_public_key_packed_bit_value,
        ]

        # creates the subject public key info
        subject_public_key_info = {
            TYPE_VALUE: {
                TYPE_CONSTRUCTED_VALUE: 1,
                TYPE_NUMBER_VALUE: SEQUENCE_TYPE,
                TYPE_CLASS_VALUE: 0,
            },
            VALUE_VALUE: subject_public_key_info_contents,
        }

        # packs the subject public key info
        subject_public_key_info_packed = ber_structure.pack(subject_public_key_info)

        # returns the subject public key info
        return subject_public_key_info_packed

    def load_private_key_der(self, private_key_der):
        # creates the ber structure
        ber_structure = self.ber_plugin.create_structure({})

        # unpacks the RSA private key
        rsa_private_key_unpacked = ber_structure.unpack(private_key_der)

        # retrieves the RSA private key value
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
        public_key = {"n": modulus_value, "e": public_exponent_value}

        # creates the private key map
        private_key = {
            "d": private_exponent_value,
            "p": prime_1_value,
            "q": prime_2_value,
        }

        # creates the extras map
        extras = {
            "fe": exponent_1_value,
            "se": exponent_2_value,
            "c": coefficient_value,
        }

        # creates the keys tuple
        keys = (public_key, private_key, extras)

        # creates the return tuple
        return_tuple = (keys, version_value)

        # returns the return tuple
        return return_tuple

    def load_public_key_der(self, private_key_der):
        # creates the ber structure
        ber_structure = self.ber_plugin.create_structure({})

        # unpacks the RSA public key
        rsa_public_key_unpacked = ber_structure.unpack(private_key_der)

        # retrieves the RSA public key value
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

        # retrieves the RSA public key packed bit value and the RSA public key packed bit value value
        rsa_public_key_packed_bit = rsa_public_key_value[1]
        rsa_public_key_packed_bit_value_value = rsa_public_key_packed_bit[VALUE_VALUE]

        # unpacks the RSA public key packed bit value value
        rsa_public_key = ber_structure.unpack(rsa_public_key_packed_bit_value_value)

        # retrieves the RSA public key value value
        rsa_public_key_value_value = rsa_public_key[VALUE_VALUE]

        # retrieves the modulus and the modulus value
        modulus = rsa_public_key_value_value[0]
        modulus_value = modulus[VALUE_VALUE]

        # retrieves the public exponent and the public exponent value
        public_exponent = rsa_public_key_value_value[1]
        public_exponent_value = public_exponent[VALUE_VALUE]

        # in case the object identifier is not RSA encryption
        # raises an error as the RSA encryption is the only
        # supported encryption type
        if not algorithm_value == OBJECT_IDENTIFIERS_TUPLES_MAP["rsa_encryption"]:
            raise exceptions.InvalidFormatException(
                "invalid algorithm value: " + str(algorithm_value)
            )

        # in case the arguments value is not none must raise an exception
        # indicating the problem in the arguments
        if not arguments_value == None:
            raise exceptions.InvalidFormatException(
                "invalid arguments value: " + str(arguments_value)
            )

        # creates the public key map
        public_key = {"n": modulus_value, "e": public_exponent_value}

        # creates the private key map
        private_key = {}

        # creates the extras map
        extras = {}

        # creates the keys tuple
        keys = (public_key, private_key, extras)

        # returns the keys tuple
        return keys

    def _encrypt(self, keys, message):
        # unpacks the keys tuple, retrieving the public key,
        # private key and extras map and then retrieves the
        # modulus from the public key
        public_key, _private_key, _extras = keys
        modulus = public_key["n"]

        # calculates the size of the modulus in terms of bytes
        # this will be used as the size of the message (including
        # the padding)
        modulus_size_bytes = colony.ceil_integer(math.log(modulus, 256))

        # calculates the current size of the message and uses this
        # value to calculate the size of the pad
        message_length = len(message)
        pad_length = modulus_size_bytes - message_length - 3

        # creates the pad with the required size using just lower cased
        # characters to avoid the zero value and then constructs the final
        # padded message that includes the created padding
        pad = "".join(
            random.choice(string.ascii_lowercase)
            for _value in colony.legacy.xrange(pad_length)
        )
        message_pad = b"\x00\x02" + colony.legacy.bytes(pad) + b"\x00" + message
        return message_pad

    def _decrypt(self, keys, message_pad):
        # verifies if the provided message contains the "expected"
        # padding in case it does not returns the message (no padding)
        # is contained
        is_padded = message_pad.startswith(b"\x00\x02")
        if not is_padded:
            return message_pad

        # retrieves the remaining part of the message (excludes the
        # padding header) and tries to find the token indicating the
        # start of the message in case it's not found raises an exception
        # indicating the invalid padding
        message_pad = message_pad[2:]
        start_index = message_pad.find(b"\x00")
        if start_index == -1:
            raise exceptions.InvalidFormatException("invalid padding")

        # retrieve the message itself from the "discovered"
        # start index, this is the message without padding
        message = message_pad[start_index + 1 :]
        return message

    def _sign(self, keys, hash_algorithm_name, digest_value):
        # retrieves the hash algorithm tuple
        hash_algorithm_tuple = HASH_OBJECT_IDENTIFIERS_TUPLES_MAP[hash_algorithm_name]

        # creates the ber structure
        ber_structure = self.ber_plugin.create_structure({})

        # creates the algorithm value
        algorithm_value = {
            TYPE_VALUE: OBJECT_IDENTIFIER_TYPE,
            VALUE_VALUE: hash_algorithm_tuple,
        }

        # creates the argument value
        arguments_value = {TYPE_VALUE: NULL_TYPE, VALUE_VALUE: None}

        # creates the digest algorithm contents (list)
        digest_algorithm_contents = [algorithm_value, arguments_value]

        # creates the digest algorithm
        digest_algorithm = {
            TYPE_VALUE: {
                TYPE_CONSTRUCTED_VALUE: 1,
                TYPE_NUMBER_VALUE: SEQUENCE_TYPE,
                TYPE_CLASS_VALUE: 0,
            },
            VALUE_VALUE: digest_algorithm_contents,
        }

        # creates the digest value value
        digest_value_value = {TYPE_VALUE: OCTET_STRING_TYPE, VALUE_VALUE: digest_value}

        # creates the signature value contents (list)
        signature_value_contents = [digest_algorithm, digest_value_value]

        # creates the signature value
        signature_value = {
            TYPE_VALUE: {
                TYPE_CONSTRUCTED_VALUE: 1,
                TYPE_NUMBER_VALUE: SEQUENCE_TYPE,
                TYPE_CLASS_VALUE: 0,
            },
            VALUE_VALUE: signature_value_contents,
        }

        # packs the signature value
        signature_value_packed = ber_structure.pack(signature_value)

        # creates the signature buffer
        signature_buffer = colony.StringBuffer()

        # unpacks the keys tuple, retrieving the
        # public key, private key and extras map
        public_key, _private_key, _extras = keys

        # retrieves the modulus
        modulus = public_key["n"]

        # retrieves the signature value packed length
        signature_value_packed_length = len(signature_value_packed)

        # retrieves the modulus size in bytes
        modulus_size_bytes = colony.ceil_integer(math.log(modulus, 256))

        # calculates the padding size (from the modulus size bytes and the signature value packed length)
        padding_size = modulus_size_bytes - (signature_value_packed_length + 3)

        # writes the beginning of the padding value to the signature buffer
        signature_buffer.write(b"\x00")
        signature_buffer.write(b"\x01")

        # creates the padding string value
        padding = b"\xff" * padding_size

        # writes the padding to the signature buffer
        signature_buffer.write(padding)

        # writes the end of padding value to the signature buffer
        signature_buffer.write(b"\x00")

        # writes the signature value packed in the string buffer
        signature_buffer.write(signature_value_packed)

        # retrieves the signature verified from the string buffer
        signature_verified = signature_buffer.get_value()

        # returns the signature verified
        return signature_verified

    def _verify(self, signature_verified):
        # retrieves the first character and converts
        # it into and ordinal value
        first_character = signature_verified[0]
        first_character_ordinal = colony.legacy.ord(first_character)

        # retrieves the second character and converts
        # it into and ordinal value
        second_character = signature_verified[1]
        second_character_ordinal = colony.legacy.ord(second_character)

        # in case the first character ordinal is not zero or the second character is not one
        # must raise and invalid format exception
        if not first_character_ordinal == 0x00 or not second_character_ordinal == 0x01:
            raise exceptions.InvalidFormatException("invalid signature format")

        # creates the ber structure
        ber_structure = self.ber_plugin.create_structure({})

        # retrieves the signature verified length
        signature_verified_length = len(signature_verified)

        # iterates over the range of the signature verified length
        # starting in the one value
        for index in colony.legacy.xrange(1, signature_verified_length):
            # retrieves the current character
            current_character = signature_verified[index]

            # converts the current character to ordinal
            current_character_ordinal = colony.legacy.ord(current_character)

            # in case the current character ordinal is zero
            # (end of padding part) must break the loop
            if current_character_ordinal == 0x00:
                break

        # retrieves the signature value
        signature_value = signature_verified[index + 1 :]

        # unpacks the signature value
        signature_value_unpacked = ber_structure.unpack(signature_value)

        # retrieves the signature value value
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
        # note that this value is ensured to be bytes oriented
        digest = signature_value_value[1]
        digest_value = digest[VALUE_VALUE]
        digest_value = colony.legacy.bytes(digest_value)

        # in case the arguments value is not none
        # must raise an invalid format exception
        if not arguments_value == None:
            raise exceptions.InvalidFormatException(
                "invalid arguments value: " + str(arguments_value)
            )

        # retrieves the hash algorithm name
        hash_algorithm_name = TUPLES_HASH_OBJECT_IDENTIFIERS_MAP[algorithm_value]

        # creates the return tuple with the hash algorithm name
        # and the digest value, this is considered the verify result
        return_tuple = (hash_algorithm_name, digest_value)

        # returns the return value
        return return_tuple

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
            # to the private key DER encoded length the
            # string splitting has reached the end
            if base_index >= string_value_length:
                break

            # calculates the end index from the base index
            end_index = base_index + BASE_64_ENCODED_MAXIMUM_SIZE

            # retrieves the string value token
            string_value_token = string_value[base_index:end_index]

            # creates the string value from the string value token
            # and a newline character and adds it to the list of
            # string values to be joined
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

    def _write_file(self, file_path, string_value):
        """
        Writes the given string value to the file
        in the given file path.

        :type file_path: String
        :param file_path: The path to the file to write.
        :type string_value: String
        :param string_value: The string value to be written
        in the file.
        """

        # opens the file from the provided file path
        # this is going to be used to write the buffer
        file = open(file_path, "wb")

        # writes the string value to the file and then
        # closes the file to avoid any file structure
        # leaks (may create corruption)
        try:
            file.write(string_value)
        finally:
            file.close()

    def _read_file(self, file_path):
        """
        Reads the contents of the file in the
        given file path.

        :type file_path: String
        :param file_path: The path to the file to read.
        :rtype: String
        :return: The string value read from the file.
        """

        # opens the file using the provided file path,
        # note that the file is read in binary mode
        file = open(file_path, "rb")

        # reads the string value from the file and then
        # closes the file to avoid any file structure
        # leaks (may create corruption)
        try:
            string_value = file.read()
        finally:
            file.close()

        # returns the string value that was read from
        # the file, this should be byte buffer compliant
        return string_value
