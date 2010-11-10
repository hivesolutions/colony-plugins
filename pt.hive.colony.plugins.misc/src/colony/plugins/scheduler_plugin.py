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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class SchedulerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Scheduler plugin.
    """

    id = "pt.hive.colony.plugins.misc.scheduler"
    name = "Scheduler Plugin"
    short_name = "Scheduler"
    description = "A plugin to manage the scheduling of tasks"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/misc/scheduler/resources/baf.xml"}
    capabilities = ["scheduler", "thread", "console_command_extension", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.guid", "1.0.0"),
                    colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.console", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["misc.scheduler.console_scheduler",
                    "misc.scheduler.scheduler_system"]

    scheduler = None
    console_scheduler = None

    guid_plugin = None
    main_console_plugin = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.scheduler.scheduler_system
        import misc.scheduler.console_scheduler
        self.scheduler = misc.scheduler.scheduler_system.Scheduler(self)
        self.console_scheduler = misc.scheduler.console_scheduler.ConsoleScheduler(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

        # loads the scheduler
        self.scheduler.load_scheduler()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)
        self.scheduler.unload_scheduler()

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.misc.scheduler", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.set_configuration_property("pt.hive.colony.plugins.misc.scheduler", "1.0.0")
    def set_configuration_property(self, property_name, property):
        colony.base.plugin_system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property("pt.hive.colony.plugins.misc.scheduler", "1.0.0")
    def unset_configuration_property(self, property_name):
        colony.base.plugin_system.Plugin.unset_configuration_property(self, property_name)

    def get_console_extension_name(self):
        return self.console_scheduler.get_console_extension_name()

    def get_all_commands(self):
        return self.console_scheduler.get_all_commands()

    def get_handler_command(self, command):
        return self.console_scheduler.get_handler_command(command)

    def get_help(self):
        return self.console_scheduler.get_help()

    def register_task(self, task, time):
        return self.scheduler.register_task(task, time)

    def register_task_absolute(self, task, absolute_time):
        return self.scheduler.register_task_absolute(task, absolute_time)

    def register_task_date_time(self, task, date_time):
        return self.scheduler.register_task_date_time(task, date_time)

    def register_task_date_time_absolute(self, task, absolute_date_time):
        return self.scheduler.register_task_date_time_absolute(task, absolute_date_time)

    def register_task_recursive(self, task, time, recursion_list):
        return self.scheduler.register_task_recursive(task, time, recursion_list)

    def register_task_absolute_recursive(self, task, absolute_time, recursion_list):
        self.scheduler.register_task_absolute_recursive(task, absolute_time, recursion_list)

    def register_task_date_time_recursive(self, task, date_time, recursion_list):
        return self.scheduler.register_task_date_time_recursive(task, date_time, recursion_list)

    def register_task_date_time_absolute_recursive(self, task, absolute_date_time, recursion_list):
        return self.scheduler.register_task_date_time_absolute_recursive(task, absolute_date_time, recursion_list)

    def get_task_class(self):
        return self.scheduler.get_task_class()

    def get_guid_plugin(self):
        return self.guid_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.guid")
    def set_guid_plugin(self, guid_plugin):
        self.guid_plugin = guid_plugin

    def get_main_console_plugin(self):
        return self.main_console_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.console")
    def set_main_console_plugin(self, main_console_plugin):
        self.main_console_plugin = main_console_plugin

    @colony.base.decorators.set_configuration_property_method("startup_configuration")
    def startup_configuration_set_configuration_property(self, property_name, property):
        self.scheduler.set_startup_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("startup_configuration")
    def startup_configuration_unset_configuration_property(self, property_name):
        self.scheduler.unset_startup_configuration_property()
