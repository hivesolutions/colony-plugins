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

import language_wiki.libs.url_parser

import wiki_video.wiki_video_extension_system

VIDEO_TYPE = "youtube"
""" The highlighting type """

BASE_ADDRESS = "http://www.youtube.com/v"
""" The base address """

VALID_DOMAIN_NAMES = (
    "www.youtube.com",
    "youtube.com"
)
""" The valid domain names """

VALID_OPTIONS_LIST = (
    "hl",
    "hd",
    "fs",
    "rel",
    "border",
    "showinfo",
    "color1",
    "color2"
)
""" The valid options list """

class YoutubeVideoExtension(wiki_video.wiki_video_extension_system.WikiVideoExtension):
    """
    The youtube video extension class.
    """

    id = "pt.hive.colony.language.wiki.video.extensions.youtube_video"
    """ The extension id """

    name = "Youtube Video Plugin"
    """ The name of the extension """

    short_name = "Youtube Video"
    """ The short name of the extension """

    description = "Extension for youtube video"
    """ The description of the extension """

    version = "1.0.0"
    """ The version of the extension """

    capabilities = [
        "video"
    ]
    """ The capabilities of the extension """

    capabilities_allowed = []
    """ The capabilities allowed by the extension """

    dependencies = []
    """ The dependencies of the extension """

    def get_video_type(self):
        """
        Retrieves the video type.

        @rtype: String
        @return: The video type.
        """

        return VIDEO_TYPE

    def get_video_url(self, url, options):
        """
        Retrieves the video url for the given url structure,
        and options.

        @type url: Url
        @param url: The base url.
        @type options: Dictionary
        @param options: The map with the options.
        @rtype: String
        @return: The video url for the given url structure, and options.
        """

        # in case the url is not valid
        if not self._validate_url(url):
            # returns immediately
            return

        # retrieves the video id
        video_id = self._get_video_id(url)

        # creates a new url
        url = language_wiki.libs.url_parser.Url()

        # parses the base address
        url.parse_url(BASE_ADDRESS)

        # adds the video id option to the url
        url.add_resource_reference_item(video_id)

        # iterates over all the valid options
        for valid_option in VALID_OPTIONS_LIST:
            # in case the valid option exists in the options
            if valid_option in options:
                # retrieves the valid option value
                valid_option_value = options[valid_option]

                # adds the option to the url
                url.add_option(valid_option, valid_option_value)

        # builds the url
        http_url = url.build_url()

        # returns the url
        return http_url

    def _get_video_id(self, url):
        """
        Retrieves the video id for the given url.

        @type url: Url
        @param url: The url to retrieve the video id.
        @rtype: int
        @return: The video id for the given url.
        """

        # retrieves the url options map
        url_options_map = url.get_options_map()

        # retrieves the url resource reference list map
        resource_reference_list = url.get_resource_reference_list()

        # retrieves the video id from the option or from the resource reference
        video_id = url_options_map.get("v", resource_reference_list[-1])

        # returns the video id
        return video_id

    def _validate_url(self, url):
        """
        Validates the given url.

        @type url: Url
        @param url: The url to be validated.
        @rtype: bool
        @return: The result of the validation.
        """

        # retrieves the url base name
        url_base_name = url.get_base_name()

        # in case the url base name is valid
        if url_base_name in VALID_DOMAIN_NAMES:
            # returns true
            return True

        # returns false
        return False
