#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

from . import serializer

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

MIME_TYPE = "application/json"
""" The mime type """

class Json(colony.System):
    """
    Provides functions to interact with json.
    """

    def dumps(self, object):
        return serializer.dumps(object)

    def dumps_pretty(self, object):
        return serializer.dumps_pretty(object)

    def dumps_buffer(self, object):
        return serializer.dumps_buffer(object)

    def loads(self, json_string):
        return serializer.loads(json_string)

    def load_file(self, json_file, encoding = DEFAULT_ENCODING):
        # reads the json file
        json_file_contents = json_file.read()

        # decodes the json file contents using the default encoder
        json_file_contents_decoded = json_file_contents.decode(encoding)

        # loads the json file contents
        return self.loads(json_file_contents_decoded)

    def get_mime_type(self):
        return MIME_TYPE
