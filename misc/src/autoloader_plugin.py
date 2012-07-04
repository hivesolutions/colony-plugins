#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system

class AutoloaderPlugin(colony.base.system.Plugin):
    """
    The main class for the Autoloader plugin.
    """

    id = "pt.hive.colony.plugins.misc.autoloader"
    name = "Autoloader"
    description = "Autoloader Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT
    ]
    capabilities = [
        "main",
        "autoload",
        "console_command_extension"
    ]
    main_modules = [
        "misc.autoloader.system",
        "misc.autoloader.console"
    ]

    autoloader = None
    """ The autoloader """

    console_autoloader = None
    """ The console autoloader """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import misc.autoloader.system
        import misc.autoloader.console
        self.autoloader = misc.autoloader.system.Autoloader(self)
        self.console_autoloader = misc.autoloader.console.ConsoleAutoloader(self)
        self.autoloader.load_autoloader()

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)
        self.release_ready_semaphore()

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)
        self.autoloader.unload_autoloader()
        self.release_ready_semaphore()

    def end_unload_plugin(self):
        colony.base.system.Plugin.end_unload_plugin(self)
        self.release_ready_semaphore()

    def get_console_extension_name(self):
        return self.console_autoloader.get_console_extension_name()

    def get_all_commands(self):
        return self.console_autoloader.get_all_commands()

    def get_handler_command(self, command):
        return self.console_autoloader.get_handler_command(command)

    def get_help(self):
        return self.console_autoloader.get_help()
