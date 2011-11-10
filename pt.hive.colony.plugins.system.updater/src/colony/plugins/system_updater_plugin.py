#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class SystemUpdaterPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the System Updater plugin.
    """

    id = "pt.hive.colony.plugins.system.updater"
    name = "System Updater Plugin"
    short_name = "System Updater"
    description = "System Updater Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/system_updater/updater/resources/baf.xml"
    }
    capabilities = [
        "system_updating",
        "_console_command_extension",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "deployer"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.system.registry", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.downloader", "1.0.0")
    ]
    main_modules = [
        "system_updater.updater.console_system_updater",
        "system_updater.updater.system_updater_exceptions",
        "system_updater.updater.system_updater_parser",
        "system_updater.updater.system_updater_system"
    ]

    system_updater = None
    """ The system updater """

    console_system_updater = None
    """ The console system updater """

    deployer_plugins = []
    """ The deployer plugins """

    system_registry_plugin = None
    """ The system registry plugin """

    downloader_plugin = None
    """ The downloader plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import system_updater.updater.system_updater_system
        import system_updater.updater.console_system_updater
        self.system_updater = system_updater.updater.system_updater_system.SystemUpdater(self)
        self.console_system_updater = system_updater.updater.console_system_updater.ConsoleSystemUpdater(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.system_updater.load_system_updater()

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

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def load_repositories_information(self):
        return self.system_updater.load_repositories_information()

    def reset_repositories_information(self):
        return self.system_updater.reset_repositories_information()

    def save_repositories_cache(self):
        return self.system_updater.save_repositories_cache()

    def load_repositories_cache(self):
        return self.system_updater.load_repositories_cache()

    def get_repositories(self):
        return self.system_updater.get_repositories()

    def get_repository_information_by_repository_name(self, repository_name):
        return self.system_updater.get_repository_information_by_repository_name(repository_name)

    def install_package(self, package_id, package_version):
        return self.system_updater.install_package(package_id, package_version)

    def install_bundle(self, bundle_id, bundle_version):
        return self.system_updater.install_bundle(bundle_id, bundle_version)

    def install_plugin(self, plugin_id, plugin_version):
        return self.system_updater.install_plugin(plugin_id, plugin_version)

    def install_container(self, container_id, container_version):
        return self.system_updater.install_container(container_id, container_version)

    def uninstall_package(self, package_id, package_version):
        return self.system_updater.uninstall_package(package_id, package_version)

    def uninstall_bundle(self, bundle_id, bundle_version):
        return self.system_updater.uninstall_bundle(bundle_id, bundle_version)

    def uninstall_plugin(self, plugin_id, plugin_version):
        return self.system_updater.uninstall_plugin(plugin_id, plugin_version)

    def uninstall_container(self, container_id, container_version):
        return self.system_updater.uninstall_container(container_id, container_version)

    def get_console_extension_name(self):
        return self.console_system_updater.get_console_extension_name()

    def get_commands_map(self):
        return self.console_system_updater.get_commands_map()

    @colony.base.decorators.load_allowed_capability("deployer")
    def deployer_load_allowed(self, plugin, capability):
        self.deployer_plugins.append(plugin)
        self.system_updater.deployer_load(plugin)

    @colony.base.decorators.unload_allowed_capability("deployer")
    def deployer_unload_allowed(self, plugin, capability):
        self.deployer_plugins.remove(plugin)
        self.system_updater.deployer_unload(plugin)

    def get_system_registry_plugin(self):
        return self.system_registry_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.system.registry")
    def set_system_registry_plugin(self, system_registry_plugin):
        self.system_registry_plugin = system_registry_plugin

    def get_downloader_plugin(self):
        return self.downloader_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.downloader")
    def set_downloader_plugin(self, downloader_plugin):
        self.downloader_plugin = downloader_plugin
