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

import os
import types

import language_wiki.libs.string_buffer_util
import language_wiki.libs.extension_system

import language_wiki.wiki_exceptions
import language_wiki.wiki_extension_system

import wiki_code.wiki_code_extension_system

GENERATOR_TYPE = "code"
""" The generator type """

class WikiCodeExtension(language_wiki.wiki_extension_system.WikiExtension):
    """
    The wiki code extension class.
    """

    id = "pt.hive.colony.language.wiki.extensions.code"
    """ The extension id """

    name = "Code Generation Plugin"
    """ The name of the extension """

    short_name = "Code Generation"
    """ The short name of the extension """

    description = "Extension for code highlighting generation"
    """ The description of the extension """

    version = "1.0.0"
    """ The version of the extension """

    capabilities = [
        "generator"
    ]
    """ The capabilities of the extension """

    capabilities_allowed = []
    """ The capabilities allowed by the extension """

    dependencies = []
    """ The dependencies of the extension """

    extension_manager = None
    """ The extension manager """

    def __init__(self, manager = None, logger = None):
        """
        Constructor of the class.

        @type manager: ExtensionManager
        @param manager: The parent extension manager.
        @type logger: Logger
        @param logger: The extension manager logger.
        """

        language_wiki.wiki_extension_system.WikiExtension.__init__(self, manager, logger)

        # creates a new extension manager
        self.extension_manager = language_wiki.libs.extension_system.ExtensionManager([os.path.dirname(__file__) + "/wiki_code/extensions"])
        self.extension_manager.set_extension_class(wiki_code.wiki_code_extension_system.WikiCodeExtension)
        self.extension_manager.start_logger()
        self.extension_manager.load_system()

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

        # retrieves the code highlighting extensions
        code_highlighting_extensions = self.extension_manager.get_extensions_by_capability("code_highlighting")

        # retrieves the tag name
        node_tag_name = tag_node.tag_name

        # retrieves the tag attributes map
        node_attributes_map = tag_node.attributes_map

        # retrieves the tag attributes map keys
        node_attributes_map_keys = node_attributes_map.keys()

        # in case the number of keys in the tag attributes map
        # is less than one
        if node_attributes_map_keys < 1:
            # raisers the invalid tag name exception
            raise language_wiki.wiki_exceptions.InvalidTagName("tag name is not valid: " + node_tag_name)

        # retrieves the node tag language value
        node_tag_language_value = node_attributes_map_keys[0]

        # retrieves the code highlighting extensions for the given tag
        tag_code_highlighting_extensions = [extension for extension in code_highlighting_extensions if extension.get_highlighting_type() == node_tag_language_value]

        # in case there are no highlighting extension for the given tag
        if not tag_code_highlighting_extensions:
            # writes the start div code tag
            string_buffer.write("<div class=\"code\">")

            # writes the start code tag
            string_buffer.write("<code>")

            # escapes the contents
            contents_replaced = visitor.escape_string_value(contents)

            # writes the replaced contents
            string_buffer.write(contents_replaced)

            # writes the end code tag
            string_buffer.write("</code>")

            # writes the end div code tag
            string_buffer.write("</div>")

        # iterates over all the tag code highlighting extensions
        for tag_code_highlighting_extension in tag_code_highlighting_extensions:
            # retrieves the tokens list
            tokens_list = tag_code_highlighting_extension.get_tokens_list(contents)

            # writes the start div code tag
            string_buffer.write("<div class=\"code\">")

            # writes the start code tag
            string_buffer.write("<code>")

            # sets the initial current position
            current_position = 0

            # sets the initial current line
            current_line = 1

            # iterates over the tokens list
            for token in tokens_list:
                # unpacks the token tuple
                _token_type, token_value, token_position, token_end_position, token_line, token_class = token

                # retrieves the line delta value
                line_delta = token_line - current_line

                # retrieves the position delta
                position_delta = token_position - current_position

                # in case the line delta is bigger than zero
                if line_delta > 0:
                    for _index in range(line_delta):
                        string_buffer.write("<br />")

                for _index in range(position_delta):
                    string_buffer.write("&nbsp;")

                # sets the current position
                current_position = token_end_position

                # sets the current line
                current_line = token_line

                # in case the type of the token value is string
                if type(token_value) == types.StringType:
                    # escapes the token value
                    token_value = visitor.escape_string_value(token_value)

                # in case the token class is defined
                if token_class:
                    string_buffer.write("<span class=\"" + token_class + "\">")
                    string_buffer.write(str(token_value))
                    string_buffer.write("</span>")
                else:
                    string_buffer.write(str(token_value))

            # writes the end code tag
            string_buffer.write("</code>")

            # writes the end div code tag
            string_buffer.write("</div>")

        # retrieves the string value
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value
