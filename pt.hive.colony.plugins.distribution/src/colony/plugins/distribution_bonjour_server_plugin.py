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

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class DistributionBonjourServerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Distribution Bonjour Server plugin.
    """

    id = "pt.hive.colony.plugins.distribution.bonjour_server"
    name = "Distribution Bonjour Server Plugin"
    short_name = "Distribution Bonjour Server"
    description = "Distribution Bonjour Server Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/distribution/bonjour_server/resources/baf.xml"
    }
    capabilities = [
        "distribution_server_adapter",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.bonjour", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.remote.manager", "1.0.0")
    ]
    main_modules = [
        "distribution.bonjour_server.distribution_bonjour_server_system"
    ]

    distribution_bonjour_server = None
    """ The distribution bonjour server """

    bonjour_plugin = None
    """ The bonjour plugin """

    main_remote_manager_plugin = None
    """ The main remote manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import distribution.bonjour_server.distribution_bonjour_server_system
        self.distribution_bonjour_server = distribution.bonjour_server.distribution_bonjour_server_system.DistributionBonjourServer(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.distribution.bonjour_server", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_server_type(self):
        return self.distribution_bonjour_server.get_server_type()

    def get_distribution_server_type(self):
        return self.distribution_bonjour_server.get_distribution_server_type()

    def activate_server(self, properties):
        return self.distribution_bonjour_server.activate_server(properties)

    def deactivate_server(self, properties):
        return self.distribution_bonjour_server.deactivate_server(properties)

    def get_bonjour_plugin(self):
        return self.bonjour_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.bonjour")
    def set_bonjour_plugin(self, bonjour_plugin):
        self.bonjour_plugin = bonjour_plugin

    def get_main_remote_manager_plugin(self):
        return self.main_remote_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.remote.manager")
    def set_main_remote_manager_plugin(self, main_remote_manager_plugin):
        self.main_remote_manager_plugin = main_remote_manager_plugin
