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

class EmailBuildAutomationExtensionPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Email Build Automation Extension plugin
    """

    id = "pt.hive.colony.plugins.build.automation.extensions.email"
    name = "Email Build Automation Extension Plugin"
    short_name = "Email Build Automation Extension"
    description = "A plugin to manage the email build automation tasks"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/build_automation_extensions/email/resources/baf.xml"
    }
    capabilities = [
        "build_automation_extension",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.client.smtp", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.format.mime", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.format.mime.utils", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.template_engine.manager", "1.0.0")
    ]
    main_modules = [
        "build_automation_extensions.email.email_build_automation_extension_system"
    ]

    email_build_automation_extension = None
    """ The email build automation extension """

    main_client_smtp_plugin = None
    """ The main client smtp plugin """

    format_mime_plugin = None
    """ The format mime plugin """

    format_mime_utils_plugin = None
    """ The format mime utils plugin """

    template_engine_manager_plugin = None
    """ The template engine manager plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import build_automation_extensions.email.email_build_automation_extension_system
        self.email_build_automation_extension = build_automation_extensions.email.email_build_automation_extension_system.EmailBuildAutomationExtension(self)

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

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        return self.email_build_automation_extension.run_automation(plugin, stage, parameters, build_automation_structure, logger)

    def get_main_client_smtp_plugin(self):
        return self.main_client_smtp_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.client.smtp")
    def set_main_client_smtp_plugin(self, main_client_smtp_plugin):
        self.main_client_smtp_plugin = main_client_smtp_plugin

    def get_format_mime_plugin(self):
        return self.format_mime_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.format.mime")
    def set_format_mime_plugin(self, format_mime_plugin):
        self.format_mime_plugin = format_mime_plugin

    def get_format_mime_utils_plugin(self):
        return self.format_mime_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.format.mime.utils")
    def set_format_mime_utils_plugin(self, format_mime_utils_plugin):
        self.format_mime_utils_plugin = format_mime_utils_plugin

    def get_template_engine_manager_plugin(self):
        return self.template_engine_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.template_engine.manager")
    def set_template_engine_manager_plugin(self, template_engine_manager_plugin):
        self.template_engine_manager_plugin = template_engine_manager_plugin
