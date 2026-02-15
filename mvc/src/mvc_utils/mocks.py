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


class MockPlugin(object):
    def __init__(self):
        self.mvc_utils_plugin = None
        self.template_engine_plugin = None
        self.json_plugin = None
        self.entity_manager_plugin = None
        self.business_helper_plugin = None
        self.resources_manager_plugin = None
        self.file_manager_plugin = None
        self.manager = None
        self.template_engine = []


class MockController(object):
    def __init__(self):
        self.name = "test_controller"


class MockModelWithErrors(object):
    def __init__(self):
        self.validation_errors_map = {"email": ["invalid format", "required"]}


class MockRequest(object):
    def __init__(self, parameters=None):
        self.parameters = parameters or {}


class MockValidatedController(object):
    def __init__(self, validate_reasons=None, validation_failed_result=None):
        self._validate_reasons = validate_reasons or []
        self._validation_failed_result = validation_failed_result
        self._validation_failed_calls = []

    def validate(self, request, parameters, validation_parameters):
        return self._validate_reasons

    def validation_failed(self, request, parameters, validation_parameters, reasons):
        self._validation_failed_calls.append(
            dict(
                request=request,
                parameters=parameters,
                validation_parameters=validation_parameters,
                reasons=reasons,
            )
        )
        return self._validation_failed_result


class MockValidatedControllerNoHandler(object):
    def __init__(self, validate_reasons=None):
        self._validate_reasons = validate_reasons or []

    def validate(self, request, parameters, validation_parameters):
        return self._validate_reasons
