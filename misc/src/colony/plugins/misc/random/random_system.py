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

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import time
import random
import thread
import hashlib

TIME_FACTOR = 1000
""" The time factor """

MAXIMUM_KEY = 18446744073709551616L
""" The maximum key"""

SECRET_KEY = 123123123L
""" The pseudo secret key """

SYSTEM_RANDOM_VALUE = "SystemRandom"
""" The system random value """

class Random:
    """
    The random class.
    """

    random_plugin = None
    """ The random plugin """

    randrange = random.randrange
    """ The rand range method to be used """

    def __init__(self, random_plugin):
        """
        Constructor of the class.

        @type random_plugin: RandomPlugin
        @param random_plugin:  The random plugin.
        """

        self.random_plugin = random_plugin

        # processes the randrange values
        self.process_randrange()

    def generate_random(self):
        """
        Generates a random string for cryptographic
        usage (because of its entropy).
        The string is creating using a random number generator,
        the current process id, thread id, the current time
        and a secret key.

        @rtype: String
        @return: The generated random string for cryptographic
        usage (with high entropy).
        """

        # generates a random key
        random_key = self.randrange(0, MAXIMUM_KEY)

        # retrieves the process id
        process_id = os.getpid()

        # retrieves the process id in absolute
        process_id_absolute = abs(process_id)

        # retrieves the thread id
        thread_id = thread.get_ident()

        # retrieves the thread id in absolute
        thread_id_absolute = abs(thread_id)

        # retrieves the current time
        current_time = time.time()

        # converts the current time to integer
        current_time_integer = int(current_time * TIME_FACTOR)

        # creates the random value
        random = "%s%s%s%s%s"  % (SECRET_KEY, process_id_absolute, thread_id_absolute, current_time_integer, random_key)

        # returns the random value
        return random

    def generate_random_int(self, number_digits = None):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an integer.

        @type number_digits: int
        @param number_digits: The number of digits to
        be used in the random value.
        @rtype: int
        @return: The generated random key converted
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

        @rtype: float
        @return: The generated random value (with high entropy).
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
        into an md5 value.

        @rtype: Md5
        @return: The generated random key converted
        into an md5 value.
        """

        # generates a random value
        random = self.generate_random()

        # generates an md5 hash of the random value
        random_md5 = hashlib.md5(random)

        # returns the md5 hash of the random value
        return random_md5

    def generate_random_md5_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an md5 string value.

        @rtype: String
        @return: The generated random key converted
        into an md5 string value.
        """

        # generates the md5 hash of a random value
        random_md5 = self.generate_random_md5()

        # converts the md5 hash into string
        random_md5_string = random_md5.hexdigest()

        # returns the string value of the md5 hash
        # of the random value
        return random_md5_string

    def generate_random_sha1(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an sha1 value.

        @rtype: Sha1
        @return: The generated random key converted
        into an sha1 value.
        """

        # generates a random value
        random = self.generate_random()

        # generates an sha1 hash of the random value
        random_sha1 = hashlib.sha1(random)

        # returns the sha1 hash of the random value
        return random_sha1

    def generate_random_sha1_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an sha1 string value.

        @rtype: String
        @return: The generated random key converted
        into an sha1 string value.
        """

        # generates the sha1 hash of a random value
        random_sha1 = self.generate_random_sha1()

        # converts the sha1 hash into string
        random_sha1_string = random_sha1.hexdigest()

        # returns the string value of the sha1 hash
        # of the random value
        return random_sha1_string

    def generate_random_sha256(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an sha256 value.

        @rtype: Sha256
        @return: The generated random key converted
        into an sha256 value.
        """

        # generates a random value
        random = self.generate_random()

        # generates an sha256 hash of the random value
        random_sha256 = hashlib.sha256(random)

        # returns the sha256 hash of the random value
        return random_sha256

    def generate_random_sha256_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an sha256 string value.

        @rtype: String
        @return: The generated random key converted
        into an sha256 string value.
        """

        # generates the sha256 hash of a random value
        random_sha256 = self.generate_random_sha256()

        # converts the sha256 hash into string
        random_sha256_string = random_sha256.hexdigest()

        # returns the string value of the sha256 hash
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
