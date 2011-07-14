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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import wx.py

UNIX_DIRECTORY_SEPARATOR = "/"
""" The unix directory separator """

ICON_PATH = "misc_gui/shell_interface/resources/icons"
""" The icon path """

INTRO_MESSAGE = "Welcome to the plugin system shell"
""" The introduction message """

class ShellInterface:

    shell_interface_plugin = None
    """ The shell interface plugin """

    def __init__(self, shell_interface_plugin):
        """
        Constructor of the class.

        @type shell_interface_plugin: ShellInterfacePlugin
        @param shell_interface_plugin: The shell interface plugin.
        """

        self.shell_interface_plugin = shell_interface_plugin

    def create_panel(self, parent):
        # creates the shell panel
        shell_panel = wx.py.shell.Shell(parent, wx.ID_ANY, introText = INTRO_MESSAGE)

        # enables line numbers in the shell panel
        shell_panel.setDisplayLineNumbers(True)

        # returns the shell panel
        return shell_panel

    def get_icon_path(self):
        # retrieves the plugin manager
        shell_interface_plugin = self.shell_interface_plugin
        plugin_manager = shell_interface_plugin.manager

        # retrieves the shell interface plugin id
        shell_interface_plugin_id = shell_interface_plugin.id

        # retrieves the plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(shell_interface_plugin_id)

        # defines the shell icon path
        shell_icon_path = plugin_path + UNIX_DIRECTORY_SEPARATOR + ICON_PATH

        # returns the shell icon path
        return shell_icon_path
