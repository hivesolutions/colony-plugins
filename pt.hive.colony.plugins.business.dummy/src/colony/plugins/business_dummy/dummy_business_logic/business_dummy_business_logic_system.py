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

__revision__ = "$LastChangedRevision: 7751 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-29 18:12:16 +0100 (seg, 29 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

class BusinessDummyBusinessLogic:
    """
    The business dummy business logic class
    """

    business_dummy_business_logic_plugin = None
    """ The business dummy business logic plugin """

    business_logic_class = None
    """ The business logic class """

    def __init__(self, business_dummy_business_logic_plugin):
        """
        Constructor of the class

        @type business_dummy_business_logic_plugin: BusinessDummyBusinessLogicPlugin
        @param business_dummy_business_logic_plugin: The business dummy business logic plugin
        """

        self.business_dummy_business_logic_plugin = business_dummy_business_logic_plugin

    def generate_class(self):
        # retrieves the entity manager plugin
        entity_manager_plugin = self.business_dummy_business_logic_plugin.entity_manager_plugin

        # retrieves the business helper plugin
        business_helper_plugin = self.business_dummy_business_logic_plugin.business_helper_plugin

        # retrieves the transaction decorator
        transaction_decorator = entity_manager_plugin.get_transaction_decorator()

        # retrieves the lock table decorator
        lock_table_decorator = entity_manager_plugin.get_lock_table_decorator()

        # creates the list of global values
        global_values = [
            transaction_decorator,
            lock_table_decorator
        ]

        # retrieves the base directory name
        base_directory_name = self.get_path_directory_name()

        # imports the class module
        business_dummy_business_logic_class = business_helper_plugin.import_class_module_target("business_dummy_business_logic_class", globals(), locals(), global_values, base_directory_name, "business_dummy_business_logic_class")

        # sets the business logic class
        self.business_logic_class = business_dummy_business_logic_class.DummyBusinessLogic

    def get_business_logic_class(self):
        return self.business_logic_class

    def get_path_directory_name(self):
        return os.path.dirname(__file__)
