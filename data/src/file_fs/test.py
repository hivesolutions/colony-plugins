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

import shutil
import tempfile

import colony

from . import mocks
from . import system


class FileFSTest(colony.Test):
    """
    The file FS infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (FileFSTestCase,)

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class FileFSTestCase(colony.ColonyTestCase):
    """
    The file FS test case, verifying the file engine operations
    against a temporary directory used as the base path.
    """

    @staticmethod
    def get_description():
        return "File FS test case"

    def setUp(self):
        colony.ColonyTestCase.setUp(self)
        self.temp_path = tempfile.mkdtemp()
        self.connection = mocks.MockConnection(
            system.FsConnection("default", self.temp_path)
        )

    def tearDown(self):
        shutil.rmtree(self.temp_path, ignore_errors=True)
        colony.ColonyTestCase.tearDown(self)

    def test_exists(self):
        self.plugin.put_data(self.connection, b"hello", "hello.txt")

        self.assertEqual(self.plugin.exists(self.connection, "hello.txt"), True)
        self.assertEqual(self.plugin.exists(self.connection, "/hello.txt"), True)
        self.assertEqual(self.plugin.exists(self.connection, "missing.txt"), False)

    def test_exists_directory(self):
        # verifies that a directory is considered to exist, so that its
        # retrieval as a file fails with the error of the file system (not
        # being reported as a file that does not exist)
        self.plugin.put_data(self.connection, b"hello", "images/hello.txt")

        self.assertEqual(self.plugin.exists(self.connection, "images"), True)
        self.assertRaises(IOError, self.plugin.get, self.connection, "images")
