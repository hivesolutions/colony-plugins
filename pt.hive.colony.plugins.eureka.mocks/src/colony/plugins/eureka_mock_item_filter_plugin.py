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

import colony.base.plugin_system

class EurekaMockItemFilterPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the sample Mock Item Filter plugin.
    """

    id = "pt.hive.colony.plugins.eureka.mock_item_filter_plugin"
    name = "Eureka Mock Item Filter Plugin"
    short_name = "Eureka Mock Item Filter"
    description = "Eureka Mock Item Filter plugin to illustrate and test the eureka_item_filter capability"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/eureka_mock_item_filter/mock_item_filter/resources/baf.xml"}
    capabilities = ["eureka_item_processer.filter", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["eureka_mock_item_filter.mock_item_filter.eureka_mock_item_filter_system"]

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def process_items_for_string(self, items, search_string, max_items):
        return self.process_items_for_string_with_context(items, search_string, None, max_items)

    def process_items_for_string_with_context(self, items, search_string, context, max_items):
        """
        Returns a raw list with all the items matching the search_string.

        @type input_list: List
        @param input_list: Processed list of EurekaItems.
        """

        search_string_list = search_string.split()
        filtered_items = []

        for item in items:
            # finds which words in the input string belong to the item's keywords
            keywords_found = [word for word in search_string_list if word in item.keywords]
            # includes the item if there are any keywords found
            if keywords_found:
                filtered_items.append(item)

        return filtered_items[0:max_items]
