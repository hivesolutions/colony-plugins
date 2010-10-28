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

import time
import types

import business_session_manager_exceptions

POOL_SIZE = 15
""" The pool size """

MAX_POOL_SIZE = 30
""" The maximum pool size """

SCHEDULING_ALGORITHM = 1
""" The scheduling algorithm """

CREATE_PERSISTENT_SESSION_TYPE_VALUE = "create_persistent_session"
""" The create persistent session type value """

GET_SESSION_METHODS_TYPE_VALUE = "get_session_methods"
""" The get session methods type value """

UPDATE_SESSION_INFORMATION_TYPE_VALUE = "update_session_information"
""" The update session information type value """

FLUSH_SESSION_INFORMATION_TYPE_VALUE = "flush_session_information"
""" The flush session information type value """

CALL_SESSION_METHOD_TYPE_VALUE = "call_session_method"
""" The call session method type value """

SESSION_ID_VALUE = "session_id"
""" The session id value """

SESSION_CREATION_TIME_VALUE = "session_creation_time"
""" The session creation time value """

SESSION_TIMEOUT_TIME_VALUE = "session_timeout_time"
""" The session timeout time value """

SESSION_INFORMATION_MAP_VALUE = "session_information_map"
""" The session information map value """

PARAMS_VALUE = "params"
""" The params value """

DEFAULT_PERSISTENT_SESSION_TIMEOUT = 86400
""" The default persistent session timeout """

