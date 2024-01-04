#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
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
        return "Mime Base test case"

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

    def test_read_headers(self):
        message = self.system.create_message({})
        message.read_simple(colony.legacy.u("MIME-Version: 1.0\r\nTest: 你好世界\r\n\r\n你好世界"))
        result = message.get_header("Test")
        self.assertEqual(result, colony.legacy.u("你好世界"))

    def test_base_64(self):
        message = self.system.create_message({})
        message.write_base_64("Hello World")
        result = message.get_value(encode = True)
        self.assertEqual(result, b"MIME-Version: 1.0\r\n\r\nSGVsbG8gV29ybGQ=")

    def test_headers(self):
        message = self.system.create_message({})
        message.write("Hello World")
        message.set_header("Test", "Hello World")
        result = message.get_value(encode = True)
        self.assertEqual(result, b"MIME-Version: 1.0\r\nTest: Hello World\r\n\r\nHello World")

        message = self.system.create_message({})
        message.write("你好世界")
        message.set_header("Test", "你好世界")
        result = message.get_value(encode = False)
        self.assertEqual(result, colony.legacy.u("MIME-Version: 1.0\r\nTest: 你好世界\r\n\r\n你好世界"))

    def test_multi_part(self):
        message = self.system.create_message({})
        part = self.system.create_message_part({})
        part.write("Hello World")

        message.set_multi_part("mixed")
        message.add_part(part)

        result = message.get_value(encode = False)
        boundary = message.get_boundary()

        expected = colony.legacy.u(
            "Content-Type: multipart/mixed;boundary=\"%s\"\r\n" % boundary +\
            "MIME-Version: 1.0\r\n\r\n" +\
            "This is a multi-part message in MIME format\r\n" +\
            "--" + boundary + "\r\n\r\n" +\
            "Hello World" +\
            "\r\n--" + boundary + "--\r\n"
        )

        self.assertEqual(result,expected)
