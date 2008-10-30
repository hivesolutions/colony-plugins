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

class BuildAutomationPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Build Automation plugin
    """

    id = "pt.hive.colony.plugins.build.automation"
    name = "Build Automation Plugin"
    short_name = "Build Automation"
    description = "A plugin to manage complete build automation"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["build_automation", "console_command_extension"]
    capabilities_allowed = ["build_automation_extension", "build_automation_item"]
    dependencies = []
    events_handled = []
    events_registrable = []

    build_automation = None
    console_build_automation = None

    build_automation_extension_plugins = []
    build_automation_item_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global build_automation
        import build_automation.automation.build_automation_system
        import build_automation.automation.console_build_automation
        self.build_automation = build_automation.automation.build_automation_system.BuildAutomation(self)
        self.console_build_automation = build_automation.automation.console_build_automation.ConsoleBuildAutomation(self)

        self.build_automation_extension_plugins = []
        self.build_automation_item_plugins = []

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.build.automation", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.build.automation", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_all_commands(self):
        return self.console_build_automation.get_all_commands()

    def get_handler_command(self, command):
        return self.console_build_automation.get_handler_command(command)

    def get_help(self):
        return self.console_build_automation.get_help()

    def run_automation_plugin_id(self, plugind_id):
        self.build_automation.run_automation_plugin_id_version(plugin_id)

    def run_automation_plugin_id_plugin_version(self, plugind_id, plugin_version):
        self.build_automation.run_automation_plugin_id_version(plugin_id, plugin_version)

    @colony.plugins.decorators.load_allowed_capability("build_automation_extension")
    def build_automation_extension_load_allowed(self, plugin, capability):
        self.build_automation_extension_plugins.append(plugin)

    @colony.plugins.decorators.load_allowed_capability("build_automation_item")
    def build_automation_item_load_allowed(self, plugin, capability):
        self.build_automation_item_plugins.append(plugin)
        self.build_automation.load_build_automation_item_plugin(plugin)

    @colony.plugins.decorators.unload_allowed_capability("build_automation_extension")
    def build_automation_extension_unload_allowed(self, plugin, capability):
        self.build_automation_extension_plugins.remove(plugin)

    @colony.plugins.decorators.unload_allowed_capability("build_automation_item")
    def build_automation_item_unload_allowed(self, plugin, capability):
        self.build_automation_item_plugins.remove(plugin)
        self.build_automation.unload_build_automation_item_plugin(plugin)
