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


class FileGridFSTest(colony.Test):
    """
    The file GridFS infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (FileGridFSTestCase,)

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class FileGridFSTestCase(colony.ColonyTestCase):
    """
    The file GridFS test case, verifying the file engine operations
    against a mock GridFS system (no MongoDB server is required).
    """

    @staticmethod
    def get_description():
        return "File GridFS test case"

    def test_exists(self):
        connection = mocks.MockConnection(
            mocks.MockGridFS(file_names=["/images/hello.png"])
        )

        self.assertEqual(self.plugin.exists(connection, "images/hello.png"), True)
        self.assertEqual(self.plugin.exists(connection, "/images/hello.png"), True)
        self.assertEqual(self.plugin.exists(connection, "images/missing.png"), False)
