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


class URLParserPlugin(colony.Plugin):
    """
    The main class for the URL Parser plugin.
    """

    id = "pt.hive.colony.plugins.misc.url_parser"
    name = "URL Parser"
    description = "A plugin to parse URL for agile interpretation"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT]
    capabilities = ["url_parse"]
    main_modules = ["url_parser_c"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import url_parser_c

        self.system = url_parser_c.URLParser(self)

    def parse_url(self, url):
        """
        Parses the given URL retrieving the URL object.

        :type url: String
        :param url:  The URL to be parsed.
        :rtype: URL
        :return: The URL object representing the URL.
        """

        return self.system.parse_url(url)
