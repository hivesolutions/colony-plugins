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
import os.path

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

    def update_plugin_files(self):
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
                                print "o plugin:" +  plugin_id + " foi modificado"
                                self.plugin_id_modified_date_map[plugin_id] = modified_date
                        elif plugin_id in javascript_manager.plugin_id_plugin_descriptor_map:
                            # e apenas a primeira vez ke pediu e tem de por a data
                            # neste momento nao conseguimos saber se foi updatada ou nao
                            print "primeira vez para o" + plugin_id
                            self.plugin_id_modified_date_map[plugin_id] = modified_date
                        else:
                            # adds the plugin descriptor to the list of plugin descriptors
                            # in the javascript manager
                            javascript_manager.plugin_descriptors_list.append(plugin_descriptor)

                            javascript_manager.plugin_id_plugin_descriptor_map[plugin_id] = plugin_descriptor

                            self.plugin_id_modified_date_map[plugin_id] = modified_date

        # creates a new timestamp for the update
        self.javascript_manager_last_update_timestamp = time.time();

    def update_plugin_manager(self):
        self.update_plugin_files()

    def get_new_plugins(self):
        # tenho de mandar timestamp
        return List()

    def get_new_plugin_descriptors(self):
        # tenho de mandar timestamp
        return List()

    def get_updated_plugins(self):
        # tenho de mandar timestamp
        return List()

    def get_updated_plugin_descriptors(self):
        # tennho de mandar timestamp
        return List()

    def get_removed_plugins(self):
        # tenho de mandar timestamp
        return List()

    def get_removed_plugin_descriptors(self):
        # tenho de mandar timestamp
        return List()

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
