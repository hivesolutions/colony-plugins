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

ENTITY_CLASSES_LIST_VALUE = "entity_classes_list"
""" The entity classes list value """

ENTITY_CLASSES_MAP_VALUE = "entity_classes_map"
""" The entity classes map value """

FILE_PATH_VALUE = "file_path"
""" The file path value """

DEFAULT_DATABASE_SUFFIX = "database.db"
""" The default database suffix """

DEFAULT_DATABASE_PREFIX = "dummy_business_logic_1_"
""" The default database prefix """

ENTITY_CLASSES_NAMESPACES = ("pt.hive.colony.business.dummy",)
""" The entity classes namespaces """

BUSINESS_LOGIC_CLASSES_NAMESPACES = ("pt.hive.colony.business.dummy",)
""" The business logic classes namespaces """

class DummyBusinessLogic1:
    """
    The dummy business logic 1 class.
    """

    dummy_business_logic_1_plugin = None
    """ The dummy business logic 1 plugin """

    def __init__(self, dummy_business_logic_1_plugin):
        """
        Constructor of the class.

        @type dummy_business_logic_1_plugin: DummyBusinessLogic1Plugin
        @param dummy_business_logic_1_plugin: The dummy business logic 1 plugin.
        """

        self.dummy_business_logic_1_plugin = dummy_business_logic_1_plugin

    def create_dummy_session(self):
        """
        Creates a dummy session to test it.
        """

        # retrieves the business session manager plugin
        business_session_manager_plugin = self.dummy_business_logic_1_plugin.business_session_manager_plugin

        # retrieves the business helper plugin
        business_helper_plugin = self.dummy_business_logic_1_plugin.business_helper_plugin

        # retrieves the entity classes for the omni base data namespaces
        entity_classes = business_helper_plugin.get_entity_classes_namespaces(ENTITY_CLASSES_NAMESPACES)

        # retrieves the business logic classes for the omni base logic namespaces
        business_logic_classes = business_helper_plugin.get_business_logic_classes_namespaces(BUSINESS_LOGIC_CLASSES_NAMESPACES)

        # generates the entity classes map from the entity classes list
        # creating the map associating the class names with the classes
        entity_classes_map = business_helper_plugin.generate_bundle_map(entity_classes)

        # generates the business logic classes map from the business logic classes list
        # creating the map associating the class names with the classes
        business_logic_classes_map = business_helper_plugin.generate_bundle_map(business_logic_classes)

        # creates the entity manager properties
        entity_manager_properties = {ENTITY_CLASSES_LIST_VALUE : entity_classes, ENTITY_CLASSES_MAP_VALUE : entity_classes_map}

        # creates the dummy session
        dummy_session = business_session_manager_plugin.load_session_manager_master_entity_manager_business_logic("dummy_session", "sqlite", entity_manager_properties,  business_logic_classes, business_logic_classes_map)

        # retrieves the entity manager
        entity_manager = dummy_session.entity_manager

        # retrieves the entity manager connection parameters
        connection_parameters = self._get_connection_parameters()

        # sets the connection parameters for the entity manager
        entity_manager.set_connection_parameters(connection_parameters)

        # loads the entity manager
        entity_manager.load_entity_manager()

        # start the session in the dummy session
        dummy_session.start_session()

        # calls the echo dummy method in the dummy business logic entity
        dummy_session.DummyBusinessLogic.echo_dummy()

        # calls the save remove entity method in the dummy business logic entity
        dummy_session.DummyBusinessLogic.save_remove_entity()

        # calls the save complex entity method in the dummy business logic entity
        dummy_session.DummyBusinessLogic.save_complex_entity()

    def _get_connection_parameters(self):
        """
        Retrieves the entity manager connection parameters.

        @rtype: Dictionary
        @return: The entity manager connection parameters.
        """

        # retrieves the resource manager plugin
        resource_manager_plugin = self.dummy_business_logic_1_plugin.resource_manager_plugin

        # creates the entity manager connection parameters
        connection_parameters = {"autocommit" : False}

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

        # retrieves the dummy business logic 1 plugin id
        dummy_business_logic_1_plugin_id = self.dummy_business_logic_1_plugin.id

        # creates the database file path using the plugin id and the system database filename
        database_file_path = "%configuration:" + dummy_business_logic_1_plugin_id + "%/" + system_database_filename

        # sets the file path in the entity manager connection parameters
        connection_parameters[FILE_PATH_VALUE] = database_file_path

        # resolves the connection parameters
        self._resolve_connection_parameters(connection_parameters)

        # returns the entity manager connection parameters
        return connection_parameters

    def _resolve_connection_parameters(self, connection_parameters):
        """
        Resolves the given connection parameters map, substituting
        the values with the resolved ones.

        @type connection_parameters: Dictionary
        @param connection_parameters: The connection parameters to be resolved.
        """

        # retrieves the plugin manager
        plugin_manager = self.dummy_business_logic_1_plugin.manager

        # resolves the file path
        connection_parameters[FILE_PATH_VALUE] = plugin_manager.resolve_file_path(connection_parameters[FILE_PATH_VALUE], True, True)
