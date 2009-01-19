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

class DummyBusinessLogic:

    def print_dummy(self):
        print "dummy echo"

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
        dummy_entity_instance.address = "Tobias Street, 120"

        # saves the entity instance
        self.entity_manager.save(dummy_entity_instance)

        # sets the entity name
        self.name = dummy_entity_instance.name 

    @transaction_decorator("requires")
    def remove_entity(self):
        # retrieves the DummyEntity class from the entity manager
        dummy_entity_class = self.entity_manager.get_entity_class("DummyEntity")

        # creates a new dummy entity instance
        dummy_entity_instance = dummy_entity_class()

        # sets the entity attribute values
        dummy_entity_instance.name = self.name

        # removes the entity instance
        self.entity_manager.remove(dummy_entity_instance)

    @transaction_decorator("requires")
    def save_remove_entity(self):
        # saves the entity instance
        self.save_entity()

        # removes the entity instance
        self.remove_entity()
