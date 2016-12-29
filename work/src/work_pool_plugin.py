#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class WorkPoolPlugin(colony.Plugin):
    """
    The main class for the Work Pool plugin
    """

    id = "pt.hive.colony.plugins.work.pool"
    name = "Work Pool"
    description = "Work Pool Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "work_pool",
        "system_information"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.threads.pool")
    ]
    main_modules = [
        "work_pool"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import work_pool
        self.system = work_pool.WorkPool(self)

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.system.unload()

    def create_new_work_pool(
        self,
        name,
        description,
        work_processing_task_class,
        work_processing_task_arguments,
        number_threads, scheduling_algorithm,
        maximum_number_threads,
        maximum_number_works_thread,
        work_scheduling_algorithm
    ):
        return self.system.create_new_work_pool(
            name,
            description,
            work_processing_task_class,
            work_processing_task_arguments,
            number_threads,
            scheduling_algorithm,
            maximum_number_threads,
            maximum_number_works_thread,
            work_scheduling_algorithm
        )

    def get_system_information(self):
        """
        Retrieves the system information map, containing structured
        information to be visible using presentation viewers.

        @rtype: Dictionary
        @return: The system information map.
        """

        return self.system.get_system_information()
