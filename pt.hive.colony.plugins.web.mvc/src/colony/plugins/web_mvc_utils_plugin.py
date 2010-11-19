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

class WebMvcUtilsPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Web Mvc Utils plugin.
    """

    id = "pt.hive.colony.plugins.web.mvc.utils"
    name = "Web Mvc Utils Plugin"
    short_name = "Web Mvc Utils"
    description = "The plugin that offers the top-level abstractions for mvc processing"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/web_mvc_utils/mvc_utils/resources/baf.xml"}
    capabilities = ["web.mvc.utils", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.template_engine.manager", "1.0.0"),
                    colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.data.entity_manager", "1.0.0"),
                    colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.business.helper", "1.0.0"),
                    colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.web.mvc.search", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["web_mvc_utils.mvc_utils.web_mvc_controller",
                    "web_mvc_utils.mvc_utils.web_mvc_entity_model",
                    "web_mvc_utils.mvc_utils.web_mvc_model",
                    "web_mvc_utils.mvc_utils.web_mvc_utils",
                    "web_mvc_utils.mvc_utils.web_mvc_utils_exceptions",
                    "web_mvc_utils.mvc_utils.web_mvc_utils_system"]

    web_mvc_utils = None

    template_engine_manager_plugin = None
    entity_manager_plugin = None
    business_helper_plugin = None
    web_mvc_search_plugin = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global web_mvc_utils
        import web_mvc_utils.mvc_utils.web_mvc_utils_system
        self.web_mvc_utils = web_mvc_utils.mvc_utils.web_mvc_utils_system.WebMvcUtils(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.web.mvc.utils", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def import_module_mvc_utils(self, module_name, package_name, directory_path):
        return self.web_mvc_utils.import_module_mvc_utils(module_name, package_name, directory_path)

    def create_model(self, base_model, base_arguments_list, base_arguments_map):
        return self.web_mvc_utils.create_model(base_model, base_arguments_list, base_arguments_map)

    def create_controller(self, base_controller, base_arguments_list, base_arguments_map):
        return self.web_mvc_utils.create_controller(base_controller, base_arguments_list, base_arguments_map)

    def create_entity_models(self, base_entity_models_module_name, entity_manager_arguments, directory_path):
        return self.web_mvc_utils.create_entity_models(base_entity_models_module_name, entity_manager_arguments, directory_path)

    def create_search_index_controller(self, search_index_identifier, search_index_configuration_map, entity_models_modules):
        return self.web_mvc_utils.create_search_index_controller(search_index_identifier, search_index_configuration_map, entity_models_modules)

    def get_template_engine_manager_plugin(self):
        return self.template_engine_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.template_engine.manager")
    def set_template_engine_manager_plugin(self, template_engine_manager_plugin):
        self.template_engine_manager_plugin = template_engine_manager_plugin

    def get_entity_manager_plugin(self):
        return self.entity_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.data.entity_manager")
    def set_entity_manager_plugin(self, entity_manager_plugin):
        self.entity_manager_plugin = entity_manager_plugin

    def get_business_helper_plugin(self):
        return self.business_helper_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.business.helper")
    def set_business_helper_plugin(self, business_helper_plugin):
        self.business_helper_plugin = business_helper_plugin

    def get_web_mvc_search_plugin(self):
        return self.web_mvc_search_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.web.mvc.search")
    def set_web_mvc_search_plugin(self, web_mvc_search_plugin):
        self.web_mvc_search_plugin = web_mvc_search_plugin
