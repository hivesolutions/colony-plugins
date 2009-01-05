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

    def get_menu_item(self):
        # retrieves the plugin manager
        manager = self.template_administration_default_items_plugin.manager

        # retrieves the plugin path
        plugin_path = manager.get_plugin_path_by_id(self.template_administration_default_items_plugin.id)

        # creates the resources path
        resources_path = plugin_path + "/template_administration/default_items/resources"

        # creates the default menu item file path
        default_menu_item_file_path = resources_path + "/default_menu_item.ctp" 

        # opens the default menu item file
        default_menu_item_file = open(default_menu_item_file_path, "r")

        # reads the default menu item
        default_menu_item = default_menu_item_file.read()

        # closes the default menu item
        default_menu_item_file.close()

        # returns the default menu item
        return default_menu_item
