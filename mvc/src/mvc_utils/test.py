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

from . import utils
from . import mocks
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
            ValidatedDecoratorTestCase,
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
        mock_plugin = mocks.MockPlugin()
        mvc_utils = system.MVCUtils(mock_plugin)

        self.assertEqual(mvc_utils.models_modules_map, {})
        self.assertEqual(mvc_utils.package_path_models_map, {})
        self.assertEqual(mvc_utils.package_path_controllers_map, {})

    def test_get_models_not_found(self):
        mock_plugin = mocks.MockPlugin()
        mvc_utils = system.MVCUtils(mock_plugin)

        raised = False
        try:
            mvc_utils.get_models("nonexistent")
        except Exception:
            raised = True
        self.assertEqual(raised, True)

    def test_convert_controller_name(self):
        mock_plugin = mocks.MockPlugin()
        mvc_utils = system.MVCUtils(mock_plugin)

        ref_name, base_name = mvc_utils._convert_controller_name("MainController")
        self.assertEqual(ref_name, "main_controller")
        self.assertEqual(base_name, "main")

    def test_convert_controller_name_with_prefix(self):
        mock_plugin = mocks.MockPlugin()
        mvc_utils = system.MVCUtils(mock_plugin)

        ref_name, base_name = mvc_utils._convert_controller_name(
            "UserController", prefix_name="admin"
        )
        self.assertEqual(ref_name, "admin_user_controller")
        self.assertEqual(base_name, "user")

    def test_convert_controller_name_complex(self):
        mock_plugin = mocks.MockPlugin()
        mvc_utils = system.MVCUtils(mock_plugin)

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
        self.assertEqual(system.DataReferenceModel.data_reference, True)

    def test_raw_model_creation(self):
        class TestModel(system.RawModel):
            def __init__(self):
                self.name = "test"

        model = TestModel()
        self.assertEqual(model.name, "test")

    def test_raw_model_has_value(self):
        class TestModel(system.RawModel):
            pass

        model = TestModel()
        model.test_attr = "value"

        self.assertEqual(model.has_value("test_attr"), True)
        self.assertEqual(model.has_value("nonexistent"), False)

    def test_raw_model_get_value(self):
        class TestModel(system.RawModel):
            pass

        model = TestModel()
        model.test_attr = "test_value"

        result = model.get_value("test_attr")
        self.assertEqual(result, "test_value")

        result = model.get_value("nonexistent")
        self.assertEqual(result, None)

    def test_raw_model_attach_detach(self):
        class TestModel(system.RawModel):
            pass

        model = TestModel()
        model.attach()
        model.detach()


class ValidatedDecoratorTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Validated Decorator test case"

    def test_validated_calls_function(self):
        controller = mocks.MockValidatedController()

        @utils.validated()
        def action(self, request):
            return "success"

        request = mocks.MockRequest()
        result = action(controller, request)

        self.assertEqual(result, "success")

    def test_validated_raises_without_validate_method(self):
        controller = mocks.MockController()
        request = mocks.MockRequest()

        @utils.validated()
        def action(self, request):
            return "success"

        self.assertRaises(
            exceptions.ControllerValidationError, action, controller, request
        )

    def test_validated_pre_validation_failure_with_handler(self):
        controller = mocks.MockValidatedController(
            validate_reasons=["missing token"],
            validation_failed_result="handled",
        )

        @utils.validated()
        def action(self, request):
            return "success"

        request = mocks.MockRequest()
        result = action(controller, request)

        self.assertEqual(result, "handled")
        self.assertEqual(len(controller._validation_failed_calls), 1)
        self.assertEqual(
            controller._validation_failed_calls[0]["reasons"], ["missing token"]
        )

    def test_validated_pre_validation_failure_raises_without_handler(self):
        controller = mocks.MockValidatedControllerNoHandler(
            validate_reasons=["missing token"],
        )

        @utils.validated()
        def action(self, request):
            return "success"

        request = mocks.MockRequest()
        self.assertRaises(
            exceptions.ControllerValidationReasonFailed, action, controller, request
        )

    def test_validated_catches_controller_validation_error(self):
        controller = mocks.MockValidatedController(
            validation_failed_result="handled",
        )

        @utils.validated()
        def action(self, request):
            raise exceptions.ControllerValidationError("access denied")

        request = mocks.MockRequest()
        result = action(controller, request)

        self.assertEqual(result, "handled")
        self.assertEqual(len(controller._validation_failed_calls), 1)
        call = controller._validation_failed_calls[0]
        self.assertEqual(call["validation_parameters"], None)
        self.assertEqual(call["reasons"], "Controller validation error - access denied")

    def test_validated_catches_reason_failed_with_reasons_list(self):
        controller = mocks.MockValidatedController(
            validation_failed_result="handled",
        )

        @utils.validated()
        def action(self, request):
            raise exceptions.ControllerValidationReasonFailed(
                "auth failed",
                reasons_list=["expired token", "invalid scope"],
            )

        request = mocks.MockRequest()
        result = action(controller, request)

        self.assertEqual(result, "handled")
        self.assertEqual(len(controller._validation_failed_calls), 1)
        call = controller._validation_failed_calls[0]
        self.assertEqual(call["reasons"], ["expired token", "invalid scope"])

    def test_validated_reraises_without_handler(self):
        controller = mocks.MockValidatedControllerNoHandler()

        @utils.validated()
        def action(self, request):
            raise exceptions.ControllerValidationError("access denied")

        request = mocks.MockRequest()
        self.assertRaises(
            exceptions.ControllerValidationError, action, controller, request
        )

    def test_validated_reraises_when_should_call_false(self):
        controller = mocks.MockValidatedController(
            validation_failed_result="handled",
        )

        @utils.validated(call_validation_failed=False)
        def action(self, request):
            raise exceptions.ControllerValidationError("access denied")

        request = mocks.MockRequest()
        self.assertRaises(
            exceptions.ControllerValidationError, action, controller, request
        )

    def test_validated_sets_validated_flag(self):
        controller = mocks.MockValidatedController()

        @utils.validated()
        def action(self, request):
            return "success"

        request = mocks.MockRequest()
        action(controller, request)

        self.assertEqual(request.parameters.get("validated"), True)

    def test_validated_skips_validation_when_already_validated(self):
        call_count = []
        controller = mocks.MockValidatedController()

        original_validate = controller.validate

        def counting_validate(request, parameters, validation_parameters):
            call_count.append(True)
            return original_validate(request, parameters, validation_parameters)

        controller.validate = counting_validate

        @utils.validated()
        def action(self, request):
            return "success"

        request = mocks.MockRequest(parameters={"validated": True})
        action(controller, request)

        self.assertEqual(len(call_count), 0)

    def test_validated_preserves_function_name(self):
        controller = mocks.MockValidatedController()

        @utils.validated()
        def my_action(self, request):
            return "success"

        self.assertEqual(my_action.__name__, "my_action")


class ExceptionsTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "MVC Utils Exceptions test case"

    def test_mvc_utils_exception(self):
        exception = exceptions.MVCUtilsExceptionException()
        self.assertEqual(exception.message, None)

    def test_invalid_validation_method(self):
        exception = exceptions.InvalidValidationMethod("unknown_method")
        self.assertEqual(exception.message, "unknown_method")
        self.assertEqual(str(exception), "Invalid validation method - unknown_method")

    def test_invalid_attribute_name(self):
        exception = exceptions.InvalidAttributeName("123invalid")
        self.assertEqual(exception.message, "123invalid")
        self.assertEqual(str(exception), "Invalid attribute name - 123invalid")

    def test_insufficient_http_information(self):
        exception = exceptions.InsufficientHTTPInformation("missing host header")
        self.assertEqual(exception.message, "missing host header")
        self.assertEqual(
            str(exception), "Insufficient HTTP information - missing host header"
        )

    def test_not_found_error(self):
        exception = exceptions.NotFoundError("user not found")
        self.assertEqual(exception.message, "user not found")
        self.assertEqual(exception.status_code, 404)
        self.assertEqual(str(exception), "Not found error - user not found")

    def test_validation_error(self):
        exception = exceptions.ValidationError("invalid email format")
        self.assertEqual(exception.message, "invalid email format")
        self.assertEqual(str(exception), "Validation error - invalid email format")

    def test_validation_error_with_variable(self):
        exception = exceptions.ValidationError("required field", variable="email")
        self.assertEqual(exception.message, "required field")
        self.assertEqual(exception.variable, "email")

    def test_model_validation_error(self):
        exception = exceptions.ModelValidationError("validation failed")
        self.assertEqual(exception.message, "validation failed")

    def test_model_validation_error_with_model(self):
        mock_model = mocks.MockModelWithErrors()
        exception = exceptions.ModelValidationError(
            "validation failed", model=mock_model
        )
        self.assertEqual(exception.model, mock_model)

        str_repr = str(exception)
        self.assertIn("Model validation error", str_repr)

    def test_model_validation_error_get_validation_s(self):
        exception = exceptions.ModelValidationError("validation failed")
        result = exception.get_validation_s()
        self.assertEqual(result, "no model defined")

    def test_model_validation_error_get_validation_s_with_model(self):
        mock_model = mocks.MockModelWithErrors()
        exception = exceptions.ModelValidationError(
            "validation failed", model=mock_model
        )
        result = exception.get_validation_s()
        self.assertIn("email", result)
        self.assertIn("invalid format", result)

    def test_controller_validation_error(self):
        exception = exceptions.ControllerValidationError("access denied")
        self.assertEqual(exception.message, "access denied")
        self.assertEqual(exception.status_code, 403)
        self.assertEqual(str(exception), "Controller validation error - access denied")

    def test_controller_validation_error_with_controller(self):
        mock_controller = mocks.MockController()
        exception = exceptions.ControllerValidationError(
            "permission denied", controller=mock_controller
        )
        self.assertEqual(exception.controller, mock_controller)

    def test_controller_validation_reason_failed(self):
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
        exception = exceptions.ValidationMethodError("method not callable")
        self.assertEqual(exception.message, "method not callable")
        self.assertEqual(
            str(exception), "Validation method error - method not callable"
        )

    def test_model_apply_exception(self):
        exception = exceptions.ModelApplyException("cannot apply data")
        self.assertEqual(exception.message, "cannot apply data")
        self.assertEqual(str(exception), "Model apply exception - cannot apply data")

    def test_exception_inheritance(self):
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
        exception_list = [
            exceptions.ModelValidationError("test"),
            exceptions.ControllerValidationError("test"),
            exceptions.ControllerValidationReasonFailed("test"),
        ]
        for exception in exception_list:
            self.assertTrue(isinstance(exception, exceptions.ValidationError))
