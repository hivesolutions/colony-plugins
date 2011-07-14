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
import types
import threading

import colony.libs.update_thread_util

DEFAULT_UPDATING_TIME = 3
""" The default updating time """

DEFAULT_LIMIT_COUNTER = 10
""" The default limit counter """

class JavascriptManagerAutoloader:
    """
    The javascript manager autoloader class.
    """

    javascript_manager_autoloader_plugin = None
    """ The javascript manager autoloader plugin """

    javascript_manager_last_update_timestamp = None
    """ The javascript manager last update timestamp """

    update_plugin_lock = None
    """ The update plugin lock """

    auto_update_plugin_files_flag = None
    """ The auto update plugin files flag """

    auto_update_plugin_files_timer = None
    """ The auto update plugin files timer """

    auto_update_plugin_files_timeout_counter = 0
    """ The auto update plugin files timeout counter """

    plugin_id_modified_date_map = {}
    """ The map that relates the plugin id with it's modification date """

    plugin_id_removal_date_map = {}
    """ The map that relates the plugin id with it's removal date """

    plugin_id_file_modified_date_map = {}
    """ The map that relates the plugin id with it's file modification date """

    def __init__(self, javascript_manager_autoloader_plugin):
        """
        Constructor of the class.

        @type javascript_manager_autoloader_plugin: JavascriptManagerAutoloaderPlugin
        @param javascript_manager_autoloader_plugin: The javascript manager autoloader plugin.
        """

        self.javascript_manager_autoloader_plugin = javascript_manager_autoloader_plugin

        self.update_plugin_lock = threading.Lock()

        self.plugin_id_modified_date_map = {}
        self.plugin_id_removal_date_map = {}
        self.plugin_id_file_modified_date_map = {}

    def start_auto_update_plugin_files(self):
        self.auto_update_plugin_files_flag = True
        self.auto_update_plugin_files()

    def stop_auto_update_plugin_files(self):
        # unsets the auto update plugin files flag
        self.auto_update_plugin_files_flag = False

        # in case the auto update plugin files timer is defined
        if self.auto_update_plugin_files_timer:
            # stops the auto update plugin files system
            self.auto_update_plugin_files_timer.stop()

    def auto_update_plugin_files(self):
        # in case the auto update plugin files flag is active
        if self.auto_update_plugin_files_flag:
            # creates the auto update plugin files timer timer thread
            self.auto_update_plugin_files_timer = colony.libs.update_thread_util.UpdateThread()

            # sets the timeout in the auto update plugin files timer timer thread
            self.auto_update_plugin_files_timer.set_timeout(DEFAULT_UPDATING_TIME)

            # sets the call method in the auto update plugin files timer timer thread
            self.auto_update_plugin_files_timer.set_call_method(self.auto_update_plugin_files_handler)

            # starts the auto update plugin files system
            self.auto_update_plugin_files_timer.start()

    def auto_update_plugin_files_handler(self):
        # in case the auto update plugin files timeout counter is zero
        if self.auto_update_plugin_files_timeout_counter == 0:
            # updates the plugin files
            self.update_plugin_files()

            # resets the auto update plugin files timeout counter
            self.auto_update_plugin_files_timeout_counter = DEFAULT_LIMIT_COUNTER

        # decrements the auto update plugin files timeout counter
        self.auto_update_plugin_files_timeout_counter -= 1

    def update_plugin_files(self):
        # prints debug message
        self.javascript_manager_autoloader_plugin.debug("Starting update of plugin files")

        # acquires the update plugin lock
        self.update_plugin_lock.acquire()

        # retrieves the javascript manager plugin
        javascript_manager_plugin = self.javascript_manager_autoloader_plugin.javascript_manager_plugin

        # retrieves the javascript manager
        javascript_manager = javascript_manager_plugin.javascript_manager

        # retrieves the plugin search directories lock
        plugin_search_directories_lock = javascript_manager.plugin_search_directories_lock

        # acquires the plugin search directories lock
        plugin_search_directories_lock.acquire()

        try:
            # retrieves the plugin search directories map
            plugin_search_directories_map = javascript_manager_plugin.get_plugin_search_directories_map()

            # retrieves the plugin descriptor parser
            plugin_descriptor_parser_class = javascript_manager_plugin.get_plugin_descriptor_parser()

            # the list of available plugin ids list
            available_plugin_id_list = []

            # iterates over all the items in the plugin search directories map
            for plugin_search_directory_item_file_name, plugin_search_directory_item_full_path in plugin_search_directories_map.items():
                # in case the plugin search directory item exists
                if not type(plugin_search_directory_item_full_path) == types.DictionaryType and os.path.exists(plugin_search_directory_item_full_path):
                    # retrieves the file stat value
                    file_stat = os.stat(plugin_search_directory_item_full_path)

                    # retrieves the file last modification time
                    modified_date = time.localtime(file_stat[stat.ST_MTIME])

                    # retrieves the file mode
                    mode = file_stat[stat.ST_MODE]

                    # splits the file name
                    split = os.path.splitext(plugin_search_directory_item_file_name)

                    # retrieves the extension name
                    extension_name = split[-1]

                    # in case it's not a directory and the extension of the file is .xml (xml file)
                    if not stat.S_ISDIR(mode) and extension_name == ".xml":
                        # creates the plugin descriptor parser for the xml file
                        plugin_descriptor_parser = plugin_descriptor_parser_class(plugin_search_directory_item_full_path)

                        # parses the xml files
                        plugin_descriptor_parser.parse()

                        # retrieves the plugin descriptor resultant of the parsing
                        plugin_descriptor = plugin_descriptor_parser.get_value()

                        # retrieves the plugin id from the plugin descriptor
                        plugin_id = plugin_descriptor.id

                        # in case it is an updated version of the plugin
                        if plugin_id in self.plugin_id_file_modified_date_map:
                            # retrieves the current file modified date
                            current_file_modified_date = self.plugin_id_file_modified_date_map[plugin_id]

                            # in case the modified date is greater that the current file modified date
                            if modified_date > current_file_modified_date:
                                # prints a log message
                                self.javascript_manager_autoloader_plugin.debug("Javascript plugin %s updated" % plugin_id)

                                # sets the modified date in the plugin id modified date map
                                self.plugin_id_modified_date_map[plugin_id] = time.localtime()

                                # sets the modified date in the plugin id file emodified date map
                                self.plugin_id_file_modified_date_map[plugin_id] = modified_date
                        elif plugin_id in javascript_manager.plugin_id_plugin_descriptor_map:
                            # prints a log message
                            self.javascript_manager_autoloader_plugin.debug("Javascript plugin %s inserted in autoloading structures" % plugin_id)

                            # sets the modified date in the plugin id modified date map
                            self.plugin_id_modified_date_map[plugin_id] = time.localtime(javascript_manager.javascript_manager_last_update_timestamp)

                            # sets the modified date in the plugin id file emodified date map
                            self.plugin_id_file_modified_date_map[plugin_id] = modified_date
                        else:
                            # prints a log message
                            self.javascript_manager_autoloader_plugin.debug("Javascript plugin %s added" % plugin_id)

                            # adds the plugin descriptor to the list of plugin descriptors
                            # in the javascript manager
                            javascript_manager.plugin_descriptors_list.append(plugin_descriptor)

                            # sets the plugin descriptor in the plugin id plugin descriptor map
                            javascript_manager.plugin_id_plugin_descriptor_map[plugin_id] = plugin_descriptor

                            # sets the modified date in the plugin id modified date map
                            self.plugin_id_modified_date_map[plugin_id] = time.localtime(javascript_manager.javascript_manager_last_update_timestamp)

                            # sets the modified date in the plugin id file emodified date map
                            self.plugin_id_file_modified_date_map[plugin_id] = modified_date

                            # in case the plugin id exists in the plugin id removal date map
                            if plugin_id in self.plugin_id_removal_date_map:
                                # unsets the plugin id in the plugin id removal date map
                                del self.plugin_id_removal_date_map[plugin_id]

                        # adds the plugin id to the list of available plugins
                        available_plugin_id_list.append(plugin_id)

            # retrieves the list of not available plugin id
            not_available_plugin_id_list = [plugin_id for plugin_id in self.plugin_id_modified_date_map if not plugin_id in available_plugin_id_list]

            # iterates over all the not available plugin id
            # to remove the plugins from the javascript manager
            for not_available_plugin_id in not_available_plugin_id_list:
                # prints a log message
                self.javascript_manager_autoloader_plugin.debug("Javascript plugin %s removed" % not_available_plugin_id)

                # retrieves the not available plugin descriptor
                not_available_plugin_descritor = javascript_manager.plugin_id_plugin_descriptor_map[not_available_plugin_id]

                # removes the plugin descriptor to the list of plugin descriptors
                # in the javascript manager
                javascript_manager.plugin_descriptors_list.remove(not_available_plugin_descritor)

                # unsets the plugin descriptor in the plugin id plugin descriptor map
                del javascript_manager.plugin_id_plugin_descriptor_map[not_available_plugin_id]

                # unsets the modified date in the plugin id modified date map
                del self.plugin_id_modified_date_map[not_available_plugin_id]

                # unsets the modified date in the plugin id file modified date map
                del self.plugin_id_file_modified_date_map[not_available_plugin_id]

                # sets the removal date in the plugin id removal date map
                self.plugin_id_removal_date_map[not_available_plugin_id] = time.localtime()

            # updates the timestamp with the javascript manager timestamp
            self.javascript_manager_last_update_timestamp = javascript_manager.javascript_manager_last_update_timestamp
        finally:
            # releases the plugin search directories lock
            plugin_search_directories_lock.release()

            # releases the update plugin lock
            self.update_plugin_lock.release()

        # prints debug message
        self.javascript_manager_autoloader_plugin.debug("Ending update of plugin files")

    def update_plugin_manager(self):
        self.update_plugin_files()

    def get_status_plugins(self, timestamp):
        # converts the timestamp to local time
        local_timestamp = time.localtime(timestamp)

        # acquires the update plugin lock
        self.update_plugin_lock.acquire()

        try:
            # retrieves the current timestamp
            current_timestamp = self.javascript_manager_last_update_timestamp

            # in case it's the first call (timestamp is 0), ignore the request
            if timestamp == 0:
                # sets the updated plugins list as empty (initialization)
                updated_plugins = []

                # sets the removed plugins list as empty (initialization)
                removed_plugins = []
            else:
                # retrieves the list of updated plugins since the timestamp
                updated_plugins = self.get_updated_plugins_from_local_timestamp(local_timestamp)

                # retrieves the list of removed plugins since the timestamp
                removed_plugins = self.get_removed_plugins_from_local_timestamp(local_timestamp)
        finally:
            # releases the update plugin lock
            self.update_plugin_lock.release()

        # creates the status map for the response
        status_map = {
            "timestamp" : current_timestamp,
            "updated_plugins" : updated_plugins,
            "removed_plugins" : removed_plugins
        }

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

        # retrieves the current timestamp
        current_timestamp = self.javascript_manager_last_update_timestamp

        # converts the current timestamp to local time
        local_current_timestamp = time.localtime(current_timestamp)

        # the list of updated plugins
        updated_plugins = []

        # iterates over all the items in the plugin id modified date map
        for plugin_id, modified_date in self.plugin_id_modified_date_map.items():
            # in case the modified date is located between the given local timestamp
            # and the current (last update) timestamp
            if modified_date > local_timestamp and modified_date <= local_current_timestamp:
                # appends the plugin id to the list of updated plugins
                updated_plugins.append(plugin_id)

        # returns the updated plugins
        return updated_plugins

    def get_removed_plugins_from_local_timestamp(self, local_timestamp):
        """
        Retrieves the list of all the removed plugins since the time in
        the given local timestamp.

        @type local_timestamp: TimestampTuple
        @param local_timestamp: The local timestamp to retrieve the removed plugins.
        @rtype: List
        @return: The list of all the removed plugins since the time in
        the given local timestamp.
        """

        # retrieves the current timestamp
        current_timestamp = self.javascript_manager_last_update_timestamp

        # converts the current timestamp to local time
        local_current_timestamp = time.localtime(current_timestamp)

        # the list of removed plugins
        removed_plugins = []

        # iterates over all the items in the plugin id removal date map
        for plugin_id, removal_date in self.plugin_id_removal_date_map.items():
            # in case the removal date is located between the given local timestamp
            # and the current (last update) timestamp
            if removal_date > local_timestamp and removal_date <= local_current_timestamp:
                # appends the plugin id to the list of removed plugins
                removed_plugins.append(plugin_id)

        # returns the removed plugins
        return removed_plugins

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
