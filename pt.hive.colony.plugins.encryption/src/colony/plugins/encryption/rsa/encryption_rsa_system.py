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

import os
import math
import types
import base64
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

        @type encryption_ras_plugin: EncryptionRsaPlugin
        @param encryption_ras_plugin: The encryption rsa plugin.
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
        Generates public and private keys.

        @type number_bits: int
        @param number_bits: The number of bits to be
        used in the generated key.
        """

        # generates the keys for the given number
        # of bits
        p, q, e, d = self._generate_keys(number_bits)

        # calculates the modulus
        n = p * q

        # calculates the first exponent
        fe = d % (p - 1)

        # calculates the second exponent
        se = d % (q - 1)

        # calculates the coefficient
        c = (1 / q) % p

        # creates the public and private keys map
        public_key_map = {"n": n, "e": e}
        private_key_map = {"d": d, "p": p, "q": q}
        extras_map = {"fe": fe, "se": se, "c": c}

        # creates the keys (tuple)
        keys = (public_key_map, private_key_map, extras_map)

        # sets the keys (tuple) in the instance
        self.keys = keys

    def encrypt(self, message, public_key = None):
        """
        Encrypts a string "message" with the public key "key"
        """

        # retrieves the public key to be used
        public_key = public_key and public_key or self.keys[0]

        # retrieves the public key values
        modulus = public_key["n"]
        public_exponent = public_key["e"]

        return self.chopstring(message, public_exponent, modulus)

    def decrypt(self, message, private_key = None):
        """
        Decrypts a cypher with the private key "key"
        """

        # retrieves the key to be used
        private_key = private_key and private_key or self.keys[1]

        # retrieves the private key values
        private_exponent = private_key["d"]
        prime_1 = private_key["p"]
        prime_2 = private_key["q"]

        # calculates the modulus
        modulus = prime_1 * prime_2

        return self.gluechops(message, private_exponent, modulus)

    def sign(self, message, private_key = None):
        """
        Signs a string "message" with the private key "key"
        """

        # retrieves the key to be used
        private_key = private_key and private_key or self.keys[1]

        # retrieves the private key values
        private_exponent = private_key["d"]
        prime_1 = private_key["p"]
        prime_2 = private_key["q"]

        # calculates the modulus
        modulus = prime_1 * prime_2

        return self.chopstring(message, private_exponent, modulus)

    def verify(self, message, public_key = None):
        """
        Verifies a cypher with the public key "key"
        """

        # retrieves the public key to be used
        public_key = public_key and public_key or self.keys[0]

        # retrieves the public key values
        modulus = public_key["n"]
        public_exponent = public_key["e"]

        return self.gluechops(message, public_exponent, modulus)

    def is_prime(self, number):
        """
        Returns True if the number is prime, and False otherwise.
        """

        # in case the randomized primality testing fails
        if not self._randomized_primality_testing(number, 5):
            # return false (invalid)
            # according to jacobi
            return False

        # returns true (valid)
        return True

    def generate_prime_number(self, number_bits):
        """
        Returns a prime number of max. "math.ceil(number bits / 8) * 8" bits. In
        other words: number_bits is rounded up to whole bytes.
        """

        # iterates continuously
        while True:
            # generates a random number
            integer = self._generate_random_integer(number_bits)

            # make sure its odd
            integer |= 1

            # checks if it's prime
            if self.is_prime(integer):
                # breaks the loop
                break

        # returns the (generated) integer
        return integer

    def are_relatively_prime(self, first_value, second_value):
        """
        Returns True if a and b are relatively prime, and False if they
        are not.
        """

        # retrieves the greatest common divisor between the
        # two values
        divisor = colony.libs.math_util.greatest_common_divisor(first_value, second_value)

        # returns if the divisor is one (relatively prime)
        return divisor == 1

    def find_p_q(self, number_bits):
        """
        Returns a tuple of two different primes of number bits bits.
        """

        # generates a prime number to serve as p value
        p_value = self.generate_prime_number(number_bits)

        # iterates continuously
        while True:
            # generates a prime number to serve as q value
            q_value = self.generate_prime_number(number_bits)

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

    def extended_euclid_greatest_common_divisor(self, a, b):
        """
        Returns a tuple (d, i, j) such that d = greatest_common_divisor(a, b) = ia + jb.greatest_common_divisor
        """

        if b == 0:
            return (a, 1, 0)

        q = abs(a % b)
        r = long(a / b)

        d, k, l = self.extended_euclid_greatest_common_divisor(b, q)

        return (d, l, k - l * r)

    def calculate_keys(self, p, q, number_bits):
        """
        Calculates an encryption and a decryption key (exponent)
        for p and q, returning them as a tuple.
        """

        # calculates the modulus
        n = p * q

        # calculates the phi modulus
        phi_n = (p - 1) * (q - 1)

        # iterates continuously to find
        # a valid exponent
        while True:
            # make sure e has enough bits so we ensure "wrapping" through
            # modulus (n)
            e = self.generate_prime_number(max(8, number_bits / 2))

            # checks if the exponent and the modulus are relative primes
            # and also checks if the exponent and the phi modulus are relative
            # primes
            if self.are_relatively_prime(e, n) and self.are_relatively_prime(e, phi_n):
                # breaks the loop
                break

        # retrieves the result of the extended euclid greatest common divisor
        d, i, _j = self.extended_euclid_greatest_common_divisor(e, phi_n)

        # in case the greatest common divisor between both
        # is not one (not relative primes)
        if not d == 1:
            # raises the key generation error
            raise encryption_rsa_exceptions.KeyGenerationError("The exponent '%d' and the phi modulus '%d' are not relative primes" % (e, phi_n))

        # in case the test for multiplicative inverse
        # modulo fails
        if not (e * i) % phi_n == 1:
            # raises the key generation error
            raise encryption_rsa_exceptions.KeyGenerationError("The exponent '%d' and exponent '%d' are not multiplicative inverse modulo of phi modulus '%d'" % (e, i, phi_n))

        # creates a tuple with the keys
        keys_tuple = (e, i)

        # returns the keys tuple
        return keys_tuple

    def _generate_keys(self, number_bits):
        """
        Generate RSA keys of number_bits bits. Returns (p, q, e, d).
        Note: this can take a long time, depending on the key size.
        """

        # iterates continuously
        while True:
            p, q = self.find_p_q(number_bits)

            # calculates the keys (private and public) for
            # the given prime number and number of bits
            e, d = self.calculate_keys(p, q, number_bits)

            # For some reason, d is sometimes negative. We don't know how
            # to fix it (yet), so we keep trying until everything is shiny
            if d > 0:
                # breaks the loop
                break

        # creates a tuple with the generated keys
        generated_keys = (p, q, e, d)

        # returns the generated keys
        return generated_keys

    def encrypt_int(self, message, ekey, n):
        """
        Encrypts a message using encryption key 'ekey', working modulo n.
        """

        if type(message) is types.IntType:
            return self.encrypt_int(long(message), ekey, n)

        if not type(message) is types.LongType:
            raise TypeError("You must pass a long or an int")

        if message > 0 and math.floor(math.log(message, 2)) > math.floor(math.log(n, 2)):
            raise OverflowError("The message is too long")

        return pow(message, ekey, n)

    def chopstring(self, message, key, n_value):
        """
        Splits "message" into chops that are at most as long as n,
        converts these into integers, and calls funcref(integer, key, n)
        for each chop.

        Used by "encrypt" and "sign".
        """

        message_integer = self._string_to_integer(message)

        cypered_message_integer = self.encrypt_int(message_integer, key, n_value)

        cypered_message = self._integer_to_string(cypered_message_integer)

        cypered_message_encoded = base64.b64encode(cypered_message)

        return cypered_message_encoded

#        msglen = len(message)
#        mbits = msglen * 8
#        number_bits = int(math.floor(math.log(n, 2)))
#        nbytes = number_bits / 8
#        blocks = msglen / nbytes
#
#        if msglen % nbytes > 0:
#            blocks += 1
#
#        cypher = []
#
#        for bindex in range(blocks):
#            offset = bindex * nbytes
#            block = message[offset:offset+nbytes]
#            value = self.bytes2int(block)
#            cypher.append(funcref(value, key, n))
#
#        return self.picklechops(cypher)

    def gluechops(self, chops, key, n_value):
        """
        Glues chops back together into a string.  calls
        funcref(integer, key, n) for each chop.

        Used by "decrypt" and "verify".
        """

        chops = base64.b64decode(chops)

        cypher_integer = self._string_to_integer(chops)

        message_integer = self.encrypt_int(cypher_integer, key, n_value)

        message = self._integer_to_string(message_integer)

        return message

#        message = ""
#
#        chops = self.unpicklechops(chops)
#
#        for cpart in chops:
#            mpart = funcref(cpart, key, n)
#            message += self.int2bytes(mpart)
#
#        return message

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

    def _integer_to_string(self, integer_value):
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

        # reverses the characters list
        characters_list.reverse()

        # retrieves the string value from the list
        # of characters
        string_value = "".join(characters_list)

        # returns the string value
        return string_value

    def _generate_random_interval(self, minimum_value, maximum_value):
        """
        Returns a random integer x with minvalue <= x <= maxvalue
        """

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
        Reads a random integer of approximately number bits bits rounded up
        to whole bytes.
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

    def _randomized_primality_testing(self, number, k_value):
        """
        Calculates whether n is composite (which is always correct) or
        prime (which is incorrect with error probability 2**-k)

        Returns False if the number if composite, and True if it's
        probably prime.
        """

        # the property of the jacobi witness function
        q_value = 0.5

        # calculates t to ha
        t_value = colony.libs.math_util.ceil_integer(k_value / math.log(1 / q_value, 2))

        # iterates over the range of t value plus one
        for _index in range(t_value + 1):
            # generates a random number in the interval
            random_number = self._generate_random_interval(1, number - 1)

            # in case the random number is a jacobi witness
            # then the number is not prime
            if self._jacobi_witness(random_number, number):
                # returns false (invalid)
                return False

        # returns true (valid)
        return True

    def _jacobi_witness(self, x_value, n_value):
        """
        Returns False if n is an Euler pseudo-prime with base x, and
        True otherwise.
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
        Calculates the value of the Jacobi symbol (a / b).
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
