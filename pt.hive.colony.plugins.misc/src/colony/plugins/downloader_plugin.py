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

import colony.base.plugin_system
import colony.base.decorators

class DownloaderPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Downloader plugin.
    """

    id = "pt.hive.colony.plugins.misc.downloader"
    name = "Downloader Plugin"
    short_name = "Downloader"
    description = "Downloader Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/misc/downloader/resources/baf.xml"
    }
    capabilities = [
        "download",
        "_console_command_extension",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.client.http", "1.0.0")
    ]
    main_modules = [
        "misc.downloader.console_downloader",
        "misc.downloader.downloader_exceptions",
        "misc.downloader.downloader_system"
    ]

    downloader = None
    """ The downloader """

    console_downloader = None
    """ The console downloader """

    main_client_http_plugin = None
    """ The main client http plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import misc.downloader.downloader_system
        import misc.downloader.console_downloader
        self.downloader = misc.downloader.downloader_system.Downloader(self)
        self.console_downloader = misc.downloader.console_downloader.ConsoleDownloader(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.misc.downloader", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def download_package(self, address, target_directory):
        return self.downloader.download_package(address, target_directory)

    def test_package(self, address):
        return self.downloader.test_package(address)

    def get_download_package_stream(self, address):
        return self.downloader.get_download_package_stream(address)

    def get_console_extension_name(self):
        return self.console_downloader.get_console_extension_name()

    def get_commands_map(self):
        return self.console_downloader.get_commands_map()

    def get_main_client_http_plugin(self):
        return self.main_client_http_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.client.http")
    def set_main_client_http_plugin(self, main_client_http_plugin):
        self.main_client_http_plugin = main_client_http_plugin
