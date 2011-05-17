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
        "_console_command_extension",
        "plugin_test_case_bundle"
    ]
    main_modules = [
        "${out value=scaffold_attributes.backend_namespace /}.console_${out value=scaffold_attributes.variable_name /}",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_exceptions",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test"
    ]

    ${out value=scaffold_attributes.variable_name /} = None
    """ The ${out value=scaffold_attributes.short_name_lowercase /} """

    console_${out value=scaffold_attributes.variable_name /} = None
    """ The console ${out value=scaffold_attributes.short_name_lowercase /} plugin """

    ${out value=scaffold_attributes.variable_name /}_test = None
    """ The ${out value=scaffold_attributes.short_name_lowercase /} test """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global ${out value=scaffold_attributes.root_folder_name /}
        import ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system
        import ${out value=scaffold_attributes.backend_namespace /}.console_${out value=scaffold_attributes.variable_name /}
        import ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test
        self.${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system.${out value=scaffold_attributes.class_name /}(self)
        self.console_${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.backend_namespace /}.console_${out value=scaffold_attributes.variable_name /}.Console${out value=scaffold_attributes.class_name /}(self)
        self.${out value=scaffold_attributes.variable_name /}_test = ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_test.${out value=scaffold_attributes.class_name /}Test(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

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

    def dummy_method(self):
        return self.${out value=scaffold_attributes.variable_name /}.dummy_method()

    def get_console_extension_name(self):
        return self.console_${out value=scaffold_attributes.variable_name /}.get_console_extension_name()

    def get_commands_map(self):
        return self.console_${out value=scaffold_attributes.variable_name /}.get_commands_map()

    def get_plugin_test_case_bundle(self):
        return self.${out value=scaffold_attributes.variable_name /}_test.get_plugin_test_case_bundle()
