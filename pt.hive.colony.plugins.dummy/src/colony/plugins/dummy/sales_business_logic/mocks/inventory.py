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

class Inventory:
    """
    The dummy inventory class.
    """
    id = None
    merchandise_id = None
    contactable_id = None
    stock_on_hand = None
    price = None
    discount = None
    max_stock = None
    min_stock = None
    stock_in_transit = None
    stock_reserved = None
    margin = None
    
    def __init__(self):
        self.id = 22
        self.merchandise_id = 11
        self.contactable_id = 55
        self.stock_on_hand = 23
        self.price = 33.33
        self.discount = 11.11
        self.max_stock = 40
        self.min_stock = 5
        self.stock_in_transit = 2
        self.stock_reserved = 2
        self.margin = 44.44

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_stock_on_hand(self):
        return self.stock_on_hand