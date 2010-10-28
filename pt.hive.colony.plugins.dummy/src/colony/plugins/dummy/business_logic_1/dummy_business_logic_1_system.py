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

        # retrieves the business session manager plugin
        business_session_manager_plugin = self.dummy_business_logic_1_plugin.business_session_manager_plugin

        # retrieves the resource manager plugin
        resource_manager_plugin = self.dummy_business_logic_1_plugin.resource_manager_plugin

        # retrieves the user home path resource
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")

        # retrieves the user home path value
        user_home_path = user_home_path_resource.data

        # retrieves the database file name resource
        database_file_name_resource = resource_manager_plugin.get_resource("system.database.file_name")

        # retrieves the database file name
        database_file_name = database_file_name_resource.data

        # creates the dummy session
        dummy_session = business_session_manager_plugin.load_session_manager_entity_manager("dummy_session", "sqlite", {})

        # retrieves the entity manager
        entity_manager = dummy_session.entity_manager

        # sets the connection parameters for the entity manager
        entity_manager.set_connection_parameters({"file_path" : user_home_path + "/" + database_file_name, "autocommit" : False})

        # loads the entity manager
        entity_manager.load_entity_manager()

        # start the session in the dummy session
        dummy_session.start_session()

        # calls the print dummy method in the dummy business logic entity
        dummy_session.DummyBusinessLogic.print_dummy()

        # calls the save entity method in the dummy business logic entity
        dummy_session.DummyBusinessLogic.save_entity()

        # calls the update entity method in the dummy business logic entity
        dummy_session.DummyBusinessLogic.update_entity()

        # calls the remove entity method in the dummy business logic entity
        dummy_session.DummyBusinessLogic.remove_entity()

        # calls the save remove entity method in the dummy business logic entity
        dummy_session.DummyBusinessLogic.save_remove_entity()

        # calls the save complex entity method in the dummy business logic entity
        dummy_session.DummyBusinessLogic.save_complex_entity()
