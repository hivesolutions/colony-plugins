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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import colony.base.plugin_system
import colony.base.decorators

class MainGuiPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Gui Main plugin.
    """

    id = "pt.hive.colony.plugins.main.gui"
    name = "Gui Main Plugin"
    short_name = "Gui Main"
    description = "Gui Main Plugin for wx bindings"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_gui/gui/resources/baf.xml"
    }
    capabilities = [
        "main",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "gui_panel"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.bitmap_loader", "1.0.0"),
        colony.base.plugin_system.PackageDependency("Wx Python", "wx", "2.8.7.x", "http://wxpython.org")
    ]
    main_modules = [
        "main_gui.gui.main_gui_system"
    ]

    main_gui = None
    """ The main gui """

    gui_panel_plugins = []
    """ The gui panel plugins """

    bitmap_loader_plugin = None
    """ The bitmap loader plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_gui.gui.main_gui_system
        self.main_gui = main_gui.gui.main_gui_system.MainGui(self)

        # initializes the gui panel plugins
        self.gui_panel_plugins = []

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

        # loads the main application
        self.main_gui.load_main_application()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

        # unloads the main application
        self.main_gui.unload_main_application()

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def init_complete(self):
        colony.base.plugin_system.Plugin.init_complete(self)

        # shows the main frame
        self.main_gui.show_main_application()

    @colony.base.decorators.load_allowed_capability("gui_panel")
    def gui_panel_load_allowed(self, plugin, capability):
        # adds the plugin to the gui panel plugins list
        self.gui_panel_plugins.append(plugin)

        # loads the gui panel plugin
        self.main_gui.load_gui_panel_plugin(plugin)

    @colony.base.decorators.unload_allowed_capability("gui_panel")
    def gui_panel_unload_allowed(self, plugin, capability):
        # removes the plugin from the gui panel plugins list
        self.gui_panel_plugins.remove(plugin)

        # unloads the gui panel plugin
        self.main_gui.unload_gui_panel_plugin(plugin)

    def get_bitmap_loader_plugin(self):
        return self.bitmap_loader_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.bitmap_loader")
    def set_bitmap_loader_plugin(self, bitmap_loader_plugin):
        self.bitmap_loader_plugin = bitmap_loader_plugin
