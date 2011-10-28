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

import os
import time

SLEEP_TIME_VALUE = 1.0
""" The sleep time value """

class ResourceAutoloader:
    """
    The resource autoloader
    """

    continue_flag = True
    """ The continue flag that controls the autoloading system """

    file_path_modified_time_map = {}
    """ The map associating the file path with the modified time """

    def __init__(self, resource_autoloader_plugin):
        """
        Constructor of the class.

        @type resource_autoloader_plugin: Plugin
        @param resource_autoloader_plugin: The resource autoloader plugin.
        """

        self.resource_autoloader_plugin = resource_autoloader_plugin

        self.file_path_modified_time_map = {}

    def load_autoloader(self):
        """
        Loads the autoloader starting all the necessary structures
        and setting the update time.
        The autoloader runs continuously until the continue
        flag is unset.
        """

        # retrieves the plugin manager
        plugin_manager = self.resource_autoloader_plugin.manager

        # retrieves the resource manager plugin
        resource_manager_plugin = self.resource_autoloader_plugin.resource_manager_plugin

        # retrieves the configuration paths
        configuration_paths = plugin_manager.get_plugin_configuration_paths_by_id(resource_manager_plugin.id, True)

        # retrieves the base plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(resource_manager_plugin.id)

        # retrieve the file path resources list map from the resource manager
        # and then retrieves the keys from the map as the current used file paths
        file_path_resources_list_map = resource_manager_plugin.get_file_path_resources_list_map()
        file_paths = file_path_resources_list_map.keys()

        # -----------------------------------------------------

        BASE_RESOURCES_PATH = "resources/resource_manager/resources"
        """ The base resources path """

        #@todo: this is extremly bad

        # constructs the base resources path
        base_resources_path = os.path.join(plugin_path, BASE_RESOURCES_PATH)

        # -----------------------------------------------------

        # iterates over all the (resource) file paths
        # to update the stored modified time values
        for file_path in file_paths:
            # retrieves the modified time for the current
            # file (for timestamp checking) and then sets it
            # in the file path modified time map
            modified_time = os.path.getmtime(file_path)
            self.file_path_modified_time_map[file_path] = modified_time

        # notifies the ready semaphore
        self.resource_autoloader_plugin.release_ready_semaphore()

        # sets the continue flag
        self.continue_flag = True

        # while the flag is active
        while self.continue_flag:
            # iterates over all the configuration paths

            # creates a new list for the verified (existent)
            # resource paths
            verified_resource_paths_list = []

            # iterates over all the configuration paths to operate over
            # them and load or reload any foudn resource file
            for configuration_path in list(configuration_paths) + [base_resources_path]:
                # analyzes the current configuration path (directory) to load (new resources)
                # or reload (updated resources) the resources
                self._analyze_resources_directory(configuration_path, verified_resource_paths_list)

            # unloads the "pending" resource files for unloading
            self._unload_pending_resource_files(verified_resource_paths_list)

            # sleeps for the given sleep time
            time.sleep(SLEEP_TIME_VALUE)

    def unload_autoloader(self):
        """
        Unloads the autoloader unsetting the continue flag.
        """

        # unsets the continue flag
        self.continue_flag = False

    def _analyze_resources_directory(self, directory_path, verified_resource_paths_list):
        """
        Loads the resources in the directory with
        the given path.

        @type directory_path: String
        @param directory_path: The directory path to search for resources.
        """

        # in case the directory path does not exists
        if not os.path.exists(directory_path):
            # returns immediately
            return

        # retrieves the resource manager plugin
        resource_manager_plugin = self.resource_autoloader_plugin.resource_manager_plugin

        # retrieves the file path resources list map from the resource manager
        file_path_resources_list_map = resource_manager_plugin.get_file_path_resources_list_map()

        # retrieves the resources path directory contents
        resources_path_directory_contents = os.listdir(directory_path)

        # iterates over the resources path directory contents
        # to load them in the resource manager
        for resources_path_item in resources_path_directory_contents:

            # TENHO DE TER UM METODO NO MAGER TIPO is_resource_name
            # para testar se o name corresponde a um resource


            RESOURCES_SUFFIX_LENGTH = 13
            """ The resources suffix length """

            RESOURCES_SUFFIX_START_INDEX = -13
            """ The resources suffix value """

            RESOURCES_SUFIX_VALUE = "resources.xml"
            """ The resources suffix value """

            import colony.libs.path_util



            # creates the resources full path item
            resources_full_path_item = os.path.join(directory_path, resources_path_item)



            # in case the length of the resources path item is greater or equal than the resources suffix length
            # and the last item of the resources path item is the same as the resources suffix value
            if len(resources_path_item) >= RESOURCES_SUFFIX_LENGTH and resources_path_item[RESOURCES_SUFFIX_START_INDEX:] == RESOURCES_SUFIX_VALUE:
                # normalizes the resources full path (for file verification)
                resources_full_path_item_normalized = colony.libs.path_util.normalize_path(resources_full_path_item)

                # adds the resource path to the verified resource paths list
                # because the resource has been verified as existent
                verified_resource_paths_list.append(resources_full_path_item_normalized)

                # retrieves the current modified time from the resource and the
                # modified time currently stored in the internal structure
                # for later comparison
                current_modified_time = os.path.getmtime(resources_full_path_item_normalized)
                modified_time = self.file_path_modified_time_map.get(resources_full_path_item_normalized, None)

                # in case the modified time hasn't changed
                # the file is considered to be the same
                if current_modified_time == modified_time:
                    # continues the loop (nothing changed)
                    continue

                # in case there's no current modified time defined (the file
                # did not already existed)
                if modified_time == None:
                    # prints an info message (about the loading)
                    self.resource_autoloader_plugin.info("Loading resource file '%s' in resource manager" % resources_full_path_item_normalized)
                # otherwise the file already existed but the modified time has
                # changed (reload case)
                else:
                    # prints an info message (about the reloading)
                    self.resource_autoloader_plugin.info("Reloading resource file '%s' in resource manager" % resources_full_path_item_normalized)

                    # retrieves the resources list for the resources path and then uses it to
                    # unregister the resources in the resource manager

                    # @todo: remove the direct reference
                    resources_list = file_path_resources_list_map[resources_full_path_item_normalized]
                    resource_manager_plugin.unregister_resources(resources_list, resources_full_path_item, directory_path)

                # parses the resources description file
                resource_manager_plugin.parse_file(resources_full_path_item, directory_path)

                # sets the "new" modified time in the file path modified
                # time map (updates the modified time)
                self.file_path_modified_time_map[resources_full_path_item_normalized] = current_modified_time
            # otherwise in case the resources full path is a directory
            # path a descent must be done
            elif os.path.isdir(resources_full_path_item):
                # analyzes the resources for the directory
                self._analyze_resources_directory(resources_full_path_item, verified_resource_paths_list)

    def _unload_pending_resource_files(self, verified_resource_paths_list):
        # retrieves the resource manager plugin
        resource_manager_plugin = self.resource_autoloader_plugin.resource_manager_plugin

        # retrieves the file path resources list map and the file path
        # file information map from the resource manager and then retrieves
        # the keys from the map as the current used (resource) file paths
        file_path_resources_list_map = resource_manager_plugin.get_file_path_resources_list_map()
        file_path_file_information_map = resource_manager_plugin.get_file_path_file_information_map()
        resource_file_paths = file_path_resources_list_map.keys()

        # iterates over all the resource file path
        # to check if the associated resources shall be
        # unloaded
        for resource_file_path in resource_file_paths:
            # in case the resource file path is contained in
            # the verified resource paths list (no need to unload)
            if resource_file_path in verified_resource_paths_list:
                # continues the loop (nothing
                # to be removed)
                continue

            # prints an info message (about the unloading)
            self.resource_autoloader_plugin.info("Unloading resource file '%s' from resource manager" % resource_file_path)

            # retrieves both the resources list and the file information tuple
            # (file path and full resources path) for the resource file path
            resources_list = file_path_resources_list_map[resource_file_path]
            file_path, full_resources_path = file_path_file_information_map[resource_file_path]

            # unregisters the resources for the current resource file in the resource manager
            resource_manager_plugin.unregister_resources(resources_list, file_path, full_resources_path)

            # removes the modified time reference for the resource file
            # in the file path modified time map
            del self.file_path_modified_time_map[resource_file_path]
