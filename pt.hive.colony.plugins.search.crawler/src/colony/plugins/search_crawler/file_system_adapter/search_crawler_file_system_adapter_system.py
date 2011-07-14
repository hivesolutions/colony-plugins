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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

import search_crawler_file_system_adapter_exceptions

SEARCH_CRAWLER_ADAPTER_TYPE = "file_system"
""" The search crawler adapter type """

START_PATH_VALUE = "start_path"
""" The key for the start path parameter in the properties map """

TOKEN_LIST_VALUE = "token_list"
""" The key for the token list in the properties map """

FILE_PATH_VALUE = "file_path"
""" The key for the file path to crawl, in the properties map """

FILE_PATH_SLASH = "/"
""" The standard file path hierarchy indicator """

class SearchCrawlerFileSystemAdapter:
    """
    The search crawler file system adapter class.
    """

    search_crawler_file_system_adapter_plugin = None
    """ The search crawler file system adapter plugin """

    def __init__(self, search_crawler_file_system_adapter_plugin):
        """
        Constructor of the class.

        @type search_crawler_file_system_adapter_plugin: SearchCrawlerFileSystemAdapterPlugin
        @param search_crawler_file_system_adapter_plugin: The search crawler file system adapter plugin.
        """

        self.search_crawler_file_system_adapter_plugin = search_crawler_file_system_adapter_plugin

    def get_type(self):
        return SEARCH_CRAWLER_ADAPTER_TYPE

    def get_tokens(self, properties):
        if not START_PATH_VALUE in properties:
            raise search_crawler_file_system_adapter_exceptions.MissingProperty(START_PATH_VALUE)

        # retrieves the start path
        start_path = properties[START_PATH_VALUE]

        # creates the token list
        token_list = []
        properties[TOKEN_LIST_VALUE] = token_list

        # start the path walking in the start path
        os.path.walk(start_path, self.walker, properties)

        # returns the token list
        return token_list

    def walker(self, args, directory_name, names):
        """
        The walker method, that iterates through all the
        search provider text file plugins.

        @type args: Object
        @param args: The walker arguments.
        @type directory_name: String
        @param directory_name: The directory name.
        @type names: List
        @param names: The name of the files of the current directory.
        """

        # retrieves the token list
        properties = args
        token_list = properties[TOKEN_LIST_VALUE]

        # creates the file paths list
        file_paths_list = [directory_name + FILE_PATH_SLASH + value for value in names]

        # iterates over all the file paths
        for file_path in file_paths_list:
            # sets the properties for the handler plugin
            properties[FILE_PATH_VALUE] = file_path

            search_provider_file_system_plugin = self.get_handler_plugin(properties)

            if search_provider_file_system_plugin:
                tokens = search_provider_file_system_plugin.get_tokens(properties)
                token_list.append(tokens)

    def get_handler_plugin(self, properties):
        search_provider_file_system_plugins = self.search_crawler_file_system_adapter_plugin.search_provider_file_system_plugins

        for search_provider_file_system_plugin in search_provider_file_system_plugins:
            if search_provider_file_system_plugin.is_file_provider(properties):
                return search_provider_file_system_plugin
