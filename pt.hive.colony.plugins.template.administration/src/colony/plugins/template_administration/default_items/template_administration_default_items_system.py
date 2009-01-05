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

    def get_menu_items(self):
        # retrieves the plugin manager
        manager = self.template_administration_default_items_plugin.manager

        # retrieves the plugin path
        plugin_path = manager.get_plugin_path_by_id(self.template_administration_default_items_plugin.id)

        # creates the resources path
        resources_path = plugin_path + "/template_administration/default_items/resources"

        # creates the colony menu item file path
        colony_menu_item_file_path = resources_path + "/colony_menu_item.ctp" 

        # opens the colony menu item file
        colony_menu_item_file = open(colony_menu_item_file_path, "r")

        # reads the colony menu item
        colony_menu_item = colony_menu_item_file.read()

        # closes the colony menu item
        colony_menu_item_file.close()

        # returns the menu items
        return [colony_menu_item]

    def get_content_items(self):
        # retrieves the plugin manager
        manager = self.template_administration_default_items_plugin.manager

        # retrieves the plugin path
        plugin_path = manager.get_plugin_path_by_id(self.template_administration_default_items_plugin.id)

        # creates the resources path
        resources_path = plugin_path + "/template_administration/default_items/resources"

        # creates the colony plugin administration content item file path
        colony_plugin_administration_content_item_file_path = resources_path + "/colony_plugin_administration_content_item.ctp" 

        # opens the colony plugin administration content item file
        colony_plugin_administration_content_item_file = open(colony_plugin_administration_content_item_file_path, "r")

        # reads the colony plugin administration content item
        colony_plugin_administration_content_item = colony_plugin_administration_content_item_file.read()

        # closes the colony plugin administration content item
        colony_plugin_administration_content_item_file.close()

        # creates the colony information content item file path
        colony_information_content_item_file_path = resources_path + "/colony_information_content_item.ctp" 

        # opens the colony information content item file
        colony_information_content_item_file = open(colony_information_content_item_file_path, "r")

        # reads the colony information content item
        colony_information_content_item = colony_information_content_item_file.read()

        # closes the colony plugin administration content item
        colony_information_content_item_file.close()

        # returns the content items
        return [colony_plugin_administration_content_item, colony_information_content_item]
