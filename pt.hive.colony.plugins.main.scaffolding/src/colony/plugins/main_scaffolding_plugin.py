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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainScaffoldingPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Main Scaffolding Plugin.
    """

    id = "pt.hive.colony.plugins.main.scaffolding"
    name = "Main Scaffolding Plugin"
    short_name = "Main Scaffolding"
    description = "The main scaffolding plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_scaffolding/scaffolding/resources/baf.xml"
    }
    capabilities = [
        "_console_command_extension",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "scaffolder"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.template_engine.manager", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.0.0")
    ]
    main_modules = [
        "main_scaffolding.scaffolding.console_main_scaffolding",
        "main_scaffolding.scaffolding.main_scaffolding_exceptions",
        "main_scaffolding.scaffolding.main_scaffolding_system"
    ]

    main_scaffolding = None
    """ The main scaffolding """

    console_main_scaffolding = None
    """ The console main scaffolding """

    template_engine_manager_plugin = None
    """ The template engine manager plugin """

    json_plugin = None
    """ The json plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global main_scaffolding
        import main_scaffolding.scaffolding.main_scaffolding_system
        import main_scaffolding.scaffolding.console_main_scaffolding
        self.main_scaffolding = main_scaffolding.scaffolding.main_scaffolding_system.MainScaffolding(self)
        self.console_main_scaffolding = main_scaffolding.scaffolding.console_main_scaffolding.ConsoleMainScaffolding(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.main.scaffolding", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.main.scaffolding", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.main.scaffolding", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_scaffolder_types(self):
        return self.main_scaffolding.get_scaffolder_types()

    def generate_scaffold(self, scaffolder_type, plugin_id, plugin_version, scaffold_path, specification_file_path):
        self.main_scaffolding.generate_scaffold(scaffolder_type, plugin_id, plugin_version, scaffold_path, specification_file_path)

    def get_console_extension_name(self):
        return self.console_main_scaffolding.get_console_extension_name()

    def get_commands_map(self):
        return self.console_main_scaffolding.get_commands_map()

    @colony.base.decorators.load_allowed_capability("scaffolder")
    def scaffolder_load_allowed(self, plugin, capability):
        self.main_scaffolding.load_scaffolder_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("scaffolder")
    def scaffolder_unload_allowed(self, plugin, capability):
        self.main_scaffolding.unload_scaffolder_plugin(plugin)

    def get_template_engine_manager_plugin(self):
        return self.template_engine_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.template_engine.manager")
    def set_template_engine_manager_plugin(self, template_engine_manager_plugin):
        self.template_engine_manager_plugin = template_engine_manager_plugin

    def get_json_plugin(self):
        return self.json_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin
