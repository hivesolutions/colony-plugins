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

HANDLER_FILENAME = "colony_manager/"
""" The handler filename """

class TemplateAdministration:
    """
    The template administration class.
    """

    template_administration_plugin = None
    """ The template administration plugin """

    def __init__(self, template_administration_plugin):
        """
        Constructor of the class.
        
        @type template_administration_plugin: TemplateAdministrationPlugin
        @param template_administration_plugin: The template administration plugin.
        """

        self.template_administration_plugin = template_administration_plugin

    def get_handler_filename(self):
        return HANDLER_FILENAME

    def get_template_path(self):
        # retrieves the plugin manager
        manager = self.template_administration_plugin.manager

        # retrieves the plugin path
        plugin_path = manager.get_plugin_path_by_id(self.template_administration_plugin.id)

        # creates the resources path
        resources_path = plugin_path + "/template_administration/administration/resources"

        # creates the colony manager template path
        colony_manager_template_path = resources_path + "/colony_manager.ctp"

        return colony_manager_template_path

    def get_resources_paths_map(self):
        # retrieves the plugin manager
        manager = self.template_administration_plugin.manager

        # retrieves the plugin path
        plugin_path = manager.get_plugin_path_by_id(self.template_administration_plugin.id)

        # creates the resources path
        resources_path = plugin_path + "/template_administration/administration/resources"

        return {"/" : resources_path}

    def get_menu_items(self):
        # retrieves the template administration menu item plugins
        template_administration_menu_item_plugins = self.template_administration_plugin.template_administration_menu_item_plugins

        # creates the menu items empty list
        menu_items = []

        for template_administration_menu_item_plugin in template_administration_menu_item_plugins:
            # retrieves the menu item from the template administration menu item plugin
            menu_item = template_administration_menu_item_plugin.get_menu_item()

            # adds the menu item to the list of menu items
            menu_items.append(menu_item)

        # returns the list of menu items
        return menu_items

    def get_content_items(self):
        # retrieves the template administration content item plugins
        template_administration_content_item_plugins = self.template_administration_plugin.template_administration_content_item_plugins

        # creates the content items empty list
        content_items = []

        for template_administration_content_item_plugin in template_administration_content_item_plugins:
            # retrieves the content item from the template administration content item plugin
            content_item = template_administration_content_item_plugin.get_content_item()

            # adds the content item to the list of content items
            content_items.append(content_item)

        # returns the list of content items
        return content_items
