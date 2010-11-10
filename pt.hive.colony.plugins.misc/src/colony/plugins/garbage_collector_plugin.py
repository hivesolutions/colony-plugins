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

class GarbageCollectorPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Garbage Collector plugin.
    """

    id = "pt.hive.colony.plugins.misc.garbage_collector"
    name = "Garbage Collector Plugin"
    short_name = "Garbage Collector"
    description = "Garbage Collector Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/misc/garbage_collector/resources/baf.xml"}
    capabilities = ["garbage_collector", "console_command_extension", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["misc.garbage_collector.console_garbage_collector",
                    "misc.garbage_collector.garbage_collector_system"]

    garbage_collector = None
    console_garbage_collector = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.garbage_collector.garbage_collector_system
        import misc.garbage_collector.console_garbage_collector
        self.garbage_collector = misc.garbage_collector.garbage_collector_system.GarbageCollector(self)
        self.console_garbage_collector = misc.garbage_collector.console_garbage_collector.ConsoleGarbageCollector(self)

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

    def run_garbage_collector(self):
        return self.garbage_collector.run_garbage_collector()

    def enable(self):
        return self.garbage_collector.enable()

    def disable(self):
        return self.garbage_collector.disable()

    def set_debug(self, flags):
        return self.garbage_collector.set_debug(flags)

    def is_enabled(self):
        return self.garbage_collector.is_enabled()

    def get_count(self):
        return self.garbage_collector.get_count()

    def get_console_extension_name(self):
        return self.console_garbage_collector.get_console_extension_name()

    def get_all_commands(self):
        return self.console_garbage_collector.get_all_commands()

    def get_handler_command(self, command):
        return self.console_garbage_collector.get_handler_command(command)

    def get_help(self):
        return self.console_garbage_collector.get_help()
