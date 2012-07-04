#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "downloader"
""" The console extension name """

class ConsoleDownloader:
    """
    The console downloader class.
    """

    downloader_plugin = None
    """ The downloader plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, downloader_plugin):
        """
        Constructor of the class.

        @type downloader_plugin: DownloaderPlugin
        @param downloader_plugin: The downloader plugin.
        """

        self.downloader_plugin = downloader_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_download(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the download command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the downloader instance
        downloader = self.downloader_plugin.downloader

        # retrieves the file path from the arguments
        file_path = arguments_map["file_path"]

        # creates a new set of handlers map to be used in the current
        # command line execution context
        handlers_map = console_context and console_context.create_handlers_map(output_method) or {}

        try:
            # downloads the specified file, and notifies the appropriate
            # handlers for messages
            downloader.download_package(file_path, handlers_map = handlers_map)
        finally:
            # flushes the handlers map, avoids possible data
            # synchronization problems
            console_context and console_context.flush_handlers_map(handlers_map)

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "download" : {
                "handler" : self.process_download,
                "description" : "starts the download of the file",
                "arguments" : [
                    {
                        "name" : "file_path",
                        "description" : "the path of the file to download",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            }
        }

        # returns the commands map
        return commands_map
