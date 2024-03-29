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


class YadisHTMLParser(colony.legacy.HTMLParser.HTMLParser):
    """
    The Yadis HTML parser, used to retrieve the Yadis
    provider URL from the HTML code.
    """

    yadis_provider_url = None
    """ The Yadis provider URL """

    def handle_starttag(self, tag, attributes):
        """
        Handles the parsing of the start of a tag.

        :type tag: String
        :param tag: The value of the start of a tag.
        :type attributes: List
        :param attributes: The list of attribute pairs of the tag.
        """

        # in case the tag is of type meta
        if tag == "meta":
            # converts the attribute pairs into a map
            attributes_map = dict(attributes)

            # checks if the HTTP equiv reference exists
            # and is valid
            if attributes_map.get("http-equiv", None).lower() == "x-xrds-location":
                # sets the Yadis provider URL
                self.yadis_provider_url = attributes_map.get("content", None)
