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

__revision__ = "$LastChangedRevision: 210 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-27 19:06:07 +0000 (Seg, 27 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class ColonyIntegrationBuildAutomationItemPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Colony Integration Build Automation Item plugin.
    """

    id = "pt.hive.colony.plugins.build.automation.items.colony_integration"
    name = "Colony Integration Build Automation Item Plugin"
    short_name = "Colony Integration Build Automation Item"
    description = "The build automation item for the integration of the colony framework"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/build_automation_items/colony_integration/resources/baf.xml"
    }
    capabilities = [
        "build_automation_item"
    ]
    main_modules = [
        "build_automation_items.colony_integration.colony_integration_build_automation_item_system"
    ]

    colony_integration_build_automation_item = None
    """ The colony integration build automation item """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import build_automation_items.colony_integration.colony_integration_build_automation_item_system
        self.colony_integration_build_automation_item = build_automation_items.colony_integration.colony_integration_build_automation_item_system.ColonyIntegrationBuildAutomationItem(self)

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
