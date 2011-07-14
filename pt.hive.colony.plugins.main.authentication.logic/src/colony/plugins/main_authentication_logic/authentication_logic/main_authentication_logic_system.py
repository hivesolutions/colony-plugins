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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 1026 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-01-19 23:05:23 +0000 (seg, 19 Jan 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

import main_authentication_logic_exceptions

class MainAuthenticationLogic:
    """
    The main authentication logic class.
    """

    main_authentication_logic_plugin = None
    """ The main authentication logic plugin """

    business_logic_bundle = []
    """ The bundle containing the business logic classes """

    business_logic_bundle_map = {}
    """ The map associating the business logic classes with their names """

    def __init__(self, main_authentication_logic_plugin):
        """
        Constructor of the class.

        @type main_authentication_logic_plugin: MainAuthenticationLogic
        @param main_authentication_logic_plugin: The main authentication logic plugin.
        """

        self.main_authentication_logic_plugin = main_authentication_logic_plugin

        self.business_logic_bundle = []
        self.business_logic_bundle_map = {}

    def generate_classes(self):
        # retrieves the entity manager plugin
        entity_manager_plugin = self.main_authentication_logic_plugin.entity_manager_plugin

        # retrieves the business helper plugin
        business_helper_plugin = self.main_authentication_logic_plugin.business_helper_plugin

        # retrieves the transaction decorator
        transaction_decorator = entity_manager_plugin.get_transaction_decorator()

        # retrieves the lock table decorator
        lock_table_decorator = entity_manager_plugin.get_lock_table_decorator()

        # creates the list of global values
        global_values = [
            transaction_decorator,
            lock_table_decorator,
            main_authentication_logic_exceptions
        ]

        # retrieves the base directory name
        base_directory_name = self.get_path_directory_name()

        # imports the class module
        main_authentication_logic_classes = business_helper_plugin.import_class_module_target("main_authentication_logic_classes", globals(), locals(), global_values, base_directory_name, "main_authentication_logic_classes")

        # sets the business logic bundle
        self.business_logic_bundle = main_authentication_logic_classes.BUSINESS_LOGIC_CLASSES

        # generates the business logic bundle map from the business logic bundle
        self.business_logic_bundle_map = business_helper_plugin.generate_bundle_map(self.business_logic_bundle)

    def get_business_logic_bundle(self):
        return self.business_logic_bundle

    def get_business_logic_bundle_map(self):
        return self.business_logic_bundle_map

    def get_path_directory_name(self):
        return os.path.dirname(__file__)
