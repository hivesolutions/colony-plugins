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

import sys

import console_window

BRANDING_TEXT = "Hive Colony %s (Hive Solutions Lda. r%s:%s)"
""" The branding text value """

VERSION_PRE_TEXT = "Python "
""" The version pre text value """

HELP_TEXT = "Type \"help\" for more information."
""" The help text value """

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
        # generates the information
        information = self.generate_information()

        # creates the console window from the given intro message
        console_panel = console_window.ConsoleWindow(parent, intro_message = information)

        # sets the display of line numbers in the console panel
        console_panel.set_display_line_numbers(True)

        # sets the console plugin in the console panel
        console_panel.set_console_plugin(self.console_interface_plugin.console_plugin)

        # returns the control panel
        return console_panel

    def generate_information(self):
        """
        Generates the system information to be used as into message.

        @rtype: String
        @return: The system information to be used as into message.
        """

        # retrieves the plugin manager
        plugin_manager = self.console_interface_plugin.manager

        # retrieves the plugin manager version
        plugin_manager_version = plugin_manager.get_version()

        # retrieves the plugin manager release
        plugin_manager_release = plugin_manager.get_release()

        # retrieves the plugin manager release date
        plugin_manager_release_date = plugin_manager.get_release_date()

        # creates the information string
        information = str()

        # adds the branding information text
        information += BRANDING_TEXT % (plugin_manager_version, plugin_manager_release, plugin_manager_release_date) + "\n"

        # adds the python information
        information += VERSION_PRE_TEXT + sys.version + "\n"

        # adds the help text
        information += HELP_TEXT

        # returns the information
        return information
