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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

import dns_storage_database_exceptions

ENTITIES_MODULE_NAME = "dns_storage_database_entities"
""" The entities module name """

FILTERS_VALUE = "filters"
""" The filters value """

FILTER_TYPE_VALUE = "filter_type"
""" The filter type value """

FILTER_FIELDS_VALUE = "filter_fields"
""" The filter fields value """

class DnsStorageDatabase:
    """
    The dns storage database class.
    """

    dns_storage_database_plugin = None
    """ The dns storage database plugin """

    def __init__(self, dns_storage_database_plugin):
        """
        Constructor of the class.

        @type dns_storage_database_plugin: DnsStorageDatabasePlugin
        @param dns_storage_database_plugin: The dns storage database plugin.
        """

        self.dns_storage_database_plugin = dns_storage_database_plugin

    def create_client(self, parameters):
        """
        Creates a client object for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to be used in creating
        the client object.
        @rtype: DnsStorageDatabaseClient
        @return: The created client object.
        """

        # retrieves the entity manager arguments
        entity_manager_arguments = parameters.get("entity_manager_arguments", {})

        # creates the dns storage database client
        dns_storage_database_client = DnsStorageDatabaseClient(self, entity_manager_arguments)

        # returns the dns storage database client
        return dns_storage_database_client

class DnsStorageDatabaseClient:
    """
    The dns storage database client class.
    """

    dns_storage_database = None
    """ The dns storage database """

    entity_manager_arguments = None
    """ The entity manager arguments """

    entity_manager = None
    """ The entity manager to be used to access the database """

    def __init__(self, dns_storage_database, entity_manager_arguments):
        """
        Constructor of the class.

        @type dns_storage_database: DnsStorageDatabase
        @param dns_storage_database: The dns storage database.
        @type entity_manager_arguments: Dictionary
        @param entity_manager_arguments: The entity manager arguments.
        """

        self.dns_storage_database = dns_storage_database
        self.entity_manager_arguments = entity_manager_arguments

    def create_zone(self, name):
        # retrieves the entity manager
        entity_manager = self._get_entity_manager()

        # creates a transaction
        entity_manager.create_transaction()

        try:
            # retrieves the zone class
            zone_class = entity_manager.get_entity_class("Zone")

            # creates the new zone instance
            zone = zone_class()

            # sets the initial zone attributes
            zone.name = name

            # saves the zone
            entity_manager.save(zone)
        except:
            # rolls back the transaction
            entity_manager.rollback_transaction()

            # re-raises the exception
            raise
        else:
            # commits the transaction
            entity_manager.commit_transaction()

    def create_record(self, zone_name, name, type, class_, time_to_live, value):
        # retrieves the entity manager
        entity_manager = self._get_entity_manager()

        # creates a transaction
        entity_manager.create_transaction()

        try:
            # retrieves the zone
            zone = self.get_zone_name(zone_name)

            # in case no zone is found
            if not zone:
                # raises the invalid zone error
                raise dns_storage_database_exceptions.InvalidZoneError(zone)

            # retrieves the record class
            record_class = entity_manager.get_entity_class("Record")

            # creates the new record instance
            record = record_class()

            # sets the initial record attributes
            record.name = name
            record.type = type
            record.class_ = class_
            record.time_to_live = time_to_live
            record.value = value

            # saves the record
            entity_manager.save(record)
        except:
            # rolls back the transaction
            entity_manager.rollback_transaction()

            # re-raises the exception
            raise
        else:
            # commits the transaction
            entity_manager.commit_transaction()

    def get_records_filtered(self, name, type, class_):
        """
        Retrieves the records for the given name, type and class.

        @type name: String
        @param name: The name of the record to be retrieved.
        @type type: String
        @param type: The type of the record to be retrieved.
        @type class_: String
        @param class_: The class of the record to be retrieved.
        @rtype: List
        @return: The retrieved records.
        """

        # retrieves the entity manager
        entity_manager = self._get_entity_manager()

        # retrieves the record class
        record_class = entity_manager.get_entity_class("Record")

        # defines the find options for retrieving the records
        find_options = {
            FILTERS_VALUE : [
                {
                    FILTER_TYPE_VALUE : "equals",
                    FILTER_FIELDS_VALUE : (
                        {
                            "field_name" : "name",
                            "field_value" : name
                        },
                        {
                            "field_name" : "type",
                            "field_value" : type
                        },
                        {
                            "field_name" : "class_",
                            "field_value" : class_
                        }
                    )
                }
            ]
        }

        # retrieves the valid records
        records = entity_manager.find_a(record_class, find_options)

        return records

    def get_zone_name(self, name):
        """
        Retrieves the zone for the given name.

        @type name: String
        @param name: The name of the zone to be retrieved.
        @rtype: Zone
        @requires: The retrieved zone.
        """

        # retrieves the entity manager
        entity_manager = self._get_entity_manager()

        # retrieves the zone class
        zone_class = entity_manager.get_entity_class("Zone")

        # defines the find options for retrieving the zones
        find_options = {
            FILTERS_VALUE : (
                {
                    FILTER_TYPE_VALUE : "equals",
                    FILTER_FIELDS_VALUE : (
                        {
                            "field_name" : "name",
                            "field_value" : name
                        },
                    )
                },
            )
        }

        # retrieves the valid zones
        zones = entity_manager.find_a(zone_class, find_options)

        if len(zones):
            return zones[0]

    def _get_entity_manager(self):
        """
        Retrieves the currently available entity
        manager instance.

        @rtype: EntityManager
        @return: The currently available entity
        manager instance.
        """

        # in case the entity manager is not set
        # the entity manager is not loaded
        if not self.entity_manager:
            # loads the entity manager
            self._load_entity_manager()

        # returns the entity manager
        return self.entity_manager

    def _load_entity_manager(self):
        """
        Loads the entity manager object, used to access
        the database.
        """

        # retrieves the entity manager helper plugin
        entity_manager_helper_plugin = self.dns_storage_database.dns_storage_database_plugin.entity_manager_helper_plugin

        # loads the entity manager for the entities module name
        self.entity_manager = entity_manager_helper_plugin.load_entity_manager(ENTITIES_MODULE_NAME, os.path.dirname(__file__), self.entity_manager_arguments)
