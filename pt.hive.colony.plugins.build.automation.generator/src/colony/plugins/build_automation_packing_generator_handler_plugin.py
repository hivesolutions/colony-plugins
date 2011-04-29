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

__revision__ = "$LastChangedRevision: 429 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-21 13:03:27 +0000 (Sex, 21 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class BuildAutomationPackingGeneratorHandlerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Build Automation Packing Generator Handler plugin.
    """

    id = "pt.hive.colony.plugins.build.automation.packing_generator_handler"
    name = "Build Automation Packing Generator Handler Plugin"
    short_name = "Build Automation Packing Generator Handler"
    description = "A plugin to generate pacing build automation files"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/build_automation_generator/packing_generator_handler/resources/baf.xml"
    }
    capabilities = [
        "build_automation_generator_handler",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.template_engine.manager", "1.0.0")
    ]
    main_modules = [
        "build_automation_generator.packing_generator_handler.build_automation_packing_generator_handler_system"
    ]

    build_automation_packing_generator_handler = None
    """ The build automation packing generator handler """

    template_engine_manager_plugin = None
    """ The template engine manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global build_automation_generator
        import build_automation_generator.packing_generator_handler.build_automation_packing_generator_handler_system
        self.build_automation_packing_generator_handler = build_automation_generator.packing_generator_handler.build_automation_packing_generator_handler_system.BuildAutomationPackingGeneratorHandler(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.build.automation.packing_generator_handler", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_build_automation_generator_handler_name(self):
        return self.build_automation_packing_generator_handler.get_build_automation_generator_handler_name()

    def generate_plugin_build_automation(self, plugin, properties):
        """
        Generates a build automation string describing the structure
        and specification of the given plugin.

        @type plugin: Plugin
        @param plugin: The plugin to be used to generate plugin build automation.
        @type properties: Dictionary
        @param properties: The properties for plugin build automation generation.
        @rtype: String
        @return: The generated plugin build automation string.
        """

        return self.build_automation_packing_generator_handler.generate_plugin_build_automation(plugin, properties)

    def get_template_engine_manager_plugin(self):
        return self.template_engine_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.template_engine.manager")
    def set_template_engine_manager_plugin(self, template_engine_manager_plugin):
        self.template_engine_manager_plugin = template_engine_manager_plugin
