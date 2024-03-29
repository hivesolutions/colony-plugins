#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony


class DownloaderPlugin(colony.Plugin):
    """
    The main class for the Downloader plugin.
    """

    id = "pt.hive.colony.plugins.misc.downloader"
    name = "Downloader"
    description = "Downloader Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT]
    capabilities = ["download", "console_command_extension"]
    dependencies = [colony.PluginDependency("pt.hive.colony.plugins.client.http")]
    main_modules = ["downloader_c"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import downloader_c

        self.system = downloader_c.Downloader(self)
        self.console = downloader_c.ConsoleDownloader(self)

    def download_package(self, address, target_directory):
        return self.system.download_package(address, target_directory)

    def download_package_handlers(self, address, target_directory, handlers_map):
        return self.system.download_package(address, target_directory, handlers_map)

    def get_download_package_stream(self, address):
        return self.system.get_download_package_stream(address)

    def get_download_package_stream_handlers(self, address, handlers_map):
        return self.system.get_download_package_stream(address, handlers_map)

    def get_console_extension_name(self):
        return self.console.get_console_extension_name()

    def get_commands_map(self):
        return self.console.get_commands_map()
