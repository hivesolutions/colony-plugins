#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

ENCODING_NAME = "gzip"
""" The encoding name """


class ServiceHTTPGzip(colony.System):
    """
    The service HTTP gzip (encoding) class.
    """

    def get_encoding_name(self):
        return ENCODING_NAME

    def encode_contents(self, contents_string):
        # retrieves the gzip plugin
        gzip_plugin = self.plugin.gzip_plugin

        # encodes the contents string into gzip
        contents_string_encoded = gzip_plugin.gzip_contents(contents_string)

        # returns the contents string encoded
        return contents_string_encoded
