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

import colony

from . import mocks
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
            EntityManagerRsetTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

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
        Tests the on-to-many relations saving and retrieval
        of values.

        == Objectives ==
        * Tests that the persistence layer correctly saves
        one to many relations.
        * Tests that the retrieval method correctly retrieves
        one to many relations.
        * Tests that both sides of the (one-to-many) relation
        can be used for saving of the relation.
        * Test that parent (on-to-many) relations are correctly
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
        return "Entity Manager Concrete Table Inheritance test case"

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
