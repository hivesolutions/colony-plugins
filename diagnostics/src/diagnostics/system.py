#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

import colony

class Diagnostics(colony.System):

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.data = dict()
        self.currents = dict()
        self.diagnostics = colony.conf("DIAGNOSTICS", False, cast = bool)

    def start(self):
        if not self.diagnostics: return
        colony.register_g("request.start", self.request_start)
        colony.register_g("request.stop", self.request_stop)
        colony.register_g("sql.executed", self.sql_executed)

    def stop(self):
        if not self.diagnostics: return
        colony.unregister_g("request.start", self.request_start)
        colony.unregister_g("request.stop", self.request_stop)
        colony.unregister_g("sql.executed", self.sql_executed)

    def get_data(self):
        return self.data

    def request_start(self, request):
        requests = self.data.get("requests", {})
        requests_l = self.data.get("requests_l", [])
        data = dict(
            id = request._generation_time,
            initial = request._generation_time,
            path = request.get_path(),
            operations = dict()
        )
        requests[request] = data
        requests_l.append(request)
        self.data["requests"] = requests
        self.data["requests_l"] = requests_l
        self.currents["request"] = data

    def request_stop(self, request):
        requests = self.data.get("requests", {})
        data = requests[request]
        initial = data["initial"]
        final = time.time()
        delta = int((final - initial) * 1000)
        data["final"] = final
        data["time"] = delta
        self.currents["request"] = None

        import pprint
        pprint.pprint(data)

    def sql_executed(self, query, time, engine):
        data = dict(
            query = query,
            time = time,
            engine = engine
        )
        sql = self.data.get("sql", [])
        sql.append(data)
        self.data["sql"] = sql

        request_data = self.currents.get("request", None)
        if not request_data: return

        operations = request_data["operations"]
        sql = operations.get("sql", [])
        sql.append(data)
        operations["sql"] = sql
