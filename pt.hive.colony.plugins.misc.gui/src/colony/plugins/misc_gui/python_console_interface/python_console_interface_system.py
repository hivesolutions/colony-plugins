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

__revision__ = "$LastChangedRevision: 14422 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-05-27 14:46:32 +0100 (Fri, 27 May 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import wx.py

UNIX_DIRECTORY_SEPARATOR = "/"
""" The unix directory separator """

ICON_PATH = "misc_gui/python_console_interface/resources/icons"
""" The icon path """

INTRO_MESSAGE = "Welcome to the python console"
""" The introduction message """

class PythonConsoleInterface:

    python_console_interface_plugin = None
    """ The python console interface plugin """

    def __init__(self, python_console_interface_plugin):
        """
        Constructor of the class.

        @type python_console_interface_plugin: PythonConsoleInterfacePlugin
        @param python_console_interface_plugin: The python console interface plugin.
        """

        self.python_console_interface_plugin = python_console_interface_plugin

    def create_panel(self, parent):
        # creates the shell panel
        shell_panel = wx.py.shell.Shell(parent, wx.ID_ANY, introText = INTRO_MESSAGE)

        # enables line numbers in the shell panel
        shell_panel.setDisplayLineNumbers(True)

        # returns the shell panel
        return shell_panel

    def get_icon_path(self):
        # retrieves the plugin manager
        python_console_interface_plugin = self.python_console_interface_plugin
        plugin_manager = python_console_interface_plugin.manager

        # retrieves the shell interface plugin id
        python_console_interface_plugin_id = python_console_interface_plugin.id

        # retrieves the plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(python_console_interface_plugin_id)

        # defines the icon path
        icon_path = plugin_path + UNIX_DIRECTORY_SEPARATOR + ICON_PATH

        # returns the icon path
        return icon_path
