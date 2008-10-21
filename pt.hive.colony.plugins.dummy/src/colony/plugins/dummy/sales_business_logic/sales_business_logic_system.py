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
import datetime
import dummy.sales_business_logic.mocks.sale

class DummySalesBusinessLogic:
    """
    The dummy sales business logic class.
    """

    sales_business_logic_plugin = None
    """ The dummy sales business logic plugin """

    def __init__(self, sales_business_logic_plugin):
        """
        Constructor of the class
        
        @type dummy_sales_business_logic_plugin: DummySalesBusinessLogicPlugin
        @param dummy_sales_business_logic_plugin: The dummy sales business logic plugin
        """

        self.sales_business_logic_plugin = sales_business_logic_plugin

#sblp = plugin_manager.get_plugin_by_id("pt.hive.colony.plugins.dummy.sales_business_logic")

    def create_sale(self, keys, values):
        """
        #sellers_stockholders, customers_stockholders, sellers_participants, customers_participants, merchandise_lines, payments
        Create and execute a new sales instance
        """

        # create sale instance
        sale = dummy.sales_business_logic.mocks.sale.Sale()
        
        # decrease available inventory at Seller
        sale_lines = sale.sale_lines
        
        # update warranty of items sold
        for sale_line in sale_lines:
            today = datetime.date.today()
            warranty_time = datetime.timedelta(days = sale_line.merchandise.warranty)
            sale_line.warranty_duration = today + warranty_time
        
        #generate invoice
        
        
        
        print('create sale')
    
    def read_sale(self, sale_id):
        print('read sale')
    
    def update_sale(self, keys, values):
        print('update sale')

    def delete_sale(self, sale_id):
        print('delete sale')
        
    def list_sales(self):
        print('list sales')
