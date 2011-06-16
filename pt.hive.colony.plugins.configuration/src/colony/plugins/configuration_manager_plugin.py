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

class ConfigurationManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Configuration Manager plugin.
    """

    id = "pt.hive.colony.plugins.configuration.manager"
    name = "Configuration Manager Plugin"
    short_name = "Configuration Manager"
    description = "The plugin that controls the deployment and retrieval of configurations"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/configuration_manager/manager/resources/baf.xml"
    }
    capabilities = [
        "startup",
        "configuration_manager",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "configuration_model_provider"
    ]
    main_modules = [
        "configuration_manager.manager.configuration_manager_system"
    ]

    configuration_manager = None
    """ The configuration manager """

    configuration_model_provider_plugins = []
    """ The configuration model provider plugins """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import configuration_manager.manager.configuration_manager_system
        self.configuration_manager = configuration_manager.manager.configuration_manager_system.ConfigurationManager(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.load_allowed_capability("configuration_model_provider")
    def configuration_model_provider_load_allowed(self, plugin, capability):
        self.configuration_model_provider_plugins.append(plugin)
        self.configuration_manager.configuration_model_provider_load(plugin)

    @colony.base.decorators.unload_allowed_capability("configuration_model_provider")
    def configuration_model_provider_unload_allowed(self, plugin, capability):
        self.configuration_model_provider_plugins.remove(plugin)
        self.configuration_manager.configuration_model_provider_unload(plugin)
