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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CACHE_DIRECTORY_IDENTIFIER = "cache_generated"
""" The cache directory identifier """

class MainCacheManager:
    """
    The main cache manager class.
    """

    main_cache_manager_plugin = None
    """ The main cache manager plugin """

    def __init__(self, main_cache_manager_plugin):
        """
        Constructor of the class.

        @type main_cache_manager_plugin: MainCacheManagerPlugin
        @param main_cache_manager_plugin: The main cache manager plugin.
        """

        self.main_cache_manager_plugin = main_cache_manager_plugin

    def get_cache_directory_path(self):
        """
        Retrieves the default cache directory path.

        @rtype: String
        @return: The default cache directory path.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_cache_manager_plugin.manager

        # retrieves the configuration path for the main cache manager plugin
        _configuration_path, workspace_path = plugin_manager.get_plugin_configuration_paths_by_id(self.main_cache_manager_plugin.id)

        # creates the full cache directory path appending
        # the cache generated part to the workspace path
        cache_directory_path = workspace_path + "/" + CACHE_DIRECTORY_IDENTIFIER

        # returns the cache directory path
        return cache_directory_path

    def generate_cache_context(self, parameters):
        """
        Generates a new cache context using the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to the cache context generation.
        @rtype: CacheContext
        @return: The generated cache context.
        """

        return self.main_cache_manager.generate_cache_context(parameters)

class CacheContext:
    """
    The cache context class.
    """

    def __init__(self):
        pass
