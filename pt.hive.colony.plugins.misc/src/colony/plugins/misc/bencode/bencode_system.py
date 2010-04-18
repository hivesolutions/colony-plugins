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

__author__ = "Jo�o Magalh�es <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import bencode_serializer

class Bencode:
    """
    Provides functions to interact with bencode.
    """

    bencode_plugin = None
    """ The bencode plugin """

    def __init__(self, bencode_plugin):
        """
        Constructor of the class.

        @type bencode_plugin: BencodePlugin
        @param bencode_plugin: The bencode plugin.
        """

        self.bencode_plugin = bencode_plugin

    def dumps(self, object):
        return bencode_serializer.dumps(object)

    def loads(self, bencode_string):
        return bencode_serializer.loads(bencode_string)

    def load_file(self, bencode_file):
        # reads the bencode file
        bencode_file_contents = bencode_file.read()

        # loads the bencode file contents
        return self.loads(bencode_file_contents)
