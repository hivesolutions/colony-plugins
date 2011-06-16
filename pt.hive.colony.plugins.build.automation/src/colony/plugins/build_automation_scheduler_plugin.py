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

class BuildAutomationSchedulerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Build Automation Scheduler plugin
    """

    id = "pt.hive.colony.plugins.build.automation.scheduler"
    name = "Build Automation Scheduler Plugin"
    short_name = "Build Automation Scheduler"
    description = "A plugin to manage the build automation scheduling"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/build_automation/scheduler/resources/baf.xml"
    }
    capabilities = [
        "build_automation_scheduler",
        "_console_command_extension",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.build.automation", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.scheduler", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.messaging.manager", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.guid", "1.0.0")
    ]
    main_modules = [
        "build_automation.scheduler.build_automation_scheduler_system",
        "build_automation.scheduler.console_build_automation_scheduler"
    ]

    build_automation_scheduler = None
    """ The build automation scheduler """

    console_build_automation_scheduler = None
    """ The console build automation scheduler """

    build_automation_plugin = None
    """ The build automation plugin """

    scheduler_plugin = None
    """ The scheduler plugin """

    messaging_manager_plugin = None
    """ The messaging manager plugin """

    guid_plugin = None
    """ The guid plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import build_automation.scheduler.build_automation_scheduler_system
        import build_automation.scheduler.console_build_automation_scheduler
        self.build_automation_scheduler = build_automation.scheduler.build_automation_scheduler_system.BuildAutomationScheduler(self)
        self.console_build_automation_scheduler = build_automation.scheduler.console_build_automation_scheduler.ConsoleBuildAutomationScheduler(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_console_extension_name(self):
        return self.console_build_automation_scheduler.get_console_extension_name()

    def get_commands_map(self):
        return self.console_build_automation_scheduler.get_commands_map()

    def get_build_automation_plugin(self):
        return self.build_automation_plugin

    def register_build_automation_plugin_id(self, plugin_id, date_time, recursion_list):
        return self.build_automation_scheduler.register_build_automation_plugin_id(plugin_id, date_time, recursion_list)

    def register_build_automation_plugin_id_version(self, plugin_id, plugin_version, date_time, recursion_list):
        return self.build_automation_scheduler.register_build_automation_plugin_id(plugin_id, plugin_version, date_time, recursion_list)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.build.automation")
    def set_build_automation_plugin(self, build_automation_plugin):
        self.build_automation_plugin = build_automation_plugin

    def get_scheduler_plugin(self):
        return self.scheduler_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.scheduler")
    def set_scheduler_plugin(self, scheduler_plugin):
        self.scheduler_plugin = scheduler_plugin

    def get_messaging_manager_plugin(self):
        return self.messaging_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.messaging.manager")
    def set_messaging_manager_plugin(self, messaging_manager_plugin):
        self.messaging_manager_plugin = messaging_manager_plugin

    def get_guid_plugin(self):
        return self.guid_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.guid")
    def set_guid_plugin(self, guid_plugin):
        self.guid_plugin = guid_plugin
