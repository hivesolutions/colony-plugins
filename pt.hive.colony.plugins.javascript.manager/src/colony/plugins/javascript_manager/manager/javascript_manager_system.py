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
import time
import stat
import string
import os.path

import javascript_manager_parser
import javascript_manager_exceptions

class JavascriptManager:

    javascript_manager_plugin = None
    workspace_base_path = None

    plugin_search_directories_list = []
    plugin_descriptors_list = []
    plugin_search_directories_map = {}

    def __init__(self, javascript_manager_plugin):
        self.javascript_manager_plugin = javascript_manager_plugin

        self.plugin_search_directories_list = []
        self.plugin_descriptors_list = []
        self.plugin_search_directories_map = {}

    def set_plugin_search_directories(self):
        # retrieves the resource manager plugin
        resource_manager_plugin = self.javascript_manager_plugin.resource_manager_plugin

        # retrieves the workspace home path resource
        workspace_home_path_resource = resource_manager_plugin.get_resource("system.path.workspace_home")

        # retrieves the workspace home path value
        workspace_home_path = workspace_home_path_resource.data

        # sets the workspace base path
        self.workspace_base_path = workspace_home_path

        # sets the plugin search directories list
        self.plugin_search_directories_list = [self.workspace_base_path + "/pt.hive.colony.web/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.data_structure/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.development/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.dummy/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.gui.component.data_editor/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.gui.component.eureka/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.gui.component.login/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.gui.component.toolbar/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.gui.component.window/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.gui.component.wizard/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.gui.main/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.gui.main.extjs/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.gui.perspective_manager/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.misc/plugins",
                                               self.workspace_base_path + "/pt.hive.colony.web.plugins.mvc/plugins",
                                               self.workspace_base_path + "/pt.hive.omni.web.plugins.gui.functional_unit/plugins",
                                               self.workspace_base_path + "/pt.hive.omni.web.plugins.gui.main/plugins",
                                               self.workspace_base_path + "/pt.hive.omni.web.plugins.gui.misc/plugins",
                                               self.workspace_base_path + "/pt.hive.omni.web.plugins.gui.navigation_tree/plugins",
                                               self.workspace_base_path + "/pt.hive.omni.web.plugins.gui.pos/plugins",
                                               self.workspace_base_path + "/pt.hive.omni.web.plugins.gui.toolbar/plugins"]

    def index_plugin_search_directories(self):
        # iterates over all the search directories
        for plugin_search_directory in self.plugin_search_directories_list:
            # sets the current plugin search directories map
            current_plugin_search_directories_map = self.plugin_search_directories_map

            # indexes the current search directory
            self.index_plugin_search_directory(plugin_search_directory, current_plugin_search_directories_map)

    def index_plugin_search_directory(self, plugin_search_directory, current_plugin_search_directories_map):
        # the list of files in the javascript plugins directory
        dir_list = os.listdir(plugin_search_directory)

        # for all the files in the directory 
        for file_name in dir_list:
            # retrieves the file full path
            full_path = plugin_search_directory + "/" + file_name

            # retrieves the is directory value
            is_directory = os.path.isdir(full_path)

            # in case it's a directory
            if is_directory:
                if not file_name in current_plugin_search_directories_map:
                    current_plugin_search_directories_map[file_name] = {}
                current_plugin_search_directories_map_aux = current_plugin_search_directories_map[file_name]
                self.index_plugin_search_directory(full_path, current_plugin_search_directories_map_aux)
            else:
                current_plugin_search_directories_map[file_name] = full_path

    def load_plugin_files(self):
        # iterates over all the search directories
        for plugin_search_directory in self.plugin_search_directories_list:
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
                    plugin_descriptor_parser = javascript_manager_parser.PluginDescriptorParser(full_path)

                    # parses the xml files
                    plugin_descriptor_parser.parse()

                    # retrieves the plugin descriptor resultant of the parsing
                    plugin_descriptor = plugin_descriptor_parser.get_value()

                    # adds the plugin descriptor to the list of plugin descriptors
                    self.plugin_descriptors_list.append(plugin_descriptor)

    def update_plugin_files(self):
        pass

    def get_plugin_descriptor(self, plugin_id):
        pass

    def get_available_plugins(self):
        # the available plugins list
        available_plugins_list = []

        # iterates over all the available plugin descriptors
        for plugin_descriptor in self.plugin_descriptors_list:
            plugin_descriptor_id = plugin_descriptor.id
            available_plugins_list.append(plugin_descriptor_id)

        # creates a list object to support the list
        available_plugins_list_list = List()

        # sets the list value for the list object
        available_plugins_list_list.list = available_plugins_list

        # returns the created list object
        return available_plugins_list_list

    def get_available_plugin_descriptors(self):
        # creates a list object to support the list
        plugin_descriptors_list_list = List()

        # sets the list value for the list object
        plugin_descriptors_list_list.list = self.plugin_descriptors_list

        # returns the created list object
        return plugin_descriptors_list_list

    def update_plugin_manager(self):
        pass

    def get_new_plugins(self):
        return List()

    def get_new_plugin_descriptors(self):
        return List()

    def get_updated_plugins(self):
        return List()

    def get_updated_plugin_descriptors(self):
        return List()

    def get_removed_plugins(self):
        return List()

    def get_removed_plugin_descriptors(self):
        return List()

    def get_plugin_search_directories_list(self):
        return self.plugin_search_directories_list

    def get_file_full_path(self, relative_file_path):
        # strip the file path from "/" chararcter
        relative_file_path_striped = relative_file_path.strip("/")

        # splits the file path usgin the "/" character
        relative_file_path_splited = relative_file_path_striped.split("/")

        # retrieves the current plugin search directories map
        current_plugin_search_directories_map = self.plugin_search_directories_map

        # iterates over all the relative file path splited
        for relative_file_path_item in relative_file_path_splited:
            # in case the item exists in the current plugin search directories map
            if relative_file_path_item in current_plugin_search_directories_map:
                current_plugin_search_directories_map = current_plugin_search_directories_map[relative_file_path_item]
            else:
                raise javascript_manager_exceptions.InvalidFileNameException("the file: " + relative_file_path_item + " is not valid")

        # returns the full file path
        return current_plugin_search_directories_map

class List:
    """
    The generic List class.
    """

    list = []
    """ The list object for javascript list """

    def __init__(self):
        """
        Constructor of the class
        """

        self.list = []
