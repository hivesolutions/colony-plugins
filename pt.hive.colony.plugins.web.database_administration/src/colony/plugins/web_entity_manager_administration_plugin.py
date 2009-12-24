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

import colony.plugins.plugin_system
import colony.plugins.decorators

class WebEntityManagerAdministrationPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Web Entity Manager Administration plugin.
    """

    id = "pt.hive.colony.plugins.web.entity_manager_administration"
    name = "Web Entity Manager Administration Plugin"
    short_name = "Web Entity Manager Administration"
    description = "The plugin that offers a web interface for colony entity manager administration"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["web.entity_manager_administration", "rest_service"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.resources.resource_manager", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.business.entity_manager", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["web_entity_manager_administration.administration.web_entity_manager_administration_system"]

    web_entity_manager_administration = None

    resource_manager_plugin = None
    business_entity_manager_plugin = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global web_entity_manager_administration
        import web_entity_manager_administration.administration.web_entity_manager_administration_system
        self.web_entity_manager_administration = web_entity_manager_administration.administration.web_entity_manager_administration_system.WebEntityManagerAdministration(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.web.entity_manager_administration", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_routes(self):
        pass

    def handle_rest_request(self, rest_request):
        return self.web_entity_manager_administration.handle_rest_request(rest_request)

    def get_resource_manager_plugin(self):
        return self.resource_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.resources.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin

    def get_business_entity_manager_plugin(self):
        return self.business_entity_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.business.entity_manager")
    def set_business_entity_manager_plugin(self, business_entity_manager_plugin):
        self.business_entity_manager_plugin = business_entity_manager_plugin
