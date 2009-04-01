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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2072 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-20 12:02:33 +0100 (Mon, 20 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class EurekaEngine:
    """
    This is the back-end for the Eureka Engine plugin. This class does the actual instruction routing.
    """

    def __init__(self, eureka_engine_plugin):
        """
        @type eureka_engine_plugin: EurekaEnginePlugin
        @param eureka_engine_plugin: The eureka engine plugin.
        """

        self.eureka_engine_plugin = eureka_engine_plugin

    def get_all_items(self, search_string, context = None, max_items = None):
        """
        Back-end for the raw items getter.
        Should return the item list without going through the item processing plugin chain.
        """

        items = []

        # loops through the extension plugins
        for extension_plugin in self.eureka_engine_plugin.eureka_item_extension_plugins:
            # pushes the search_string, context and max_items into the plugin's get_all_items
            extension_plugin_items = extension_plugin.get_all_items(search_string, context, max_items)
            items.extend(extension_plugin_items)

        # slices to get the first max_items (when not specified returns all items)
        items = items[0:max_items]

        return items

    def get_items_for_string(self, search_string, max_items):
        context = None
        return self.get_items_for_string_with_context(search_string, context, max_items)

    def get_items_for_string_with_context(self, search_string, context, max_items):
        """
        Back-end for the processed items getter (using the plugin chain).
        """

        items = []

        # loops through the extension plugins
        for extension_plugin in self.eureka_engine_plugin.eureka_item_extension_plugins:
            # pushes the search_string, context and max_items into the plugin's get_items
            extension_plugin_items = extension_plugin.get_items_for_string_with_context(search_string, context, max_items)
            items.extend(extension_plugin_items)

        # loop through the plugin chain (filter, mapper, sorter)
        for filter_plugin in self.eureka_engine_plugin.eureka_item_filter_plugins:
            filtered_items = filter_plugin.process_items_for_string_with_context(items, search_string, context, max_items)
            items = filtered_items
        for mapper_plugin in self.eureka_engine_plugin.eureka_item_mapper_plugins:
            mapped_items = mapper_plugin.process_items_for_string_with_context(items, search_string, context, max_items)
            items = mapped_items
        for sorter_plugin in self.eureka_engine_plugin.eureka_item_sorter_plugins:
            sorted_items = sorter_plugin.process_items_for_string_with_context(items, search_string, context, max_items)
            items = sorted_items

        # Slices to get the first max_items (when not specified returns all items)
        items = items[0:max_items]

        return items
