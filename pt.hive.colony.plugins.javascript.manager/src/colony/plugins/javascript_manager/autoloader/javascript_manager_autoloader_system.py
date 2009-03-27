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

__revision__ = "$LastChangedRevision: 2092 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-03-20 13:54:09 +0000 (sex, 20 Mar 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import stat
import time
import threading
import os.path

DEFAULT_UPDATING_TIME = 5
""" The default updating time """

class JavascriptManagerAutoloader:
    """
    The javascript manager autoloader class.
    """

    javascript_manager_autoloader_plugin = None
    """ The javascript manager autoloader plugin """

    javascript_manager_last_update_timestamp = None
    """ The javascript manager last update timestamp """

    plugin_id_modified_date_map = {}
    """ The map that relates the plugin id with it's modification date """

    def __init__(self, javascript_manager_autoloader_plugin):
        """
        Constructor of the class.
        
        @type javascript_manager_autoloader_plugin: JavascriptManagerAutoloaderPlugin
        @param javascript_manager_autoloader_plugin: The javascript manager autoloader plugin.
        """

        self.javascript_manager_autoloader_plugin = javascript_manager_autoloader_plugin

        self.plugin_id_modified_date_map = {}

    def auto_update_plugin_files(self):
        # launches the auto update plugin files system
        threading.Timer(DEFAULT_UPDATING_TIME, self.auto_update_plugin_files_handler, ()).start()

    def auto_update_plugin_files_handler(self):
        # updates the plugin files
        self.update_plugin_files()

        # re-launches the auto update plugin files system
        self.auto_update_plugin_files()

    def update_plugin_files(self):
        # prints debug message
        self.javascript_manager_autoloader_plugin.debug("Starting update of plugin files")
        
        # retrieves the javascript manager plugin
        javascript_manager_plugin = self.javascript_manager_autoloader_plugin.javascript_manager_plugin

        # retrieves the javascript manager
        javascript_manager = javascript_manager_plugin.javascript_manager

        # retrieves the plugin search directories list
        plugin_search_directories_list = javascript_manager_plugin.get_plugin_search_directories_list()

        # retrieves the plugin descriptor parser
        plugin_descriptor_parser_class = javascript_manager_plugin.get_plugin_descriptor_parser()

        # iterates over all the plugin search directories
        for plugin_search_directory in plugin_search_directories_list:
            # in case the javascript plugins directory exists
            if os.path.exists(plugin_search_directory):
                # the list of files in the javascript plugins directory
                dir_list = os.listdir(plugin_search_directory)

                # for all the files in the directory 
                for file_name in dir_list:
                    # retrieves the file full path
                    full_path = plugin_search_directory + "/" + file_name

                    # retrieves the file stat value
                    file_stat = os.stat(full_path)

                    # retrieves the file last modification time
                    modified_date = time.localtime(file_stat[stat.ST_MTIME])

                    # retrieves the file mode
                    mode = file_stat[stat.ST_MODE]

                    # splits the file name
                    split = os.path.splitext(file_name)

                    # retrieves the extension name
                    extension_name = split[-1]

                    # in case it's not a directory and the extension of the file is .xml (xml file)
                    if not stat.S_ISDIR(mode) and extension_name == ".xml":
                        # creates the plugin descriptor parser for the xml file
                        plugin_descriptor_parser = plugin_descriptor_parser_class(full_path)

                        # parses the xml files
                        plugin_descriptor_parser.parse()

                        # retrieves the plugin descriptor resultant of the parsing
                        plugin_descriptor = plugin_descriptor_parser.get_value()

                        # retrieves the plugin id from the plugin descriptor
                        plugin_id = plugin_descriptor.id;

                        # in case it is an updated version of the plugin
                        if plugin_id in self.plugin_id_modified_date_map:
                            # retrieves the current modified date
                            current_modified_date = self.plugin_id_modified_date_map[plugin_id]

                            # in case the mofied date is greater that the current modified date 
                            if modified_date > current_modified_date:
                                # prints a log message
                                self.javascript_manager_autoloader_plugin.debug("Javascript plugin %s updated" % plugin_id)

                                # sets the mofied date in the plugin id modified date map
                                self.plugin_id_modified_date_map[plugin_id] = modified_date
                        elif plugin_id in javascript_manager.plugin_id_plugin_descriptor_map:
                            # prints a log message
                            self.javascript_manager_autoloader_plugin.debug("Javascript plugin %s inserted in autoloading structures" % plugin_id)

                            # sets the mofied date in the plugin id modified date map
                            self.plugin_id_modified_date_map[plugin_id] = modified_date
                        else:
                            # prints a log message
                            self.javascript_manager_autoloader_plugin.debug("Javascript plugin %s added" % plugin_id)

                            # adds the plugin descriptor to the list of plugin descriptors
                            # in the javascript manager
                            javascript_manager.plugin_descriptors_list.append(plugin_descriptor)

                            # sets the plugin descriptor in the plugin id plugin descriptor map
                            javascript_manager.plugin_id_plugin_descriptor_map[plugin_id] = plugin_descriptor

                            # sets the mofied date in the plugin id modified date map
                            self.plugin_id_modified_date_map[plugin_id] = modified_date

                            # @todo change this into a more soft way (too expensive now)
                            javascript_manager.index_plugin_search_directories()

        # creates a new timestamp for the update
        self.javascript_manager_last_update_timestamp = time.time();

        # prints debug message
        self.javascript_manager_autoloader_plugin.debug("Ending update of plugin files")

    def update_plugin_manager(self):
        self.update_plugin_files()

    def get_status_plugins(self, timestamp):
        # converts the timestamp to local time
        local_timestamp = time.localtime(timestamp)

        # retrieves the current timestamp
        current_timestamp = time.time()

        # in case it's the first call (timestamp is 0), ignore the request
        if timestamp == 0:
            updated_plugins = []
        else:
            # retrieves the list of updated plugins since the timestamp
            updated_plugins = self.get_updated_plugins_from_local_timestamp(local_timestamp)

        # creates the status map for the response
        status_map = {"timestamp" : current_timestamp,
                      "updated_plugins" : updated_plugins}

        # returns the status map
        return status_map

    def get_updated_plugins_from_local_timestamp(self, local_timestamp):
        """
        Retrieves the list of all the updated plugins since the time in
        the given local timestamp.
        
        @type local_timestamp: TimestampTuple
        @param local_timestamp: The local timestamp to retrieve the updated plugins.
        @rtype: List
        @return: The list of all the updated plugins since the time in
        the given local timestamp.
        """

        # the list of updated plugins
        updated_plugins = []

        for plugin_id, modified_date in self.plugin_id_modified_date_map.items():
            if modified_date >= local_timestamp:
                updated_plugins.append(plugin_id)

        return updated_plugins

class List:
    """
    The generic List class.
    """

    list = []
    """ The list object for javascript list """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.list = []
