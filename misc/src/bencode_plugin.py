#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class BencodePlugin(colony.Plugin):
    """
    The main class for the Bencode plugin.
    """

    id = "pt.hive.colony.plugins.misc.bencode"
    name = "Bencode"
    description = "A plugin to serialize and unserialize bencode files"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "serializer.bencode"
    ]
    main_modules = [
        "bencode_c.exceptions",
        "bencode_c.serializer",
        "bencode_c.system"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import bencode_c
        self.system = bencode_c.Bencode(self)

    def dumps(self, object):
        return self.system.dumps(object)

    def loads(self, bencode_string):
        return self.system.loads(bencode_string)

    def load_file(self, bencode_file):
        return self.system.load_file(bencode_file)

    def load_file_encoding(self, bencode_file, encoding):
        return self.system.load_file(bencode_file, encoding)

    def get_mime_type(self):
        return self.system.get_mime_type()
