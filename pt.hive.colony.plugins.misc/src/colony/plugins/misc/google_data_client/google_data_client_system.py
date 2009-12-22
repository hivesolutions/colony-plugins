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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import gdata.docs.service
import gdata.youtube.service

class GoogleDataClient:
    """
    The google data client class.
    """

    google_data_client_plugin = None
    """ The google data client plugin """

    youtube_service = None
    """ The youtube service """

    docs_service = None
    """ The docs service """

    def __init__(self, google_data_client_plugin):
        """
        Constructor of the class.

        @type google_data_client_plugin: GoogleDataClientPlugin
        @param google_data_client_plugin: The google data client plugin.
        """

        self.google_data_client_plugin = google_data_client_plugin

    def connect(self, username, password):
        """
        Connects to the available services.

        @type username: String
        @param username: The username for the connection.
        @type password: String
        @param password: The password for the connection.
        """

        self.connect_youtube(username, password)
        self.connect_google_docs(username, password)

    def connect_youtube(self, username, password):
        # creates a youtube service
        self.youtube_service = gdata.youtube.service.YouTubeService()

    def connect_google_docs(self, username, password):
        # creates a docs service
        self.docs_service = gdata.docs.service.DocsService()

        # authenticates the docs service
        self.docs_service.ClientLogin(username, password)

    def google_docs_get_document_list(self):
        # retrieves the document titles
        documents_feed = self.docs_service.GetDocumentListFeed()

        # collects the document titles
        document_title_list = [document_entry.title.text for document_entry in documents_feed.entry]

        return document_title_list

    def youtube_get_entry(self, id):
        # returns the specified youtube entry
        return self.youtube_service.GetYouTubeVideoEntry(video_id = id)

    def youtube_get_video_title(self, id):
        # retrieves the specified youtube entry
        entry = self.youtube_get_entry(id)

        # returns the youtube entry's title
        return entry.media.title.text

    def youtube_get_video_publish_date(self, id):
        # retrieves the specified youtube entry
        entry = self.youtube_get_entry(id)

        # returns the youtube entry's publish date
        return entry.published.text

    def youtube_get_video_description(self, id):
        # retrieves the specified youtube entry
        entry = self.youtube_get_entry(id)

        # returns the youtube entry's description
        return entry.media.description.text

    def youtube_get_video_category(self, id):
        # retrieves the specified youtube entry
        entry = self.youtube_get_entry(id)

        # returns the youtube entry's category
        return entry.media.category[0].text

    def youtube_get_video_tags(self, id):
        # retrieves the specified youtube entry
        entry = self.youtube_get_entry(id)

        # returns the youtube entry's tags
        return entry.media.keywords.text

    def youtube_get_video_watch_page(self, id):
        # retrieves the specified youtube entry
        entry = self.youtube_get_entry(id)

        # returns the youtube entry's watch page url
        return entry.media.player.url

    def youtube_get_video_duration(self, id):
        # retrieves the specified youtube entry
        entry = self.youtube_get_entry(id)

        # returns the youtube entry's video duration
        return entry.media.duration.seconds

    def youtube_get_video_view_count(self, id):
        # retrieves the specified youtube entry
        entry = self.youtube_get_entry(id)

        # returns the youtube entry's view count
        return entry.statistics.view_count

    def youtube_get_video_rating(self, id):
        # retrieves the specified youtube entry
        entry = self.youtube_get_entry(id)

        # returns the youtube entry's average rating
        return entry.rating.average

    def youtube_get_video_thumbnail_url(self, id):
        # retrieves the specified youtube entry
        entry = self.youtube_get_entry(id)

        # collects the youtube entry's thumbnails
        thumbnails = [thumbnail for thumbnail in entry.media.thumbnail]

        return thumbnails
