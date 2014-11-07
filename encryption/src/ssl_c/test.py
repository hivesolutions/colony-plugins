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
import shutil
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

        system = self.plugin.system

        test_case.dir_path = tempfile.mkdtemp()
        test_case.private_path = os.path.join(test_case.dir_path, "private.key")
        test_case.public_path = os.path.join(test_case.dir_path, "public.key")

        test_case.ssl = system.create_structure({})
        test_case.ssl.generate_keys(
            test_case.private_path,
            test_case.public_path,
            number_bits = 128
        )

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)

        if os.path.isdir(test_case.dir_path): shutil.rmtree(test_case.dir_path)

        test_case.dir_path = None
        test_case.private_path = None
        test_case.public_path = None
        test_case.ssl = None

class SslBaseTestCase(colony.ColonyTestCase):

    @staticmethod
    def get_description():
        return "Ssl Plugin test case"

    def test_encrypt_base_64(self):
        result = self.ssl.encrypt_base_64(self.public_path, "Hello World")
        #self.assertEqual(result, "AG0XpKTXRpbnC/0Dp0E9PQ==\n")
