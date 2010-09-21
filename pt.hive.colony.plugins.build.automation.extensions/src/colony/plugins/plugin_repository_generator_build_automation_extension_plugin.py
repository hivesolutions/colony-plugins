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

class PluginRepositoryGeneratorBuildAutomationExtensionPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Plugin Repository Generator Build Automation Extension plugin
    """

    id = "pt.hive.colony.plugins.build.automation.extensions.plugin_repository.generator"
    name = "Plugin Repository Generator Build Automation Extension Plugin"
    short_name = "Plugin Repository Generator Build Automation Extension"
    description = "A plugin to manage the plugin repository generator build automation tasks"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/build_automation_extensions/plugin_repository_generator/resources/baf.xml"}
    capabilities = ["build_automation_extension", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.repository_descriptor_generator", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["build_automation_extensions.plugin_repository_generator.plugin_repository_generator_build_automation_extension_system"]

    plugin_repository_generator_build_automation_extension = None

    repository_descriptor_generator_plugin = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global build_automation_extensions
        import build_automation_extensions.plugin_repository_generator.plugin_repository_generator_build_automation_extension_system
        self.plugin_repository_generator_build_automation_extension = build_automation_extensions.plugin_repository_generator.plugin_repository_generator_build_automation_extension_system.PluginRepositoryGeneratorBuildAutomationExtension(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.build.automation.extensions.plugin_repository.generator", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        self.plugin_repository_generator_build_automation_extension.run_automation(plugin, stage, parameters, build_automation_structure, logger)

    def get_repository_descriptor_generator_plugin(self):
        return self.repository_descriptor_generator_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.repository_descriptor_generator")
    def set_repository_descriptor_generator_plugin(self, repository_descriptor_generator_plugin):
        self.repository_descriptor_generator_plugin = repository_descriptor_generator_plugin
