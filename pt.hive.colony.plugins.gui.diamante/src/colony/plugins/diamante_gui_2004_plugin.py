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

__revision__ = "$LastChangedRevision: 2107 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 15:06:41 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class DiamanteGuiPlugin_2004(colony.plugins.plugin_system.Plugin):
    """
    Provides wx widgets that are required to assemble the Diamante 2004 migrator interface
    """    

    id = "pt.hive.colony.plugins.gui.diamante.diamante_2004"
    name = "GUI widgets for the Diamante 2004 migrator"
    short_name = "GUI widgets Diamante 2004"
    description = "Provides wx widgets that are required to assemble the Diamante 2004 migrator interface"
    version = "4.4.1"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["diamante.gui.widgets"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.gui.diamante.gui_manager", "1.0.0"),
                    colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.gui.diamante.diamante_2003", "4.4.1")]
    events_handled = []
    events_registrable = []
    valid = True

    codebase = None
    """ Base code supplied by this plugin, meant to be accessible only with the methods supplied by the plugin class"""
    input_adapter_plugin = None
    """ Input adapter that this plugin will use """
    gui_manager_plugin = None
    """ Reference to the parent gui manager plugin instance """
    widget_plugins = []
    """ Widget plugins this one depends on """

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global diamante_gui
        import diamante_gui.diamante.diamante_gui_2004
        self.codebase = diamante_gui.diamante.diamante_gui_2004.DiamanteGui_2004(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.codebase = None
        self.input_adapter_plugin = None
        self.gui_manager_plugin = None
        self.widget_plugins = []

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)
        if "diamante.gui.widgets" in plugin.capabilities:
            self.widget_plugins.append(plugin)
        elif "input_adapter" in plugin.capabilities:
            self.input_adapter_plugin = plugin
        elif "gui_manager" in plugin.capabilities:
            self.gui_manager_plugin = plugin

    def do_panel(self, panel_structure):
        """
        @see: colony.plugins.diamante_gui.diamante.diamante_gui_2004.do_panel()
        """
        return self.codebase.do_panel(panel_structure)

    def get_product_version(self):
        """
        Returns the product version supported by the graphical user interface this plugin is supposed to contribute widgets to
        
        @return: String with a product version
        """
        return self.codebase.product_version
