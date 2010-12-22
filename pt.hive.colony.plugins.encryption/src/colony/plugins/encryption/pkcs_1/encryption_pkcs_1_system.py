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

import base64

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

BASE_64_ENCODED_MAXIMUM_SIZE = 64
""" The base 64 encoded maximum size """

INTEGER_TYPE = 0x02
""" The integer type """

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

    def generate_private_key_pem(self, keys):
        """
        Generates the a private key in pem format, using
        the given keys value.

        @type keys: Tuple
        @param keys: A tuple containing the public, private
        and extra key values.
        @rtype: String
        @return: The generated private key in pem format.
        """

        # retrieves the private key in der format
        private_key_der = self.generate_private_key_der(keys)

        # encodes the private key der in base 64
        private_key_der_encoded = base64.b64encode(private_key_der)

        # retrieves the private key der length
        private_key_der_encoded_length = len(private_key_der_encoded)

        # starts the base index
        base_index = 0

        # creates the list
        string_value_list = []

        # adds the begin rsa private value to the string value list
        string_value_list.append(BEGIN_RSA_PRIVATE_VALUE + "\n")

        # iterates continuously
        while True:
            # in case the base index is greater or equal
            # to the private key der encoded length
            if base_index >= private_key_der_encoded_length:
                # breaks the loop
                break

            # calculates the end index from the base index
            end_index = base_index + BASE_64_ENCODED_MAXIMUM_SIZE

            # retrieves the string value line
            string_value_line = private_key_der_encoded[base_index:end_index]

            # creates the string value from the string value line
            string_value = string_value_line + "\n"

            # adds the string value to the string value list
            string_value_list.append(string_value)

            # sets the base index as the end index
            base_index = end_index

        # adds the end rsa private value to the string value list
        string_value_list.append(END_RSA_PRIVATE_VALUE + "\n")

        # joins the string value list retrieving the
        # private key pem value
        private_key_pem = "".join(string_value_list)

        # returns the private key pem value
        return private_key_pem

    def generate_private_key_der(self, keys):
        """
        Generates the a private key in der format, using
        the given keys value.

        @type keys: Tuple
        @param keys: A tuple containing the public, private
        and extra key values.
        @rtype: String
        @return: The generated private key in der format.
        """

        # unpacks the keys value
        public_key, private_key, extras = keys

        # retrieves the pubic key values
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
        version_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : 0}
        modulus_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : modulus}
        public_exponent_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : public_exponent}
        private_exponent_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : private_exponent}
        prime_1_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : prime_1}
        prime_2_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : prime_2}
        exponent_1_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : exponent_1}
        exponent_2_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : exponent_2}
        coefficient_value = {TYPE_VALUE : INTEGER_TYPE, VALUE_VALUE : coefficient}

        # creates the rsa private key contents contents (list)
        rsa_private_key_contents = [version_value, modulus_value, public_exponent_value, private_exponent_value, prime_1_value, prime_2_value, exponent_1_value, exponent_2_value, coefficient_value]

        # creates the rsa private key
        rsa_private_key = {TYPE_VALUE : {TYPE_CONSTRUCTED_VALUE : 1, TYPE_NUMBER_VALUE : 16, TYPE_CLASS_VALUE : 0}, VALUE_VALUE : rsa_private_key_contents}

        # packs the rsa private key
        rsa_private_key_packed = ber_structure.pack(rsa_private_key)

        # returns the rsa private key packed
        return rsa_private_key_packed
