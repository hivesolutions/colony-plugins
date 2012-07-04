#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system

class RandomPlugin(colony.base.system.Plugin):
    """
    The main class for the Random plugin.
    """

    id = "pt.hive.colony.plugins.misc.random"
    name = "Random Plugin"
    short_name = "Random"
    description = "A plugin to generate ramdom numbers"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/misc/random/resources/baf.xml"
    }
    capabilities = [
        "random",
        "build_automation_item"
    ]
    main_modules = [
        "misc.random.random_system"
    ]

    random = None
    """ The random """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import misc.random.random_system
        self.random = misc.random.random_system.Random(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

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

        return self.random.generate_random()

    def generate_random_int(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an integer.

        @rtype: int
        @return: The generated random key converted
        into integer.
        """

        return self.random.generate_random_int()

    def generate_random_int_number_digit(self, number_digits):
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

        return self.random.generate_random_int(number_digits)

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

        return self.random.generate_random_value()

    def generate_random_md5(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an md5 value.

        @rtype: Md5
        @return: The generated random key converted
        into an md5 value.
        """

        return self.random.generate_random_md5()

    def generate_random_md5_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an md5 string value.

        @rtype: String
        @return: The generated random key converted
        into an md5 string value.
        """

        return self.random.generate_random_md5_string()

    def generate_random_sha1(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an sha1 value.

        @rtype: Sha1
        @return: The generated random key converted
        into an sha1 value.
        """

        return self.random.generate_random_sha1()

    def generate_random_sha1_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an sha1 string value.

        @rtype: String
        @return: The generated random key converted
        into an sha1 string value.
        """

        return self.random.generate_random_sha1_string()

    def generate_random_sha256(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an sha256 value.

        @rtype: Sha256
        @return: The generated random key converted
        into an sha256 value.
        """

        return self.random.generate_random_sha256()

    def generate_random_sha256_string(self):
        """
        Generates a random key, using the current
        default random generator and converts it
        into an sha256 string value.

        @rtype: String
        @return: The generated random key converted
        into an sha256 string value.
        """

        return self.random.generate_random_sha256_string()
