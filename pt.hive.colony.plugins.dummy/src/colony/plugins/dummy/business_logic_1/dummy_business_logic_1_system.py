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

__revision__ = "$LastChangedRevision: 1613 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-08-07 18:17:10 +0100 (Thu, 07 Aug 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class DummyBusinessLogic1:
    """
    The dummy business logic 1 class.
    """

    dummy_business_logic_1_plugin = None
    """ The dummy business logic 1 plugin """

    def __init__(self, dummy_business_logic_1_plugin):
        """
        Constructor of the class.
        
        @type dummy_business_logic_1_plugin: DummyBusinessLogic1Plugin
        @param dummy_business_logic_1_plugin: The dummy business logic 1 plugin.
        """

        self.dummy_business_logic_1_plugin = dummy_business_logic_1_plugin

    def create_dummy_session(self):
        """
        Creates a dummy session to test it.
        """

        # creates the session manager
        session_manager = self.dummy_business_logic_1_plugin.business_session_manager_plugin.load_session_manager_entity_manager("dummy_session", "sqlite")

        # retrieves the entity manager
        entity_manager = session_manager.entity_manager

        # sets the connection parameters for the entity manager
        entity_manager.set_connection_parameters({"file_path" : "/Users/joamag/test_database.db", "autocommit" : False})

        # loads the entity manager
        entity_manager.load_entity_manager()

        # start the session in the session manager
        session_manager.start_session()

        # calls the print dummy method in the dummy business logic entity
        session_manager.DummyBusinessLogic.print_dummy()

        # calls the save entity method in the dummy business logi entity
        session_manager.DummyBusinessLogic.save_entity()
