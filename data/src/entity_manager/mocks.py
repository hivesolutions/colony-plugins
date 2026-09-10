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

from . import structures


class RootEntity(structures.EntityClass):
    """
    The root entity class, this class represents
    a typical base class for a model hierarchy.
    """

    object_id = dict(id=True, type="integer", generated=True)
    """ The object id of the root entity """

    status = dict(type="integer")
    """ The status of the entity (1-enabled, 2-disabled) """

    metadata = dict(type="metadata")
    """ Simple metadata value that is going to be used
    for storage of structured data (maps and lists) """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.object_id = None
        self.status = 1


class RootEntityAbstract(structures.EntityClass):
    """
    The root entity abstract class, this class represents
    a typical base class for a model hierarchy.

    This version is set as an abstract class so that no
    representation of it is created in the data source.
    """

    abstract = True
    """ Abstract class flag, indicating that this class is not
    meant to be stored in the data source """

    object_id = dict(id=True, type="integer", generated=True)
    """ The object id of the root entity abstract """

    status = dict(type="integer")
    """ The status of the entity (1-enabled, 2-disabled) """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.object_id = None
        self.status = 1


class Loggable(structures.EntityClass):
    """
    The (interface) class that decorates an entity with
    the "loggable" attribute for polymorphic retrieval.
    """

    object_id = dict(id=True, type="integer", generated=True)
    """ The object id of the "loggable" """

    log_id = dict(
        type="integer",
        generated=True,
        generator_type="table",
        generator_field_name="logable_log_id",
    )
    """ The id of the log entry (primary identifier) """

    log_number = dict(type="integer")
    """ The log number of the taxable """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.object_id = None
        self.log_id = None
        self.log_number = 1009


class Taxable(RootEntity):
    """
    The (interface) class that decorates an entity with
    the taxable attribute for polymorphic retrieval.
    """

    tax_number = dict(type="integer")
    """ The tax number of the taxable """

    def __init__(self):
        RootEntity.__init__(self)


class Person(RootEntity):
    """
    The person entity class, represents the set of typical
    attributes of a person.
    """

    name = dict(type="text")
    """ The name of the person """

    age = dict(type="integer")
    """ The age of the person """

    weight = dict(type="decimal")
    """ The weight of the person """

    parent = dict(type="relation")
    """ The parent for the current person """

    children = dict(type="relation")
    """ The children of the current person """

    dogs = dict(type="relation")
    """ The dogs "owned" by the person """

    cars = dict(type="relation")
    """ The cars "owned" by the person """

    employees = dict(type="relation")
    """ The employees associated with the person """

    address = dict(type="relation")
    """ The address associated with the person """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.name = "Anonymous"
        self.age = 18

    @staticmethod
    def _relation_parent():
        return dict(type="to-one", target=Person, reverse="children", is_mapper=True)

    @staticmethod
    def _relation_children():
        return dict(type="to-many", target=Person, reverse="parent")

    @staticmethod
    def _relation_dogs():
        return dict(type="to-many", target=Dog, reverse="owner")

    @staticmethod
    def _relation_cars():
        return dict(type="to-many", target=Car, reverse="owners")

    @staticmethod
    def _relation_employees():
        return dict(type="to-many", target=Employee, reverse="boss")

    @staticmethod
    def _relation_address():
        return dict(type="to-one", target=Address, reverse="person", is_mapper=True)

    @classmethod
    def _attr_double_age(cls, instance):
        return cls._attr(instance, "age") * 2


class Employee(Person, Loggable, Taxable):
    """
    The employee entity class, the set of attributes
    contained in this class should be able to represent
    an employee in a typical enterprise system.
    """

    salary = dict(type="integer")
    """ The salary of the employee """

    boss = dict(type="relation")
    """ The boss of the employee (only one is allowed) """

    def __init__(self):
        """
        Constructor of the class.
        """

        Person.__init__(self)
        Loggable.__init__(self)
        Taxable.__init__(self)
        self.salary = 200

    @staticmethod
    def _relation_boss():
        return dict(type="to-one", target=Person, reverse="employees", is_mapper=True)


