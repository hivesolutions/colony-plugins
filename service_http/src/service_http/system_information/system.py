#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

import colony.base.system
import colony.libs.time_util
import colony.libs.structures_util

HANDLER_NAME = "system_information"
""" The handler name """

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

DEFAULT_TEMPLATE_ENCODING = "utf-8"
""" The default template encoding """

HTML_MIME_TYPE = "text/html"
""" The html mime type """

SYSTEM_INFORMATION_RESOURCES_PATH = "service_http/system_information/resources"
""" The system information resources path """

SYSTEM_INFORMATION_HTML_TEMPLATE_FILE_NAME = "system_information.html.tpl"
""" The system information html template file name """

class ServiceHttpSystemInformation(colony.base.system.System):
    """
    The service http system information (handler) class.
    """

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        """

        # sets the request content type
        request.content_type = HTML_MIME_TYPE

        # sets the request status code
        request.status_code = 200

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the template engine plugin
        template_engine_plugin = self.plugin.template_engine_plugin

        # retrieves the plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(self.plugin.id)

        # creates the template file path
        template_file_path = plugin_path +\
            "/" + SYSTEM_INFORMATION_RESOURCES_PATH + "/" + SYSTEM_INFORMATION_HTML_TEMPLATE_FILE_NAME

        # parses the template file path
        template_file = template_engine_plugin.parse_file_path_encoding(template_file_path, DEFAULT_TEMPLATE_ENCODING)

        # retrieves the system information
        system_information = self._get_system_information()

        # retrieves the plugin manager version
        plugin_manager_version = plugin_manager.get_version()

        # retrieves the plugin manager release
        plugin_manager_release = plugin_manager.get_release()

        # assigns the template variables
        template_file.assign("plugin_manager_version", plugin_manager_version)
        template_file.assign("plugin_manager_release", plugin_manager_release)
        template_file.assign("system_information", system_information)

        # processes the template file
        processed_template_file = template_file.process()

        # encodes the processed template file using the default encoding
        processed_template_file_encoded = processed_template_file.encode(DEFAULT_ENCODING)

        # writes the processed template file encoded to the request
        request.write(processed_template_file_encoded)

        # returns true (valid)
        return True

    def _get_system_information(self):
        """
        Retrieves the system information map.

        @rtype: Dictionary
        @return: The system information map.
        """

        # retrieves the system information plugins
        system_information_plugins = self.plugin.system_information_plugins

        # creates the map to hold the system information (ordered  map)
        system_information = colony.libs.structures_util.OrderedMap()

        # retrieves the framework information
        framework_information = self._get_framework_information()

        # defines the framework main item columns
        framework_main_item_columns = [
            {
                "type" : "name",
                "value" : "Name"
            },
            {
                "type" : "value",
                "value" : "Value"
            }
        ]

        # creates the framework main item
        framework_main_item = {}

        # sets the framework main item values
        framework_main_item["type"] = "map"
        framework_main_item["columns"] = framework_main_item_columns
        framework_main_item["values"] = framework_information

        # creates the framework copyright item
        framework_copyright_item = {}

        # sets the framework copyright item values
        framework_copyright_item["type"] = "simple"
        framework_copyright_item["columns"] = []
        framework_copyright_item["value"] = "This program makes use of the Hive Colony Framework, Copyright (c) 2010-2012 Hive Solutions Lda."

        # creates the system information framework item
        system_information_framework_item = {}

        # sets the system information framework item values
        system_information_framework_item["name"] = "Framework"
        system_information_framework_item["items"] = [
            framework_main_item,
            framework_copyright_item
        ]

        # sets the system information framework item in the system information
        system_information["framework"] = system_information_framework_item

        # iterates over all the system information plugins
        for system_information_plugin in system_information_plugins:
            # retrieves the system information from the system information
            # plugin (the map containing the information)
            _system_information = system_information_plugin.get_system_information()

            # sets the system information in the system information map
            system_information[system_information_plugin.id] = _system_information

        # returns the system information
        return system_information

    def _get_framework_information(self):
        """
        Retrieves an information map containing information
        about the framework.

        @rtype: Dictionary
        @return: An information map containing information
        about the framework.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the plugin amnager uid
        plugin_manager_uid = plugin_manager.uid

        # retrieves the plugin manager version
        plugin_manager_version = plugin_manager.get_version()

        # retrieves the plugin manager release
        plugin_manager_release = plugin_manager.get_release()

        # retrieves the plugin manager build
        plugin_manager_build = plugin_manager.get_build()

        # retrieves the plugin manager release date time
        plugin_manager_release_date_time = plugin_manager.get_release_date_time()

        # retrieves the plugin manager layout mode
        plugin_manager_layout_mode = plugin_manager.get_layout_mode()

        # retrieves the plugin manager run mode
        plugin_manager_run_mode = plugin_manager.get_run_mode()

        # retrieves the plugin manager environment
        plugin_manager_environment = plugin_manager.get_environment()

        # retrieves the current time
        current_time = time.time()

        # retrieves the plugin manager timestamp
        plugin_manager_timestamp = plugin_manager.plugin_manager_timestamp

        # calculates the uptime
        uptime = current_time - plugin_manager_timestamp

        # creates the uptime string
        uptime_string = colony.libs.time_util.format_seconds_smart(uptime, "basic", ("day", "hour", "minute", "second"))

        # retrieves the plugin manager instances
        plugin_manager_instances = plugin_manager.plugin_instances

        # retrieves the plugin strings from the plugin manager instances
        plugins_string, replicas_string, instances_string = self._get_plugin_strings(plugin_manager_instances)

        # creates the framework information map
        framework_information = colony.libs.structures_util.OrderedMap()

        # sets the framework information (map) values
        framework_information["uid"] = plugin_manager_uid
        framework_information["version"] = plugin_manager_version
        framework_information["release"] = plugin_manager_release
        framework_information["build"] = plugin_manager_build
        framework_information["release date"] = plugin_manager_release_date_time
        framework_information["environment"] = plugin_manager_environment
        framework_information["layout mode"] = plugin_manager_layout_mode
        framework_information["run mode"] = plugin_manager_run_mode
        framework_information["uptime"] = uptime_string
        framework_information["plugins"] = plugins_string
        framework_information["replicas"] = replicas_string
        framework_information["instances"] = instances_string

        # returns the framework information (map)
        return framework_information

    def _get_plugin_strings(self, plugin_manager_instances):
        """
        Constructs the various plugin strings from the
        given plugin manager instances.

        @type plugin_manager_instances: List
        @param plugin_manager_instances: The list of plugin manager instances.
        @rtype: Tuple
        @return: A tuple containing the plugin strings.
        """

        # creates the plugin counters
        plugins_loaded = 0
        plugins_total = 0
        replicas_loaded = 0
        replicas_total = 0
        instances_loaded = 0
        instances_total = 0

        # iterates over all the plugin manager instances to
        # construct the plugin values
        for plugin_manager_instance in plugin_manager_instances:
            # in case it is a replica
            if plugin_manager_instance.is_replica():
                # in case the plugin manager instance is loaded
                if plugin_manager_instance.is_loaded():
                    # increments the replicas loaded
                    replicas_loaded += 1

                # increments the replicas total
                replicas_total += 1
            else:
                # in case the plugin manager instance is loaded
                if plugin_manager_instance.is_loaded():
                    # increments the plugins loaded
                    plugins_loaded += 1

                # increments the plugins total
                plugins_total += 1

            # in case the plugin manager instance is loaded
            if plugin_manager_instance.is_loaded():
                # increments the instances loaded
                instances_loaded += 1

            # increments the instances total
            instances_total += 1

        # creates the plugins string
        plugins_string = str(plugins_loaded) + "/" + str(plugins_total)

        # creates the replicas string
        replicas_string = str(replicas_loaded) + "/" + str(replicas_total)

        # creates the instances string
        instances_string = str(instances_loaded) + "/" + str(instances_total)

        # creates the plugins tuple from the plugins string, the replicas
        # string and the instances string
        plugins_tuple = (
            plugins_string,
            replicas_string,
            instances_string
        )

        # returns the plugins tuple
        return plugins_tuple
