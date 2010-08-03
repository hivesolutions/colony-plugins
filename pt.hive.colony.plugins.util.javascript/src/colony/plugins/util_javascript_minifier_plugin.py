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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class JavascriptMinifierUtilPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Javascript Minifier Util plugin.
    """

    id = "pt.hive.colony.plugins.util.javascript.minifier"
    name = "Javascript Minifier Util plugin"
    short_name = "Javascript Minifier Util"
    description = "The plugin that offers minification support for javascript"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/util_javascript_minifier/javascript_minifier/resources/baf.xml"}
    capabilities = ["build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    main_modules = ["util_javascript_minifier.javascript_minifier.util_javascript_minifier_system"]

    util_javascript_minifier = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global util_javascript_minifier
        import util_javascript_minifier.javascript_minifier.util_javascript_minifier_system
        self.util_javascript_minifier = util_javascript_minifier.javascript_minifier.util_javascript_minifier_system.UtilJavascriptMinifier(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def event_handler(self, event_name, *event_args):
        colony.plugins.plugin_system.Plugin.event_handler(self, event_name, *event_args)
