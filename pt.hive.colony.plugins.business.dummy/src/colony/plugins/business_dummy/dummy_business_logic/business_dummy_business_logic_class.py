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

__revision__ = "$LastChangedRevision: 7681 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-24 18:27:03 +0000 (qua, 24 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import datetime

import colony.libs.importer_util

TRANSACTION_DECORATOR_VALUE = "transaction_decorator"
""" The transaction decorator value """

# imports the transaction decorator
transaction_decorator = colony.libs.importer_util.__importer__(TRANSACTION_DECORATOR_VALUE)

class DummyBusinessLogic:

    def print_dummy(self):
        print "dummy echo"

    def echo_dummy(self):
        return "dummy echo"

    def hello_world(self, name):
        return "hello world " + name

    def hello_world_both(self, name1, name2):
        return "hello world " + name1 + " and " + name2

    def print_entity_manager(self):
        print str(self.entity_manager)

    @transaction_decorator("requires")
    def save_entity(self):
        # retrieves the DummyEntity class from the entity manager
        dummy_entity_class = self.entity_manager.get_entity_class("DummyEntity")

        # creates a new dummy entity instance
        dummy_entity_instance = dummy_entity_class()

        # sets the entity attribute values
        dummy_entity_instance.name = "dummy_name"
        dummy_entity_instance.address = "Test Street, 123"

        # saves the entity instance
        self.entity_manager.save(dummy_entity_instance)

    @transaction_decorator("requires")
    def update_entity(self):
        # retrieves the DummyEntity class from the entity manager
        dummy_entity_class = self.entity_manager.get_entity_class("DummyEntity")

        # creates a new dummy entity instance
        dummy_entity_instance = dummy_entity_class()

        # sets the entity attribute values
        dummy_entity_instance.name = "dummy_name"
        dummy_entity_instance.address = "Test Street 2, 123"

        # updates the entity instance
        self.entity_manager.update(dummy_entity_instance)

    @transaction_decorator("requires")
    def remove_entity(self):
        # retrieves the DummyEntity class from the entity manager
        dummy_entity_class = self.entity_manager.get_entity_class("DummyEntity")

        # creates a new dummy entity instance
        dummy_entity_instance = dummy_entity_class()

        # sets the entity attribute values
        dummy_entity_instance.name = "dummy_name"

        # removes the entity instance
        self.entity_manager.remove(dummy_entity_instance)

    @transaction_decorator("requires")
    def save_remove_entity(self):
        # saves the entity instance
        self.save_entity()

        # removes the entity instance
        self.remove_entity()

    @transaction_decorator("requires")
    def save_complex_entity(self):
        # retrieves the DummyEntityBundle class from the entity manager
        dummy_entity_bundle_class = self.entity_manager.get_entity_class("DummyEntityBundle")

        # retrieves the DummyEntityBundleAssociation class from the entity manager
        dummy_entity_bundle_association_class = self.entity_manager.get_entity_class("DummyEntityBundleAssociation")

        # retrieves the DummyEntityBundleNew class from the entity manager
        dummy_entity_bundle_new_class = self.entity_manager.get_entity_class("DummyEntityBundleNew")

        # creates a new dummy entity bundle instance
        dummy_entity_bundle_instance = dummy_entity_bundle_class()

        # creates a new dummy entity bundle instance
        dummy_entity_bundle_instance_1 = dummy_entity_bundle_class()

        # creates a new dummy entity bundle association instance
        dummy_entity_bundle_association_instance = dummy_entity_bundle_association_class()

        # create a new dummy entity bundle new instance
        dummy_entity_bundle_new_instance = dummy_entity_bundle_new_class()

        # sets the dummy entity bundle instance attributes
        dummy_entity_bundle_instance.name = "test"
        dummy_entity_bundle_instance.age = 25
        dummy_entity_bundle_instance.local_date = datetime.datetime.utcnow()

        # sets the dummy entity bundle instance attributes
        dummy_entity_bundle_instance_1.name = "test_1"
        dummy_entity_bundle_instance_1.age = 21
        dummy_entity_bundle_instance_1.local_date = datetime.datetime.utcnow()

        # sets the dummy entity bundle association instance attributes
        dummy_entity_bundle_association_instance.name = "test_association"

        # sets the dummy entity bundle new instance attributes
        dummy_entity_bundle_new_instance.name = "test_association_2"

        # sets the entity instances relation attributes
        dummy_entity_bundle_association_instance.entity_other_to_many_relation = [dummy_entity_bundle_new_instance]

        dummy_entity_bundle_instance.entity_relation = dummy_entity_bundle_association_instance
        dummy_entity_bundle_instance.entity_relation = dummy_entity_bundle_association_instance
        dummy_entity_bundle_instance_1.entity_relation = dummy_entity_bundle_association_instance
        dummy_entity_bundle_instance.entity_to_many_relation = [dummy_entity_bundle_association_instance]

        # saves the entity instance
        self.entity_manager.save(dummy_entity_bundle_new_instance)

        # saves the entity instance
        self.entity_manager.save(dummy_entity_bundle_association_instance)

        # saves the entity instance
        self.entity_manager.save(dummy_entity_bundle_instance)

        # saves the entity instance
        self.entity_manager.save(dummy_entity_bundle_instance_1)

        # creates the get options map
        get_options = {
            "eager_loading_relations" : {
                "entity_relation" : {},
                "entity_to_many_relation" : {
                    "eager_loading_relations" : {
                        "entity_other_to_many_relation" : {}
                    }
                }
            }
        }

        # finds the entity bundle instance
        dummy_entity_bundle_instance = self.entity_manager.get(dummy_entity_bundle_class, "test", get_options)

        # sets the entity to many as empty
        dummy_entity_bundle_instance.entity_to_many_relation = []

        # updates the entity bundle instance
        self.entity_manager.update(dummy_entity_bundle_instance)

        # creates the find options map
        find_options = {
            "retrieve_eager_loading_relations" : True,
            "fields" : [
                "age"
            ],
            "order_by" : [
                (
                    "name",
                    "descending"
                ),
                (
                    "age",
                    "descending"
                )
            ],
            "filters" : [
                {
                    "filter_type" : "equals",
                    "filter_fields" : [
                        {
                            "field_name" : "name",
                            "field_value" : "test_1"
                        },
                        {
                            "field_name" : "name",
                            "field_value" : "test"
                        }
                    ]
                },
                {
                    "filter_type" : "like",
                    "filter_fields" : [
                        {
                            "field_name" : "name",
                            "field_value" : "test"
                        }
                    ]
                }
            ]
        }

        # finds all the dummy entity bundle entities with the given filter
        self.entity_manager.find_a(dummy_entity_bundle_class, find_options)

        # removes the entity instance
        self.entity_manager.remove(dummy_entity_bundle_new_instance)

        # removes the entity instance
        self.entity_manager.remove(dummy_entity_bundle_association_instance)

        # removes the entity instance
        self.entity_manager.remove(dummy_entity_bundle_instance)

        # removes the entity instance
        self.entity_manager.remove(dummy_entity_bundle_instance_1)
