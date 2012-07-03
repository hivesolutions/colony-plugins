#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import os
import math
import types
import random

import colony.libs.math_util

import encryption_rsa_exceptions

class EncryptionRsa:
    """
    The encryption rsa class.
    """

    encryption_rsa_plugin = None
    """ The encryption rsa plugin """

    def __init__(self, encryption_rsa_plugin):
        """
        Constructor of the class.

        @type encryption_rsa_plugin: EncryptionRsaPlugin
        @param encryption_rsa_plugin: The encryption rsa plugin.
        """

        self.encryption_rsa_plugin = encryption_rsa_plugin

    def create_structure(self, parameters):
        # retrieves the keys (if available)
        keys = parameters.get("keys", None)

        # creates the rsa structure
        rsa_structure = RsaStructure(keys)

        # returns the rsa structure
        return rsa_structure

class RsaStructure:
    """
    Class representing the rsa,
    cryptographic protocol structure.
    """

    keys = None
    """ Tuple containing the public, private and extra keys """

    def __init__(self, keys):
        """
        Constructor of the class.

        @type keys: Tuple
        @param keys: Tuple containing the public, private and extra keys.
        """

        self.keys = keys

    def generate_keys(self, number_bits):
        """
        Generates public, private and extra keys, using
        the given number of bits to generate the keys

        @type number_bits: int
        @param number_bits: The number of bits to be
        used in the generated keys.
        @rtype: Tuple
        @return: A tuple containing the public, private
        and extra keys.
        """

        # generates the keys for the given number
        # of bits
        p_value, q_value, e_value, d_value = self._generate_keys(number_bits)

        # calculates the modulus
        n_value = p_value * q_value

        # calculates the first exponent
        fe_value = d_value % (p_value - 1)

        # calculates the second exponent
        se_value = d_value % (q_value - 1)

        # calculates the coefficient
        c_value = (1 / q_value) % p_value

        # creates the public key map
        public_key_map = {
            "n" : n_value,
            "e" : e_value
        }

        # creates the private key map
        private_key_map = {
            "d" : d_value,
            "p" : p_value,
            "q" : q_value
        }

        # creates the extra map
        extra_map = {
            "fe" : fe_value,
            "se" : se_value,
            "c" : c_value
        }

        # creates the keys (tuple)
        keys = (
            public_key_map,
            private_key_map,
            extra_map
        )

        # sets the keys (tuple) in the instance
        self.keys = keys

    def encrypt(self, message, public_key = None):
        """
        Encrypts the given message using the given public key.

        @type message: String
        @param message: The message to be encrypted.
        @type public_key: Dictionary
        @param public_key: The map containing the public key.
        @rtype: String
        @return: The encrypted message (cypher).
        """

        # retrieves the public key to be used
        public_key = public_key and public_key or self.keys[0]

        # retrieves the public key values
        modulus = public_key["n"]
        public_exponent = public_key["e"]

        return self._encrypt_buffer(message, public_exponent, modulus)

    def decrypt(self, encrypted_message, private_key = None):
        """
        Decrypts the given message using the given private key.

        @type encrypted_message: String
        @param encrypted_message: The encrypted message (cyper) to
        be decrypted.
        @type private_key: Dictionary
        @param private_key: The map containing the private key.
        @rtype: String
        @return: The decrypted message.
        """

        # retrieves the key to be used
        private_key = private_key and private_key or self.keys[1]

        # retrieves the private key values
        private_exponent = private_key["d"]
        prime_1 = private_key["p"]
        prime_2 = private_key["q"]

        # calculates the modulus
        modulus = prime_1 * prime_2

        return self._decrypt_buffer(encrypted_message, private_exponent, modulus)

    def sign(self, message, private_key = None):
        """
        Signs the given message using the given private key.

        @type message: String
        @param message: The encrypted message (cyper) to
        be signed.
        @type private_key: Dictionary
        @param private_key: The map containing the private key.
        @rtype: String
        @return: The signed message.
        """

        # retrieves the key to be used
        private_key = private_key and private_key or self.keys[1]

        # retrieves the private key values
        private_exponent = private_key["d"]
        prime_1 = private_key["p"]
        prime_2 = private_key["q"]

        # calculates the modulus
        modulus = prime_1 * prime_2

        return self._encrypt_string(message, private_exponent, modulus)

    def verify(self, signed_message, public_key = None):
        """
        Verifies the given signed message using the given public key.

        @type signed_message: String
        @param signed_message: The signed message to be verified.
        @type public_key: Dictionary
        @param public_key: The map containing the public key.
        @rtype: String
        @return: The (original) message.
        """

        # retrieves the public key to be used
        public_key = public_key and public_key or self.keys[0]

        # retrieves the public key values
        modulus = public_key["n"]
        public_exponent = public_key["e"]

        return self._encrypt_string(signed_message, public_exponent, modulus)

    def get_keys(self):
        """
        Returns the keys.

        @rtype: Dictionary
        @return: The keys.
        """

        return self.keys

    def set_keys(self, keys):
        """
        Sets the keys.

        @type keys: Dictionary
        @param keys: The keys.
        """

        self.keys = keys

    def _encrypt_buffer(self, message, key, modulus):
        # retrieves the modulus number of bits
        modulus_number_bits = math.log(modulus, 2)

        # converts the modulus number of bits to integer
        modulus_number_bits_integer = int(modulus_number_bits)

        # converts the modulus number of bits to bytes
        modulus_number_bytes = modulus_number_bits_integer / 8

        # retrieves the message length
        message_length = len(message)

        # calculates the message block count (number of message blocks)
        message_block_count = message_length / modulus_number_bytes

        # in case the modulus of the message length
        # and the modulus number bytes is greater than zero
        if message_length % modulus_number_bytes > 0:
            # increments the message block count
            message_block_count += 1

        # creates the block values list
        block_values = []

        # iterate over the range of message block count
        for index in range(message_block_count):
            # calculates the offset value
            offset = index * modulus_number_bytes

            # retrieves the current block value
            current_block_value = message[offset:offset + modulus_number_bytes]

            # encrypts the current block value
            current_block_value_encrypted = self._encrypt_string(current_block_value, key, modulus)

            # adds the encrypted current block value to the block values (list)
            block_values.append(current_block_value_encrypted)

        # returns the block values list
        return block_values

    def _decrypt_buffer(self, message_values_list, key, modulus):
        # creates the part value list
        part_values = []

        # iterates over all the message values list
        for message_value in message_values_list:
            # decrypts the message value, retrieving
            # the current part value
            current_part_value = self._encrypt_string(message_value, key, modulus)

            # adds the current part value to the part values (list)
            part_values.append(current_part_value)

        # joins the parts in the part values list
        # to re-create the message decrypted
        message_decrypted = "".join(part_values)

        # returns the message decrypted
        return message_decrypted

    def _encrypt_string(self, message, key, modulus):
        # retrieves the modulus size in bytes
        modulus_size_bytes = colony.libs.math_util.ceil_integer(math.log(modulus, 256))

        # converts the message to integer
        message_integer = self._string_to_integer(message)

        # encrypts the message integer value with the given key and modulus
        message_integer_encrypted = self._encrypt_integer(message_integer, key, modulus)

        # converts the integer to string, retrieving the message encrypted
        message_encrypted = self._integer_to_string(message_integer_encrypted, modulus_size_bytes)

        # returns the message encrypted
        return message_encrypted

    def _encrypt_integer(self, message, e_value, n_value):
        """
        Encrypts a message (integer mode) using the given exponent
        and modulus values.

        @type message: int
        @param message: The message represented as an integer.
        @type e_value: int
        @param e_value: The exponent to be used.
        @type n_value: int
        @param n_value: The modulus value.
        @rtype: int
        @return: The encrypted message as an integer.
        """

        if type(message) is types.IntType:
            return self._encrypt_integer(long(message), e_value, n_value)

        if not type(message) is types.LongType:
            # raises a type error
            raise TypeError("you must pass a long or an int")

        if message > 0 and math.floor(math.log(message, 2)) > math.floor(math.log(n_value, 2)):
            # raises an overflow error
            raise OverflowError("the message is too long")

        return pow(message, e_value, n_value)

    def _generate_keys(self, number_bits):
        """
        Generates the rsa keys with the given number
        of bits.
        This method is cpu intensive.

        @type number_bits: int
        @param number_bits: The number of bits to be used
        in the keys generation.
        @rtype: Tuple
        @return: A tuple containing the various rsa keys.
        """

        # iterates continuously
        while True:
            # generates the p and q values for the defined
            # number of bits
            p_value, q_value = self._generate_p_q_values(number_bits)

            # calculates the exponents (private and public) for
            # the given prime number and number of bits
            e_value, d_value = self._generate_exponents(p_value, q_value, number_bits)

            # tests if the number is positive
            if d_value > 0:
                # breaks the loop
                break

        # creates a tuple with the generated keys
        generated_keys = (
            p_value,
            q_value,
            e_value,
            d_value
        )

        # returns the generated keys
        return generated_keys

    def _generate_exponents(self, p_value, q_value, number_bits):
        """
        Generates the exponents, using the given p and q prime values
        according to the given number of bits.

        @type p_value: int
        @param p_value: The p prime value.
        @type q_value: int
        @param q_value: The q prime value.
        @type number_bits: int
        @param number_bits: The number of bits for the key.
        @rtype: Tuple
        @return: A Tuple containing the exponents.
        """

        # calculates the modulus
        n_value = p_value * q_value

        # calculates the phi modulus
        phi_n_value = (p_value - 1) * (q_value - 1)

        # iterates continuously to find
        # a valid exponent
        while True:
            # make sure e has enough bits so we ensure "wrapping" through
            # modulus (n value)
            e_value = self._generate_prime_number(max(8, number_bits / 2))

            # checks if the exponent and the modulus are relative primes
            # and also checks if the exponent and the phi modulus are relative
            # primes
            if self._relatively_prime(e_value, n_value) and self._relatively_prime(e_value, phi_n_value):
                # breaks the loop
                break

        # retrieves the result of the extended euclid greatest common divisor
        d_value, i_value, _j_value = self._extended_euclid_greatest_common_divisor(e_value, phi_n_value)

        # in case the greatest common divisor between both
        # is not one (not relative primes)
        if not d_value == 1:
            # raises the key generation error
            raise encryption_rsa_exceptions.KeyGenerationError("The public exponent '%d' and the phi modulus '%d' are not relative primes" % (e_value, phi_n_value))

        # in case the test for multiplicative inverse
        # modulo fails
        if not (e_value * i_value) % phi_n_value == 1:
            # raises the key generation error
            raise encryption_rsa_exceptions.KeyGenerationError("The public exponent '%d' and private exponent '%d' are not multiplicative inverse modulo of phi modulus '%d'" % (e_value, i_value, phi_n_value))

        # creates a tuple with the keys
        keys_tuple = (
            e_value,
            i_value
        )

        # returns the keys tuple
        return keys_tuple

    def _generate_p_q_values(self, number_bits):
        """
        Generates two different prime numbers (p and q values)
        and returns them in a tuple.
        The generation is made according to the number
        of bits defined

        @type number_bits: int
        @param number_bits: The number of bits to be used in
        prime generation.
        @rtype: Tuple
        @return: A tuple containing the two different prime
        numbers
        """

        # generates a prime number to serve as p value
        p_value = self._generate_prime_number(number_bits)

        # iterates continuously
        while True:
            # generates a prime number to serve as q value
            q_value = self._generate_prime_number(number_bits)

            # in case the q value and the p
            # value are different
            if not q_value == p_value:
                # breaks the loop
                break

        # creates a tuple with the generated
        # prime numbers
        prime_tuple = (p_value, q_value)

        # returns the prime tuple
        return prime_tuple

    def _generate_prime_number(self, number_bits):
        """
        Generates a prime number with the given number of bits
        in length.

        @type number_bits: int
        @param number_bits: The number of bits to be used in
        the prime number generation.
        @rtype: int
        @return: The generated prime number.
        """

        # iterates continuously
        while True:
            # generates a random number
            integer = self._generate_random_integer(number_bits)

            # make sure its odd
            integer |= 1

            # checks if it's prime
            if self._is_prime(integer):
                # breaks the loop
                break

        # returns the (generated) integer
        return integer

    def _is_prime(self, number):
        """
        Tests if the given number is a prime number.

        @type number: int
        @param number: The number to be tested as prime.
        @rtype: bool
        @return: The result of the test.
        """

        # in case the randomized primality testing fails
        if not self._randomized_primality_testing(number, 5):
            # return false (invalid)
            # according to jacobi
            return False

        # returns true (valid)
        return True

    def _randomized_primality_testing(self, number, k_value):
        # the property of the jacobi witness function
        q_value = 0.5

        # calculates t to ha
        t_value = colony.libs.math_util.ceil_integer(k_value / math.log(1 / q_value, 2))

        # iterates over the range of t value plus one
        for _index in range(t_value + 1):
            # generates a random number in the interval
            random_number = self._generate_random_integer_interval(1, number - 1)

            # in case the random number is a jacobi witness
            # then the number is not prime
            if self._jacobi_witness(random_number, number):
                # returns false (invalid)
                return False

        # returns true (valid)
        return True

    def _jacobi_witness(self, x_value, n_value):
        """
        Checks if the given x value is witness to n value
        non primality.
        This check is made according to euler's theorem.

        @type x_value: int
        @param x_value: The value to be checked for witness.
        @type n_value: int
        @param n_value: The value to be checked for primality.
        @rtype: bool
        @return: The result of the checking.
        """

        # calculates the j value from jacobi
        j_value = self._jacobi(x_value, n_value) % n_value

        # calculates the f value
        f_value = pow(x_value, (n_value - 1) / 2, n_value)

        # in case the j value and the f value
        # are the same
        if j_value == f_value:
            # returns false (not witness)
            return False
        # otherwise
        else:
            # returns true (witness)
            return True

    def _jacobi(self, a_value, b_value):
        """
        Calculates the value of the jacobi symbol, using the
        given a and b values.

        @type a_value: int
        @param a_value: The a value.
        @type b_value: int
        @param b_value: The b value.
        @rtype: int
        @return: The calculated jacobi symbol.
        """

        # in case the modulus of the a value
        # with the b value is zero
        if a_value % b_value == 0:
            # returns zero
            return 0

        # sets the initial result
        result = 1

        # iterates while the a value
        # is greater than zero
        while a_value > 1:
            # in case the a value is odd
            if a_value & 1:
                if ((a_value - 1) * (b_value - 1) >> 2) & 1:
                    # inverts the result
                    result = -result

                b_value, a_value = a_value, b_value % a_value
            # otherwise it must be even
            else:
                if ((b_value ** 2 - 1) >> 3) & 1:
                    # inverts the result
                    result = -result

                # shifts the a value one bit to the right
                a_value >>= 1

        # returns the result
        return result

    def _relatively_prime(self, first_value, second_value):
        """
        Tests if the given values are relative primes
        to each other.

        @type first_value: int
        @param first_value: The first value to be tested.
        @type second_value: int
        @param second_value: The second value to be tested.
        @rtype: bool
        @return: The result of the relative prime test.
        """

        # retrieves the greatest common divisor between the
        # two values
        divisor = colony.libs.math_util.greatest_common_divisor(first_value, second_value)

        # returns if the divisor is one (relatively prime)
        return divisor == 1

    def _extended_euclid_greatest_common_divisor(self, a_value, b_value):
        # in case the b value is zero
        if b_value == 0:
            # creates a simple common divisor tuple
            common_divisor_tuple = (
                a_value,
                1,
                0
            )

            # returns the common divisor tuple
            return common_divisor_tuple

        # calculates the q value
        q_value = abs(a_value % b_value)

        # calculates the r value
        r_value = long(a_value / b_value)

        # retrieves the extended euclid greatest common divisor for b value and q value
        d_value, k_value, l_value = self._extended_euclid_greatest_common_divisor(b_value, q_value)

        # creates the common divisor tuple
        common_divisor_tuple = (
            d_value,
            l_value,
            k_value - l_value * r_value
        )

        # returns the common divisor tuple
        return common_divisor_tuple

    def _string_to_integer(self, string_value):
        # starts the integer value
        integer_value = 0

        # sets the is first flag
        is_first = True

        # iterates over all the character values
        for character_value in string_value:
            # in case the is first flag is set
            if is_first:
                # unsets the is first flag
                is_first = False
            # otherwise
            else:
                # shift the integer value eight bits
                # to the left
                integer_value <<= 8

            # retrieves the character original value
            character_ordinal_value = ord(character_value)

            # increments the integer value with
            # the character ordinal value
            integer_value += character_ordinal_value

        # returns the integer value
        return integer_value

    def _integer_to_string(self, integer_value, string_length = None):
        # creates the characters list that will hold
        # the various characters
        characters_list = []

        # iterates over all the character values
        while integer_value > 0:
            # retrieves the character value for
            # the least significant byte value of
            # the integer
            character_value = chr(integer_value & 0xff)

            # adds the character value to the character list
            characters_list.append(character_value)

            # shifts the integer value eight bits
            # to the right
            integer_value >>= 8

        # retrieves the characters list length
        characters_list_length = len(characters_list)

        # in case the string length is defined
        if string_length:
            # calculates the extra characters length from the string length
            extra_characters_length = string_length - characters_list_length

            # iterates over the range of extra characters length
            for _index in range(extra_characters_length):
                # adds the extra padding character
                characters_list.append("\x00")

        # reverses the characters list
        characters_list.reverse()

        # retrieves the string value from the list
        # of characters
        string_value = "".join(characters_list)

        # returns the string value
        return string_value

    def _generate_random_integer_interval(self, minimum_value, maximum_value):
        # sets the default minimum number of bits, even if the
        # range is too small
        minimum_number_bits = 32

        # calculates the range of the random numbers
        # to generate
        range = maximum_value - minimum_value

        # converts the range into bits
        range_bits = math.log(range, 2)

        # converts the range into bytes
        range_bytes = colony.libs.math_util.ceil_integer(range_bits / 8.0)

        # converts the range into bits, but verifies that there
        # is at least a minimum number of bits
        range_bits = max(range_bytes * 8, minimum_number_bits * 2)

        # generates the random number of bits to be used
        number_bits = random.randint(minimum_number_bits, range_bits)

        # generates the random integer with the number of bits generated
        # and applying modulo of the range
        random_base_value = self._generate_random_integer(number_bits) % range

        # creates the random value adding the minimum value to the
        # random base value
        random_value = random_base_value + minimum_value

        # returns the random value
        return random_value

    def _generate_random_integer(self, number_bits):
        """
        Generates a random integer of approximately the
        size of the provided number bits bits rounded up
        to whole bytes.

        @type number_bits: int
        @param number_bits: The number of bits of the generated
        random integer.
        @rtype: int
        @return: The generated random integer.
        """

        # calculates the number of bytes to represent the number
        number_bytes = colony.libs.math_util.ceil_integer(number_bits / 8.0)

        # generates a random data string with the specified
        # number of bytes in length
        random_data = os.urandom(number_bytes)

        # converts the random data to integer
        random_integer = self._string_to_integer(random_data)

        # returns the random integer
        return random_integer
