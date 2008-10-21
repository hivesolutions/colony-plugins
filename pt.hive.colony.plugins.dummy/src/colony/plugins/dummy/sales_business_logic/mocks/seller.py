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

__author__ = "Simão Rio <srio@hive.pt>"
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

global dummy
import dummy.sales_business_logic.mocks.inventory

class Seller:
    """
    The dummy seller class.
    """
    id = None
    preferred_name = None
    organizational_hierarchy_merchandise_supplier = None
    inventory = None
    sales_as_seller = None
    sales_as_stockholder = None

    def __init__(self):
        self.id = 55
        self.preferred_name = 'Simao e seus amigos os vendedores'
        self.organizational_hierarchy_merchandise_supplier = []
        inventory = dummy.sales_business_logic.mocks.inventory.Inventory()
        self.inventory = [inventory]
        self.sales_as_seller = []
        self.sales_as_stockholder = []

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

