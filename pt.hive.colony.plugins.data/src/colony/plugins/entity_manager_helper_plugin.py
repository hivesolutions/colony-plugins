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

__revision__ = "$LastChangedRevision: 7681 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-24 18:27:03 +0000 (qua, 24 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class EntityManagerHelperPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Business Helper plugin.
    """

    id = "pt.hive.colony.plugins.data.entity_manager_helper"
    name = "Entity Manager Helper Plugin"
    short_name = "Entity Manager Helper"
    description = "Entity Manager Helper Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/data/entity_manager_helper/resources/baf.xml"
    }
    capabilities = [
        "entity_manager_helper",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.data.entity_manager", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.business.helper", "1.0.0")
    ]
    main_modules = [
        "data.entity_manager_helper.entity_manager_helper_system"
    ]

    entity_manger_helper = None
    """ The entity manager helper """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global data
        import data.entity_manager_helper.entity_manager_helper_system
        self.entity_manger_helper = data.entity_manager_helper.entity_manager_helper_system.EntityManagerHelper(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.data.entity_manager_helper", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def load_entity_manager(self, entities_module_name, entities_module_path, entity_manager_arguments):
        """
        Loads the entity manager object, used to access
        the database.
        The entity manager is loaded for the entities in the module
        located in the entities module path and in the module with the given
        entities module name.
        The given entity manager arguments are used in the connection establishment.

        @type entities_module_name: String
        @param entities_module_name: The name of the entities module.
        @type entities_module_path: String
        @param entities_module_path: The path to the entities module.
        @type entity_manager_arguments: Dictionary
        @param entity_manager_arguments: The arguments for the entity manager
        loading.
        @rtype: EntityManager
        @return: The loaded entity manager.
        """

        return self.entity_manger_helper.load_entity_manager(entities_module_name, entities_module_path, entity_manager_arguments)

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
