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
import threading

import colony.libs.string_buffer_util
import colony.libs.update_thread_util

import javascript_manager_parser
import javascript_manager_exceptions

DEFAULT_INDEX_TIME = 3
""" The default index time """

DEFAULT_LIMIT_COUNTER = 10
""" The default limit counter """

DEFAULT_CHARSET = "utf-8"
""" The default charset """

BASE_PATHS_LIST =  [
    "%prefix:colony_demo%/pt.hive.colony.demo.web.plugins.todo_list/plugins",
    "%prefix:colony_demo%/pt.hive.colony.demo.web.plugins.twitter/plugins",
    "%prefix:colony_demo%/pt.hive.colony.demo.web.plugins.wiki/plugins",
    "%prefix:colony_web%/pt.hive.colony.web/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.browserplus/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.data_structure/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.business/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.content.manager/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.dummy/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.gui.key_activators/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.gui.login/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.gui.main/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.gui.perspective_manager/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.gui.plugin_manager/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.gui.search.manager/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.main.localization/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.main.localization.translation_bundle/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.main.test/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.misc/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.mvc/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.printing/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.sorting/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.tasks/plugins",
    "%prefix:colony_web%/pt.hive.colony.web.plugins.ui/plugins",
    #"%prefix:omni_web%/pt.hive.omni.web.plugins.gui.consignments/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.customers_suppliers/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.address/plugins",
    #"%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.company/plugins",
    #"%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.consignment/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.contact_information/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.contactable/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.customer/plugins",
    #"%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.employee/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.person/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.pos/plugins",
    #"%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.purchase/plugins",
    #"%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.reservation/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.saft_pt/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.sale/plugins",
    #"%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.stock_adjustment/plugins",
    #"%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.supplier/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.transactional_merchandise/plugins",
    #"%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.transfer/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.general.user/plugins",
    #"%prefix:omni_web%/pt.hive.omni.web.plugins.gui.human_resources/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.inventory/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.main/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.misc/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.pos/plugins",
    #"%prefix:omni_web%/pt.hive.omni.web.plugins.gui.purchases/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.sales/plugins",
    "%prefix:omni_web%/pt.hive.omni.web.plugins.gui.system/plugins",
    "%prefix:colony_web_ui%/pt.hive.colony.web.ui"
]
""" The list of base paths to be used in the javascript manager """

