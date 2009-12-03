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

import wiki_parser
import wiki_visitor
import wiki_html_generation

# opens the wiki file
wiki_file = open("test.wiki")

# reads the wiki file contents
wiki_file_contents = wiki_file.read()

# closes the wiki file
wiki_file.close()

# parses the javascript file retrieving the result
parse_result = wiki_parser.parser.parse(wiki_file_contents)

visitor = wiki_visitor.Visitor()

generation_visitor = wiki_html_generation.HtmlGenerationVisitor()

parse_result.accept(visitor)
parse_result.accept_double(generation_visitor)

html_value = generation_visitor.get_string_buffer().getvalue()

# opens the html file
html_file = open("test.html", "w+")

html_file.write(html_value)

html_file.close()
