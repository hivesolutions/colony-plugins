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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class MainTestPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Test Main plugin
    """

    id = "pt.hive.colony.plugins.main.test"
    name = "Test Main Plugin"
    short_name = "Test Main"
    description = "Test Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["test", "console_command_extension"]
    capabilities_allowed = ["test_manager", "test_case", "test_case_bundle", "plugin_test_case", "plugin_test_case_bundle"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.code_coverage", "1.0.0")]
    events_handled = []
    events_registrable = []

    main_test = None
    console_test = None

    test_case_plugins = []
    test_case_bundle_plugins = []
    plugin_test_case_plugins = []
    plugin_test_case_bundle_plugins = []

    code_coverage_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_test
        import main_test.test.main_test_system
        import main_test.test.console_test
        self.main_test = main_test.test.main_test_system.MainTest(self)
        self.console_test = main_test.test.console_test.ConsoleTest(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)    

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.main.test", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.main.test", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.main.test", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_console_extension_name(self):
        return self.console_test.get_console_extension_name()

    def get_all_commands(self):
        return self.console_test.get_all_commands()

    def get_handler_command(self, command):
        return self.console_test.get_handler_command(command)

    def get_help(self):
        return self.console_test.get_help()

    def get_all_test_cases(self):
        return self.main_test.get_all_test_cases()

    def get_all_test_cases_plugin(self, plugin_id, plugin_version):
        return self.main_test.get_all_test_cases_plugin(plugin_id, plugin_version)

    def start_all_test(self):
        return self.main_test.start_all_test()

    def start_test(self, test_cases_list):
        return self.main_test.start_test(test_cases_list)

    @colony.plugins.decorators.load_allowed_capability("test_manager")
    def test_manager_capability_load_allowed(self, plugin, capability):
        pass

    @colony.plugins.decorators.load_allowed_capability("test_case")
    def test_case_capability_load_allowed(self, plugin, capability):
        self.test_case_plugins.append(plugin)
        self.main_test.load_test_case_plugin(plugin)

    @colony.plugins.decorators.load_allowed_capability("test_case_bundle")
    def test_case_bundle_capability_load_allowed(self, plugin, capability):
        self.test_case_bundle_plugins.append(plugin)
        self.main_test.load_test_case_bundle_plugin(plugin)

    @colony.plugins.decorators.load_allowed_capability("plugin_test_case")
    def plugin_test_case_capability_load_allowed(self, plugin, capability):
        self.plugin_test_case_plugins.append(plugin)
        self.main_test.load_plugin_test_case_plugin(plugin)

    @colony.plugins.decorators.load_allowed_capability("plugin_test_case_bundle")
    def plugin_test_case_bundle_capability_load_allowed(self, plugin, capability):
        self.plugin_test_case_bundle_plugins.append(plugin)
        self.main_test.load_plugin_test_case_bundle_plugin(plugin)

    @colony.plugins.decorators.unload_allowed_capability("test_manager")
    def test_manager_capability_unload_allowed(self, plugin, capability):
        pass

    @colony.plugins.decorators.unload_allowed_capability("test_case")
    def test_case_capability_unload_allowed(self, plugin, capability):
        self.test_case_plugins.remove(plugin)
        self.main_test.unload_test_case_plugin(plugin)

    @colony.plugins.decorators.unload_allowed_capability("test_case_bundle")
    def test_case_bundle_capability_unload_allowed(self, plugin, capability):
        self.test_case_bundle_plugins.remove(plugin)
        self.main_test.unload_test_case_bundle_plugin(plugin)

    @colony.plugins.decorators.unload_allowed_capability("plugin_test_case")
    def plugin_test_case_capability_unload_allowed(self, plugin, capability):
        self.plugin_test_case_plugins.remove(plugin)
        self.main_test.unload_plugin_test_case_plugin(plugin)

    @colony.plugins.decorators.unload_allowed_capability("plugin_test_case_bundle")
    def plugin_test_case_bundle_capability_unload_allowed(self, plugin, capability):
        self.plugin_test_case_bundle_plugins.remove(plugin)
        self.main_test.unload_plugin_test_case_bundle_plugin(plugin)

    def get_code_coverage_plugin(self):
        return self.code_coverage_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.code_coverage")
    def set_code_coverage_plugin(self, code_coverage_plugin):
        self.code_coverage_plugin = code_coverage_plugin
