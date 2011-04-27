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

import language_wiki.libs.string_buffer_util

import language_wiki.wiki_extension_system

GENERATOR_TYPE = "console_input"
""" The generator type """

CONFIGURATION_MAP = {
    "generate_footer" : False,
    "simple_parse" : True
}
""" The configuration map """

class WikiConsoleInputExtension(language_wiki.wiki_extension_system.WikiExtension):
    """
    The wiki console input extension class.
    """

    id = "pt.hive.colony.language.wiki.extensions.console_input"
    """ The extension id """

    name = "Console Input Generation Plugin"
    """ The name of the extension """

    short_name = "Console Input Generation"
    """ The short name of the extension """

    description = "Extension for console input generation"
    """ The description of the extension """

    version = "1.0.0"
    """ The version of the extension """

    capabilities = ["generator"]
    """ The capabilities of the extension """

    capabilities_allowed = []
    """ The capabilities allowed by the extension """

    dependencies = []
    """ The dependencies of the extension """

    def get_generator_type(self):
        """
        Retrieves the generator type.

        @rtype: String
        @return: The generator type.
        """

        return GENERATOR_TYPE

    def generate_html(self, tag_node, visitor):
        """
        Generates the html code for the given tag node.

        @type tag_node: TagNode
        @param tag_node: The tag node to be processed.
        @type visitor: Visitor
        @param visitor: The requester visitor.
        @rtype: String
        @return: The generated html code.
        """

        # retrieves the tag contents
        contents = tag_node.contents

        # creates the string buffer
        string_buffer = language_wiki.libs.string_buffer_util.StringBuffer()

        # writes the start div console input tag
        string_buffer.write("<div class=\"console_input\">")

        # processes a new parse in the contents
        visitor.new_parse(contents, CONFIGURATION_MAP, string_buffer)

        # writes the end div console input tag
        string_buffer.write("</div>")

        # retrieves the string value
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value
