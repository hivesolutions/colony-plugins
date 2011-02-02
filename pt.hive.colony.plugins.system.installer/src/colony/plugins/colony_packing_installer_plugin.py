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

__revision__ = "$LastChangedRevision: 7715 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-26 07:31:00 +0000 (sex, 26 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class ColonyPackingInstallerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Colony Packing Installer plugin.
    """

    id = "pt.hive.colony.plugins.system.installer.colony_packing_installer"
    name = "Colony Packing Installer Plugin"
    short_name = "Colony Packing Installer"
    description = "Colony Packing Installer Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/system_installer/colony_packing/resources/baf.xml"}
    capabilities = ["installer", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.packing.manager", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["system_installer.colony_packing.colony_packing_installer_exceptions",
                    "system_installer.colony_packing.colony_packing_installer_system"]

    colony_packing_installer = None

    packing_manager_plugin = None
    """ Plugin to for packing of files """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global system_installer
        import system_installer.colony_packing.colony_packing_installer_system
        self.colony_packing_installer = system_installer.colony_packing.colony_packing_installer_system.ColonyPackingInstaller(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.system.updater.colony_packing_installer", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_installer_type(self):
        return self.colony_packing_installer.get_installer_type()

    def install_bundle(self, file_path, properties):
        """
        Method called upon deployment of the bundle with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the bundle file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        """

        return self.colony_packing_installer.install_bundle(file_path, properties)

    def install_plugin(self, file_path, properties):
        """
        Method called upon deployment of the plugin with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the plugin file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        """

        return self.colony_packing_installer.install_plugin(file_path, properties)

    def get_packing_manager_plugin(self):
        return self.packing_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.packing.manager")
    def set_packing_manager_plugin(self, packing_manager_plugin):
        self.packing_manager_plugin = packing_manager_plugin
