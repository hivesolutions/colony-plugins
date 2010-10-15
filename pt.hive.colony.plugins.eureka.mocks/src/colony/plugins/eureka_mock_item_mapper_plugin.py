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

class EurekaMockItemMapperPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the sample Mock Item Mapper plugin.
    """

    id = "pt.hive.colony.plugins.eureka.mock_item_mapper_plugin"
    name = "Eureka Mock Item Mapper Plugin"
    short_name = "Eureka Mock Item Mapper"
    description = "Eureka Mock Item Mapper plugin to illustrate and test the eureka_item_mapper capability"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/eureka_mock_item_mapper/mock_item_mapper/resources/baf.xml"}
    capabilities = ["eureka_item_processer.mapper", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["eureka_mock_item_mapper.mock_item_mapper.eureka_mock_item_mapper_system"]

    mock_item_mapper = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)

        self.mock_item_mapper = MockItemMapper()

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

        # scores each of the items in the list using the above scorer function
        mapped_items = [self.mock_item_mapper.scorer(item, search_string) for item in items]

        return mapped_items[0:max_items]

class MockItemMapper:

    def scorer(self,item, search_string):
        """
        Sets the score on an EurekaItem by searching for similarity with an input string.

        @type item: EurekaItem
        @param item: The EurekaItem to be scored according to the search_string.
        @type search_string: String
        @param search_string: The search string.
        """

        search_string_list = search_string.split()
        keywords_found = [word for word in search_string_list if word in item.keywords]

        # score according to the ratio of keywords found by input words received
        # also factors in the size of the input words in relation to the overall keywords length
        joined_keywords_found_length = len("".join(keywords_found))
        joined_keywords_length = len("".join(item.keywords))
        item.score = float(joined_keywords_found_length) / float(joined_keywords_length)

        return item
