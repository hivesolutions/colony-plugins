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

import colony


class DiagnosticsPlugin(colony.Plugin):
    """
    The main class for plugin responsible for the gathering
    and processing of diagnostics information to be used
    both for profiling and debugging.
    """

    id = "pt.hive.colony.plugins.diagnostics"
    name = "Diagnostics Engine"
    description = "Diagnostics Engine Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT,
    ]
    capabilities = ["diagnostics"]
    main_modules = ["diagnostics"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import diagnostics

        self.diagnostics = diagnostics.Diagnostics(self)
        self.diagnostics.start()

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.diagnostics.stop()

    def get_data(self):
        return self.diagnostics.get_data()
