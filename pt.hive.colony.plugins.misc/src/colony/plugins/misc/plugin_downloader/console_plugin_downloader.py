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

CONSOLE_EXTENSION_NAME = "plugin_downloader"
INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
INVALID_ADDRESS_MESSAGE = "invalid address"
HELP_TEXT = "### PLUGIN DOWNLOADER HELP ###\n\
plugindownload <plugin-id> [plugin-version]     - starts the download of the plugin\n\
plugintestdownload <plugin-id> [plugin-version] - test the download of the plugin"

#@todo: review and comment this file
class ConsolePluginDownloader:

    commands = ["plugindownload", "plugintestdownload"]

    plugin_downloader_plugin = None

    def __init__(self, plugin_downloader_plugin = None):
        self.plugin_downloader_plugin = plugin_downloader_plugin

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_plugindownload(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return
        
        plugin_identifier = args[0]

        if len(args) == 1:
            self.plugin_downloader_plugin.plugin_downloader.download_plugin(plugin_identifier)
        else:
            plugin_version = args[1]
            self.plugin_downloader_plugin.plugin_downloader.download_plugin(plugin_identifier, plugin_version)

    def process_plugintestdownload(self, args, output_method):
        pass
