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

__author__ = "João Magalhães <joamag@hive.pt>"
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

import os
import sys
import time
import stat

SLEEP_TIME_VALUE = 10.0
""" The sleep time value """

SLEEP_STEP_VALUE = 0.5
""" The step value to be used for sleep """

LOAD_ACTION = 1
""" The load action value """

RELOAD_ACTION = 2
""" The reload action value """

UNLOAD_ACTION = 3
""" The unload action value """

class Autoloader:
    """
    The autoloader class.
    """

    autoloader_plugin = None
    """ The autoloader plugin """

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

        self.search_directories = []
        self.search_directories_information_map = {}

    def load_autoloader(self):
        """
        Loads the autoloader starting all the necessary structures
        and setting the update time.
        """

        # retrieves the plugin manager
        plugin_manager = self.autoloader_plugin.manager

        # retrieves the plugin paths
        plugin_paths = plugin_manager.get_plugin_paths()

        # adds the plugin paths to the search directories
        self.add_search_directories(plugin_paths)

        # notifies the ready semaphore
        self.autoloader_plugin.release_ready_semaphore()

        # sets the continue flag
        self.continue_flag = True

        # while the flag is active
        while self.continue_flag:
            # starts the operations list as an empty list
            # (will be populated with the proper actions)
            operations = []

            # iterates over all the search directories (lists)
            for search_directory_list in self.search_directories:
                # iterates over all the search directories
                for search_directory in search_directory_list:
                    # analyzes the given search directory
                    self.analyze_search_directory(search_directory, operations)

            # executes the various operations present in the operations
            # list (proper execution of the actions)
            self.execute_operations(operations)

            # sleeps for the given sleep time
            self._sleep(SLEEP_TIME_VALUE)

    def analyze_search_directory(self, search_directory, operations):
        """
        Analyzes the given search directory: loading, unloading or
        reloading the appropriate plugins.

        @type search_directory: String
        @param search_directory: The search directory to be analyzed.
        @type operations: List
        @param operations: The list to hold the various operations that
        compose the jounal of operations for the transaction unit.
        """

        # retrieves the plugin manager
        plugin_manager = self.autoloader_plugin.manager

        # in case the search directory does not exists
        if not os.path.exists(search_directory):
            # prints a debug message
            self.autoloader_plugin.debug("Search directory '%s' does not exist in the current filesystem" % (search_directory))

            # returns immediately
            return

        # iterates over all the search directories in the search directories information map
        if search_directory in self.search_directories_information_map:
            for file_name in self.search_directories_information_map[search_directory]:
                self.search_directories_information_map[search_directory][file_name].exists = False

            # unsets the new flag
            new_flag = False
        # otherwise
        else:
            # initializes the search directories information map for the
            # search directory information
            self.search_directories_information_map[search_directory] = {}

            # sets the new flag
            new_flag = True

        # retrieves the directories list
        dir_list = os.listdir(search_directory)

        # for all the files in the directory
        for file_name in dir_list:
            # constructs the full path from the seach directory and the file name
            full_path = search_directory + "/" + file_name

            # in case the search directory does not exists
            if not os.path.exists(full_path):
                # prints a debug message
                self.autoloader_plugin.debug("Path '%s' does not exist in the current filesystem" % (search_directory))

                # returns immediately
                return

            # retrieves the file stat
            file_stat = os.stat(full_path)

            # retrieves the modified date
            modified_date = time.localtime(file_stat[stat.ST_MTIME])

            # retrieves the mode
            mode = file_stat[stat.ST_MODE]

            # splits the file name
            split = os.path.splitext(file_name)

            # retrieves the module name
            module_name = "".join(split[:-1])

            # retrieves the extension name
            extension_name = split[-1]

            # in case it's not a directory and the extension of the file is .py (python file)
            # must be checked for previous existence or modification
            if not stat.S_ISDIR(mode) and extension_name == ".py":
                # in case the file name exists in the search directories information map
                # for the current search directory
                if file_name in self.search_directories_information_map[search_directory]:
                    # retrieves the file information for the given file name,
                    # then uses it to retrieve the file properties
                    file_information = self.search_directories_information_map[search_directory][file_name]
                    file_properties = file_information.file_properties

                    # in case the modified data is different from
                    # the modified date in the file properties (file changed)
                    if not modified_date == file_properties.modified_date:
                        # tries to retrieve the plugin from the plugin manager using
                        # the module name, in case the plugin does not exists an invalid
                        # reference is returned
                        plugin = plugin_manager.get_plugin_by_module_name(module_name)

                        # in case the plugin is already loaded in the plugin manager
                        # must use the reload approach to get the plugin updated,
                        # the state of the environment is not changed
                        if plugin: self.reload_module(plugin, module_name, operations = operations)

                        # otherwise the plugin is not loaded and the module
                        # must only be loaded in the plugin manager
                        else: self.load_module(search_directory, module_name, operations = operations)

                        # sets the new modified date
                        file_properties.modified_date = modified_date

                    # sets the file information exists flag as true
                    file_information.exists = True
                # otherwise the file must be new and a new
                # file information structure should be created
                else:
                    # creates a file properties instance for the given
                    # modified date
                    file_properties = FileProperties(modified_date)

                    # creates a new file information
                    file_information = FileInformation(file_name, file_properties, True)

                    # sets the file information in the search directories information map
                    # for the current file name and search directory
                    self.search_directories_information_map[search_directory][file_name] = file_information

                    # in case the new plugin manager loading is complete or
                    # the new flag is not set loads the module
                    (plugin_manager.init_complete or not new_flag) and self.load_module(search_directory, module_name, operations = operations)

        # the list of file names to be removed
        remove_list = []

        for file_name in self.search_directories_information_map[search_directory]:
            file_information = self.search_directories_information_map[search_directory][file_name]
            if not file_information.exists:
                # adds the file name to the remove
                # list (for file removal)
                remove_list.append(file_name)

        # removes all the modules in the remove list
        # (pending files for removal)
        for remove_item in remove_list:
            # splits the path of the remove item
            split = os.path.splitext(remove_item)

            # retrieves the module name
            module_name = "".join(split[:-1])

            # unloads the module for the given
            # module name
            self.unload_module(module_name, operations = operations)

            # deletes the search directories information map reference
            del self.search_directories_information_map[search_directory][remove_item]

    def execute_operations(self, operations):
        """
        Executes a series of journalized operation given as
        argument (provides deferred loading).

        This method is useful for situations where no synchronous
        loading is possible or wanted.

        @type operations: List
        @param operations: The list of operation tuples to be
        used to perform the concrete actions.
        """

        # in case the operations list is empty, no need
        # to perform any action (returns immediately)
        if not operations: return

        # retrieves the plugin manager reference for
        # latter usage
        plugin_manager = self.autoloader_plugin.manager

        # sorts the operations list in a reverse order so
        # that the unload operations are positioned first
        # for execution (avoids possible problems)
        operations.sort(reverse = True)

        # iterates over all the operations to be performed
        # to execute them in the correct order, this loop
        # is meant to execute only the unload operations
        for item in operations:
            # retrieves the name of the action to be executed
            # this is going to be used to select the proper
            # code to be executed
            action = item[0]

            # in case the action to be performed is not an
            # unload operation (time to skipp the loop)
            if not action == UNLOAD_ACTION: break

            # unpacks the item into the action and the target
            # module name and then uses it to unload the module
            _action, module_name = item
            self.unload_module(module_name)

        # retrieves the loaded plugins and then creates a
        # new list for the loaded plugins ids this is going
        # to be used later for re-loading, this must be done
        # after the unloading of the plugins
        loaded_plugins = plugin_manager.get_all_loaded_plugins()
        loaded_plugins_ids = [loaded_plugin.id for loaded_plugin in loaded_plugins]

        # iterates over all the operations to be performed
        # to execute them in the correct order
        for item in operations:
            # retrieves the name of the action to be executed
            # this is going to be used to select the proper
            # code to be executed
            action = item[0]

            # in case the action to be performed is the load
            # operation must load the module for the first time
            if action == LOAD_ACTION:
                # unpacks the item into the action, the target module name
                # and the search directory and then uses it to load the module
                _action, module_name, search_directory = item
                self.load_module(search_directory, module_name, load_plugins = False)

                # retrieves the target plugin from the module and then adds its
                # it to the list of loaded plugins (to be loaded at the end)
                target_plugin = plugin_manager.get_plugin_by_module_name(module_name)
                loaded_plugins_ids.append(target_plugin.id)

            # in case the action to be performed is the reload
            # operation must load the module again
            elif action == RELOAD_ACTION:
                # unpacks the item into the action, the target module name
                # and the plugin name and then uses it to reload the module
                _action, module_name, plugin = item
                self.reload_module(plugin, module_name, load_plugins = False)

        # iterates over all the loaded plugins ids to load
        # them into the current plugin manager instance
        for loaded_plugin_id in loaded_plugins_ids: plugin_manager.load_plugin(loaded_plugin_id)

    def load_module(self, search_directory, module_name, load_plugins = True, operations = None):
        """
        Loads a module with the given module name and
        for the given search directory.

        @type search_directory: String
        @param search_directory: The search directory to be used as base in the module load.
        @type module_name: String
        @param module_name: The name of the module to be loaded.
        @type operations: List
        @param operations: The list to hold the various operations that
        compose the jounal of operations for the transaction unit.
        """

        # in case the operations list is set no synchronous operation
        # is intended and so the operation tuple is added instead
        # then returns from the method immediately
        if not operations == None: operations.append((LOAD_ACTION, module_name, search_directory)); return

        try:
            # prints an info message
            self.autoloader_plugin.info("Loading module " + module_name)

            # retrieves the plugin manager
            plugin_manager = self.autoloader_plugin.manager

            # in case the search directory is not is the system path
            # it's inserted into it (for local import reference)
            if not search_directory in sys.path: sys.path.insert(0, search_directory)

            # loads the plugins for the module name, this should
            # be able to import the main plugin file into the
            # current environment
            plugin_manager.load_plugins([module_name])

            # starts all the plugins in the plugin manager, this
            # should load the singleton instance for newly loaded
            # plugin class (start plugin process)
            plugin_manager.start_plugins()

            # retrieves the plugin for the module name and then
            # loads the proper plugin into the current environment
            plugin = plugin_manager.get_plugin_by_module_name(module_name)
            load_plugins and plugin_manager.load_plugin(plugin.id)
        except Exception, exception:
            # prints an error message
            self.autoloader_plugin.error("There was a problem loading module %s: %s" % (module_name, unicode(exception)))

    def unload_module(self, module_name, operations = None):
        """
        Unloads a module with the given module name.

        @type module_name: String
        @param module_name: The name of the module to be unloaded.
        @type operations: List
        @param operations: The list to hold the various operations that
        compose the jounal of operations for the transaction unit.
        """

        # in case the operations list is set no synchronous operation
        # is intended and so the operation tuple is added instead
        # then returns from the method immediately
        if not operations == None: operations.append((UNLOAD_ACTION, module_name)); return

        try:
            # prints an info message
            self.autoloader_plugin.info("Unloading module " + module_name)

            # retrieves the plugin manager
            plugin_manager = self.autoloader_plugin.manager

            # stops the module
            plugin_manager.stop_module(module_name)
        except Exception, exception:
            # prints an error message
            self.autoloader_plugin.error("There was a problem unloading module %s: %s" % (module_name, unicode(exception)))

    def reload_module(self, plugin, module_name, load_plugins = True, operations = None):
        """
        Reloads the module with the given module name and
        reloads the main modules of the given plugin.

        An optional argument controls if the the plugin loading
        state is restored to the original state.

        @type plugin: Plugin
        @param plugin: The plugin to have the main modules reloaded.
        @type module_name: String
        @param module_name: The name of the module to be reloaded.
        @type load_plugins: bool
        @param load_plugins: If the plugins should be loaded again
        to the original state (this is an expensive operation).
        @type operations: List
        @param operations: The list to hold the various operations that
        compose the jounal of operations for the transaction unit.
        """

        # in case the operations list is set no synchronous operation
        # is intended and so the operation tuple is added instead
        # then returns from the method immediately
        if not operations == None: operations.append((RELOAD_ACTION, module_name, plugin)); return

        try:
            # prints an info message
            self.autoloader_plugin.info("Reloading module " + module_name)

            # retrieves the plugin manager
            plugin_manager = self.autoloader_plugin.manager

            # retrieves the plugin id
            plugin_id = plugin.id

            # retrieves the loaded plugins
            loaded_plugins = plugin_manager.get_all_loaded_plugins()

            # creates a new list for the loaded plugins ids
            # this is going to be used later for re-loading
            if load_plugins: loaded_plugins_ids = [loaded_plugin.id for loaded_plugin in loaded_plugins]
            else: loaded_plugins_ids = []

            # stops the module, this should remove the code
            # of referenced by the name from the virtual machine
            plugin_manager.stop_module(module_name)

            # loads the plugins for the module name, this should
            # be able to import the main plugin file into the
            # current environment
            plugin_manager.load_plugins([module_name])

            # starts all the plugins in the plugin manager, this
            # should load the singleton instance for newly loaded
            # plugin class (start plugin process)
            plugin_manager.start_plugins()

            # retrieves the plugin using the plugin id an then
            # reloads its modules (this is going to update the
            # modules code in the virtual machine)
            plugin = plugin_manager._get_plugin_by_id(plugin_id)
            plugin.reload_main_modules()

            # iterates over all the loaded plugins ids to load
            # them into the current plugin manager instance
            for loaded_plugin_id in loaded_plugins_ids: plugin_manager.load_plugin(loaded_plugin_id)
        except Exception, exception:
            # prints an error message
            self.autoloader_plugin.error("There was a problem reloading module %s: %s" % (module_name, unicode(exception)))

    def unload_autoloader(self):
        """
        Unloads the autoloader unsetting the continue flag.
        """

        # unsets the continue flag
        self.continue_flag = False

    def add_search_path(self):
        """
        Adds the system (path) path search directories
        to the autoloader search path.
        """

        # adds the search directories with the system
        # path (list)
        self.search_directories.append(sys.path)

    def add_search_directories(self, paths_list):
        """
        Adds the given paths list to the autoloader search path.

        @type path: String
        @param path: The paths list to be added to the autoloader
        search path.
        """

        # adds the paths list to the search directories
        self.search_directories.append(paths_list)

    def _sleep(self, sleep_time):
        """
        Custom sleep function used to be easily (and fast)
        cancel the loading loop.

        @type sleep_time: int
        @param sleep_time: The amount of time to sleep.
        """

        # calculates the number of iterations to be used
        # from the sleep step
        iterations = int(sleep_time / SLEEP_STEP_VALUE)

        # calculates the extra sleep time from the sleep
        # step modulus
        extra_sleep_time = sleep_time % SLEEP_STEP_VALUE

        # iterates over the range of iterations
        for _index in range(iterations):
            # sleep the sleep step
            time.sleep(SLEEP_STEP_VALUE)

            # in case the continue flag is not set
            # must return immediately
            if not self.continue_flag: return

        # sleeps the extra sleep time
        time.sleep(extra_sleep_time)

class FileInformation:
    """
    The file information class.
    """

    filename = "none"
    """ The file name """

    file_properties = None
    """ The file properties """

    exists = False
    """ The exists flag """

    def __init__(self, filename = "none", file_properties = None, exists = False):
        """
        Constructor of the class.

        @type filename: String
        @param filename: The file name.
        @type file_properties: FileProperties
        @param file_properties: The file properties.
        @type exists: bool
        @param exists: The exists flag.
        """

        self.filename = filename
        self.file_properties = file_properties
        self.exists = exists

class FileProperties:
    """
    The file properties class.
    """

    modified_date = None
    """ The modified date """

    def __init__(self, modified_date = None):
        """
        Constructor of the class.

        @type modified_date: Tuple
        @param modified_date: The modified date time tuple.
        """

        self.modified_date = modified_date
