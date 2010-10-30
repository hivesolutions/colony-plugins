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

class EurekaMockItemExtensionPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Eureka Engine plugin.
    """

    id = "pt.hive.colony.plugins.eureka.mock_item_extension_plugin"
    name = "Eureka Mock Item Extension Plugin"
    short_name = "Eureka Mock Item Extension"
    description = "Eureka Mock Item Extension plugin to illustrate and test the eureka_item_extension capability"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/eureka_mock_item_extension/mock_item_extension/resources/baf.xml"}
    capabilities = ["eureka_item_extension", "build_automation_item"]
    capabilities_allowed = ["eureka_item_processer.filter", "eureka_item_processer.mapper", "eureka_item_processer.sorter"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["eureka_mock_item_extension.mock_item_extension.mock_entity_item",
                    "eureka_mock_item_extension.mock_item_extension.mock_operation_item",
                    "eureka_mock_item_extension.mock_item_extension.mock_procedure_item",
                    "eureka_mock_item_extension.mock_item_extension.mock_text_parameter_item",
                    "eureka_mock_item_extension.mock_item_extension.eureka_mock_item_extension_system"]

    all_items = []

    eureka_item_filter_plugins = []
    eureka_item_mapper_plugins = []
    eureka_item_sorter_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global eureka
        global eureka_mock_item_extension
        import eureka_mock_item_extension.mock_item_extension.mock_entity_item
        import eureka_mock_item_extension.mock_item_extension.mock_operation_item
        import eureka_mock_item_extension.mock_item_extension.mock_procedure_item
        import eureka_mock_item_extension.mock_item_extension.mock_text_parameter_item

        # initializes the item list.
        # this step should usually depend on loading an XML file, or using a factory for dynamic items (such as entities)
        entity_item = eureka_mock_item_extension.mock_item_extension.mock_entity_item.MockEntityItem()
        operation_item = eureka_mock_item_extension.mock_item_extension.mock_operation_item.MockOperationItem()
        procedure_item = eureka_mock_item_extension.mock_item_extension.mock_procedure_item.MockProcedureItem()
        text_parameter_item = eureka_mock_item_extension.mock_item_extension.mock_text_parameter_item.MockTextParameterItem()

        self.all_items = [entity_item, operation_item, procedure_item, text_parameter_item]

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

        if capability == "eureka_item_processer.filter":
            self.eureka_item_filter_plugins.append(plugin)

        if capability == "eureka_item_processer.mapper":
            self.eureka_item_mapper_plugins.append(plugin)

        if capability == "eureka_item_processer.sorter":
            self.eureka_item_sorter_plugins.append(plugin)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

        if capability == "eureka_item_processer.filter":
            self.eureka_item_filter_plugins.remove(plugin)

        if capability == "eureka_item_processer.mapper":
            self.eureka_item_mapper_plugins.remove(plugin)

        if capability == "eureka_item_processer.sorter":
            self.eureka_item_sorter_plugins.remove(plugin)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_all_items(self, search_string, context, max_items):
        """
        Returns a raw list with all the items matching the search_string.
        """

        items = self.all_items

        return items[0:max_items]

    def get_items_for_string(self, search_string, context, max_items):
        return self.get_items_for_string_with_context(search_string, context, max_items)

    def get_items_for_string_with_context(self, search_string, context, max_items):
        """
        Returns a processed list, going through the plugin chain (filter, mappers and sorters).
        """

        items = self.all_items

        for filter_plugin in self.eureka_item_filter_plugins:
            filtered_items = filter_plugin.process_items_for_string_with_context(items, search_string, context, max_items)
            items = filtered_items

        for mapper_plugin in self.eureka_item_mapper_plugins:
            mapped_items = mapper_plugin.process_items_for_string_with_context(items, search_string, context, max_items)
            items = mapped_items

        for sorter_plugin in self.eureka_item_sorter_plugins:
            sorted_items = sorter_plugin.process_items_for_string_with_context(items, search_string, context, max_items)
            items = sorted_items

        return items[0:max_items]
