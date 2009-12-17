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

import sys

import wiki_video.wiki_video_extension_system

VIDEO_TYPE = "youtube"
""" The highlighting type """

BASE_ADDRESS = "http://www.youtube.com/v/"
""" The base address """

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

    capabilities = ["video"]
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
        pass

    def _get_video_id(self, url):
        #http://www.youtube.com/watch?v=67OYoGDha0U&feature=player_embedded
        watch_index = url.find("watch?")
        if not watch_index == -1:
            # splits the url
            url_splitted = url.split("?")

            # TENHO DE GENERALIZAR A EXTRACCAO DE ARGUMENTOS DE UM URL

            url_splitted = url_splitted.split("&")

        # retrieves the url splitted length
        url_splitted_length = len(url_splitted)

        if url_splitted_length == 4:
            if url_splitted[2] == "www.youtube.com":
                return BASE_ADDRESS + "?clip_id=7079800"
        elif url_splitted_length == 2:
            if url_splitted[0] == "www.youtube.com":
                return BASE_ADDRESS + "?clip_id=7079800"
