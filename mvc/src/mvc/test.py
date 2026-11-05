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

from . import system
from . import exceptions
from . import mocks


class MVCTest(colony.Test):
    """
    The MVC infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (MVCSystemTestCase,)

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class MVCSystemTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "MVC System test case"

    def setUp(self):
        colony.ColonyTestCase.setUp(self)
        self._saved_keep = colony.conf("SESSION_KEEP", None)
        colony.conf_r("SESSION_KEEP")

    def tearDown(self):
        colony.conf_r("SESSION_KEEP")
        if not self._saved_keep == None:
            colony.conf_s("SESSION_KEEP", self._saved_keep)

    def test_handle_rest_request(self):
        mock_plugin = mocks.MockPlugin()
        mvc = system.MVC(mock_plugin)

        service_plugin = mocks.MockMVCServicePlugin()
        mvc.load_mvc_service_plugin(service_plugin)
        mvc.unload_mvc_service_plugin(service_plugin)

        mock_request = mocks.MockRESTRequest()
        self.assertRaises(
            exceptions.MVCRequestNotHandled, mvc.handle_rest_request, mock_request
        )
        self.assertEqual(mock_request.calls, ["clear_sessions"])
        self.assertEqual(mvc.clear_pending, False)

        # runs a second request so that it's verified that only the
        # first request after the unloading clears the sessions
        self.assertRaises(
            exceptions.MVCRequestNotHandled, mvc.handle_rest_request, mock_request
        )
        self.assertEqual(mock_request.calls, ["clear_sessions"])

    def test_handle_rest_request_keep(self):
        colony.conf_s("SESSION_KEEP", "1")

        mock_plugin = mocks.MockPlugin()
        mvc = system.MVC(mock_plugin)

        service_plugin = mocks.MockMVCServicePlugin()
        mvc.load_mvc_service_plugin(service_plugin)
        mvc.unload_mvc_service_plugin(service_plugin)

        mock_request = mocks.MockRESTRequest()
        self.assertRaises(
            exceptions.MVCRequestNotHandled, mvc.handle_rest_request, mock_request
        )
        self.assertEqual(mock_request.calls, [])

    def test_unload_mvc_service_plugin(self):
        mock_plugin = mocks.MockPlugin()
        mvc = system.MVC(mock_plugin)

        service_plugin = mocks.MockMVCServicePlugin()
        mvc.load_mvc_service_plugin(service_plugin)
        self.assertIn("^mvc/test$", mvc.patterns_map)
        self.assertIn("mock.mock.handle_test", mvc.patterns_index)
        self.assertEqual(mvc.clear_pending, False)

        mvc.unload_mvc_service_plugin(service_plugin)
        self.assertNotIn("^mvc/test$", mvc.patterns_map)
        self.assertNotIn("mock.mock.handle_test", mvc.patterns_index)
        self.assertEqual(mvc.clear_pending, True)

    def test_unload_mvc_service_plugin_production(self):
        mock_plugin = mocks.MockPlugin()
        mock_plugin.manager.run_mode = "production"
        mvc = system.MVC(mock_plugin)

        service_plugin = mocks.MockMVCServicePlugin()
        mvc.load_mvc_service_plugin(service_plugin)
        mvc.unload_mvc_service_plugin(service_plugin)
        self.assertNotIn("^mvc/test$", mvc.patterns_map)
        self.assertEqual(mvc.clear_pending, False)

    def test_unload_mvc_service_plugin_keep(self):
        mock_plugin = mocks.MockPlugin()
        mvc = system.MVC(mock_plugin)

        service_plugin = mocks.MockMVCServicePlugin()
        mvc.load_mvc_service_plugin(service_plugin)

        # sets the value only after the loading so that it's verified
        # that the configuration is read at the time of the unloading
        colony.conf_s("SESSION_KEEP", "1")
        mvc.unload_mvc_service_plugin(service_plugin)
        self.assertNotIn("^mvc/test$", mvc.patterns_map)
        self.assertNotIn("mock.mock.handle_test", mvc.patterns_index)
        self.assertEqual(mvc.clear_pending, False)

    def test_unload_mvc_service_plugin_keep_disabled(self):
        colony.conf_s("SESSION_KEEP", "0")

        mock_plugin = mocks.MockPlugin()
        mvc = system.MVC(mock_plugin)

        service_plugin = mocks.MockMVCServicePlugin()
        mvc.load_mvc_service_plugin(service_plugin)
        mvc.unload_mvc_service_plugin(service_plugin)
        self.assertEqual(mvc.clear_pending, True)
