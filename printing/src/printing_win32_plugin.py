#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

class PrintingWin32Plugin(colony.base.system.Plugin):
    """
    The main class for the Printing Win32 plugin.
    """

    id = "pt.hive.colony.plugins.printing.win32"
    name = "Printing Win32"
    description = "Printing Win32 Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "printing"
    ]
    dependencies = [
        colony.PackageDependency("Win32 Extensions for Python", "win32print"),
        colony.PackageDependency("Python Imaging Library (PIL)", "PIL")
    ]
    main_modules = [
        "printing.win32.constants",
        "printing.win32.exceptions",
        "printing.win32.system",
        "printing.win32.visitor"
    ]

    printing_win32 = None
    """ The printing win32 """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import printing.win32.system
        self.printing_win32 = printing.win32.system.PrintingWin32(self)

    def get_printing_name(self):
        """
        Retrieves the printing name.

        @rtype: String
        @return: The printing name.
        """

        return self.printing_win32.get_printing_name()

    def print_test(self, printing_options):
        return self.printing_win32.print_test(printing_options)

    def print_test_image(self, image_path, printing_options):
        return self.printing_win32.print_test_image(image_path, printing_options)

    def print_printing_language(self, printing_document, printing_options):
        return self.printing_win32.print_printing_language(printing_document, printing_options)
