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

import colony.base.plugin_system

class MainConsoleFileSystemPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Console File System Main plugin.
    """

    id = "pt.hive.colony.plugins.main.console.file_system"
    name = "Console File System Main Plugin"
    short_name = "Console File System Main"
    description = "The plugin that provides the file system commands for the system"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "_console_command_extension",
        "build_automation_item"
    ]
    main_modules = [
        "main_console.file_system.main_console_file_system_system"
    ]

    console_file_system = None
    """ The console file system """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_console.file_system.main_console_file_system_system
        self.console_file_system = main_console.file_system.main_console_file_system_system.MainConsoleFileSystem(self)

    def get_console_extension_name(self):
        return self.console_file_system.get_console_extension_name()

    def get_commands_map(self):
        return self.console_file_system.get_commands_map()