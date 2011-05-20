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

class ProgressInformationPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Progress Information plugin
    """

    id = "pt.hive.colony.plugins.misc.gui.progress_information"
    name = "Progress Information Plugin"
    short_name = "Progress Information"
    description = "Progress Information Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/misc_gui/progress_information/resources/baf.xml"
    }
    capabilities = [
        "gui_progress_information",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "task_information"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.bitmap_loader", "1.0.0"),
        colony.base.plugin_system.PackageDependency("Wx Python", "wx", "2.8.7.x", "http://wxpython.org")
    ]
    events_handled = [
        "gui_progress_information_changed"
    ]
    events_registrable = [
        "task_information_changed"
    ]
    main_modules = [
        "misc_gui.progress_information.progress_information_logic",
        "misc_gui.progress_information.progress_information_system"
    ]

    progress_information = None
    """ The progress information """

    bitmap_loader_plugin = None
    """ The bitmap loader plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import misc_gui.progress_information.progress_information_system
        self.progress_information = misc_gui.progress_information.progress_information_system.ProgressInformation(self)

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

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.misc.gui.progress_information", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.event_handler("pt.hive.colony.plugins.misc.gui.progress_information", "1.0.0")
    def event_handler(self, event_name, *event_args):
        try:
            colony.base.plugin_system.Plugin.event_handler(self, event_name, *event_args)
        except Exception, exception:
            colony.base.plugin_system.Plugin.treat_exception(self, exception)

    def do_panel(self, parent):
        return self.progress_information.do_panel(parent)

    def add_task_progress_information_item(self, task_name, task_description, current_description, percentage_complete, bitmap):
        return self.progress_information.add_task_progress_information_item(task_name, task_description, current_description, percentage_complete, bitmap)

    @colony.base.decorators.event_handler_method("task_information_changed")
    def task_information_changed_handler(self, event_name, *event_args):
        self.progress_information.process_task_information_changed_event(event_name, event_args)

    def get_bitmap_loader_plugin(self):
        return self.bitmap_loader_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.bitmap_loader")
    def set_bitmap_loader_plugin(self, bitmap_loader_plugin):
        self.bitmap_loader_plugin = bitmap_loader_plugin
