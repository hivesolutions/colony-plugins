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

import colony

class SchedulerPlugin(colony.Plugin):
    """
    The main class for the Scheduler plugin.
    """

    id = "pt.hive.colony.plugins.misc.scheduler"
    name = "Scheduler"
    description = "A plugin to manage the scheduling of tasks"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "main",
        "scheduler",
        "console_command_extension"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.misc.guid"),
        colony.PluginDependency("pt.hive.colony.plugins.console")
    ]
    main_modules = [
        "scheduler_c.console",
        "scheduler_c.exceptions",
        "scheduler_c.system"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import scheduler_c
        self.system = scheduler_c.Scheduler(self)
        self.console = scheduler_c.ConsoleScheduler(self)
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.Plugin.end_load_plugin(self)
        self.system.load_scheduler()

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.system.unload_scheduler()
        self.release_ready_semaphore()

    def end_unload_plugin(self):
        colony.Plugin.end_unload_plugin(self)
        self.release_ready_semaphore()

    @colony.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.Plugin.set_configuration_property(self, property_name, property)

    @colony.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.Plugin.unset_configuration_property(self, property_name)

    def get_console_extension_name(self):
        return self.console.get_console_extension_name()

    def get_commands_map(self):
        return self.console.get_commands_map()

    def register_task(self, task, time):
        return self.system.register_task(task, time)

    def register_task_absolute(self, task, absolute_time):
        return self.system.register_task_absolute(task, absolute_time)

    def register_task_date_time(self, task, date_time):
        return self.system.register_task_date_time(task, date_time)

    def register_task_date_time_absolute(self, task, absolute_date_time):
        return self.system.register_task_date_time_absolute(task, absolute_date_time)

    def register_task_recursive(self, task, time, recursion_list):
        return self.system.register_task_recursive(task, time, recursion_list)

    def register_task_absolute_recursive(self, task, absolute_time, recursion_list):
        return self.system.register_task_absolute_recursive(task, absolute_time, recursion_list)

    def register_task_date_time_recursive(self, task, date_time, recursion_list):
        return self.system.register_task_date_time_recursive(task, date_time, recursion_list)

    def register_task_date_time_absolute_recursive(self, task, absolute_date_time, recursion_list):
        return self.system.register_task_date_time_absolute_recursive(task, absolute_date_time, recursion_list)

    def unregister_task(self, task):
        return self.system.unregister_task(task)

    def get_task_class(self):
        """
        Retrieves the class that represents
        a task in the current scope.

        @rtype: Class
        @return: The task class for the current scope.
        """

        return self.system.get_task_class()

    @colony.set_configuration_property_method("startup_configuration")
    def startup_configuration_set_configuration_property(self, property_name, property):
        self.system.set_startup_configuration_property(property)

    @colony.unset_configuration_property_method("startup_configuration")
    def startup_configuration_unset_configuration_property(self, property_name):
        self.system.unset_startup_configuration_property()
