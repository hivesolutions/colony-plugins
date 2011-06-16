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

class WebEntityManagerAdministrationPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Web Entity Manager Administration plugin.
    """

    id = "pt.hive.colony.plugins.web.entity_manager_administration"
    name = "Web Entity Manager Administration Plugin"
    short_name = "Web Entity Manager Administration"
    description = "The plugin that offers a web interface for colony entity manager administration"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/web_entity_manager_administration/administration/resources/baf.xml"
    }
    capabilities = [
        "web.entity_manager_administration",
        "rest_service",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.resources.resource_manager", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.data.entity_manager", "1.0.0")
    ]
    main_modules = [
        "web_entity_manager_administration.administration.web_entity_manager_administration_system"
    ]

    web_entity_manager_administration = None
    """ The web entity manager administration """

    resource_manager_plugin = None
    """ The resource manager plugin """

    entity_manager_plugin = None
    """ The entity manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import web_entity_manager_administration.administration.web_entity_manager_administration_system
        self.web_entity_manager_administration = web_entity_manager_administration.administration.web_entity_manager_administration_system.WebEntityManagerAdministration(self)

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

    def get_routes(self):
        """
        Retrieves the list of regular expressions to be used as route,
        to the rest service.

        @rtype: List
        @return: The list of regular expressions to be used as route,
        to the rest service.
        """

        return self.web_entity_manager_administration.get_routes()

    def handle_rest_request(self, rest_request):
        """
        Handles the given rest request.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled.
        """

        return self.web_entity_manager_administration.handle_rest_request(rest_request)

    def get_resource_manager_plugin(self):
        """
        Retrieves the resource manager plugin.

        @rtype: ResourceManagerPlugin
        @return: The resource manager plugin.
        """

        return self.resource_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.resources.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        """
        Sets the resource manager plugin.

        @type resource_manager_plugin: ResourceManagerPlugin.
        @param resource_manager_plugin: The resource manager plugin.
        """

        self.resource_manager_plugin = resource_manager_plugin

    def get_entity_manager_plugin(self):
        """
        Retrieves the entity manager plugin.

        @rtype: EntityManagerPlugin
        @return: The entity manager plugin.
        """

        return self.entity_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.data.entity_manager")
    def set_entity_manager_plugin(self, entity_manager_plugin):
        """
        Sets the entity manager plugin.

        @type entity_manager_plugin: EntityManagerPlugin
        @param entity_manager_plugin: The entity manager plugin.
        """

        self.entity_manager_plugin = entity_manager_plugin
