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

__revision__ = "$LastChangedRevision: 5731 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-10-21 19:04:42 +0100 (qua, 21 Out 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import csv_serializer

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

class Csv:
    """
    Provides functions to interact with csv.
    """

    csv_plugin = None
    """ The csv plugin """

    def __init__(self, csv_plugin):
        """
        Constructor of the class.

        @type csv_plugin: CsvPlugin
        @param csv_plugin: The csv plugin.
        """

        self.csv_plugin = csv_plugin

    def dumps(self, object):
        return csv_serializer.dumps(object)

    def loads(self, csv_string):
        return csv_serializer.loads(csv_string)

    def load_file(self, csv_file, encoding = DEFAULT_ENCODING):
        # reads the csv file
        csv_file_contents = csv_file.read()

        # decodes the csv file contents using the default encoder
        csv_file_contents_decoded = csv_file_contents.decode(encoding)

        # loads the csv file contents
        return self.loads(csv_file_contents_decoded)
