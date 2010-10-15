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
import colony.base.decorators

class EurekaEnginePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Eureka Engine plugin.
    """

    id = "pt.hive.colony.plugins.eureka.engine"
    name = "Eureka Engine Plugin"
    short_name = "Eureka Engine"
    description = "Eureka Engine Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/eureka_engine/engine/resources/baf.xml"}
    capabilities = ["eureka_engine", "plugin_test_case_bundle", "build_automation_item"]
    capabilities_allowed = ["eureka_item_extension", "eureka_engine_item_processer.filter", "eureka_engine_item_processer.mapper", "eureka_engine_item_processer.sorter"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["eureka_engine.engine.eureka_engine_system", "eureka_engine.engine.eureka_engine_test", "eureka_engine.engine.eureka_item"]

    eureka_engine = None
    eureka_engine_test = None

    eureka_item_extension_plugins = []
    eureka_item_filter_plugins = []
    eureka_item_mapper_plugins = []
    eureka_item_sorter_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global eureka
        import eureka_engine.engine.eureka_engine_system
        import eureka_engine.engine.eureka_engine_test
        self.eureka_engine = eureka_engine.engine.eureka_engine_system.EurekaEngine(self)
        self.eureka_engine_test = eureka_engine.engine.eureka_engine_test.EurekaEngineTest(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.eureka.engine", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.eureka.engine", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_items_for_string(self, search_string, max_items):
        """
        Returns a processed list of max_items EurekaItems, matching the supplied search_string.

        @type search_string: String
        @param search_string: The string to be matched.
        @type max_items: Integer
        @param max_items: The number of items to be returned.
        @rtype: List
        @return: A processed list of max_items EurekaItems, matching the supplied search_string.
        """

        return self.eureka_engine.get_items_for_string(search_string, max_items)

    def get_items_for_string_with_context(self, search_string, context, max_items):
        """
        Returns a processed list of max_items EurekaItems, matching the supplied search_string for the supplied context.

        @type search_string: String
        @param search_string: The string to be matched.
        @type max_items: Integer
        @param max_items: The number of items to be returned.
        @type context: List
        @param context: A stack of EurekaItems to allow Eureka to take the previously selected items into account
        while matching the search_string.
        @rtype: List
        @return: A processed list of max_items EurekaItems, matching the supplied search_string for the supplied context.
        """

        return self.eureka_engine.get_items_for_string_with_context(search_string, context, max_items)

    def get_all_items(self, search_string):
        """
        Returns an unprocessed list with all the items matching the search_string.
        """

        return self.eureka_engine.get_all_items(search_string)

    def get_plugin_test_case_bundle(self):
        return self.eureka_engine_test.get_plugin_test_case_bundle()

    @colony.base.decorators.load_allowed_capability("eureka_item_extension")
    def eureka_item_extension_load_allowed(self, plugin, capability):
        self.eureka_item_extension_plugins.append(plugin)

    @colony.base.decorators.load_allowed_capability("eureka_engine_item_processer.filter")
    def eureka_item_filter_load_allowed(self, plugin, capability):
        self.eureka_item_filter_plugins.append(plugin)

    @colony.base.decorators.load_allowed_capability("eureka_engine_item_processer.mapper")
    def eureka_item_mapper_load_allowed(self, plugin, capability):
        self.eureka_item_mapper_plugins.append(plugin)

    @colony.base.decorators.load_allowed_capability("eureka_engine_item_processer.sorter")
    def eureka_item_sorter_load_allowed(self, plugin, capability):
        self.eureka_item_sorter_plugins.append(plugin)

    @colony.base.decorators.unload_allowed_capability("eureka_item_extension")
    def eureka_item_extension_unload_allowed(self, plugin, capability):
        self.eureka_item_extension_plugins.remove(plugin)

    @colony.base.decorators.unload_allowed_capability("eureka_engine_item_processer.filter")
    def eureka_item_filter_unload_allowed(self, plugin, capability):
        self.eureka_item_filter_plugins.remove(plugin)

    @colony.base.decorators.unload_allowed_capability("eureka_engine_item_processer.mapper")
    def eureka_item_mapper_unload_allowed(self, plugin, capability):
        self.eureka_item_mapper_plugins.remove(plugin)

    @colony.base.decorators.unload_allowed_capability("eureka_engine_item_processer.sorter")
    def eureka_item_sorter_unload_allowed(self, plugin, capability):
        self.eureka_item_sorter_plugins.remove(plugin)
