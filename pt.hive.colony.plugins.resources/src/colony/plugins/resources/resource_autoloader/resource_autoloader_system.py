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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

SLEEP_TIME_VALUE = 1.0
""" The sleep time value """

class ResourceAutoloader:
    """
    The resource autoloader
    """

    def __init__(self, resource_autoloader_plugin):
        """
        Constructor of the class.

        @type resource_autoloader_plugin: Plugin
        @param resource_autoloader_plugin: The resource autoloader plugin.
        """

        self.resource_autoloader_plugin = resource_autoloader_plugin

    def load_autoloader(self):
        """
        Loads the autoloader starting all the necessary structures
        and setting the update time.
        The autoloader runs continuously until the continue
        flag is unset.
        """

        # retrieves the plugin manager
        plugin_manager = self.resource_autoloader_plugin.manager

        # retrieves the meta paths
        meta_paths = plugin_manager.get_meta_paths()

        # notifies the ready semaphore
        self.autoloader_plugin.release_ready_semaphore()

        # while the flag is active
        while self.continue_flag:
            # iterates over all the meta paths
            for meta_path in meta_paths:
                print meta_path
                # iterates over all the search directories
            #    for search_directory in meta_paths:
                    # analyzes the given search directory
            #        self.analyze_search_directory(search_directory)

            # sleeps for the given sleep time
            time.sleep(SLEEP_TIME_VALUE)
