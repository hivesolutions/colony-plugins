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

import colony.plugins.plugin_system

class GoogleDataClientPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Google Data Client plugin.
    """

    id = "pt.hive.colony.plugins.misc.google_data_client"
    name = "Google Data Client Plugin"
    short_name = "Google Data Client"
    description = "Google Data Client Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["google_data_client", "console_command_extension"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PackageDependency(
                    "Google Data API Python Client Library", ["gdata", "gdata.docs", "gdata.youtube"], "1.1.x", "http://code.google.com/p/gdata-python-client")]
    events_handled = []
    events_registrable = []

    google_data_client = None
    console_google_data_client = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.google_data_client.google_data_client_system
        import misc.google_data_client.console_google_data_client
        self.google_data_client = misc.google_data_client.google_data_client_system.GoogleDataClient(self)
        self.console_google_data_client = misc.google_data_client.console_google_data_client.ConsoleGoogleDataClient(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def connect(self, username, password):
        """
        Connects to the available services.

        @type username: String
        @param username: The username for the connection.
        @type password: String
        @param password: The password for the connection.
        """

        self.google_data_client.connect()

    def youtube_get_video_title(self, id):
        return self.google_data_client.youtube_get_video_title(id)

    def youtube_get_video_publish_date(self, id):
        return self.google_data_client.youtube_get_video_publish_date(id)

    def youtube_get_video_description(self, id):
        return self.google_data_client.youtube_get_video_description(id)

    def youtube_get_video_category(self, id):
        return self.google_data_client.youtube_get_video_category(id)

    def youtube_get_video_tags(self, id):
        return self.google_data_client.youtube_get_video_tags(id)

    def youtube_get_video_watch_page(self, id):
        return self.google_data_client.youtube_get_video_watch_page(id)

    def youtube_get_video_duration(self, id):
        return self.google_data_client.youtube_get_video_duration(id)

    def youtube_get_video_view_count(self, id):
        return self.google_data_client.youtube_get_video_view_count(id)

    def youtube_get_video_rating(self, id):
        return self.google_data_client.youtube_get_video_rating(id)

    def youtube_get_video_thumbnail_url(self, id):
        return self.google_data_client.youtube_get_video_thumbnail_url(id)

    def get_console_extension_name(self):
        return self.console_google_data_client.get_console_extension_name()

    def get_all_commands(self):
        return self.console_google_data_client.get_all_commands()

    def get_handler_command(self, command):
        return self.console_google_data_client.get_handler_command(command)

    def get_help(self):
        return self.console_google_data_client.get_help()