class Breeder(Person):
    """
    The specialized version of a person that takes care of a
    professional/specialized dog or cat.
    """

    license_number = dict(type="text")
    """ The license number as a set of characters for the
    breeder that is going to identify him professionally """

    @staticmethod
    def _relation_dogs():
        return dict(type="to-many", target=BreedDog, reverse="owner")


class Address(RootEntity):
    """
    The address entity class, representing the typical
    set of attributes for a postal address.
    """

    street = dict(type="text")
    """ The street of the address """

    number = dict(type="integer")
    """ The door number of the address """

    country = dict(type="text")
    """ The country of the address """

    person = dict(type="relation")
    """ The person associated with the address """

    def __init__(self):
        """
        Constructor for the class.
        """

        RootEntity.__init__(self)
        self.street = "N/A"
        self.number = 0
        self.country = "N/A"

    @staticmethod
    def _relation_person():
        return dict(type="to-one", target=Person, reverse="address")


class Dog(RootEntity):
    """
    The dog entity class, representing the typical
    attribute of a pet with the characteristics
    of a dog.
    """

    name = dict(type="text")
    """ The name of the dog """

    owner = dict(type="relation")
    """ The owner of the dog """

    enemy = dict(type="relation")
    """ The enemy of the dog """

    def __init__(self):
        """
        Constructor for the class.
        """

        RootEntity.__init__(self)
        self.name = "Anonymous"

    @staticmethod
    def _relation_owner():
        return dict(type="to-one", target=Person, reverse="dogs", is_mapper=True)

    @staticmethod
    def _relation_enemy():
        return dict(type="to-one", target=Cat, is_mapper=True)


class BreedDog(Dog):
    """
    The specialized dog class for dogs that are meant to be
    adopted by proper breeders, should contain special attributes
    like the digital tag.
    """

    digital_tag = dict(type="text")
    """ The digital tag of the dog, meant to identify
    it in any intervention """

    @staticmethod
    def _relation_owner():
        return dict(type="to-one", target=Breeder, reverse="dogs", is_mapper=True)


class Cat(RootEntity):
    """
    The cat entity class, representing the typical
    attribute of a pet with the characteristics
    of a cat.
    """

    name = dict(type="text")
    """ The name of the cat """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.name = "Anonymous"


class Car(RootEntity):
    """
    The car entity class, representing the car vehicle
    typical attributes.
    """

    tires = dict(type="integer")
    """ The salary of the cat """

    owners = dict(type="relation")
    """ The owner of the car """

    suppliers = dict(type="relation")
    """ The suppliers of spare parts to the car """

    mechanic = dict(type="relation")
    """ The mechanic (person) to be used to repair the car """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.tires = 4

    @staticmethod
    def _relation_owners():
        return dict(type="to-many", target=Person, reverse="cars")

    @staticmethod
    def _relation_suppliers():
        return dict(type="to-many", target=Supplier)

    @staticmethod
    def _relation_mechanic():
        return dict(type="to-one", target=Person)


