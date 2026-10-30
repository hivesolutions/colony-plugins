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


class MockSerializer(object):
    def __init__(self, mime_type="application/json"):
        self._mime_type = mime_type

    def dumps(self, value):
        return "serialized"

    def get_mime_type(self):
        return self._mime_type


class MockSerializedController(object):
    def __init__(self):
        self.status_code = None
        self.contents = None
        self.messages = []

    def debug(self, message):
        self.messages.append(message)

    def warning(self, message):
        self.messages.append(message)

    def set_status_code(self, request, status_code):
        self.status_code = status_code

    def set_contents(self, request, contents, content_type=None):
        self.contents = contents

    def get_exception_map(self, exception, request):
        return dict(
            exception=dict(message=str(exception), traceback=None),
            environment=dict(method="GET"),
        )


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


class MockEntityManager(object):
    def __init__(self, entities=None):
        self.entities = entities or dict()
        self.calls = []

    def get_entity(self, entity_name):
        return self.entities.get(entity_name, None)

    def normalize_options(self, options):
        eager = options.get("eager", None)
        if type(eager) in (list, tuple):
            options["eager"] = dict([(name, dict()) for name in eager])
        return options

    def begin(self):
        self.calls.append("begin")

    def commit(self):
        self.calls.append("commit")

    def rollback(self):
        self.calls.append("rollback")


class MockEntity(object):
    data_reference = False
    _entity_manager = MockEntityManager()
    _names = ()
    _targets = dict()

    @classmethod
    def is_reference(cls):
        return cls.data_reference

    @classmethod
    def has_name(cls, name):
        return name in cls._names

    @classmethod
    def get_target(cls, relation_name):
        return cls._targets.get(relation_name, cls)

    @classmethod
    def _cast_value(cls, name, value):
        if not name in cls._names:
            return None
        return value


class MockAddress(MockEntity):
    _names = ("object_id", "street")


class MockAddressReference(MockEntity):
    data_reference = True


class MockPerson(MockEntity):
    _names = ("object_id", "name", "age", "address")
    _targets = dict(address=MockAddress)


class MockPersonReference(MockEntity):
    data_reference = True


class MockCompany(MockEntity):
    _names = ("object_id", "name", "address", "owner")
    _targets = dict(address=MockAddressReference, owner=MockPersonReference)


class MockDeleteEntity(object):
    def __init__(self, failure=None):
        self._entity_manager = MockEntityManager()
        self._failure = failure
        self.calls = []
        self.persist_types = []
        self.exceptions = []
        self.entity_managers = []

    def pre_delete(self, persist_type):
        self._call("pre_delete", persist_type)

    def pre_remove(self, persist_type):
        self._call("pre_remove", persist_type)

    def on_delete(self, persist_type):
        self._call("on_delete", persist_type)

    def on_remove(self, persist_type):
        self._call("on_remove", persist_type)

    def fail_delete(self, persist_type, exception):
        self._call("fail_delete", persist_type)
        self.exceptions.append(exception)

    def fail_remove(self, persist_type, exception):
        self._call("fail_remove", persist_type)
        self.exceptions.append(exception)

    def post_delete(self, persist_type):
        self._call("post_delete", persist_type)

    def post_remove(self, persist_type):
        self._call("post_remove", persist_type)

    def remove(self, entity_manager=None):
        self.entity_managers.append(entity_manager)
        self._call("remove")

    def _call(self, name, persist_type=None):
        self.calls.append(name)
        if not persist_type == None:
            self.persist_types.append(persist_type)
        if name == self._failure:
            raise ValueError("invalid value")


class MockDeleteEntityNoHooks(object):
    def __init__(self, failure=None):
        self._entity_manager = MockEntityManager()
        self._failure = failure
        self.calls = []

    def remove(self, entity_manager=None):
        self.calls.append("remove")
        if self._failure == "remove":
            raise ValueError("invalid value")


class MockDeleteEntityStoreHooks(MockDeleteEntity):
    def on_store(self, persist_type):
        self._call("on_store", persist_type)

    def on_save(self, persist_type):
        self._call("on_save", persist_type)

    def on_update(self, persist_type):
        self._call("on_update", persist_type)
