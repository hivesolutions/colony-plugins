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

__revision__ = "$LastChangedRevision: 14422 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-05-27 14:46:32 +0100 (Fri, 27 May 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys

import colony_console_window

UNIX_DIRECTORY_SEPARATOR = "/"
""" The unix directory separator """

BRANDING_TEXT = "Hive Colony %s (Hive Solutions Lda. r%s:%s %s)"
""" The branding text value """

VERSION_PRE_TEXT = "Python "
""" The version pre text value """

HELP_TEXT = "Type \"help\" for more information."
""" The help text value """

ICON_PATH = "misc_gui/colony_console_interface/resources/icons"
""" The colony console interface icon path """

class ColonyConsoleInterface:
    """
    The colony console interface class.
    """

    colony_console_interface_plugin = None
    """ The console interface plugin """

    def __init__(self, colony_console_interface_plugin):
        """
        Constructor of the class.

        @type colony_console_interface_plugin: ColonyConsoleInterfacePlugin
        @param colony_console_interface_plugin: The colony console interface plugin.
        """

        self.colony_console_interface_plugin = colony_console_interface_plugin

    def create_panel(self, parent):
        # generates the information
        information = self.generate_information()

        # creates the colony console window from the given intro message
        colony_console_panel = colony_console_window.ColonyConsoleWindow(parent, intro_message = information)

        # sets the display of line numbers in the console panel
        colony_console_panel.set_display_line_numbers(True)

        # sets the console plugin in the colony console panel
        colony_console_panel.set_console_plugin(self.colony_console_interface_plugin.console_plugin)

        # returns the control panel
        return colony_console_panel

    def get_icon_path(self):
        # retrieves the plugin manager
        colony_console_interface_plugin = self.colony_console_interface_plugin
        plugin_manager = colony_console_interface_plugin.manager

        # retrieves the console interface plugin id
        colony_console_interface_plugin_id = colony_console_interface_plugin.id

        # retrieves the plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(colony_console_interface_plugin_id)

        # defines the icon path
        icon_path = plugin_path + UNIX_DIRECTORY_SEPARATOR + ICON_PATH

        # returns the icon path
        return icon_path

    def generate_information(self):
        """
        Generates the system information to be used as into message.

        @rtype: String
        @return: The system information to be used as into message.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_console_interface_plugin.manager

        # retrieves the plugin manager version
        plugin_manager_version = plugin_manager.get_version()

        # retrieves the plugin manager release
        plugin_manager_release = plugin_manager.get_release()

        # retrieves the plugin manager build
        plugin_manager_build = plugin_manager.get_build()

        # retrieves the plugin manager release date
        plugin_manager_release_date = plugin_manager.get_release_date()

        # creates the information string
        information = str()

        # adds the branding information text
        information += BRANDING_TEXT % (plugin_manager_version, plugin_manager_release, plugin_manager_build, plugin_manager_release_date) + "\n"

        # adds the python information
        information += VERSION_PRE_TEXT + sys.version + "\n"

        # adds the help text
        information += HELP_TEXT

        # returns the information
        return information
