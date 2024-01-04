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

import time

import colony

class Diagnostics(colony.System):

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.data = dict()
        self.state = dict()
        self.diagnostics = colony.conf("DIAGNOSTICS", False, cast = bool)

    def start(self):
        if not self.diagnostics: return
        colony.register_g("request.begin", self.request_begin)
        colony.register_g("request.end", self.request_end)
        colony.register_g("template.begin", self.template_begin)
        colony.register_g("template.end", self.template_end)
        colony.register_g("orm.begin", self.orm_begin)
        colony.register_g("orm.end", self.orm_end)
        colony.register_g("sql.executed", self.sql_executed)

    def stop(self):
        if not self.diagnostics: return
        colony.unregister_g("request.begin", self.request_begin)
        colony.unregister_g("request.end", self.request_end)
        colony.unregister_g("template.begin", self.template_begin)
        colony.unregister_g("template.end", self.template_end)
        colony.unregister_g("orm.begin", self.orm_begin)
        colony.unregister_g("orm.end", self.orm_end)
        colony.unregister_g("sql.executed", self.sql_executed)

    def get_data(self):
        return self.data

    def push_state(self, name, value):
        stack = self.state.get(name, [])
        stack.append(value)
        self.state[name] = stack

    def pop_state(self, name):
        stack = self.state[name]
        return stack.pop()

    def peek_state(self, name, default = None):
        stack = self.state.get(name, None)
        if not stack: return default
        return stack[-1]

    def add_operation(self, name, target, data):
        state = self.peek_state(target)
        if not state: return False
        totals = state["totals"]
        operations = state["operations"]
        sequence = operations.get(name, [])
        sequence.append(data)
        total = totals.get(name, 0)
        time = data.get("time", 0)
        total += time
        operations[name] = sequence
        totals[name] = total
        return True

    def try_operation(self, name, targets, data):
        for target in targets:
            result = self.add_operation(name, target, data)
            if result: break

    def set_time(self, data):
        initial = data["initial"]
        final = time.time()
        delta = int((final - initial) * 1000)
        data["final"] = final
        data["time"] = delta

    def request_begin(self, request):
        identifier = id(request)
        requests = self.data.get("requests", {})
        requests_l = self.data.get("requests_l", [])
        data = dict(
            id = identifier,
            initial = time.time(),
            method = request.get_method(),
            path = request.get_path(),
            operations = dict(),
            totals = dict()
        )
        requests[identifier] = data
        requests_l.append(data)
        self.data["requests"] = requests
        self.data["requests_l"] = requests_l
        self.push_state("request", data)

    def request_end(self, request):
        identifier = id(request)
        requests = self.data.get("requests", {})
        data = requests[identifier]
        data["code"] = request.get_status_code() or 500
        self.set_time(data)
        self.pop_state("request")

    def template_begin(self, identifier):
        templates = self.data.get("templates", {})
        templates_l = self.data.get("templates_l", [])
        data = dict(
            id = identifier,
            initial = time.time(),
            operations = dict(),
            totals = dict()
        )
        templates[identifier] = data
        templates_l.append(data)
        self.data["templates"] = templates
        self.data["templates_l"] = templates_l
        self.push_state("template", data)

    def template_end(self, identifier, template_file = None):
        templates = self.data.get("templates", {})
        data = templates[identifier]
        data["file_path"] = template_file and template_file.file_path
        self.set_time(data)
        self.pop_state("template")
        self.try_operation("template", ("template", "request"), data)

    def orm_begin(self, identifier, operation, options = None):
        orms = self.data.get("orms", {})
        orms_l = self.data.get("orms_l", [])
        data = dict(
            id = identifier,
            initial = time.time(),
            operation = operation,
            operations = dict(),
            totals = dict()
        )
        orms[identifier] = data
        orms_l.append(data)
        self.data["orms"] = orms
        self.data["orms_l"] = orms_l
        self.push_state("orm", data)

    def orm_end(self, identifier, count = None):
        orms = self.data.get("orms", {})
        data = orms[identifier]
        data["count"] = count
        self.set_time(data)
        self.pop_state("orm")
        self.try_operation("orm", ("orm", "template", "request"), data)

    def sql_executed(self, query, engine, time):
        is_bytes = type(query) == colony.legacy.BYTES
        query = query.decode("utf-8") if is_bytes else query
        data = dict(
            query = query,
            engine = engine,
            time = time
        )
        sql = self.data.get("sql", [])
        sql.append(data)
        self.data["sql"] = sql
        self.try_operation("sql", ("orm", "template", "request"), data)
