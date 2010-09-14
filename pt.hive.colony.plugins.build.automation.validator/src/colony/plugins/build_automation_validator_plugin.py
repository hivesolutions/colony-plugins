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

class BuildAutomationValidatorPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Build Automation Validator plugin
    """

    id = "pt.hive.colony.plugins.build.automation.validator"
    name = "Build Automation Validator Plugin"
    short_name = "Build Automation Validator"
    description = "A plugin used to validate that all resources are valid for build automation"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT,
                 colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/build_automation_validator/resources/baf.xml"}
    capabilities = ["console_command_extension", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["build_automation_validator.build_automation_validator_system",
                    "build_automation_validator.console_build_automation_validator"]

    build_automation_validator = None
    """ The build automation validator """

    console_build_automation_validator = None
    """ The console build automation validator """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        global build_automation_validator
        import build_automation_validator.build_automation_validator_system
        import build_automation_validator.console_build_automation_validator
        self.build_automation_validator = build_automation_validator.build_automation_validator_system.BuildAutomationValidator(self)
        self.console_build_automation_validator = build_automation_validator.console_build_automation_validator.ConsoleBuildAutomationValidator(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.build.automation.validator", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.build.automation.validator", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.build.automation.validator", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_console_extension_name(self):
        return self.console_build_automation_validator.get_console_extension_name()

    def get_all_commands(self):
        return self.console_build_automation_validator.get_all_commands()

    def get_handler_command(self, command):
        return self.console_build_automation_validator.get_handler_command(command)

    def get_help(self):
        return self.console_build_automation_validator.get_help()

    def validate_build_automation(self):
        self.build_automation_validator.validate_build_automation()

    def validate_build_automation_plugin(self, plugin_id):
        return self.build_automation_validator.validate_build_automation_plugin(plugin_id)
