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

class WebDeployerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Web Deployer plugin
    """

    id = "pt.hive.colony.plugins.system.updater.web_deployer"
    name = "Web Deployer Plugin"
    short_name = "Web Deployer"
    description = "Web Deployer Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["deployer"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.zip", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.resource_manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    web_deployer = None

    zip_plugin = None
    """ Plugin to manage zip files """

    resource_manager_plugin = None
    """ Plugin to manage resouces """

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global system_updater
        import system_updater.web_deployer.web_deployment_system
        self.web_deployer = system_updater.web_deployer.web_deployment_system.WebDeployer(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.web_deployer.load_deployer()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.system.updater.web_deployer", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def deploy_package(self, zip_file, plugin_id, plugin_version):
        self.web_deployer.deploy_package(zip_file, plugin_id, plugin_version)

    def get_deployer_type(self):
        return "web"

    def get_zip_plugin(self):
        return self.zip_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.zip")
    def set_zip_plugin(self, zip_plugin):
        self.zip_plugin = zip_plugin

    def get_resource_manager_plugin(self):
        return self.resource_manager

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.resource_manager")
    def set_resource_manager(self, resource_manager):
        self.resource_manager = resource_manager
