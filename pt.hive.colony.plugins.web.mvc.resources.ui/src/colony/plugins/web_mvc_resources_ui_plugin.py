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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class WebMvcResourcesUiPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Web Mvc Resources Ui plugin.
    """

    id = "pt.hive.colony.plugins.web.mvc.resources.ui"
    name = "Web Mvc Resources Ui Plugin"
    short_name = "Web Mvc Resources Ui"
    description = "The plugin that offers the web mvc resources ui infrastructure"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/web_mvc_resources_ui/resources_ui/resources/baf.xml"
    }
    capabilities = [
        "web.mvc_resources",
        "build_automation_item"
    ]
    main_modules = [
        "web_mvc_resources_ui.resources_ui.web_mvc_resources_ui_system"
    ]

    web_mvc_resources_ui = None
    """ The web mvc resources ui """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global web_mvc_resources_ui
        import web_mvc_resources_ui.resources_ui.web_mvc_resources_ui_system
        self.web_mvc_resources_ui = web_mvc_resources_ui.resources_ui.web_mvc_resources_ui_system.WebMvcResourcesUi(self)

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

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_resources_path(self):
        """
        Retrieves the path to the resources.
        This path should be used as the base reference to the resources.

        @rtype: String
        @return: The path to the resources.
        """

        return self.web_mvc_resources_ui.get_resources_path()
