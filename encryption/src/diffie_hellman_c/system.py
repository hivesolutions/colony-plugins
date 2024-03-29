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


class DiffieHellman(colony.System):
    """
    The diffie hellman class, responsible for the management
    of the diffie hellman key exchange protocol.
    """

    def create_structure(self, parameters):
        # retrieves both the prime and the base values, in case
        # they are available and then uses them for the construction
        # of the diffie hellman structure, returning then the same
        # structure to the caller method
        prime_value = parameters.get("prime_value", None)
        base_value = parameters.get("base_value", None)
        diffie_hellman_structure = DiffieHellmanStructure(prime_value, base_value)
        return diffie_hellman_structure


class DiffieHellmanStructure(object):
    """
    Class representing the diffie hellman,
    cryptographic protocol structure.
    """

    a_value = None
    """ The "a" value """

    b_value = None
    """ The "b" value """

    A_value = None
    """ The "A" value """

    B_value = None
    """ The "B" value """

    p_value = None
    """ The "p" (prime number) value """

    g_value = None
    """ The "g" (base) value """

    def __init__(self, p_value=None, g_value=None):
        """
        Constructor of the class.

        :type p_value: int
        :param p_value: The "p" (prime number) value.
        :type g_value: int
        :param g_value: The "g" value.
        """

        self.p_value = p_value
        self.g_value = g_value

    def generate_A(self):
        """
        Generates the "A" value to be sent to the "second"
        party of the communication.

        :rtype: int
        :return: The generated "A" value.
        """

        return pow(self.g_value, self.a_value, self.p_value)

    def generate_B(self):
        """
        Generates the "B" value to be sent to the "first"
        party of the communication.

        :rtype: int
        :return: The generated "B" value.
        """

        return pow(self.g_value, self.b_value, self.p_value)

    def calculate_Ka(self):
        """
        Calculates the secret "K" value for the first party.

        :rtype: int
        :return: The calculated secret "K" value.
        """

        return pow(self.B_value, self.a_value, self.p_value)

    def calculate_Kb(self):
        """
        Calculates the secret "K" value for the second party.

        :rtype: int
        :return: The calculated secret "K" value.
        """

        return pow(self.A_value, self.b_value, self.p_value)

    def get_a_value(self):
        """
        Retrieves the "a" value.

        :rtype: int
        :return: The "a" value.
        """

        return self.a_value

    def set_a_value(self, a_value):
        """
        Sets the "a" value.

        :type a_value: int
        :param a_value: The "a" value.
        """

        self.a_value = a_value

    def get_b_value(self):
        """
        Retrieves the "b" value.

        :rtype: int
        :return: The "b" value.
        """

        return self.b_value

    def set_b_value(self, b_value):
        """
        Sets the "b" value.

        :type b_value: int
        :param b_value: The "b" value.
        """

        self.b_value = b_value

    def get_A_value(self):
        """
        Retrieves the "A" value.

        :rtype: int
        :return: The "A" value.
        """

        return self.A_value

    def set_A_value(self, A_value):
        """
        Sets the "A" value.

        :type A_value: int
        :param A_value: The "A" value.
        """

        self.A_value = A_value

    def get_B_value(self):
        """
        Retrieves the "B" value.

        :rtype: int
        :return: The "B" value.
        """

        return self.B_value

    def set_B_value(self, B_value):
        """
        Sets the "B" value.

        :type B_value: int
        :param B_value: The "B" value.
        """

        self.B_value = B_value

    def get_p_value(self):
        """
        Retrieves the "p" value.

        :rtype: int
        :return: The "p" value.
        """

        return self.p_value

    def set_p_value(self, p_value):
        """
        Sets the "p" value.

        :type p_value: int
        :param p_value: The "p" value.
        """

        self.p_value = p_value

    def get_g_value(self):
        """
        Retrieves the "g" value.

        :rtype: int
        :return: The "g" value.
        """

        return self.g_value

    def set_g_value(self, g_value):
        """
        Sets the "g" value.

        :type g_value: int
        :param g_value: The "g" value.
        """

        self.g_value = g_value
