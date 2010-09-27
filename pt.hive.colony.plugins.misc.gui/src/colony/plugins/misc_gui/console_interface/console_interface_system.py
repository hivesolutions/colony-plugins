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

import console_window

INTRO_MESSAGE = "Welcome to the plugin system console"
""" The intro message to be printed at the beginning of the console """

class ConsoleInterface:
    """
    The console interface class.
    """

    console_interface_plugin = None
    """ The console interface plugin """

    def __init__(self, console_interface_plugin):
        """
        Constructor of the class.

        @type console_interface_plugin: ConsoleInterfacePlugin
        @param console_interface_plugin: The console interface plugin.
        """

        self.console_interface_plugin = console_interface_plugin

    def do_panel(self, parent):
        # creates the console window from the given intro message
        console_panel = console_window.ConsoleWindow(parent, intro_message = INTRO_MESSAGE)

        # sets the display of line numbers in the console panel
        console_panel.set_display_line_numbers(True)

        # sets the console plugin in the console panel
        console_panel.set_console_plugin(self.console_interface_plugin.console_plugin)

        # returns the control panel
        return console_panel
