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

MENU_ITEMS_VALUE = "menu_items"
""" The menu items value """

CONTENT_ITEMS_VALUE = "content_items"
""" The content items value """

class TemplateAdministration:
    """
    The template administration class.
    """

    template_administration_plugin = None
    """ The template administration plugin """

    resources_map = {}
    """ The resources map """

    def __init__(self, template_administration_plugin):
        """
        Constructor of the class.
        
        @type template_administration_plugin: TemplateAdministrationPlugin
        @param template_administration_plugin: The template administration plugin.
        """

        self.template_administration_plugin = template_administration_plugin

        self.resources_map = {}

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

        resources_paths_map = {"/" : resources_path}

        # retrieves the template administration extension plugins
        template_administration_extension_plugins = self.template_administration_plugin.template_administration_extension_plugins

        # iterates over all the template administration extension plugins
        for template_administration_extension_plugin in template_administration_extension_plugins:
            # retrieves the extension name for the template administration extension plugin
            extension_name = template_administration_extension_plugin.get_extension_name()

            # retrieves the base resources path for the template administration extension plugin
            base_resources_path = template_administration_extension_plugin.get_base_resources_path()

            resources_paths_map[extension_name] = base_resources_path

        return resources_paths_map

    def update_resources(self):
        menu_items = self.retrieve_menu_items()
        content_items = self.retrieve_content_items()
        bundle_items_tuple = self.retrieve_bundle_items()

        menu_items_bundle, content_items_bundle = bundle_items_tuple

        menu_items.extend(menu_items_bundle)
        content_items.extend(content_items_bundle)

        self.resources_map[MENU_ITEMS_VALUE] = menu_items
        self.resources_map[CONTENT_ITEMS_VALUE] = content_items

    def retrieve_menu_items(self):
        # retrieves the template administration extension menu item plugins
        template_administration_extension_menu_item_plugins = self.template_administration_plugin.template_administration_extension_menu_item_plugins

        # creates the menu items empty list
        menu_items = []

        # iterates over all the template administration extension menu item plugins
        for template_administration_extension_menu_item_plugin in template_administration_extension_menu_item_plugins:
            # retrieves the menu item from the template administration extension menu item plugin
            menu_item = template_administration_extension_menu_item_plugin.get_menu_item()

            # adds the menu item to the list of menu items
            menu_items.append(menu_item)

        # returns the list of menu items
        return menu_items

    def retrieve_content_items(self):
        # retrieves the template administration extension content item plugins
        template_administration_extension_content_item_plugins = self.template_administration_plugin.template_administration_extension_content_item_plugins

        # creates the content items empty list
        content_items = []

        # iterates over all the template administration extension content item plugins
        for template_administration_extension_content_item_plugin in template_administration_extension_content_item_plugins:
            # retrieves the content item from the template administration extension content item plugin
            content_item = template_administration_extension_content_item_plugin.get_content_item()

            # adds the content item to the list of content items
            content_items.append(content_item)

        # returns the list of content items
        return content_items

    def retrieve_bundle_items(self):
        # retrieves the template administration extension bundle plugins
        template_administration_extension_bundle_plugins = self.template_administration_plugin.template_administration_extension_bundle_plugins

        # creates the menu items empty list
        menu_items = []

        # creates the content items empty list
        content_items = []

        # iterates over all the template administration extension bundle plugins
        for template_administration_extension_bundle_plugin in template_administration_extension_bundle_plugins:
            # retrieves the menu items bundle from the template administration bundle plugin
            menu_items_bundle = template_administration_extension_bundle_plugin.get_menu_items()

            # adds the menu items bundle to the list of menu items
            menu_items.extend(menu_items_bundle)

            # retrieves the content items bundle from the template administration bundle plugin
            content_items_bundle = template_administration_extension_bundle_plugin.get_content_items()

            # adds the content items bundle to the list of content items
            content_items.extend(content_items_bundle)

        # returns the tuple with the all the items
        return (menu_items, content_items)

    def get_css_files(self):
        # retrieves the template administration extension plugins
        template_administration_extension_plugins = self.template_administration_plugin.template_administration_extension_plugins

        # creates the empty css files list
        css_files = []

        for template_administration_extension_plugin in template_administration_extension_plugins:
            extension_plugin_css_files = template_administration_extension_plugin.get_css_files()

            css_files.extend(extension_plugin_css_files)

        return css_files

    def get_js_files(self):
        # retrieves the template administration extension plugins
        template_administration_extension_plugins = self.template_administration_plugin.template_administration_extension_plugins

        # creates the empty js files list
        js_files = []

        for template_administration_extension_plugin in template_administration_extension_plugins:
            extension_plugin_js_files = template_administration_extension_plugin.get_js_files()

            js_files.extend(extension_plugin_js_files)

        return js_files

    def get_menu_items(self):
        self.update_resources()
        return self.resources_map.get(MENU_ITEMS_VALUE, [])

    def get_content_items(self):
        self.update_resources()
        return self.resources_map.get(CONTENT_ITEMS_VALUE, [])
