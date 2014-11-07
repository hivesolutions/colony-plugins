#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import string
import random
import tempfile

import colony

class SslTest(colony.Test):
    """
    The ssl infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            SslBaseTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

        manager = self.plugin.manager
        system = self.plugin.system

        plugin_path = manager.get_plugin_path_by_id(self.plugin.id)
        resources_path = os.path.join(plugin_path, "ssl_c", "resources")

        test_case.private_path = os.path.join(resources_path, "private.key")
        test_case.public_path = os.path.join(resources_path, "public.key")

        test_case.ssl = system.create_structure({})

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)

        test_case.private_path = None
        test_case.public_path = None
        test_case.ssl = None

class SslBaseTestCase(colony.ColonyTestCase):

    @staticmethod
    def get_description():
        return "Ssl Plugin test case"

    def test_generate_keys(self):
        dir_path = tempfile.mkdtemp()
        private_path = os.path.join(dir_path, "private.key")
        public_path = os.path.join(dir_path, "public.key")

        self.ssl.generate_keys(private_path, public_path, number_bits = 128)

        result_encrypt = self.ssl.encrypt_base_64(public_path, "Hello World")
        result = self.ssl.decrypt_base_64(private_path, result_encrypt)
        self.assertEqual(result, "Hello World")

        for _index in range(0, 128):
            value = "".join(random.choice(string.ascii_lowercase) for _index in range(12))
            result_encrypt = self.ssl.encrypt_base_64(public_path, value)
            result = self.ssl.decrypt_base_64(private_path, result_encrypt)
            self.assertEqual(result, value)

    def test_encrypt_base_64(self):
        result = self.ssl.encrypt_base_64(self.public_path, self._pad("Hello World"))
        self.assertEqual(result, "Ar8fujgbooIjkjBLqqmb5lDkVoLKd/7kOFp0foQTVew=\n")

        result = self.ssl.decrypt_base_64(self.private_path, "Ar8fujgbooIjkjBLqqmb5lDkVoLKd/7kOFp0foQTVew=\n")
        self.assertEqual(result, self._pad("Hello World"))

    def _pad(self, message, size = 256):
        size_b = size // 8
        message_s = len(message)
        pad_size = size_b - message_s - 3
        return message + "\x00" * pad_size
