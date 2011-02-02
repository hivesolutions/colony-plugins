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

__revision__ = "$LastChangedRevision: 12930 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-02-01 13:59:19 +0000 (ter, 01 Fev 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "system_installer"
""" The console extension name """

class ConsoleSystemInstaller:
    """
    The console system installer class.
    """

    system_installer_plugin = None
    """ The system installer plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, system_installer_plugin):
        """
        Constructor of the class.

        @type system_installer_plugin: SystemInstallerPlugin
        @param system_installer_plugin: The system installer plugin.
        """

        self.system_installer_plugin = system_installer_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
                    }

        # returns the commands map
        return commands_map
