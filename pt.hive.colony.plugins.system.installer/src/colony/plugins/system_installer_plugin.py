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

__revision__ = "$LastChangedRevision: 12928 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-02-01 13:28:26 +0000 (ter, 01 Fev 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class SystemInstallerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the System Installer plugin.
    """

    id = "pt.hive.colony.plugins.system.installer"
    name = "System Installer Plugin"
    short_name = "System Installer"
    description = "System Installer Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/system_installer/installer/resources/baf.xml"}
    capabilities = ["system_installation", "_console_command_extension", "build_automation_item"]
    capabilities_allowed = ["installer"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["system_installer.installer.console_system_installer",
                    "system_installer.installer.system_installer_exceptions",
                    "system_installer.installer.system_installer_system"]

    system_installer = None
    console_system_installer = None

    installer_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global system_installer
        import system_installer.installer.system_installer_system
        import system_installer.installer.console_system_installer
        self.system_installer = system_installer.installer.system_installer_system.SystemInstaller(self)
        self.console_system_installer = system_installer.installer.console_system_installer.ConsoleSystemInstaller(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.system.installer", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.system.installer", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.system.installer", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def install_package(self, package_id, package_version):
        return self.system_installer.install_package(package_id, package_version)

    def install_bundle(self, bundle_id, bundle_version):
        return self.system_installer.install_bundle(bundle_id, bundle_version)

    def install_plugin(self, plugin_id, plugin_version):
        return self.system_installer.install_plugin(plugin_id, plugin_version)

    def get_console_extension_name(self):
        return self.console_system_installer.get_console_extension_name()

    def get_commands_map(self):
        return self.console_system_installer.get_commands_map()

    @colony.base.decorators.load_allowed_capability("installer")
    def deployer_load_allowed(self, plugin, capability):
        self.installer_plugins.append(plugin)
        self.system_installer.installer_load(plugin)

    @colony.base.decorators.unload_allowed_capability("installer")
    def deployer_unload_allowed(self, plugin, capability):
        self.installer_plugins.remove(plugin)
        self.system_installer.installer_unload(plugin)
