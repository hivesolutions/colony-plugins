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

from . import controller


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
    def __init__(self, parameters=None, path_list=None):
        self.parameters = parameters or {}
        self.path_list = path_list or []


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


class MockTemplateFile(object):
    def __init__(self):
        self.assigns = {}
        self.process_methods_list = []
        self.variable_encoding = None

    def set_variable_encoding(self, variable_encoding):
        self.variable_encoding = variable_encoding

    def attach_process_methods(self, process_methods_list):
        self.process_methods_list = process_methods_list

    def assign(self, name, value):
        self.assigns[name] = value

    def process(self):
        return "processed"


class MockTemplateController(object):
    def __init__(self, user_acl=None):
        self._user_acl = user_acl
        self._session_attribute_names = []

    def get_process_method(self, request, method_name):
        return None

    def get_session_attribute(self, request, session_attribute_name):
        self._session_attribute_names.append(session_attribute_name)
        return self._user_acl

    def process_acl_values(
        self, acl_list, key, wildcard_value="*", maximum_value=10000
    ):
        return controller.process_acl_values(
            self,
            acl_list,
            key,
            wildcard_value=wildcard_value,
            maximum_value=maximum_value,
        )

    def validate_acl_session(
        self, request, key, value=10, session_attribute="user_acl"
    ):
        return controller.validate_acl_session(
            self, request, key, value=value, session_attribute=session_attribute
        )


class MockTemplateNode(object):
    def __init__(self, attributes=None, children=None):
        self.attributes = attributes or {}
        self.children = children or []
        self.accepted = False

    def get_attributes(self):
        return self.attributes

    def accept(self, visitor):
        self.accepted = True


class MockTemplateVisitor(object):
    def __init__(self, visit_childs=True):
        self.visit_childs = visit_childs

    def get_value(self, value):
        return value

    def get_literal_value(self, value):
        return value

    def _validate_accept_node(self, node, accept_node):
        return accept_node


class MockRedirectEntity(object):
    def __init__(self, object_id=1):
        self.object_id = object_id

    def _get_entity_class_pluralized(self, entity_class=None):
        return "mock_redirect_entities"

    def get_id_attribute_value(self):
        return self.object_id


class MockRedirectController(object):
    def __init__(self):
        self.redirect_target = None
        self.redirect_status_code = None

    def get_base_path(self, request):
        return controller.get_base_path(self, request)

    def get_mvc_path(self, request, delta_value=1):
        return controller.get_mvc_path(self, request, delta_value)

    def redirect_action(self, request, entity, **kwargs):
        controller.redirect_action(self, request, entity, **kwargs)

    def redirect_base_path(self, request, target, **kwargs):
        controller.redirect_base_path(self, request, target, **kwargs)

    def redirect_mvc_path(self, request, target, **kwargs):
        controller.redirect_mvc_path(self, request, target, **kwargs)

    def redirect(
        self,
        request,
        target,
        status_code=302,
        quote=False,
        keep=False,
        attributes_map=None,
    ):
        self.redirect_target = target
        self.redirect_status_code = status_code
