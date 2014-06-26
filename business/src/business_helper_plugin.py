#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class BusinessHelperPlugin(colony.Plugin):
    """
    The main class for the Business Helper plugin.
    """

    id = "pt.hive.colony.plugins.business.helper"
    name = "Business Helper"
    description = "Business Helper Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "business_helper"
    ]
    capabilities_allowed = [
        "entity",
        "entity_bundle",
        "business_logic",
        "business_logic_bundle"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.data.entity.manager")
    ]
    main_modules = [
        "business_helper"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import business_helper
        self.system = business_helper.BusinessHelper(self)

    @colony.load_allowed
    def load_allowed(self, plugin, capability):
        colony.Plugin.load_allowed(self, plugin, capability)

    @colony.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.Plugin.unload_allowed(self, plugin, capability)

    def import_class_module(
        self,
        class_module_name,
        globals,
        locals,
        global_values,
        base_directory_path
    ):
        return self.system.import_class_module(
            class_module_name,
            globals,
            locals,
            global_values,
            base_directory_path
        )

    def import_class_module_target(
        self,
        class_module_name,
        globals,
        locals,
        global_values,
        base_directory_path,
        target_module_name
    ):
        return self.system.import_class_module(
            class_module_name,
            globals,
            locals,
            global_values,
            base_directory_path,
            target_module_name
        )

    def import_class_module_extra(
        self,
        class_module_name,
        globals,
        locals,
        global_values,
        base_directory_path,
        target_module_name,
        extra_symbols_map,
        extra_globals_map
    ):
        return self.system.import_class_module(
            class_module_name,
            globals,
            locals,
            global_values,
            base_directory_path,
            target_module_name,
            extra_symbols_map,
            extra_globals_map
        )

    def generate_bundle_map(self, bundle_classes):
        return self.system.generate_bundle_map(bundle_classes)

    def generate_module_bundle(self, bundle_module_name, bundle_map):
        return self.system.generate_module_bundle(bundle_module_name, bundle_map)

    def get_entity_class(self):
        return self.system.get_entity_class()

    def get_entity_classes_namespaces(self, namespaces):
        return self.system.get_entity_classes_namespaces(namespaces)

    def get_business_logic_classes_namespaces(self, namespaces):
        return self.system.get_business_logic_classes_namespaces(namespaces)

    @colony.load_allowed_capability("entity")
    def entity_load_allowed(self, plugin, capability):
        self.system.entity_load(plugin)

    @colony.load_allowed_capability("entity_bundle")
    def entity_bundle_load_allowed(self, plugin, capability):
        self.system.entity_bundle_load(plugin)

    @colony.load_allowed_capability("business_logic")
    def business_logic_load_allowed(self, plugin, capability):
        self.system.business_logic_load(plugin)

    @colony.load_allowed_capability("business_logic_bundle")
    def business_logic_bundle_load_allowed(self, plugin, capability):
        self.system.business_logic_bundle_load(plugin)

    @colony.unload_allowed_capability("entity")
    def entity_unload_allowed(self, plugin, capability):
        self.system.entity_unload(plugin)

    @colony.unload_allowed_capability("entity_bundle")
    def entity_bundle_unload_allowed(self, plugin, capability):
        self.system.entity_bundle_unload(plugin)

    @colony.unload_allowed_capability("business_logic")
    def business_logic_unload_allowed(self, plugin, capability):
        self.system.business_logic_unload(plugin)

    @colony.unload_allowed_capability("business_logic_bundle")
    def business_logic_bundle_unload_allowed(self, plugin, capability):
        self.system.business_logic_bundle_unload(plugin)
