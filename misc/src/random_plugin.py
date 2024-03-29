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


class RandomPlugin(colony.Plugin):
    """
    The main class for the Random plugin.
    """

    id = "pt.hive.colony.plugins.misc.random"
    name = "Random"
    description = "A plugin to generate random numbers"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT, colony.JYTHON_ENVIRONMENT]
    capabilities = ["random"]
    main_modules = ["random_c"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import random_c

        self.system = random_c.Random(self)

    def generate_random(self):
        """
        Generates a random string for cryptographic
        usage (because of its entropy).
        The string is creating using a random number generator,
        the current process id, thread id, the current time
        and a secret key.

        :rtype: String
        :return: The generated random string for cryptographic
        usage (with high entropy).
        """

        return self.system.generate_random()

    def generate_random_int(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an integer.

        :rtype: int
        :return: The generated random key converted
        into integer.
        """

        return self.system.generate_random_int()

    def generate_random_int_number_digit(self, number_digits):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an integer.

        :type number_digits: int
        :param number_digits: The number of digits to
        be used in the random value.
        :rtype: int
        :return: The generated random key converted
        into integer.
        """

        return self.system.generate_random_int(number_digits)

    def generate_random_value(self):
        """
        Generates a random value, using a key generated
        using the default random generator.
        This value is considered to be more "random" than
        using the default random generator because it uses
        a system with more entropy.

        :rtype: float
        :return: The generated random value (with high entropy).
        """

        return self.system.generate_random_value()

    def generate_random_md5(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an MD5 value.

        :rtype: MD5
        :return: The generated random key converted
        into an MD5 value.
        """

        return self.system.generate_random_md5()

    def generate_random_md5_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an MD5 string value.

        :rtype: String
        :return: The generated random key converted
        into an MD5 string value.
        """

        return self.system.generate_random_md5_string()

    def generate_random_sha1(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an SHA1 value.

        :rtype: SHA1
        :return: The generated random key converted
        into an SHA1 value.
        """

        return self.system.generate_random_sha1()

    def generate_random_sha1_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an SHA1 string value.

        :rtype: String
        :return: The generated random key converted
        into an SHA1 string value.
        """

        return self.system.generate_random_sha1_string()

    def generate_random_sha256(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an SHA256 value.

        :rtype: SHA256
        :return: The generated random key converted
        into an SHA256 value.
        """

        return self.system.generate_random_sha256()

    def generate_random_sha256_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an SHA256 string value.

        :rtype: String
        :return: The generated random key converted
        into an SHA256 string value.
        """

        return self.system.generate_random_sha256_string()
