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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

class TemplateHandlerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Template Handler plugin.
    """

    id = "pt.hive.colony.plugins.template.handler"
    name = "Template Handler Plugin"
    short_name = "Template Handler"
    description = "Template Handler Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["http_python_handler"]
    capabilities_allowed = ["template_handler_extension"]
    dependencies = []
    events_handled = []
    events_registrable = []

    template_handler = None

    template_handler_extension_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global template_handler
        import template_handler.handler.template_handler_system
        self.template_handler = template_handler.handler.template_handler_system.TemplateHandler(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.template.handler", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.template.handler", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_handler_filename(self):
        return self.template_handler.get_handler_filename()

    def is_request_handler(self, request):
        return self.template_handler.is_request_handler(request)

    def handle_request(self, request):
        self.template_handler.handle_request(request)

    @colony.plugins.decorators.load_allowed_capability("template_handler_extension")
    def template_handler_extension_load_allowed(self, plugin, capability):
        self.template_handler_extension_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("template_handler_extension")
    def template_handler_extension_unload_allowed(self, plugin, capability):
        self.template_handler_extension_plugins.remove(plugin)
