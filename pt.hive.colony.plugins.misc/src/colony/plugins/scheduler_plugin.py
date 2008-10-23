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

import colony.plugins.plugin_system
import colony.plugins.decorators

class SchedulerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Scheduler plugin
    """

    id = "pt.hive.colony.plugins.misc.scheduler"
    name = "Scheduler Plugin"
    short_name = "Scheduler"
    description = "A Plugin to manage the scheduling of tasks"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["scheduler", "thread"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.guid", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.console", "1.0.0")]
    events_handled = []
    events_registrable = []

    scheduler = None

    guid_plugin = None
    main_console_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.scheduler.scheduler_system
        self.scheduler = misc.scheduler.scheduler_system.Scheduler(self)
        self.scheduler.load_scheduler()

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)    

        #self.register_console_script_task(5, "showall")

        self.register_console_script_task_recursive(5, [0, 0, 1, 0, 0], "show 1")

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.scheduler.unload_scheduler()

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.misc.scheduler", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def register_console_script_task(self, time, console_script):
        self.scheduler.register_console_script_task(time, console_script)

    def register_console_script_task_date_time(self, date_time, console_script):
        self.scheduler.register_console_script_task_date_time(date_time, console_script)

    def register_console_script_task_recursive(self, time, recursion_list, console_script):
        self.scheduler.register_console_script_task_recursive(time, recursion_list, console_script)

    def get_guid_plugin(self):
        return self.guid_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.guid")
    def set_guid_plugin(self, guid_plugin):
        self.guid_plugin = guid_plugin

    def get_main_console_plugin(self):
        return self.main_console_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.main.console")
    def set_main_console_plugin(self, main_console_plugin):
        self.main_console_plugin = main_console_plugin