class JavascriptManager:
    """
    The javascript manager class.
    """

    javascript_manager_plugin = None
    """ The javascript manager plugin """

    plugin_search_directories_lock = None
    """ The plugin search directories lock """

    javascript_manager_last_update_timestamp = None
    """ The javascript manager last update timestamp """

    auto_index_plugin_search_directories_flag = None
    """ The auto index plugin search directories flag """

    auto_index_plugin_search_directories_timer = None
    """ The auto index plugin search directories timer """

    auto_index_plugin_search_directories_timeout_counter = 0
    """ The auto index plugin search directories timeout counter """

    plugin_search_directories_list = []
    """ The plugin search directories list """

    plugin_descriptors_list = []
    """ The plugin descriptors list """

    plugin_id_plugin_descriptor_map = {}
    """ The map relating the plugin id with the plugin descriptor """

    plugin_search_directories_map = {}
    """ The plugin search directories map """

    def __init__(self, javascript_manager_plugin):
        """
        Constructor of the class.

        @type javascript_manager_plugin: JavascriptManagerPlugin
        @param javascript_manager_plugin: The javascript manager plugin.
        """

        self.javascript_manager_plugin = javascript_manager_plugin

        self.plugin_search_directories_lock = threading.Lock()

        self.plugin_search_directories_list = []
        self.plugin_descriptors_list = []
        self.plugin_id_plugin_descriptor_map = {}
        self.plugin_search_directories_map = {}

        self.timeout_counter = 0

    def set_plugin_search_directories(self):
        # retrieves the plugin manager
        plugin_manager = self.javascript_manager_plugin.manager

        # sets the plugin search directories list
        self.plugin_search_directories_list = [plugin_manager.resolve_file_path(value) or value for value in BASE_PATHS_LIST]

    def start_auto_index_plugin_search_directories(self):
        self.auto_index_plugin_search_directories_flag = True
        self.auto_index_plugin_search_directories()

    def stop_auto_index_plugin_search_directories(self):
        # unsets the auto index plugin search directories flag
        self.auto_index_plugin_search_directories_flag = False

        # in case the auto index plugin search directories timer thread is active
        if self.auto_index_plugin_search_directories_timer:
            # stops the auto index plugin search directories system
            self.auto_index_plugin_search_directories_timer.stop()

    def auto_index_plugin_search_directories(self):
        # in case the auto index plugin search directories flag is active
        if self.auto_index_plugin_search_directories_flag:
            # creates the auto index plugin search directories timer thread
            self.auto_index_plugin_search_directories_timer = colony.libs.update_thread_util.UpdateThread()

            # sets the timeout in the auto index plugin search directories timer thread
            self.auto_index_plugin_search_directories_timer.set_timeout(DEFAULT_INDEX_TIME)

            # sets the timeout in the call method index plugin search directories timer thread
            self.auto_index_plugin_search_directories_timer.set_call_method(self.auto_index_plugin_search_directories_handler)

            # starts the auto index plugin search directories system
            self.auto_index_plugin_search_directories_timer.start()

    def auto_index_plugin_search_directories_handler(self):
        # in case the auto index plugin search directories timeout counter is zero
        if self.auto_index_plugin_search_directories_timeout_counter == 0:
            # indexes the plugin search directories
            self.index_plugin_search_directories()

            # resets the auto index plugin search directories timeout counter
            self.auto_index_plugin_search_directories_timeout_counter = DEFAULT_LIMIT_COUNTER

        # decrements the auto index plugin search directories timeout counter
        self.auto_index_plugin_search_directories_timeout_counter -= 1

    def index_plugin_search_directories(self):
        # prints debug message
        self.javascript_manager_plugin.debug("Starting index of plugin search directories")

        # acquires the plugin search directories lock
        self.plugin_search_directories_lock.acquire()

        try:
            # creates the current plugin search directories map
            current_plugin_search_directories_map = {}

            # iterates over all the search directories
            for plugin_search_directory in self.plugin_search_directories_list:
                # indexes the current search directory
                self.index_plugin_search_directory(plugin_search_directory, current_plugin_search_directories_map)

            # retrieves the old plugin search directories map (for latter removal)
            old_plugin_search_directories_map = self.plugin_search_directories_map

            # sets the current plugin search directories map as the
            # plugin search directories map
            self.plugin_search_directories_map = current_plugin_search_directories_map

            # deletes the old plugin search directories map
            del old_plugin_search_directories_map

            # creates a new timestamp for the update
            self.javascript_manager_last_update_timestamp = time.time()
        finally:
            # releases the plugin search directories lock
            self.plugin_search_directories_lock.release()

        # prints debug message
        self.javascript_manager_plugin.debug("Ending index of plugin search directories")

    def index_plugin_search_directory(self, plugin_search_directory, current_plugin_search_directories_map):
        # in case the javascript plugins directory does not exists
        if not os.path.exists(plugin_search_directory):
            # prints a warning message
            self.javascript_manager_plugin.warning("Path '%s' does not exist in the current filesystem" % (plugin_search_directory))

            # returns immediately
            return

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
                # in case there is no directory map created
                if not file_name in current_plugin_search_directories_map:
                    current_plugin_search_directories_map[file_name] = {}

                # retrieves the directory map
                current_plugin_search_directories_map_aux = current_plugin_search_directories_map[file_name]

                # indexes the directory map
                self.index_plugin_search_directory(full_path, current_plugin_search_directories_map_aux)
            # in case it's a regular file
            else:
                # indexes the regular file
                current_plugin_search_directories_map[file_name] = full_path

    def load_plugin_files(self):
        # iterates over all the search directories
        for plugin_search_directory in self.plugin_search_directories_list:
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

                        # retrieves the plugin id from the plugin descriptor
                        plugin_id = plugin_descriptor.id

                        # adds the plugin descriptor to the list of plugin descriptors
                        self.plugin_descriptors_list.append(plugin_descriptor)

                        # sets the plugin descriptor in the plugin id plugin descriptors map
                        self.plugin_id_plugin_descriptor_map[plugin_id] = plugin_descriptor

    def get_plugin_descriptor(self, plugin_id):
        return self.plugin_id_plugin_descriptor_map.get(plugin_id, None)

    def get_plugin_file(self, plugin_id):
        # retrieves the plugin descriptor for the given plugin id
        plugin_descriptor = self.plugin_id_plugin_descriptor_map.get(plugin_id, None)

        # retrieves the plugin descriptor main file
        main_file = plugin_descriptor.main_file

        # retrieves the main file full path
        main_file_full_path = self.get_file_full_path(main_file)

        # opens the file for reading
        file = open(main_file_full_path, "rb")

        # reads the file contents
        file_contents = file.read()

        # closes the file
        file.close()

        # returns the file contents
        return file_contents

    def get_plugins_files(self, plugin_id_list):
        # creates the stream buffer
        stream_buffer = colony.libs.string_buffer_util.StringBuffer()

        # iterates over the plugins ids list
        for plugin_id in plugin_id_list:
            # retrieves the file contents for the given plugin id
            file_contents = self.get_plugin_file(plugin_id)

            # writes the file contents to the stream buffer
            stream_buffer.write(file_contents)

        # retrieves the stream buffer contents
        files_contents = stream_buffer.get_value()

        # decodes the file contents
        file_contents_decoded = files_contents.decode(DEFAULT_CHARSET)

        # returns the files contents decoded
        return file_contents_decoded

    def get_plugin_payload(self, plugin_id):
        pass

    def get_plugins_payload(self, plugin_id_list):
        pass

    def get_plugin_file_payload(self, plugin_id):
        pass

    def get_plugins_files_payload(self, plugin_id_list):
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
            # otherwise
            else:
                # raises the invalid file name exception
                raise javascript_manager_exceptions.InvalidFileNameException("the file: " + relative_file_path_item + " is not valid")

        # returns the full file path
        return current_plugin_search_directories_map

    def get_plugin_search_directories_list(self):
        return self.plugin_search_directories_list

    def set_plugin_search_directories_list(self, plugin_search_directories_list):
        self.plugin_search_directories_list = plugin_search_directories_list

    def get_plugin_search_directories_map(self):
        return self.plugin_search_directories_map

    def set_plugin_search_directories_map(self, plugin_search_directories_map):
        self.plugin_search_directories_map = plugin_search_directories_map

    def get_plugin_descriptor_parser(self):
        return javascript_manager_parser.PluginDescriptorParser

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
