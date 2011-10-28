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



        BASE_RESOURCES_PATH = "resources/resource_manager/resources"
        """ The base resources path """

        #@todo: this is extremly bad

        # constructs the base resources path
        base_resources_path = os.path.join(plugin_path, BASE_RESOURCES_PATH)


        # notifies the ready semaphore
        self.resource_autoloader_plugin.release_ready_semaphore()


        #@todo this is a temporary HACK

        for file_path in resource_manager_plugin.resource_manager.file_path_resources_list_map.keys():
            # retrieves the modified time for the current
            # file (for timestamp checking) and then sets it
            # in the file path modified time map
            modified_time = os.path.getmtime(file_path)
            self.file_path_modified_time_map[file_path] = modified_time

        # sets the continue flag
        self.continue_flag = True

        # while the flag is active
        while self.continue_flag:
            # iterates over all the configuration paths

            verified_resources_path_list = []

            #@todo this is so bad
            for configuration_path in list(configuration_paths) + [base_resources_path]:
                self._load_resources_directory(configuration_path, verified_resources_path_list)

            for tobias in self.file_path_modified_time_map.keys():
                if tobias in verified_resources_path_list:
                    # continues the loop (nothing
                    # to be removed)
                    continue

                print "Vai remover configuracao: '%s'" % tobias

                del self.file_path_modified_time_map[tobias]

                resources_list = resource_manager_plugin.resource_manager.file_path_resources_list_map[tobias]
                file_path, full_resources_path = resource_manager_plugin.resource_manager.file_path_file_information_map[tobias]

                resource_manager_plugin.resource_manager.unregister_resources(resources_list, file_path, full_resources_path)

                # iterates over all the search directories
            #    for search_directory in meta_paths:
                    # analyzes the given search directory
            #        self.analyze_search_directory(search_directory)

            # sleeps for the given sleep time
            time.sleep(SLEEP_TIME_VALUE)

    def unload_autoloader(self):
        """
        Unloads the autoloader unsetting the continue flag.
        """

        # unsets the continue flag
        self.continue_flag = False

    def _load_resources_directory(self, directory_path, verified_resources_path_list):
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
            """ The resources sufix value """

            import colony.libs.path_util



            # creates the resources full path item
            resources_full_path_item = os.path.join(directory_path, resources_path_item)



            # in case the length of the resources path item is greater or equal than the resources suffix length
            # and the last item of the resources path item is the same as the resources suffix value
            if len(resources_path_item) >= RESOURCES_SUFFIX_LENGTH and resources_path_item[RESOURCES_SUFFIX_START_INDEX:] == RESOURCES_SUFIX_VALUE:

                # normalizes the resources full path (for file verification)
                resources_full_path_item_normalized = colony.libs.path_util.normalize_path(resources_full_path_item)

                current_modified_time = os.path.getmtime(resources_full_path_item_normalized)
                modified_time = self.file_path_modified_time_map.get(resources_full_path_item_normalized, None)


                verified_resources_path_list.append(resources_full_path_item_normalized)



                # in case the modified time hasn't changed
                # the file is considered to be the same
                if current_modified_time == modified_time:
                    # continues the loop (nothing changed)
                    continue

                # in case there's no current modified time defined (the file
                # did not already existed)
                if modified_time == None:
                    print "vai fazer load inicial do ficheiro %s" % resources_full_path_item_normalized
                # otherwise the file already existed but the modified time has
                # changed (reload case)
                else:
                    print "VAI FAZER RELOAD DO FICHEIRO %s" % resources_full_path_item_normalized
                    resources_list = resource_manager_plugin.resource_manager.file_path_resources_list_map[resources_full_path_item_normalized]

                    resource_manager_plugin.resource_manager.unregister_resources(resources_list, resources_full_path_item, directory_path)

                # @todo: THIS IS NOT OK (direct reference)
                # parses the resources description file
                resource_manager_plugin.resource_manager.parse_file(resources_full_path_item, directory_path)

                # sets the "new" modified time in the file path modified
                # tim map (updates the modified time)
                self.file_path_modified_time_map[resources_full_path_item_normalized] = current_modified_time
            # otherwise in case the resources full path is a directory
            # path a descent must be done
            elif os.path.isdir(resources_full_path_item):
                # loads the resources for the directory
                self._load_resources_directory(resources_full_path_item, verified_resources_path_list)
