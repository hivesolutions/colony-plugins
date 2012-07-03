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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

ENCODING_NAME = "gzip"
""" The encoding name """

class MainServiceHttpGzipEncoding:
    """
    The main service http gzip encoding class.
    """

    main_service_http_gzip_encoding_plugin = None
    """ The main service http gzip encoding plugin """

    def __init__(self, main_service_http_gzip_encoding_plugin):
        """
        Constructor of the class.

        @type main_service_http_gzip_encoding_plugin: MainServiceHttpGzipEncodingPlugin
        @param main_service_http_gzip_encoding_plugin: The main service http gzip encoding plugin.
        """

        self.main_service_http_gzip_encoding_plugin = main_service_http_gzip_encoding_plugin

    def get_encoding_name(self):
        return ENCODING_NAME

    def encode_contents(self, contents_string):
        # retrieves the gzip plugin
        gzip_plugin = self.main_service_http_gzip_encoding_plugin.gzip_plugin

        # encodes the contents string into gzip
        contents_string_encoded = gzip_plugin.gzip_contents(contents_string)

        # returns the contents string encoded
        return contents_string_encoded
