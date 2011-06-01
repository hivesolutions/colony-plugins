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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.structures_util

import web_mvc_wiki_exceptions

WEB_MVC_WIKI_RESOURCES_PATH = "web_mvc_wiki/mvc_wiki/resources"
""" The web mvc wiki resources path """

EXTRAS_PATH = WEB_MVC_WIKI_RESOURCES_PATH + "/extras"
""" The extras path """

class WebMvcWiki:
    """
    The web mvc wiki class.
    """

    web_mvc_wiki_plugin = None
    """ The web mvc wiki plugin """

    instances_map = {}
    """ The map of instances reference """

    def __init__(self, web_mvc_wiki_plugin):
        """
        Constructor of the class.

        @type web_mvc_wiki_plugin: WebMvcWikiPlugin
        @param web_mvc_wiki_plugin: The web mvc wiki plugin.
        """

        self.web_mvc_wiki_plugin = web_mvc_wiki_plugin

        self.instances_map = {}

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_wiki_plugin.web_mvc_utils_plugin

        # creates the controllers for the web mvc wiki controllers module
        web_mvc_utils_plugin.create_controllers("web_mvc_wiki.mvc_wiki.web_mvc_wiki_controllers", self, self.web_mvc_wiki_plugin, "web_mvc_wiki")

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the web mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return (
            (r"^wiki/(?P<instance_name>[a-zA-Z]+)/pages$", self.web_mvc_wiki_page_controller.handle_create, "post"),
            (r"^wiki/(?P<instance_name>[a-zA-Z]+)/pages/(?P<page_name>[a-zA-Z0-9_:\.]+)/update$", self.web_mvc_wiki_page_controller.handle_update_json, "post", "json"),
            (r"^wiki/(?P<instance_name>[a-zA-Z]+)/(?P<page_name>[a-zA-Z0-9_:\.]*)$", self.web_mvc_wiki_main_controller.handle_wiki, "get"),
            (r"^wiki/(?P<instance_name>[a-zA-Z]+)/(?:(?P<resource_type>js|images|css))/(?P<resource_name>.*)$", self.web_mvc_wiki_main_controller.handle_resources, "get")
        )

    def get_communication_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as communication patterns,
        to the web mvc service. The tuple should relate the route with a tuple
        containing the data handler, the connection changed handler and the name
        of the connection.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as communication patterns,
        to the web mvc service.
        """

        return ()

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the web mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_wiki_plugin.manager

        # retrieves the web mvc wiki plugin path
        web_mvc_wiki_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_wiki_plugin.id)

        return (
            (r"^wiki/resources/.+$", (web_mvc_wiki_plugin_path + "/" + EXTRAS_PATH, "wiki/resources")),
        )

    def get_system_information(self):
        """
        Retrieves the system information map, containing structured
        information to be visible using presentation viewers.

        @rtype: Dictionary
        @return: The system information map.
        """

        # creates the map to hold the system information (ordered  map)
        web_mvc_wiki_information = colony.libs.structures_util.OrderedMap()

        # iterates over all the instances to creates the information
        for instance_name, instance_value in self.instances_map.items():
            # retrieves the instance values
            instance_repository_path = instance_value["repository_path"]
            instance_repository_type = instance_value["repository_type"]

            # sets the instance value for the web mvc wiki information
            web_mvc_wiki_information[instance_name] = (
                instance_repository_path,
                instance_repository_type
            )

        # defines the web mvc wiki main item columns
        web_mvc_wiki_main_item_columns = [
            {
                "type" : "name",
                "value" : "Instance"
            },
            {
                "type" : "value",
                "value" : "Path"
            },
            {
                "type" : "value",
                "value" : "Repository Type"
            }
        ]

        # creates the web mvc wiki main item
        web_mvc_wiki_main_item = {}

        # sets the web mvc wiki main item values
        web_mvc_wiki_main_item["type"] = "map"
        web_mvc_wiki_main_item["columns"] = web_mvc_wiki_main_item_columns
        web_mvc_wiki_main_item["values"] = web_mvc_wiki_information

        # creates the system information (item)
        system_information = {}

        # sets the system information (item) values
        system_information["name"] = "Web Mvc Wiki"
        system_information["items"] = [
            web_mvc_wiki_main_item
        ]

        # returns the system information
        return system_information

    def set_configuration_property(self, configuration_propery):
        # retrieves the configuration
        configuration = configuration_propery.get_data()

        # retrieves the instances map
        instances_map = configuration["instances"]

        # sets the instances map
        self.instances_map = instances_map

    def unset_configuration_property(self):
        # sets the instances map
        self.instances_map = {}

    def _get_instance(self, instance_name):
        """
        Retrieves the current instance for the
        given instance name.

        @type instance_name: String
        @param instance_name: The instance name to retrieve.
        """

        # in case the instance name does not exist
        # in the instances map
        if not instance_name in self.instances_map:
            # raises the instance not found exception
            raise web_mvc_wiki_exceptions.InstanceNotFound(instance_name)

        # retrieves the instance from the instance name
        instance = self.instances_map[instance_name]

        # returns the instance
        return instance
