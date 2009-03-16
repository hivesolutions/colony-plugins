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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
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

    id = "pt.hive.colony.plugins.data_converter.tools.internal_structure_visualizer"
    name = "Internal Structure Visualizer Plugin"
    short_name = "Internal Structure Visualizer"
    description = "Internal Structure Visualizer"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["gui_panel", "data_converter_observer"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.gui.tree_visualizer", "1.0.0")]
    events_handled = []
    events_registrable = []
    
    panel = None
    """ Internal structure visualizer panel """
    
    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global data_converter
        import data_converter.tools.internal_structure_visualizer.internal_structure_visualizer_system
        
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

    def do_panel(self, parent):
        self.panel = data_converter.tools.internal_structure_visualizer.internal_structure_visualizer_system.InternalStructureVisualizerPanel(parent, self)
        return self.panel

    def notify_data_conversion_status(self, status):
        """
        Notifies this plugin of the current data conversion status.
        
        @type status: Dictionary
        @param status: Dictionary with informations related to the data conversion status.
        """
        
        internal_structure = status["internal_structure"]
        if self.panel:
            self.panel.set_internal_structure(internal_structure)
