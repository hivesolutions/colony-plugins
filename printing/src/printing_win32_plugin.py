#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class PrintingWin32Plugin(colony.Plugin):
    """
    The main class for the Printing Win32 plugin.
    """

    id = "pt.hive.colony.plugins.printing.win32"
    name = "Printing Win32"
    description = "Printing Win32 Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "printing"
    ]
    dependencies = [
        colony.PackageDependency("Win32 Extensions for Python", "win32print"),
        colony.PackageDependency("Python Imaging Library (PIL)", "PIL")
    ]
    main_modules = [
        "printing_win32"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import printing_win32
        self.system = printing_win32.PrintingWin32(self)

    def get_printing_name(self):
        """
        Retrieves the printing name.

        @rtype: String
        @return: The printing name.
        """

        return self.system.get_printing_name()

    def print_test(self, printing_options):
        return self.system.print_test(printing_options)

    def print_test_image(self, image_path, printing_options):
        return self.system.print_test_image(image_path, printing_options)

    def print_printing_language(self, printing_document, printing_options):
        return self.system.print_printing_language(printing_document, printing_options)
