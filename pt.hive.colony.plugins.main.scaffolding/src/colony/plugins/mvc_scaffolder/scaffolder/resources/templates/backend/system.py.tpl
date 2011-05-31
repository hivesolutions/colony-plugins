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

ENTITY_MANAGER_ARGUMENTS = {
    "engine" : "sqlite",
    "connection_parameters" : {
        "autocommit" : False
    }
}
""" The entity manager arguments """

ENTITY_MANAGER_PARAMETERS = {
    "default_database_prefix" : "${out value=scaffold_attributes.variable_name /}_"
}
""" The entity manager parameters """

class ${out value=scaffold_attributes.class_name /}:
    """
    The ${out value=scaffold_attributes.short_name_lowercase /} class.
    """

    ${out value=scaffold_attributes.variable_name /}_plugin = None
    """ The ${out value=scaffold_attributes.short_name_lowercase /} plugin """

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

        # creates the controllers for the ${out value=scaffold_attributes.short_name_lowercase /} controllers module
        web_mvc_utils_plugin.create_controllers("${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_controllers", self, self.${out value=scaffold_attributes.variable_name /}_plugin, "${out value=scaffold_attributes.variable_name /}")

        # creates the entity models classes by creating the entity manager and updating the classes
        web_mvc_utils_plugin.create_models("${out value=scaffold_attributes.variable_name /}_entity_models", self, self.${out value=scaffold_attributes.variable_name /}_plugin, entity_manager_arguments)

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
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_list, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/new$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_new, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_create, "post"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_show, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)/edit$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_edit, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)/update$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_update, "post"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)/delete$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_delete, "post")
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
        plugin_manager = self.${out value=scaffold_attributes.variable_name /}_plugin.manager

        # retrieves the ${out value=scaffold_attributes.short_name_lowercase /} plugin path
        ${out value=scaffold_attributes.variable_name /}_plugin_path = plugin_manager.get_plugin_path_by_id(self.${out value=scaffold_attributes.variable_name /}_plugin.id)

        return (
            (r"^${out value=scaffold_attributes.variable_name /}/resources/.+$", (${out value=scaffold_attributes.variable_name /}_plugin_path + "/${out value=scaffold_attributes.relative_backend_path /}/resources/extras", "${out value=scaffold_attributes.variable_name /}/resources")),
        )

    def get_entity_manager_arguments(self):
        """
        Retrieves the entity manager arguments.

        @rtype: Dictionary
        @return: The entity manager arguments.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.${out value=scaffold_attributes.variable_name /}_plugin.web_mvc_utils_plugin

        # generates the entity manager arguments
        entity_manager_arguments = web_mvc_utils_plugin.generate_entity_manager_arguments(self.${out value=scaffold_attributes.variable_name /}_plugin, ENTITY_MANAGER_ARGUMENTS, ENTITY_MANAGER_PARAMETERS)

        # returns the entity manager arguments
        return entity_manager_arguments
