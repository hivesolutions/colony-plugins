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


class MVCUtilsTest(colony.Test):
    """
    The MVC utils infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            MVCUtilsBaseTestCase,
            RawModelTestCase,
            ExceptionsTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class MVCUtilsBaseTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "MVC Utils Base test case"

    def test_initialization(self):
        # creates a mock plugin and initializes mvc utils
        mock_plugin = MockPlugin()
        mvc_utils = system.MVCUtils(mock_plugin)

        # verifies the maps are initialized
        self.assertEqual(mvc_utils.models_modules_map, {})
        self.assertEqual(mvc_utils.package_path_models_map, {})
        self.assertEqual(mvc_utils.package_path_controllers_map, {})

    def test_get_models_not_found(self):
        # creates a mock plugin and mvc utils
        mock_plugin = MockPlugin()
        mvc_utils = system.MVCUtils(mock_plugin)

        # verifies getting a non-existent models id raises exception
        raised = False
        try:
            mvc_utils.get_models("nonexistent")
        except Exception:
            raised = True
        self.assertEqual(raised, True)

    def test_convert_controller_name(self):
        # creates a mock plugin and mvc utils
        mock_plugin = MockPlugin()
        mvc_utils = system.MVCUtils(mock_plugin)

        # tests controller name conversion
        ref_name, base_name = mvc_utils._convert_controller_name("MainController")
        self.assertEqual(ref_name, "main_controller")
        self.assertEqual(base_name, "main")

    def test_convert_controller_name_with_prefix(self):
        # creates a mock plugin and mvc utils
        mock_plugin = MockPlugin()
        mvc_utils = system.MVCUtils(mock_plugin)

        # tests controller name conversion with prefix
        ref_name, base_name = mvc_utils._convert_controller_name(
            "UserController", prefix_name="admin"
        )
        self.assertEqual(ref_name, "admin_user_controller")
        self.assertEqual(base_name, "user")

    def test_convert_controller_name_complex(self):
        # creates a mock plugin and mvc utils
        mock_plugin = MockPlugin()
        mvc_utils = system.MVCUtils(mock_plugin)

        # tests complex controller name conversion
        ref_name, base_name = mvc_utils._convert_controller_name(
            "UserAccountSettingsController"
        )
        self.assertEqual(ref_name, "user_account_settings_controller")
        self.assertEqual(base_name, "user_account_settings")


class RawModelTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Raw Model test case"

    def test_data_reference_model(self):
        # verifies data reference model has the flag
        self.assertEqual(system.DataReferenceModel.data_reference, True)

    def test_raw_model_creation(self):
        # creates a raw model subclass for testing
        class TestModel(system.RawModel):
            def __init__(self):
                self.name = "test"

        # creates an instance
        model = TestModel()
        self.assertEqual(model.name, "test")

    def test_raw_model_has_value(self):
        # creates a raw model subclass for testing
        class TestModel(system.RawModel):
            pass

        # creates an instance and sets a value
        model = TestModel()
        model.test_attr = "value"

        # verifies has_value works
        self.assertEqual(model.has_value("test_attr"), True)
        self.assertEqual(model.has_value("nonexistent"), False)

    def test_raw_model_get_value(self):
        # creates a raw model subclass for testing
        class TestModel(system.RawModel):
            pass

        # creates an instance and sets a value
        model = TestModel()
        model.test_attr = "test_value"

        # verifies get_value works
        result = model.get_value("test_attr")
        self.assertEqual(result, "test_value")

        # verifies get_value returns None for non-existent
        result = model.get_value("nonexistent")
        self.assertEqual(result, None)

    def test_raw_model_attach_detach(self):
        # creates a raw model subclass for testing
        class TestModel(system.RawModel):
            pass

        # creates an instance
        model = TestModel()

        # verifies attach and detach don't raise
        model.attach()
        model.detach()


class ExceptionsTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "MVC Utils Exceptions test case"

    def test_mvc_utils_exception(self):
        # creates a base exception
        exception = exceptions.MVCUtilsExceptionException()
        self.assertEqual(exception.message, None)

    def test_invalid_validation_method(self):
        # creates exception with message
        exception = exceptions.InvalidValidationMethod("unknown_method")
        self.assertEqual(exception.message, "unknown_method")
        self.assertEqual(str(exception), "Invalid validation method - unknown_method")

    def test_invalid_attribute_name(self):
        # creates exception with message
        exception = exceptions.InvalidAttributeName("123invalid")
        self.assertEqual(exception.message, "123invalid")
        self.assertEqual(str(exception), "Invalid attribute name - 123invalid")

    def test_insufficient_http_information(self):
        # creates exception with message
        exception = exceptions.InsufficientHTTPInformation("missing host header")
        self.assertEqual(exception.message, "missing host header")
        self.assertEqual(
            str(exception), "Insufficient HTTP information - missing host header"
        )

    def test_not_found_error(self):
        # creates exception with message
        exception = exceptions.NotFoundError("user not found")
        self.assertEqual(exception.message, "user not found")
        self.assertEqual(exception.status_code, 404)
        self.assertEqual(str(exception), "Not found error - user not found")

    def test_validation_error(self):
        # creates exception with message
        exception = exceptions.ValidationError("invalid email format")
        self.assertEqual(exception.message, "invalid email format")
        self.assertEqual(str(exception), "Validation error - invalid email format")

    def test_validation_error_with_variable(self):
        # creates exception with message and variable
        exception = exceptions.ValidationError("required field", variable="email")
        self.assertEqual(exception.message, "required field")
        self.assertEqual(exception.variable, "email")

    def test_model_validation_error(self):
        # creates exception with message
        exception = exceptions.ModelValidationError("validation failed")
        self.assertEqual(exception.message, "validation failed")

    def test_model_validation_error_with_model(self):
        # creates a mock model with validation errors
        mock_model = MockModelWithErrors()
        exception = exceptions.ModelValidationError(
            "validation failed", model=mock_model
        )
        self.assertEqual(exception.model, mock_model)

        # verifies string representation includes model info
        str_repr = str(exception)
        self.assertIn("Model validation error", str_repr)

    def test_model_validation_error_get_validation_s(self):
        # creates exception without model
        exception = exceptions.ModelValidationError("validation failed")
        result = exception.get_validation_s()
        self.assertEqual(result, "no model defined")

    def test_model_validation_error_get_validation_s_with_model(self):
        # creates a mock model with validation errors
        mock_model = MockModelWithErrors()
        exception = exceptions.ModelValidationError(
            "validation failed", model=mock_model
        )
        result = exception.get_validation_s()
        self.assertIn("email", result)
        self.assertIn("invalid format", result)

    def test_controller_validation_error(self):
        # creates exception with message
        exception = exceptions.ControllerValidationError("access denied")
        self.assertEqual(exception.message, "access denied")
        self.assertEqual(exception.status_code, 403)
        self.assertEqual(str(exception), "Controller validation error - access denied")

    def test_controller_validation_error_with_controller(self):
        # creates exception with controller
        mock_controller = MockController()
        exception = exceptions.ControllerValidationError(
            "permission denied", controller=mock_controller
        )
        self.assertEqual(exception.controller, mock_controller)

    def test_controller_validation_reason_failed(self):
        # creates exception with reasons
        reasons = ["invalid token", "expired session"]
        exception = exceptions.ControllerValidationReasonFailed(
            "authentication failed", reasons_list=reasons
        )
        self.assertEqual(exception.message, "authentication failed")
        self.assertEqual(exception.reasons_list, reasons)
        self.assertEqual(
            str(exception), "Controller validation reason error - authentication failed"
        )

    def test_validation_method_error(self):
        # creates exception with message
        exception = exceptions.ValidationMethodError("method not callable")
        self.assertEqual(exception.message, "method not callable")
        self.assertEqual(
            str(exception), "Validation method error - method not callable"
        )

    def test_model_apply_exception(self):
        # creates exception with message
        exception = exceptions.ModelApplyException("cannot apply data")
        self.assertEqual(exception.message, "cannot apply data")
        self.assertEqual(str(exception), "Model apply exception - cannot apply data")

    def test_exception_inheritance(self):
        # verifies all exceptions inherit from base
        exception_list = [
            exceptions.InvalidValidationMethod("test"),
            exceptions.InvalidAttributeName("test"),
            exceptions.InsufficientHTTPInformation("test"),
            exceptions.NotFoundError("test"),
            exceptions.ValidationError("test"),
            exceptions.ModelValidationError("test"),
            exceptions.ControllerValidationError("test"),
            exceptions.ControllerValidationReasonFailed("test"),
            exceptions.ValidationMethodError("test"),
            exceptions.ModelApplyException("test"),
        ]
        for exception in exception_list:
            self.assertTrue(
                isinstance(exception, exceptions.MVCUtilsExceptionException)
            )
            self.assertTrue(isinstance(exception, colony.ColonyException))

    def test_validation_error_inheritance(self):
        # verifies validation exceptions inherit from ValidationError
        exception_list = [
            exceptions.ModelValidationError("test"),
            exceptions.ControllerValidationError("test"),
            exceptions.ControllerValidationReasonFailed("test"),
        ]
        for exception in exception_list:
            self.assertTrue(isinstance(exception, exceptions.ValidationError))


class MockPlugin:
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


class MockController:
    def __init__(self):
        self.name = "test_controller"


class MockModelWithErrors:
    def __init__(self):
        self.validation_errors_map = {"email": ["invalid format", "required"]}
