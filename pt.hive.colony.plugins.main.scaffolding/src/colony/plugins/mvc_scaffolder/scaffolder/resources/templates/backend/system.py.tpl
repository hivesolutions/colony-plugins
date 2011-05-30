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

import os

import colony.libs.map_util

FILE_PATH_VALUE = "file_path"
""" The file path value """

ENTITY_MANAGER_ARGUMENTS = {
    "engine" : "sqlite",
    "connection_parameters" : {
        "autocommit" : False
    }
}
""" The entity manager arguments """

CONNECTION_PARAMETERS_VALUE = "connection_parameters"
""" The connection parameters value """

DEFAULT_DATABASE_SUFFIX = "database.db"
""" The default database suffix """

DEFAULT_DATABASE_PREFIX = "${out value=scaffold_attributes.variable_name /}_"
""" The default database prefix """

class ${out value=scaffold_attributes.class_name /}:
    """
    The ${out value=scaffold_attributes.short_name_lowercase /} class.
    """

    ${out value=scaffold_attributes.variable_name /}_plugin = None
    """ The ${out value=scaffold_attributes.short_name_lowercase /} plugin """

    root_entity_controller = None
    """ The root entity controller """

    ${out value=scaffold_attributes.variable_name /}_entity_models = None
    """ The ${out value=scaffold_attributes.short_name_lowercase /} entity models """

    ${out value=scaffold_attributes.variable_name /}_controllers = {}
    """ The ${out value=scaffold_attributes.short_name_lowercase /} controllers """

    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin):
        """
        Constructor of the class.

        @type ${out value=scaffold_attributes.variable_name /}_plugin: ${out value=scaffold_attributes.class_name /}Plugin
        @param ${out value=scaffold_attributes.variable_name /}_plugin: The ${out value=scaffold_attributes.short_name_lowercase /} plugin.
        """

        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.${out value=scaffold_attributes.variable_name /}_plugin.web_mvc_utils_plugin

        # retrieves the entity manager arguments
        entity_manager_arguments = self.get_entity_manager_arguments()

        # retrieves the current directory path
        current_directory_path = os.path.dirname(__file__)

        # loads the mvc utils in the ${out value=scaffold_attributes.short_name /} controllers
        ${out value=scaffold_attributes.variable_name /}_controllers = web_mvc_utils_plugin.import_module_mvc_utils("${out value=scaffold_attributes.variable_name /}_controllers", "${out value=scaffold_attributes.backend_namespace /}", current_directory_path)

        # creates the ${out value=scaffold_attributes.short_name_lowercase /} controller
        self.root_entity_controller = web_mvc_utils_plugin.create_controller(${out value=scaffold_attributes.variable_name /}_controllers.RootEntityController, [self.${out value=scaffold_attributes.variable_name /}_plugin, self], {})

        # creates the entity models classes by creating the entity manager and updating the classes
        self.${out value=scaffold_attributes.variable_name /}_entity_models = web_mvc_utils_plugin.create_entity_models_path("${out value=scaffold_attributes.variable_name /}_entity_models", entity_manager_arguments, current_directory_path)

        # defines the ${out value=scaffold_attributes.short_name_lowercase /} controllers map
        self.${out value=scaffold_attributes.variable_name /}_controllers = {
            "root_entity" : self.root_entity_controller
        }

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
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities$", self.root_entity_controller.handle_list, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities/new$", self.root_entity_controller.handle_new, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities/new$", self.root_entity_controller.handle_create, "post"),
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities/(?P<root_entity_object_id>[0-9]+)$", self.root_entity_controller.handle_show, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities/(?P<root_entity_object_id>[0-9]+)/update$", self.root_entity_controller.handle_edit, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities/(?P<root_entity_object_id>[0-9]+)/update$", self.root_entity_controller.handle_update, "post"),
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities/(?P<root_entity_object_id>[0-9]+)/delete$", self.root_entity_controller.handle_delete, "get")
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

        return ()

    def get_entity_manager_arguments(self):
        """
        Retrieves the entity manager arguments.

        @rtype: Dictionary
        @return: The entity manager arguments.
        """

        # retrieves the resource manager plugin
        resource_manager_plugin = self.${out value=scaffold_attributes.variable_name /}_plugin.resource_manager_plugin

        # creates the entity manager arguments map
        entity_manager_arguments = {}

        # copies the entity manager arguments constant to the new entity manager arguments
        colony.libs.map_util.map_copy_deep(ENTITY_MANAGER_ARGUMENTS, entity_manager_arguments)

        # retrieves the system database file name resource
        system_database_filename_resource = resource_manager_plugin.get_resource("system.database.file_name")

        # retrieves the system database filename suffix
        system_database_filename_suffix = system_database_filename_resource and system_database_filename_resource.data or DEFAULT_DATABASE_SUFFIX

        # creates the system database file name value using the prefix and suffix values
        system_database_filename = DEFAULT_DATABASE_PREFIX + system_database_filename_suffix

        # retrieves the ${out value=scaffold_attributes.short_name_lowercase /} plugin id
        ${out value=scaffold_attributes.variable_name /}_plugin_id = self.${out value=scaffold_attributes.variable_name /}_plugin.id

        # creates the database file path using the plugin id and the system database filename
        database_file_path = "%configuration:" + ${out value=scaffold_attributes.variable_name /}_plugin_id + "%/" + system_database_filename

        # sets the file path in the entity manager arguments
        entity_manager_arguments[CONNECTION_PARAMETERS_VALUE][FILE_PATH_VALUE] = database_file_path

        # returns the entity manager arguments
        return entity_manager_arguments
