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

__revision__ = "$LastChangedRevision: 8461 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-05-12 06:45:34 +0100 (qua, 12 Mai 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class InstallationManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Installation Manager plugin.
    """

    id = "pt.hive.colony.plugins.installation.manager"
    name = "Installation Manager Plugin"
    short_name = "Installation Manager"
    description = "A plugin to manage the installation generation of the packages"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/installation/manager/resources/baf.xml"}
    capabilities = ["installation.manager", "build_automation_item"]
    capabilities_allowed = ["installation.adapter"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["installation.manager.installation_manager_exceptions",
                    "installation.manager.installation_manager_system"]

    installation_manager = None

    installation_adapter_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global installation
        import installation.manager.installation_manager_system
        self.installation_manager = installation.manager.installation_manager_system.InstallationManager(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.installation.manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.installation.manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def generate_installation_file(self, parameters):
        """
        Generates the installation file for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the installation file generation.
        """

        return self.installation_manager.generate_installation_file(parameters)

    @colony.base.decorators.load_allowed_capability("installation.adapter")
    def installation_adapter_load_allowed(self, plugin, capability):
        self.installation_adapter_plugins.append(plugin)
        self.installation_manager.installation_adapter_load(plugin)

    @colony.base.decorators.unload_allowed_capability("installation.adapter")
    def installation_adapter_unload_allowed(self, plugin, capability):
        self.installation_adapter_plugins.remove(plugin)
        self.installation_manager.installation_adapter_unload(plugin)
