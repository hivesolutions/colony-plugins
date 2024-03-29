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

import os
import time
import random
import hashlib
import threading

import colony

TIME_FACTOR = 1000
""" The time factor """

MAXIMUM_KEY = colony.legacy.LONG(18446744073709551616)
""" The maximum key"""

SECRET_KEY = colony.legacy.LONG(123123123)
""" The pseudo secret key """

SYSTEM_RANDOM_VALUE = "SystemRandom"
""" The system random value """


class Random(colony.System):
    """
    The random class.
    """

    randrange = random.randrange
    """ The rand range method to be used """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)

        # processes the rand range of values
        self.process_randrange()

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

        # generates a random key
        random_key = self.randrange(0, MAXIMUM_KEY)

        # retrieves the process id
        process_id = os.getpid()

        # retrieves the process id in absolute
        process_id_absolute = abs(process_id)

        # retrieves the thread id
        thread_id = threading.current_thread().ident

        # retrieves the thread id in absolute
        thread_id_absolute = abs(thread_id)

        # retrieves the current time
        current_time = time.time()

        # converts the current time to integer
        current_time_integer = int(current_time * TIME_FACTOR)

        # creates the random value
        random = "%s%s%s%s%s" % (
            SECRET_KEY,
            process_id_absolute,
            thread_id_absolute,
            current_time_integer,
            random_key,
        )

        # returns the random value
        return random

    def generate_random_int(self, number_digits=None):
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

        # generates a random value
        random = self.generate_random()

        # converts the random to int value
        random_int = int(random)

        # converts the random into to the number of
        # digits wanted
        random_int = number_digits and random_int % pow(10, number_digits) or random_int

        # returns the random int value
        return random_int

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

        # generates a random int value
        random_int = self.generate_random_int()

        # sets the current seed in random
        random.seed(random_int)

        # generates a random value
        random_value = random.random()

        # returns the random value
        return random_value

    def generate_random_md5(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an MD5 value.

        :rtype: MD5
        :return: The generated random key converted
        into an MD5 value.
        """

        # generates a random value
        random = self.generate_random()

        # generates an MD5 hash of the random value
        # note that the random value is first encoded
        # into a bytes value before the hash
        random = colony.legacy.bytes(random)
        random_md5 = hashlib.md5(random)

        # returns the MD5 hash of the random value
        return random_md5

    def generate_random_md5_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an MD5 string value.

        :rtype: String
        :return: The generated random key converted
        into an MD5 string value.
        """

        # generates the MD5 hash of a random value
        random_md5 = self.generate_random_md5()

        # converts the MD5 hash into string
        random_md5_string = random_md5.hexdigest()

        # returns the string value of the MD5 hash
        # of the random value
        return random_md5_string

    def generate_random_sha1(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an SHA1 value.

        :rtype: SHA1
        :return: The generated random key converted
        into an SHA1 value.
        """

        # generates a random value
        random = self.generate_random()

        # generates an SHA1 hash of the random value
        # note that the random value is first encoded
        # into a bytes value before the hash
        random = colony.legacy.bytes(random)
        random_sha1 = hashlib.sha1(random)

        # returns the SHA1 hash of the random value
        return random_sha1

    def generate_random_sha1_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an SHA1 string value.

        :rtype: String
        :return: The generated random key converted
        into an SHA1 string value.
        """

        # generates the SHA1 hash of a random value
        random_sha1 = self.generate_random_sha1()

        # converts the SHA1 hash into string
        random_sha1_string = random_sha1.hexdigest()

        # returns the string value of the SHA1 hash
        # of the random value
        return random_sha1_string

    def generate_random_sha256(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an SHA256 value.

        :rtype: SHA256
        :return: The generated random key converted
        into an SHA256 value.
        """

        # generates a random value
        random = self.generate_random()

        # generates an SHA256 hash of the random value
        # note that the random value is first encoded
        # into a bytes value before the hash
        random = colony.legacy.bytes(random)
        random_sha256 = hashlib.sha256(random)

        # returns the SHA256 hash of the random value
        return random_sha256

    def generate_random_sha256_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an SHA256 string value.

        :rtype: String
        :return: The generated random key converted
        into an SHA256 string value.
        """

        # generates the SHA256 hash of a random value
        random_sha256 = self.generate_random_sha256()

        # converts the SHA256 hash into string
        random_sha256_string = random_sha256.hexdigest()

        # returns the string value of the SHA256 hash
        # of the random value
        return random_sha256_string

    def process_randrange(self):
        """
        Processes the current rand range method
        setting the best possible one.
        """

        # in case the system random is defined
        if hasattr(random, SYSTEM_RANDOM_VALUE):
            # creates a "new" system random
            system_random = random.SystemRandom()

            # sets the random range method
            self.randrange = system_random.randrange
        # otherwise
        else:
            # sets the random range method (default one)
            self.randrange = random.randrange
