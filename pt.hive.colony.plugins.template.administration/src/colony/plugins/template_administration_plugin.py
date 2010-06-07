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

__revision__ = "$LastChangedRevision: 723 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-15 21:09:57 +0000 (Seg, 15 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class TemplateAdministrationPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Template Administration plugin.
    """

    id = "pt.hive.colony.plugins.template.administration"
    name = "Template Administration Plugin"
    short_name = "Template Administration"
    description = "Template Administration Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/template_administration/administration/resources/baf.xml"}
    capabilities = ["template_administration", "template_handler_extension", "build_automation_item"]
    capabilities_allowed = ["template_administration_extension.menu_item", "template_administration_extension.top_menu_item",
                            "template_administration_extension.status_item", "template_administration_extension.content_item",
                            "template_administration_extension.bundle"]
    dependencies = []
    events_handled = []
    events_registrable = []

    template_administration = None

    template_administration_extension_plugins = []
    template_administration_extension_menu_item_plugins = []
    template_administration_extension_top_menu_item_plugins = []
    template_administration_extension_status_item_plugins = []
    template_administration_extension_content_item_plugins = []
    template_administration_extension_bundle_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global template_administration
        import template_administration.administration.template_administration_system
        self.template_administration = template_administration.administration.template_administration_system.TemplateAdministration(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.template.administration", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.template.administration", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_handler_filename(self):
        return self.template_administration.get_handler_filename()

    def get_template_path(self):
        return self.template_administration.get_template_path()

    def get_resources_paths_map(self):
        return self.template_administration.get_resources_paths_map()

    def get_css_files(self):
        return self.template_administration.get_css_files()

    def get_js_files(self):
        return self.template_administration.get_js_files()

    def get_menu_items(self):
        return self.template_administration.get_menu_items()

    def get_content_items(self):
        return self.template_administration.get_content_items()

    @colony.plugins.decorators.load_allowed_capability("template_administration_extension.menu_item")
    def template_administration_extension_menu_item_load_allowed(self, plugin, capability):
        self.template_administration_extension_menu_item_plugins.append(plugin)
        self.template_administration_extension_plugins.append(plugin)
        self.template_administration.update_resources()

    @colony.plugins.decorators.load_allowed_capability("template_administration_extension.content_item")
    def template_administration_extension_content_item_load_allowed(self, plugin, capability):
        self.template_administration_extension_content_item_plugins.append(plugin)
        self.template_administration_extension_plugins.append(plugin)
        self.template_administration.update_resources()

    @colony.plugins.decorators.load_allowed_capability("template_administration_extension.bundle")
    def template_administration_extension_bundle_load_allowed(self, plugin, capability):
        self.template_administration_extension_bundle_plugins.append(plugin)
        self.template_administration_extension_plugins.append(plugin)
        self.template_administration.update_resources()

    @colony.plugins.decorators.unload_allowed_capability("template_administration_extension.menu_item")
    def template_administration_extension_menu_item_unload_allowed(self, plugin, capability):
        self.template_administration_extension_menu_item_plugins.remove(plugin)
        self.template_administration_extension_plugins.remove(plugin)
        self.template_administration.update_resources()

    @colony.plugins.decorators.unload_allowed_capability("template_administration_extension.content_item")
    def template_administration_extension_content_item_unload_allowed(self, plugin, capability):
        self.template_administration_extension_content_item_plugins.remove(plugin)
        self.template_administration_extension_plugins.remove(plugin)
        self.template_administration.update_resources()

    @colony.plugins.decorators.unload_allowed_capability("template_administration_extension.bundle")
    def template_administration_extension_bundle_unload_allowed(self, plugin, capability):
        self.template_administration_extension_bundle_plugins.remove(plugin)
        self.template_administration_extension_plugins.remove(plugin)
        self.template_administration.update_resources()
