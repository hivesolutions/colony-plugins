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

__revision__ = "$LastChangedRevision: 2021 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-15 02:04:33 +0100 (Wed, 15 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class BusinessSessionManager:
    """
    The business session manager class
    """

    business_session_manager_plugin = None
    """ The business session manager plugin """

    active_session_manager_list = []
    """ The list of active session managers """

    loaded_business_logic_classes_list = []
    """ The list of loaded business logic classes """

    loaded_business_logic_classes_map = {}
    """ The map associating the loaded business logic classes with their names """

    def __init__(self, business_session_manager_plugin):
        """
        Constructor of the class
        
        @type business_session_manager_plugin: BusinessSessionManagerPlugin
        @param business_session_manager_plugin: The business session manager plugin
        """

        self.business_session_manager_plugin = business_session_manager_plugin

        self.active_session_manager_list = []
        self.loaded_business_logic_classes_list = []
        self.loaded_business_logic_classes_map = {}

    def load_business_logic_class(self, business_logic_class):
        # retrieves the business logic class name
        business_logic_name = business_logic_class.__name__

        self.loaded_business_logic_classes_list.append(business_logic_class)
        self.loaded_business_logic_classes_map[business_logic_name] = business_logic_class

    def unload_business_logic_class(self, business_logic_class):
        # retrieves the business logic class name
        business_logic_name = business_logic_class.__name__

        if business_logic_class in self.loaded_business_logic_classes_list:
            self.loaded_business_logic_classes_list.remove(business_logic_class)

        if business_logic_name in self.loaded_business_logic_classes_map:
            del self.loaded_business_logic_classes_map[business_logic_name]

    def load_business_logic_bundle(self, business_logic_bundle):
        for business_logic_class in business_logic_bundle:
            self.load_business_logic_class(business_logic_class)

    def unload_business_logic_bundle(self, business_logic_bundle):
        for business_logic_class in entity_bundle:
            self.unload_business_logic_class(business_logic_class)

    def load_session_manager(self, session_name, entity_manager = None):
        # creates the session manager
        session_manager = SessionManager(session_name, self.loaded_business_logic_classes_list, self.loaded_business_logic_classes_map, entity_manager)

        # adds the created session manager to the list of active session managers
        self.active_session_manager_list.append(session_manager)

        # returns the created session manager
        return session_manager

    def load_session_manager_entity_manager(self, session_name, engine_name):
        # retrieves the business entity manager plugin
        business_entity_manager_plugin = self.business_session_manager_plugin.business_entity_manager_plugin

        # creates the entity manager
        entity_manager = business_entity_manager_plugin.load_entity_manager(engine_name)

        # creates the session manager and returns it
        return self.load_session_manager(session_name, entity_manager)

class SessionManager:
    """
    The session manager class.
    """

    session_name = "none"
    """ The name of the current session """

    business_logic_classes_list = []
    """ The list of business logic classes """

    business_logic_classes_map = {}
    """ The map associating the business logic classes with their names """

    entity_manager = None
    """ The entity manager associated with the current session"""

    business_logic_instances_list = []
    """ The list of business logic instances """

    business_logic_instances_map = {}
    """ The map associating the business logic instances with their names """

    def __init__(self, session_name, business_logic_classes_list, business_logic_classes_map, entity_manager = None):
        self.session_name = session_name
        self.business_logic_classes_list = business_logic_classes_list
        self.business_logic_classes_map = business_logic_classes_map
        self.entity_manager = entity_manager

        self.business_logic_instances_list = []
        self.business_logic_instances_map = {}

    def start_session(self):
        """
        Starts the session in the session manager.
        """

        self.instantiate_business_logic()
        self.inject_session_manager()
        self.inject_business_logic()

    def stop_session(self):
        """
        Stops the session in the session manager.
        """

        pass

    def instantiate_business_logic(self):
        # iterates over the business logic classes map
        for business_logic_class_name in self.business_logic_classes_map:
            # retrieves the business logic class
            business_logic_class = self.business_logic_classes_map[business_logic_class_name]

            # creates the business logic instance
            business_logic_instance = business_logic_class()

            # adds the business logic instance to the list of business logic instances
            self.business_logic_instances_list.append(business_logic_instance)

            # associates the business logic class name with the business logic instance
            self.business_logic_instances_map[business_logic_class_name] = business_logic_instance

    def inject_session_manager(self):
        # iterates over all the business logic classes
        for business_logic_class in self.business_logic_classes_list:
            setattr(business_logic_class, "entity_manager", self.entity_manager)

    def inject_business_logic(self):
        # iterates over the business logic instance map
        for business_logic_instance_name in self.business_logic_instances_map:
            # retrieves the business logic instance
            business_logic_instance = self.business_logic_instances_map[business_logic_instance_name]

            setattr(self, business_logic_instance_name, business_logic_instance)
