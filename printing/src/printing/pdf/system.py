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

import visitor

PRINTING_NAME = "pdf"
""" The printing name """

class PrintingPdf(colony.base.system.System):
    """
    The printing pdf class.
    """

    def get_printing_name(self):
        """
        Retrieves the printing name.

        @rtype: String
        @return: The printing name.
        """

        return PRINTING_NAME

    def print_test(self, printing_options = {}):
        pass

    def print_test_image(self, image_path, printing_options = {}):
        pass

    def print_printing_language(self, printing_document, printing_options = {}):
        # creates the pdf printing visitor
        _visitor = visitor.Visitor()

        # sets the printing options in the visitor
        _visitor.set_printing_options(printing_options)

        # accepts the visitor in the printing document,
        # using double visiting mode
        printing_document.accept_double(_visitor)
