#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system
import colony.base.decorators

class WebMvcUtilsPlugin(colony.base.system.Plugin):
    """
    The main class for the Web Mvc Utils plugin.
    """

    id = "pt.hive.colony.plugins.web.mvc.utils"
    name = "Web Mvc Utils Plugin"
    short_name = "Web Mvc Utils"
    description = "The plugin that offers the top-level abstractions for mvc processing"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "web.mvc.utils"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.template_engine.manager", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.data.entity_manager.new", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.data.file_manager", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.business.helper", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.resources.resource_manager", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.x.x")
    ]
    main_modules = [
        "web_mvc_utils.mvc_utils.web_mvc_controller",
        "web_mvc_utils.mvc_utils.web_mvc_entity_model",
        "web_mvc_utils.mvc_utils.web_mvc_model",
        "web_mvc_utils.mvc_utils.web_mvc_utils",
        "web_mvc_utils.mvc_utils.web_mvc_utils_exceptions",
        "web_mvc_utils.mvc_utils.web_mvc_utils_system"
    ]

    web_mvc_utils = None
    """ The web mvc utils """

    template_engine_manager_plugin = None
    """ The template engine manager plugin """

    entity_manager_plugin = None
    """ The entity manager plugin """

    file_manager_plugin = None
    """ The file manager plugin """

    business_helper_plugin = None
    """ The business helper plugin """

    web_mvc_search_plugin = None
    """ The web mvc search plugin """

    resource_manager_plugin = None
    """ The resource manager plugin """

    json_plugin = None
    """ The json plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import web_mvc_utils.mvc_utils.web_mvc_utils_system
        self.web_mvc_utils = web_mvc_utils.mvc_utils.web_mvc_utils_system.WebMvcUtils(self)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def import_module_mvc_utils(self, module_name, package_name, directory_path):
        return self.web_mvc_utils.import_module_mvc_utils(module_name, package_name, directory_path)

    def create_model(self, base_model, base_arguments_list, base_arguments_map):
        return self.web_mvc_utils.create_model(base_model, base_arguments_list, base_arguments_map)

    def create_controller(self, base_controller, base_arguments_list, base_arguments_map):
        return self.web_mvc_utils.create_controller(base_controller, base_arguments_list, base_arguments_map)

    def create_base_models(self, system_instance, package_path, entity_manager_arguments):
        return self.web_mvc_utils.create_base_models(package_path, entity_manager_arguments)

    def create_base_models_path(self, system_instance, package_path, entity_manager_arguments, directory_path):
        return self.web_mvc_utils.create_base_models(system_instance, package_path, entity_manager_arguments, directory_path)

    def create_models(self, system_instance, plugin_instance, package_path, entity_manager_arguments):
        return self.web_mvc_utils.create_models(system_instance, plugin_instance, package_path, entity_manager_arguments)

    def create_models_extra(self, system_instance, plugin_instance, package_path, entity_manager_arguments, extra_models):
        return self.web_mvc_utils.create_models(system_instance, plugin_instance, package_path, entity_manager_arguments, extra_models)

    def assign_models(self, system_instance, plugin_instance, entity_manager_arguments):
        return self.web_mvc_utils.create_models(system_instance, plugin_instance, entity_manager_arguments = entity_manager_arguments)

    def unassign_models(self, system_instance, entity_manager_arguments):
        return self.web_mvc_utils.destroy_models(system_instance, entity_manager_arguments = entity_manager_arguments)

    def create_controllers(self, system_instance, plugin_instance, package_path, prefix_name):
        return self.web_mvc_utils.create_controllers(system_instance, plugin_instance, package_path, prefix_name)

    def assign_controllers(self, system_instance, plugin_instance):
        return self.web_mvc_utils.create_controllers(system_instance, plugin_instance)

    def unassign_controllers(self, system_instance):
        return self.web_mvc_utils.destroy_controllers(system_instance)

    def assign_models_controllers(self, system_instance, plugin_instance, entity_manager_arguments):
        self.web_mvc_utils.create_models(system_instance, plugin_instance, entity_manager_arguments = entity_manager_arguments)
        self.web_mvc_utils.create_controllers(system_instance, plugin_instance)
        return True

    def unassign_models_controllers(self, system_instance, entity_manager_arguments):
        self.web_mvc_utils.destroy_models(system_instance, entity_manager_arguments = entity_manager_arguments)
        self.web_mvc_utils.destroy_controllers(system_instance)
        return True

    def create_file_manager(self, engine_name, connection_parameters):
        """
        Creates a new file manager reference, to manage files
        in an indirect and adapted fashion.
        The created file manager respects the given engine name
        and connection parameters.

        @type engine_name: String
        @param engine_name: The name of the engine to be used in
        the file manager.
        @type connection_parameters: Dictionary
        @param connection_parameters: The parameters for the connection
        in the file manager.
        @rtype: FileManager
        @return: The created file manager.
        """

        return self.web_mvc_utils.create_file_manager(engine_name, connection_parameters)

    def generate_patterns(self, patterns, controller, prefix_name):
        return self.web_mvc_utils.generate_patterns(patterns, controller, prefix_name)

    def generate_entity_manager_arguments(self, plugin, base_entity_manager_arguments, parameters = {}):
        return self.web_mvc_utils.generate_entity_manager_arguments(plugin, base_entity_manager_arguments, parameters)

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.template_engine.manager")
    def set_template_engine_manager_plugin(self, template_engine_manager_plugin):
        self.template_engine_manager_plugin = template_engine_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.data.entity_manager.new")
    def set_entity_manager_plugin(self, entity_manager_plugin):
        self.entity_manager_plugin = entity_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.data.file_manager")
    def set_file_manager_plugin(self, file_manager_plugin):
        self.file_manager_plugin = file_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.business.helper")
    def set_business_helper_plugin(self, business_helper_plugin):
        self.business_helper_plugin = business_helper_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.resources.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin
