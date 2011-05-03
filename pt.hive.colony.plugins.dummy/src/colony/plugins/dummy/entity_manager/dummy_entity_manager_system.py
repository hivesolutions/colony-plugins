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

DEFAULT_DATABASE_PREFIX = "dummy_entity_manager_"
""" The default database prefix """

ENTITY_CLASSES_NAMESPACES = (
    "pt.hive.colony.business.dummy",
)
""" The entity classes namespaces """

class DummyEntityManager:
    """
    The dummy entity manager class
    """

    dummy_entity_manager_plugin = None
    """ The dummy entity manager plugin """

    def __init__(self, dummy_entity_manager_plugin):
        """
        Constructor of the class

        @type dummy_entity_manager_plugin: DummyEntityManagerPlugin
        @param dummy_entity_manager_plugin: The dummy entity manager plugin.
        """

        self.dummy_entity_manager_plugin = dummy_entity_manager_plugin

    def test_entity_manager(self):
        """
        Tests the entity manager creating some booting the manager
        and persisting some entities.
        """

        # retrieves the entity manager plugin
        entity_manager_plugin = self.dummy_entity_manager_plugin.entity_manager_plugin

        # retrieves the business helper plugin
        business_helper_plugin = self.dummy_entity_manager_plugin.business_helper_plugin

        # retrieves the entity classes for the omni base data namespaces
        entity_classes = business_helper_plugin.get_entity_classes_namespaces(ENTITY_CLASSES_NAMESPACES)

        # generates the entity classes map from the entity classes list
        # creating the map associating the class names with the classes
        entity_classes_map = business_helper_plugin.generate_bundle_map(entity_classes)

        # creates the entity manager properties
        entity_manager_properties = {
            ENTITY_CLASSES_LIST_VALUE : entity_classes,
            ENTITY_CLASSES_MAP_VALUE : entity_classes_map
        }

        # creates a new entity manager with the sqlite engine
        entity_manager = entity_manager_plugin.load_entity_manager_properties("sqlite", entity_manager_properties)

        # retrieves the entity manager connection parameters
        connection_parameters = self._get_connection_parameters()

        # sets the connection parameters for the entity manager
        entity_manager.set_connection_parameters(connection_parameters)

        # loads the entity manager
        entity_manager.load_entity_manager()

        # creates a new transaction
        entity_manager.create_transaction("test_transaction")

        # retrieves the business dummy entity plugin
        business_dummy_entity_plugin = self.dummy_entity_manager_plugin.business_dummy_entity_plugin

        # retrieves the dummy entity class
        dummy_entity_class = business_dummy_entity_plugin.get_entity_class()

        # creates a dummy entity instance from the class
        dummy_entity = dummy_entity_class()

        # sets the entity attributes
        dummy_entity.name = "dummy"
        dummy_entity.age = 1

        try:
            # persists the entity in the entity manager
            entity_manager.save(dummy_entity)
        except Exception, exception:
            # prints an info message
            self.dummy_entity_manager_plugin.info("Error saving: " + unicode(exception))

        # finds the entity
        entity_manager.find(dummy_entity_class, "dummy")

        # removes the entity from the database
        entity_manager.remove(dummy_entity)

        # retrieves the entity class from the entity manager
        entity_manager.get_entity_class("DummyEntity")

        # retrieves the dummy entity bundle class from the entity manager
        dummy_entity_bundle_class = entity_manager.get_entity_class("DummyEntityBundle")

        # retrieves the dummy entity bundle association class from the entity manager
        dummy_entity_bundle_association_class = entity_manager.get_entity_class("DummyEntityBundleAssociation")

        # creates a new entity bundle association instance
        dummy_entity_bundle_association = dummy_entity_bundle_association_class()

        # sets the dummy entity bundle attributes
        dummy_entity_bundle_association.name = "test_name2"
        dummy_entity_bundle_association.address = "Tobias Street, 120"
        dummy_entity_bundle_association.hair_type = "blonde"

        try:
            # persists the entity in the entity manager
            entity_manager.save(dummy_entity_bundle_association)
        except Exception, exception:
            # prints an info message
            self.dummy_entity_manager_plugin.info("Error saving: " + unicode(exception))

        # creates a new entity bundle instance
        dummy_entity_bundle = dummy_entity_bundle_class()

        # sets the entity bundle attributes
        dummy_entity_bundle.name = "test_name"
        dummy_entity_bundle.address = "Sesame Street, 12"
        dummy_entity_bundle.age = 12
        dummy_entity_bundle.entity_relation = dummy_entity_bundle_association

        try:
            # persists the entity in the entity manager
            entity_manager.save(dummy_entity_bundle)
        except Exception, exception:
            # prints an info message
            self.dummy_entity_manager_plugin.info("Error saving: " + unicode(exception))

        # retrieves the dummy entity bundle class with test_name key
        entity_manager.find(dummy_entity_bundle_class, "test_name")

        # commits the transaction
        entity_manager.commit_transaction("test_transaction")

        # creates a new transaction
        entity_manager.create_transaction("test_transaction_removal")

        # removes the entity
        entity_manager.remove(dummy_entity_bundle)

        # removes the entity
        entity_manager.remove(dummy_entity_bundle_association)

        # commits the transaction
        entity_manager.commit_transaction("test_transaction_removal")

        # commits the entity manager
        entity_manager.commit()

    def _get_connection_parameters(self):
        """
        Retrieves the entity manager connection parameters.

        @rtype: Dictionary
        @return: The entity manager connection parameters.
        """

        # retrieves the resource manager plugin
        resource_manager_plugin = self.dummy_entity_manager_plugin.resource_manager_plugin

        # creates the entity manager connection parameters
        connection_parameters = {
            "autocommit" : False
        }

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

        # retrieves the dummy entity manager plugin id
        dummy_entity_manager_plugin_id = self.dummy_entity_manager_plugin.id

        # creates the database file path using the plugin id and the system database filename
        database_file_path = "%configuration:" + dummy_entity_manager_plugin_id + "%/" + system_database_filename

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
        plugin_manager = self.dummy_entity_manager_plugin.manager

        # resolves the file path
        connection_parameters[FILE_PATH_VALUE] = plugin_manager.resolve_file_path(connection_parameters[FILE_PATH_VALUE], True, True)

class BusinessLogicDummy:
    pass
