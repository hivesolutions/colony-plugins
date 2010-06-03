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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class TaskManagerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Task Manager plugin
    """

    id = "pt.hive.colony.plugins.main.tasks.task_manager"
    name = "Task Manager Plugin"
    short_name = "Task Manager"
    description = "Task Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/main_tasks/task_manager/resources/baf.xml"}
    capabilities = ["task_manager", "task_information", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.threads.thread_pool_manager", "1.0.0")]
    events_handled = ["task_information_changed"]
    events_registrable = []

    task_manager = None

    thread_pool_manager_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_tasks
        import main_tasks.task_manager.task_manager_system
        self.task_manager = main_tasks.task_manager.task_manager_system.TaskManager(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

        # starts the task manager
        self.task_manager.start()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.main.tasks.task_manager", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_new_task(self, name, description, task_creation_handler):
        return self.task_manager.create_new_task(name, description, task_creation_handler)

    def get_thread_pool_manager_plugin(self):
        return self.thread_pool_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.threads.thread_pool_manager")
    def set_thread_pool_manager_plugin(self, thread_pool_manager_plugin):
        self.thread_pool_manager_plugin = thread_pool_manager_plugin
