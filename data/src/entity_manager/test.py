#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import sys
import shutil
import sqlite3
import tempfile

import colony

from . import mocks
from . import migration
from . import structures
from . import exceptions


class EntityManagerTest(colony.Test):
    """
    The entity manager class.
    """

    def get_bundle(self):
        return (
            EntityManagerBaseTestCase,
            EntityManagerConcreteTableTestCase,
            EntityManagerMigrationTestCase,
            EntityManagerRsetTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

        # saves and removes the global inheritance override, the test cases
        # pin the inheritance strategy of their own entity classes and so an
        # ambient override (used to migrate complete applications) would
        # invalidate the expectations of the complete bundle
        test_case.data_inheritance = colony.conf("DATA_INHERITANCE")
        colony.conf_r("DATA_INHERITANCE")

        # retrieves the entity manager (system)
        system = self.plugin.system

        # loads a new entity manager, extends it with the
        # entity manager test mocks opens it (loading and
        # generator creation) and begins a new  transaction
        # context (for the current set of operations)
        test_case.entity_manager = system.load_entity_manager("sqlite")
        test_case.entity_manager.extend_module(mocks)
        test_case.entity_manager.open(start=False)
        test_case.entity_manager.create_generator()
        test_case.entity_manager.begin()

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)

        # restores the global inheritance override that was removed for
        # the execution of the current test case
        if test_case.data_inheritance:
            colony.conf_s("DATA_INHERITANCE", test_case.data_inheritance)

        # rolls back the current transaction in the
        # entity manager
        test_case.entity_manager.rollback()

        # destroys the underlying data source, removes
        # all files and structures associated with the
        # current entity manager context
        test_case.entity_manager.destroy()


class EntityManagerBaseTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Entity Manager Base test case"

    def test_create(self):
        # creates the complete set of entities existent in the current
        # mocks bundle set (this should take a while)
        self.entity_manager.create(mocks.RootEntity)
        self.entity_manager.create(mocks.Loggable)
        self.entity_manager.create(mocks.Taxable)
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Employee)
        self.entity_manager.create(mocks.Address)
        self.entity_manager.create(mocks.Dog)
        self.entity_manager.create(mocks.Cat)
        self.entity_manager.create(mocks.Car)
        self.entity_manager.create(mocks.Supplier)
        self.entity_manager.create(mocks.Operation)

        # verifies that all the data source references for the entity classes
        # have been created successfully
        self.assertTrue(self.entity_manager.exists(mocks.RootEntity))
        self.assertTrue(self.entity_manager.exists(mocks.Loggable))
        self.assertTrue(self.entity_manager.exists(mocks.Taxable))
        self.assertTrue(self.entity_manager.exists(mocks.Person))
        self.assertTrue(self.entity_manager.exists(mocks.Employee))
        self.assertTrue(self.entity_manager.exists(mocks.Address))
        self.assertTrue(self.entity_manager.exists(mocks.Dog))
        self.assertTrue(self.entity_manager.exists(mocks.Cat))
        self.assertTrue(self.entity_manager.exists(mocks.Car))
        self.assertTrue(self.entity_manager.exists(mocks.Supplier))
        self.assertTrue(self.entity_manager.exists(mocks.Operation))

    def test_delete(self):
        # creates the complete set of entities existent in the current
        # mocks bundle set (this should take a while)
        self.entity_manager.create(mocks.RootEntity)
        self.entity_manager.create(mocks.Loggable)
        self.entity_manager.create(mocks.Taxable)
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Employee)
        self.entity_manager.create(mocks.Address)
        self.entity_manager.create(mocks.Dog)
        self.entity_manager.create(mocks.Cat)
        self.entity_manager.create(mocks.Car)
        self.entity_manager.create(mocks.Supplier)
        self.entity_manager.create(mocks.Operation)

        # verifies that all the data source references for the entity classes
        # have been created successfully
        self.assertTrue(self.entity_manager.exists(mocks.RootEntity))
        self.assertTrue(self.entity_manager.exists(mocks.Loggable))
        self.assertTrue(self.entity_manager.exists(mocks.Taxable))
        self.assertTrue(self.entity_manager.exists(mocks.Person))
        self.assertTrue(self.entity_manager.exists(mocks.Employee))
        self.assertTrue(self.entity_manager.exists(mocks.Address))
        self.assertTrue(self.entity_manager.exists(mocks.Dog))
        self.assertTrue(self.entity_manager.exists(mocks.Cat))
        self.assertTrue(self.entity_manager.exists(mocks.Car))
        self.assertTrue(self.entity_manager.exists(mocks.Supplier))
        self.assertTrue(self.entity_manager.exists(mocks.Operation))

        # deletes the complete set of entities existent in the current
        # mocks bundle set (this should take a while)
        self.entity_manager.delete(mocks.RootEntity)
        self.entity_manager.delete(mocks.Loggable)
        self.entity_manager.delete(mocks.Taxable)
        self.entity_manager.delete(mocks.Person)
        self.entity_manager.delete(mocks.Employee)
        self.entity_manager.delete(mocks.Address)
        self.entity_manager.delete(mocks.Dog)
        self.entity_manager.delete(mocks.Cat)
        self.entity_manager.delete(mocks.Car)
        self.entity_manager.delete(mocks.Supplier)
        self.entity_manager.delete(mocks.Operation)

        # verifies that all the data source references for the entity classes
        # have been deleted successfully
        self.assertFalse(self.entity_manager.exists(mocks.RootEntity))
        self.assertFalse(self.entity_manager.exists(mocks.Loggable))
        self.assertFalse(self.entity_manager.exists(mocks.Taxable))
        self.assertFalse(self.entity_manager.exists(mocks.Person))
        self.assertFalse(self.entity_manager.exists(mocks.Employee))
        self.assertFalse(self.entity_manager.exists(mocks.Address))
        self.assertFalse(self.entity_manager.exists(mocks.Dog))
        self.assertFalse(self.entity_manager.exists(mocks.Cat))
        self.assertFalse(self.entity_manager.exists(mocks.Car))
        self.assertFalse(self.entity_manager.exists(mocks.Supplier))
        self.assertFalse(self.entity_manager.exists(mocks.Operation))

    def test_save(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Dog)

        # creates the person entity that is going to be used
        # for the verification of the save method and saves it
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(person.object_id, 1)
        self.assertEqual(person.name, "name_person")

        # retrieves the saved person by the unique identifier
        # of it and verifies that the object is not modified
        saved_person = self.entity_manager.get(mocks.Person, 1)
        self.assertNotEqual(saved_person, None)

        # verifies that the entity values of the retrieve entity
        # are the same as the original entity
        self.assertEqual(saved_person.object_id, person.object_id)
        self.assertEqual(saved_person.name, person.name)

        # creates the dog entity that is going to be used
        # for the verification of the save of relations
        # then saves it associated with the person
        dog = mocks.Dog()
        dog.object_id = 2
        dog.name = "name_dog"
        dog.owner = person
        self.entity_manager.save(dog)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(dog.object_id, 2)
        self.assertEqual(dog.name, "name_dog")

        # retrieves both the dog and the "associated" person to test them
        # for the correct relations
        saved_dog = self.entity_manager.get(mocks.Dog, 2)
        saved_person = self.entity_manager.get(mocks.Person, 1)
        self.assertNotEqual(saved_dog, None)
        self.assertNotEqual(saved_person, None)

        # verifies that both sides of the relations are correct,
        # both the dog is related with the owner and the person
        # with the appropriate dogs
        self.assertEqual(saved_dog.owner.object_id, person.object_id)
        self.assertEqual(saved_person.dogs[0].object_id, dog.object_id)

    def test_self_relation(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates the parent person and child person entities
        # using the self-referencing parent/children relation
        parent = mocks.Person()
        parent.object_id = 1
        parent.name = "parent_person"
        child_a = mocks.Person()
        child_a.object_id = 2
        child_a.name = "child_a"
        child_a.parent = parent
        child_b = mocks.Person()
        child_b.object_id = 3
        child_b.name = "child_b"
        child_b.parent = parent
        self.entity_manager.save(parent)
        self.entity_manager.save(child_a)
        self.entity_manager.save(child_b)

        # retrieves the parent person and verifies that the children
        # relation is correctly populated via the reverse side
        saved_parent = self.entity_manager.get(mocks.Person, 1)
        self.assertNotEqual(saved_parent, None)
        self.assertNotEqual(saved_parent.children, [])
        self.assertEqual(len(saved_parent.children), 2)

        # retrieves a child and verifies that the parent relation
        # is correctly set on the mapped side
        saved_child = self.entity_manager.get(mocks.Person, 2)
        self.assertNotEqual(saved_child, None)
        self.assertNotEqual(saved_child.parent, None)
        self.assertEqual(saved_child.parent.object_id, parent.object_id)

        # updates the parent reference of a child (re-parent)
        # and verifies the update is persisted correctly
        new_parent = mocks.Person()
        new_parent.object_id = 4
        new_parent.name = "new_parent"
        self.entity_manager.save(new_parent)
        child_a.parent = new_parent
        self.entity_manager.update(child_a)

        # retrieves the re-parented child and verifies the new
        # parent reference is correctly persisted
        saved_child = self.entity_manager.get(mocks.Person, 2)
        self.assertNotEqual(saved_child, None)
        self.assertNotEqual(saved_child.parent, None)
        self.assertEqual(saved_child.parent.object_id, new_parent.object_id)

    def test_metadata(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates the the person with a series of default information
        # and with some metadata added to it (as expected)
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        person.metadata = dict(occupation="student", salary=100)
        self.entity_manager.save(person)

        # retrieves the person from the data source and verifies that
        # the complete information is correctly retrieved from the
        # data source, including the metadata structure
        saved_person = self.entity_manager.get(mocks.Person, 1)
        self.assertNotEqual(saved_person, None)
        self.assertEqual(saved_person.object_id, 1)
        self.assertEqual(saved_person.name, "name_person")
        self.assertEqual(saved_person.metadata, dict(occupation="student", salary=100))

        # creates a new person and populates the information, this time
        # the person's occupation is encoded with special characters in order
        # to test the unicode encoding of metadata
        person = mocks.Person()
        person.object_id = 2
        person.name = "name_person"
        person.metadata = dict(occupation=colony.legacy.u("学生"), salary=10)
        self.entity_manager.save(person)

        # retrieves the person from the data source and verifies that
        # the complete information is correctly retrieved from the
        # data source, including the metadata structure
        saved_person = self.entity_manager.get(mocks.Person, 2)
        self.assertNotEqual(saved_person, None)
        self.assertEqual(saved_person.object_id, 2)
        self.assertEqual(saved_person.name, "name_person")
        self.assertEqual(
            saved_person.metadata, dict(occupation=colony.legacy.u("学生"), salary=10)
        )

    def test_one_to_one(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Address)
        self.entity_manager.create(mocks.Employee)

        # creates the the person and address entities and populates
        # them with some values, then sets the person relation
        # in the address side and saves both entities
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        address = mocks.Address()
        address.object_id = 2
        address.street = "street_address"
        address.door = 1
        address.country = "country_address"
        address.person = person
        self.entity_manager.save(person)
        self.entity_manager.save(address)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(person.object_id, 1)
        self.assertEqual(person.name, "name_person")
        self.assertEqual(address.object_id, 2)
        self.assertEqual(address.street, "street_address")
        self.assertEqual(address.door, 1)
        self.assertEqual(address.country, "country_address")

        # retrieves both the person and the address to test them
        # for the correct relations
        saved_person = self.entity_manager.get(mocks.Person, 1)
        saved_address = self.entity_manager.get(mocks.Address, 2)
        self.assertNotEqual(saved_person, None)
        self.assertNotEqual(saved_address, None)

        # verifies that both sides of the relations are correct,
        # both the person has the appropriate address and the address
        # has the correct person
        self.assertNotEqual(saved_person.address, None)
        self.assertNotEqual(saved_address.person, None)
        self.assertEqual(saved_person.address.object_id, address.object_id)
        self.assertEqual(saved_address.person.object_id, person.object_id)

        # creates the the address and person entities and populates
        # them with some values, then sets the person relation
        # in the address side and saves both entities
        address = mocks.Address()
        address.object_id = 3
        address.name = "name_address"
        person = mocks.Person()
        person.object_id = 4
        person.name = "name_person"
        person.address = address
        self.entity_manager.save(address)
        self.entity_manager.save(person)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(address.object_id, 3)
        self.assertEqual(address.name, "name_address")
        self.assertEqual(person.object_id, 4)
        self.assertEqual(person.name, "name_person")

        # retrieves both the address and the person to test them
        # for the correct relations
        saved_address = self.entity_manager.get(mocks.Address, 3)
        saved_person = self.entity_manager.get(mocks.Person, 4)
        self.assertNotEqual(saved_address, None)
        self.assertNotEqual(saved_person, None)

        # verifies that both sides of the relations are correct,
        # both the address has the correct person and the person has the
        # appropriate address
        self.assertNotEqual(saved_address.person, None)
        self.assertNotEqual(saved_person.address, None)
        self.assertEqual(saved_address.person.object_id, person.object_id)
        self.assertEqual(saved_person.address.object_id, address.object_id)

        # creates the the employee and address entities and populates
        # them with some values, then sets the employee relation
        # in the address side and saves both entities
        employee = mocks.Employee()
        employee.object_id = 5
        employee.name = "name_employee"
        address = mocks.Address()
        address.object_id = 6
        address.street = "street_address"
        address.door = 1
        address.country = "country_address"
        address.person = employee
        self.entity_manager.save(employee)
        self.entity_manager.save(address)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(employee.object_id, 5)
        self.assertEqual(employee.name, "name_employee")
        self.assertEqual(address.object_id, 6)
        self.assertEqual(address.street, "street_address")
        self.assertEqual(address.door, 1)
        self.assertEqual(address.country, "country_address")

        # retrieves both the employee and the address to test them
        # for the correct relations
        saved_employee = self.entity_manager.get(mocks.Employee, 5)
        saved_address = self.entity_manager.get(mocks.Address, 6)
        self.assertNotEqual(saved_employee, None)
        self.assertNotEqual(saved_address, None)

        # verifies that both sides of the relations are correct,
        # both the employee has the appropriate address and the address
        # has the correct employee
        self.assertNotEqual(saved_employee.address, None)
        self.assertNotEqual(saved_address.person, None)
        self.assertEqual(saved_employee.address.object_id, address.object_id)
        self.assertEqual(saved_address.person.object_id, employee.object_id)

        # creates the the address and employee entities and populates
        # them with some values, then sets the employee relation
        # in the address side and saves both entities
        address = mocks.Address()
        address.object_id = 7
        address.name = "name_address"
        employee = mocks.Employee()
        employee.object_id = 8
        employee.name = "name_employee"
        employee.address = address
        self.entity_manager.save(address)
        self.entity_manager.save(employee)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(address.object_id, 7)
        self.assertEqual(address.name, "name_address")
        self.assertEqual(employee.object_id, 8)
        self.assertEqual(employee.name, "name_employee")

        # retrieves both the address and the employee to test them
        # for the correct relations
        saved_address = self.entity_manager.get(mocks.Address, 7)
        saved_employee = self.entity_manager.get(mocks.Employee, 8)
        self.assertNotEqual(saved_address, None)
        self.assertNotEqual(saved_employee, None)

        # verifies that both sides of the relations are correct,
        # both the address has the correct employee and the employee has the
        # appropriate address
        self.assertNotEqual(saved_address.person, None)
        self.assertNotEqual(saved_employee.address, None)
        self.assertEqual(saved_address.person.object_id, employee.object_id)
        self.assertEqual(saved_employee.address.object_id, address.object_id)

    def test_one_to_many(self):
        """
        Tests the one-to-many relations saving and retrieval
        of values.

        == Objectives ==
        * Tests that the persistence layer correctly saves
        one to many relations.
        * Tests that the retrieval method correctly retrieves
        one to many relations.
        * Tests that both sides of the (one-to-many) relation
        can be used for saving of the relation.
        * Test that parent (one-to-many) relations are correctly
        persisted and retrieved.

        == Steps ==
        * Creates the person and dog entities.
        * Associate them via the person.
        * Saves both of the relations.
        * Retrieves both relations from the data source.
        * Tests that both sides of the relation retrieve the
        correct and expected relations.

        * Repeats the process inverting the saving side
        of the relation (used the person side)

        * Repeats the overall process but using the employee
        (sub class of person) to test the relation with a sub
        class.
        """

        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Dog)
        self.entity_manager.create(mocks.Employee)

        # creates the the person and dog entities and populates
        # them with some values, then sets the owner relation
        # in the dog side and saves both entities
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        dog = mocks.Dog()
        dog.object_id = 2
        dog.name = "name_dog"
        dog.owner = person
        self.entity_manager.save(person)
        self.entity_manager.save(dog)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(person.object_id, 1)
        self.assertEqual(person.name, "name_person")
        self.assertEqual(dog.object_id, 2)
        self.assertEqual(dog.name, "name_dog")

        # retrieves both the person and the dog to test them
        # for the correct relations
        saved_person = self.entity_manager.get(mocks.Person, 1)
        saved_dog = self.entity_manager.get(mocks.Dog, 2)
        self.assertNotEqual(saved_person, None)
        self.assertNotEqual(saved_dog, None)

        # verifies that both sides of the relations are correct,
        # both the person has the appropriate dogs and the dog
        # has the correct owner
        self.assertNotEqual(saved_person.dogs, [])
        self.assertNotEqual(saved_dog.owner, None)
        self.assertEqual(saved_person.dogs[0].object_id, dog.object_id)
        self.assertEqual(saved_dog.owner.object_id, person.object_id)

        # creates the the dog and person entities and populates
        # them with some values, then sets the owner relation
        # in the dog side and saves both entities
        dog = mocks.Dog()
        dog.object_id = 3
        dog.name = "name_dog"
        person = mocks.Person()
        person.object_id = 4
        person.name = "name_person"
        person.dogs = [dog]
        self.entity_manager.save(dog)
        self.entity_manager.save(person)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(dog.object_id, 3)
        self.assertEqual(dog.name, "name_dog")
        self.assertEqual(person.object_id, 4)
        self.assertEqual(person.name, "name_person")

        # retrieves both the dog and the person to test them
        # for the correct relations
        saved_dog = self.entity_manager.get(mocks.Dog, 3)
        saved_person = self.entity_manager.get(mocks.Person, 4)
        self.assertNotEqual(saved_dog, None)
        self.assertNotEqual(saved_person, None)

        # verifies that both sides of the relations are correct,
        # both the dog has the correct owner and the person has the
        # appropriate dogs
        self.assertNotEqual(saved_dog.owner, None)
        self.assertNotEqual(saved_person.dogs, [])
        self.assertEqual(saved_dog.owner.object_id, person.object_id)
        self.assertEqual(saved_person.dogs[0].object_id, dog.object_id)

        # creates the the employee and dog entities and populates
        # them with some values, then sets the owner relation
        # in the dog side and saves both entities
        employee = mocks.Employee()
        employee.object_id = 5
        employee.name = "name_employee"
        dog = mocks.Dog()
        dog.object_id = 6
        dog.name = "name_dog"
        dog.owner = employee
        self.entity_manager.save(employee)
        self.entity_manager.save(dog)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(employee.object_id, 5)
        self.assertEqual(employee.name, "name_employee")
        self.assertEqual(dog.object_id, 6)
        self.assertEqual(dog.name, "name_dog")

        # retrieves both the employee and the dog to test them
        # for the correct relations
        saved_employee = self.entity_manager.get(mocks.Employee, 5)
        saved_dog = self.entity_manager.get(mocks.Dog, 6)
        self.assertNotEqual(saved_employee, None)
        self.assertNotEqual(saved_dog, None)

        # verifies that both sides of the relations are correct,
        # both the employee has the appropriate dogs and the dog
        # has the correct owner
        self.assertNotEqual(saved_employee.dogs, [])
        self.assertNotEqual(saved_dog.owner, None)
        self.assertEqual(saved_employee.dogs[0].object_id, dog.object_id)
        self.assertEqual(saved_dog.owner.object_id, employee.object_id)

        # creates the the dog and employee entities and populates
        # them with some values, then sets the owner relation
        # in the dog side and saves both entities
        dog = mocks.Dog()
        dog.object_id = 7
        dog.name = "name_dog"
        employee = mocks.Employee()
        employee.object_id = 8
        employee.name = "name_employee"
        employee.dogs = [dog]
        self.entity_manager.save(dog)
        self.entity_manager.save(employee)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(dog.object_id, 7)
        self.assertEqual(dog.name, "name_dog")
        self.assertEqual(employee.object_id, 8)
        self.assertEqual(employee.name, "name_employee")

        # retrieves both the dog and the employee to test them
        # for the correct relations
        saved_dog = self.entity_manager.get(mocks.Dog, 7)
        saved_employee = self.entity_manager.get(mocks.Employee, 8)
        self.assertNotEqual(saved_dog, None)
        self.assertNotEqual(saved_employee, None)

        # verifies that both sides of the relations are correct,
        # both the dog has the correct owner and the employee has the
        # appropriate dogs
        self.assertNotEqual(saved_dog.owner, None)
        self.assertNotEqual(saved_employee.dogs, [])
        self.assertEqual(saved_dog.owner.object_id, employee.object_id)
        self.assertEqual(saved_employee.dogs[0].object_id, dog.object_id)

    def test_many_to_many(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Car)
        self.entity_manager.create(mocks.Employee)

        # creates the the person and car entities and populates
        # them with some values, then sets the owners relation
        # in the dog side and saves both entities
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        car = mocks.Car()
        car.object_id = 2
        car.tires = 4
        car.owners = [person]
        self.entity_manager.save(person)
        self.entity_manager.save(car)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(person.object_id, 1)
        self.assertEqual(person.name, "name_person")
        self.assertEqual(car.object_id, 2)
        self.assertEqual(car.tires, 4)

        # retrieves both the person and the car to test them
        # for the correct relations
        saved_person = self.entity_manager.get(mocks.Person, 1)
        saved_car = self.entity_manager.get(mocks.Car, 2)
        self.assertNotEqual(saved_person, None)
        self.assertNotEqual(saved_car, None)

        # verifies that both sides of the relations are correct,
        # both the person has the appropriate cars and the car
        # has the correct owners
        self.assertNotEqual(saved_person.cars, [])
        self.assertNotEqual(saved_car.owners, [])
        self.assertEqual(saved_person.cars[0].object_id, car.object_id)
        self.assertEqual(saved_car.owners[0].object_id, person.object_id)

        # creates the the car and person entities and populates
        # them with some values, then sets the owners relation
        # in the car side and saves both entities
        car = mocks.Car()
        car.object_id = 3
        car.tires = 4
        person = mocks.Person()
        person.object_id = 4
        person.name = "name_person"
        person.cars = [car]
        self.entity_manager.save(car)
        self.entity_manager.save(person)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(car.object_id, 3)
        self.assertEqual(car.tires, 4)
        self.assertEqual(person.object_id, 4)
        self.assertEqual(person.name, "name_person")

        # retrieves both the car and the person to test them
        # for the correct relations
        saved_car = self.entity_manager.get(mocks.Car, 3)
        saved_person = self.entity_manager.get(mocks.Person, 4)
        self.assertNotEqual(saved_car, None)
        self.assertNotEqual(saved_person, None)

        # verifies that both sides of the relations are correct,
        # both the car has the correct owners and the person has the
        # appropriate cars
        self.assertNotEqual(saved_car.owners, [])
        self.assertNotEqual(saved_person.cars, [])
        self.assertEqual(saved_car.owners[0].object_id, person.object_id)
        self.assertEqual(saved_person.cars[0].object_id, car.object_id)

        # creates the the employee and car entities and populates
        # them with some values, then sets the owners relation
        # in the dog side and saves both entities
        employee = mocks.Employee()
        employee.object_id = 5
        employee.name = "name_employee"
        car = mocks.Car()
        car.object_id = 6
        car.tires = 4
        car.owners = [employee]
        self.entity_manager.save(employee)
        self.entity_manager.save(car)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(employee.object_id, 5)
        self.assertEqual(employee.name, "name_employee")
        self.assertEqual(car.object_id, 6)
        self.assertEqual(car.tires, 4)

        # retrieves both the employee and the car to test them
        # for the correct relations
        saved_employee = self.entity_manager.get(mocks.Employee, 5)
        saved_car = self.entity_manager.get(mocks.Car, 6)
        self.assertNotEqual(saved_employee, None)
        self.assertNotEqual(saved_car, None)

        # verifies that both sides of the relations are correct,
        # both the employee has the appropriate cars and the car
        # has the correct owners
        self.assertNotEqual(saved_employee.cars, [])
        self.assertNotEqual(saved_car.owners, [])
        self.assertEqual(saved_employee.cars[0].object_id, car.object_id)
        self.assertEqual(saved_car.owners[0].object_id, employee.object_id)

        # creates the the car and employee entities and populates
        # them with some values, then sets the owners relation
        # in the car side and saves both entities
        car = mocks.Car()
        car.object_id = 7
        car.tires = 4
        employee = mocks.Employee()
        employee.object_id = 8
        employee.name = "name_employee"
        employee.cars = [car]
        self.entity_manager.save(car)
        self.entity_manager.save(employee)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(car.object_id, 7)
        self.assertEqual(car.tires, 4)
        self.assertEqual(employee.object_id, 8)
        self.assertEqual(employee.name, "name_employee")

        # retrieves both the car and the employee to test them
        # for the correct relations
        saved_car = self.entity_manager.get(mocks.Car, 7)
        saved_employee = self.entity_manager.get(mocks.Employee, 8)
        self.assertNotEqual(saved_car, None)
        self.assertNotEqual(saved_employee, None)

        # verifies that both sides of the relations are correct,
        # both the car has the correct owners and the employee has the
        # appropriate cars
        self.assertNotEqual(saved_car.owners, [])
        self.assertNotEqual(saved_employee.cars, [])
        self.assertEqual(saved_car.owners[0].object_id, employee.object_id)
        self.assertEqual(saved_employee.cars[0].object_id, car.object_id)

    def test_to_one(self):
        pass

    def test_to_many(self):
        pass

    def test_to_one_indirect(self):
        pass

    def test_multilevel(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Breeder)
        self.entity_manager.create(mocks.BreedDog)

        # creates the initial breeder entity that will be used latter
        # to be set as the owner of the new breed dog
        breeder = mocks.Breeder()
        breeder.object_id = 1
        breeder.name = "name_breeder"
        breeder.license_number = "license_number_breeder"
        self.entity_manager.save(breeder)

        # creates the breed dog entity that is going to be associated
        # to the breeder at a multi layer relation level
        breed_dog = mocks.BreedDog()
        breed_dog.object_id = 2
        breed_dog.name = "name_breed_dog"
        breed_dog.owner = breeder
        breed_dog.digital_tag = "digital_tag_breed_dog"
        self.entity_manager.save(breed_dog)

        # retrieves both the breeder so that the proper relations at
        # a multi layer level may be properly tested
        saved_breeder = self.entity_manager.get(mocks.Breeder, 1)
        self.assertNotEqual(saved_breeder, None)

        # verifies that the to many dogs relations is correctly retrieved
        # and that the breed dog level attributes are available
        self.assertNotEqual(saved_breeder.dogs, [])
        self.assertEqual(saved_breeder.dogs[0].object_id, breed_dog.object_id)
        self.assertEqual(saved_breeder.dogs[0].digital_tag, breed_dog.digital_tag)

        # retrieves the breed dog using an eager approach to the owner and then
        # verifies that the license number is properly set (as expected)
        saved_breed_dog = self.entity_manager.get(
            mocks.BreedDog, 2, dict(eager=("owner",))
        )
        self.assertEqual(saved_breed_dog.owner.license_number, breeder.license_number)

    def test_save_with_cycle(self):
        pass

    def test_find(self):
        pass

    def test_invalid_relation(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Dog)
        self.entity_manager.create(mocks.Car)

        # creates the the person and dog entities and populates
        # them with some values, then sets the owner relation
        # in the dog side and saves both entities, note that no
        # object id is set in the person nor it is generated because
        # no person is saved
        person = mocks.Person()
        person.object_id = None
        person.name = "name_person"
        dog = mocks.Dog()
        dog.object_id = 1
        dog.name = "name_dog"
        dog.owner = person

        # verifies that an exception is raised because no identifier
        # is set in the person object associated with the dog, cannot
        # associate an item with no identifier
        self.assert_raises(exceptions.ValidationError, self.entity_manager.save, dog)

        # creates the the dog and person entities and populates
        # them with some values, then sets the dogs relation
        # in the person side and saves both entities, note that no
        # object id is set in the dog nor it is generated because
        # no dog is saved
        dog = mocks.Dog()
        dog.object_id = None
        dog.name = "name_dog"
        person = mocks.Person()
        person.object_id = 2
        person.name = "name_person"
        person.dogs = [dog]

        # verifies that an exception is raised because no identifier
        # is set in the dog object associated with the person, cannot
        # associate an item with no identifier
        self.assert_raises(exceptions.ValidationError, self.entity_manager.save, person)

        # creates the the car and person entities and populates
        # them with some values, then sets the cars relation
        # in the person side and saves both entities, note that no
        # object id is set in the car nor it is generated because
        # no dog is saved
        car = mocks.Car()
        car.object_id = None
        car.tires = 4
        person = mocks.Person()
        person.object_id = 3
        person.name = "name_person"
        person.cars = [car]

        # verifies that an exception is raised because no identifier
        # is set in the car object associated with the person, cannot
        # associate an item with no identifier
        self.assert_raises(exceptions.ValidationError, self.entity_manager.save, person)

        # creates the the car and dog entities and populates
        # them with some values, then sets the owner relation
        # in the dog side with the (invalid) car value
        car = mocks.Car()
        car.object_id = 4
        car.tires = 4
        dog = mocks.Dog()
        dog.object_id = 5
        dog.name = "name_dog"
        dog.owner = car

        # verifies that an exception is raised because the type of object
        # for the owner relation in the dog entity is invalid (should be
        # person instead got car)
        self.assert_raises(
            exceptions.RelationValidationError, self.entity_manager.save, dog
        )

        # creates the the car and person entities and populates
        # them with some values, then sets the dogs relation
        # in the person side with the (invalid) car value
        car = mocks.Car()
        car.object_id = 6
        car.tires = 4
        person = mocks.Person()
        person.object_id = 7
        person.name = "name_person"
        person.dogs = [car]

        # verifies that an exception is raised because the type of object
        # for the dogs relation in the dog entity is invalid (should be
        # dog instead got car)
        self.assert_raises(
            exceptions.RelationValidationError, self.entity_manager.save, person
        )

        # creates the the dog and car entities and populates
        # them with some values, then sets the owners relation
        # in the car side with the (invalid) dog value
        dog = mocks.Dog()
        dog.object_id = 8
        dog.name = "name_dog"
        car = mocks.Car()
        car.object_id = 9
        car.tires = 4
        car.owners = [dog]

        # verifies that an exception is raised because the type of object
        # for the owners relation in the car entity is invalid (should be
        # person instead got dog)
        self.assert_raises(
            exceptions.RelationValidationError, self.entity_manager.save, car
        )

        # creates the the person and car entities and populates
        # them with some values, then sets the owners relation
        # in the car side with an invalid type value (not sequence)
        person = mocks.Person()
        person.object_id = 10
        person.name = "name_person"
        car = mocks.Car()
        car.object_id = 11
        car.tires = 4
        car.owners = person

        # verifies that an exception is raised because the type of object
        # for the owners relation in the car entity is invalid (should be
        # a sequence type got a single person instead)
        self.assert_raises(exceptions.ValidationError, self.entity_manager.save, car)

    def test_database_integrity(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Dog)

        # creates and saves a person, then creates a dog associated
        # with the person and saves it to verify referential integrity
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        dog = mocks.Dog()
        dog.object_id = 2
        dog.name = "name_dog"
        dog.owner = person
        self.entity_manager.save(dog)

        # removes the dog and verifies that the person still exists
        # in the data source (removing a child should not affect parent)
        self.entity_manager.remove(dog)
        saved_person = self.entity_manager.get(mocks.Person, 1)
        self.assertNotEqual(saved_person, None)
        self.assertEqual(saved_person.name, "name_person")

        # verifies the dog has been removed
        saved_dog = self.entity_manager.get(mocks.Dog, 2)
        self.assertEqual(saved_dog, None)

    def test_invalid_type(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a person entity with an invalid type for the
        # age field (should be integer but setting a list instead)
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        person.age = [1, 2, 3]

        # verifies that a validation error is raised because the
        # age field has an invalid type
        self.assert_raises(exceptions.ValidationError, self.entity_manager.save, person)

    def test_polymorphism(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a person entity with it's default attributes and
        # saves it into the data source
        person = mocks.Person()
        person.object_id = 1
        person.status = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(person.object_id, 1)
        self.assertEqual(person.status, 1)
        self.assertEqual(person.name, "name_person")

        # retrieves the person using a polymorphic query so
        # that only the root entity fields are populated and
        # then verifies that the result is valid/set
        saved_person = self.entity_manager.get(mocks.RootEntity, 1)
        self.assertNotEqual(saved_person, None)

        # detaches the person from the data source and verifies
        # that the root entity level fields are set but the person
        # level ones are not (polymorphic query)
        saved_person.detach()
        self.assertEqual(saved_person.object_id, 1)
        self.assertEqual(saved_person.status, 1)
        self.assertEqual(saved_person.name, None)

        # attaches the person back to the data source (enabling lazy
        # attribute evaluation) and verifies that the person level
        # attributes are now accessible and that the top level ones
        # (root entity) remain the same after lazy attribute evaluation
        saved_person.attach()
        saved_person.status = 2
        self.assertEqual(saved_person.name, "name_person")
        self.assertEqual(saved_person.status, 2)

        # runs the original test one more time be using the root entity
        # level of retrieval and then forces the loading of the lazy
        # attribute (should populate also upper layers) and verifies
        # that the status value is returned to the original value because
        # of the forced loading of the upper layer attributes
        saved_person = self.entity_manager.get(mocks.RootEntity, 1)
        self.assertNotEqual(saved_person, None)
        saved_person.status = 2
        saved_person._load_lazy_attr("name", force=True)
        self.assertEqual(saved_person.name, "name_person")
        self.assertEqual(saved_person.status, 1)

    def test_map(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a series of person entities and saves them
        person_a = mocks.Person()
        person_a.object_id = 1
        person_a.name = "name_person_a"
        person_a.age = 30
        person_b = mocks.Person()
        person_b.object_id = 2
        person_b.name = "name_person_b"
        person_b.age = 25
        self.entity_manager.save(person_a)
        self.entity_manager.save(person_b)

        # retrieves all persons using the map option so that the
        # result is returned as a list of dictionaries
        persons = self.entity_manager.find(mocks.Person, dict(map=True))

        # verifies that the result is a list of maps (dictionaries)
        # and that the values are correctly set
        self.assertNotEqual(persons, [])
        self.assertEqual(len(persons), 2)
        self.assertEqual(type(persons[0]), dict)
        self.assertTrue("name" in persons[0])
        self.assertTrue("object_id" in persons[0])

    def test_map_relations(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Address)
        self.entity_manager.create(mocks.Dog)

        # creates a person with both a "to one" and a "to many" relation
        # so that the map based retrieval has to build the nested
        # structures for each one of them
        address = mocks.Address()
        address.object_id = 1
        address.street = "street_address"
        person = mocks.Person()
        person.object_id = 2
        person.name = "name_person"
        person.address = address
        dog = mocks.Dog()
        dog.object_id = 3
        dog.name = "name_dog"
        dog.owner = person
        self.entity_manager.save(address)
        self.entity_manager.save(person)
        self.entity_manager.save(dog)

        # retrieves the person as a map, eagerly loading the "to one"
        # relation, and verifies that it is unpacked as a nested map
        persons = self.entity_manager.find(
            mocks.Person, dict(map=True, eager=("address",))
        )
        self.assertEqual(len(persons), 1)
        self.assertEqual(type(persons[0]), dict)
        self.assertEqual(type(persons[0]["address"]), dict)
        self.assertEqual(persons[0]["address"]["object_id"], 1)
        self.assertEqual(persons[0]["address"]["street"], "street_address")

        # retrieves the person eagerly loading the "to many" relation and
        # verifies that it is unpacked as a list of maps instead
        persons = self.entity_manager.find(
            mocks.Person, dict(map=True, eager=("dogs",))
        )
        self.assertEqual(len(persons), 1)
        self.assertEqual(type(persons[0]["dogs"]), list)
        self.assertEqual(len(persons[0]["dogs"]), 1)
        self.assertEqual(persons[0]["dogs"][0]["name"], "name_dog")

        # verifies that the discriminator is unpacked both for the entity
        # and for the eagerly loaded relations
        self.assertEqual(persons[0]["_class"], "Person")
        self.assertEqual(persons[0]["dogs"][0]["_class"], "Dog")

    def test_map_relations_nested(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Address)
        self.entity_manager.create(mocks.Dog)

        # creates a dog owned by a person that in turn has an address,
        # so that the retrieval has to traverse two levels of relations
        address = mocks.Address()
        address.object_id = 1
        address.street = "street_address"
        person = mocks.Person()
        person.object_id = 2
        person.name = "name_person"
        person.address = address
        dog = mocks.Dog()
        dog.object_id = 3
        dog.name = "name_dog"
        dog.owner = person
        self.entity_manager.save(address)
        self.entity_manager.save(person)
        self.entity_manager.save(dog)

        # retrieves the dog eagerly loading both the owner and the
        # address of the owner, the deepest relation path of the mock
        # entities, and verifies that every level is unpacked
        dogs = self.entity_manager.find(
            mocks.Dog, dict(map=True, eager=dict(owner=dict(eager=("address",))))
        )
        self.assertEqual(len(dogs), 1)
        self.assertEqual(dogs[0]["name"], "name_dog")
        self.assertEqual(type(dogs[0]["owner"]), dict)
        self.assertEqual(dogs[0]["owner"]["name"], "name_person")
        self.assertEqual(type(dogs[0]["owner"]["address"]), dict)
        self.assertEqual(dogs[0]["owner"]["address"]["street"], "street_address")

    def test_map_relations_undefined(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Address)
        self.entity_manager.create(mocks.Dog)

        # creates a person with no address associated, so that the
        # eagerly loaded relation has no value to be unpacked
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # retrieves the person as a map eagerly loading the relation and
        # verifies that the undefined relation is reported as such
        # instead of originating a partially built map
        persons = self.entity_manager.find(
            mocks.Person, dict(map=True, eager=("address",))
        )
        self.assertEqual(len(persons), 1)
        self.assertEqual(persons[0]["name"], "name_person")
        self.assertEqual(persons[0]["address"], None)

        # retrieves the person eagerly loading a "to many" relation with
        # no values and verifies that an empty list is reported
        persons = self.entity_manager.find(
            mocks.Person, dict(map=True, eager=("dogs",))
        )
        self.assertEqual(len(persons), 1)
        self.assertEqual(persons[0]["dogs"], [])

    def test_map_cache(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates and saves a person to be retrieved as a map
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # retrieves the person as a map re-using an (initially empty)
        # entities map and then changes one of its attributes, so that the
        # cache mode may be verified in the retrievals that follow
        entities = {}
        persons = self.entity_manager.find(
            mocks.Person, dict(map=True, entities=entities)
        )
        self.assertEqual(persons[0]["name"], "name_person")
        persons[0]["name"] = "name_changed"

        # retrieves the person again re-using the entities map and with the
        # cache mode enabled, the value that is already set must prevail
        # over the one coming from the data source
        persons = self.entity_manager.find(
            mocks.Person, dict(map=True, cache=True, entities=entities)
        )
        self.assertEqual(persons[0]["name"], "name_changed")

        # retrieves the person once more with the cache mode disabled and
        # verifies that the value of the data source is used instead
        persons = self.entity_manager.find(
            mocks.Person, dict(map=True, entities=entities)
        )
        self.assertEqual(persons[0]["name"], "name_person")

    def test_order_by(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Address)

        # creates the the various person entities and populates
        # them with some ordered values to be able to sort them
        person_a = mocks.Person()
        person_a.object_id = 1
        person_a.name = "name_person_a"
        person_c = mocks.Person()
        person_c.object_id = 2
        person_c.name = "name_person_c"
        person_b = mocks.Person()
        person_b.object_id = 3
        person_b.name = "name_person_b"
        self.entity_manager.save(person_a)
        self.entity_manager.save(person_c)
        self.entity_manager.save(person_b)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(person_a.object_id, 1)
        self.assertEqual(person_a.name, "name_person_a")
        self.assertEqual(person_c.object_id, 2)
        self.assertEqual(person_c.name, "name_person_c")
        self.assertEqual(person_b.object_id, 3)
        self.assertEqual(person_b.name, "name_person_b")

        # retrieves the persons from the data source ordered
        # by the name attribute (defaults as descending)
        persons = self.entity_manager.find(mocks.Person, dict(order_by="name"))

        # verifies that the retrieved list is not empty and that
        # the various persons are ordered in the expected order
        self.assertNotEqual(persons, [])
        self.assertEqual(persons[0].object_id, person_c.object_id)
        self.assertEqual(persons[1].object_id, person_b.object_id)
        self.assertEqual(persons[2].object_id, person_a.object_id)

        # retrieves the persons from the data source ordered
        # by the name attribute in descending order (explicit)
        persons = self.entity_manager.find(
            mocks.Person, dict(order_by=(("name", "descending"),))
        )

        # verifies that the retrieved list is not empty and that
        # the various persons are ordered in the expected order
        self.assertNotEqual(persons, [])
        self.assertEqual(persons[0].object_id, person_c.object_id)
        self.assertEqual(persons[1].object_id, person_b.object_id)
        self.assertEqual(persons[2].object_id, person_a.object_id)

        # retrieves the persons from the data source ordered
        # by the name attribute in ascending order (explicit)
        persons = self.entity_manager.find(
            mocks.Person, dict(order_by=(("name", "ascending"),))
        )

        # verifies that the retrieved list is not empty and that
        # the various persons are ordered in the expected order
        self.assertNotEqual(persons, [])
        self.assertEqual(persons[0].object_id, person_a.object_id)
        self.assertEqual(persons[1].object_id, person_b.object_id)
        self.assertEqual(persons[2].object_id, person_c.object_id)

        # creates the the various address entities and populates
        # them with some ordered values to be able to sort them,
        # then associates them with a series of person, this will
        # allow the testing of relation based sorting
        address_a = mocks.Address()
        address_a.object_id = 4
        address_a.street = "street_address_a"
        address_a.person = person_b
        address_b = mocks.Address()
        address_b.object_id = 5
        address_b.street = "street_address_b"
        address_b.person = person_c
        address_c = mocks.Address()
        address_c.object_id = 6
        address_c.street = "street_address_c"
        address_c.person = person_a
        self.entity_manager.save(address_a)
        self.entity_manager.save(address_b)
        self.entity_manager.save(address_c)

        # retrieves the persons from the data source ordered
        # by the address street attribute in descending order
        persons = self.entity_manager.find(
            mocks.Person,
            dict(eager=("address",), order_by=(("address.street", "descending"),)),
        )

        # verifies that the retrieved list is not empty and that
        # the various persons are ordered in the expected order
        self.assertNotEqual(persons, [])
        self.assertEqual(persons[0].object_id, person_a.object_id)
        self.assertEqual(persons[1].object_id, person_c.object_id)
        self.assertEqual(persons[2].object_id, person_b.object_id)

        # retrieves the persons from the data source ordered
        # by the address street attribute in ascending order
        persons = self.entity_manager.find(
            mocks.Person,
            dict(eager=("address",), order_by=(("address.street", "ascending"),)),
        )

        # verifies that the retrieved list is not empty and that
        # the various persons are ordered in the expected order
        self.assertNotEqual(persons, [])
        self.assertEqual(persons[0].object_id, person_b.object_id)
        self.assertEqual(persons[1].object_id, person_c.object_id)
        self.assertEqual(persons[2].object_id, person_a.object_id)

        # retrieves the persons from the data source ordered
        # by the address street attribute in ascending order,
        # now using the asc contraction
        persons = self.entity_manager.find(
            mocks.Person,
            dict(eager=("address",), order_by=(("address.street", "asc"),)),
        )

        # verifies that the retrieved list is not empty and that
        # the various persons are ordered in the expected order
        self.assertNotEqual(persons, [])
        self.assertEqual(persons[0].object_id, person_b.object_id)
        self.assertEqual(persons[1].object_id, person_c.object_id)
        self.assertEqual(persons[2].object_id, person_a.object_id)

    def test_range(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a series of person entities to test pagination
        for i in range(1, 6):
            person = mocks.Person()
            person.object_id = i
            person.name = "name_person_%d" % i
            self.entity_manager.save(person)

        # retrieves all persons without pagination and verifies count
        persons = self.entity_manager.find(mocks.Person)
        self.assertEqual(len(persons), 5)

        # retrieves persons using pagination (first page of 2 items)
        persons = self.entity_manager.find(
            mocks.Person, dict(start_record=0, number_records=2)
        )
        self.assertEqual(len(persons), 2)

        # retrieves persons using pagination (second page of 2 items)
        persons = self.entity_manager.find(
            mocks.Person, dict(start_record=2, number_records=2)
        )
        self.assertEqual(len(persons), 2)

        # retrieves persons using pagination (last page with 1 item)
        persons = self.entity_manager.find(
            mocks.Person, dict(start_record=4, number_records=2)
        )
        self.assertEqual(len(persons), 1)

        # retrieves persons using pagination beyond range (empty result)
        persons = self.entity_manager.find(
            mocks.Person, dict(start_record=10, number_records=2)
        )
        self.assertEqual(len(persons), 0)

    def test_reload(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Dog)

        # creates a person entity with it's default attributes and
        # saves it into the data source
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(person.object_id, 1)
        self.assertEqual(person.name, "name_person")

        # creates a new person entity with new (reload) attributes
        # and updates it into the data source, the person contains
        # the same object id so an update should be done correctly
        person_reload = mocks.Person()
        person_reload.object_id = 1
        person_reload.name = "name_person_reload"
        self.entity_manager.update(person_reload)

        # verifies that the data remains unchanged after
        # the updating (persistence)
        self.assertEqual(person_reload.object_id, 1)
        self.assertEqual(person_reload.name, "name_person_reload")

        # verifies that the (original) data remains unchanged after
        # the updating (persistence)
        self.assertEqual(person.object_id, 1)
        self.assertEqual(person.name, "name_person")

        # reloads the (original) person entity, this should trigger
        # the changing of the person information (data update)
        self.entity_manager.reload(person)

        # verifies that the new data is set in the original entities
        # the reload of the data occurred
        self.assertEqual(person.object_id, 1)
        self.assertEqual(person.name, "name_person_reload")

        # verifies that no dogs are associated with the person, this
        # should trigger the loading of the lazy loaded relation
        self.assertEqual(person.dogs, [])

        # creates a dog entity with it's default attributes associated
        # with the previously created person and saves it into the
        # data source
        dog = mocks.Dog()
        dog.object_id = 2
        dog.name = "name_dog"
        dog.owner = person
        self.entity_manager.save(dog)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(dog.object_id, 2)
        self.assertEqual(dog.name, "name_dog")

        # verifies that the dogs relation of the person remains unchanged
        # after the dog saving (already eagerly loaded before)
        self.assertEqual(person.dogs, [])

        # reloads the (original) person entity, this should trigger
        # the changing of the person information (data update)
        self.entity_manager.reload(person)

        # verifies that the created dog is now associated with the
        # person (this must have triggered a new loading of lazy load)
        self.assertNotEqual(person.dogs, [])
        self.assertEqual(person.dogs[0].object_id, dog.object_id)

    def test_count(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a person entity with it's default attributes and
        # saves it into the data source
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # counts the amount of entities of type person
        # present in the data source
        count = self.entity_manager.count(mocks.Person)

        # verifies that the amount of "persons" in the data
        # source is one (only one persist)
        self.assertEqual(count, 1)

        # creates a person entity with it's default attributes and
        # saves it into the data source
        person = mocks.Person()
        person.object_id = 2
        person.name = "name_person"
        self.entity_manager.save(person)

        # counts the amount of entities of type person
        # present in the data source
        count = self.entity_manager.count(mocks.Person)

        # verifies that the amount of "persons" in the data
        # source is two (two persists)
        self.assertEqual(count, 2)

    def test_generate_id(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a person entity with it's default attributes and
        # (but no identifier) saves it into the data source
        person = mocks.Person()
        person.name = "name_person"
        self.entity_manager.save(person)

        # retrieves the object id value for the person, uses
        # the safest method to avoid possible set problems
        object_id = person.get_value("object_id")

        # verifies that the person object id is correctly set
        # and not null
        self.assertNotEqual(object_id, None)

    def test_duplicate(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Employee)
        self.entity_manager.create(mocks.Car)

        # creates a person entity with it's default attributes and
        # saves it into the data source
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # verifies that a second (duplicate) save of the entity would
        # result in an integrity error raises from the entity manager
        self.assert_raises("IntegrityError", self.entity_manager.save, person)

        # creates a new employee entity (sub class of person) with the
        # same identifier as the created person
        employee = mocks.Employee()
        employee.object_id = 1
        employee.name = "name_employee"

        # verifies that saving the employee also raises an integrity
        # error because the class hierarchy overlaps and the identifier
        # is the same for both objects
        self.assert_raises("IntegrityError", self.entity_manager.save, employee)

        # creates a new employee entity (sub class of root entity and same
        # class hierarchy as the person) with the same identifier as the created
        # person, should also fail on saving
        car = mocks.Car()
        car.object_id = 1
        car.tires = 4

        # verifies that saving the car also raises an integrity
        # error because the class hierarchy overlaps and the identifier
        # is the same for both objects (person and car)
        self.assert_raises("IntegrityError", self.entity_manager.save, car)

    def test_validate_relation(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Dog)

        # creates the the person and dog entities and populates
        # them with some values and saves both entities
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        dog = mocks.Dog()
        dog.object_id = 2
        dog.name = "name_dog"
        self.entity_manager.save(person)
        self.entity_manager.save(dog)

        # associates the dog to the set of dogs present in it
        # but no persistence is made
        person.dogs = [dog]

        # verifies that the relation with the dogs is not considered
        # to be valid because it's not currently persisted in the data
        # source (persistence layer)
        valid_relation = self.entity_manager.validate_relation(person, "dogs")
        self.assertEqual(valid_relation, False)

        # sets the person as the owner of the dog and updates the dog entity
        # to reflect this change, this will allow validation of the relation
        # from the other side of the relation
        dog.owner = person
        self.entity_manager.update(dog)

        # verifies that now the relation is considered to be valid because the
        # owner of the dog is the person, the dog is contained in the person's
        # set of dogs
        valid_relation = self.entity_manager.validate_relation(person, "dogs")
        self.assertEqual(valid_relation, True)

        # creates the the person and the parent (person) entities and populates
        # them with some values and saves both entities
        person = mocks.Person()
        person.object_id = 3
        person.name = "name_person"
        parent = mocks.Person()
        parent.object_id = 4
        parent.name = "name_parent"
        self.entity_manager.save(person)
        self.entity_manager.save(parent)

        # sets the parent of the person, but no persistence is made
        person.parent = parent

        # verifies that the relation with the parent is not considered
        # to be valid because it's not currently persisted in the data
        # source (persistence layer)
        valid_relation = self.entity_manager.validate_relation(person, "parent")
        self.assertEqual(valid_relation, False)

        # sets the person as the set of children of the parent and updates the
        # parent entity to reflect this change, this will allow validation of
        # the relation from the other side of the relation
        parent.children = [person]
        self.entity_manager.update(parent)

        # verifies that now the relation is considered to be valid because the
        # person is one of the children of the parent, the parent of the person
        # is the parent
        valid_relation = self.entity_manager.validate_relation(person, "parent")
        self.assertEqual(valid_relation, True)

    def test_relation_cache(self):
        # retrieves the attributes of a relation twice and verifies that
        # the very same map is returned, meaning that the description is
        # cached instead of being rebuilt on every retrieval
        relation = mocks.Person.get_relation("address")
        self.assertEqual(relation, mocks.Person.get_relation("address"))
        self.assertTrue(relation is mocks.Person.get_relation("address"))

        # verifies that the cache is stored in the class itself and that
        # it only holds the relations that have been retrieved
        self.assertTrue("_relation_attributes" in mocks.Person.__dict__)
        self.assertTrue("address" in mocks.Person._relation_attributes)

        # verifies that the cached description is the expected one, so
        # that the caching does not change the resolution
        self.assertEqual(relation.get("type"), "to-one")
        self.assertEqual(relation.get("target"), mocks.Address)
        self.assertEqual(relation.get("is_mapper"), True)

    def test_relation_cache_subclass(self):
        # retrieves the attributes of a relation in the parent class so
        # that the description is cached at that level
        parent_relation = mocks.Person.get_relation("dogs")
        self.assertEqual(parent_relation.get("target"), mocks.Dog)

        # retrieves the same relation in a subclass that redefines it
        # and verifies that the redefinition is honoured, the cache of
        # the parent must not shadow the description of the descendant
        breeder_relation = mocks.Breeder.get_relation("dogs")
        self.assertEqual(breeder_relation.get("target"), mocks.BreedDog)

        # verifies that each of the classes holds its own cache, so that
        # the descriptions of the two levels remain independent
        self.assertTrue("_relation_attributes" in mocks.Breeder.__dict__)
        self.assertEqual(mocks.Person.get_relation("dogs").get("target"), mocks.Dog)
        self.assertEqual(
            mocks.Breeder.get_relation("dogs").get("target"), mocks.BreedDog
        )

    def test_relation_cache_missing(self):
        # retrieves a relation that does not exist and verifies that an
        # empty description is returned instead of an exception
        self.assertEqual(mocks.Person.get_relation("not_a_relation"), {})

        # verifies that the missing relation is not cached, so that the
        # raise exception behaviour remains available for it
        relation_attributes = mocks.Person.__dict__.get("_relation_attributes", {})
        self.assertFalse("not_a_relation" in relation_attributes)

        # verifies that the very same retrieval raises an exception once
        # the raise exception flag is set
        self.assert_raises(
            exceptions.MissingRelationMethod,
            mocks.Person.get_relation,
            "not_a_relation",
            raise_exception=True,
        )

    def test_relation_cache_not_a_field(self):
        # retrieves a relation so that the cache is created in the class
        # and then verifies that the cache attribute is not mistaken for
        # a field of the entity, which would create a spurious column
        mocks.Person.get_relation("address")
        self.assertFalse("_relation_attributes" in mocks.Person.get_items())
        self.assertFalse("_relation_attributes" in mocks.Person.get_names())
        self.assertFalse("_relation_attributes" in mocks.Person.get_all_items())

    def test_set_sql_value_data_type(self):
        # creates a person entity to be used as the target of the
        # setting of the values coming from the data source
        person = mocks.Person()

        # sets a value without providing the data type and verifies
        # that it is resolved from the entity class
        person.set_sql_value("age", "21")
        self.assertEqual(person.age, 21)

        # sets a value providing the data type explicitly and verifies
        # that the provided one is the one being honoured
        person.set_sql_value("age", "22", data_type="text")
        self.assertEqual(person.age, "22")

    def test_get_data_type_cache(self):
        # retrieves the data type of an attribute twice and verifies
        # that the same value is resolved, the resolution is cached
        self.assertEqual(mocks.Person._get_data_type("age"), "integer")
        self.assertEqual(mocks.Person._get_data_type("age"), "integer")
        self.assertEqual(mocks.Person._get_data_type("name"), "text")
        self.assertEqual(mocks.Person._get_data_type("weight"), "decimal")

        # verifies that the cache is stored in the class itself and that
        # it is indexed by both the name and the resolution mode
        self.assertTrue("_data_types" in mocks.Person.__dict__)
        self.assertTrue(("age", True) in mocks.Person._data_types)

    def test_get_data_type_cache_relations(self):
        # retrieves the data type of a mapped relation with the relation
        # resolution enabled, the type of the identifier of the target
        # class is the one that should be resolved
        self.assertEqual(mocks.Person._get_data_type("address"), "integer")

        # retrieves the same data type with the relation resolution
        # disabled and verifies that the relation type is reported
        # instead, so that the two modes are cached independently
        self.assertEqual(
            mocks.Person._get_data_type("address", resolve_relations=False),
            "relation",
        )
        self.assertEqual(mocks.Person._get_data_type("address"), "integer")

    def test_get_data_type_cache_subclass(self):
        # resolves the data type of an attribute in the parent class so
        # that it becomes cached at that level, then resolves it in a
        # subclass and verifies that both levels agree, the cache of the
        # parent must not be reused by the descendant
        self.assertEqual(mocks.Person._get_data_type("age"), "integer")
        self.assertEqual(mocks.Employee._get_data_type("age"), "integer")
        self.assertTrue("_data_types" in mocks.Employee.__dict__)

        # verifies that an attribute declared by the subclass is also
        # correctly resolved and cached at its own level
        self.assertEqual(mocks.Employee._get_data_type("salary"), "integer")
        self.assertFalse(("salary", True) in mocks.Person.__dict__["_data_types"])

    def test_get_data_type_cache_not_a_field(self):
        # resolves a data type so that the cache is created in the class
        # and then verifies that the cache attribute is not mistaken for
        # a field of the entity, which would create a spurious column
        mocks.Person._get_data_type("age")
        self.assertFalse("_data_types" in mocks.Person.get_items())
        self.assertFalse("_data_types" in mocks.Person.get_names())
        self.assertFalse("_data_types" in mocks.Person.get_all_items())

    def test_from_sql_value_data_type(self):
        # converts a value without providing the data type and verifies
        # that it is resolved from the entity class
        self.assertEqual(mocks.Person._from_sql_value("age", "21"), 21)

        # converts the same value providing the data type explicitly and
        # verifies that the provided one takes precedence, so that the
        # callers may resolve it once for a complete set of values
        self.assertEqual(
            mocks.Person._from_sql_value("age", "21", data_type="text"), "21"
        )

        # verifies that an undefined value is converted to an undefined
        # one, no matter the data type that has been provided
        self.assertEqual(
            mocks.Person._from_sql_value("age", None, data_type="integer"), None
        )

    def test_abstract(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.RootEntityAbstract)
        self.entity_manager.create(mocks.Chair)

        # verifies that all the data source references for the entity classes
        # have been created successfully (or not created depending if the class
        # is abstract or not)
        self.assertFalse(self.entity_manager.has_definition(mocks.RootEntityAbstract))
        self.assertTrue(self.entity_manager.has_definition(mocks.Chair))

        # creates the the chair entity and populates
        # them with some values and saves the entity
        chair = mocks.Chair()
        chair.object_id = 1
        chair.legs = 4
        self.entity_manager.save(chair)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(chair.object_id, 1)
        self.assertEqual(chair.legs, 4)

        # retrieves the saved chair by the unique identifier
        # of it and verifies that the object is not modified
        saved_chair = self.entity_manager.get(mocks.Chair, 1)
        self.assertNotEqual(saved_chair, None)

        # verifies that the entity values of the retrieve entity
        # are the same as the original entity
        self.assertEqual(saved_chair.object_id, chair.object_id)
        self.assertEqual(saved_chair.legs, chair.legs)

    def test_cache(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Address)

        # creates the the person and address entities and populates
        # them with some values, then sets the address relation
        # in the person side and saves both entities
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        address = mocks.Address()
        address.object_id = 2
        address.street = "street_address"
        address.door = 1
        address.country = "country_address"
        person.address = address

        # saves both entities in the data source so that they may be use
        # in the next text operation
        self.entity_manager.save(address)
        self.entity_manager.save(person)

        # retrieves the person from the data source and then retrieves
        # the associated address instance
        person = self.entity_manager.get(mocks.Person, 1)
        address = person.address

        # verifies that the "hidden" entities map is exactly the
        # same instance for both the person and the address
        self.assertEqual(id(person._entities), id(address._entities))

        # verifies that if the typical cache based retrieval approach
        # is used to retrieve the address the instance is the one that
        # has been retrieved using eager loading relations
        _address = person._entities[mocks.Address][2]
        self.assertEqual(id(address), id(_address))

        # runs the reloading operation for the person entity and then
        # verifies that the entities cache map has changed (different
        # instance) and that the size of the new map is one
        self.entity_manager.reload(person)
        self.assertNotEqual(id(person._entities), id(address._entities))
        self.assertEqual(len(person._entities), 1)

        # runs the cache reset operation in the address instance and then
        # verifies/checks that the cache map associated with it is empty
        address.reset_cache()
        self.assertEqual(address._entities, {})

    def test_cache_usage(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Address)

        # creates the the person and address entities and populates
        # them with some values, then sets the address relation
        # in the person side and saves both entities
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        address = mocks.Address()
        address.object_id = 2
        address.street = "street_address"
        address.door = 1
        address.country = "country_address"
        person.address = address

        # saves both entities in the data source so that they may be use
        # in the next text operation
        self.entity_manager.save(address)
        self.entity_manager.save(person)

        # retrieves the person from the data source and then retrieves
        # the associated address instance
        person = self.entity_manager.get(mocks.Person, 1)
        address = person.address

        # changes the name of the person, without persisting it to the
        # data source (this is only a local reference change)
        person.name = "name_person_changed"

        # verifies that even without persisting the value to the data
        # source the name value of the person associated with the address
        # is the same as the person's name, this should have triggered
        # a lazy loading relation (uses cache based retrieval)
        self.assertEqual(person.name, person.address.person.name)
        self.assertEqual(person.address.person.name, "name_person_changed")

        # tries to retrieve the person from the data source using a different
        # set of entities cache and then verifies that the name is the old
        # one as the value is yet to be persisted (as expected)
        cached_person = self.entity_manager.get(mocks.Person, 1)
        self.assertNotEqual(person.name, cached_person.name)
        self.assertEqual(cached_person.name, "name_person")

        # re-tries to retrieve the same person value from the data source but
        # now with the same set of entities cache as the base person and using
        # the cache based strategy, this strategy avoids the access to the data
        # source value as re-uses the cached one, so that the name that is access
        # is the same as the one changed locally by the test
        options = dict(entities=person._entities, cache=True)
        cached_person = self.entity_manager.get(mocks.Person, 1, options=options)
        self.assertEqual(person.name, cached_person.name)
        self.assertEqual(cached_person.name, "name_person_changed")

        # re-uses the previous test, using the same dictionary of entities cache
        # but disables the cache usage so that value is retrieved from the data
        # source changing/reverting the name of the person to the original value
        options = dict(entities=person._entities, cache=False)
        cached_person = self.entity_manager.get(mocks.Person, 1, options=options)
        self.assertEqual(person.name, cached_person.name)
        self.assertEqual(cached_person.name, "name_person")

    def test_nullify(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Address)

        # creates the the person and address entities and populates
        # them with some values, then sets the address relation
        # in the person side and saves both entities
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        address = mocks.Address()
        address.object_id = 2
        address.street = "street_address"
        address.door = 1
        address.country = "country_address"
        person.address = address

        # removes a series of attributes so that is possible to test
        # the nullification process on them
        delattr(person, "name")
        delattr(address, "country")

        # runs the nullify process on the person in a non recursive
        # fashion (no relations are affected) then verifies that the
        # unset attributes in the person and address are none (not set)
        person.nullify(recursive=False)
        self.assertEqual(person.name, None)
        self.assertEqual(address.country, None)

        # creates the the person and address entities and populates
        # them with some values, then sets the address relation
        # in the person side and saves both entities
        person = mocks.Person()
        person.object_id = 3
        person.name = "name_person"
        address = mocks.Address()
        address.object_id = 4
        address.street = "street_address"
        address.door = 1
        address.country = "country_address"
        person.address = address

        # removes a series of attributes so that is possible to test
        # the nullification process on them
        delattr(person, "name")
        delattr(address, "country")

        # runs the nullify process on the person in a recursive
        # fashion (relations are affected) then verifies that the
        # unset attributes in the person and the ones in the address
        # are set to none
        person.nullify(recursive=True)
        self.assertEqual(person.name, None)
        self.assertEqual(address.country, None)

    def test_sort_to_many(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Dog)

        # creates the base person that is going to have the various
        # dogs associated for the sort of to many relations test
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # creates the complete range of dogs that are going to be used
        # in the sorting test, note that they are associated with the
        # previously created person (all of them)
        dog_a = mocks.Dog()
        dog_a.object_id = 2
        dog_a.name = "name_dog_a"
        dog_a.owner = person
        dog_b = mocks.Dog()
        dog_b.object_id = 3
        dog_b.name = "name_dog_b"
        dog_b.owner = person
        dog_c = mocks.Dog()
        dog_c.object_id = 4
        dog_c.name = "name_dog_c"
        dog_c.owner = person
        self.entity_manager.save(dog_a)
        self.entity_manager.save(dog_b)
        self.entity_manager.save(dog_c)

        # retrieves the person that was created from the data source, using
        # no ordering in the relations (default ordering should apply)
        person = self.entity_manager.get(mocks.Person, 1)

        # verifies that the retrieval was a success and that the dogs are
        # correctly sorted using the default sorting (identifier ascending)
        self.assertNotEqual(person, None)
        self.assertNotEqual(person.dogs, [])
        self.assertEqual(person.dogs[0].object_id, 2)
        self.assertEqual(person.dogs[1].object_id, 3)
        self.assertEqual(person.dogs[2].object_id, 4)

        # re-retrieves the person from the data source, sorting the dogs
        # relation using the name in a descending order
        person = self.entity_manager.get(
            mocks.Person,
            1,
            options=dict(eager=("dogs",), order_by=(("dogs.name", "descending"),)),
        )

        # verifies that the retrieval was a success and that the dogs are now
        # sorted in the opposite order, when compared with the first retrieval
        self.assertNotEqual(person, None)
        self.assertNotEqual(person.dogs, [])
        self.assertEqual(person.dogs[0].object_id, 4)
        self.assertEqual(person.dogs[1].object_id, 3)
        self.assertEqual(person.dogs[2].object_id, 2)

        # re-retrieves the person from the data source, sorting the dogs
        # relation using the name in a descending order, now using the simplified
        person = self.entity_manager.get(
            mocks.Person,
            1,
            options=dict(eager=("dogs",), order_by=(("dogs.name", "desc"),)),
        )

        # verifies that the retrieval was a success and that the dogs are now
        # sorted in the opposite order, when compared with the first retrieval
        self.assertNotEqual(person, None)
        self.assertNotEqual(person.dogs, [])
        self.assertEqual(person.dogs[0].object_id, 4)
        self.assertEqual(person.dogs[1].object_id, 3)
        self.assertEqual(person.dogs[2].object_id, 2)

    def test_decimal(self):
        # makes sure that the proper entity classes are registered
        # and created in the data source (going to be used)
        self.entity_manager.create(mocks.Person)

        # creates a person entity with the proper weight value set to
        # a complicated float value (extra decimal places)
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        person.weight = 88.151 - 88.15

        # verifies that no exact decimal value exists for the weight value
        # and that it's currently being represented by a float type
        self.assertNotEqual(person.weight, 0.001)
        self.assertEqual(type(person.weight), float)

        # converts the person's weight value to a decimal value (required to
        # be able to pass strict validation) and then saves the entity
        person.weight = colony.Decimal(person.weight)
        self.entity_manager.save(person)

        # tries to retrieve the person from the data source and verifies that
        # the weight value is now an "exact" (fixed point) value and that proper
        # comparisons are permitted/allowed by the "new" data type
        person = self.entity_manager.get(mocks.Person, 1)
        self.assertEqual(person.weight, 0.001)
        self.assertEqual(type(person.weight), colony.Decimal)

    def test_normalize_options(self):
        # creates a simple filter for name base selection and runs
        # the normalization process, creating the full complex based
        # filtering structure and verifies the result
        result = self.entity_manager.normalize_options(dict(name="person_a"))
        self.assertEqual(
            result,
            dict(
                _normalized=True,
                filters=(
                    dict(
                        type="equals",
                        fields=[
                            dict(name="name", value="person_a"),
                        ],
                    ),
                ),
            ),
        )

        # normalizes the options map of a find operation that
        # orders the enemies of the associated dogs meaning that
        # order by propagation will occur and then verifies that
        # the result is normalized and valid
        result = self.entity_manager.normalize_options(
            dict(
                eager=dict(dogs=dict(eager=("enemies",))),
                order_by=(("dogs.enemies.name", "descending"),),
            )
        )
        self.assertEqual(
            result,
            dict(
                _normalized=True,
                eager=dict(
                    dogs=dict(
                        _normalized=True,
                        eager=dict(enemies=dict(order_by=(("name", "descending"),))),
                    )
                ),
                order_by=(("dogs.enemies.name", "descending"),),
            ),
        )

    def test_get_nonexistent(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # tries to retrieve a person that does not exist in the
        # data source and verifies that the result is none
        person = self.entity_manager.get(mocks.Person, 999)
        self.assertEqual(person, None)

    def test_find_empty(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # retrieves all persons from an empty table and verifies
        # that the result is an empty list
        persons = self.entity_manager.find(mocks.Person)
        self.assertEqual(persons, [])

        # counts the persons and verifies the count is zero
        count = self.entity_manager.count(mocks.Person)
        self.assertEqual(count, 0)

    def test_find_filters(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a series of person entities with different attributes
        person_a = mocks.Person()
        person_a.object_id = 1
        person_a.name = "name_person_a"
        person_a.age = 20
        person_b = mocks.Person()
        person_b.object_id = 2
        person_b.name = "name_person_b"
        person_b.age = 30
        person_c = mocks.Person()
        person_c.object_id = 3
        person_c.name = "name_person_c"
        person_c.age = 40
        self.entity_manager.save(person_a)
        self.entity_manager.save(person_b)
        self.entity_manager.save(person_c)

        # retrieves persons using an equals filter on name
        persons = self.entity_manager.find(
            mocks.Person,
            dict(
                filters=[
                    dict(
                        type="equals",
                        fields=[dict(name="name", value="name_person_b")],
                    )
                ]
            ),
        )
        self.assertEqual(len(persons), 1)
        self.assertEqual(persons[0].object_id, 2)

        # retrieves persons using a greater than filter on age
        persons = self.entity_manager.find(
            mocks.Person,
            dict(filters=[dict(type="greater", fields=[dict(name="age", value=25)])]),
        )
        self.assertEqual(len(persons), 2)

        # retrieves persons using a lesser filter on age
        persons = self.entity_manager.find(
            mocks.Person,
            dict(filters=[dict(type="lesser", fields=[dict(name="age", value=25)])]),
        )
        self.assertEqual(len(persons), 1)
        self.assertEqual(persons[0].object_id, 1)

        # retrieves persons using multiple combined filters
        persons = self.entity_manager.find(
            mocks.Person,
            dict(
                filters=[
                    dict(
                        type="greater",
                        fields=[dict(name="age", value=15)],
                    ),
                    dict(
                        type="lesser",
                        fields=[dict(name="age", value=35)],
                    ),
                ]
            ),
        )
        self.assertEqual(len(persons), 2)

    def test_count_with_filters(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a series of person entities with different ages
        for i in range(1, 6):
            person = mocks.Person()
            person.object_id = i
            person.name = "name_person_%d" % i
            person.age = i * 10
            self.entity_manager.save(person)

        # counts all persons
        count = self.entity_manager.count(mocks.Person)
        self.assertEqual(count, 5)

        # counts persons with a filter on age
        count = self.entity_manager.count(
            mocks.Person,
            dict(
                filters=[
                    dict(
                        type="greater",
                        fields=[dict(name="age", value=25)],
                    )
                ]
            ),
        )
        self.assertEqual(count, 3)

    def test_update_nullify_field(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a person with a name and age set and saves it
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        person.age = 30
        self.entity_manager.save(person)

        # updates the person setting the age to none (null)
        person.age = None
        self.entity_manager.update(person)

        # retrieves the updated person and verifies that the
        # age field has been set to none
        saved_person = self.entity_manager.get(mocks.Person, 1)
        self.assertNotEqual(saved_person, None)
        self.assertEqual(saved_person.name, "name_person")
        self.assertEqual(saved_person.age, None)

    def test_update_relation_change(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Dog)

        # creates two persons and a dog, initially owned by person_a
        person_a = mocks.Person()
        person_a.object_id = 1
        person_a.name = "person_a"
        person_b = mocks.Person()
        person_b.object_id = 2
        person_b.name = "person_b"
        dog = mocks.Dog()
        dog.object_id = 3
        dog.name = "name_dog"
        dog.owner = person_a
        self.entity_manager.save(person_a)
        self.entity_manager.save(person_b)
        self.entity_manager.save(dog)

        # verifies the initial relation
        saved_dog = self.entity_manager.get(mocks.Dog, 3)
        self.assertEqual(saved_dog.owner.object_id, 1)

        # updates the dog's owner to person_b
        dog.owner = person_b
        self.entity_manager.update(dog)

        # retrieves the dog and verifies the owner has changed
        saved_dog = self.entity_manager.get(mocks.Dog, 3)
        self.assertEqual(saved_dog.owner.object_id, 2)

        # verifies that person_b now has the dog and person_a doesn't
        saved_person_b = self.entity_manager.get(mocks.Person, 2)
        self.assertNotEqual(saved_person_b.dogs, [])
        self.assertEqual(saved_person_b.dogs[0].object_id, 3)
        saved_person_a = self.entity_manager.get(mocks.Person, 1)
        self.assertEqual(saved_person_a.dogs, [])

    def test_update_nullify_relation(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Dog)

        # creates a person and a dog with an owner relation
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        dog = mocks.Dog()
        dog.object_id = 2
        dog.name = "name_dog"
        dog.owner = person
        self.entity_manager.save(person)
        self.entity_manager.save(dog)

        # verifies the initial relation is set
        saved_dog = self.entity_manager.get(mocks.Dog, 2)
        self.assertNotEqual(saved_dog.owner, None)

        # nullifies the owner relation and updates
        dog.owner = None
        self.entity_manager.update(dog)

        # retrieves the dog and verifies the relation has been removed
        saved_dog = self.entity_manager.get(mocks.Dog, 2)
        self.assertEqual(saved_dog.owner, None)

        # verifies that the person no longer has the dog
        saved_person = self.entity_manager.get(mocks.Person, 1)
        self.assertEqual(saved_person.dogs, [])

    def test_multiple_inheritance(self):
        # creates the required entity classes in the data source
        # to test the Employee class which inherits from Person,
        # Loggable, and Taxable (multiple inheritance)
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Employee)

        # creates an employee entity with fields from all parent
        # classes and saves it into the data source
        employee = mocks.Employee()
        employee.object_id = 1
        employee.name = "name_employee"
        employee.age = 30
        employee.salary = 500
        employee.tax_number = 12345
        self.entity_manager.save(employee)

        # retrieves the employee and verifies that all fields from
        # all parent classes are correctly persisted
        saved_employee = self.entity_manager.get(mocks.Employee, 1)
        self.assertNotEqual(saved_employee, None)
        self.assertEqual(saved_employee.object_id, 1)
        self.assertEqual(saved_employee.name, "name_employee")
        self.assertEqual(saved_employee.age, 30)
        self.assertEqual(saved_employee.salary, 500)
        self.assertEqual(saved_employee.tax_number, 12345)
        self.assertEqual(saved_employee.status, 1)

    def test_polymorphism_employee(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Employee)

        # creates an employee and a regular person and saves them
        person = mocks.Person()
        person.object_id = 1
        person.name = "regular_person"
        employee = mocks.Employee()
        employee.object_id = 2
        employee.name = "employee_person"
        employee.salary = 500
        self.entity_manager.save(person)
        self.entity_manager.save(employee)

        # queries using the parent class (Person) to retrieve both
        # the person and the employee
        all_persons = self.entity_manager.find(mocks.Person)
        self.assertEqual(len(all_persons), 2)

        # queries using the RootEntity to retrieve both entities
        all_roots = self.entity_manager.find(mocks.RootEntity)
        self.assertEqual(len(all_roots), 2)

        # queries using Employee to retrieve only the employee
        all_employees = self.entity_manager.find(mocks.Employee)
        self.assertEqual(len(all_employees), 1)
        self.assertEqual(all_employees[0].name, "employee_person")
        self.assertEqual(all_employees[0].salary, 500)

    def test_save_update_remove_cycle(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a person entity and saves it
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        person.age = 25
        self.entity_manager.save(person)

        # verifies the initial state
        saved = self.entity_manager.get(mocks.Person, 1)
        self.assertEqual(saved.name, "name_person")
        self.assertEqual(saved.age, 25)

        # updates the person entity multiple times
        person.name = "updated_1"
        self.entity_manager.update(person)
        person.name = "updated_2"
        self.entity_manager.update(person)
        person.name = "updated_3"
        self.entity_manager.update(person)

        # verifies that only the last update is persisted
        saved = self.entity_manager.get(mocks.Person, 1)
        self.assertEqual(saved.name, "updated_3")
        self.assertEqual(saved.age, 25)

        # removes the entity
        self.entity_manager.remove(person)
        saved = self.entity_manager.get(mocks.Person, 1)
        self.assertEqual(saved, None)

        # verifies that saving a new entity with the same id
        # works after the previous one was removed
        person_new = mocks.Person()
        person_new.object_id = 1
        person_new.name = "new_person"
        self.entity_manager.save(person_new)
        saved = self.entity_manager.get(mocks.Person, 1)
        self.assertNotEqual(saved, None)
        self.assertEqual(saved.name, "new_person")

    def test_file_data_type(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.File)

        # creates a file entity with binary/text data and saves it
        file = mocks.File()
        file.object_id = 1
        file.filename = "test_file.txt"
        file.data = "Hello World - data content"
        self.entity_manager.save(file)

        # retrieves the file and verifies the data field is
        # correctly persisted and retrieved
        saved_file = self.entity_manager.get(mocks.File, 1)
        self.assertNotEqual(saved_file, None)
        self.assertEqual(saved_file.filename, "test_file.txt")
        self.assertEqual(saved_file.data, "Hello World - data content")

    def test_unicode_fields(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a person with unicode characters in the name
        person = mocks.Person()
        person.object_id = 1
        person.name = colony.legacy.u("José Магалхес 学生")
        self.entity_manager.save(person)

        # retrieves the person and verifies the unicode name is
        # correctly persisted and retrieved
        saved_person = self.entity_manager.get(mocks.Person, 1)
        self.assertNotEqual(saved_person, None)
        self.assertEqual(saved_person.name, colony.legacy.u("José Магалхес 学生"))

    def test_find_with_set(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)

        # creates a person entity and saves it
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        person.age = 30
        self.entity_manager.save(person)

        # retrieves the person using the set option to get raw
        # result set with headers instead of entity instances
        result = self.entity_manager.find(mocks.Person, dict(set=True))
        self.assertNotEqual(result, None)

        # verifies that the result set contains data
        data = result.data()
        self.assertEqual(len(data), 1)

        # verifies that the header contains the expected field names
        header = result.header()
        self.assertTrue("name" in header)
        self.assertTrue("object_id" in header)

    def test_breeder_subclass(self):
        # creates the required entity classes in the data source
        # to test the Breeder (subclass of Person) and BreedDog
        # (subclass of Dog) specialized relation overriding
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Dog)
        self.entity_manager.create(mocks.Breeder)
        self.entity_manager.create(mocks.BreedDog)

        # creates a breeder with a license number and saves it
        breeder = mocks.Breeder()
        breeder.object_id = 1
        breeder.name = "breeder_person"
        breeder.license_number = "LIC-12345"
        self.entity_manager.save(breeder)

        # creates a breed dog associated with the breeder
        breed_dog = mocks.BreedDog()
        breed_dog.object_id = 2
        breed_dog.name = "breed_dog"
        breed_dog.digital_tag = "TAG-9876"
        breed_dog.owner = breeder
        self.entity_manager.save(breed_dog)

        # retrieves the breeder and verifies it is correct
        saved_breeder = self.entity_manager.get(mocks.Breeder, 1)
        self.assertNotEqual(saved_breeder, None)
        self.assertEqual(saved_breeder.license_number, "LIC-12345")

        # retrieves the breed dog and verifies the relation
        saved_dog = self.entity_manager.get(mocks.BreedDog, 2)
        self.assertNotEqual(saved_dog, None)
        self.assertEqual(saved_dog.digital_tag, "TAG-9876")
        self.assertNotEqual(saved_dog.owner, None)
        self.assertEqual(saved_dog.owner.object_id, breeder.object_id)

    def test_remove_with_relations(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Dog)

        # creates a person with two dogs (mapped relations)
        person = mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        dog_a = mocks.Dog()
        dog_a.object_id = 2
        dog_a.name = "dog_a"
        dog_a.owner = person
        dog_b = mocks.Dog()
        dog_b.object_id = 3
        dog_b.name = "dog_b"
        dog_b.owner = person
        self.entity_manager.save(person)
        self.entity_manager.save(dog_a)
        self.entity_manager.save(dog_b)

        # verifies the person has two dogs
        saved_person = self.entity_manager.get(mocks.Person, 1)
        self.assertEqual(len(saved_person.dogs), 2)

        # removes one of the dogs and verifies the person now
        # has only one dog
        self.entity_manager.remove(dog_a)
        saved_person = self.entity_manager.get(mocks.Person, 1)
        self.assertEqual(len(saved_person.dogs), 1)
        self.assertEqual(saved_person.dogs[0].object_id, 3)


class EntityManagerConcreteTableTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Entity Manager Concrete Table test case"

    def test_get_all_items(self):
        # verifies that get_all_items returns all inherited items
        # for a concrete table entity class
        items = mocks.ConcretePerson.get_all_items()
        self.assertTrue("object_id" in items)
        self.assertTrue("status" in items)
        self.assertTrue("name" in items)
        self.assertTrue("age" in items)
        self.assertTrue("weight" in items)

        # verifies that employee includes all items from the
        # complete hierarchy
        items = mocks.ConcreteEmployee.get_all_items()
        self.assertTrue("object_id" in items)
        self.assertTrue("status" in items)
        self.assertTrue("name" in items)
        self.assertTrue("age" in items)
        self.assertTrue("salary" in items)

        # verifies that the root entity only has its own items
        items = mocks.ConcreteRootEntity.get_all_items()
        self.assertTrue("object_id" in items)
        self.assertTrue("status" in items)
        self.assertFalse("name" in items)
        self.assertFalse("salary" in items)

    def test_get_all_items_foreign_relations(self):
        # retrieves the items without the foreign relations and verifies
        # that only the mapped relations are present, the "to-many"
        # relations are mapped by the other side of the relation and so
        # they should not originate a column in the entity's table
        items = mocks.ConcretePerson.get_all_items()
        self.assertTrue("parent" in items)
        self.assertTrue("address" in items)
        self.assertFalse("children" in items)
        self.assertFalse("employees" in items)

        # retrieves the items with the foreign relations enabled and
        # verifies that the non mapped relations are now included
        items = mocks.ConcretePerson.get_all_items(foreign_relations=True)
        self.assertTrue("parent" in items)
        self.assertTrue("children" in items)
        self.assertTrue("employees" in items)

        # verifies that the two variants are cached independently, so
        # that a retrieval of one does not "poison" the other
        self.assertFalse(
            "children" in mocks.ConcretePerson.get_all_items(),
        )

    def test_get_all_items_abstract_parent(self):
        # verifies that the items declared in an abstract parent are
        # flattened into the first concrete class of the hierarchy,
        # as no table exists for the abstract class to hold them
        items = mocks.ConcreteAbstractPerson.get_all_items()
        self.assertTrue("object_id" in items)
        self.assertTrue("status" in items)
        self.assertTrue("name" in items)
        self.assertTrue("age" in items)
        self.assertFalse("salary" in items)

        # verifies that the second concrete level also carries the
        # complete set of items down from the abstract root
        items = mocks.ConcreteAbstractEmployee.get_all_items()
        self.assertTrue("object_id" in items)
        self.assertTrue("status" in items)
        self.assertTrue("name" in items)
        self.assertTrue("salary" in items)

        # verifies that an abstract class still reports its own items
        # so that they may be inherited by the concrete descendants
        items = mocks.ConcreteAbstract.get_all_items()
        self.assertTrue("object_id" in items)
        self.assertTrue("status" in items)

    def test_get_all_indexed(self):
        # verifies that a concrete table entity class reports the items
        # declared at its own level as meant to be indexed
        self.assertEqual(mocks.ConcretePerson.get_all_indexed(), ["name"])

        # verifies that a descendant of it also reports the inherited
        # item, as the column is flattened into its own table and so it
        # has to be indexed there as well
        self.assertEqual(mocks.ConcreteEmployee.get_all_indexed(), ["name"])

        # verifies that the "native" (non flattened) retrieval keeps
        # reporting only the items declared at the level of the class
        # itself, so that both of the retrievals remain independent
        self.assertEqual(mocks.ConcretePerson.get_indexed(), ["name"])
        self.assertEqual(mocks.ConcreteEmployee.get_indexed(), [])

        # verifies that a class whose hierarchy declares no indexed
        # items reports an empty set of items
        self.assertEqual(mocks.ConcreteAddress.get_all_indexed(), [])

    def test_get_all_indexed_cache(self):
        # retrieves the indexed items twice and verifies that the very
        # same list is returned, meaning that the resolution is cached
        # instead of being rebuilt on every retrieval
        indexed = mocks.ConcreteEmployee.get_all_indexed()
        self.assertTrue(indexed is mocks.ConcreteEmployee.get_all_indexed())

        # verifies that the cache is stored in the class itself, so that
        # the levels of the hierarchy do not shadow each other
        self.assertTrue("_all_indexed" in mocks.ConcreteEmployee.__dict__)

        # verifies that the cache attribute is not mistaken for a field
        # of the entity, which would create a spurious column
        self.assertFalse("_all_indexed" in mocks.ConcreteEmployee.get_names())
        self.assertFalse("_all_indexed" in mocks.ConcreteEmployee.get_all_items())

    def test_get_cls_tables(self):
        # verifies that for the concrete table strategy the tables that
        # hold a copy of an inherited column are the ones of every non
        # abstract level from the declaring class down to the current one
        self.assertEqual(
            mocks.ConcreteEmployee.get_cls_tables("name"),
            ["_concrete_person", "_concrete_employee"],
        )
        self.assertEqual(
            mocks.ConcreteEmployee.get_cls_tables("status"),
            ["_concrete_root_entity", "_concrete_person", "_concrete_employee"],
        )

        # verifies that a column declared by the current class only
        # exists in the table of the class itself
        self.assertEqual(
            mocks.ConcreteEmployee.get_cls_tables("salary"),
            ["_concrete_employee"],
        )

        # verifies that the levels above the declaring class are not
        # included, as their tables do not hold the column
        self.assertEqual(
            mocks.ConcretePerson.get_cls_tables("name"), ["_concrete_person"]
        )

        # verifies that the abstract levels of the hierarchy are skipped,
        # as they have no associated table
        self.assertEqual(
            mocks.ConcreteAbstractEmployee.get_cls_tables("status"),
            ["_concrete_abstract_person", "_concrete_abstract_employee"],
        )

        # verifies that for the class table strategy only the table of
        # the declaring class holds the column
        self.assertEqual(mocks.Employee.get_cls_tables("name"), ["_person"])
        self.assertEqual(mocks.Employee.get_cls_tables("salary"), ["_employee"])

        # verifies that an unknown name resolves to no table at all
        self.assertEqual(mocks.ConcreteEmployee.get_cls_tables("not_a_column"), [])
        self.assertEqual(mocks.Employee.get_cls_tables("not_a_column"), [])

    def test_strategy_selector(self):
        # verifies that the inheritance strategy is correctly resolved
        # for the concrete table hierarchy
        self.assertEqual(
            mocks.ConcreteRootEntity.get_inheritance_strategy(), "concrete_table"
        )
        self.assertEqual(
            mocks.ConcretePerson.get_inheritance_strategy(), "concrete_table"
        )
        self.assertEqual(
            mocks.ConcreteEmployee.get_inheritance_strategy(), "concrete_table"
        )

        # verifies the is_concrete_table helper method
        self.assertTrue(mocks.ConcreteRootEntity.is_concrete_table())
        self.assertTrue(mocks.ConcretePerson.is_concrete_table())
        self.assertTrue(mocks.ConcreteEmployee.is_concrete_table())

        # verifies that the existing class table entities are
        # not affected by the new strategy
        self.assertEqual(mocks.RootEntity.get_inheritance_strategy(), "class_table")
        self.assertEqual(mocks.Person.get_inheritance_strategy(), "class_table")
        self.assertFalse(mocks.RootEntity.is_concrete_table())
        self.assertFalse(mocks.Person.is_concrete_table())

    def test_strategy_selector_deep(self):
        # verifies that the strategy is resolved through a hierarchy
        # where only the root class declares the inheritance attribute,
        # the intermediate and leaf classes must inherit it
        self.assertFalse("inheritance" in mocks.ConcretePerson.__dict__)
        self.assertFalse("inheritance" in mocks.ConcreteEmployee.__dict__)
        self.assertEqual(
            mocks.ConcreteEmployee.get_inheritance_strategy(), "concrete_table"
        )

        # verifies the same resolution for a hierarchy whose root is
        # an abstract class declaring the strategy
        self.assertEqual(
            mocks.ConcreteAbstract.get_inheritance_strategy(), "concrete_table"
        )
        self.assertEqual(
            mocks.ConcreteAbstractEmployee.get_inheritance_strategy(),
            "concrete_table",
        )
        self.assertTrue(mocks.ConcreteAbstractEmployee.is_concrete_table())

        # verifies that a sibling hierarchy that does not declare the
        # attribute is not affected and keeps the default strategy
        self.assertEqual(mocks.Employee.get_inheritance_strategy(), "class_table")
        self.assertFalse(mocks.Employee.is_concrete_table())

    def test_global_inheritance_override(self):
        # verifies that the DATA_INHERITANCE global config value
        # overrides the class-level inheritance attribute, allowing
        # a system-wide switch without changing entity code, note
        # that no cache clearing is performed as the override is
        # expected to be resolved on every strategy retrieval

        # resolves the strategy for both hierarchies before the
        # override is set, so that the per class cache is populated
        # and the override is verified to take precedence over it
        self.assertEqual(mocks.RootEntity.get_inheritance_strategy(), "class_table")
        self.assertEqual(
            mocks.ConcreteRootEntity.get_inheritance_strategy(), "concrete_table"
        )

        # saves the original value for restoration
        original = structures.DATA_INHERITANCE

        try:
            structures.DATA_INHERITANCE = "concrete_table"

            # verifies that a class_table entity now reports
            # concrete_table due to the global override
            self.assertEqual(
                mocks.RootEntity.get_inheritance_strategy(), "concrete_table"
            )
            self.assertTrue(mocks.RootEntity.is_concrete_table())

            structures.DATA_INHERITANCE = "class_table"

            # verifies that concrete_table entities now report
            # class_table due to the global override
            self.assertEqual(
                mocks.ConcreteRootEntity.get_inheritance_strategy(), "class_table"
            )
            self.assertFalse(mocks.ConcreteRootEntity.is_concrete_table())

            structures.DATA_INHERITANCE = None

            # verifies that removing the override restores the
            # class-level attribute resolution for both hierarchies
            self.assertEqual(mocks.RootEntity.get_inheritance_strategy(), "class_table")
            self.assertEqual(
                mocks.ConcreteRootEntity.get_inheritance_strategy(), "concrete_table"
            )
        finally:
            # restores the original value to avoid affecting
            # other tests in the suite
            structures.DATA_INHERITANCE = original

    def test_global_inheritance_override_conf(self):
        # verifies that the DATA_INHERITANCE configuration value is
        # honoured as the documented (environment variable) way of
        # setting the global override, taking precedence over the
        # module level fallback value
        try:
            colony.conf_s("DATA_INHERITANCE", "concrete_table")

            self.assertEqual(
                mocks.RootEntity.get_inheritance_strategy(), "concrete_table"
            )
            self.assertTrue(mocks.Person.is_concrete_table())

            colony.conf_s("DATA_INHERITANCE", "class_table")

            self.assertEqual(
                mocks.ConcreteRootEntity.get_inheritance_strategy(), "class_table"
            )
            self.assertFalse(mocks.ConcretePerson.is_concrete_table())
        finally:
            # removes the configuration value to avoid affecting
            # other tests in the suite
            colony.conf_r("DATA_INHERITANCE")

        # verifies that the strategy resolution is restored once the
        # configuration value has been removed
        self.assertEqual(mocks.RootEntity.get_inheritance_strategy(), "class_table")
        self.assertEqual(
            mocks.ConcreteRootEntity.get_inheritance_strategy(), "concrete_table"
        )

    def test_create(self):
        # creates the concrete table entities and verifies that the
        # data source references have been created successfully
        self.entity_manager.create(mocks.ConcreteRootEntity)
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)
        self.entity_manager.create(mocks.ConcreteAddress)

        # verifies that all the data source references for the entity
        # classes have been created successfully
        self.assertTrue(self.entity_manager.exists(mocks.ConcreteRootEntity))
        self.assertTrue(self.entity_manager.exists(mocks.ConcretePerson))
        self.assertTrue(self.entity_manager.exists(mocks.ConcreteEmployee))
        self.assertTrue(self.entity_manager.exists(mocks.ConcreteAddress))

    def test_create_abstract_parent(self):
        # creates the entity classes of a hierarchy whose root is
        # abstract, no table should be created for the abstract class
        self.entity_manager.create(mocks.ConcreteAbstractPerson)
        self.entity_manager.create(mocks.ConcreteAbstractEmployee)

        # verifies that the concrete classes have a definition in the
        # data source while the abstract root does not (it has no table)
        self.assertTrue(
            self.entity_manager.has_definition(mocks.ConcreteAbstractPerson)
        )
        self.assertTrue(
            self.entity_manager.has_definition(mocks.ConcreteAbstractEmployee)
        )
        self.assertFalse(self.entity_manager.has_definition(mocks.ConcreteAbstract))

    def test_index_fields(self):
        # creates the entity classes of a concrete table hierarchy in
        # the data source, the indexes of the fields declared as indexed
        # are created as part of the operation
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)

        # verifies that the indexed field is indexed both in the table
        # of the class that declares it and in the one of the descendant
        # class, as the column is flattened into both of them
        self.assertTrue(self._has_index("_concrete_person_name_hash"))
        self.assertTrue(self._has_index("_concrete_employee_name_hash"))

        # creates the entity classes of a class table hierarchy and
        # verifies that the indexed field is only indexed in the table
        # of the class that declares it, the descendant shares the row
        # of the parent and so it holds no copy of the column
        self.entity_manager.create(mocks.Person)
        self.entity_manager.create(mocks.Employee)
        self.assertTrue(self._has_index("_person_name_hash"))
        self.assertFalse(self._has_index("_employee_name_hash"))

    def test_get_items_map(self):
        # retrieves the items map for a concrete table entity including
        # the ancestor levels, an entry should exist for each of the non
        # abstract classes of the hierarchy plus the entity class itself
        items_map = self.entity_manager._get_items_map(mocks.ConcreteEmployee)
        classes = list(items_map)
        self.assertTrue(mocks.ConcreteRootEntity in classes)
        self.assertTrue(mocks.ConcretePerson in classes)
        self.assertTrue(mocks.ConcreteEmployee in classes)

        # verifies that each entry contains the items flattened down to
        # the associated hierarchy level (and not the complete set)
        self.assertFalse("name" in items_map[mocks.ConcreteRootEntity])
        self.assertTrue("name" in items_map[mocks.ConcretePerson])
        self.assertFalse("salary" in items_map[mocks.ConcretePerson])
        self.assertTrue("salary" in items_map[mocks.ConcreteEmployee])

        # retrieves the items map without the ancestor levels and
        # verifies that only the entity class entry is present
        items_map = self.entity_manager._get_items_map(
            mocks.ConcreteEmployee, ancestors=False
        )
        self.assertEqual(list(items_map), [mocks.ConcreteEmployee])
        self.assertTrue("salary" in items_map[mocks.ConcreteEmployee])
        self.assertTrue("name" in items_map[mocks.ConcreteEmployee])

        # verifies that the abstract classes of the hierarchy are not
        # included in the map as they have no associated table
        items_map = self.entity_manager._get_items_map(mocks.ConcreteAbstractEmployee)
        self.assertFalse(mocks.ConcreteAbstract in list(items_map))
        self.assertEqual(
            list(items_map),
            [mocks.ConcreteAbstractPerson, mocks.ConcreteAbstractEmployee],
        )

        # verifies that a class table entity falls back to the "native"
        # items map, where each level only holds its own items
        items_map = self.entity_manager._get_items_map(mocks.Employee)
        self.assertEqual(items_map, mocks.Employee.get_items_map())

    def test_save(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)

        # creates the person entity that is going to be used
        # for the verification of the save method and saves it
        person = mocks.ConcretePerson()
        person.object_id = 1
        person.name = "name_person"
        person.age = 30
        self.entity_manager.save(person)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(person.object_id, 1)
        self.assertEqual(person.name, "name_person")
        self.assertEqual(person.age, 30)

        # retrieves the saved person by the unique identifier
        # of it and verifies that the object is not modified
        saved_person = self.entity_manager.get(mocks.ConcretePerson, 1)
        self.assertNotEqual(saved_person, None)

        # verifies that the entity values of the retrieved entity
        # are the same as the original entity, including the
        # inherited fields from the concrete root entity
        self.assertEqual(saved_person.object_id, person.object_id)
        self.assertEqual(saved_person.name, person.name)
        self.assertEqual(saved_person.age, person.age)
        self.assertEqual(saved_person.status, 1)

    def test_save_hierarchy(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)

        # creates an employee entity (child of person) and saves it,
        # the employee table should contain all inherited fields
        employee = mocks.ConcreteEmployee()
        employee.object_id = 1
        employee.name = "name_employee"
        employee.age = 28
        employee.salary = 500
        self.entity_manager.save(employee)

        # retrieves the saved employee by the unique identifier
        # and verifies all attributes including inherited ones
        saved_employee = self.entity_manager.get(mocks.ConcreteEmployee, 1)
        self.assertNotEqual(saved_employee, None)
        self.assertEqual(saved_employee.object_id, 1)
        self.assertEqual(saved_employee.name, "name_employee")
        self.assertEqual(saved_employee.age, 28)
        self.assertEqual(saved_employee.salary, 500)
        self.assertEqual(saved_employee.status, 1)

    def test_save_abstract_parent(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcreteAbstractPerson)
        self.entity_manager.create(mocks.ConcreteAbstractEmployee)

        # creates and saves an employee of a hierarchy whose root is
        # abstract, the abstract level must be skipped in the write
        employee = mocks.ConcreteAbstractEmployee()
        employee.object_id = 1
        employee.name = "abstract_employee"
        employee.age = 33
        employee.salary = 750
        self.entity_manager.save(employee)

        # verifies that the entity is retrievable from both of the
        # concrete levels of the hierarchy
        saved_employee = self.entity_manager.get(mocks.ConcreteAbstractEmployee, 1)
        self.assertNotEqual(saved_employee, None)
        self.assertEqual(saved_employee.name, "abstract_employee")
        self.assertEqual(saved_employee.salary, 750)

        saved_person = self.entity_manager.get(mocks.ConcreteAbstractPerson, 1)
        self.assertNotEqual(saved_person, None)
        self.assertEqual(saved_person.name, "abstract_employee")
        self.assertEqual(saved_person.age, 33)

    def test_update(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)

        # creates the person entity and saves it
        person = mocks.ConcretePerson()
        person.object_id = 1
        person.name = "name_person"
        person.age = 30
        self.entity_manager.save(person)

        # updates the person entity with new values
        person.name = "updated_name"
        person.age = 31
        self.entity_manager.update(person)

        # retrieves the updated person and verifies the changes
        saved_person = self.entity_manager.get(mocks.ConcretePerson, 1)
        self.assertNotEqual(saved_person, None)
        self.assertEqual(saved_person.name, "updated_name")
        self.assertEqual(saved_person.age, 31)
        self.assertEqual(saved_person.status, 1)

    def test_update_hierarchy(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)

        # creates an employee entity and saves it
        employee = mocks.ConcreteEmployee()
        employee.object_id = 1
        employee.name = "name_employee"
        employee.age = 28
        employee.salary = 500
        self.entity_manager.save(employee)

        # updates the employee entity with new values across
        # multiple hierarchy levels (inherited + own)
        employee.name = "updated_name"
        employee.salary = 600
        employee.status = 2
        self.entity_manager.update(employee)

        # retrieves the updated employee and verifies the changes
        saved_employee = self.entity_manager.get(mocks.ConcreteEmployee, 1)
        self.assertNotEqual(saved_employee, None)
        self.assertEqual(saved_employee.name, "updated_name")
        self.assertEqual(saved_employee.salary, 600)
        self.assertEqual(saved_employee.status, 2)

    def test_update_abstract_parent(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcreteAbstractPerson)
        self.entity_manager.create(mocks.ConcreteAbstractEmployee)

        # creates and saves an employee to be updated afterwards
        employee = mocks.ConcreteAbstractEmployee()
        employee.object_id = 1
        employee.name = "abstract_employee"
        employee.salary = 750
        self.entity_manager.save(employee)

        # updates a field inherited from the abstract root and one
        # declared in the leaf class, both must be persisted
        employee.name = "abstract_employee_changed"
        employee.salary = 900
        self.entity_manager.update(employee)

        # verifies that the update reached the leaf table
        saved_employee = self.entity_manager.get(mocks.ConcreteAbstractEmployee, 1)
        self.assertEqual(saved_employee.name, "abstract_employee_changed")
        self.assertEqual(saved_employee.salary, 900)

        # verifies that the update also reached the intermediate table,
        # as the concrete table strategy duplicates the inherited fields
        saved_person = self.entity_manager.get(mocks.ConcreteAbstractPerson, 1)
        self.assertEqual(saved_person.name, "abstract_employee_changed")

    def test_delete(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)

        # creates the person entity and saves it
        person = mocks.ConcretePerson()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # verifies the person exists
        saved_person = self.entity_manager.get(mocks.ConcretePerson, 1)
        self.assertNotEqual(saved_person, None)

        # removes the person entity and verifies it no longer exists
        self.entity_manager.remove(person)
        saved_person = self.entity_manager.get(mocks.ConcretePerson, 1)
        self.assertEqual(saved_person, None)

    def test_delete_hierarchy(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)

        # creates an employee entity and saves it
        employee = mocks.ConcreteEmployee()
        employee.object_id = 1
        employee.name = "name_employee"
        employee.salary = 500
        self.entity_manager.save(employee)

        # removes the employee entity and verifies it no longer exists
        self.entity_manager.remove(employee)
        saved_employee = self.entity_manager.get(mocks.ConcreteEmployee, 1)
        self.assertEqual(saved_employee, None)

    def test_find(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)

        # creates multiple person entities and saves them
        person_a = mocks.ConcretePerson()
        person_a.object_id = 1
        person_a.name = "name_person_a"
        person_a.age = 30
        person_b = mocks.ConcretePerson()
        person_b.object_id = 2
        person_b.name = "name_person_b"
        person_b.age = 25
        self.entity_manager.save(person_a)
        self.entity_manager.save(person_b)

        # retrieves all persons and verifies the results
        persons = self.entity_manager.find(mocks.ConcretePerson)
        self.assertEqual(len(persons), 2)

        # retrieves persons with a filter on age
        persons = self.entity_manager.find(
            mocks.ConcretePerson,
            dict(
                filters=[
                    dict(
                        type="equals",
                        fields=[dict(name="age", value=30)],
                    )
                ]
            ),
        )
        self.assertEqual(len(persons), 1)
        self.assertEqual(persons[0].name, "name_person_a")

    def test_count(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)

        # creates one plain person and two employees, so that the
        # counts differ at each level of the hierarchy
        person = mocks.ConcretePerson()
        person.object_id = 1
        person.name = "counted_person"
        self.entity_manager.save(person)
        for index in range(2):
            employee = mocks.ConcreteEmployee()
            employee.object_id = index + 2
            employee.name = "counted_employee_%d" % index
            self.entity_manager.save(employee)

        # counts at each level of the hierarchy, the concrete table
        # strategy resolves the count as a single table scan with the
        # descendant entities present in every ancestor table
        self.assertEqual(self.entity_manager.count(mocks.ConcreteRootEntity), 3)
        self.assertEqual(self.entity_manager.count(mocks.ConcretePerson), 3)
        self.assertEqual(self.entity_manager.count(mocks.ConcreteEmployee), 2)

        # counts using a filter on an inherited field to verify that
        # the filtering is applied on the single table scan
        count = self.entity_manager.count(
            mocks.ConcreteEmployee,
            dict(
                filters=[
                    dict(
                        type="equals",
                        fields=[dict(name="name", value="counted_employee_0")],
                    )
                ]
            ),
        )
        self.assertEqual(count, 1)

    def test_polymorphic_query(self):
        # creates the required entity classes in the data source,
        # the concrete table strategy creates tables for all levels
        # in the hierarchy with flattened columns
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)

        # creates a person and an employee and saves them, this
        # should insert rows into all ancestor tables
        person = mocks.ConcretePerson()
        person.object_id = 1
        person.name = "regular_person"
        person.age = 25
        employee = mocks.ConcreteEmployee()
        employee.object_id = 2
        employee.name = "employee_person"
        employee.age = 30
        employee.salary = 500
        self.entity_manager.save(person)
        self.entity_manager.save(employee)

        # queries using the root entity class to retrieve all
        # entities in the hierarchy (polymorphic query), both
        # the person and the employee should appear
        all_roots = self.entity_manager.find(mocks.ConcreteRootEntity)
        self.assertEqual(len(all_roots), 2)

        # queries using the person class, the employee should
        # also appear since it has a row in the person table
        all_persons = self.entity_manager.find(mocks.ConcretePerson)
        self.assertEqual(len(all_persons), 2)

        # queries using the employee class, only the employee
        # should appear
        all_employees = self.entity_manager.find(mocks.ConcreteEmployee)
        self.assertEqual(len(all_employees), 1)
        self.assertEqual(all_employees[0].name, "employee_person")
        self.assertEqual(all_employees[0].salary, 500)

        # retrieves a specific entity by ID at the root level
        # and verifies the root-level fields are accessible
        root_entity = self.entity_manager.get(mocks.ConcreteRootEntity, 2)
        self.assertNotEqual(root_entity, None)
        self.assertEqual(root_entity.status, 1)

    def test_polymorphic_class_identity(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)

        # creates a plain person and an employee so that the parent
        # level table holds rows of two distinct concrete classes
        person = mocks.ConcretePerson()
        person.object_id = 1
        person.name = "plain_person"
        employee = mocks.ConcreteEmployee()
        employee.object_id = 2
        employee.name = "real_employee"
        employee.salary = 1500
        self.entity_manager.save(person)
        self.entity_manager.save(employee)

        # retrieves the entities through the parent class and indexes
        # them by identifier so that each one may be verified
        found = self.entity_manager.find(mocks.ConcretePerson)
        self.assertEqual(len(found), 2)
        found_map = dict((entity.object_id, entity) for entity in found)

        # verifies that the discriminator column of the parent table
        # is honoured, so that the entity read from the parent level
        # is built as the concrete class it was stored as
        self.assertEqual(found_map[1].__class__, mocks.ConcretePerson)
        self.assertEqual(found_map[2].__class__, mocks.ConcreteEmployee)
        self.assertTrue(isinstance(found_map[2], mocks.ConcreteEmployee))

        # verifies that a field declared only in the descendant class
        # is not loaded by the parent level read, as the parent table
        # does not contain a column for it
        self.assertFalse(found_map[2].has_value("salary"))
        self.assertTrue(found_map[2].has_value("name"))

        # verifies that accessing the non loaded field resolves it
        # lazily from the descendant table, instead of returning the
        # class level definition of the attribute
        self.assertEqual(found_map[2].salary, 1500)

        # verifies the same behaviour for a retrieval through the root
        # of the hierarchy, which holds none of the person fields
        root_entity = self.entity_manager.get(mocks.ConcreteRootEntity, 2)
        self.assertEqual(root_entity.__class__, mocks.ConcreteEmployee)
        self.assertFalse(root_entity.has_value("name"))
        self.assertEqual(root_entity.name, "real_employee")
        self.assertEqual(root_entity.salary, 1500)

    def test_get_descendant_tables(self):
        # retrieves the tables of a concrete table entity class that has
        # descendants, the column copies live in the table of the class
        # itself and in the ones of every class below it
        tables = self.entity_manager._get_descendant_tables(mocks.ConcretePerson)
        self.assertEqual(sorted(tables), ["_concrete_employee", "_concrete_person"])

        # retrieves the tables of a leaf class of the same hierarchy and
        # verifies that only its own table is reported, the levels above
        # it are not to be considered
        tables = self.entity_manager._get_descendant_tables(mocks.ConcreteEmployee)
        self.assertEqual(tables, ["_concrete_employee"])

        # retrieves the tables of the root of the hierarchy and verifies
        # that the complete set of descendants is reported, no matter the
        # depth at which they are declared
        tables = self.entity_manager._get_descendant_tables(mocks.ConcreteRootEntity)
        self.assertEqual(
            sorted(tables),
            [
                "_concrete_address",
                "_concrete_employee",
                "_concrete_person",
                "_concrete_root_entity",
            ],
        )

    def test_get_descendant_tables_abstract(self):
        # retrieves the tables of an abstract class of a concrete table
        # hierarchy and verifies that its own table is not reported, as
        # no representation of it exists in the data source
        tables = self.entity_manager._get_descendant_tables(mocks.ConcreteAbstract)
        self.assertEqual(
            sorted(tables),
            ["_concrete_abstract_employee", "_concrete_abstract_person"],
        )

    def test_get_descendant_tables_class_table(self):
        # retrieves the tables of a class table entity class that has
        # descendants and verifies that only its own table is reported,
        # the descendants share the row of their ancestors and so they
        # hold no copy of the columns
        tables = self.entity_manager._get_descendant_tables(mocks.Person)
        self.assertEqual(tables, ["_person"])

    def test_get_descendant_tables_unregistered(self):
        # removes one of the descendants from the entity manager so that
        # it becomes a class with no representation in the data source
        self.entity_manager.shrink(dict(ConcreteEmployee=mocks.ConcreteEmployee))

        # verifies that the unregistered descendant is not reported, as
        # writing to a table that does not exist would fail
        try:
            tables = self.entity_manager._get_descendant_tables(mocks.ConcretePerson)
            self.assertEqual(tables, ["_concrete_person"])
        finally:
            self.entity_manager.extend(dict(ConcreteEmployee=mocks.ConcreteEmployee))

        # verifies that the descendant is reported again once it has
        # been registered back in the entity manager
        tables = self.entity_manager._get_descendant_tables(mocks.ConcretePerson)
        self.assertEqual(sorted(tables), ["_concrete_employee", "_concrete_person"])

    def test_one_to_one(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteAddress)

        # creates the person and address entities and populates
        # them with some values, then sets the relation and saves
        person = mocks.ConcretePerson()
        person.object_id = 1
        person.name = "name_person"

        address = mocks.ConcreteAddress()
        address.object_id = 2
        address.street = "street_address"
        address.number = 100
        address.country = "country_address"

        person.address = address
        self.entity_manager.save(person)
        self.entity_manager.save(address)

        # retrieves both the person and address to verify the
        # relation is correctly persisted
        saved_person = self.entity_manager.get(
            mocks.ConcretePerson, 1, dict(eager=dict(address={}))
        )
        self.assertNotEqual(saved_person, None)
        self.assertNotEqual(saved_person.address, None)
        self.assertEqual(saved_person.address.object_id, address.object_id)
        self.assertEqual(saved_person.address.street, "street_address")

    def test_one_to_many(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)

        # creates a parent person and child persons
        parent = mocks.ConcretePerson()
        parent.object_id = 1
        parent.name = "parent_person"

        child_a = mocks.ConcretePerson()
        child_a.object_id = 2
        child_a.name = "child_a"
        child_a.parent = parent

        child_b = mocks.ConcretePerson()
        child_b.object_id = 3
        child_b.name = "child_b"
        child_b.parent = parent

        self.entity_manager.save(parent)
        self.entity_manager.save(child_a)
        self.entity_manager.save(child_b)

        # retrieves the parent and verifies the children relation
        saved_parent = self.entity_manager.get(
            mocks.ConcretePerson, 1, dict(eager=dict(children={}))
        )
        self.assertNotEqual(saved_parent, None)
        self.assertEqual(len(saved_parent.children), 2)

    def test_boss_relation(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)

        # creates the boss (a plain person) and two employees that
        # reference it through the mapped "boss" relation
        boss = mocks.ConcretePerson()
        boss.object_id = 1
        boss.name = "the_boss"
        self.entity_manager.save(boss)
        for index in range(2):
            employee = mocks.ConcreteEmployee()
            employee.object_id = index + 2
            employee.name = "employee_%d" % index
            employee.boss = boss
            self.entity_manager.save(employee)

        # verifies that the mapped side of the relation is correctly
        # persisted and retrieved for the concrete table strategy
        saved_employee = self.entity_manager.get(mocks.ConcreteEmployee, 2)
        self.assertNotEqual(saved_employee.boss, None)
        self.assertEqual(saved_employee.boss.object_id, boss.object_id)

        # verifies that the reverse side of the relation resolves to
        # the complete set of employees associated with the boss
        saved_boss = self.entity_manager.get(mocks.ConcretePerson, 1)
        self.assertEqual(len(saved_boss.employees), 2)

        # verifies that the reverse relation is declared consistently,
        # the reverse of the reverse must resolve back to the origin
        relation = mocks.ConcreteEmployee.get_relation("boss")
        target = relation.get("target")
        reverse = target.get_relation(relation.get("reverse"))
        self.assertEqual(reverse.get("reverse"), "boss")
        self.assertEqual(reverse.get("target"), mocks.ConcreteEmployee)

    def test_one_to_one_reverse(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)
        self.entity_manager.create(mocks.ConcreteAddress)

        # creates an employee and an address and sets the relation from
        # the address side, which is the non mapped (reverse) side of it
        # so that the foreign key has to be written into the tables of
        # the employee hierarchy instead of the address one
        employee = mocks.ConcreteEmployee()
        employee.object_id = 1
        employee.name = "reverse_employee"
        employee.salary = 400
        address = mocks.ConcreteAddress()
        address.object_id = 2
        address.street = "street_address"
        address.country = "country_address"
        address.person = employee
        self.entity_manager.save(employee)
        self.entity_manager.save(address)

        # verifies that both sides of the relation resolve correctly, the
        # employee level must see the address even though the relation is
        # declared (and mapped) by the person level of the hierarchy
        saved_employee = self.entity_manager.get(mocks.ConcreteEmployee, 1)
        self.assertNotEqual(saved_employee, None)
        self.assertNotEqual(saved_employee.address, None)
        self.assertEqual(saved_employee.address.object_id, address.object_id)

        saved_address = self.entity_manager.get(mocks.ConcreteAddress, 2)
        self.assertNotEqual(saved_address, None)
        self.assertNotEqual(saved_address.person, None)
        self.assertEqual(saved_address.person.object_id, employee.object_id)

        # verifies that the relation is also visible from the parent level
        # of the hierarchy, as the column is duplicated into every table
        saved_person = self.entity_manager.get(mocks.ConcretePerson, 1)
        self.assertNotEqual(saved_person, None)
        self.assertNotEqual(saved_person.address, None)
        self.assertEqual(saved_person.address.object_id, address.object_id)

        # re-assigns the relation to a second address and verifies that
        # the change is visible from every level of the hierarchy, so that
        # no stale copy of the foreign key is left behind
        other_address = mocks.ConcreteAddress()
        other_address.object_id = 3
        other_address.street = "other_street"
        other_address.person = employee
        self.entity_manager.save(other_address)

        saved_employee = self.entity_manager.get(mocks.ConcreteEmployee, 1)
        self.assertEqual(saved_employee.address.object_id, other_address.object_id)
        saved_person = self.entity_manager.get(mocks.ConcretePerson, 1)
        self.assertEqual(saved_person.address.object_id, other_address.object_id)

    def test_one_to_many_reverse_unset(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)

        # creates a parent person and two employees (a level below the
        # class that declares the reverse relation) to be associated
        # with it through the "to many" side of the relation
        parent = mocks.ConcretePerson()
        parent.object_id = 1
        parent.name = "parent_person"
        child_a = mocks.ConcreteEmployee()
        child_a.object_id = 2
        child_a.name = "child_a"
        child_b = mocks.ConcreteEmployee()
        child_b.object_id = 3
        child_b.name = "child_b"
        self.entity_manager.save(child_a)
        self.entity_manager.save(child_b)

        # associates both of the employees with the parent and verifies
        # that the relation is visible from both levels of the hierarchy
        parent.children = [child_a, child_b]
        self.entity_manager.save(parent)

        saved_child = self.entity_manager.get(mocks.ConcreteEmployee, 2)
        self.assertEqual(saved_child.parent.object_id, parent.object_id)
        saved_child = self.entity_manager.get(mocks.ConcretePerson, 2)
        self.assertEqual(saved_child.parent.object_id, parent.object_id)

        # re-assigns the relation so that only one of the employees
        # remains associated with the parent, the previous values must
        # be unset in every table that holds a copy of the column
        parent.children = [child_b]
        self.entity_manager.update(parent)

        saved_child = self.entity_manager.get(mocks.ConcreteEmployee, 2)
        self.assertEqual(saved_child.parent, None)
        saved_child = self.entity_manager.get(mocks.ConcretePerson, 2)
        self.assertEqual(saved_child.parent, None)

        # verifies that the remaining association is untouched, the
        # unset must be followed by the set of the new values
        saved_child = self.entity_manager.get(mocks.ConcreteEmployee, 3)
        self.assertEqual(saved_child.parent.object_id, parent.object_id)

        # verifies that the reverse side of the relation reports the
        # very same set of children, so that both sides agree
        saved_parent = self.entity_manager.get(
            mocks.ConcretePerson, 1, dict(eager=dict(children={}))
        )
        self.assertEqual(len(saved_parent.children), 1)
        self.assertEqual(saved_parent.children[0].object_id, child_b.object_id)

    def test_map_relations(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)
        self.entity_manager.create(mocks.ConcreteAddress)

        # creates an employee with an address associated, so that the
        # map based retrieval has to unpack a relation whose target is
        # part of a concrete table hierarchy
        address = mocks.ConcreteAddress()
        address.object_id = 1
        address.street = "street_address"
        employee = mocks.ConcreteEmployee()
        employee.object_id = 2
        employee.name = "name_employee"
        employee.address = address
        self.entity_manager.save(address)
        self.entity_manager.save(employee)

        # retrieves the employee as a map, eagerly loading the relation,
        # and verifies that it is unpacked as a nested map
        employees = self.entity_manager.find(
            mocks.ConcreteEmployee, dict(map=True, eager=("address",))
        )
        self.assertEqual(len(employees), 1)
        self.assertEqual(type(employees[0]), dict)
        self.assertEqual(type(employees[0]["address"]), dict)
        self.assertEqual(employees[0]["address"]["object_id"], 1)
        self.assertEqual(employees[0]["address"]["street"], "street_address")

        # verifies that the discriminator is unpacked both for the entity
        # and for the eagerly loaded relation, for the concrete table
        # strategy it is held in the table of the target itself
        self.assertEqual(employees[0]["_class"], "ConcreteEmployee")
        self.assertEqual(employees[0]["address"]["_class"], "ConcreteAddress")

        # creates a plain person to be the boss of the employee, so that
        # the reverse ("to many") side of a relation may also be part of
        # the map based retrieval
        boss = mocks.ConcretePerson()
        boss.object_id = 3
        boss.name = "name_boss"
        employee.boss = boss
        self.entity_manager.save(boss)
        self.entity_manager.update(employee)

        # retrieves the boss as a map, eagerly loading the "to many"
        # relation, and verifies that it is unpacked as a list of maps
        persons = self.entity_manager.find(
            mocks.ConcretePerson,
            dict(
                map=True,
                eager=("employees",),
                filters=[dict(type="equals", fields=[dict(name="object_id", value=3)])],
            ),
        )
        self.assertEqual(len(persons), 1)
        self.assertEqual(type(persons[0]["employees"]), list)
        self.assertEqual(len(persons[0]["employees"]), 1)
        self.assertEqual(persons[0]["employees"][0]["name"], "name_employee")

    def test_find_filter_inherited_field(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.ConcretePerson)
        self.entity_manager.create(mocks.ConcreteEmployee)

        # creates a set of employees with distinct values for a field
        # inherited from the parent class of the hierarchy
        for index in range(3):
            employee = mocks.ConcreteEmployee()
            employee.object_id = index + 1
            employee.name = "employee_%d" % index
            employee.age = 20 + index * 10
            employee.salary = 100 * (index + 1)
            self.entity_manager.save(employee)

        # filters on a field inherited from the parent class, for the
        # concrete table strategy the column resides in the entity's
        # own table so no parent table qualification may be used
        found = self.entity_manager.find(
            mocks.ConcreteEmployee,
            dict(
                filters=[
                    dict(type="equals", fields=[dict(name="name", value="employee_1")])
                ]
            ),
        )
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].object_id, 2)
        self.assertEqual(found[0].salary, 200)

        # filters on an inherited field using a greater than operation
        # to verify that the range based filters resolve correctly
        found = self.entity_manager.find(
            mocks.ConcreteEmployee,
            dict(filters=[dict(type="greater", fields=[dict(name="age", value=25)])]),
        )
        self.assertEqual(len(found), 2)

        # filters on a field declared in the leaf class itself, so that
        # both the inherited and the own columns are verified
        found = self.entity_manager.find(
            mocks.ConcreteEmployee,
            dict(
                filters=[dict(type="equals", fields=[dict(name="salary", value=300)])]
            ),
        )
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].name, "employee_2")

        # orders the results by an inherited field to verify that the
        # ordering also resolves the table name of the column
        found = self.entity_manager.find(
            mocks.ConcreteEmployee, dict(order_by=(("age", "descending"),))
        )
        self.assertEqual(len(found), 3)
        self.assertEqual(found[0].age, 40)
        self.assertEqual(found[2].age, 20)

    def _has_index(self, index_name):
        """
        Verifies if an index with the provided name is currently
        defined in the data source that backs the entity manager.

        :type index_name: String
        :param index_name: The name of the index to be verified.
        :rtype: bool
        :return: If the index is defined in the data source.
        """

        result_set = self.entity_manager.execute(
            "select count(*) from sqlite_master where type = 'index' "
            "and name = '%s'" % index_name
        )
        return result_set[0][0] == 1


class EntityManagerMigrationTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Entity Manager Migration test case"

    def test_has_table(self):
        # creates the required entity classes in the data source
        # and retrieves the underlying (raw) connection
        self.entity_manager.create(mocks.MigrationPerson)
        connection = self._get_connection()

        # verifies that the tables created for the hierarchy are
        # correctly detected in the data source catalog
        self.assertTrue(migration.has_table(connection, "_migration_root_entity"))
        self.assertTrue(migration.has_table(connection, "_migration_person"))

    def test_has_table_missing(self):
        # verifies that a table that was never created is not
        # reported as existing in the data source
        connection = self._get_connection()
        self.assertFalse(migration.has_table(connection, "_not_a_table"))

    def test_has_table_unknown_engine(self):
        # verifies that an unknown engine optimistically reports the
        # table as existing, as no catalog query may be performed
        connection = self._get_connection()
        self.assertTrue(
            migration.has_table(connection, "_not_a_table", engine="oracle")
        )

    def test_has_table_engines(self):
        # runs the table existence check against a cursor that records
        # the executed queries, so that the catalog query used for
        # each of the engines may be verified
        connection = mocks.MockRecordingConnection()

        self.assertTrue(migration.has_table(connection, "_person", "mysql"))
        self.assertTrue("information_schema.tables" in connection.queries[0])

        # verifies that the catalog query is scoped to the schema that
        # is currently in use, otherwise a table with the same name in
        # another schema of the server would be reported as existing
        self.assertTrue("table_schema = database()" in connection.queries[0])

        connection = mocks.MockRecordingConnection()
        self.assertTrue(migration.has_table(connection, "_person", "pgsql"))
        self.assertTrue("pg_tables" in connection.queries[0])
        self.assertTrue("schemaname = current_schema()" in connection.queries[0])

        # verifies that the SQLite catalog is used by default, and that
        # a zero count is correctly reported as a missing table
        connection = mocks.MockRecordingConnection(result=(0,))
        self.assertFalse(migration.has_table(connection, "_person"))
        self.assertTrue("sqlite_master" in connection.queries[0])

    def test_index_query(self):
        # verifies the index creation syntax for SQLite, where no
        # index method may be specified
        query = migration.index_query("_person", "object_id", "hash")
        self.assertEqual(
            query, "create index _person_object_id_hash on _person(object_id)"
        )

        # verifies the MySQL syntax, where the index method is
        # written after the indexed column
        query = migration.index_query("_person", "object_id", "hash", "mysql")
        self.assertEqual(
            query,
            "create index _person_object_id_hash on _person(object_id) using hash",
        )

        # verifies the PostgreSQL syntax, where the index method is
        # written before the indexed column
        query = migration.index_query("_person", "object_id", "btree", "pgsql")
        self.assertEqual(
            query,
            "create index _person_object_id_btree on _person using btree (object_id)",
        )

    def test_index_query_name_truncation(self):
        # builds an index name that exceeds the limits imposed by
        # both the MySQL and the PostgreSQL engines
        table_name = "_very_long_table_name_that_exceeds_the_engine_limits"
        attribute_name = "very_long_attribute_name_for_the_index"

        # verifies that the index name is truncated to the MySQL limit
        query = migration.index_query(table_name, attribute_name, "hash", "mysql")
        index_name = query.split(" on ")[0].replace("create index ", "")
        self.assertEqual(len(index_name), 64)

        # verifies that the index name is truncated to the (smaller)
        # PostgreSQL limit
        query = migration.index_query(table_name, attribute_name, "hash", "pgsql")
        index_name = query.split(" on ")[0].replace("create index ", "")
        self.assertEqual(len(index_name), 63)

        # verifies that two names that only differ in their beginning
        # do not collapse into the same index name once truncated, as
        # the resulting names would collide in the data source
        other_table = "_another_long_table_name_that_exceeds_the_engine_limits"
        other = migration.index_query(other_table, attribute_name, "hash", "pgsql")
        other_name = other.split(" on ")[0].replace("create index ", "")
        self.assertEqual(len(other_name), 63)
        self.assertNotEqual(index_name, other_name)

        # verifies that the index type is still part of the name of the
        # indexes that do not require any truncation at all
        query = migration.index_query("_person", "age", "btree", "pgsql")
        index_name = query.split(" on ")[0].replace("create index ", "")
        self.assertTrue(index_name.endswith("_btree"))

        # verifies that a name within the limits is not truncated
        query = migration.index_query("_person", "age", "hash", "mysql")
        index_name = query.split(" on ")[0].replace("create index ", "")
        self.assertEqual(index_name, "_person_age_hash")

    def test_insert_ignore_query(self):
        # verifies the duplicate safe insert syntax for each of the
        # supported engines, as they differ substantially
        select = "select object_id from _tmp"

        query = migration.insert_ignore_query("_person", "object_id", select)
        self.assertEqual(query, "insert or ignore into _person(object_id) " + select)

        query = migration.insert_ignore_query("_person", "object_id", select, "mysql")
        self.assertEqual(query, "insert ignore into _person(object_id) " + select)

        query = migration.insert_ignore_query("_person", "object_id", select, "pgsql")
        self.assertEqual(
            query,
            "insert into _person(object_id) " + select + " on conflict do nothing",
        )

    def test_get_hierarchy_classes(self):
        # retrieves the classes of the hierarchy and verifies that
        # they are ordered from the root down to the leaf
        classes = migration.get_hierarchy_classes(mocks.MigrationRootEntity)
        self.assertEqual(
            classes,
            [
                mocks.MigrationRootEntity,
                mocks.MigrationPerson,
                mocks.MigrationEmployee,
            ],
        )

        # retrieves the classes starting from an intermediate level
        # and verifies that only that level and below are returned
        classes = migration.get_hierarchy_classes(mocks.MigrationPerson)
        self.assertEqual(classes, [mocks.MigrationPerson, mocks.MigrationEmployee])

        # retrieves the classes for a leaf class and verifies that
        # only the class itself is returned
        classes = migration.get_hierarchy_classes(mocks.MigrationEmployee)
        self.assertEqual(classes, [mocks.MigrationEmployee])

    def test_get_hierarchy_classes_abstract_root(self):
        # verifies that an abstract root is not included in the
        # hierarchy classes, as it has no associated table
        classes = migration.get_hierarchy_classes(mocks.ConcreteAbstract)
        self.assertFalse(mocks.ConcreteAbstract in classes)
        self.assertTrue(mocks.ConcreteAbstractPerson in classes)
        self.assertTrue(mocks.ConcreteAbstractEmployee in classes)

    def test_get_hierarchy_classes_multiple_inheritance(self):
        # retrieves the hierarchy of a root class whose descendant is
        # reachable through more than one inheritance path, the
        # employee inherits from both the person and the taxable
        classes = migration.get_hierarchy_classes(mocks.RootEntity)

        # verifies that the duplicated class appears exactly once, so
        # that the migration does not operate twice on the same table
        self.assertEqual(classes.count(mocks.Employee), 1)
        self.assertEqual(classes.count(mocks.Person), 1)
        self.assertEqual(classes.count(mocks.Taxable), 1)

        # verifies that the root class comes first, as the ordering is
        # relied upon when the tables are created
        self.assertEqual(classes[0], mocks.RootEntity)

    def test_get_chain_root(self):
        # verifies that the chain root of a class of a hierarchy whose
        # root is not abstract is the root of the hierarchy itself
        self.assertEqual(
            migration.get_chain_root(mocks.MigrationEmployee),
            mocks.MigrationRootEntity,
        )

        # verifies that a class with no parents is its own chain root
        self.assertEqual(
            migration.get_chain_root(mocks.MigrationRootEntity),
            mocks.MigrationRootEntity,
        )

    def test_get_chain_root_abstract(self):
        # verifies that an abstract ancestor is not considered, as it
        # has no table to hold the discriminator column
        self.assertEqual(
            migration.get_chain_root(mocks.MigrationBranchAlpha),
            mocks.MigrationBranchAlpha,
        )

        # verifies that each of the chains that descend from the same
        # abstract root resolves to the top of its own chain, and not
        # to the first one of them
        self.assertEqual(
            migration.get_chain_root(mocks.MigrationBranchLeaf),
            mocks.MigrationBranchBeta,
        )
        self.assertEqual(
            migration.get_chain_root(mocks.MigrationBranchBeta),
            mocks.MigrationBranchBeta,
        )

    def test_get_column_definitions(self):
        # retrieves the column definitions for the intermediate level
        # of the hierarchy and indexes them by name for verification
        columns = migration.get_column_definitions(
            mocks.MigrationPerson, migration.SQL_TYPES_MAP
        )
        columns_map = dict((name, (type, is_pk)) for name, type, is_pk in columns)

        # verifies that both the own and the inherited columns are
        # present with the expected SQL types
        self.assertEqual(columns_map["object_id"], ("integer", True))
        self.assertEqual(columns_map["status"], ("integer", False))
        self.assertEqual(columns_map["name"], ("text", False))
        self.assertEqual(columns_map["age"], ("integer", False))

        # verifies that the leaf level also carries the column
        # declared by itself
        columns = migration.get_column_definitions(
            mocks.MigrationEmployee, migration.SQL_TYPES_MAP
        )
        names = [name for name, _type, _is_pk in columns]
        self.assertTrue("salary" in names)
        self.assertTrue("name" in names)

        # verifies that exactly one of the columns is the primary key
        primary = [name for name, _type, is_pk in columns if is_pk]
        self.assertEqual(primary, ["object_id"])

    def test_get_column_definitions_relations(self):
        # retrieves the column definitions for an entity class that
        # declares both mapped and non mapped relations
        columns = migration.get_column_definitions(
            mocks.ConcretePerson, migration.SQL_TYPES_MAP
        )
        names = [name for name, _type, _is_pk in columns]

        # verifies that the mapped relations originate a column while
        # the non mapped ones (reverse side) do not
        self.assertTrue("parent" in names)
        self.assertTrue("address" in names)
        self.assertFalse("children" in names)
        self.assertFalse("employees" in names)

        # verifies that the relation column takes the SQL type of the
        # identifier attribute of the target class
        columns_map = dict((name, type) for name, type, _is_pk in columns)
        self.assertEqual(columns_map["parent"], "integer")

    def test_get_column_definitions_relation_override(self):
        # retrieves the column definitions for a class that redefines an
        # inherited relation using the name of the target class instead
        # of the class itself, the relation has to be read from the
        # class that declares it, otherwise the name would be used as
        # if it were the class and the resolution would fail
        columns = migration.get_column_definitions(
            mocks.MigrationOverrideChild, migration.SQL_TYPES_MAP
        )
        columns_map = dict((name, type) for name, type, _is_pk in columns)

        # verifies that the relation column is present and that it takes
        # the SQL type of the identifier of the target class
        self.assertEqual(columns_map["parent"], "integer")
        self.assertEqual(columns_map["object_id"], "integer")

    def test_get_source_table_for_column(self):
        # verifies that a column declared by the root class resolves
        # to the table of the root class
        self.assertEqual(
            migration.get_source_table_for_column(mocks.MigrationEmployee, "status"),
            "_migration_root_entity",
        )

        # verifies that a column declared by an intermediate class
        # resolves to the table of that class
        self.assertEqual(
            migration.get_source_table_for_column(mocks.MigrationEmployee, "name"),
            "_migration_person",
        )

        # verifies that a column declared by the class itself resolves
        # to its own table
        self.assertEqual(
            migration.get_source_table_for_column(mocks.MigrationEmployee, "salary"),
            "_migration_employee",
        )

        # verifies that an unknown column falls back to the table of
        # the entity class used as the resolution context
        self.assertEqual(
            migration.get_source_table_for_column(
                mocks.MigrationEmployee, "not_a_column"
            ),
            "_migration_employee",
        )

    def test_checkpoint_database(self):
        # creates a temporary database using the write ahead log and
        # writes some data into it, so that the log holds content
        descriptor, file_path = tempfile.mkstemp(suffix=".db")
        os.close(descriptor)

        connection = sqlite3.connect(file_path)
        try:
            cursor = connection.cursor()
            try:
                # consumes the result of the journal mode change, as some
                # of the runtimes consider the statement to be still in
                # progress while its result has not been read
                cursor.execute("pragma journal_mode = wal")
                cursor.fetchall()
                cursor.execute("create table _logged(object_id integer primary key)")
                cursor.execute("insert into _logged values(1)")
            finally:
                cursor.close()
            connection.commit()

            # flushes the log and verifies that the database file has
            # grown, meaning that the content of the log reached it
            migration.checkpoint_database(file_path)
            self.assertTrue(os.path.getsize(file_path) > 0)
        finally:
            connection.close()
            os.remove(file_path)

    def test_checkpoint_database_invalid(self):
        # verifies that the flushing of the log is a best effort
        # operation, a path that may not be opened must be ignored
        # instead of raising an exception
        migration.checkpoint_database("/not/a/valid/path/database.db")

        # verifies the same for a file that exists but that is not a
        # valid database, where the flushing itself is the failing part
        descriptor, file_path = tempfile.mkstemp(suffix=".db")
        os.write(descriptor, b"not a database at all")
        os.close(descriptor)
        try:
            migration.checkpoint_database(file_path)
        finally:
            os.remove(file_path)

    def test_backup_database(self):
        # creates the required entity classes in the data source so
        # that the database file has some content to be copied
        self.entity_manager.create(mocks.MigrationPerson)
        file_path = self._get_file_path()

        # creates the backup of the database and verifies that the
        # resulting file exists and follows the naming convention
        backup_path = migration.backup_database(dict(file_path=file_path), "sqlite")
        try:
            self.assertTrue(os.path.exists(backup_path))
            self.assertTrue(os.path.getsize(backup_path) > 0)
            self.assertTrue(".backup." in backup_path)
            self.assertTrue(backup_path.startswith(file_path))
        finally:
            os.remove(backup_path)

    def test_backup_database_data_integrity(self):
        # creates the required entity classes and saves an entity so
        # that there is data to be verified in the backup
        self.entity_manager.create(mocks.MigrationPerson)
        person = mocks.MigrationPerson()
        person.object_id = 1
        person.name = "backed_up_person"
        person.age = 42
        self.entity_manager.save(person)

        # commits the pending transaction so that the saved data is
        # flushed into the database file before it is copied, then
        # begins a new one so that the tear down remains balanced
        self.entity_manager.commit()
        self.entity_manager.begin()

        # creates the backup and opens it as an independent connection
        # so that the copied contents may be inspected
        backup_path = migration.backup_database(
            dict(file_path=self._get_file_path()), "sqlite"
        )
        backup_connection = None
        try:
            backup_connection = sqlite3.connect(backup_path)
            cursor = backup_connection.cursor()
            try:
                # verifies that the tables of the hierarchy have been
                # copied into the backup
                self.assertTrue(
                    migration.has_table(backup_connection, "_migration_root_entity")
                )
                self.assertTrue(
                    migration.has_table(backup_connection, "_migration_person")
                )

                # verifies that the row values have been preserved by
                # the backup operation
                cursor.execute(
                    "select name, age from _migration_person where object_id = 1"
                )
                row = cursor.fetchone()
                self.assertNotEqual(row, None)
                self.assertEqual(row[0], "backed_up_person")
                self.assertEqual(row[1], 42)
            finally:
                cursor.close()
        finally:
            # closes the backup connection before removing the file so
            # that the handle is released (required under Windows)
            if backup_connection:
                backup_connection.close()
            os.remove(backup_path)

    def test_backup_database_write_ahead_log(self):
        # creates a temporary database configured to use the write ahead
        # log, the journal mode under which a file based copy of the
        # database may miss the data that is still held in the log
        descriptor, file_path = tempfile.mkstemp(suffix=".db")
        os.close(descriptor)

        connection = sqlite3.connect(file_path)
        try:
            cursor = connection.cursor()
            try:
                # consumes the result of the journal mode change, as some
                # of the runtimes consider the statement to be still in
                # progress while its result has not been read
                cursor.execute("pragma journal_mode = wal")
                cursor.fetchall()
                cursor.execute(
                    "create table _logged(" "object_id integer primary key, name text)"
                )
                cursor.execute("insert into _logged values(1, 'logged_name')")
            finally:
                cursor.close()
            connection.commit()

            # creates the backup while the connection is still open, so
            # that the log is not flushed by the closing of the connection
            backup_path = migration.backup_database(dict(file_path=file_path), "sqlite")
        finally:
            connection.close()

        # opens the backup as an independent connection and verifies that
        # the committed data is part of it, which is only the case when
        # the log has been flushed into the database file
        backup_connection = None
        try:
            backup_connection = sqlite3.connect(backup_path)
            cursor = backup_connection.cursor()
            try:
                cursor.execute("select name from _logged where object_id = 1")
                row = cursor.fetchone()
                self.assertNotEqual(row, None)
                self.assertEqual(row[0], "logged_name")
            finally:
                cursor.close()
        finally:
            if backup_connection:
                backup_connection.close()
            os.remove(backup_path)
            os.remove(file_path)

    def test_backup_database_credentials(self):
        # replaces the subprocess module by one that records the issued
        # commands, so that the backup of the "external" engines may be
        # verified without the corresponding database utilities
        subprocess = mocks.MockRecordingSubprocess()
        original = migration.subprocess
        migration.subprocess = subprocess

        # creates the temporary directory that is going to hold the
        # backup file, the database name is used as its path
        directory_path = tempfile.mkdtemp()
        database = os.path.join(directory_path, "database")

        try:
            # creates the backup of a PostgreSQL data source and
            # verifies that the password is passed to the utility
            # through the environment, as it does not accept it as
            # a command line argument
            backup_path = migration.backup_database(
                dict(database=database, user="user", password="password"), "pgsql"
            )
            args, kwargs = subprocess.calls[0]
            self.assertEqual(args[0], "pg_dump")
            self.assertEqual(kwargs["env"]["PGPASSWORD"], "password")
            self.assertTrue(backup_path.startswith(database))

            # creates the backup of a MySQL data source and verifies
            # that the password is passed through the environment, as
            # providing it in the command line would expose it in the
            # process listing
            backup_path = migration.backup_database(
                dict(database=database, user="user", password="password"), "mysql"
            )
            args, kwargs = subprocess.calls[1]
            self.assertEqual(args[0], "mysqldump")
            self.assertEqual(kwargs["env"]["MYSQL_PWD"], "password")
            self.assertFalse(self._any_matching(args, "password"))
        finally:
            migration.subprocess = original
            shutil.rmtree(directory_path)

    def test_backup_database_credentials_undefined(self):
        # replaces the subprocess module by one that records the issued
        # commands so that the backup may be verified without the
        # corresponding database utilities
        subprocess = mocks.MockRecordingSubprocess()
        original = migration.subprocess
        migration.subprocess = subprocess

        directory_path = tempfile.mkdtemp()
        database = os.path.join(directory_path, "database")

        try:
            # creates the backup with no password defined and verifies
            # that no credentials are set in the environment, so that
            # the ambient ones remain the ones in use
            migration.backup_database(dict(database=database), "pgsql")
            _args, kwargs = subprocess.calls[0]
            self.assertFalse("PGPASSWORD" in kwargs["env"])
        finally:
            migration.subprocess = original
            shutil.rmtree(directory_path)

    def test_backup_database_unsupported_engine(self):
        # verifies that an unsupported engine raises an error instead
        # of silently skipping the backup step
        self.assert_raises(
            ValueError,
            migration.backup_database,
            dict(file_path=self._get_file_path()),
            "oracle",
        )

    def test_validate_hierarchy_same_strategy(self):
        # verifies that a migration to the strategy already in use is
        # rejected for a class table hierarchy
        is_valid, messages = migration.validate_hierarchy(
            mocks.MigrationRootEntity, "class_table"
        )
        self.assertFalse(is_valid)
        self.assertTrue(self._any_matching(messages, "already uses"))

        # verifies the same rejection for a concrete table hierarchy
        is_valid, messages = migration.validate_hierarchy(
            mocks.MigrationConcreteRoot, "concrete_table"
        )
        self.assertFalse(is_valid)
        self.assertTrue(self._any_matching(messages, "already uses"))

    def test_validate_hierarchy_cti_to_concrete(self):
        # verifies that a class table hierarchy may be migrated to the
        # concrete table strategy
        is_valid, messages = migration.validate_hierarchy(
            mocks.MigrationRootEntity, "concrete_table"
        )
        self.assertTrue(is_valid)
        self.assertTrue(self._any_matching(messages, "validation passed"))

    def test_validate_hierarchy_concrete_to_cti(self):
        # verifies that a concrete table hierarchy may be migrated back
        # to the class table strategy
        is_valid, messages = migration.validate_hierarchy(
            mocks.MigrationConcreteRoot, "class_table"
        )
        self.assertTrue(is_valid)
        self.assertTrue(self._any_matching(messages, "validation passed"))

    def test_validate_hierarchy_mixed_strategies(self):
        # validates a hierarchy whose descendant declares a strategy
        # that conflicts with the one of the root class
        is_valid, messages = migration.validate_hierarchy(
            mocks.MigrationMixedRoot, "concrete_table"
        )

        # verifies that the misconfiguration is rejected and that the
        # offending class is named in the reported messages
        self.assertFalse(is_valid)
        self.assertTrue(self._any_matching(messages, "MigrationMixedChild"))
        self.assertTrue(self._any_matching(messages, "expected 'class_table'"))

    def test_validate_data(self):
        # creates the required entity classes and saves entities at
        # both levels of the hierarchy so that the data is consistent
        self.entity_manager.create(mocks.MigrationPerson)
        self.entity_manager.create(mocks.MigrationEmployee)
        employee = mocks.MigrationEmployee()
        employee.object_id = 1
        employee.name = "consistent_employee"
        self.entity_manager.save(employee)

        # validates the data and verifies that no orphaned rows are
        # reported for the consistent hierarchy
        messages = []
        is_valid = migration.validate_data(
            self._get_connection(), mocks.MigrationRootEntity, messages
        )
        self.assertTrue(is_valid)

    def test_validate_data_orphaned(self):
        # creates the required entity classes and saves an entity so
        # that rows exist at both levels of the hierarchy
        self.entity_manager.create(mocks.MigrationPerson)
        self.entity_manager.create(mocks.MigrationEmployee)
        employee = mocks.MigrationEmployee()
        employee.object_id = 1
        employee.name = "orphan_to_be"
        self.entity_manager.save(employee)

        # removes the root level row directly, leaving the descendant
        # rows orphaned and the hierarchy inconsistent
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("delete from _migration_root_entity where object_id = 1")
        finally:
            cursor.close()

        # validates the data and verifies that the orphaned rows are
        # detected and reported
        messages = []
        is_valid = migration.validate_data(
            connection, mocks.MigrationRootEntity, messages
        )
        self.assertFalse(is_valid)
        self.assertTrue(self._any_matching(messages, "orphaned"))

    def test_validate_data_engine(self):
        # runs the validation against a cursor that records the queries
        # executed through it, so that the catalog query used to filter
        # the hierarchy may be verified for an engine other than the
        # one that backs the current entity manager
        connection = mocks.MockRecordingConnection(result=(0,))
        messages = []
        is_valid = migration.validate_data(
            connection, mocks.MigrationRootEntity, messages, "mysql"
        )

        # verifies that the engine is honoured, otherwise the SQLite
        # catalog would be queried in a data source that has none
        self.assertTrue(is_valid)
        self.assertTrue("information_schema.tables" in connection.queries[0])

    def test_generate_cti_to_concrete_queries(self):
        # generates the queries for the migration and groups them by
        # the statement type so that each group may be verified
        queries = migration.generate_cti_to_concrete_queries(mocks.MigrationRootEntity)
        self.assertNotEqual(queries, [])

        # verifies that the complete set of statement types required
        # by the migration is generated
        self.assertTrue(self._any_starting(queries, "create table"))
        self.assertTrue(self._any_starting(queries, "insert into"))
        self.assertTrue(self._any_starting(queries, "drop table"))
        self.assertTrue(self._any_starting(queries, "alter table"))
        self.assertTrue(self._any_starting(queries, "create index"))

        # verifies that the temporary table created for the leaf level
        # carries the columns inherited from the upper levels
        create = self._first_matching(queries, "_migration_employee")
        self.assertTrue("status" in create)
        self.assertTrue("name" in create)
        self.assertTrue("salary" in create)

    def test_generate_cti_to_concrete_queries_indexes(self):
        # generates the queries for the MySQL engine and verifies that
        # the index statements use the engine specific syntax
        queries = migration.generate_cti_to_concrete_queries(
            mocks.MigrationRootEntity, engine="mysql"
        )
        indexes = [query for query in queries if query.startswith("create index")]
        self.assertNotEqual(indexes, [])
        for index in indexes:
            self.assertTrue(" using " in index)

        # generates the queries for the PostgreSQL engine and verifies
        # the same for its own syntax
        queries = migration.generate_cti_to_concrete_queries(
            mocks.MigrationRootEntity, engine="pgsql"
        )
        indexes = [query for query in queries if query.startswith("create index")]
        self.assertNotEqual(indexes, [])
        for index in indexes:
            self.assertTrue(" using " in index)

    def test_generate_cti_to_concrete_queries_relations(self):
        # generates the queries for a hierarchy that declares mapped
        # relations and whose levels are reachable through abstract
        # ancestors, no connection is given so that every class of the
        # hierarchy is considered
        queries = migration.generate_cti_to_concrete_queries(mocks.RootEntity)
        self.assertNotEqual(queries, [])

        # verifies that the mapped relations originate a column in the
        # flattened table of the class that maps them
        create = self._first_matching(queries, "create table _person__concrete_tmp")
        self.assertTrue("parent" in create)
        self.assertTrue("address" in create)

        # verifies that the non mapped (reverse) relations do not
        # originate a column, as they live on the other side
        self.assertFalse("children" in create)
        self.assertFalse("dogs" in create)

        # verifies that an index is created for the mapped relation
        # columns, so that the joins remain efficient after migrating
        indexes = [query for query in queries if query.startswith("create index")]
        self.assertTrue(self._any_matching(indexes, "_person_parent_hash"))
        self.assertTrue(self._any_matching(indexes, "_person_address_hash"))

    def test_generate_cti_to_concrete_queries_abstract(self):
        # generates the queries for a hierarchy whose root class is
        # abstract, the abstract level must not originate a table
        queries = migration.generate_cti_to_concrete_queries(mocks.RootEntityAbstract)
        self.assertNotEqual(queries, [])

        # verifies that no table is created for the abstract root
        self.assertFalse(self._any_matching(queries, "_root_entity_abstract"))

        # verifies that the concrete descendant carries the columns
        # inherited from the abstract root
        create = self._first_matching(queries, "create table _chair__concrete_tmp")
        self.assertTrue("status" in create)
        self.assertTrue("legs" in create)

    def test_generate_cti_to_concrete_queries_branches(self):
        # generates the queries for a hierarchy whose abstract root
        # branches into more than one independent chain of classes
        queries = migration.generate_cti_to_concrete_queries(mocks.MigrationBranchRoot)
        self.assertNotEqual(queries, [])

        # verifies that the discriminator of a class of the second of
        # the chains is read from the table at the top of its own chain
        # and not from the one of the first, which is not joined
        insert = self._first_matching(
            queries, "insert into _migration_branch_leaf__concrete_tmp"
        )
        self.assertTrue("_migration_branch_beta._class" in insert)
        self.assertFalse("_migration_branch_alpha" in insert)

        # verifies that the filtering by the discriminator is also
        # scoped to the table at the top of the chain of the class
        self.assertTrue("where _migration_branch_beta._class in" in insert)

        # verifies that the class at the top of a chain reads the
        # discriminator from its own table, as it holds it
        insert = self._first_matching(
            queries, "insert into _migration_branch_alpha__concrete_tmp"
        )
        self.assertTrue("_migration_branch_alpha._class" in insert)
        self.assertFalse("where" in insert)

    def test_generate_concrete_to_cti_queries(self):
        # generates the queries for the reverse migration and verifies
        # that the expected statement types are generated
        queries = migration.generate_concrete_to_cti_queries(
            mocks.MigrationConcreteRoot
        )
        self.assertNotEqual(queries, [])
        self.assertTrue(self._any_starting(queries, "create table"))
        self.assertTrue(self._any_starting(queries, "insert"))
        self.assertTrue(self._any_starting(queries, "drop table"))

    def test_generate_concrete_to_cti_queries_inserts(self):
        # generates the queries for the MySQL engine and verifies that
        # the duplicate safe insert syntax of the engine is used
        queries = migration.generate_concrete_to_cti_queries(
            mocks.MigrationConcreteRoot, engine="mysql"
        )
        inserts = [query for query in queries if query.startswith("insert")]
        self.assertNotEqual(inserts, [])
        for insert in inserts:
            self.assertTrue(insert.startswith("insert ignore"))

        # generates the queries for the PostgreSQL engine and verifies
        # the same for its own conflict handling syntax
        queries = migration.generate_concrete_to_cti_queries(
            mocks.MigrationConcreteRoot, engine="pgsql"
        )
        inserts = [query for query in queries if query.startswith("insert")]
        self.assertNotEqual(inserts, [])
        for insert in inserts:
            self.assertTrue(insert.endswith("on conflict do nothing"))

    def test_generate_concrete_to_cti_queries_relations(self):
        # generates the queries for a concrete table hierarchy that
        # declares mapped relations at more than one level
        queries = migration.generate_concrete_to_cti_queries(mocks.ConcreteRootEntity)
        self.assertNotEqual(queries, [])

        # verifies that the mapped relation columns are assigned to
        # the level of the hierarchy that declares them
        create = self._first_matching(queries, "create table _concrete_person__cti_tmp")
        self.assertTrue("parent" in create)
        self.assertTrue("address" in create)
        self.assertFalse("boss" in create)

        create = self._first_matching(
            queries, "create table _concrete_employee__cti_tmp"
        )
        self.assertTrue("boss" in create)
        self.assertFalse("parent" in create)

        # verifies that an index is created for the mapped relation
        # columns of each of the levels
        indexes = [query for query in queries if query.startswith("create index")]
        self.assertTrue(self._any_matching(indexes, "_concrete_person_parent_hash"))
        self.assertTrue(self._any_matching(indexes, "_concrete_employee_boss_hash"))

    def test_generate_concrete_to_cti_queries_abstract(self):
        # generates the queries for a concrete table hierarchy whose
        # root class is abstract, the abstract level must be skipped
        queries = migration.generate_concrete_to_cti_queries(mocks.ConcreteAbstract)
        self.assertNotEqual(queries, [])

        # verifies that no table is created for the abstract root and
        # that the first concrete level keeps the inherited columns
        self.assertFalse(self._any_matching(queries, "_concrete_abstract__cti_tmp"))
        create = self._first_matching(
            queries, "create table _concrete_abstract_person__cti_tmp"
        )
        self.assertTrue("status" in create)
        self.assertTrue("name" in create)

        # verifies that the second concrete level only keeps the
        # column that it declares itself
        create = self._first_matching(
            queries, "create table _concrete_abstract_employee__cti_tmp"
        )
        self.assertTrue("salary" in create)
        self.assertFalse("name" in create)

    def test_migrate_validate_only(self):
        # runs the migration in validation only mode and verifies that
        # it succeeds without touching the data source
        self.entity_manager.create(mocks.MigrationPerson)
        success, messages = migration.migrate(
            entity_class=mocks.MigrationRootEntity,
            target_strategy="concrete_table",
            connection=self._get_connection(),
            skip_backup=True,
            validate_only=True,
        )
        self.assertTrue(success)
        self.assertTrue(self._any_matching(messages, "validation passed"))

        # verifies that the class table structure is left untouched, so
        # the intermediate table still lacks the inherited column
        self.assertFalse("status" in self._get_columns("_migration_person"))

    def test_migrate_rejected_strategy(self):
        # runs the migration towards the strategy already in use and
        # verifies that it is rejected before any change is made
        self.entity_manager.create(mocks.MigrationPerson)
        success, messages = migration.migrate(
            entity_class=mocks.MigrationRootEntity,
            target_strategy="class_table",
            connection=self._get_connection(),
            skip_backup=True,
        )
        self.assertFalse(success)
        self.assertTrue(self._any_matching(messages, "already uses"))

    def test_migrate_aborts_on_orphaned_data(self):
        # creates the required entity classes in the data source and
        # saves an entity so that rows exist at both levels
        self.entity_manager.create(mocks.MigrationPerson)
        self.entity_manager.create(mocks.MigrationEmployee)
        employee = mocks.MigrationEmployee()
        employee.object_id = 1
        employee.name = "orphan_to_be"
        self.entity_manager.save(employee)

        # removes the root level row directly, leaving the descendant
        # rows orphaned, the join that copies the rows into the new
        # tables would otherwise drop them silently
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("delete from _migration_root_entity where object_id = 1")
        finally:
            cursor.close()

        # runs the migration and verifies that it is aborted before any
        # of the tables is touched, the data loss must be reported
        success, messages = migration.migrate(
            entity_class=mocks.MigrationRootEntity,
            target_strategy="concrete_table",
            connection=connection,
            skip_backup=True,
        )
        self.assertFalse(success)
        self.assertTrue(self._any_matching(messages, "orphaned"))

        # verifies that the class table structure is left untouched, so
        # that the inconsistency may be resolved before retrying
        self.assertFalse("name" in self._get_columns("_migration_employee"))

    def test_migrate_unsupported_direction(self):
        # runs the migration towards a strategy that is not one of the
        # supported ones, so that no migration direction resolves
        self.entity_manager.create(mocks.MigrationPerson)
        success, messages = migration.migrate(
            entity_class=mocks.MigrationRootEntity,
            target_strategy="single_table",
            connection=self._get_connection(),
            skip_backup=True,
        )

        # verifies that the migration is refused and that the reason
        # names the direction that could not be resolved
        self.assertFalse(success)
        self.assertTrue(self._any_matching(messages, "unsupported migration direction"))

    def test_migrate_dry_run(self):
        # runs the migration in dry-run mode, the queries should be
        # reported but never executed against the data source
        self.entity_manager.create(mocks.MigrationPerson)
        self.entity_manager.create(mocks.MigrationEmployee)
        success, messages = migration.migrate(
            entity_class=mocks.MigrationRootEntity,
            target_strategy="concrete_table",
            connection=self._get_connection(),
            dry_run=True,
            skip_backup=True,
        )
        self.assertTrue(success)
        self.assertTrue(self._any_matching(messages, "dry-run mode"))
        self.assertTrue(self._any_matching(messages, "create table"))

        # verifies that the original tables are still present and that
        # the schema has not been flattened
        self.assertTrue(
            migration.has_table(self._get_connection(), "_migration_person")
        )
        self.assertFalse("status" in self._get_columns("_migration_person"))

    def test_migrate_skip_backup_unsupported_engine(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.MigrationPerson)

        # runs the migration for an engine that commits the schema
        # changes implicitly, asking for the backup to be skipped
        success, messages = migration.migrate(
            entity_class=mocks.MigrationBranchAlpha,
            target_strategy="concrete_table",
            connection=mocks.MockRecordingConnection(),
            engine="mysql",
            skip_backup=True,
        )

        # verifies that the request is refused, as the roll back is not
        # able to undo the schema changes under such engines and the
        # backup is then the only way back from a failure
        self.assertFalse(success)
        self.assertTrue(self._any_matching(messages, "may not be skipped"))

    def test_migrate_skip_backup_supported_engine(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.MigrationPerson)
        self.entity_manager.create(mocks.MigrationEmployee)

        # runs the migration for the engine that treats the schema
        # changes as part of the transaction, asking for the backup
        # to be skipped
        success, messages = migration.migrate(
            entity_class=mocks.MigrationRootEntity,
            target_strategy="concrete_table",
            connection=self._get_connection(),
            skip_backup=True,
        )

        # verifies that the request is honoured, the roll back is able
        # to undo the schema changes under it
        self.assertTrue(success, "; ".join(messages))
        self.assertFalse(self._any_matching(messages, "backup created at"))

    def test_migrate_creates_backup(self):
        # creates the required entity classes so that the database
        # file exists and may be backed up
        self.entity_manager.create(mocks.MigrationConcretePerson)

        # uses a connection that fails on the migration queries so that
        # the migration aborts right after the backup has been created,
        # isolating the backup step from the migration itself
        connection = mocks.MockFailingConnection(self._get_connection())

        success, messages = migration.migrate(
            entity_class=mocks.MigrationConcreteRoot,
            target_strategy="class_table",
            connection=connection,
            connection_params=dict(file_path=self._get_file_path()),
            skip_backup=False,
        )

        # verifies that the migration failed and that exactly one
        # backup was reported as created
        self.assertFalse(success)
        backups = [message for message in messages if "backup created at: " in message]
        self.assertEqual(len(backups), 1)

        # verifies that the reported backup file was actually written
        backup_path = backups[0].split("backup created at: ")[1]
        try:
            self.assertTrue(os.path.exists(backup_path))
            self.assertTrue(os.path.getsize(backup_path) > 0)
        finally:
            os.remove(backup_path)

    def test_migrate_aborts_on_backup_failure(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.MigrationConcretePerson)

        # runs the migration pointing the backup at a path that cannot
        # be written, so that the backup step fails
        success, messages = migration.migrate(
            entity_class=mocks.MigrationConcreteRoot,
            target_strategy="class_table",
            connection=self._get_connection(),
            connection_params=dict(file_path="/not/a/valid/path/database.db"),
            skip_backup=False,
        )

        # verifies that the migration is aborted instead of proceeding
        # without a backup of the data source
        self.assertFalse(success)
        self.assertTrue(self._any_matching(messages, "failed to create backup"))

        # verifies that the concrete table structure was left untouched
        self.assertTrue("status" in self._get_columns("_migration_concrete_person"))

    def test_migrate_rollback_on_failure(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.MigrationPerson)
        self.entity_manager.create(mocks.MigrationEmployee)

        # wraps the connection so that it fails after the first of the
        # migration queries, leaving the migration partially applied
        connection = mocks.MockFailingConnection(self._get_connection(), fail_after=1)

        success, messages = migration.migrate(
            entity_class=mocks.MigrationRootEntity,
            target_strategy="concrete_table",
            connection=connection,
            skip_backup=True,
        )

        # verifies that the failure is reported and that the
        # transaction was explicitly rolled back
        self.assertFalse(success)
        self.assertTrue(self._any_matching(messages, "migration failed"))
        self.assertTrue(self._any_matching(messages, "rolled back"))
        self.assertTrue(connection.rolled_back)

        # verifies that every cursor created by the migration was
        # closed, so that no reference to them is leaked
        for cursor in connection.cursors:
            self.assertTrue(cursor.closed)

    def test_migrate_rollback_not_transactional(self):
        # replaces the subprocess module by one that records the issued
        # commands, so that the backup of the "external" engine may be
        # created without the corresponding database utility
        subprocess = mocks.MockRecordingSubprocess()
        original = migration.subprocess
        migration.subprocess = subprocess

        # creates the temporary directory that is going to hold the
        # backup file, the database name is used as its path
        directory_path = tempfile.mkdtemp()
        database = os.path.join(directory_path, "database")

        # wraps a recording connection so that it fails after the first
        # of the migration queries, leaving the migration partially
        # applied in a data source that is not able to roll it back
        connection = mocks.MockFailingConnection(
            mocks.MockRecordingConnection(), fail_after=1
        )

        try:
            success, messages = migration.migrate(
                entity_class=mocks.MigrationBranchAlpha,
                target_strategy="concrete_table",
                connection=connection,
                engine="mysql",
                connection_params=dict(database=database),
            )
        finally:
            migration.subprocess = original
            shutil.rmtree(directory_path)

        # verifies that the roll back was attempted and that the report
        # of the failure is honest about the schema changes it was not
        # able to undo, so that the backup is known to be required
        self.assertFalse(success)
        self.assertTrue(connection.rolled_back)
        self.assertTrue(self._any_matching(messages, "not transactional"))
        self.assertTrue(self._any_matching(messages, "restore the backup"))

    def test_migrate_rollback_failure(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.MigrationPerson)
        self.entity_manager.create(mocks.MigrationEmployee)

        # wraps the connection so that the migration queries fail and
        # the rollback that follows also fails, the worst case for the
        # error handling of the migration
        connection = mocks.MockFailingConnection(
            self._get_connection(), rollback_fails=True
        )

        success, messages = migration.migrate(
            entity_class=mocks.MigrationRootEntity,
            target_strategy="concrete_table",
            connection=connection,
            skip_backup=True,
        )

        # verifies that the failure is still reported, instead of the
        # rollback error masking the original migration error
        self.assertFalse(success)
        self.assertTrue(self._any_matching(messages, "migration failed"))
        self.assertTrue(self._any_matching(messages, "rolled back"))

    def test_migrate_closes_cursor(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.MigrationPerson)
        self.entity_manager.create(mocks.MigrationEmployee)

        # wraps the connection so that the cursors it creates keep track
        # of their own state, the failure threshold is set high enough
        # for the migration to be allowed to run to completion
        connection = mocks.MockFailingConnection(
            self._get_connection(), fail_after=1000
        )

        success, messages = migration.migrate(
            entity_class=mocks.MigrationRootEntity,
            target_strategy="concrete_table",
            connection=connection,
            skip_backup=True,
        )
        self.assertTrue(success, "; ".join(messages))

        # verifies that every cursor created by the migration was
        # closed, so that no reference to them is leaked
        for cursor in connection.cursors:
            self.assertTrue(cursor.closed)

    def test_migrate_cti_to_concrete(self):
        # creates the required entity classes in the data source and
        # saves entities at two distinct levels of the hierarchy
        self.entity_manager.create(mocks.MigrationPerson)
        self.entity_manager.create(mocks.MigrationEmployee)
        person = mocks.MigrationPerson()
        person.object_id = 1
        person.name = "migrated_person"
        person.age = 25
        employee = mocks.MigrationEmployee()
        employee.object_id = 2
        employee.name = "migrated_employee"
        employee.age = 30
        employee.salary = 500
        self.entity_manager.save(person)
        self.entity_manager.save(employee)

        # verifies the class table structure before the migration, the
        # intermediate table must not carry the inherited column
        self.assertFalse("status" in self._get_columns("_migration_person"))
        self.assertEqual(self._count_rows("_migration_root_entity"), 2)
        self.assertEqual(self._count_rows("_migration_person"), 2)
        self.assertEqual(self._count_rows("_migration_employee"), 1)

        # runs the migration towards the concrete table strategy
        success, messages = migration.migrate(
            entity_class=mocks.MigrationRootEntity,
            target_strategy="concrete_table",
            connection=self._get_connection(),
            skip_backup=True,
        )
        self.assertTrue(success, "; ".join(messages))

        # verifies that every level of the hierarchy now carries the
        # complete set of columns flattened down to it
        columns = self._get_columns("_migration_person")
        self.assertTrue("object_id" in columns)
        self.assertTrue("status" in columns)
        self.assertTrue("name" in columns)
        self.assertFalse("salary" in columns)

        columns = self._get_columns("_migration_employee")
        self.assertTrue("status" in columns)
        self.assertTrue("name" in columns)
        self.assertTrue("salary" in columns)

        # verifies that the row counts are preserved at every level
        self.assertEqual(self._count_rows("_migration_root_entity"), 2)
        self.assertEqual(self._count_rows("_migration_person"), 2)
        self.assertEqual(self._count_rows("_migration_employee"), 1)

        # verifies that the values of the employee were carried into
        # the flattened leaf table, including the inherited ones
        row = self._fetch_row(
            "select status, name, age, salary, _class from _migration_employee "
            "where object_id = 2"
        )
        self.assertNotEqual(row, None)
        self.assertEqual(row[0], 1)
        self.assertEqual(row[1], "migrated_employee")
        self.assertEqual(row[2], 30)
        self.assertEqual(row[3], 500)
        self.assertEqual(row[4], "MigrationEmployee")

        # verifies that the employee is also present in the ancestor
        # table with the discriminator of its own concrete class
        row = self._fetch_row(
            "select name, _class from _migration_person where object_id = 2"
        )
        self.assertNotEqual(row, None)
        self.assertEqual(row[0], "migrated_employee")
        self.assertEqual(row[1], "MigrationEmployee")

    def test_migrate_concrete_to_cti(self):
        # creates the required entity classes in the data source and
        # saves entities at two distinct levels of the hierarchy
        self.entity_manager.create(mocks.MigrationConcretePerson)
        self.entity_manager.create(mocks.MigrationConcreteEmployee)
        person = mocks.MigrationConcretePerson()
        person.object_id = 1
        person.name = "migrated_person"
        person.age = 25
        employee = mocks.MigrationConcreteEmployee()
        employee.object_id = 2
        employee.name = "migrated_employee"
        employee.age = 30
        employee.salary = 500
        self.entity_manager.save(person)
        self.entity_manager.save(employee)

        # verifies the concrete table structure before the migration,
        # the intermediate table must carry the inherited column
        self.assertTrue("status" in self._get_columns("_migration_concrete_person"))

        # runs the migration towards the class table strategy
        success, messages = migration.migrate(
            entity_class=mocks.MigrationConcreteRoot,
            target_strategy="class_table",
            connection=self._get_connection(),
            skip_backup=True,
        )
        self.assertTrue(success, "; ".join(messages))

        # verifies that the inherited columns have been removed from
        # the descendant tables, which now only hold their own fields
        columns = self._get_columns("_migration_concrete_person")
        self.assertTrue("object_id" in columns)
        self.assertTrue("name" in columns)
        self.assertFalse("status" in columns)

        columns = self._get_columns("_migration_concrete_employee")
        self.assertTrue("salary" in columns)
        self.assertFalse("name" in columns)

        # verifies that the values remain accessible at the level that
        # declares each one of the attributes
        row = self._fetch_row(
            "select name, age from _migration_concrete_person where object_id = 1"
        )
        self.assertNotEqual(row, None)
        self.assertEqual(row[0], "migrated_person")
        self.assertEqual(row[1], 25)

        row = self._fetch_row(
            "select salary from _migration_concrete_employee where object_id = 2"
        )
        self.assertNotEqual(row, None)
        self.assertEqual(row[0], 500)

        # verifies that the discriminator was kept at the root level
        row = self._fetch_row(
            "select _class from _migration_concrete_root where object_id = 2"
        )
        self.assertNotEqual(row, None)
        self.assertEqual(row[0], "MigrationConcreteEmployee")

    def test_migrate_preserves_indexes(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.MigrationPerson)
        self.entity_manager.create(mocks.MigrationEmployee)

        # runs the migration towards the concrete table strategy
        success, messages = migration.migrate(
            entity_class=mocks.MigrationRootEntity,
            target_strategy="concrete_table",
            connection=self._get_connection(),
            skip_backup=True,
        )
        self.assertTrue(success, "; ".join(messages))

        # verifies that the indexes were recreated on the migrated
        # table, both for the primary key and the modified time
        row = self._fetch_row(
            "select count(*) from sqlite_master where type='index' "
            "and tbl_name='_migration_person'"
        )
        self.assertTrue(row[0] >= 4)

        # verifies that the index of the field declared as indexed by
        # the model is recreated in the table of the class that declares
        # it and in the one of the descendant, as the column is
        # flattened into both of them
        self.assertTrue(self._has_index("_migration_person_name_hash"))
        self.assertTrue(self._has_index("_migration_employee_name_hash"))

    def test_migrate_preserves_indexes_reverse(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(mocks.MigrationConcretePerson)
        self.entity_manager.create(mocks.MigrationConcreteEmployee)

        # runs the migration towards the class table strategy
        success, messages = migration.migrate(
            entity_class=mocks.MigrationConcreteRoot,
            target_strategy="class_table",
            connection=self._get_connection(),
            skip_backup=True,
        )
        self.assertTrue(success, "; ".join(messages))

        # verifies that the index of the field declared as indexed by
        # the model is recreated in the table of the class that declares
        # it, and only in it, as the descendant now shares its row
        self.assertTrue(self._has_index("_migration_concrete_person_name_hash"))
        self.assertFalse(self._has_index("_migration_concrete_employee_name_hash"))

    def _get_connection(self):
        """
        Retrieves the underlying (raw) connection object of the entity
        manager, to be used in the direct interaction with the data
        source required by the migration operations.

        :rtype: Connection
        :return: The raw connection object for the data source that
        backs the current entity manager.
        """

        connection = self.entity_manager.get_connection()
        return connection._connection.get_connection()

    def _get_file_path(self):
        """
        Retrieves the file path of the data source that backs the
        current entity manager, to be used in the backup operations.

        :rtype: String
        :return: The file path of the current data source.
        """

        connection = self.entity_manager.get_connection()
        return connection._connection.get_file_path()

    def _get_columns(self, table_name):
        """
        Retrieves the names of the columns of the provided table, as
        currently defined in the data source.

        :type table_name: String
        :param table_name: The name of the table to be inspected.
        :rtype: List
        :return: The list containing the names of the columns.
        """

        cursor = self._get_connection().cursor()
        try:
            cursor.execute("pragma table_info(%s)" % table_name)
            return [row[1] for row in cursor.fetchall()]
        finally:
            cursor.close()

    def _count_rows(self, table_name):
        """
        Counts the number of rows currently present in the provided
        table of the data source.

        :type table_name: String
        :param table_name: The name of the table to be counted.
        :rtype: int
        :return: The number of rows in the table.
        """

        return self._fetch_row("select count(*) from %s" % table_name)[0]

    def _has_index(self, index_name):
        """
        Verifies if an index with the provided name is currently
        defined in the data source that backs the entity manager.

        :type index_name: String
        :param index_name: The name of the index to be verified.
        :rtype: bool
        :return: If the index is defined in the data source.
        """

        row = self._fetch_row(
            "select count(*) from sqlite_master where type = 'index' "
            "and name = '%s'" % index_name
        )
        return row[0] == 1

    def _fetch_row(self, query):
        """
        Executes the provided query in the data source and retrieves
        the first row of the corresponding result.

        :type query: String
        :param query: The query to be executed in the data source.
        :rtype: Tuple
        :return: The first row of the result of the query.
        """

        cursor = self._get_connection().cursor()
        try:
            cursor.execute(query)
            return cursor.fetchone()
        finally:
            cursor.close()

    def _any_matching(self, messages, value):
        """
        Verifies if any of the provided messages contains the
        requested value.

        :type messages: List
        :param messages: The list of messages to be verified.
        :type value: String
        :param value: The value to be searched in the messages.
        :rtype: bool
        :return: If any of the messages contains the value.
        """

        for message in messages:
            if value in message:
                return True
        return False

    def _any_starting(self, queries, value):
        """
        Verifies if any of the provided queries starts with the
        requested value.

        :type queries: List
        :param queries: The list of queries to be verified.
        :type value: String
        :param value: The value the queries are tested against.
        :rtype: bool
        :return: If any of the queries starts with the value.
        """

        for query in queries:
            if query.startswith(value):
                return True
        return False

    def _first_matching(self, queries, value):
        """
        Retrieves the first of the provided queries that contains the
        requested value, defaulting to an empty string.

        :type queries: List
        :param queries: The list of queries to be searched.
        :type value: String
        :param value: The value to be searched in the queries.
        :rtype: String
        :return: The first query containing the value.
        """

        for query in queries:
            if value in query:
                return query
        return ""


class EntityManagerRsetTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Entity Manager Rset test case"

    def test_simple(self):
        first_set = structures.rset([["First", 30]])
        first_set.set_h(["name", "age"])

        result = first_set.header()
        self.assertEqual(result, ["name", "age"])

        result = first_set.data()
        self.assertEqual(result, [["First", 30]])

        second_set = structures.rset([["Second", 24]])
        second_set.set_h(["name", "age"])

        first_set.join(second_set)

        first_set.sort_set("age")

        result = first_set.data()
        self.assertEqual(result, [["Second", 24], ["First", 30]])

    def test_rdict(self):
        set = structures.rset([["First", 30], ["Second", 30]])
        set.set_h(["name", "age"])

        iterator = set.rdict_iter()
        iterator = list(iterator)

        first = iterator[0]
        self.assertEqual(first["name"], "First")
        self.assertEqual(first["age"], 30)

        for line in iterator:
            line["salary"] = 100

        result = set.header()
        self.assertEqual(result, ["name", "age", "salary"])

        result = set.data()
        self.assertEqual(result, [["First", 30, 100], ["Second", 30, 100]])
