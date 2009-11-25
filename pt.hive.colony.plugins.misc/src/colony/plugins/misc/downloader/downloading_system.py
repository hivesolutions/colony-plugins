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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import urllib2

PLUGIN_DIRECTORY = "colony/plugins"
""" The plugin directory """

class Downloader:
    """
    The downloader class.
    """

    downloader_plugin = None
    """ The downloader plugin """

    def __init__(self, downloader_plugin):
        """
        Class constructor.

        @type downloader_plugin: DownloaderPlugin
        @param downloader_plugin: The downloader plugin.
        """

        self.downloader_plugin = downloader_plugin

    def download_package(self, address, target_directory = PLUGIN_DIRECTORY):
        """
        Downloads a package from the given url address to a target directory.

        @type address: String
        @param address: The url address of the package to download.
        @type target_directory: String
        @param target_directory: The target directory of the download.
        @rtype: bool
        @return: The result of the download (if successful or not).
        """

        try:
            # retrieves the file name from the url path
            file_name = self.get_file_name_url(address)

            # opens the url
            url = urllib2.urlopen(address)

            # reads the contents from the url
            file_contents = url.read()

            # in case there is no directory
            if not os.path.isdir(target_directory):
                # creates the directory and intermediate directories
                os.makedirs(target_directory)

            # opens a new file and creates it if necessary
            file = open(target_directory + "/" + file_name, "wb")

            # writes the contents to the file
            file.write(file_contents)

            # closes the file
            file.close()
            return True
        except urllib2.HTTPError, error:
            self.downloader_plugin.error("Error downloading file: " + address + ", server error: " + str(error.code))
            return False
        except urllib2.URLError, error:
            self.downloader_plugin.error("Error downloading file: " + address + ", server not available")
            return False

    def test_package(self, address):
        """
        Tests the package in the given address.

        @type address: String
        @param address: The address of the package to be tested.
        @rtype bool
        @return: The result of the test (if successful or not).
        """

        pass

    def get_download_package_stream(self, address):
        """
        Retrieves the download package stream for the given address.

        @type address: String
        @param address: The address of the download package to retrieve the stream.
        @rtype: String
        @return: The download package stream for the given address.
        """

        try:
            # retrieves the file name from the address
            file_name = self.get_file_name_url(address)

            # opens the address retrieving the url
            url = urllib2.urlopen(address)

            # reads the package contents from the url
            file_contents = url.read()

            # returns the file contents
            return file_contents
        except urllib2.HTTPError, error:
            self.downloader_plugin.error("Error downloading file: " + address + ", server error: " + str(error.code))
        except urllib2.URLError, error:
            self.downloader_plugin.error("Error downloading file: " + address + ", server not available")

    def get_file_name_url(url):
        """
        Retrieves the file name for the given url.

        @type url: String
        @param url: The url to retrieve the file name.
        @rtype: String
        @return: The file name for the given url.
        """

        # splits the url
        url_split = url.split("/")

        # in case the last group is empty
        if url_split[-1] == "":
            return url_split[-2]
        else:
            return url_split[-1]
