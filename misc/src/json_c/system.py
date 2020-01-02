#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from . import serializer

DEFAULT_ENCODING = "utf-8"
""" The default encoding to be used for the JSON based operations,
should be the most permissive possible (avoiding issues) """

MIME_TYPE = "application/json"
""" The mime type for the JSON structure, this value should
be changed according to the standard values """

FAST_LOADS = True
""" Flag that controls if by default the strategy for the loading
operation should try to use the embedded loader (faster) """

class JSON(colony.System):
    """
    Provides functions to interact with JSON, this class should
    implement (and conform) with the generic serialization methods.
    """

    def dumps(self, object):
        return serializer.dumps(object)

    def dumps_lazy(self, object):
        return serializer.dumps_lazy(object)

    def dumps_pretty(self, object):
        return serializer.dumps_pretty(object)

    def dumps_buffer(self, object):
        return serializer.dumps_buffer(object)

    def loads(self, json_string, fast = FAST_LOADS):
        if fast: return serializer.loads_f(json_string)
        return serializer.loads(json_string)

    def load_file(self, json_file, encoding = DEFAULT_ENCODING):
        # reads the JSON file
        json_file_contents = json_file.read()

        # decodes the JSON file contents using the default encoder
        json_file_contents_decoded = json_file_contents.decode(encoding)

        # loads the JSON file contents
        return self.loads(json_file_contents_decoded)

    def get_mime_type(self):
        return MIME_TYPE
