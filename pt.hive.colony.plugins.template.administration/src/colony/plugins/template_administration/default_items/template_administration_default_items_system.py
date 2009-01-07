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

EXTENSION_NAME = "default"
""" The extension name """

class TemplateAdministrationDefaultItems:
    """
    The template administration default items class.
    """

    template_administration_default_items_plugin = None
    """ The template administration default items plugin """

    def __init__(self, template_administration_default_items_plugin):
        """
        Constructor of the class.
        
        @type template_administration_default_items_plugin: TemplateAdministrationDefaultItemsPlugin
        @param template_administration_default_items_plugin: The template administration default items plugin.
        """

        self.template_administration_default_items_plugin = template_administration_default_items_plugin

    def get_extension_name(self):
        return EXTENSION_NAME

    def get_base_resources_path(self):
        # retrieves the plugin manager
        manager = self.template_administration_default_items_plugin.manager

        # retrieves the plugin path
        plugin_path = manager.get_plugin_path_by_id(self.template_administration_default_items_plugin.id)

        # creates the resources path
        resources_path = plugin_path + "/template_administration/default_items/resources"

        return resources_path

    def get_css_files(self):
        return ["css/colony_plugin_administration_content_item.js"]

    def get_js_files(self):
        return ["js/colony_plugin_administration_content_item.js"]

    def get_menu_items(self):
        # the menu items path list
        menu_items_paths = ["colony_menu_item.ctp"]

        # creates the empty menu items list
        menu_items = []

        # iterates over all the menu items paths
        for menu_item_path in menu_items_paths:
            # reads the menu item
            menu_item = self.get_file_contents(menu_item_path)

            # adds the menu item to the list of menu items
            menu_items.append(menu_item)

        # returns the menu items
        return menu_items

    def get_content_items(self):
        # the content items path list
        content_items_paths = ["colony_information_content_item.ctp", "colony_plugin_administration_content_item.ctp"]

        # creates the empty content items list
        content_items = []

        # iterates over all the content items paths
        for content_item_path in content_items_paths:
            # reads the content item
            content_item = self.get_file_contents(content_item_path)

            # adds the content item to the list of content items
            content_items.append(content_item)

        # returns the content items
        return content_items

    def get_file_contents(self, relative_file_path):
        # retrieves the plugin manager
        manager = self.template_administration_default_items_plugin.manager

        # retrieves the plugin path
        plugin_path = manager.get_plugin_path_by_id(self.template_administration_default_items_plugin.id)

        # creates the resources path
        resources_path = plugin_path + "/template_administration/default_items/resources"

        # creates the file path
        file_path = resources_path + "/" + relative_file_path
    
        # opens the file
        file = open(file_path, "r")
    
        # reads the file contents
        file_contents = file.read()
    
        # closes the file
        file.close()

        # returns the file contents
        return file_contents
