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
import zlib
import math
import types
import base64
import random
import cPickle

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
        # creates the rsa structure
        rsa_structure = RsaStructure()

        # returns the rsa structure
        return rsa_structure

class RsaStructure:
    """
    Class representing the rsa,
    cryptographic protocol structure.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def gcd(self, p, q):
        """
        Returns the greatest common divisor of p and q.

        >>> gcd(42, 6)
        6
        """

        if p < q:
            return self.gcd(q, p)

        if q == 0:
            return p

        return self.gcd(q, abs(p%q))

    def bytes2int(self, bytes):
        """
        Converts a list of bytes or a string to an integer.

        >>> (128*256 + 64)*256 + + 15
        8405007
        >>> l = [128, 64, 15]
        >>> bytes2int(l)
        8405007
        """

        if not (type(bytes) is types.ListType or type(bytes) is types.StringType):
            raise TypeError("You must pass a string or a list")

        # Convert byte stream to integer
        integer = 0
        for byte in bytes:
            integer *= 256
            if type(byte) is types.StringType: byte = ord(byte)
            integer += byte

        return integer

    def int2bytes(self, number):
        """
        Converts a number to a string of bytes

        >>> bytes2int(int2bytes(123456789))
        123456789
        """

        if not (type(number) is types.LongType or type(number) is types.IntType):
            raise TypeError("You must pass a long or an int")

        string = ""

        while number > 0:
            string = "%s%s" % (chr(number & 0xFF), string)
            number /= 256

        return string

    def fast_exponentiation(self, a, p, n):
        """
        Calculates r = a^p mod n
        """

        result = a % n
        remainders = []
        while p != 1:
            remainders.append(p & 1)
            p = p >> 1
        while remainders:
            rem = remainders.pop()
            result = ((a ** rem) * result ** 2) % n
        return result

    def read_random_int(self, nbits):
        """
        Reads a random integer of approximately nbits bits rounded up
        to whole bytes.
        """

        nbytes = self.ceil(nbits/8.)

        randomdata = os.urandom(nbytes)

        return self.bytes2int(randomdata)

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
        min_nbits = 32

        # The range of the random numbers we need to generate
        range = maxvalue - minvalue

        # Which is this number of bytes
        rangebytes = self.ceil(math.log(range, 2) / 8.)

        # Convert to bits, but make sure it's always at least min_nbits*2
        rangebits = max(rangebytes * 8, min_nbits * 2)

        # Take a random number of bits between min_nbits and rangebits
        nbits = random.randint(min_nbits, rangebits)

        return (self.read_random_int(nbits) % range) + minvalue

    def fermat_little_theorem(self, p):
        """
        Returns 1 if p may be prime, and something else if p definitely
        is not prime.
        """

        a = self.randint(1, p-1)

        return self.fast_exponentiation(a, p-1, p)

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
        f = self.fast_exponentiation(x, (n-1)/2, n)

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

        q = 0.5     # Property of the jacobi_witness function

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

        if self.randomized_primality_testing(number, 5):
            # prime, according to jacobi
            return True

        # returns false (not prime)
        return False

    def getprime(self, nbits):
        """
        Returns a prime number of max. "math.ceil(nbits/8)*8" bits. In
        other words: nbits is rounded up to whole bytes.

        >>> p = getprime(8)
        >>> is_prime(p-1)
        0
        >>> is_prime(p)
        1
        >>> is_prime(p+1)
        0
        """

        nbytes = int(math.ceil(nbits/8.))

        while True:
            integer = self.read_random_int(nbits)

            # Make sure it's odd
            integer |= 1

            # Test for primeness
            if self.is_prime(integer):
                break

            # Retry if not prime

        return integer

    def are_relatively_prime(self, a, b):
        """
        Returns True if a and b are relatively prime, and False if they
        are not.

        >>> are_relatively_prime(2, 3)
        1
        >>> are_relatively_prime(2, 4)
        0
        """

        d = self.gcd(a, b)

        return (d == 1)

    def find_p_q(self, nbits):
        """
        Returns a tuple of two different primes of nbits bits.
        """

        p = self.getprime(nbits)
        while True:
            q = self.getprime(nbits)
            if not q == p: break

        return (p, q)

    def extended_euclid_gcd(self, a, b):
        """
        Returns a tuple (d, i, j) such that d = gcd(a, b) = ia + jb.
        """

        if b == 0:
            return (a, 1, 0)

        q = abs(a % b)
        r = long(a / b)
        (d, k, l) = self.extended_euclid_gcd(b, q)

        return (d, l, k - l*r)

    # Main function: calculate encryption and decryption keys
    def calculate_keys(self, p, q, nbits):
        """
        Calculates an encryption and a decryption key for p and q, and
        returns them as a tuple (e, d).
        """

        n = p * q
        phi_n = (p-1) * (q-1)

        while True:
            # make sure e has enough bits so we ensure "wrapping" through
            # modulo n
            e = self.getprime(max(8, nbits / 2))
            if self.are_relatively_prime(e, n) and self.are_relatively_prime(e, phi_n):
                break

        (d, i, _j) = self.extended_euclid_gcd(e, phi_n)

        if not d == 1:
            raise Exception("e (%d) and phi_n (%d) are not relatively prime" % (e, phi_n))

        if not (e * i) % phi_n == 1:
            raise Exception("e (%d) and i (%d) are not mult. inv. modulo phi_n (%d)" % (e, i, phi_n))

        return (e, i)


    def gen_keys(self, nbits):
        """
        Generate RSA keys of nbits bits. Returns (p, q, e, d).
        Note: this can take a long time, depending on the key size.
        """

        while True:
            (p, q) = self.find_p_q(nbits)
            (e, d) = self.calculate_keys(p, q, nbits)

            # For some reason, d is sometimes negative. We don't know how
            # to fix it (yet), so we keep trying until everything is shiny
            if d > 0: break

        return (p, q, e, d)

    def gen_pubpriv_keys(self, number_bits):
        """
        Generates public and private keys, and returns them as (pub,
        priv).

        The public key consists of a dict {e: ..., , n: ....). The private
        key consists of a dict {d: ...., p: ...., q: ....).
        """

        # generates the keys for the given number
        # of bits
        p, q, e, d = self.gen_keys(number_bits)

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

        # creates the keys tuple
        keys_tuple = (public_key_map, private_key_map, extras_map)

        # returns the key tuple
        return keys_tuple

    def string_to_integer(self, string_value):
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

    def integer_to_string(self, integer_value):
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

        return self.fast_exponentiation(message, ekey, n)

    def decrypt_int(self, cyphertext, dkey, n):
        """
        Decrypts a cypher text using the decryption key "dkey", working
        modulo n.
        """

        return self.encrypt_int(cyphertext, dkey, n)

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

    def picklechops(self, chops):
        """
        Pickles and encodes it's argument in base 64 chops.
        """

        value = zlib.compress(cPickle.dumps(chops))
        encoded = base64.encodestring(value)

        return encoded.strip()

    def unpicklechops(self, string):
        """
        base64decodes and unpickes it's argument string into chops.
        """

        return cPickle.loads(zlib.decompress(base64.decodestring(string)))

    def chopstring(self, message, key, n, funcref):
        """
        Splits "message" into chops that are at most as long as n,
        converts these into integers, and calls funcref(integer, key, n)
        for each chop.

        Used by "encrypt" and "sign".
        """

        m = self.string_to_integer(message)

        c = self.encrypt_int(m, key, n)

        OB = self.integer_to_string(c)

        OB = base64.b64encode(OB)

        return OB

#        msglen = len(message)
#        mbits = msglen * 8
#        nbits = int(math.floor(math.log(n, 2)))
#        nbytes = nbits / 8
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

    def gluechops(self, chops, key, n, funcref):
        """
        Glues chops back together into a string.  calls
        funcref(integer, key, n) for each chop.

        Used by "decrypt" and "verify".
        """

        chops = base64.b64decode(chops)

        cypher_integer = self.string_to_integer(chops)

        m = self.encrypt_int(cypher_integer, key, n)

        EB = self.integer_to_string(m)

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

    def encrypt(self, message, key):
        """
        Encrypts a string "message" with the public key "key"
        """

        return self.chopstring(message, key["e"], key["n"], self.encrypt_int)

    def sign(self, message, key):
        """
        Signs a string "message" with the private key "key"
        """

        return self.chopstring(message, key["d"], key["p"] * key["q"], self.decrypt_int)

    def decrypt(self, cypher, key):
        """
        Decrypts a cypher with the private key "key"
        """

        return self.gluechops(cypher, key["d"], key["p"] * key["q"], self.decrypt_int)

    def verify(self, cypher, key):
        """
        Verifies a cypher with the public key "key"
        """

        return self.gluechops(cypher, key["e"], key["n"], self.encrypt_int)
