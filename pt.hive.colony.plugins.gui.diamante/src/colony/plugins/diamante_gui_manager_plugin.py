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

class DiamanteGuiManagerPlugin(colony.plugins.plugin_system.Plugin):
    """
    Provides a graphical user interfaces for any Diamante converter version
    """    

    id = "pt.hive.colony.plugins.gui.diamante.gui_manager"
    name = "LCR Data Diamante GUI Manager Plugin"
    short_name = "Diamante GUI Manager"
    description = "Provides a graphical user interfaces for any Diamante converter version"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["gui_manager"]
    capabilities_allowed = ["diamante.gui.widgets"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.logic", "1.0.0")]
    events_handled = ["gui_widget_plugin_changed"]
    events_registrable = []
    valid = True

    codebase = None
    """ Base code supplied by this plugin, meant to be accessible only with the methods supplied by the plugin class"""
    main_logic_plugin = None
    """ Main converter logic plugin instance """
    widget_plugins = []

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global diamante_gui
        import diamante_gui.diamante.diamante_gui_manager
        self.codebase = diamante_gui.diamante.diamante_gui_manager.DiamanteGuiManager(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.codebase = None
        self.main_logic_plugin = None

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)
        if capability == "diamante.gui.widgets":
            self.widget_plugins.append(plugin)
            self.generate_event("gui_widget_plugin_changed", ["added", plugin])

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)
        if capability == "diamante.gui.widgets":
            self.widget_plugins.remove(plugin)
            self.generate_event("gui_widget_plugin_changed", ["removed", plugin])

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)
        if "main_logic" in plugin.capabilities:
            self.main_logic_plugin = plugin            

    def get_available_gui_versions(self):
        """
        @see: colony.plugins.diamante_gui.diamante.diamante_gui_manager.get_available_gui_versions()
        """
        return self.codebase.get_available_gui_versions()

    def do_panel(self, parent, logic_version, tab_name = "none"):
        """
        @see: colony.plugins.diamante_gui.diamante.diamante_gui_manager.do_panel()
        """
        return self.codebase.do_panel(parent, logic_version, tab_name)

    #@todo: comment
    def process_query(self, args):
        self.codebase.process_query(args)
