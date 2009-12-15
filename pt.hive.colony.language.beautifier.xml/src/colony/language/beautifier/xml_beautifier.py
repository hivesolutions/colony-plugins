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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

DOUBLE_TAG_REGEX_VALUE = "\<(?P<tag>[\w]+)([^\/]|\/[^\>])*?\>[^\0]*?\<\/(?P=tag)\>"
""" The double tag regex value """

DOUBLE_TAG_REGEX = re.compile(DOUBLE_TAG_REGEX_VALUE)
""" The double tag regex """

if __name__ == "__main__":
    # opens the xml file
    xml_file = open("xml_demo_file.xml")

    # reads the file contents
    xml_file_contents = xml_file.read()

    # closes the xml file
    xml_file.close()

    xml_file_contents = xml_file_contents.strip()

    # retrieves the xml file contents length
    xml_file_contents_length = len(xml_file_contents)

    current_index = 0

    # loop while the index is valid
    while current_index < xml_file_contents_length:
        # tries to match the xml file contents with the functions regex
        buffer_match = DOUBLE_TAG_REGEX.match(xml_file_contents, current_index)

        print buffer_match.group()

        # sets the new current index
        current_index = buffer_match.end()

# 1. vou sacando nos (do lexer)
# 2. quando me sai um no do tipos single deixo na mesma linha
# 3. quando me sai um no do tipo non single imprimo dou newline dou indentacao e depois dou novo newline e imprimo o fecho


# tenho de fazer uma re para uma tag
