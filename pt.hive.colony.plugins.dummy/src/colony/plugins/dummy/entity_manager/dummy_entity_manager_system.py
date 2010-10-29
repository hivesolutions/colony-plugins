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

        # retrieves the resource manager plugin
        resource_manager_plugin = self.dummy_entity_manager_plugin.resource_manager_plugin

        # retrieves the entity manager plugin
        entity_manager_plugin = self.dummy_entity_manager_plugin.entity_manager_plugin

        # retrieves the user home path resource
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")

        # retrieves the user home path value
        user_home_path = user_home_path_resource.data

        # retrieves the database file name resource
        database_file_name_resource = resource_manager_plugin.get_resource("system.database.file_name")

        # retrieves the database file name
        database_file_name = database_file_name_resource.data

        # creates a new entity manager with the sqlite engine
        entity_manager = entity_manager_plugin.load_entity_manager("sqlite")

        # sets the connection parameters for the entity manager
        entity_manager.set_connection_parameters({"file_path" : user_home_path + "/" + database_file_name, "autocommit" : False})

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
        #entity_manager.rollback_transaction("test_transaction_removal")

        # commits the transaction
        entity_manager.commit_transaction("test_transaction_removal")

        # commits the entity manager
        entity_manager.commit()

class BusinessLogicDummy:
    pass
