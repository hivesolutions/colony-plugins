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

import os
import sys
import time
import stat

import os.path

SLEEP_TIME_VALUE = 1
""" The sleep time value """

class Autoloader:
    """
    The autoloader class.
    """

    autoloader_plugin = None
    """ The autoloader plugin """

    manager = None
    """ The plugin manager """

    continue_flag = True
    """ The continue flag that controls the autoloading system """

    search_directories = []
    """ The search directories list """

    search_directories_information_map = {}
    """ The search directories information map """

    def __init__(self, autoloader_plugin):
        """
        Constructor of the class.

        @type autoloader_plugin: AutoloaderPlugin
        @param autoloader_plugin: The autoloader plugin.
        """

        self.autoloader_plugin = autoloader_plugin
        self.manager = autoloader_plugin.manager

        self.search_directories = []

    def load_autoloader(self):
        # iterates over all the plugin manager paths
        for plugin_path in self.manager.plugin_paths:
            # adds the search path
            self.add_search_directory(plugin_path)

        # notifies the ready semaphore
        self.autoloader_plugin.release_ready_semaphore()

        # while the flag is active
        while self.continue_flag:
            for search_directory in self.search_directories:
                # in case the search directory does not exists
                if not os.path.exists(search_directory):
                    # passes iteration
                    pass

                if search_directory in self.search_directories_information_map:
                    for file_name in self.search_directories_information_map[search_directory]:
                        self.search_directories_information_map[search_directory][file_name].exists = False
                    new_flag = False
                else:
                    self.search_directories_information_map[search_directory] = {}
                    new_flag = True

                # retrieves the directories list
                dir_list = os.listdir(search_directory)

                # for all the files in the directory
                for file_name in dir_list:
                    full_path = search_directory + "/" + file_name
                    file_stat = os.stat(full_path)
                    modified_date = time.localtime(file_stat[stat.ST_MTIME])
                    mode = file_stat[stat.ST_MODE]
                    split = os.path.splitext(file_name)
                    module_name = "".join(split[:-1])
                    extension_name = split[-1]

                    # in case it's not a directory and the extension of the file is .py (python file)
                    if not stat.S_ISDIR(mode) and extension_name == ".py":
                        if file_name in self.search_directories_information_map[search_directory]:
                            file_information = self.search_directories_information_map[search_directory][file_name]
                            file_properties = file_information.file_properties
                            if not modified_date == file_properties.modified_date:
                                # tries to retrieve the plugin from the plugin manager using the module name
                                plugin = self.manager.get_plugin_by_module_name(module_name)

                                # in case the plugin is already loaded in the plugin manager
                                if plugin:
                                    self.reload_module(plugin, module_name)
                                else:
                                    self.load_module(search_directory, module_name)

                                # sets the new modified date
                                file_properties.modified_date = modified_date
                            file_information.exists = True
                        else:
                            file_properties = FileProperties(modified_date)
                            file_information = FileInformation(file_name, file_properties, True)
                            self.search_directories_information_map[search_directory][file_name] = file_information

                            if not new_flag:
                                self.load_module(search_directory, module_name)

                # the list of file names to be removed
                remove_list = []

                for file_name in self.search_directories_information_map[search_directory]:
                    file_information = self.search_directories_information_map[search_directory][file_name]
                    if not file_information.exists:
                        remove_list.append(file_name)

                # removes all the modules in the remove list
                for remove_item in remove_list:
                    split = os.path.splitext(remove_item)
                    module_name = "".join(split[:-1])
                    self.unload_module(module_name)
                    del self.search_directories_information_map[search_directory][remove_item]

            # sleeps for the given sleep time
            time.sleep(SLEEP_TIME_VALUE)

    def load_module(self, search_directory, module_name):
        try:
            self.autoloader_plugin.info("Loading module " + module_name)
            if not search_directory in sys.path:
                sys.path.insert(0, search_directory)
            self.manager.load_plugins([module_name])
            self.manager.start_plugins()
        except:
            self.autoloader_plugin.info("There was a problem loading module " + module_name)

    def unload_module(self, module_name):
        try:
            self.autoloader_plugin.info("Unloading module " + module_name)
            self.manager.stop_module(module_name)
        except:
            self.autoloader_plugin.info("There was a problem unloading module " + module_name)

    def reload_module(self, plugin, module_name):
        try:
            self.autoloader_plugin.info("Reloading module " + module_name)

            # retrieves the plugin id
            plugin_id = plugin.id

            # retrieves the loaded plugins
            loaded_plugins = self.manager.get_all_loaded_plugins()

            # creates a new list for the loaded plugins ids
            loaded_plugins_ids = []

            # iterates over all the loaded plugins
            for loaded_plugin in loaded_plugins:
                loaded_plugins_ids.append(loaded_plugin.id)

            # stops the module
            self.manager.stop_module(module_name)

            # loads the plugins for the module name
            self.manager.load_plugins([module_name])

            # starts all the plugins in the plugin manager
            self.manager.start_plugins()

            # retrieves the plugin using the plugin id
            plugin = self.manager._get_plugin_by_id(plugin_id)

            # reloads the main modules
            plugin.reload_main_modules()

            # iterates over all the loaded plugins ids
            for loaded_plugin_id in loaded_plugins_ids:
                # tries to load the plugin with the given id
                self.manager.load_plugin(loaded_plugin_id)
        except:
            self.autoloader_plugin.error("There was a problem reloading module " + module_name)

    def unload_autoloader(self):
        self.continue_flag = False

    def add_search_path(self):
        self.search_directories.extend(sys.path)

    def add_search_directory(self, path):
        self.search_directories.append(path)

class FileInformation:
    """
    The file information class.
    """

    filename = "none"
    file_properties = None
    exists = False

    def __init__(self, filename = "none", file_properties = None, exists = False):
        self.filename = filename
        self.file_properties = file_properties
        self.exists = exists

class FileProperties:
    """
    The file properties class.
    """

    modified_date = None

    def __init__(self, modified_date = None):
        self.modified_date = modified_date
