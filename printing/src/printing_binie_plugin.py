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

class PrintingBiniePlugin(colony.base.system.Plugin):
    """
    The main class for the Printing Binie plugin.
    """

    id = "pt.hive.colony.plugins.printing.binie"
    name = "Printing Binie"
    description = "Printing Binie Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "printing"
    ]
    dependencies = [
        colony.PackageDependency("Python Imaging Library (PIL)", "PIL")
    ]
    main_modules = [
        "printing.binie.exceptions",
        "printing.binie.system",
        "printing.binie.visitor"
    ]

    printing_binie = None
    """ The printing binie """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import printing.binie.system
        self.printing_binie = printing.binie.system.PrintingBinie(self)

    def get_printing_name(self):
        """
        Retrieves the printing name.

        @rtype: String
        @return: The printing name.
        """

        return self.printing_binie.get_printing_name()

    def print_test(self, printing_options):
        return self.printing_binie.print_test(printing_options)

    def print_test_image(self, image_path, printing_options):
        return self.printing_binie.print_test_image(image_path, printing_options)

    def print_printing_language(self, printing_document, printing_options):
        return self.printing_binie.print_printing_language(printing_document, printing_options)
