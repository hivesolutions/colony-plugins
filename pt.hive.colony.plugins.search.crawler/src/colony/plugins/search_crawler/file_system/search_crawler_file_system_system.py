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

import os.path

import search_crawler_file_system_exceptions

SEARCH_CRAWLER_TYPE = "file_system"

class SearchCrawlerFileSystem:
    """
    The search crawler file system class.
    """

    search_crawler_file_system_plugin = None
    """ The search crawler file system plugin """

    def __init__(self, search_crawler_file_system_plugin):
        """
        Constructor of the class.
        
        @type search_provider_text_plugin: SearchCrawlerFileSystemPlugin
        @param search_provider_text_plugin: The search crawler file system plugin.
        """

        self.search_crawler_file_system_plugin = search_crawler_file_system_plugin

    def get_type(self):
        return SEARCH_CRAWLER_TYPE

    def get_tokens(self, properties):
        if not "start_path" in properties:
            raise search_crawler_file_system_exceptions.MissingProperty("start_path")

        start_path = properties["start_path"]

        token_list = []

        os.path.walk(start_path, self.walker, token_list)

        return token_list

    def walker(self, args, directory_name, names):
        # open the directory
        
        # iterate through all the search provider text file plugins
        # have the search provider text file plugin process the file name

        token_list = args

        # creates the file paths list
        file_paths_list = [directory_name + "/" + value for value in names]

        for file_path in file_paths_list:
            properties = {"file_path" : file_path}

            search_provider_file_system_plugin = self.get_handler_plugin(properties)

            if search_provider_file_system_plugin:
                tokens = search_provider_file_system_plugin.get_tokens(properties)
                token_list.append(tokens)
    
    def get_handler_plugin(self, properties):
        search_provider_file_system_plugins = self.search_crawler_file_system_plugin.search_provider_file_system_plugins

        for search_provider_file_system_plugin in search_provider_file_system_plugins:
            if search_provider_file_system_plugin.is_file_provider(properties):
                return search_provider_file_system_plugin
