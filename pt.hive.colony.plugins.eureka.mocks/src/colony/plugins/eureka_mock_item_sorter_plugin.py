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

class EurekaMockItemSorterPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the sample Mock Item Sorter plugin.
    """

    id = "pt.hive.colony.plugins.eureka.mock_item_sorter_plugin"
    name = "Eureka Mock Item Sorter Plugin"
    short_name = "Eureka Mock Item Sorter"
    description = "Eureka Mock Item Sorter plugin to illustrate and test the eureka_item_processer.sorter capability"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/eureka_mock_item_sorter/mock_item_sorter/resources/baf.xml"}
    capabilities = ["eureka_item_processer.sorter", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["eureka_mock_item_sorter.mock_item_sorter.eureka_mock_item_sorter_system"]

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

    def process_items_for_string_with_context(self, items, search_string = None, context = None, max_items = None):
        """
        Returns a raw list with all the items matching the search_string.

        @type input_list: List
        @param input_list: Processed list of EurekaItems.
        """

        # scores each of the items in the list using the above scorer function
        sorted_items = self.sort_by_attribute(items, "score")
        sorted_items.reverse()

        return sorted_items[0:max_items]

    def sort_by_attribute(self, sequence, attribute):
        """
        Sorts the sequence items based on the values of the given attribute.

        @type sequence: List
        @param sequence: The list of EurekaItems to be sorted.
        @type attribute: String
        @param attribute: The name of the attribute to be used as sorter.
        @rtype: List
        @return: The ordered sequence of values.
        """

        intermed = [(getattr(sequence[index], attribute), index, sequence[index]) for index in xrange(len(sequence))]
        intermed.sort()
        return [tuple[-1] for tuple in intermed]
