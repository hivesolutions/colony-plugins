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

import language_wiki.libs.url_parser
import language_wiki.libs.string_buffer_util

import language_wiki.wiki_extension_system

import wiki_video.wiki_video_extension_system

GENERATOR_TYPE = "video"
""" The generator type """

DEFAULT_WIDTH = 445
""" The default width """

DEFAULT_HEIGHT = 364
""" The default width """

class WikiVideoExtension(language_wiki.wiki_extension_system.WikiExtension):
    """
    The wiki video extension class.
    """

    id = "pt.hive.colony.language.wiki.extensions.video"
    """ The extension id """

    name = "Video Generation Plugin"
    """ The name of the extension """

    short_name = "Video Generation"
    """ The short name of the extension """

    description = "Extension for video generation"
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

    url_parser = None
    """ The url parser """

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
        self.extension_manager = language_wiki.libs.extension_system.ExtensionManager([os.path.dirname(__file__) + "/wiki_video/extensions"])
        self.extension_manager.set_extension_class(wiki_video.wiki_video_extension_system.WikiVideoExtension)
        self.extension_manager.start_logger()
        self.extension_manager.load_system()

        # creates the url parser
        self.url_parser = language_wiki.libs.url_parser.UrlParser()

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

        # retrieves the tag attributes map
        attributes_map = tag_node.attributes_map

        # creates the string buffer
        string_buffer = language_wiki.libs.string_buffer_util.StringBuffer()

        # parses the url
        url = self.url_parser.parse_url(contents)

        # retrieves the video extensions
        video_extensions = self.extension_manager.get_extensions_by_capability("video")

        # writes the start div video tag
        string_buffer.write("<div class=\"video\">")

        # iterates over all the video extensions
        for video_extension in video_extensions:
            # retrieves the video url
            video_url = video_extension.get_video_url(url, attributes_map)

            # in case the video url is valid
            if video_url:
                # escapes the video url
                escaped_video_url = visitor.escape_string_value(video_url)

                # retrieves the width
                width = attributes_map.get("width", DEFAULT_WIDTH)

                # retrieves the height
                height = attributes_map.get("height", DEFAULT_HEIGHT)

                string_buffer.write("<object width=\"" + str(width) + "\" height=\"" + str(height) + "\">")
                string_buffer.write("<param name=\"allowFullScreen\" value=\"true\"></param>")
                string_buffer.write("<param name=\"allowscriptaccess\" value=\"always\"></param>")
                string_buffer.write("<param name=\"movie\" value=\"" + escaped_video_url + "\"></param>")
                string_buffer.write("<embed src=\"" + escaped_video_url + "\" type=\"application/x-shockwave-flash\" wmode=\"transparent\" allowscriptaccess=\"always\" allowfullscreen=\"true\" width=\"" + str(width) + "\" height=\"" + str(height) + "\"></embed>")
                string_buffer.write("</object>")

        # writes the end div video tag
        string_buffer.write("</div>")

        # retrieves the string value
        string_value = string_buffer.get_value()

        # returns the string value
        return string_value
