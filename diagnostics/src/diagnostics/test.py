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


class DiagnosticsTest(colony.Test):
    """
    The diagnostics infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (DiagnosticsRequestTestCase,)

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class DiagnosticsRequestTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Diagnostics request test case"

    def test_request_end(self):
        diagnostics = self._build_diagnostics()
        request = mocks.MockRequest(status_code=200)
        diagnostics.request_begin(request)

        diagnostics.request_end(request)

        data = diagnostics.get_data()["requests"][id(request)]
        self.assertEqual(data["code"], 200)
        self.assertEqual(data["method"], "GET")

    def test_request_end_exception(self):
        diagnostics = self._build_diagnostics()
        request = mocks.MockRequest(status_code=500)
        diagnostics.request_begin(request)

        # the request end event is also notified with the exception that
        # caused the request to fail, meaning that the handler must be
        # able to receive it without raising any kind of error
        diagnostics.request_end(request, RuntimeError("problem"))

        data = diagnostics.get_data()["requests"][id(request)]
        self.assertEqual(data["code"], 500)

    def test_request_end_no_status_code(self):
        diagnostics = self._build_diagnostics()
        request = mocks.MockRequest(status_code=None)
        diagnostics.request_begin(request)

        diagnostics.request_end(request)

        data = diagnostics.get_data()["requests"][id(request)]
        self.assertEqual(data["code"], 500)

    def _build_diagnostics(self):
        return system.Diagnostics(mocks.MockPlugin())
