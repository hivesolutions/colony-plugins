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

__revision__ = "$LastChangedRevision: 2114 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 15:29:05 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class InternalStructureVisualizerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Internal Structure Visualizer plugin
    """

    id = "pt.hive.colony.plugins.misc.gui.internal_structure_visualizer"
    name = "Internal Structure Visualizer Plugin"
    short_name = "Internal Structure Visualizer"
    description = "Dependencies Visualizer Plugin"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["gui_panel"]
    capabilities_allowed = ["adapter.input"]
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.gui.tree_visualizer", "1.0.0")]
    events_handled = []
    events_registrable = ["internal_structure_changed"]
    
    panel = None
    
    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global misc_gui
        import misc_gui.internal_structure_visualizer.internal_structure_visualizer_system
        
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

    @colony.plugins.decorators.event_handler("pt.hive.colony.plugins.misc.gui.internal_structure_visualizer", "1.0.0")
    def event_handler(self, event_name, *event_args):
        try:
            colony.plugins.plugin_system.Plugin.event_handler(self, event_name, *event_args)
        except Exception, exception:
            colony.plugins.plugin_system.Plugin.treat_exception(self, exception)     

    def do_panel(self, parent):
        self.panel = misc_gui.internal_structure_visualizer.internal_structure_visualizer_system.InternalStructureVisualizerPanel(parent, self)
        return self.panel

    @colony.plugins.decorators.event_handler_method("internal_structure_changed")
    def internal_structure_changed_handler(self, event_name, internal_structure, *event_args):
        if self.panel:
            self.panel.set_internal_structure(internal_structure)
