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

class WorkPoolDummyPlugin(colony.Plugin):
    """
    The main class for the Work Pool Dummy plugin
    """

    id = "pt.hive.colony.plugins.work.pool_dummy"
    name = "Work Pool Dummy"
    description = "Work Pool Dummy Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "startup"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.work.pool")
    ]
    main_modules = [
        "work_pool_dummy"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import work_pool_dummy
        self.system = work_pool_dummy.WorkPoolDummy(self)

    def end_load_plugin(self):
        colony.Plugin.end_load_plugin(self)
        self.system.start_pool()

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.system.stop_pool()
