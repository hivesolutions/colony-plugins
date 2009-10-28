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

import json_serializer

DEFAULT_ENCODER = "utf-8"
""" The default encoder """

class Json:
    """
    Provides functions to interact with json.
    """

    json_plugin = None
    """ The json plugin """

    def __init__(self, json_plugin):
        """
        Class constructor.

        @type json_plugin: JsonPlugin
        @param json_plugin: The json plugin.
        """

        self.json_plugin = json_plugin

    def dumps(self, json_string):
        return json_serializer.dumps(json_string)

    def loads(self, json_string):
        return json_serializer.loads(json_string)

    def load_file(self, json_file):
        # reads the json file
        json_file_contents = json_file.read()

        # decodes the json file contents using the default encoder
        json_file_contents_encoded = json_file_contents.decode(DEFAULT_ENCODER)

        # loads the json file contents
        return self.loads(json_file_contents_encoded)
