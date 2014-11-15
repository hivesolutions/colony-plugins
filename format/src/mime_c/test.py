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

import colony

class MimeTest(colony.Test):
    """
    The mime based test manager that handles the
    management of the associated test cases.
    """

    def get_bundle(self):
        return (
            MimeBaseTestCase,
        )

class MimeBaseTestCase(colony.ColonyTestCase):

    @staticmethod
    def get_description():
        return "Mime Plugin test case"

    def test_write(self):
        message = self.system.create_message({})
        message.write("Hello World")
        result = message.get_value(encode = True)
        self.assertEqual(result, b"MIME-Version: 1.0\r\n\r\nHello World")
        result = message.get_value(encode = False)
        self.assertEqual(result, "MIME-Version: 1.0\r\n\r\nHello World")

    def test_write_unicode(self):
        message = self.system.create_message({})
        message.write("你好世界")
        result = message.get_value(encode = True)
        self.assertEqual(result, colony.legacy.u("MIME-Version: 1.0\r\n\r\n你好世界").encode("utf-8"))
        result = message.get_value(encode = False)
        self.assertEqual(result, colony.legacy.u("MIME-Version: 1.0\r\n\r\n你好世界"))

    def test_read(self):
        message = self.system.create_message({})
        message.read_simple(b"MIME-Version: 1.0\r\n\r\nHello World")
        result = message.get_value(encode = True)
        self.assertEqual(result, b"MIME-Version: 1.0\r\n\r\nHello World")
        result = message.get_value(encode = False)
        self.assertEqual(result, "MIME-Version: 1.0\r\n\r\nHello World")

    def test_read_unicode(self):
        message = self.system.create_message({})
        message.read_simple(colony.legacy.u("MIME-Version: 1.0\r\n\r\n你好世界"))
        result = message.get_value(encode = True)
        self.assertEqual(result, colony.legacy.u("MIME-Version: 1.0\r\n\r\n你好世界").encode("utf-8"))
        result = message.get_value(encode = False)
        self.assertEqual(result, colony.legacy.u("MIME-Version: 1.0\r\n\r\n你好世界"))

    def test_base_64(self):
        message = self.system.create_message({})
        message.write_base_64("Hello World")
        result = message.get_value(encode = True)
        self.assertEqual(result, b"MIME-Version: 1.0\r\n\r\nSGVsbG8gV29ybGQ=")
