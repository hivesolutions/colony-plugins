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

import colony.base.plugin_system
import colony.base.decorators

class ${out value=scaffold_attributes.class_name /}Plugin(colony.base.plugin_system.Plugin):
    """
    The main class for the ${out value=scaffold_attributes.short_name /} plugin.
    """

    id = "${out value=scaffold_attributes.plugin_id /}"
    name = "${out value=scaffold_attributes.short_name /} Plugin"
    short_name = "${out value=scaffold_attributes.short_name /}"
    description = "${out value=scaffold_attributes.description /} plugin"
    version = "${out value=scaffold_attributes.plugin_version /}"
    author = "${out value=scaffold_attributes.author /}"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "plugin_test_case_bundle",
        "web.mvc_service"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.web.mvc.utils", "${out value=scaffold_attributes.plugin_version /}")
    ]
    main_modules = [
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_controllers",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_entity_models",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_exceptions",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test"
    ]

    ${out value=scaffold_attributes.variable_name /} = None
    """ The ${out value=scaffold_attributes.short_name_lowercase /} """

    ${out value=scaffold_attributes.variable_name /}_test = None
    """ The ${out value=scaffold_attributes.short_name_lowercase /} test """

    web_mvc_utils_plugin = None
    """ The web mvc utils plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system
        import ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test
        self.${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system.${out value=scaffold_attributes.class_name /}(self)
        self.${out value=scaffold_attributes.variable_name /}_test = ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test.${out value=scaffold_attributes.class_name /}Test(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.${out value=scaffold_attributes.variable_name /}.load_components()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("${out value=scaffold_attributes.plugin_id /}", "${out value=scaffold_attributes.plugin_version /}")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("${out value=scaffold_attributes.plugin_id /}", "${out value=scaffold_attributes.plugin_version /}")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("${out value=scaffold_attributes.plugin_id /}", "${out value=scaffold_attributes.plugin_version /}")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_plugin_test_case_bundle(self):
        return self.${out value=scaffold_attributes.variable_name /}_test.get_plugin_test_case_bundle()

    def get_patterns(self):
        return self.${out value=scaffold_attributes.variable_name /}.get_patterns()

    def get_communication_patterns(self):
        return self.${out value=scaffold_attributes.variable_name /}.get_communication_patterns()

    def get_resource_patterns(self):
        return self.${out value=scaffold_attributes.variable_name /}.get_resource_patterns()

    def get_web_mvc_utils_plugin(self):
        return self.web_mvc_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.web.mvc.utils")
    def set_web_mvc_utils_plugin(self, web_mvc_utils_plugin):
        self.web_mvc_utils_plugin = web_mvc_utils_plugin