class Supplier(RootEntity):
    """
    The car entity class, representing the car vehicle
    typical attributes.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass


class Operation(Loggable):
    """
    The operation entity class, representing a logical
    operation and attributes.
    """

    name = dict(type="text")
    """ The name of the operation """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.name = "Transaction"


class Chair(RootEntityAbstract):
    """
    The chair entity class, representing the chair (furniture)
    typical attributes.
    """

    legs = dict(type="integer")
    """ The salary of the cat """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntityAbstract.__init__(self)
        self.legs = 4


class ConcreteRootEntity(structures.EntityClass):
    """
    The concrete root entity class, this class represents
    a typical base class for a model hierarchy using the
    concrete table inheritance strategy.
    """

    inheritance = "concrete_table"
    """ Concrete table inheritance strategy, each concrete
    class stores all attributes in a single table """

    object_id = dict(id=True, type="integer", generated=True)
    """ The object id of the concrete root entity """

    status = dict(type="integer")
    """ The status of the entity (1-enabled, 2-disabled) """

    metadata = dict(type="metadata")
    """ Simple metadata value that is going to be used
    for storage of structured data (maps and lists) """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.object_id = None
        self.status = 1


class ConcretePerson(ConcreteRootEntity):
    """
    The concrete person entity class, represents the set of
    typical attributes of a person using concrete table
    inheritance.
    """

    name = dict(type="text")
    """ The name of the person """

    age = dict(type="integer")
    """ The age of the person """

    weight = dict(type="decimal")
    """ The weight of the person """

    parent = dict(type="relation")
    """ The parent for the current person """

    children = dict(type="relation")
    """ The children of the current person """

    employees = dict(type="relation")
    """ The employees associated with the person """

    address = dict(type="relation")
    """ The address associated with the person """

    def __init__(self):
        """
        Constructor of the class.
        """

        ConcreteRootEntity.__init__(self)
        self.name = "Anonymous"
        self.age = 18

    @staticmethod
    def _relation_parent():
        return dict(
            type="to-one", target=ConcretePerson, reverse="children", is_mapper=True
        )

    @staticmethod
    def _relation_children():
        return dict(type="to-many", target=ConcretePerson, reverse="parent")

    @staticmethod
    def _relation_employees():
        return dict(type="to-many", target=ConcreteEmployee, reverse="boss")

    @staticmethod
    def _relation_address():
        return dict(
            type="to-one",
            target=ConcreteAddress,
            reverse="person",
            is_mapper=True,
        )


class ConcreteEmployee(ConcretePerson):
    """
    The concrete employee entity class, the set of attributes
    contained in this class should be able to represent
    an employee using concrete table inheritance.
    """

    salary = dict(type="integer")
    """ The salary of the employee """

    boss = dict(type="relation")
    """ The boss of the employee (only one is allowed) """

    def __init__(self):
        """
        Constructor of the class.
        """

        ConcretePerson.__init__(self)
        self.salary = 200

    @staticmethod
    def _relation_boss():
        return dict(
            type="to-one", target=ConcretePerson, reverse="employees", is_mapper=True
        )


class ConcreteAddress(ConcreteRootEntity):
    """
    The concrete address entity class, representing the typical
    set of attributes for a postal address using concrete table
    inheritance.
    """

    street = dict(type="text")
    """ The street of the address """

    number = dict(type="integer")
    """ The door number of the address """

    country = dict(type="text")
    """ The country of the address """

    person = dict(type="relation")
    """ The person associated with the address """

    def __init__(self):
        """
        Constructor for the class.
        """

        ConcreteRootEntity.__init__(self)
        self.street = "N/A"
        self.number = 0
        self.country = "N/A"

    @staticmethod
    def _relation_person():
        return dict(type="to-one", target=ConcretePerson, reverse="address")


class ConcreteAbstract(structures.EntityClass):
    """
    The concrete abstract entity class, this class represents the
    root of a concrete table hierarchy that starts with an abstract
    class, so that no representation of it is created in the data
    source but its attributes are still inherited downwards.
    """

    abstract = True
    """ Abstract class flag, indicating that this class is not
    meant to be stored in the data source """

    inheritance = "concrete_table"
    """ Concrete table inheritance strategy, each concrete
    class stores all attributes in a single table """

    object_id = dict(id=True, type="integer", generated=True)
    """ The object id of the concrete abstract """

    status = dict(type="integer")
    """ The status of the entity (1-enabled, 2-disabled) """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.object_id = None
        self.status = 1


class ConcreteAbstractPerson(ConcreteAbstract):
    """
    The concrete abstract person entity class, the first concrete
    class of a hierarchy whose root is abstract, used to verify that
    abstract ancestors are skipped in the write operations.
    """

    name = dict(type="text")
    """ The name of the concrete abstract person """

    age = dict(type="integer")
    """ The age of the concrete abstract person """

    def __init__(self):
        """
        Constructor of the class.
        """

        ConcreteAbstract.__init__(self)
        self.name = "Anonymous"
        self.age = 18


class ConcreteAbstractEmployee(ConcreteAbstractPerson):
    """
    The concrete abstract employee entity class, the second concrete
    level of a hierarchy whose root is abstract.
    """

    salary = dict(type="integer")
    """ The salary of the concrete abstract employee """

    def __init__(self):
        """
        Constructor of the class.
        """

        ConcreteAbstractPerson.__init__(self)
        self.salary = 200


class MigrationRootEntity(structures.EntityClass):
    """
    The migration root entity class, the root of a narrow class
    table hierarchy used to exercise the inheritance strategy
    migration operations.
    """

    object_id = dict(id=True, type="integer", generated=True)
    """ The object id of the migration root entity """

    status = dict(type="integer")
    """ The status of the entity (1-enabled, 2-disabled) """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.object_id = None
        self.status = 1


class MigrationPerson(MigrationRootEntity):
    """
    The migration person entity class, the intermediate level of
    the class table hierarchy used for the migration operations.
    """

    name = dict(type="text")
    """ The name of the migration person """

    age = dict(type="integer")
    """ The age of the migration person """

    def __init__(self):
        """
        Constructor of the class.
        """

        MigrationRootEntity.__init__(self)
        self.name = "Anonymous"
        self.age = 18


class MigrationEmployee(MigrationPerson):
    """
    The migration employee entity class, the bottom level of the
    class table hierarchy used for the migration operations.
    """

    salary = dict(type="integer")
    """ The salary of the migration employee """

    def __init__(self):
        """
        Constructor of the class.
        """

        MigrationPerson.__init__(self)
        self.salary = 200


class MigrationConcreteRoot(structures.EntityClass):
    """
    The migration concrete root entity class, the root of a narrow
    concrete table hierarchy used to exercise the inheritance
    strategy migration operations in the reverse direction.
    """

    inheritance = "concrete_table"
    """ Concrete table inheritance strategy, each concrete
    class stores all attributes in a single table """

    object_id = dict(id=True, type="integer", generated=True)
    """ The object id of the migration concrete root """

    status = dict(type="integer")
    """ The status of the entity (1-enabled, 2-disabled) """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.object_id = None
        self.status = 1


class MigrationConcretePerson(MigrationConcreteRoot):
    """
    The migration concrete person entity class, the intermediate
    level of the concrete table hierarchy used for the migration
    operations.
    """

    name = dict(type="text")
    """ The name of the migration concrete person """

    age = dict(type="integer")
    """ The age of the migration concrete person """

    def __init__(self):
        """
        Constructor of the class.
        """

        MigrationConcreteRoot.__init__(self)
        self.name = "Anonymous"
        self.age = 18


class MigrationConcreteEmployee(MigrationConcretePerson):
    """
    The migration concrete employee entity class, the bottom level
    of the concrete table hierarchy used for the migration
    operations.
    """

    salary = dict(type="integer")
    """ The salary of the migration concrete employee """

    def __init__(self):
        """
        Constructor of the class.
        """

        MigrationConcretePerson.__init__(self)
        self.salary = 200


class MigrationMixedRoot(structures.EntityClass):
    """
    The migration mixed root entity class, the root of a hierarchy
    whose descendant declares a different inheritance strategy, used
    to verify that such a misconfiguration is rejected before any
    migration is attempted.
    """

    object_id = dict(id=True, type="integer", generated=True)
    """ The object id of the migration mixed root """

    status = dict(type="integer")
    """ The status of the entity (1-enabled, 2-disabled) """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.object_id = None
        self.status = 1


class MigrationMixedChild(MigrationMixedRoot):
    """
    The migration mixed child entity class, declares an inheritance
    strategy that conflicts with the one of its own root class.
    """

    inheritance = "concrete_table"
    """ Concrete table inheritance strategy, deliberately conflicting
    with the strategy of the root of the hierarchy """

    name = dict(type="text")
    """ The name of the migration mixed child """

    def __init__(self):
        """
        Constructor of the class.
        """

        MigrationMixedRoot.__init__(self)
        self.name = "Anonymous"


class File(RootEntity):
    """
    The file entity class, that represent a typical file
    in the normal computer file system.
    """

    filename = dict(type="text")
    """ The name (representation) of the file """

    data = dict(type="data")
    """ The (binary) data of the file """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.filename = "undefined"


class MockFailingCursor(object):
    """
    The mock cursor class that fails the execution of the queries
    that change the structure (or the contents) of the data source,
    used to simulate a failure in the middle of a migration.
    """

    MIGRATION_PREFIXES = ("create ", "insert ", "drop ", "alter ")
    """ The tuple containing the prefixes of the queries that are
    considered to be part of a migration, the ones that are going
    to be failed once the failure threshold has been reached """

    def __init__(self, cursor, fail_after=0):
        """
        Constructor of the class.

        :type cursor: Cursor
        :param cursor: The concrete cursor to which the operations
        are going to be delegated.
        :type fail_after: int
        :param fail_after: The number of migration queries that are
        allowed to be executed before the failure is triggered.
        """

        self.cursor = cursor
        self.fail_after = fail_after
        self.count = 0

    def execute(self, query, *args):
        # verifies if the query is one of the queries that change the
        # data source, the other ones are always allowed as they are
        # part of the inspection of the current structure
        is_migration = query.startswith(MockFailingCursor.MIGRATION_PREFIXES)

        # in case the query is a migration one increments the counter
        # and raises an exception once the threshold is exceeded
        if is_migration:
            self.count += 1
            if self.count > self.fail_after:
                raise RuntimeError("simulated migration failure")

        return self.cursor.execute(query, *args)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        return self.cursor.close()


class MockFailingConnection(object):
    """
    The mock connection class that creates cursors that fail the
    execution of the migration queries, used to verify both the
    backup and the rollback steps of a migration.
    """

    def __init__(self, connection, fail_after=0, rollback_fails=False):
        """
        Constructor of the class.

        :type connection: Connection
        :param connection: The concrete connection to which the
        operations are going to be delegated.
        :type fail_after: int
        :param fail_after: The number of migration queries that are
        allowed to be executed before the failure is triggered.
        :type rollback_fails: bool
        :param rollback_fails: If the rollback operation should also
        fail, simulating a connection that is no longer usable.
        """

        self.connection = connection
        self.fail_after = fail_after
        self.rollback_fails = rollback_fails
        self.rolled_back = False

    def cursor(self):
        return MockFailingCursor(self.connection.cursor(), self.fail_after)

    def commit(self):
        return self.connection.commit()

    def rollback(self):
        self.rolled_back = True
        if self.rollback_fails:
            raise RuntimeError("simulated rollback failure")
        return self.connection.rollback()


class MockRecordingCursor(object):
    """
    The mock cursor class that records the queries executed through
    it and answers them with a fixed result, used to verify the
    engine specific queries without the corresponding data source.
    """

    def __init__(self, queries, result=(1,)):
        """
        Constructor of the class.

        :type queries: List
        :param queries: The list where the executed queries are
        going to be recorded.
        :type result: Tuple
        :param result: The row that is going to be answered for
        every one of the executed queries.
        """

        self.queries = queries
        self.result = result

    def execute(self, query, *args):
        self.queries.append(query)

    def fetchone(self):
        return self.result

    def fetchall(self):
        return [self.result]

    def close(self):
        pass


class MockRecordingConnection(object):
    """
    The mock connection class that creates cursors recording the
    queries executed through them, used to verify the queries that
    target data sources other than the one in use.
    """

    def __init__(self, result=(1,)):
        """
        Constructor of the class.

        :type result: Tuple
        :param result: The row that is going to be answered for
        every one of the executed queries.
        """

        self.queries = []
        self.result = result

    def cursor(self):
        return MockRecordingCursor(self.queries, self.result)

    def commit(self):
        pass

    def rollback(self):
        pass
