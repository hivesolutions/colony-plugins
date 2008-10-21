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

__revision__ = "$LastChangedRevision: 1613 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-08-07 18:17:10 +0100 (Qui, 07 Ago 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

global dummy
import dummy.sales_business_logic.mocks.merchandise
import dummy.sales_business_logic.mocks.seller

class SaleLine:
    id = None
    merchandise = None
    seller = None
    quantity = None
    price = None
    discount = None
    warranty_duration = None
    
    def __init__(self):
        self.id = 44
        self.merchandise = dummy.sales_business_logic.mocks.merchandise.Merchandise()
        self.seller = dummy.sales_business_logic.mocks.seller.Seller()
        self.quantity = 4
        self.price = 33.33
        self.discount = 11.11
        self.warranty_duration = 40

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_quantity(self):
        return self.quantity
    
    def get_by_id(self):
        return self