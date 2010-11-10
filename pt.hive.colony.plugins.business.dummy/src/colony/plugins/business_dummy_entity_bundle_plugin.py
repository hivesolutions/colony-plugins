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

__revision__ = "$LastChangedRevision: 2300 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:10:15 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class BusinessDummyEntityBundlePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Business Dummy Entity Bundle plugin.
    """

    id = "pt.hive.colony.plugins.business.dummy.entity_bundle"
    name = "Business Dummy Entity Bundle Plugin"
    short_name = "Business Dummy Entity Bundle"
    description = "Business Dummy Entity Bundle Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/business_dummy/dummy_entity_bundle/resources/baf.xml",
                  "data_namespaces" : ("pt.hive.colony.business.dummy",)}
    capabilities = ["entity_bundle", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.business.helper", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["business_dummy.dummy_entity_bundle.business_dummy_entity_bundle_classes",
                    "business_dummy.dummy_entity_bundle.business_dummy_entity_bundle_system"]

    business_dummy_entity_bundle = None

    business_helper_plugin = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global business_dummy
        import business_dummy.dummy_entity_bundle.business_dummy_entity_bundle_system
        self.business_dummy_entity_bundle = business_dummy.dummy_entity_bundle.business_dummy_entity_bundle_system.BusinessDummyEntityBundle(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.business_dummy_entity_bundle.generate_classes()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.business.dummy.entity_bundle", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_entity_bundle(self):
        return self.business_dummy_entity_bundle.get_entity_bundle()

    def get_entity_bundle_map(self):
        return self.business_dummy_entity_bundle.get_entity_bundle_map()

    def get_business_helper_plugin(self):
        return self.business_helper_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.business.helper")
    def set_business_helper_plugin(self, business_helper_plugin):
        self.business_helper_plugin = business_helper_plugin
