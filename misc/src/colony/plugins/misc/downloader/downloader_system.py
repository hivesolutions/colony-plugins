#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 18128 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-11-23 14:28:54 +0000 (Wed, 23 Nov 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import time

import colony.libs.size_util
import colony.libs.observer_util

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

    def download_package(self, address, target_directory = None, handlers_map = {}):
        """
        Downloads a package from the given url address to a target directory.

        @type address: String
        @param address: The url address of the package to download.
        @type target_directory: String
        @param target_directory: The target directory of the download.
        @type handlers_map: Dictionary
        @param handlers_map: The map of handlers for the execution events.
        """

        try:
            # retrieves the current time for the initial time
            initial_time = time.time()

            # sets the target directory
            target_directory = target_directory or self._get_default_target_directory()

            # retrieves the main client http plugin
            main_client_http_plugin = self.downloader_plugin.main_client_http_plugin

            # notifies the handlers about the message
            colony.libs.observer_util.message(handlers_map, "Get %s" % address)

            # creates a new set of handlers map (for http client) for
            # the current context
            _handlers_map = self._create_handlers_map(handlers_map)

            # retrieves the file name from the url path
            file_name = self.get_file_name_url(address)

            # creates the http client
            http_client = main_client_http_plugin.create_client({})

            # opens the http client
            http_client.open({})

            try:
                # fetches the url retrieving the http response
                http_response = http_client.fetch_url(address, handlers_map = _handlers_map)

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

            # creates the file path by joining the target directory (path)
            # and the file name
            target_path = os.path.join(target_directory, file_name)

            # opens a new file and creates it if necessary
            file = open(target_path, "wb")

            try:
                # writes the contents to the file
                file.write(file_contents)
            finally:
                # closes the file
                file.close()

            # retrieves the current time for the final time
            # and calculates the delta time
            final_time = time.time()
            delta_time = final_time - initial_time

            # calculates the file contents length and then
            # uses it to calculate the speed of the download
            # measured in bytes
            file_contents_length = len(file_contents)
            speed = int(float(file_contents_length) / delta_time)

            # converts the speed value into a size string (speed string)
            # for simpler scale values
            speed_string = colony.libs.size_util.size_round_unit(speed, space = True)

            # notifies the handlers about the message
            colony.libs.observer_util.message(handlers_map, "Saved data as %s [%s/s]. " % (file_name, speed_string))

        except Exception, exception:
            # prints an info message
            self.downloader_plugin.info("Problem while downloading file: " + address + ", error: " + unicode(exception))

    def get_download_package_stream(self, address, handlers_map = {}):
        """
        Retrieves the download package stream for the given address.

        @type address: String
        @param address: The address of the download package to retrieve the stream.
        @type handlers_map: Dictionary
        @param handlers_map: The map of handlers for the execution events.
        @rtype: String
        @return: The download package stream for the given address.
        """

        try:
            # retrieves the main client http plugin
            main_client_http_plugin = self.downloader_plugin.main_client_http_plugin

            # creates a new set of handlers map (for http client) for
            # the current context
            _handlers_map = self._create_handlers_map(handlers_map)

            # creates the http client
            http_client = main_client_http_plugin.create_client({})

            # opens the http client
            http_client.open({})

            try:
                # fetches the url retrieving the http response
                http_response = http_client.fetch_url(address, handlers_map = _handlers_map)

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

    def _create_handlers_map(self, handlers_map):
        # creates the context map to be used to store
        # context information on the current execution
        context = {
            "message_length" : 0,
            "current_count" : 0
        }

        def headers_handler(response):
            # retrieves the various information from
            # the response object to be used as diagnostics
            # information in the observer object
            status_code = response.status_code
            status_message = response.status_message
            content_length = response.headers_map.get("Content-Length") or 0
            content_type = response.headers_map.get("Content-Type") or "N/A"
            content_length_integer = int(content_length)
            content_length_string = colony.libs.size_util.size_round_unit(content_length_integer, space = True)

            # prints a series of message to the observer object
            colony.libs.observer_util.message(handlers_map, "Request sent, awaiting response... %d %s" % (status_code, status_message))
            colony.libs.observer_util.message(handlers_map, "Received headers [%s] [%s]" % (content_length_string, content_type))
            colony.libs.observer_util.message(handlers_map, "Receiving data... ")

            # updates the message length in the current context
            context["message_length"] = content_length_integer

        def message_data_handler(response, data):
            # retrieves the received data length
            data_length = len(data)

            # retrieves the current context information from the
            # the context map
            message_length = context["message_length"]
            current_count = context.get("current_count", 0)
            current_count += data_length
            context["current_count"] = current_count

            # notifies the handlers about the progress change
            colony.libs.observer_util.progress(handlers_map, int(float(current_count) / float(message_length) * 100))

        # creates the map containing the handlers to be used in the download
        _handlers_map = {
            "message_data" : message_data_handler,
            "headers" : headers_handler
        }

        # returns the (generated) handlers map
        return _handlers_map
