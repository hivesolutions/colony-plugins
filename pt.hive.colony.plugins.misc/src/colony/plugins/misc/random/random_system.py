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
import hashlib

TIME_FACTOR = 1000
""" The time factor """

MAXIMUM_SESSION_KEY = 18446744073709551616L
""" The maximum session key"""

SECRET_KEY = 123123123L
""" The pseudo secret key """

class Random:
    """
    The random class.
    """

    random_plugin = None
    """ The random plugin """

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
        # retrieves the process id
        process_id = os.getpid()

        # retrieves the current time
        current_time = time.time()

        # converts the current time to integer
        current_time_integer = int(current_time * TIME_FACTOR)

        # creates the random value
        random = "%s%s%s%s"  % ((self.randrange(0, MAXIMUM_SESSION_KEY), process_id, current_time_integer, SECRET_KEY))

        # returns the random value
        return random

    def generate_random_int(self):
        # generates a random value
        random = self.generate_random()

        # converts the random to int value
        random_int = int(random)

        # returns the random int value
        return random_int

    def generate_random_value(self):
        # generates a random int value
        random_int = self.generate_random_int()

        # sets the current seed in random
        random.seed(random_int)

        # generates a random value
        random_value = random.random()

        # returns the random value
        return random_value

    def generate_random_md5(self):
        # generates a random value
        random = self.generate_random()

        # generates an md5 hash of the random value
        random_md5 = hashlib.md5(random)

        # returns the md5 hash of the random value
        return random_md5

    def generate_random_md5_string(self):
        # generates the md5 hash of a random value
        random_md5 = self.generate_random_md5()

        # converts the md5 hash into string
        random_md5_string = random_md5.hexdigest()

        # returns the string value of the md5 hash
        # of the random value
        return random_md5_string

    def generate_random_sha1(self):
        # generates a random value
        random = self.generate_random()

        # generates an sha1 hash of the random value
        random_sha1 = hashlib.sha1(random)

        # returns the sha1 hash of the random value
        return random_sha1

    def generate_random_sha1_string(self):
        # generates the sha1 hash of a random value
        random_sha1 = self.generate_random_sha1()

        # converts the sha1 hash into string
        random_sha1_string = random_sha1.hexdigest()

        # returns the string value of the sha1 hash
        # of the random value
        return random_sha1_string

    def generate_random_sha256(self):
        # generates a random value
        random = self.generate_random()

        # generates an sha256 hash of the random value
        random_sha256 = hashlib.sha256(random)

        # returns the sha256 hash of the random value
        return random_sha256

    def generate_random_sha256_string(self):
        # generates the sha256 hash of a random value
        random_sha256 = self.generate_random_sha256()

        # converts the sha256 hash into string
        random_sha256_string = random_sha256.hexdigest()

        # returns the string value of the sha256 hash
        # of the random value
        return random_sha256_string

    def process_randrange(self):
        if hasattr(random, "SystemRandom"):
            self.randrange = random.SystemRandom().randrange
        else:
            self.randrange = random.randrange
