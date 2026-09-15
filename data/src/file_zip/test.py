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
import shutil
import tempfile

import colony

from . import mocks
from . import system


class FileZipTest(colony.Test):
    """
    The file zip infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (FileZipTestCase,)

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class FileZipTestCase(colony.ColonyTestCase):
    """
    The file zip test case, verifying the file engine operations
    against a zip file stored in a temporary directory.
    """

    @staticmethod
    def get_description():
        return "File Zip test case"

    def setUp(self):
        colony.ColonyTestCase.setUp(self)
        self.temp_path = tempfile.mkdtemp()
        self.connection = mocks.MockConnection(
            system.ZipConnection("default", os.path.join(self.temp_path, "default.zip"))
        )

    def tearDown(self):
        shutil.rmtree(self.temp_path, ignore_errors=True)
        colony.ColonyTestCase.tearDown(self)

    def test_get(self):
        self.plugin.put_data(self.connection, b"hello", "hello.txt")

        file = self.plugin.get(self.connection, "/hello.txt")

        self.assertEqual(file.read(), b"hello")

    def test_exists(self):
        # verifies that no file exists while the zip file has not been
        # created, as no file has been put in it yet
        self.assertEqual(self.plugin.exists(self.connection, "hello.txt"), False)

        self.plugin.put_data(self.connection, b"hello", "hello.txt")

        self.assertEqual(self.plugin.exists(self.connection, "hello.txt"), True)
        self.assertEqual(self.plugin.exists(self.connection, "/hello.txt"), True)
        self.assertEqual(self.plugin.exists(self.connection, "missing.txt"), False)

    def test_exists_directory(self):
        # verifies that no directory exists while the zip file has not
        # been created, not even the root one, as nothing has been put
        self.assertEqual(self.plugin.exists_directory(self.connection, "images"), False)
        self.assertEqual(self.plugin.exists_directory(self.connection, ""), False)

        self.plugin.put_data(self.connection, b"hello", "images/hello.png")

        self.assertEqual(self.plugin.exists_directory(self.connection, "images"), True)
        self.assertEqual(self.plugin.exists_directory(self.connection, "/images"), True)
        self.assertEqual(self.plugin.exists_directory(self.connection, "images/"), True)
        self.assertEqual(self.plugin.exists_directory(self.connection, ""), True)
        self.assertEqual(
            self.plugin.exists_directory(self.connection, "missing"), False
        )

        # verifies that neither the prefix of the name of a directory nor
        # the name of a file are considered to be a directory, as a directory
        # is only matched by the complete path of its files
        self.assertEqual(self.plugin.exists_directory(self.connection, "imag"), False)
        self.assertEqual(
            self.plugin.exists_directory(self.connection, "images/hello.png"), False
        )
