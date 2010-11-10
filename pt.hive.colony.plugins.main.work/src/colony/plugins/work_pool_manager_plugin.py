#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision: 9011 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-06-22 09:36:13 +0100 (ter, 22 Jun 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class WorkPoolManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Work Pool Manager plugin
    """

    id = "pt.hive.colony.plugins.main.work.work_pool_manager"
    name = "Work Pool Manager Plugin"
    short_name = "Work Pool Manager"
    description = "Work Pool Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT,
                 colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/main_work/work_pool_manager/resources/baf.xml"}
    capabilities = ["work_pool_manager", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.threads.thread_pool_manager", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["main_work.work_pool_manager.work_pool_manager_algorithms",
                    "main_work.work_pool_manager.work_pool_manager_system"]

    work_pool_manager = None

    thread_pool_manager_plugin = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global main_work
        import main_work.work_pool_manager.work_pool_manager_system
        self.work_pool_manager = main_work.work_pool_manager.work_pool_manager_system.WorkPoolManager(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)
        self.work_pool_manager.unload()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.main.work.work_pool_manager", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_new_work_pool(self, name, description, work_processing_task_class, work_processing_task_arguments, number_threads, scheduling_algorithm, maximum_number_threads, maximum_number_works_thread, work_scheduling_algorithm):
        return self.work_pool_manager.create_new_work_pool(name, description, work_processing_task_class, work_processing_task_arguments, number_threads, scheduling_algorithm, maximum_number_threads, maximum_number_works_thread, work_scheduling_algorithm)

    def get_thread_pool_manager_plugin(self):
        return self.thread_pool_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.threads.thread_pool_manager")
    def set_thread_pool_manager_plugin(self, thread_pool_manager_plugin):
        self.thread_pool_manager_plugin = thread_pool_manager_plugin
