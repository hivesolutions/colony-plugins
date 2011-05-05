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

import downloader_exceptions

VALID_STATUS_CODES = (
    200,
)
""" The valid status codes """

class Downloader:
    """
    The downloader class.
    """

    downloader_plugin = None
    """ The downloader plugin """

    def __init__(self, downloader_plugin):
        """
        Constructor of the class.

        @type downloader_plugin: DownloaderPlugin
        @param downloader_plugin: The downloader plugin.
        """

        self.downloader_plugin = downloader_plugin

    def download_package(self, address, target_directory = None):
        """
        Downloads a package from the given url address to a target directory.

        @type address: String
        @param address: The url address of the package to download.
        @type target_directory: String
        @param target_directory: The target directory of the download.
        """

        try:
            # sets the target directory
            target_directory = target_directory or self._get_default_target_directory()

            # retrieves the main client http plugin
            main_client_http_plugin = self.downloader_plugin.main_client_http_plugin

            # retrieves the file name from the url path
            file_name = self.get_file_name_url(address)

            # creates the http client
            http_client = main_client_http_plugin.create_client({})

            # opens the http client
            http_client.open({})

            try:
                # fetches the url retrieving the http response
                http_response = http_client.fetch_url(address)

                # retrieves the status code from the http response
                status_code = http_response.status_code

                # in case the status code is not valid
                if not status_code in VALID_STATUS_CODES:
                    # retrieves the status message from the http response
                    status_message = http_response.status_message

                    # raises the invalid status code exception
                    raise downloader_exceptions.InvalidStatusCodeException("%i - %s" % (status_code, status_message))

                # retrieves the file contents from the http response
                file_contents = http_response.received_message
            finally:
                # closes the http client
                http_client.close({})

            # in case there is no directory
            if not os.path.isdir(target_directory):
                # creates the directory and intermediate directories
                os.makedirs(target_directory)

            # opens a new file and creates it if necessary
            file = open(target_directory + "/" + file_name, "wb")

            try:
                # writes the contents to the file
                file.write(file_contents)
            finally:
                # closes the file
                file.close()
        except Exception, exception:
            self.downloader_plugin.error("Problem while downloading file: " + address + ", error: " + unicode(exception))

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
            # retrieves the main client http plugin
            main_client_http_plugin = self.downloader_plugin.main_client_http_plugin

            # creates the http client
            http_client = main_client_http_plugin.create_client({})

            # opens the http client
            http_client.open({})

            try:
                # fetches the url retrieving the http response
                http_response = http_client.fetch_url(address)

                # retrieves the status code from the http response
                status_code = http_response.status_code

                # in case the status code is not valid
                if not status_code in VALID_STATUS_CODES:
                    # retrieves the status message from the http response
                    status_message = http_response.status_message

                    # raises the invalid status code exception
                    raise downloader_exceptions.InvalidStatusCodeException("%i - %s" % (status_code, status_message))

                # retrieves the file contents from the http response
                file_contents = http_response.received_message
            finally:
                # closes the http client
                http_client.close({})

            # returns the file contents
            return file_contents
        except Exception, exception:
            self.downloader_plugin.error("Problem while downloading file: " + address + ", error: " + unicode(exception))

    def get_file_name_url(self, url):
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

    def _get_default_target_directory(self):
        """
        Retrieves the default target directory.
        The default target directory is the configuration
        path of the downloader plugin

        @rtype: String
        @return: The default target directory.
        """

        # retrieves the plugin manager
        plugin_manager = self.downloader_plugin.manager

        # retrieves the configuration path for the downloader plugin
        configuration_path, _workspace_path = plugin_manager.get_plugin_configuration_paths_by_id(self.downloader_plugin.id)

        # sets the target path as the configuration path
        target_path = configuration_path

        # returns the target path
        return target_path
