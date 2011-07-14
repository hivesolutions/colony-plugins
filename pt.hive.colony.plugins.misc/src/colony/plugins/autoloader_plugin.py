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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class AutoloaderPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Autoloader plugin.
    """

    id = "pt.hive.colony.plugins.misc.autoloader"
    name = "Autoloader Plugin"
    short_name = "Autoloader"
    description = "Autoloader Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/misc/autoloader/resources/baf.xml"
    }
    capabilities = [
        "main",
        "autoload",
        "console_command_extension",
        "build_automation_item"
    ]
    main_modules = [
        "misc.autoloader.autoloader_system",
        "misc.autoloader.console_autoloader"
    ]

    autoloader = None
    """ The autoloader """

    console_autoloader = None
    """ The console autoloader """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import misc.autoloader.autoloader_system
        import misc.autoloader.console_autoloader
        self.autoloader = misc.autoloader.autoloader_system.Autoloader(self)
        self.console_autoloader = misc.autoloader.console_autoloader.ConsoleAutoloader(self)
        self.autoloader.load_autoloader()

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)
        self.autoloader.unload_autoloader()

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_console_extension_name(self):
        return self.console_autoloader.get_console_extension_name()

    def get_all_commands(self):
        return self.console_autoloader.get_all_commands()

    def get_handler_command(self, command):
        return self.console_autoloader.get_handler_command(command)

    def get_help(self):
        return self.console_autoloader.get_help()