class BusinessSessionManager:
    """
    The business session manager class.
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
        Constructor of the class.

        @type business_session_manager_plugin: BusinessSessionManagerPlugin
        @param business_session_manager_plugin: The business session manager plugin.
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
        for business_logic_class in business_logic_bundle:
            self.unload_business_logic_class(business_logic_class)

    def load_session_manager(self, session_name, entity_manager = None):
        # retrieves the plugin manager
        plugin_manager = self.business_session_manager_plugin.manager

        # retrieves the random plugin
        random_plugin = self.business_session_manager_plugin.random_plugin

        # creates the session manager
        session_manager = SessionManager(session_name, self.loaded_business_logic_classes_list, self.loaded_business_logic_classes_map, plugin_manager, entity_manager, random_plugin)

        # adds the created session manager to the list of active session managers
        self.active_session_manager_list.append(session_manager)

        # returns the created session manager
        return session_manager

    def load_session_manager_master(self, session_name, entity_manager = None):
        # retrieves the plugin manager
        plugin_manager = self.business_session_manager_plugin.manager

        # retrieves the random plugin
        random_plugin = self.business_session_manager_plugin.random_plugin

        # retrieves the business session serializer plugins
        business_session_serializer_plugins = self.business_session_manager_plugin.business_session_serializer_plugins

        # retrieves the simple pool manager plugin
        simple_pool_manager_plugin = self.business_session_manager_plugin.simple_pool_manager_plugin

        # creates the session manager master
        session_manager_master = SessionManagerMaster(session_name, self.loaded_business_logic_classes_list, self.loaded_business_logic_classes_map, plugin_manager, entity_manager, random_plugin, business_session_serializer_plugins, simple_pool_manager_plugin)

        # adds the created session manager master to the list of active session managers
        self.active_session_manager_list.append(session_manager_master)

        # returns the created session manager master
        return session_manager_master

    def load_session_manager_entity_manager(self, session_name, engine_name):
        # retrieves the entity manager plugin
        entity_manager_plugin = self.business_session_manager_plugin.entity_manager_plugin

        # creates the entity manager
        entity_manager = entity_manager_plugin.load_entity_manager(engine_name)

        # creates the session manager and returns it
        return self.load_session_manager(session_name, entity_manager)

    def load_session_manager_master_entity_manager(self, session_name, engine_name):
        # retrieves the entity manager plugin
        entity_manager_plugin = self.business_session_manager_plugin.entity_manager_plugin

        # creates the entity manager
        entity_manager = entity_manager_plugin.load_entity_manager(engine_name)

        # creates the session manager master and returns it
        return self.load_session_manager_master(session_name, entity_manager)

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

    plugin_manager = None
    """ The current plugin manager """

    entity_manager = None
    """ The entity manager associated with the current session"""

    random_plugin = None
    """ The random plugin """

    session_information_registry = None
    """ The session information registry """

    business_logic_instances_list = []
    """ The list of business logic instances """

    business_logic_instances_map = {}
    """ The map associating the business logic instances with their names """

    business_logic_class_methods_map = {}
    """ The map associating the business logic classes with their methods """

    current_session_information = None
    """ The current session information """

    def __init__(self, session_name, business_logic_classes_list, business_logic_classes_map, plugin_manager = None, entity_manager = None, random_plugin = None):
        self.session_name = session_name
        self.business_logic_classes_list = business_logic_classes_list
        self.business_logic_classes_map = business_logic_classes_map
        self.plugin_manager = plugin_manager
        self.entity_manager = entity_manager
        self.random_plugin = random_plugin

        self.session_information_registry = SessionInformationRegistry()
        self.business_logic_instances_list = []
        self.business_logic_instances_map = {}
        self.business_logic_class_methods_map = {}

    def start_session(self):
        """
        Starts the session in the session manager.
        """

        self.instantiate_business_logic()
        self.inject_entity_manager()
        self.inject_plugin_manager()
        self.inject_business_logic()

    def stop_session(self):
        """
        Stops the session in the session manager.
        """

        pass

    def instantiate_business_logic(self):
        """
        Instantiates the business logic for the current
        session name.
        """

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

            # retrieves the business logic class methods from the business logic class
            business_logic_class_methods = [value for value in dir(business_logic_class) if type(getattr(business_logic_class, value)) == types.MethodType]

            # starts the list for the current business logic class
            self.business_logic_class_methods_map[business_logic_class_name] = []

            # iterates over all the business logic class methods
            for business_logic_class_method in business_logic_class_methods:
                business_logic_class_methods_list = self.business_logic_class_methods_map[business_logic_class_name]
                business_logic_class_methods_list.append(business_logic_class_method)

    def inject_entity_manager(self):
        """
        Injects the entity manager in all the business
        logic instances.
        """

        # iterates over all the business logic instances
        for business_logic_instance in self.business_logic_instances_list:
            # sets the entity manager in the business logic instance
            business_logic_instance.entity_manager = self.entity_manager

    def inject_plugin_manager(self):
        """
        Injects the plugin manager in all the business
        logic classes.
        """

        # iterates over all the business logic classes
        for business_logic_class in self.business_logic_classes_list:
            # sets the plugin manager in the business logic class
            business_logic_class.plugin_manager = self.plugin_manager

    def inject_business_logic(self):
        """
        Injects the business logic in the current instance.
        """

        # iterates over the business logic instance map
        for business_logic_instance_name in self.business_logic_instances_map:
            # retrieves the business logic instance
            business_logic_instance = self.business_logic_instances_map[business_logic_instance_name]

            # sets the session manager in the business logic instance
            business_logic_instance.session_manager = self

            # sets the business logic as an attribute of the current instance
            setattr(self, business_logic_instance_name, business_logic_instance)

    def create_persistent_session(self):
        """
        Creates a new persistent session,
        returning the new session id.

        @rtype: SessionInformation
        @return: The created session information.
        """

        # creates a new random session id
        session_id = self.random_plugin.generate_random_md5_string()

        # retrieves the current time
        current_time = time.time()

        # creates the session creation time
        session_creation_time = current_time

        # creates the session timeout time
        session_timeout_time = current_time + DEFAULT_PERSISTENT_SESSION_TIMEOUT

        # creates a new session information
        session_information = SessionInformation(session_id, session_creation_time, session_timeout_time)

        # sets the session information in the session information registry
        self.session_information_registry.set_session_information(session_id, session_information)

        # returns the session information
        return session_information

    def get_current_session_information(self):
        """
        Retrieves the current session information.

        @rtype: SessionInformation
        @return: The current session information.
        """

        return self.current_session_information

    def set_current_session_information(self, current_session_information):
        """
        Sets the current session information.

        @type current_session_information: SessionInformation
        @param current_session_information: The current session information.
        """

        self.current_session_information = current_session_information

    def get_business_logic_instance(self, business_logic_instance_name):
        """
        Retrieves the business logic instance for the given business
        logic instance name.

        @type business_logic_instance_name: String
        @param business_logic_instance_name: The business logic instance name.
        @rtype: Object
        @return: The business logic instance for the given business logic instance name.
        """

        # retrieves the business logic instance
        business_logic_instance = self.business_logic_instances_map[business_logic_instance_name]

        # returns the business logic instance
        return business_logic_instance

class SessionManagerMaster(SessionManager):
    """
    The session manager master class.
    """

    business_session_serializer_plugins = []
    """ The business session serializer plugins """

    simple_pool_manager_plugin = None
    """ The simple pool manager plugin """

    session_proxy = None
    """ The session proxy """

    engine_name = "none"
    """ The name of the used engine """

    entity_manager_pool_size = None
    """ The entity manager pool size """

    entity_manager_scheduling_algorithm = None
    """ The entity manager scheduling algorithm """

    entity_manager_maximum_pool_size = None
    """ The entity manager maximum pool size """

    entity_manager_pool = []
    """ The entity manager pool """

    session_manager_pool_size = None
    """ The session manager pool size """

    session_manager_scheduling_algorithm = None
    """ The session manager scheduling algorithm """

    session_manager_maximum_pool_size = None
    """ The session manager maximum pool size """

    session_manager_pool = []
    """ The session manager pool """

    session_information_registry = None
    """ The session information registry """

    def __init__(self, session_name, business_logic_classes_list, business_logic_classes_map, plugin_manager = None, entity_manager = None, random_plugin = None, business_session_serializer_plugins = [], simple_pool_manager_plugin = None):
        SessionManager.__init__(self, session_name, business_logic_classes_list, business_logic_classes_map, plugin_manager, entity_manager, random_plugin)

        self.business_session_serializer_plugins = business_session_serializer_plugins
        self.simple_pool_manager_plugin = simple_pool_manager_plugin

        self.entity_manager_pool = []
        self.session_manager_pool = []

    def create_session_proxy(self):
        """
        Creates a session proxy for the session master.
        """

        # creates a new session proxy
        self.session_proxy = SessionManagerProxy(self)

    def register_session_proxy(self, replace_proxy = False):
        """
        Registers the session proxy in the session serializer.
        """

        # iterates over all the business session serializer plugins
        for business_session_serializer_plugin in self.business_session_serializer_plugins:
            # adds the session proxy to the business session serializer plugin
            business_session_serializer_plugin.add_session_proxy(self.session_proxy, replace_proxy)

    def unregister_session_proxy(self):
        """
        Unregisters the session proxy in the session serializer.
        """

        for business_session_serializer_plugin in self.business_session_serializer_plugins:
            business_session_serializer_plugin.remove_session_proxy(self.session_proxy)

    def start_entity_manager_pool(self, engine_name, pool_size = POOL_SIZE, scheduling_algorithm = SCHEDULING_ALGORITHM, maximum_pool_size = MAX_POOL_SIZE):
        pass

    def construct_session_manager_pool(self, pool_size = POOL_SIZE, scheduling_algorithm = SCHEDULING_ALGORITHM, maximum_pool_size = MAX_POOL_SIZE):
        """
        Constructs the session manager pool, with the given pool size, scheduling algorithm
        and maximum pool size.

        @type pool_size: int
        @param pool_size: The size of the pool to be constructed.
        @type scheduling_algorithm: int
        @param scheduling_algorithm: The scheduling algorithm to be used.
        @type maximum_pool_size: int
        @param maximum_pool_size: The maximum size of the pool to be constructed.
        """

        # creates the session manager pool name
        session_manager_pool_name = self.session_name + "/session_manager"

        # creates the session manager pool description
        session_manager_pool_description = session_manager_pool_name + "/description"

        # creates the session manager pool
        self.session_manager_pool = self.simple_pool_manager_plugin.create_new_simple_pool(session_manager_pool_name, session_manager_pool_description, pool_size, scheduling_algorithm, maximum_pool_size)

        # sets the item constructor for the session manager pool
        self.session_manager_pool.set_item_constructor_method(self.item_constructor_method)

        # sets the item destructor for the session manager pool
        self.session_manager_pool.set_item_destructor_method(self.item_destructor_method)

        # constructs the pool
        self.session_manager_pool.construct_pool()

    def item_constructor_method(self):
        """
        The method used to construct session manager
        instances for the pool.

        @rtype: SessionManager
        @return: The constructed session manager instance.
        """

        # creates a new session manager
        session_manager = SessionManager(self.session_name, self.business_logic_classes_list, self.business_logic_classes_map, self.plugin_manager, self.entity_manager, self.random_plugin)

        # start the session in the session manager
        session_manager.start_session()

        # returns the session manager
        return session_manager

    def item_destructor_method(self, session_manager):
        """
        The method used to destroy a session manager
        instance from the pool.

        @rtype: SessionManager
        @return: The constructed session manager instance.
        """

        pass

    def handle_create_persistent_session_request(self, session_information, session_request):
        """
        The handler for the create persistent session request.

        @type session_information: SessionInformation
        @param session_information: The session information object.
        @type session_request: SessionRequest
        @param session_request: The session request object.
        @rtype: Dictionary
        @return: The return value.
        """

        # creates the persistent session and retrieves
        # the session information
        session_information = self.create_persistent_session()

        # creates the return value
        return_value = self._create_return_value({"session_information" : session_information}, session_information)

        # returns the return value
        return return_value

    def handle_get_session_methods_request(self, session_information, session_request):
        """
        The handler for the get session methods request.

        @type session_information: SessionInformation
        @param session_information: The session information object.
        @type session_request: SessionRequest
        @param session_request: The session request object.
        @rtype: Dictionary
        @return: The return value.
        """

        try:
            # tries to retrieve the session information
            session_information = self._get_session_information(session_information)
        except business_session_manager_exceptions.InvalidSessionId:
            # creates a new persistent session
            session_information = self.create_persistent_session()

        # creates the return value
        return_value = self._create_return_value({"session_methods" : self.business_logic_class_methods_map}, session_information)

        # returns the return value
        return return_value

    def handle_update_session_information_request(self, session_information, session_request):
        """
        The handler for the update session information request.

        @type session_information: SessionInformation
        @param session_information: The session information object.
        @type session_request: SessionRequest
        @param session_request: The session request object.
        @rtype: Dictionary
        @return: The return value.
        """

        # retrieves the session information
        session_information = self._get_session_information(session_information)

        # creates the return value
        return_value = self._create_return_value({"session_information" : session_information}, session_information)

        # returns the return value
        return return_value

    def handle_flush_session_information_request(self, session_information, session_request):
        """
        The handler for the flush session information request.

        @type session_information: SessionInformation
        @param session_information: The session information object.
        @type session_request: SessionRequest
        @param session_request: The session request object.
        @rtype: Dictionary
        @return: The return value.
        """

        # retrieves the session information map
        session_information_map = session_information.session_information_map

        # retrieves the session information
        session_information = self._get_session_information(session_information)

        # sets the session information map in the session information
        session_information.set_session_information_map(session_information_map)

        # creates the return value
        return_value = self._create_return_value({"session_information" : session_information}, session_information)

        # returns the return value
        return return_value

    def handle_call_method_request(self, session_information, session_request):
        """
        The handler for the call method request.

        @type session_information: SessionInformation
        @param session_information: The session information object.
        @type session_request: SessionRequest
        @param session_request: The session request object.
        @rtype: Dictionary
        @return: The return value.
        """

        # retrieves a session manager from the pool
        session_manager = self.session_manager_pool.get_pool_item()

        # retrieves the session information
        session_information = self._get_session_information(session_information)

        # sets the session information in the session manager as the current
        session_manager.set_current_session_information(session_information)

        # retrieves the entity attribute from the instance
        entity_attribute = getattr(session_manager, session_request.session_entity)

        # retrieves the entity method attribute from the entity attribute
        entity_method_attribute = getattr(entity_attribute, session_request.session_method)

        # retrieves the session method arguments list
        session_method_arguments = session_request.session_method_arguments

        # retrieves the session method arguments map
        session_method_arguments_map = session_request.session_method_arguments_map

        # calls the entity method with the method arguments list
        return_value = entity_method_attribute(*session_method_arguments, **session_method_arguments_map)

        # releases the session manager to the pool
        self.session_manager_pool.release_pool_item(session_manager)

        # creates the return value
        return_value = self._create_return_value({"return_value" : return_value}, session_information)

        # returns the return value
        return return_value

    def _create_return_value(self, return_value, session_information):
        """
        Creates the return value from an original return value
        and a session information.

        @type return_value: Dictionary
        @param return_value: The original return value.
        @type session_information: SessionInformation
        @param session_information: The session information to be used in the creation of the return value.
        @rtype: Dictionary
        @return: The created return value.
        """

        # creates the first parameter map
        first_parameter_map = {}

        # sets the session id value in the first parameter map
        first_parameter_map[SESSION_ID_VALUE] = session_information.get_session_id()

        # sets the session creation time value in the first parameter map
        first_parameter_map[SESSION_CREATION_TIME_VALUE] = session_information.get_session_creation_time()

        # sets the session timeout time value in the first parameter map
        first_parameter_map[SESSION_TIMEOUT_TIME_VALUE] = session_information.get_session_timeout_time()

        # sets the session information map value in the first parameter map
        first_parameter_map[SESSION_INFORMATION_MAP_VALUE] = session_information.get_session_information_map()

        # creates the parameters list
        return_value[PARAMS_VALUE] = []

        # appends the first parameter to the parameters
        return_value[PARAMS_VALUE].append(first_parameter_map)

        # returns the return value
        return return_value

    def _get_session_information(self, session_information):
        """
        Retrieves the session information from the given session
        information structure.

        @type session_information: Dictionary
        @param session_information: The session information structure to retrieve the session information.
        @rtype: SessionInformation
        @return: The retrieved session information.
        """

        # retrieves the session id
        session_id = session_information.session_id

        # retrieves the session information
        session_information = self.session_information_registry.get_session_information(session_id)

        # returns the session information
        return session_information

class SessionManagerProxy:
    """
    The session proxy class.
    """

    session_manager = None
    """ The session manager """

    def __init__(self, session_manager):
        """
        Constructor of the class.

        @type session_manager: SessionManager
        @param session_manager: The session manager.
        """

        self.session_manager = session_manager

    def get_session_name(self):
        # retrieves the session name
        session_name = self.session_manager.session_name

        # returns the session name
        return session_name

    def handle_request(self, session_information, session_request):
        if session_request.session_request_type == CREATE_PERSISTENT_SESSION_TYPE_VALUE:
            return self.session_manager.handle_create_persistent_session_request(session_information, session_request)
        elif session_request.session_request_type == GET_SESSION_METHODS_TYPE_VALUE:
            return self.session_manager.handle_get_session_methods_request(session_information, session_request)
        elif session_request.session_request_type == UPDATE_SESSION_INFORMATION_TYPE_VALUE:
            return self.session_manager.handle_update_session_information_request(session_information, session_request)
        elif session_request.session_request_type == FLUSH_SESSION_INFORMATION_TYPE_VALUE:
            return self.session_manager.handle_flush_session_information_request(session_information, session_request)
        elif session_request.session_request_type == CALL_SESSION_METHOD_TYPE_VALUE:
            return self.session_manager.handle_call_method_request(session_information, session_request)

class SessionInformationRegistry:
    """
    The session information registry class.
    """

    session_id_session_information_map = {}
    """ The map relating the session id with the session information """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.session_information_map = {}

    def get_session_information(self, session_id):
        if not session_id in self.session_id_session_information_map:
            raise business_session_manager_exceptions.InvalidSessionId("session id %s is invalid" % session_id)

        return self.session_id_session_information_map[session_id]

    def set_session_information(self, session_id, session_information):
        self.session_id_session_information_map[session_id] = session_information

class SessionInformation:
    """
    The session information class.
    """

    session_id = None
    """ The session id """

    session_creation_time = None
    """ The session creation time """

    session_timeout_time = None
    """ The session timeout time """

    session_information_map = {}
    """ The session information map """

    def __init__(self, session_id, session_creation_time, session_timeout_time):
        """
        Constructor of the class.

        @type session_id: String
        @param session_id: The session id.
        @type session_creation_time: float
        @param session_creation_time: The session creation time.
        @type session_timeout_time: float
        @param session_timeout_time: The session timeout time.
        """

        self.session_id = session_id
        self.session_creation_time = session_creation_time
        self.session_timeout_time = session_timeout_time

        self.session_information_map = {}

    def get_session_property(self, property_name):
        """
        Retrieves a session property for the given property name.

        @type property_name: String
        @param property_name: The property name to retrieve the property.
        @rtype: Object
        @return: The session property for the given property name.
        """

        return self.session_information_map.get(property_name, None)

    def set_session_property(self, property_name, property_value):
        """
        Sets the session property for the given property name.

        @type property_name: String
        @param property_name: The property name for the property.
        @type property_value: Object
        @param property_value: The property value to set.
        """

        self.session_information_map[property_name] = property_value

    def get_session_id(self):
        """
        Retrieves the session id.

        @rtype: String
        @return: The session id.
        """

        return self.session_id

    def set_session_id(self, session_id):
        """
        Sets the session id.

        @type session_id: String
        @param session_id: The session id.
        """

        self.session_id = session_id

    def get_session_creation_time(self):
        """
        Retrieves the session creation time.

        @rtype: String
        @return: The session creation time.
        """

        return self.session_creation_time

    def set_session_creation_time(self, session_creation_time):
        """
        Sets the session creation time.

        @type session_creation_time: String
        @param session_creation_time: The session creation time.
        """

        self.session_creation_time = session_creation_time

    def get_session_timeout_time(self):
        """
        Retrieves the session creation time.

        @rtype: String
        @return: The session timeout time.
        """

        return self.session_timeout_time

    def set_session_timeout_time(self, session_timeout_time):
        """
        Sets the session timeout time.

        @type session_timeout_time: String
        @param session_timeout_time: The session timeout time.
        """

        self.session_timeout_time = session_timeout_time

    def get_session_information_map(self):
        """
        Retrieves the session information map.

        @rtype: Dictionary
        @return: The session information map.
        """

        return self.session_information_map

    def set_session_information_map(self, session_information_map):
        """
        Sets the session information map.

        @type session_information_map: Dictionary
        @param session_information_map: The session information map.
        """

        self.session_information_map = session_information_map
