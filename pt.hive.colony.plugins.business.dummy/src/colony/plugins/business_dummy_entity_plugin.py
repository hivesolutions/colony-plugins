#!/usr/bin/python
# -*- coding: utf-8 -*-

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

class BusinessDummyEntityPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Business Dummy Entity plugin.
    """

    id = "pt.hive.colony.plugins.business.dummy.entity"
    name = "Business Dummy Entity Plugin"
    short_name = "Business Dummy Entity"
    description = "Business Dummy Entity Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/business_dummy/dummy_entity/resources/baf.xml",
        "data_namespaces" : (
            "pt.hive.colony.business.dummy"
        ,)
    }
    capabilities = [
        "entity",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.business.helper", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.business.dummy.entity_bundle", "1.0.0")
    ]
    main_modules = [
        "business_dummy.dummy_entity.business_dummy_entity_class",
        "business_dummy.dummy_entity.business_dummy_entity_system"
    ]

    business_helper_plugin = None
    """ The business helper plugin """

    business_dummy_entity_bundle_plugin = None
    """ The business dummy entity bundle plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import business_dummy.dummy_entity.business_dummy_entity_system
        self.business_dummy_entity = business_dummy.dummy_entity.business_dummy_entity_system.BusinessDummyEntity(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.business_dummy_entity.generate_class()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_entity_class(self):
        return self.business_dummy_entity.get_entity_class()

    def get_business_helper_plugin(self):
        return self.business_helper_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.business.helper")
    def set_business_helper_plugin(self, business_helper_plugin):
        self.business_helper_plugin = business_helper_plugin

    def get_business_dummy_entity_bundle_plugin(self):
        return self.business_dummy_entity_bundle_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.business.dummy.entity_bundle")
    def set_business_dummy_entity_bundle_plugin(self, business_dummy_entity_bundle_plugin):
        self.business_dummy_entity_bundle_plugin = business_dummy_entity_bundle_plugin
