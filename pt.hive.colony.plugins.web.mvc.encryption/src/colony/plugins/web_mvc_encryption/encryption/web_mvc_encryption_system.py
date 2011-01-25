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

import os

import colony.libs.map_util

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_ENCRYPTION_RESOURCES_PATH = "web_mvc_encryption/encryption/resources"
""" The web mvc encryption resources path """

TEMPLATES_PATH = WEB_MVC_ENCRYPTION_RESOURCES_PATH + "/templates"
""" The templates path """

EXTRAS_PATH = WEB_MVC_ENCRYPTION_RESOURCES_PATH + "/extras"
""" The extras path """

ENTITY_MANAGER_ARGUMENTS = {"engine" : "sqlite",
                            "connection_parameters" : {"autocommit" : False}}
""" The entity manager arguments """

CONNECTION_PARAMETERS_VALUE = "connection_parameters"
""" The connection parameters value """

FILE_PATH_VALUE = "file_path"
""" The file path value """

DEFAULT_DATABASE_SUFFIX = "database.db"
""" The default database suffix """

DEFAULT_DATABASE_PREFIX = "web_mvc_encryption_"
""" The default database prefix """

class WebMvcEncryption:
    """
    The web mvc encryption class.
    """

    web_mvc_encryption_plugin = None
    """ The web mvc encryption plugin """

    web_mvc_encryption_main_controller = None
    """ The web mvc encryption main controller """

    web_mvc_encryption_consumer_controller = None
    """ The web mvc encryption consumer controller """

    web_mvc_encryption_entity_models = None
    """ the web mvc encryption entity models """

    keys_map = {}
    """ The map of keys """

    security_map = {}
    """ The map of security """

    def __init__(self, web_mvc_encryption_plugin):
        """
        Constructor of the class.

        @type web_mvc_encryption_plugin: WebMvcEncryptionPlugin
        @param web_mvc_encryption_plugin: The web mvc encryption plugin.
        """

        self.web_mvc_encryption_plugin = web_mvc_encryption_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_encryption_plugin.web_mvc_utils_plugin

        # retrieves the entity manager arguments
        entity_manager_arguments = self.get_entity_manager_arguments()

        # retrieves the current directory path
        current_directory_path = os.path.dirname(__file__)

        # loads the mvc utils in the web mvc encryption controllers module
        web_mvc_encryption_controllers = web_mvc_utils_plugin.import_module_mvc_utils("web_mvc_encryption_controllers", "web_mvc_encryption.encryption", current_directory_path)

        # creates the web mvc encryption main controller
        self.web_mvc_encryption_main_controller = web_mvc_utils_plugin.create_controller(web_mvc_encryption_controllers.WebMvcEncryptionMainController, [self.web_mvc_encryption_plugin, self], {})

        # creates the web mvc encryption consumer controller
        self.web_mvc_encryption_consumer_controller = web_mvc_utils_plugin.create_controller(web_mvc_encryption_controllers.ConsumerController, [self.web_mvc_encryption_plugin, self], {})

        # creates the entity models classes by creating the entity manager and updating the classes
        self.web_mvc_encryption_entity_models = web_mvc_utils_plugin.create_entity_models("web_mvc_encryption_entity_models", entity_manager_arguments, current_directory_path)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the web mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return ((r"^web_mvc_encryption/sign$", self.web_mvc_encryption_main_controller.handle_web_mvc_encryption_sign, "post"),
                (r"^web_mvc_encryption/verify$", self.web_mvc_encryption_main_controller.handle_web_mvc_encryption_verify, "post"),
                (r"^web_mvc_encryption/consumers/new$", self.web_mvc_encryption_consumer_controller.handle_new, "post"))

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
        plugin_manager = self.web_mvc_encryption_plugin.manager

        # retrieves the web mvc encryption plugin path
        web_mvc_encryption_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_encryption_plugin.id)

        return ((r"^web_mvc_encryption/resources/.+$", (web_mvc_encryption_plugin_path + "/" + EXTRAS_PATH, "web_mvc_encryption/resources")),)

    def set_configuration_property(self, configuration_property):
        # retrieves the configuration
        configuration = configuration_property.get_data()

        # retrieves the extension map
        keys_map = configuration["keys"]

        # retrieves the security map
        security_map = configuration["security"]

        # sets the keys map
        self.keys_map = keys_map

        # sets the security map
        self.security_map = security_map

    def unset_configuration_property(self):
        # sets the keys map
        self.keys_map = {}

        # sets the security map
        self.security_map = {}

    def get_entity_manager_arguments(self):
        """
        Retrieves the entity manager arguments.

        @rtype: Dictionary
        @return: The entity manager arguments.
        """

        # retrieves the resource manager plugin
        resource_manager_plugin = self.web_mvc_encryption_plugin.resource_manager_plugin

        # creates the entity manager arguments map
        entity_manager_arguments = {}

        # copies the entity manager arguments constant to the new entity manager arguments
        colony.libs.map_util.map_copy_deep(ENTITY_MANAGER_ARGUMENTS, entity_manager_arguments)

        # retrieves the system database file name resource
        system_database_filename_resource = resource_manager_plugin.get_resource("system.database.file_name")

        # in case the system database filename resource
        # is defined
        if system_database_filename_resource:
            # retrieves the system database filename suffix
            system_database_filename_suffix = system_database_filename_resource.data
        # otherwise
        else:
            # sets the system database filename suffix as the default one
            system_database_filename_suffix = DEFAULT_DATABASE_SUFFIX

        # creates the system database file name value using the prefix and suffix values
        system_database_filename = DEFAULT_DATABASE_PREFIX + system_database_filename_suffix

        # retrieves the web mvc encryption plugin id
        web_mvc_encryption_plugin_id = self.web_mvc_encryption_plugin.id

        # creates the database file path using the plugin id and the system database filename
        database_file_path = "%configuration:" + web_mvc_encryption_plugin_id + "%/" + system_database_filename

        # sets the file path in the entity manager arguments
        entity_manager_arguments[CONNECTION_PARAMETERS_VALUE][FILE_PATH_VALUE] = database_file_path

        # returns the entity manager arguments
        return entity_manager_arguments
