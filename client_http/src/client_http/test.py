#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import json

import colony

class ClientHttpTest(colony.Test):
    """
    The client http infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            ClientHttpTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

        system = self.plugin.system
        test_case.http = system.create_client({})
        test_case.http.open()

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)

        test_case.http.close()

class ClientHttpTestCase(colony.ColonyTestCase):

    @staticmethod
    def get_description():
        return "Client Http Plugin test case"

    def test_create_client(self):
        response = self.http.fetch_url("http://httpbin.org/image/png")

        self.assertEqual(response.protocol_version, "HTTP/1.1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_message, "OK")
        self.assertEqual(response.headers_map["Content-Type"], "image/png")
        self.assertEqual(type(response.received_message), colony.legacy.BYTES)
        self.assertEqual(len(response.received_message) > 100, True)

        response = self.http.fetch_url("https://httpbin.org/image/png")

        self.assertEqual(response.protocol_version, "HTTP/1.1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_message, "OK")
        self.assertEqual(response.headers_map["Content-Type"], "image/png")
        self.assertEqual(type(response.received_message), colony.legacy.BYTES)
        self.assertEqual(len(response.received_message) > 100, True)

        response = self.http.fetch_url(
            "https://httpbin.org/post",
            method = "POST",
            contents = b"hello world"
        )

        self.assertEqual(response.protocol_version, "HTTP/1.1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_message, "OK")
        self.assertEqual(response.headers_map["Content-Type"], "application/json")
        self.assertEqual(type(response.received_message), colony.legacy.BYTES)
        self.assertEqual(len(response.received_message) > 10, True)

        received_message = response.received_message.decode("utf-8")
        received_message_j = json.loads(received_message)
        self.assertEqual(received_message_j["args"], {})
        self.assertEqual(received_message_j["form"], {})
        self.assertEqual(received_message_j["data"], "hello world")

        response = self.http.fetch_url(
            "https://httpbin.org/post",
            method = "POST",
            parameters = dict(hello = "world")
        )

        self.assertEqual(response.protocol_version, "HTTP/1.1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_message, "OK")
        self.assertEqual(response.headers_map["Content-Type"], "application/json")
        self.assertEqual(type(response.received_message), colony.legacy.BYTES)
        self.assertEqual(len(response.received_message) > 10, True)

        received_message = response.received_message.decode("utf-8")
        received_message_j = json.loads(received_message)
        self.assertEqual(received_message_j["args"], {})
        self.assertEqual(received_message_j["form"], {"hello" : "world"})
        self.assertEqual(received_message_j["data"], "")
