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

class PluginDownloaderPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Plugin Downloader plugin.
    """

    id = "pt.hive.colony.plugins.misc.plugin_downloader"
    name = "Plugin Downloader Plugin"
    short_name = "Plugin Downloader"
    description = "A plugin to automatically download plugins and dependencies"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/misc/plugin_downloader/resources/baf.xml"}
    capabilities = ["console_command_extension", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.downloader", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.zip", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.dependencies_calculator", "1.0.0", False)]
    events_handled = []
    events_registrable = []

    plugin_downloader = None
    console_plugin_downloader = None

    downloader_plugin = None
    """ Plugin to access the downloading system """

    zip_plugin = None
    """ Plugin to manage zip files """

    dependencies_calculator_plugin = None
    """ Plugin to calculate dependencies """

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.plugin_downloader.plugin_downloading_system
        import misc.plugin_downloader.console_plugin_downloader
        self.plugin_downloader = misc.plugin_downloader.plugin_downloading_system.PluginDownloader(self)
        self.console_plugin_downloader = misc.plugin_downloader.console_plugin_downloader.ConsolePluginDownloader(self)
        self.plugin_downloader.load_plugin_downloader()

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

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)
        if colony.plugins.plugin_system.is_capability_or_sub_capability_in_list("download", plugin.capabilities):
            self.downloader_plugin = plugin
        elif colony.plugins.plugin_system.is_capability_or_sub_capability_in_list("zip", plugin.capabilities):
            self.zip_plugin = plugin
        elif colony.plugins.plugin_system.is_capability_or_sub_capability_in_list("dependencies_calculator", plugin.capabilities):
            self.dependencies_calculator_plugin = plugin

    def get_console_extension_name(self):
        return self.console_plugin_downloader.get_console_extension_name()

    def get_all_commands(self):
        return self.console_plugin_downloader.get_all_commands()

    def get_handler_command(self, command):
        return self.console_plugin_downloader.get_handler_command(command)

    def get_help(self):
        return self.console_plugin_downloader.get_help()
