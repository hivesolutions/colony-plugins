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

__revision__ = "$LastChangedRevision: 723 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-15 21:09:57 +0000 (Seg, 15 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class TemplateHandlerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Template Handler plugin.
    """

    id = "pt.hive.colony.plugins.template.handler"
    name = "Template Handler Plugin"
    short_name = "Template Handler"
    description = "Template Handler Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/template_handler/handler/resources/baf.xml"
    }
    capabilities = [
        "http_python_handler",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "template_handler_extension"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.format.mime", "1.0.0")
    ]
    main_modules = [
        "template_handler.handler.template_handler_exceptions",
        "template_handler.handler.template_handler_system"
    ]

    template_handler = None
    """ The template handler """

    template_handler_extension_plugins = []
    """ The template handler extension plugins """

    format_mime_plugin = None
    """ The format mime plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import template_handler.handler.template_handler_system
        self.template_handler = template_handler.handler.template_handler_system.TemplateHandler(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

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

    def get_handler_filename(self):
        return self.template_handler.get_handler_filename()

    def is_request_handler(self, request):
        return self.template_handler.is_request_handler(request)

    def handle_request(self, request):
        return self.template_handler.handle_request(request)

    @colony.base.decorators.load_allowed_capability("template_handler_extension")
    def template_handler_extension_load_allowed(self, plugin, capability):
        self.template_handler_extension_plugins.append(plugin)

    @colony.base.decorators.unload_allowed_capability("template_handler_extension")
    def template_handler_extension_unload_allowed(self, plugin, capability):
        self.template_handler_extension_plugins.remove(plugin)

    def get_format_mime_plugin(self):
        return self.format_mime_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.format.mime")
    def set_format_mime_plugin(self, format_mime_plugin):
        self.format_mime_plugin = format_mime_plugin
