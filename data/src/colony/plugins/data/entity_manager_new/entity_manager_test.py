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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.test_util

import entity_manager_exceptions
import entity_manager_test_mocks

class EntityManagerTest:
    """
    The entity manager class.
    """

    entity_manager_plugin = None
    """ The entity manager plugin """

    def __init__(self, entity_manager_plugin):
        """
        Constructor of the class.

        @type entity_manager_plugin: EntityManagerPlugin
        @param entity_manager_plugin: The entity manager plugin.
        """

        self.entity_manager_plugin = entity_manager_plugin

    def get_plugin_test_case_bundle(self):
        return (
            EntityManagerBasePluginTestCase,
        )

    def set_up(self, test_case):
        # retrieves the entity manager (system)
        entity_manager = self.entity_manager_plugin.entity_manager

        # loads a new entity manager, extends it with the
        # entity manager test mocks opens it (loading and
        # generator creation) and begins a new  transaction
        # context (for the current set of operations)
        test_case.entity_manager = entity_manager.load_entity_manager("sqlite")
        test_case.entity_manager.extend_module(entity_manager_test_mocks)
        test_case.entity_manager.open(start = False)
        test_case.entity_manager.create_generator()
        test_case.entity_manager.begin()

    def tear_down(self, test_case):
        # rolls back the current transaction in the
        # entity manager
        test_case.entity_manager.rollback()

        # destroys the underlying data source, removes
        # all files and structures associated with the
        # current entity manager context
        test_case.entity_manager.destroy()

