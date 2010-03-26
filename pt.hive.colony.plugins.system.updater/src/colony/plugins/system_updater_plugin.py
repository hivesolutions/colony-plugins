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

class SystemUpdaterPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the System Updater plugin
    """

    id = "pt.hive.colony.plugins.system.updater"
    name = "System Updater Plugin"
    short_name = "System Updater"
    description = "System Updater Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["system_updating", "console_command_extension"]
    capabilities_allowed = ["deployer"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.downloader", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["system_updater.updater.console_system_updater", "system_updater.updater.system_updating_parser",
                    "system_updater.updater.system_updating_system"]

    system_updater = None
    console_system_updater = None

    downloader_plugin = None
    deployer_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global system_updater
        import system_updater.updater.system_updating_system
        import system_updater.updater.console_system_updater
        self.system_updater = system_updater.updater.system_updating_system.SystemUpdater(self)
        self.console_system_updater = system_updater.updater.console_system_updater.ConsoleSystemUpdater(self)
        self.system_updater.load_system_updater()

        self.deployer_plugins = []

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

        if capability == "deployer":
            self.deployer_plugins.append(plugin)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.system.updater", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_deployer_by_deployer_type(self, deployer_type):
        """
        Retrieves a deployer for the given deployer type

        @type deployer_type : String
        @param deployer_type: The type of the deployer to retrieve
        @rtype: Plugin
        @return: The plugin for the given deployer type
        """

        for deployer_plugin in self.deployer_plugins:
            if deployer_plugin.get_deployer_type() == deployer_type:
                return deployer_plugin

    def get_repositories(self):
        return self.system_updater.get_repositories()

    def get_repository_information_by_repository_name(self, repository_name):
        return self.system_updater.get_repository_information_by_repository_name(repository_name)

    def get_console_extension_name(self):
        return self.console_system_updater.get_console_extension_name()

    def get_all_commands(self):
        return self.console_system_updater.get_all_commands()

    def get_handler_command(self, command):
        return self.console_system_updater.get_handler_command(command)

    def get_help(self):
        return self.console_system_updater.get_help()

    def get_downloader_plugin(self):
        return self.downloader_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.downloader")
    def set_downloader_plugin(self, downloader_plugin):
        self.downloader_plugin = downloader_plugin
