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

import colony

from . import exceptions


class RSATest(colony.Test):
    """
    The RSA infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (RSABaseTestCase,)

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

        system = self.plugin.system
        test_case.rsa = system.create_structure({})


class RSABaseTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "RSA Base test case"

    def test_generate_keys(self):
        for number_bits in (64, 128, 256):
            for _index in colony.legacy.xrange(16):
                self.rsa.generate_keys(number_bits)
                public_key, private_key, _extras = self.rsa.get_keys()

                # verifies that the modulus of the keys has exactly the
                # requested number of bits, never a smaller number of them
                modulus = private_key["p"] * private_key["q"]
                self.assertEqual(public_key["n"], modulus)
                self.assertEqual(modulus.bit_length(), number_bits)

                # verifies that both the signature and its verification
                # have the number of bytes of the modulus and that the
                # message is the one recovered by the verification
                signature = self.rsa.sign(b"Hello")
                self.assertEqual(len(signature), number_bits // 8)
                result = self.rsa.verify(signature)
                self.assertEqual(len(result), number_bits // 8)
                self.assertEqual(result.lstrip(b"\x00"), b"Hello")

        # verifies that the keys with the minimum number of bits are
        # generated, with a modulus of exactly that number of bits
        for _index in colony.legacy.xrange(16):
            self.rsa.generate_keys(10)
            public_key, _private_key, _extras = self.rsa.get_keys()
            self.assertEqual(public_key["n"].bit_length(), 10)

        # verifies that the keys whose modulus could not have the
        # requested number of bits are not generated, the ones with
        # an odd number of bits and the ones with not enough bits for
        # two distinct prime numbers, the current keys being kept
        keys = self.rsa.get_keys()
        for number_bits in (0, 2, 4, 6, 8, 9, 11, 65, 1023):
            self.assert_raises(
                exceptions.KeyGenerationError, self.rsa.generate_keys, number_bits
            )
            self.assertEqual(self.rsa.get_keys(), keys)

    def test__generate_p_q_values(self):
        for number_bits in (16, 32, 64, 128):
            for _index in colony.legacy.xrange(16):
                p_value, q_value = self.rsa._generate_p_q_values(number_bits)
                self.assertNotEqual(p_value, q_value)
                self.assertEqual(p_value.bit_length(), number_bits)
                self.assertEqual(q_value.bit_length(), number_bits)
                self.assertEqual((p_value * q_value).bit_length(), number_bits * 2)

    def test__generate_prime_number(self):
        for number_bits in (8, 12, 16, 50, 64, 128):
            for _index in colony.legacy.xrange(16):
                result = self.rsa._generate_prime_number(number_bits)

                # verifies that the number is odd and that it has exactly
                # the requested number of bits, with the two most significant
                # ones set, even when these are not a whole number of bytes
                self.assertEqual(result & 1, 1)
                self.assertEqual(result.bit_length(), number_bits)
                self.assertEqual(result >> (number_bits - 2), 3)

    def test__relatively_prime(self):
        result = self.rsa._relatively_prime(3, 1)
        self.assertEqual(result, True)

        result = self.rsa._relatively_prime(
            1303455847, 80677199572618450341522439921473626971
        )
        self.assertEqual(result, True)

        result = self.rsa._relatively_prime(
            130347, 80677199572618450341522439921472697123
        )
        self.assertEqual(result, False)

    def test__extended_euclid_greatest_common_divisor(self):
        result = self.rsa._extended_euclid_greatest_common_divisor(171, 10)
        self.assertEqual(result, (1, 1, -17))

        result = self.rsa._extended_euclid_greatest_common_divisor(418297, 225168)
        self.assertEqual(result, (1, -22391, 41596))

        result = self.rsa._extended_euclid_greatest_common_divisor(
            35713992551911994100259367902610573100, 1585944697
        )
        self.assertEqual(result, (1, -157708412, 3551446063785330185006617352461492633))

    def test__string_to_integer(self):
        result = self.rsa._string_to_integer("O\xe2\x9au\xe1")
        self.assertEqual(result, 343104189921)

        result = self.rsa._string_to_integer("\x18\x1e\xf2&\xbf\xec\xe0\x94")
        self.assertEqual(result, 1738092754454241428)

        result = self.rsa._string_to_integer("\xf0\x95\xabR\xde\x9b_\xd7")
        self.assertEqual(result, 17335950713042984919)

        result = self.rsa._string_to_integer(b"O\xe2\x9au\xe1")
        self.assertEqual(result, 343104189921)

        result = self.rsa._string_to_integer(b"\x18\x1e\xf2&\xbf\xec\xe0\x94")
        self.assertEqual(result, 1738092754454241428)

        result = self.rsa._string_to_integer(b"\xf0\x95\xabR\xde\x9b_\xd7")
        self.assertEqual(result, 17335950713042984919)

    def test__integer_to_string(self):
        result = self.rsa._integer_to_string(343104189921)
        self.assertEqual(result, b"O\xe2\x9au\xe1")

        result = self.rsa._integer_to_string(1738092754454241428)
        self.assertEqual(result, b"\x18\x1e\xf2&\xbf\xec\xe0\x94")

        result = self.rsa._integer_to_string(17335950713042984919)
        self.assertEqual(result, b"\xf0\x95\xabR\xde\x9b_\xd7")