class EntityManagerBaseTestCase(colony.libs.test_util.ColonyTestCase):

    def setUp(self):
        self.plugin.info("Setting up Entity Manager Base Test Case...")

        # retrieves the entity manager test
        self.entity_manager_test = self.plugin.entity_manager_test

        # performs the set up
        self.entity_manager_test.set_up(self)

    def tearDown(self):
        self.plugin.info("Tearing down Entity Manager Base Test Case...")

        # performs the tear down
        self.entity_manager_test.tear_down(self)

    def test_create(self):
        # creates the complete set of entities existent in the current
        # mocks bundle set (this should take a while)
        self.entity_manager.create(entity_manager_test_mocks.RootEntity)
        self.entity_manager.create(entity_manager_test_mocks.Logable)
        self.entity_manager.create(entity_manager_test_mocks.Taxable)
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Employee)
        self.entity_manager.create(entity_manager_test_mocks.Address)
        self.entity_manager.create(entity_manager_test_mocks.Dog)
        self.entity_manager.create(entity_manager_test_mocks.Cat)
        self.entity_manager.create(entity_manager_test_mocks.Car)
        self.entity_manager.create(entity_manager_test_mocks.Supplier)
        self.entity_manager.create(entity_manager_test_mocks.Operation)

        # verifies that all the data source references for the entity classes
        # have been created successfully
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.RootEntity))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Logable))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Taxable))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Person))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Employee))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Address))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Dog))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Cat))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Car))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Supplier))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Operation))

    def test_delete(self):
        # creates the complete set of entities existent in the current
        # mocks bundle set (this should take a while)
        self.entity_manager.create(entity_manager_test_mocks.RootEntity)
        self.entity_manager.create(entity_manager_test_mocks.Logable)
        self.entity_manager.create(entity_manager_test_mocks.Taxable)
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Employee)
        self.entity_manager.create(entity_manager_test_mocks.Address)
        self.entity_manager.create(entity_manager_test_mocks.Dog)
        self.entity_manager.create(entity_manager_test_mocks.Cat)
        self.entity_manager.create(entity_manager_test_mocks.Car)
        self.entity_manager.create(entity_manager_test_mocks.Supplier)
        self.entity_manager.create(entity_manager_test_mocks.Operation)

        # verifies that all the data source references for the entity classes
        # have been created successfully
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.RootEntity))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Logable))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Taxable))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Person))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Employee))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Address))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Dog))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Cat))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Car))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Supplier))
        self.assertTrue(self.entity_manager.exists(entity_manager_test_mocks.Operation))

        # deletes the complete set of entities existent in the current
        # mocks bundle set (this should take a while)
        self.entity_manager.delete(entity_manager_test_mocks.RootEntity)
        self.entity_manager.delete(entity_manager_test_mocks.Logable)
        self.entity_manager.delete(entity_manager_test_mocks.Taxable)
        self.entity_manager.delete(entity_manager_test_mocks.Person)
        self.entity_manager.delete(entity_manager_test_mocks.Employee)
        self.entity_manager.delete(entity_manager_test_mocks.Address)
        self.entity_manager.delete(entity_manager_test_mocks.Dog)
        self.entity_manager.delete(entity_manager_test_mocks.Cat)
        self.entity_manager.delete(entity_manager_test_mocks.Car)
        self.entity_manager.delete(entity_manager_test_mocks.Supplier)
        self.entity_manager.delete(entity_manager_test_mocks.Operation)

        # verifies that all the data source references for the entity classes
        # have been deleted successfully
        self.assertFalse(self.entity_manager.exists(entity_manager_test_mocks.RootEntity))
        self.assertFalse(self.entity_manager.exists(entity_manager_test_mocks.Logable))
        self.assertFalse(self.entity_manager.exists(entity_manager_test_mocks.Taxable))
        self.assertFalse(self.entity_manager.exists(entity_manager_test_mocks.Person))
        self.assertFalse(self.entity_manager.exists(entity_manager_test_mocks.Employee))
        self.assertFalse(self.entity_manager.exists(entity_manager_test_mocks.Address))
        self.assertFalse(self.entity_manager.exists(entity_manager_test_mocks.Dog))
        self.assertFalse(self.entity_manager.exists(entity_manager_test_mocks.Cat))
        self.assertFalse(self.entity_manager.exists(entity_manager_test_mocks.Car))
        self.assertFalse(self.entity_manager.exists(entity_manager_test_mocks.Supplier))
        self.assertFalse(self.entity_manager.exists(entity_manager_test_mocks.Operation))

    def test_save(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Dog)

        # creates the person entity that is going to be used
        # for the verification of the save method and saves it
        person = entity_manager_test_mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(person.object_id, 1)
        self.assertEqual(person.name, "name_person")

        # retrieves the saved person by the unique identifier
        # of it and verifies that the object is not modified
        saved_person = self.entity_manager.get(entity_manager_test_mocks.Person, 1)
        self.assertNotEqual(saved_person, None)

        # verifies that the entity values of the retrieve entity
        # are the same as the original entity
        self.assertEqual(saved_person.object_id, person.object_id)
        self.assertEqual(saved_person.name, person.name)

        # creates the dog entity that is going to be used
        # for the verification of the save of relations
        # then saves it associated with the person
        dog = entity_manager_test_mocks.Dog()
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
        saved_dog = self.entity_manager.get(entity_manager_test_mocks.Dog, 2)
        saved_person = self.entity_manager.get(entity_manager_test_mocks.Person, 1)
        self.assertNotEqual(saved_dog, None)
        self.assertNotEqual(saved_person, None)

        # verifies that both sides of the relations are correct,
        # both the dog is related with the owner and the person
        # with the appropriate dogs
        self.assertEqual(saved_dog.owner.object_id, person.object_id)
        self.assertEqual(saved_person.dogs[0].object_id, dog.object_id)

    def test_self_relation(self):
        # tests relations with himself
        # should include many-to-many (problem)
        pass

    def test_one_to_one(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Address)
        self.entity_manager.create(entity_manager_test_mocks.Employee)

        # creates the the person and address entities and populates
        # them with some values, then sets the person relation
        # in the address side and saves both entities
        person = entity_manager_test_mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        address = entity_manager_test_mocks.Address()
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
        saved_person = self.entity_manager.get(entity_manager_test_mocks.Person, 1)
        saved_address = self.entity_manager.get(entity_manager_test_mocks.Address, 2)
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
        address = entity_manager_test_mocks.Address()
        address.object_id = 3
        address.name = "name_address"
        person = entity_manager_test_mocks.Person()
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
        saved_address = self.entity_manager.get(entity_manager_test_mocks.Address, 3)
        saved_person = self.entity_manager.get(entity_manager_test_mocks.Person, 4)
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
        employee = entity_manager_test_mocks.Employee()
        employee.object_id = 5
        employee.name = "name_employee"
        address = entity_manager_test_mocks.Address()
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
        saved_employee = self.entity_manager.get(entity_manager_test_mocks.Employee, 5)
        saved_address = self.entity_manager.get(entity_manager_test_mocks.Address, 6)
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
        address = entity_manager_test_mocks.Address()
        address.object_id = 7
        address.name = "name_address"
        employee = entity_manager_test_mocks.Employee()
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
        saved_address = self.entity_manager.get(entity_manager_test_mocks.Address, 7)
        saved_employee = self.entity_manager.get(entity_manager_test_mocks.Employee, 8)
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
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Dog)
        self.entity_manager.create(entity_manager_test_mocks.Employee)

        # creates the the person and dog entities and populates
        # them with some values, then sets the owner relation
        # in the dog side and saves both entities
        person = entity_manager_test_mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        dog = entity_manager_test_mocks.Dog()
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
        saved_person = self.entity_manager.get(entity_manager_test_mocks.Person, 1)
        saved_dog = self.entity_manager.get(entity_manager_test_mocks.Dog, 2)
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
        dog = entity_manager_test_mocks.Dog()
        dog.object_id = 3
        dog.name = "name_dog"
        person = entity_manager_test_mocks.Person()
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
        saved_dog = self.entity_manager.get(entity_manager_test_mocks.Dog, 3)
        saved_person = self.entity_manager.get(entity_manager_test_mocks.Person, 4)
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
        employee = entity_manager_test_mocks.Employee()
        employee.object_id = 5
        employee.name = "name_employee"
        dog = entity_manager_test_mocks.Dog()
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
        saved_employee = self.entity_manager.get(entity_manager_test_mocks.Employee, 5)
        saved_dog = self.entity_manager.get(entity_manager_test_mocks.Dog, 6)
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
        dog = entity_manager_test_mocks.Dog()
        dog.object_id = 7
        dog.name = "name_dog"
        employee = entity_manager_test_mocks.Employee()
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
        saved_dog = self.entity_manager.get(entity_manager_test_mocks.Dog, 7)
        saved_employee = self.entity_manager.get(entity_manager_test_mocks.Employee, 8)
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
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Car)
        self.entity_manager.create(entity_manager_test_mocks.Employee)

        # creates the the person and car entities and populates
        # them with some values, then sets the owners relation
        # in the dog side and saves both entities
        person = entity_manager_test_mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        car = entity_manager_test_mocks.Car()
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
        saved_person = self.entity_manager.get(entity_manager_test_mocks.Person, 1)
        saved_car = self.entity_manager.get(entity_manager_test_mocks.Car, 2)
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
        car = entity_manager_test_mocks.Car()
        car.object_id = 3
        car.tires = 4
        person = entity_manager_test_mocks.Person()
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
        saved_car = self.entity_manager.get(entity_manager_test_mocks.Car, 3)
        saved_person = self.entity_manager.get(entity_manager_test_mocks.Person, 4)
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
        employee = entity_manager_test_mocks.Employee()
        employee.object_id = 5
        employee.name = "name_employee"
        car = entity_manager_test_mocks.Car()
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
        saved_employee = self.entity_manager.get(entity_manager_test_mocks.Employee, 5)
        saved_car = self.entity_manager.get(entity_manager_test_mocks.Car, 6)
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
        car = entity_manager_test_mocks.Car()
        car.object_id = 7
        car.tires = 4
        employee = entity_manager_test_mocks.Employee()
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
        saved_car = self.entity_manager.get(entity_manager_test_mocks.Car, 7)
        saved_employee = self.entity_manager.get(entity_manager_test_mocks.Employee, 8)
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

    def test_save_with_cycle(self):
        pass

    def test_find(self):
        # tenho de testar se o find esta a a funcar bem e
        # se as relacoes nao estao lazy nos sitios indicados
        pass

    def test_invalid_relation(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Dog)
        self.entity_manager.create(entity_manager_test_mocks.Car)

        # creates the the person and dog entities and populates
        # them with some values, then sets the owner relation
        # in the dog side and saves both entities, note that no
        # object id is set in the person nor it is generated because
        # no person is saved
        person = entity_manager_test_mocks.Person()
        person.object_id = None
        person.name = "name_person"
        dog = entity_manager_test_mocks.Dog()
        dog.object_id = 1
        dog.name = "name_dog"
        dog.owner = person

        # verifies that an exception is raised because no identifier
        # is set in the person object associated with the dog, cannot
        # associate an item with no identifier
        self.assert_raises(entity_manager_exceptions.ValidationError, self.entity_manager.save, dog)

        # creates the the dog and person entities and populates
        # them with some values, then sets the dogs relation
        # in the person side and saves both entities, note that no
        # object id is set in the dog nor it is generated because
        # no dog is saved
        dog = entity_manager_test_mocks.Dog()
        dog.object_id = None
        dog.name = "name_dog"
        person = entity_manager_test_mocks.Person()
        person.object_id = 2
        person.name = "name_person"
        person.dogs = [dog]

        # verifies that an exception is raised because no identifier
        # is set in the dog object associated with the person, cannot
        # associate an item with no identifier
        self.assert_raises(entity_manager_exceptions.ValidationError, self.entity_manager.save, person)

        # creates the the car and person entities and populates
        # them with some values, then sets the cars relation
        # in the person side and saves both entities, note that no
        # object id is set in the car nor it is generated because
        # no dog is saved
        car = entity_manager_test_mocks.Car()
        car.object_id = None
        car.tires = 4
        person = entity_manager_test_mocks.Person()
        person.object_id = 3
        person.name = "name_person"
        person.cars = [car]

        # verifies that an exception is raised because no identifier
        # is set in the car object associated with the person, cannot
        # associate an item with no identifier
        self.assert_raises(entity_manager_exceptions.ValidationError, self.entity_manager.save, person)

        # creates the the car and dog entities and populates
        # them with some values, then sets the owner relation
        # in the dog side with the (invalid) car value
        car = entity_manager_test_mocks.Car()
        car.object_id = 4
        car.tires = 4
        dog = entity_manager_test_mocks.Dog()
        dog.object_id = 5
        dog.name = "name_dog"
        dog.owner = car

        # verifies that an exception is raised because the type of object
        # for the owner relation in the dog entity is invalid (should be
        # person instead got car)
        self.assert_raises(entity_manager_exceptions.RelationValidationError, self.entity_manager.save, dog)

        # creates the the car and person entities and populates
        # them with some values, then sets the dogs relation
        # in the person side with the (invalid) car value
        car = entity_manager_test_mocks.Car()
        car.object_id = 6
        car.tires = 4
        person = entity_manager_test_mocks.Person()
        person.object_id = 7
        person.name = "name_person"
        person.dogs = [car]

        # verifies that an exception is raised because the type of object
        # for the dogs relation in the dog entity is invalid (should be
        # dog instead got car)
        self.assert_raises(entity_manager_exceptions.RelationValidationError, self.entity_manager.save, person)

        # creates the the dog and car entities and populates
        # them with some values, then sets the owners relation
        # in the car side with the (invalid) dog value
        dog = entity_manager_test_mocks.Dog()
        dog.object_id = 8
        dog.name = "name_dog"
        car = entity_manager_test_mocks.Car()
        car.object_id = 9
        car.tires = 4
        car.owners = [dog]

        # verifies that an exception is raised because the type of object
        # for the owners relation in the car entity is invalid (should be
        # person instead got dog)
        self.assert_raises(entity_manager_exceptions.RelationValidationError, self.entity_manager.save, car)

        # creates the the person and car entities and populates
        # them with some values, then sets the owners relation
        # in the car side with an invalid type value (not sequence)
        person = entity_manager_test_mocks.Person()
        person.object_id = 10
        person.name = "name_person"
        car = entity_manager_test_mocks.Car()
        car.object_id = 11
        car.tires = 4
        car.owners = person

        # verifies that an exception is raised because the type of object
        # for the owners relation in the car entity is invalid (should be
        # a sequence type got a single person instead)
        self.assert_raises(entity_manager_exceptions.ValidationError, self.entity_manager.save, car)

    def test_database_integrity(self):
        # test that the database retains reference
        # integrity through
        pass

    def test_invalid_type(self):
        # tests that the persistence fails when an
        # invalid type is set in one of the fields
        pass

    def test_polymorphism(self):
        # should test the polymorphic part
        # of the entity manager
        pass

    def test_map(self):
        # tests that the map feature of the options
        # map should be working and that the return
        # is a serialized map
        pass

    def test_order_by(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Address)

        # creates the the various person entities and populates
        # them with some ordered values to be able to sort them
        person_a = entity_manager_test_mocks.Person()
        person_a.object_id = 1
        person_a.name = "name_person_a"
        person_c = entity_manager_test_mocks.Person()
        person_c.object_id = 2
        person_c.name = "name_person_c"
        person_b = entity_manager_test_mocks.Person()
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
        persons = self.entity_manager.find(entity_manager_test_mocks.Person, {"order_by" : "name"})

        # verifies that the retrieved list is not empty and that
        # the various persons are ordered in the expected order
        self.assertNotEqual(persons, [])
        self.assertEqual(persons[0].object_id, person_c.object_id)
        self.assertEqual(persons[1].object_id, person_b.object_id)
        self.assertEqual(persons[2].object_id, person_a.object_id)

        # retrieves the persons from the data source ordered
        # by the name attribute in descending order (explicit)
        persons = self.entity_manager.find(entity_manager_test_mocks.Person, {"order_by" : (("name", "descending"),)})

        # verifies that the retrieved list is not empty and that
        # the various persons are ordered in the expected order
        self.assertNotEqual(persons, [])
        self.assertEqual(persons[0].object_id, person_c.object_id)
        self.assertEqual(persons[1].object_id, person_b.object_id)
        self.assertEqual(persons[2].object_id, person_a.object_id)

        # retrieves the persons from the data source ordered
        # by the name attribute in ascending order (explicit)
        persons = self.entity_manager.find(entity_manager_test_mocks.Person, {"order_by" : (("name", "ascending"),)})

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
        address_a = entity_manager_test_mocks.Address()
        address_a.object_id = 4
        address_a.street = "street_address_a"
        address_a.person = person_b
        address_b = entity_manager_test_mocks.Address()
        address_b.object_id = 5
        address_b.street = "street_address_b"
        address_b.person = person_c
        address_c = entity_manager_test_mocks.Address()
        address_c.object_id = 6
        address_c.street = "street_address_c"
        address_c.person = person_a
        self.entity_manager.save(address_a)
        self.entity_manager.save(address_b)
        self.entity_manager.save(address_c)

        # retrieves the persons from the data source ordered
        # by the address street attribute in descending order
        persons = self.entity_manager.find(entity_manager_test_mocks.Person, {"eager" : ("address",), "order_by" : (("address.street", "descending"),)})

        # verifies that the retrieved list is not empty and that
        # the various persons are ordered in the expected order
        self.assertNotEqual(persons, [])
        self.assertEqual(persons[0].object_id, person_a.object_id)
        self.assertEqual(persons[1].object_id, person_c.object_id)
        self.assertEqual(persons[2].object_id, person_b.object_id)

        # retrieves the persons from the data source ordered
        # by the address street attribute in ascending order
        persons = self.entity_manager.find(entity_manager_test_mocks.Person, {"eager" : ("address",), "order_by" : (("address.street", "ascending"),)})

        # verifies that the retrieved list is not empty and that
        # the various persons are ordered in the expected order
        self.assertNotEqual(persons, [])
        self.assertEqual(persons[0].object_id, person_b.object_id)
        self.assertEqual(persons[1].object_id, person_c.object_id)
        self.assertEqual(persons[2].object_id, person_a.object_id)

    def test_range(self):
        # tests that the range part of the query
        # work correctly in every way
        pass

    def test_reload(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Dog)

        # creates a person entity with it's default attributes and
        # saves it into the data source
        person = entity_manager_test_mocks.Person()
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
        person_reload = entity_manager_test_mocks.Person()
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
        dog = entity_manager_test_mocks.Dog()
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
        self.entity_manager.create(entity_manager_test_mocks.Person)

        # creates a person entity with it's default attributes and
        # saves it into the data source
        person = entity_manager_test_mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # counts the amount of entities of type person
        # present in the data source
        count = self.entity_manager.count(entity_manager_test_mocks.Person)

        # verifies that the amount of "persons" in the data
        # source is one (only one persist)
        self.assertEqual(count, 1)

        # creates a person entity with it's default attributes and
        # saves it into the data source
        person = entity_manager_test_mocks.Person()
        person.object_id = 2
        person.name = "name_person"
        self.entity_manager.save(person)

        # counts the amount of entities of type person
        # present in the data source
        count = self.entity_manager.count(entity_manager_test_mocks.Person)

        # verifies that the amount of "persons" in the data
        # source is two (two persists)
        self.assertEqual(count, 2)

    def test_generate_id(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(entity_manager_test_mocks.Person)

        # creates a person entity with it's default attributes and
        # (but no identifier) saves it into the data source
        person = entity_manager_test_mocks.Person()
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
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Employee)
        self.entity_manager.create(entity_manager_test_mocks.Car)

        # creates a person entity with it's default attributes and
        # saves it into the data source
        person = entity_manager_test_mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        self.entity_manager.save(person)

        # verifies that a second (duplicate) save of the entity would
        # result in an integrity error raises from the entity manager
        self.assert_raises("IntegrityError", self.entity_manager.save, person)

        # creates a new employee entity (sub class of person) with the
        # same identifier as the created person
        employee = entity_manager_test_mocks.Employee()
        employee.object_id = 1
        employee.name = "name_employee"

        # verifies that saving the employee also raises an integrity
        # error because the class hierarchy overlaps and the identifier
        # is the same for both objects
        self.assert_raises("IntegrityError", self.entity_manager.save, employee)

        # creates a new employee entity (sub class of root entity and same
        # class hierarchy as the person) with the same identifier as the created
        # person, should also fail on saving
        car = entity_manager_test_mocks.Car()
        car.object_id = 1
        car.tires = 4

        # verifies that saving the car also raises an integrity
        # error because the class hierarchy overlaps and the identifier
        # is the same for both objects (person and car)
        self.assert_raises("IntegrityError", self.entity_manager.save, car)

    def test_validate_relation(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Dog)

        # creates the the person and dog entities and populates
        # them with some values and saves both entities
        person = entity_manager_test_mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        dog = entity_manager_test_mocks.Dog()
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
        person = entity_manager_test_mocks.Person()
        person.object_id = 3
        person.name = "name_person"
        parent = entity_manager_test_mocks.Person()
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
        self.entity_manager.create(entity_manager_test_mocks.RootEntityAbstract)
        self.entity_manager.create(entity_manager_test_mocks.Chair)

        # verifies that all the data source references for the entity classes
        # have been created successfully (or not created depending if the class
        # is abstract or not)
        self.assertFalse(self.entity_manager.has_definition(entity_manager_test_mocks.RootEntityAbstract))
        self.assertTrue(self.entity_manager.has_definition(entity_manager_test_mocks.Chair))

        # creates the the chair entity and populates
        # them with some values and saves the entity
        chair = entity_manager_test_mocks.Chair()
        chair.object_id = 1
        chair.legs = 4
        self.entity_manager.save(chair)

        # verifies that the data remains unchanged after
        # the saving (persistence)
        self.assertEqual(chair.object_id, 1)
        self.assertEqual(chair.legs, 4)

        # retrieves the saved chair by the unique identifier
        # of it and verifies that the object is not modified
        saved_chair = self.entity_manager.get(entity_manager_test_mocks.Chair, 1)
        self.assertNotEqual(saved_chair, None)

        # verifies that the entity values of the retrieve entity
        # are the same as the original entity
        self.assertEqual(saved_chair.object_id, chair.object_id)
        self.assertEqual(saved_chair.legs, chair.legs)

    def test_nullify(self):
        # creates the required entity classes in the data source
        self.entity_manager.create(entity_manager_test_mocks.Person)
        self.entity_manager.create(entity_manager_test_mocks.Address)

        # creates the the person and address entities and populates
        # them with some values, then sets the address relation
        # in the person side and saves both entities
        person = entity_manager_test_mocks.Person()
        person.object_id = 1
        person.name = "name_person"
        address = entity_manager_test_mocks.Address()
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
        # unset attributes in the person are none but that the ones
        # in the address are not
        person.nullify(recursive = False)
        self.assertEqual(person.name, None)
        self.assertNotEqual(address.country, None)

        # creates the the person and address entities and populates
        # them with some values, then sets the address relation
        # in the person side and saves both entities
        person = entity_manager_test_mocks.Person()
        person.object_id = 3
        person.name = "name_person"
        address = entity_manager_test_mocks.Address()
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
        person.nullify(recursive = True)
        self.assertEqual(person.name, None)
        self.assertEqual(address.country, None)

class EntityManagerBasePluginTestCase:

    @staticmethod
    def get_test_case():
        return EntityManagerBaseTestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "Entity Manager Base Plugin test case"
