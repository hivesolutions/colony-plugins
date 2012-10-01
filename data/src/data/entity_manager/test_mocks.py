#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import structures

class RootEntity(structures.EntityClass):
    """
    The root entity class, this class represents
    a typical base class for a model hierarchy.
    """

    object_id = {
        "id" : True,
        "data_type" : "integer",
        "generated" : True
    }
    """ The object id of the root entity """

    status = {
        "data_type" : "integer"
    }
    """ The status of the entity (1-enabled, 2-disabled) """

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

    object_id = {
        "id" : True,
        "data_type" : "integer",
        "generated" : True
    }
    """ The object id of the root entity abstract """

    status = {
        "data_type" : "integer"
    }
    """ The status of the entity (1-enabled, 2-disabled) """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.object_id = None
        self.status = 1

class Logable(structures.EntityClass):
    """
    The (interface) class that decorates an entity with
    the "logable" attribute for polymorphic retrieval.
    """

    object_id = {
        "id" : True,
        "data_type" : "integer",
        "generated" : True
    }
    """ The object id of the "logable" """

    log_id = {
        "data_type" : "integer",
        "generated" : True,
        "generator_type" : "table",
        "generator_field_name" : "logable_log_id"
    }
    """ The id of the log entry (primary identifier) """

    log_number = {
        "data_type" : "integer"
    }
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

    tax_number = {
        "data_type" : "integer"
    }
    """ The tax number of the taxable """

    def __init__(self):
        RootEntity.__init__(self)

class Person(RootEntity):
    """
    The person entity class, represents the set of typical
    attributes of a person.
    """

    name = {
        "data_type" : "text"
    }
    """ The name of the person """

    age = {
        "data_type" : "integer"
    }
    """ The age of the person """

    parent = {
        "data_type" : "relation"
    }
    """ The parent for the current person """

    children = {
        "data_type" : "relation"
    }
    """ The children of the current person """

    dogs = {
        "data_type" : "relation"
    }
    """ The dogs "owned" by the person """

    cars = {
        "data_type" : "relation"
    }
    """ The cars "owned" by the person """

    employees = {
        "data_type" : "relation"
    }
    """ The employees associated with the person """

    address = {
        "data_type" : "relation"
    }
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
        return {
            "type" : "to-one",
            "target" : Person,
            "reverse" : "children",
            "is_mapper" : True
        }

    @staticmethod
    def _relation_children():
        return {
            "type" : "to-many",
            "target" : Person,
            "reverse" : "parent"
        }

    @staticmethod
    def _relation_dogs():
        return {
            "type" : "to-many",
            "target" : Dog,
            "reverse" : "owner"
        }

    @staticmethod
    def _relation_cars():
        return {
            "type" : "to-many",
            "target" : Car,
            "reverse" : "owners"
        }

    @staticmethod
    def _relation_employees():
        return {
            "type" : "to-many",
            "target" : Employee,
            "reverse" : "boss"
        }

    @staticmethod
    def _relation_address():
        return {
            "type" : "to-one",
            "target" : Address,
            "reverse" : "person",
            "is_mapper" : True
        }

    @staticmethod
    def _attr_double_age(instance):
        return Person._attr(instance, "age") * 2

class Employee(Person, Logable, Taxable):
    """
    The employee entity class, the set of attributes
    contained in this class should be able to represent
    an employee in a typical enterprise system.
    """

    salary = {
        "data_type" : "integer"
    }
    """ The salary of the employee """

    boss = {
        "data_type" : "relation"
    }
    """ The boss of the employee (only one is allowed) """

    def __init__(self):
        """
        Constructor of the class.
        """

        Person.__init__(self)
        Logable.__init__(self)
        Taxable.__init__(self)
        self.salary = 200

    @staticmethod
    def _relation_boss():
        return {
            "type" : "to-one",
            "target" : Person,
            "reverse" : "employees",
            "is_mapper" : True
        }

class Address(RootEntity):
    """
    The address entity class, representing the typical
    set of attributes for a postal address.
    """

    street = {
        "data_type" : "text"
    }
    """ The street of the address """

    number = {
        "data_type" : "integer"
    }
    """ The door number of the address """

    country = {
        "data_type" : "text"
    }
    """ The country of the address """

    person = {
        "data_type" : "relation"
    }
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
        return {
            "type" : "to-one",
            "target" : Person,
            "reverse" : "address"
        }

class Dog(RootEntity):
    """
    The dog entity class, representing the typical
    attribute of a pet with the characteristics
    of a dog.
    """

    name = {
        "data_type" : "text"
    }
    """ The name of the dog """

    owner = {
        "data_type" : "relation"
    }
    """ The owner of the dog """

    enemy = {
        "data_type" : "relation"
    }
    """ The enemy of the dog """

    def __init__(self):
        """
        Constructor for the class.
        """

        RootEntity.__init__(self)
        self.name = "Anonymous"

    @staticmethod
    def _relation_owner():
        return {
            "type" : "to-one",
            "target" : Person,
            "reverse" : "dogs",
            "is_mapper" : True
        }

    @staticmethod
    def _relation_enemy():
        return {
            "type" : "to-one",
            "target" : Cat,
            "is_mapper" : True
        }

class Cat(RootEntity):
    """
    The cat entity class, representing the typical
    attribute of a pet with the characteristics
    of a cat.
    """

    name = {
        "data_type" : "text"
    }
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

    tires = {
        "data_type" : "integer"
    }
    """ The salary of the cat """

    owners = {
        "data_type" : "relation"
    }
    """ The owner of the car """

    suppliers = {
        "data_type" : "relation"
    }
    """ The suppliers of spare parts to the car """

    mechanic = {
        "data_type" : "relation"
    }
    """ The mechanic (person) to be used to repair the car """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.tires = 4

    @staticmethod
    def _relation_owners():
        return {
            "type" : "to-many",
            "target" : Person,
            "reverse" : "cars"
        }

    @staticmethod
    def _relation_suppliers():
        return {
            "type" : "to-many",
            "target" : Supplier
        }

    @staticmethod
    def _relation_mechanic():
        return {
            "type" : "to-one",
            "target" : Person
        }

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

class Operation(Logable):
    """
    The operation entity class, representing a logical
    operation and attributes.
    """

    name = {
        "data_type" : "text"
    }
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

    legs = {
        "data_type" : "integer"
    }
    """ The salary of the cat """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntityAbstract.__init__(self)
        self.legs = 4

class File(RootEntity):
    """
    The file entity class, that represent a typical file
    in the normal computer file system.
    """

    filename = {
        "data_type" : "text"
    }
    """ The name (representation) of the file """

    data = {
        "data_type" : "data"
    }
    """ The (binary) data of the file """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.filename = "undefined"
