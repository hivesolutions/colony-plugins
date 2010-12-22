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

    def greatest_common_divisor(self, p, q):
        """
        Returns the greatest common divisor of p and q.
        """

        if p < q:
            return self.greatest_common_divisor(q, p)

        if q == 0:
            return p

        return self.greatest_common_divisor(q, abs(p % q))

    def read_random_int(self, number_bits):
        """
        Reads a random integer of approximately number bits bits rounded up
        to whole bytes.
        """

        number_bytes = self.ceil(number_bits / 8)

        random_data = os.urandom(number_bytes)

        return self._string_to_integer(random_data)

    def ceil(self, x):
        """
        ceil(x) -> int(math.ceil(x))
        """

        return int(math.ceil(x))

    def randint(self, minvalue, maxvalue):
        """
        Returns a random integer x with minvalue <= x <= maxvalue
        """

        # safety - get a lot of random data even if the range is fairly
        # small
        min_number_bits = 32

        # The range of the random numbers we need to generate
        range = maxvalue - minvalue

        # Which is this number of bytes
        rangebytes = self.ceil(math.log(range, 2) / 8.)

        # Convert to bits, but make sure it's always at least min_number_bits*2
        rangebits = max(rangebytes * 8, min_number_bits * 2)

        # Take a random number of bits between min_number_bits and rangebits
        number_bits = random.randint(min_number_bits, rangebits)

        return (self.read_random_int(number_bits) % range) + minvalue

    def fermat_little_theorem(self, p):
        """
        Returns 1 if p may be prime, and something else if p definitely
        is not prime.
        """

        a = self.randint(1, p-1)

        return pow(a, p - 1, p)

    def jacobi(self, a, b):
        """
        Calculates the value of the Jacobi symbol (a / b).
        """

        if a % b == 0:
            return 0

        # sets the initial result
        result = 1

        while a > 1:
            if a & 1:
                if ((a-1)*(b-1) >> 2) & 1:
                    result = -result
                b, a = a, b % a
            else:
                if ((b ** 2 - 1) >> 3) & 1:
                    result = -result
                a = a >> 1

        # returns the result
        return result

    def jacobi_witness(self, x, n):
        """
        Returns False if n is an Euler pseudo-prime with base x, and
        True otherwise.
        """

        j = self.jacobi(x, n) % n
        f = pow(x, (n - 1) / 2, n)

        if j == f:
            return False
        else:
            return True

    def randomized_primality_testing(self, n, k):
        """
        Calculates whether n is composite (which is always correct) or
        prime (which is incorrect with error probability 2**-k)

        Returns False if the number if composite, and True if it's
        probably prime.
        """

        # Property of the jacobi_witness function
        q = 0.5

        # t = int(math.ceil(k / math.log(1/q, 2)))
        t = self.ceil(k / math.log(1 / q, 2))

        for _index in range(t + 1):
            x = self.randint(1, n-1)

            if self.jacobi_witness(x, n):
                return False

        return True

    def is_prime(self, number):
        """
        Returns True if the number is prime, and False otherwise.

        >>> is_prime(42)
        0
        >>> is_prime(41)
        1
        """

        """
        if not fermat_little_theorem(number) == 1:
            # Not prime, according to Fermat's little theorem
            return False
        """

        if not self.miller_rabin(number):
            return False

        if not self.fermat(number):
            return False

        if self.randomized_primality_testing(number, 5):
            # prime, according to jacobi
            return True

        # returns false (not prime)
        return False

    def miller_rabin(self, n, s = 50):
        for j in xrange(1, s + 1):
            a = random.randint(1, n - 1)
            if (self.test(a, n)):
                return False # n is complex
            return True # n is prime

    def toBinary(self, n):
        r = []
        while (n > 0):
            r.append(n % 2)
            n = n / 2
        return r

    def test(self, a, n):
        b = self.toBinary(n - 1)
        d = 1
        for i in xrange(len(b) - 1, -1, -1):
            x = d
            d = (d * d) % n
            if d == 1 and x != 1 and x != n - 1:
                return True # Complex
            if b[i] == 1:
                d = (d * a) % n
        if d != 1:
            return True # Complex
        return False # Prime

    def fermat(self, n, b = 2):
        """
        Test for primality based on Fermat's Little Theorem.

        returns 0 (condition false) if n is composite, -1 if
        base is not relatively prime
        """

        if self.greatest_common_divisor(n, b) > 1:
            return False
        else:
            return pow(b, n - 1, n) == 1

    def generate_prime_number(self, number_bits):
        """
        Returns a prime number of max. "math.ceil(number bits / 8) * 8" bits. In
        other words: number_bits is rounded up to whole bytes.
        """

        # iterates continuously
        while True:
            # generates a random number
            integer = self.read_random_int(number_bits)

            # make sure its odd
            integer |= 1

            # checks if it's prime
            if self.is_prime(integer):
                # breaks the loop
                break

        # returns the (generated) integer
        return integer

    def are_relatively_prime(self, a, b):
        """
        Returns True if a and b are relatively prime, and False if they
        are not.
        """

        d = self.greatest_common_divisor(a, b)

        return d == 1

    def find_p_q(self, number_bits):
        """
        Returns a tuple of two different primes of number bits bits.
        """

        p = self.generate_prime_number(number_bits)

        # iterates continuously
        while True:
            q = self.generate_prime_number(number_bits)

            if not q == p:
                break

        return (p, q)

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

    # Main function: calculate encryption and decryption keys
    def calculate_keys(self, p, q, number_bits):
        """
        Calculates an encryption and a decryption key for p and q, and
        returns them as a tuple (e, d).
        """

        n = p * q
        phi_n = (p-1) * (q-1)

        while True:
            # make sure e has enough bits so we ensure "wrapping" through
            # modulo n
            e = self.generate_prime_number(max(8, number_bits / 2))
            if self.are_relatively_prime(e, n) and self.are_relatively_prime(e, phi_n):
                break

        d, i, _j = self.extended_euclid_greatest_common_divisor(e, phi_n)

        if not d == 1:
            raise Exception("e (%d) and phi_n (%d) are not relatively prime" % (e, phi_n))

        if not (e * i) % phi_n == 1:
            raise Exception("e (%d) and i (%d) are not mult. inv. modulo phi_n (%d)" % (e, i, phi_n))

        return (e, i)

    def _generate_keys(self, number_bits):
        """
        Generate RSA keys of number_bits bits. Returns (p, q, e, d).
        Note: this can take a long time, depending on the key size.
        """

        while True:
            p, q = self.find_p_q(number_bits)
            e, d = self.calculate_keys(p, q, number_bits)

            # For some reason, d is sometimes negative. We don't know how
            # to fix it (yet), so we keep trying until everything is shiny
            if d > 0:
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

    def sign_int(self, message, dkey, n):
        """
        Signs "message" using key "dkey", working modulo n.
        """

        return self.decrypt_int(message, dkey, n)

    def verify_int(self, signed, ekey, n):
        """
        Verifies "signed" using key "ekey", working modulo n.
        """

        return self.encrypt_int(signed, ekey, n)

    def chopstring(self, message, key, n):
        """
        Splits "message" into chops that are at most as long as n,
        converts these into integers, and calls funcref(integer, key, n)
        for each chop.

        Used by "encrypt" and "sign".
        """

        m = self._string_to_integer(message)

        c = self.encrypt_int(m, key, n)

        OB = self._integer_to_string(c)

        OB = base64.b64encode(OB)

        return OB

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

    def gluechops(self, chops, key, n):
        """
        Glues chops back together into a string.  calls
        funcref(integer, key, n) for each chop.

        Used by "decrypt" and "verify".
        """

        chops = base64.b64decode(chops)

        cypher_integer = self._string_to_integer(chops)

        m = self.encrypt_int(cypher_integer, key, n)

        EB = self._integer_to_string(m)

        return EB

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

            # retrieves the character oringal value
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
