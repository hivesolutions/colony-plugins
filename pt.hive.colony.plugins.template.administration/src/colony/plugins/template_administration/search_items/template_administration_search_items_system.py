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

__revision__ = "$LastChangedRevision: 516 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-28 14:30:47 +0000 (Sex, 28 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

EXTENSION_NAME = "search"
""" The extension name """

class TemplateAdministrationSearchItems:
    """
    The template administration search items class.
    """

    template_administration_search_items_plugin = None
    """ The template administration search items plugin """

    def __init__(self, template_administration_search_items_plugin):
        """
        Constructor of the class.
        
        @type template_administration_search_items_plugin: TemplateAdministrationSearchItemsPlugin
        @param template_administration_search_items_plugin: The template administration search items plugin.
        """

        self.template_administration_search_items_plugin = template_administration_search_items_plugin

    def get_extension_name(self):
        return EXTENSION_NAME

    def get_base_resources_path(self):
        # retrieves the plugin manager
        manager = self.template_administration_search_items_plugin.manager

        # retrieves the plugin path
        plugin_path = manager.get_plugin_path_by_id(self.template_administration_search_items_plugin.id)

        # creates the resources path
        resources_path = plugin_path + "/template_administration/search_items/resources"

        return resources_path

    def get_css_files(self):
        return ["css/search_tester_content_item.css"]

    def get_js_files(self):
        return ["js/search_tester_content_item.js"]

    def get_menu_items(self):
        # retrieves the plugin manager
        manager = self.template_administration_search_items_plugin.manager

        # retrieves the plugin path
        plugin_path = manager.get_plugin_path_by_id(self.template_administration_search_items_plugin.id)

        # creates the resources path
        resources_path = plugin_path + "/template_administration/search_items/resources"

        # creates the search menu item file path
        search_menu_item_file_path = resources_path + "/search_menu_item.ctp" 

        # opens the search menu item file
        search_menu_item_file = open(search_menu_item_file_path, "r")

        # reads the search menu item
        search_menu_item = search_menu_item_file.read()

        # closes the search menu item file
        search_menu_item_file.close()

        # returns the menu items
        return [search_menu_item]

    def get_content_items(self):
        # the content items path list
        content_items_paths = ["search_tester_content_item.ctp", "search_index_content_item.ctp"]

        # creates the empty content items list
        content_items = []

        # retrieves the plugin manager
        manager = self.template_administration_search_items_plugin.manager

        # retrieves the plugin path
        plugin_path = manager.get_plugin_path_by_id(self.template_administration_search_items_plugin.id)

        # creates the resources path
        resources_path = plugin_path + "/template_administration/search_items/resources"

        # iterates over all the content items paths
        for content_item_path in content_items_paths:
            # creates the content item file path
            content_item_file_path = resources_path + "/" + content_item_path

            # opens the content item file
            content_item_file = open(content_item_file_path, "r")

            # reads the content item
            content_item = content_item_file.read()

            # closes the content item file
            content_item_file.close()

            # adds the content item to the list of content items
            content_items.append(content_item)

        # returns the content items
        return content_items
