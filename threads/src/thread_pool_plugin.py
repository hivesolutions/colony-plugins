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


class ThreadPoolPlugin(colony.Plugin):
    """
    The main class for the Thread Pool plugin
    """

    id = "pt.hive.colony.plugins.threads.pool"
    name = "Thread Pool"
    description = "Thread Pool Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT,
    ]
    capabilities = ["threads", "thread_pool", "system_information"]
    main_modules = ["thread_pool"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import thread_pool

        self.system = thread_pool.ThreadPool(self)

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.system.unload()

    def create_new_thread_pool(
        self,
        name,
        description,
        number_threads,
        scheduling_algorithm,
        maximum_number_threads,
    ):
        return self.system.create_new_thread_pool(
            name,
            description,
            number_threads,
            scheduling_algorithm,
            maximum_number_threads,
        )

    def get_thread_task_descriptor_class(self):
        return self.system.get_thread_task_descriptor_class()

    def get_system_information(self):
        """
        Retrieves the system information map, containing structured
        information to be visible using presentation viewers.

        :rtype: Dictionary
        :return: The system information map.
        """

        return self.system.get_system_information()
