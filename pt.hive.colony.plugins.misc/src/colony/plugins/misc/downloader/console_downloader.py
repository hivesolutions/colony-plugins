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

__revision__ = "$LastChangedRevision: 2096 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 13:02:08 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
INVALID_ADDRESS_MESSAGE = "invalid address"
HELP_TEXT = "### DOWNLOADER HELP ###\n\
download <file-address> - starts the download of the file\n\
testdownload <file-address> - test the download of the file"

#@todo: review and comment this file
class ConsoleDownloader:

    commands = ["download", "testdownload"]

    downloader_plugin = None

    def __init__(self, downloader_plugin = None):
        self.downloader_plugin = downloader_plugin

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_download(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        file_path = args[0]

        output_method("starting download of " + file_path)

        self.downloader_plugin.downloader.download_package(file_path)

    def process_testdownload(self, args, output_method):
        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        file_path = args[0]

        output_method("starting test of " + file_path)

        self.downloader_plugin.downloader.test_package(file_path)
