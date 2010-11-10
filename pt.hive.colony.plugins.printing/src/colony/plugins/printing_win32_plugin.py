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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class PrintingWin32Plugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Printing Win32 plugin.
    """

    id = "pt.hive.colony.plugins.printing.win32"
    name = "Printing Win32 Plugin"
    short_name = "Printing Win32"
    description = "Printing Win32 Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/printing/win32/resources/baf.xml"}
    capabilities = ["printing", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PackageDependency(
                    "Win32 Extensions for Python", "win32print", "b202", "http://starship.python.net/crew/mhammond/win32"),
                    colony.base.plugin_system.PackageDependency(
                    "Python Imaging Library (PIL)", "PIL", "1.1.x", "http://www.pythonware.com/products/pil")]
    events_handled = []
    events_registrable = []
    main_modules = ["printing.win32.printing_win32_constants",
                    "printing.win32.printing_win32_exceptions",
                    "printing.win32.printing_win32_system",
                    "printing.win32.printing_win32_visitor"]

    printing_win32 = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global printing
        import printing.win32.printing_win32_system
        self.printing_win32 = printing.win32.printing_win32_system.PrintingWin32(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_printing_name(self):
        """
        Retrieves the printing name.

        @rtype: String
        @return: The printing name.
        """

        return self.printing_win32.get_printing_name()

    def print_test(self, printing_options):
        self.printing_win32.print_test(printing_options)

    def print_test_image(self, image_path, printing_options):
        self.printing_win32.print_test_image(image_path, printing_options)

    def print_printing_language(self, printing_document, printing_options):
        self.printing_win32.print_printing_language(printing_document, printing_options)
