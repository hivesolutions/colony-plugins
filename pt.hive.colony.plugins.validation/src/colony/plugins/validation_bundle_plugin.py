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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class ValidationBundlePlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Validation Bundle Plugin
    """

    id = "pt.hive.colony.plugins.validation.bundle"
    name = "Bundle Validation Plugin"
    short_name = "Bundle Validation"
    description = "A plugin used to check that all bundles are valid in terms of integrity"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/validation_bundle/bundle/resources/baf.xml"
    }
    capabilities = [
        "validation.bundle",
        "_console_command_extension",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.0.0")
    ]
    main_modules = [
        "validation_bundle.bundle.console_validation_bundle",
        "validation_bundle.bundle.validation_bundle_system"
    ]

    validation_bundle = None
    """ The validation bundle """

    console_validation_bundle = None
    """ The console validation bundle """

    json_plugin = None
    """ The json plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        import validation_bundle.bundle.validation_bundle_system
        import validation_bundle.bundle.console_validation_bundle
        self.validation_bundle = validation_bundle.bundle.validation_bundle_system.ValidationBundle(self)
        self.console_validation_bundle = validation_bundle.bundle.console_validation_bundle.ConsoleValidationBundle(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_console_extension_name(self):
        return self.console_validation_bundle.get_console_extension_name()

    def get_commands_map(self):
        return self.console_validation_bundle.get_commands_map()

    def validate_bundles(self, bundle_file_paths):
        return self.validation_bundle.validate_bundles(bundle_file_paths)

    def get_json_plugin(self):
        return self.json_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin
