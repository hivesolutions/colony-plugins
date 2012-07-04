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

class ConsoleFileSystemPlugin(colony.base.system.Plugin):
    """
    The main class for the Console File System plugin.
    """

    id = "pt.hive.colony.plugins.console.file_system"
    name = "Console File System"
    description = "The plugin that provides the file system commands for the system"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT,
        colony.base.system.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "_console_command_extension"
    ]
    main_modules = [
        "console.file_system.system"
    ]

    console_file_system = None
    """ The console file system """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import console.file_system.system
        self.console_file_system = console.file_system.system.ConsoleFileSystem(self)

    def get_console_extension_name(self):
        return self.console_file_system.get_console_extension_name()

    def get_commands_map(self):
        return self.console_file_system.get_commands_map()
