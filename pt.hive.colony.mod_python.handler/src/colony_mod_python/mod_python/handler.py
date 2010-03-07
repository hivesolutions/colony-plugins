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

import sys
import types
import datetime

import mod_python.apache

CONTAINER_NAME = "apache"
""" The container name """

MOD_PYTHON_PLUGIN_ID = "pt.hive.colony.plugins.main.mod_python"
""" The mod python plugin id """

DEFAULT_CONTENT_ENCODING = "utf-8"
""" The default content encoding """

ETAG_VALUE = "ETag"
""" The etag value """

EXPIRES_VALUE = "Expires"
""" The expires value """

LAST_MODIFIED_VALUE = "Last-Modified"
""" The last modified value """

IF_MODIFIED_SINCE_VALUE = "If-Modified-Since"
""" The if modified since value """

IF_NONE_MATCH_VALUE = "If-None-Match"
""" The if none match value """

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
""" The date format """

plugin_manager = None
""" The plugin manager """

class PluginManagerHandler:
    """
    The plugin manager handler class for the mod_python.
    """

    req = None
    """ The http request sent by the mod_python """

    local_address = None
    """ The local address for the request """

    local_port = None
    """ The local port for the request """

    _old_write = None
    """ The old write method """

    def __init__(self, req):
        """
        Constructor of the class.

        @type req: HttpRequest
        @param req: The http request sent by the mod_python.
        """

        self.req = req
        self.local_address, self.local_port = req.connection.local_addr

        # processes the request
        self._process_request(req)

        # changes the write method
        self._old_write = req.write
        req.write = self._write

        # puts the extra methods in the request
        req.get_header = self._get_header
        req.set_etag = self._set_etag
        req.set_expiration_timestamp = self._set_expiration_timestamp
        req.set_last_modified_timestamp = self._set_last_modified_timestamp
        req.verify_resource_modification = self._verify_resource_modification

    def handle_request(self, data):
        """
        Handles the requested data.

        @type data: String
        @param data: The data to handle.
        """

        # creates the plugin handler id object
        plugin_handler_id = None

        # retrieves the mod python options
        python_options = self.req.get_options()

        # retrieves the plugin manager
        manager = self.get_plugin_manager(python_options)

        # retrieves the mod_python plugin
        mod_python_plugin = manager.get_plugin_by_id(MOD_PYTHON_PLUGIN_ID)

        # retrieves the plugin handler id for the current request
        if "PluginHandlerEnv" in python_options:
            plugin_handler_id = python_options["PluginHandlerEnv"]

        # sends the request to the mod_python to handle it
        mod_python_plugin.handle_request(self.req, plugin_handler_id)

        # in case the status code attribute is set
        if hasattr(self.req, "status_code"):
            # sets the request status
            self.req.status = self.req.status_code

        # returns true
        return True

    def get_plugin_manager(self, python_options = {}):
        """
        Retrieves the plugin manager with the given python options.

        @type python_options: List
        @param python_options: The list of python options to the (possible) startup of the plugin manager.
        """

        # in case the plugin manager is not loaded
        if not plugin_manager:
            # loads the plugin manager
            self.load_plugin_manager(python_options)

        return plugin_manager

    def load_plugin_manager(self, python_options):
        """
        Loads the plugin manager with the given python options.

        @type python_options: List
        @param python_options: The list of python options to the startup of the plugin manager.
        """

        # sets the plugin_manager as a global variable
        global plugin_manager

        # tests the python options to retrieve the plugin manager path
        if not "PluginManagerEnv" in python_options:
            return True

        # retrieves the plugin manager path from the python options
        plugin_manager_path = python_options["PluginManagerEnv"]

        # inserts the plugin path into the default python path
        sys.path.insert(0, plugin_manager_path)

        # imports the main module
        import main

        # sets the command line arguments
        sys.argv.append("--debug")
        sys.argv.append("--noloop")
        sys.argv.append("--container=" + CONTAINER_NAME)
        sys.argv.append("--attributes=apache_address:" + self.local_address + ",apache_port:" + str(self.local_port))
        sys.argv.append("--manager_dir=" + plugin_manager_path)

        # starts the plugin manager
        main.main()

        # retrieves the plugin manager, setting the variable
        plugin_manager = main.plugin_manager

    def _get_header(self, header_name):
        """
        Retrieves the header attribute for the given
        header name.

        @type header_name: String
        @param header_name: The name of the header to retrieve.
        @rtype: Object
        @return: The header value for the given header name.
        """

        return self.req.headers_out.get(header_name, None)

    def _set_etag(self, etag_value):
        """
        Sets the etag value in the request.

        @type etag_value: String
        @param etag_value: The value to be set in the request.
        """

        # sets the etag value in the header
        self.req.headers_out[ETAG_VALUE] = etag_value

    def _set_expiration_timestamp(self, expiration_timestamp):
        """
        Sets the expiration timestamp value in the request.

        @type expiration_timestamp: int
        @param expiration_timestamp: The expiration timestamp
        to be set in the request.
        """

        # converts the expiration timestamp to date time
        expiration_date_time = datetime.datetime.fromtimestamp(expiration_timestamp)

        # formats the expiration date time according to the http specification
        expiration_date_time_formatted = expiration_date_time.strftime(DATE_FORMAT)

        # sets the expiration date time formatted in the header
        self.req.headers_out[EXPIRES_VALUE] = expiration_date_time_formatted

    def _set_last_modified_timestamp(self, last_modified_timestamp):
        """
        Sets the last modified timestamp value in the request.

        @type last_modified_timestamp: int
        @param last_modified_timestamp: The last modified timestamp
        to be set in the request.
        """

        # converts the last modified timestamp to date time
        last_modified_date_time = datetime.datetime.fromtimestamp(last_modified_timestamp)

        # formats the last modified date time according to the http specification
        last_modified_date_time_formatted = last_modified_date_time.strftime(DATE_FORMAT)

        # sets the last modified date time formatted in the header
        self.req.headers_out[LAST_MODIFIED_VALUE] = last_modified_date_time_formatted

    def _verify_resource_modification(self, modified_timestamp = None, etag_value = None):
        """
        Verifies the resource to check for any modification since the
        value defined in the http request.

        @type modified_timestamp: int
        @param modified_timestamp: The timestamp of the resource modification.
        @type etag_value: String
        @param etag_value: The etag value of the resource.
        @rtype: bool
        @return: The result of the resource modification test.
        """

        # retrieves the if modified header value
        if_modified_header = self.req.get_header(IF_MODIFIED_SINCE_VALUE)

        # in case the modified timestamp and if modified header are defined
        if modified_timestamp and if_modified_header:
            # converts the if modified header value to date time
            if_modified_header_data_time = datetime.datetime.strptime(if_modified_header, DATE_FORMAT)

            # converts the modified timestamp to date time
            modified_date_time = datetime.datetime.fromtimestamp(modified_timestamp)

            # in case the modified date time is less or the same
            # as the if modified header date time (no modification)
            if modified_date_time <= if_modified_header_data_time:
                # returns false (not modified)
                return False

        # retrieves the if none match value
        if_none_match_header = self.req.get_header(IF_NONE_MATCH_VALUE)

        # in case the etag value and the if none header are defined
        if etag_value and if_none_match_header:
            # in case the value of the if modified header is the same
            # as the etag value of the file (no modification)
            if if_modified_header == etag_value:
                # returns false (not modified)
                return False

        # returns false (modified or no information for
        # modification test)
        return True

    def _write(self, message):
        """
        The request write wrapper to allow encoding.

        @type message: String
        @param message: The message to be written in the buffer.
        """

        # retrieves the message type
        message_type = type(message)

        # in case the message type is unicode
        if message_type == types.UnicodeType:
            # checks the request content encoding
            if self.req.content_encoding:
                # sets the content encoding defined in the request
                content_encoding = self.req.content_encoding
            else:
                # sets the content encoding as the default one
                content_encoding = DEFAULT_CONTENT_ENCODING

            # encodes the message with the defined content type charset
            message = message.encode(content_encoding)

        # calls the old write method
        self._old_write(message)

    def _process_request(self, req):
        """
        Processes the request object.

        @type req: HttpRequest
        @param req: The http request sent by the mod_python.
        """

        # creates the attributes map in the request
        req.attributes_map = {}

        # retrieves the arguments from the path splitted
        arguments = req.args

        # in case the arguments are not defined
        if not arguments:
            # returns immediately
            return

        # retrieves the attribute fields list
        attribute_fields_list = arguments.split("&")

        # iterates over all the attribute fields
        for attribute_field in attribute_fields_list:
            # splits the attribute field in the equals operator
            attribute_field_splitted = attribute_field.split("=")

            # retrieves the attribute field splitted length
            attribute_field_splitted_length = len(attribute_field_splitted)

            # in case the attribute field splitted length is invalid
            if attribute_field_splitted_length == 0 or attribute_field_splitted_length > 2:
                continue

            # in case the attribute field splitted length is two
            if attribute_field_splitted_length == 2:
                # retrieves the attribute name and the attribute value,
                # from the attribute field splitted
                attribute_name, attribute_value = attribute_field_splitted
            # in case the attribute field splitted length is one
            elif attribute_field_splitted_length == 1:
                # retrieves the attribute name, from the attribute field splitted
                attribute_name, = attribute_field_splitted

                # sets the attribute value to none
                attribute_value = None

            # sets the attribute value
            req.attributes_map[attribute_name] = attribute_value

def handler(req):
    """
    The initial handler function for the mod_python.

    @type req: HttpRequest
    @param req: The http request sent by the mod_python.
    @rtype: int
    @return: The status for the request.
    """

    # in case the handling was successful
    if PluginManagerHandler(req).handle_request(req):
        return mod_python.apache.OK
    # in case the handling was unsuccessful
    else:
        return mod_python.apache.DECLINED
