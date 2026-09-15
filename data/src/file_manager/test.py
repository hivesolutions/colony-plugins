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

from . import mocks
from . import system
from . import exceptions

MTIME = 1789400000.0
""" The modification timestamp of the file kept in the mock
file engine, used to verify the value retrieved for it """


class FileManagerTest(colony.Test):
    """
    The file manager infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (FileManagerTestCase, ExceptionsTestCase)

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class FileManagerTestCase(colony.ColonyTestCase):
    """
    The file manager test case, verifying that the operations are
    delegated to the file engine and that a file (or directory) that
    does not exist is reported with the not found error, independently
    of the file engine, when that's requested by the caller.
    """

    @staticmethod
    def get_description():
        return "File Manager test case"

    def setUp(self):
        colony.ColonyTestCase.setUp(self)
        files = dict(hello=(b"hello", MTIME))
        files["images/hello.png"] = (b"image", MTIME)
        self.file_engine_plugin = mocks.MockFileEnginePlugin(files=files)
        self.file_manager = system.FileManager(self.file_engine_plugin)

    def test_get(self):
        self.assertEqual(self.file_manager.get("hello"), b"hello")
        self.assertEqual(self.file_manager.get("hello", raise_e=True), b"hello")

    def test_get_not_found(self):
        # verifies that by default the error of the file engine is raised
        # as it is and that the file not found error is raised instead when
        # the raising of the error is requested by the caller
        self.assert_raises(KeyError, self.file_manager.get, "missing")
        self.assert_raises(
            exceptions.FileNotFound, self.file_manager.get, "missing", raise_e=True
        )

    def test_delete(self):
        self.file_manager.delete("hello", raise_e=True)

        self.assertEqual(self.file_manager.exists("hello"), False)

    def test_delete_not_found(self):
        self.assert_raises(KeyError, self.file_manager.delete, "missing")
        self.assert_raises(
            exceptions.FileNotFound, self.file_manager.delete, "missing", raise_e=True
        )

    def test_list(self):
        self.assertEqual(self.file_manager.list("images"), ["hello.png"])
        self.assertEqual(self.file_manager.list("images", raise_e=True), ["hello.png"])

    def test_list_not_found(self):
        # verifies that a file is not considered to be a directory, so
        # that its listing fails as the listing of any other directory
        # that does not exist, raising the directory not found error when
        # the raising of the error is requested by the caller
        self.assert_raises(KeyError, self.file_manager.list, "hello")
        self.assert_raises(
            exceptions.DirectoryNotFound, self.file_manager.list, "hello", raise_e=True
        )
        self.assert_raises(
            exceptions.DirectoryNotFound,
            self.file_manager.list,
            "missing",
            raise_e=True,
        )

    def test_size(self):
        self.assertEqual(self.file_manager.size("hello"), 5)
        self.assertEqual(self.file_manager.size("hello", raise_e=True), 5)

    def test_size_not_found(self):
        self.assert_raises(KeyError, self.file_manager.size, "missing")
        self.assert_raises(
            exceptions.FileNotFound, self.file_manager.size, "missing", raise_e=True
        )

    def test_mtime(self):
        self.assertEqual(self.file_manager.mtime("hello"), MTIME)
        self.assertEqual(self.file_manager.mtime("hello", raise_e=True), MTIME)

    def test_mtime_not_found(self):
        self.assert_raises(KeyError, self.file_manager.mtime, "missing")
        self.assert_raises(
            exceptions.FileNotFound, self.file_manager.mtime, "missing", raise_e=True
        )

    def test_exists(self):
        self.assertEqual(self.file_manager.exists("hello"), True)
        self.assertEqual(self.file_manager.exists("missing"), False)

    def test_exists_directory(self):
        self.assertEqual(self.file_manager.exists_directory("images"), True)
        self.assertEqual(self.file_manager.exists_directory("hello"), False)
        self.assertEqual(self.file_manager.exists_directory("missing"), False)


class ExceptionsTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "File Manager exceptions test case"

    def test_file_manager_exception(self):
        exception = exceptions.FileManagerException()

        self.assertTrue(isinstance(exception, colony.ColonyException))
        self.assertEqual(exception.message, None)

    def test_file_not_found(self):
        exception = exceptions.FileNotFound("/images/hello.png")

        self.assertTrue(isinstance(exception, exceptions.FileManagerException))
        self.assertEqual(exception.message, "/images/hello.png")
        self.assertEqual(str(exception), "File not found - /images/hello.png")

    def test_directory_not_found(self):
        exception = exceptions.DirectoryNotFound("/images")

        self.assertTrue(isinstance(exception, exceptions.FileManagerException))
        self.assertEqual(exception.message, "/images")
        self.assertEqual(str(exception), "Directory not found - /images")
