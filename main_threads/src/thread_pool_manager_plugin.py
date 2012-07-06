#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system

class ThreadPoolManagerPlugin(colony.base.system.Plugin):
    """
    The main class for the Thread Pool Manager plugin
    """

    id = "pt.hive.colony.plugins.main.threads.thread_pool_manager"
    name = "Thread Pool Manager"
    description = "Thread Pool Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT,
        colony.base.system.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "threads",
        "thread_pool_manager",
        "system_information"
    ]
    main_modules = [
        "main_threads.thread_pool_manager.thread_pool_manager_system"
    ]

    thread_pool_manager = None
    """ The thread pool manager """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import main_threads.thread_pool_manager.thread_pool_manager_system
        self.thread_pool_manager = main_threads.thread_pool_manager.thread_pool_manager_system.ThreadPoolManager(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)

        # unloads the thread pool manager
        self.thread_pool_manager.unload()

    def end_unload_plugin(self):
        colony.base.system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def create_new_thread_pool(self, name, description, number_threads, scheduling_algorithm, maximum_number_threads):
        return self.thread_pool_manager.create_new_thread_pool(name, description, number_threads, scheduling_algorithm, maximum_number_threads)

    def get_thread_task_descriptor_class(self):
        return self.thread_pool_manager.get_thread_task_descriptor_class()

    def get_system_information(self):
        """
        Retrieves the system information map, containing structured
        information to be visible using presentation viewers.

        @rtype: Dictionary
        @return: The system information map.
        """

        return self.thread_pool_manager.get_system_information()
