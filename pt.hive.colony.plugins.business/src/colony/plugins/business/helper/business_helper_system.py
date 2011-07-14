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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import imp

BASE_ENTITY_MODULE_VALUE = "base_entity"
""" The base entity module value """

GLOBALS_REFERENCE_VALUE = "_globals"
""" The globals reference value """

LOCALS_REFERENCE_VALUE = "_locals"
""" The locals reference value """

DEFAULT_MODULE_NAME = "helper_module"
""" The default module name """

class BusinessHelper:
    """
    The business helper class.
    """

    business_helper_plugin = None
    """ The business helper plugin """

    namespace_entity_classes_map = {}
    """ The map associating the namespace with the entity classes """

    namespace_business_logic_classes_map = {}
    """ The map associating the namespace with the business logic classes """

    def __init__(self, business_helper_plugin):
        """
        Constructor of the class.

        @type business_helper_plugin: BusinessHelperPlugin
        @param business_helper_plugin: The business helper plugin.
        """

        self.business_helper_plugin = business_helper_plugin

    def import_class_module(self, class_module_name, globals, locals, global_values, base_directory_path, target_module_name=DEFAULT_MODULE_NAME):
        """
        Imports the class module using the globals and locals from the current target,
        it imports the symbols in the module to the current globals environment.

        @type class_module_name: String
        @param class_module_name: The name of the module containing the classes to be imported.
        @type globals: Dictionary
        @param globals: The global variables map.
        @type locals: Dictionary
        @param locals: The local variables map.
        @type global_values: List
        @param global_values: A list containing the global values to be converted from locals.
        @type base_directory_path: String
        @param base_directory_path: The base directory path to be used.
        @type target_module_name: String
        @param target_module_name: The name of the module to import the classes.
        @rtype: Module
        @return: The created target module.
        """

        # tries to retrieve the target module
        target_module = self._get_target_module(target_module_name, globals)

        # sets the target module dictionary as the target map
        target_map = target_module.__dict__

        # retrieves the base entity module
        base_entity_module = self._get_target_module(BASE_ENTITY_MODULE_VALUE, globals)

        # sets the entity class in the base entity module
        base_entity_module.__dict__[EntityClass.__name__] = EntityClass

        # sets the base entity module in the globals
        globals[BASE_ENTITY_MODULE_VALUE] = base_entity_module

        # sets the globals reference attribute
        target_map[GLOBALS_REFERENCE_VALUE] = globals

        # sets the locals reference attribute
        target_map[LOCALS_REFERENCE_VALUE] = locals

        # executes the file in the given environment
        # to import the symbols
        execfile(base_directory_path + "/" + class_module_name + ".py", target_map, target_map)

        # returns the target module
        return target_module

    def generate_bundle_map(self, bundle_classes):
        # creates the bundle map
        bundle_map = {}

        # iterates over all the bundle classes
        for bundle_class in bundle_classes:
            # retrieves the bundle class name
            bundle_class_name = bundle_class.__name__

            # sets the class in the bundle bundle map
            bundle_map[bundle_class_name] = bundle_class

        # returns the bundle map
        return bundle_map

    def generate_module_bundle(self, bundle_module_name, bundle_map):
        # creates the bundle module
        bundle_module = imp.new_module(bundle_module_name)

        for bundle_key, bundle_value in bundle_map.items():
            bundle_module.__dict__[bundle_key] = bundle_value

        # returns the bundle module
        return bundle_module

    def get_entity_class(self):
        return EntityClass

    def get_entity_classes_namespaces(self, namespaces):
        # creates the list to hold the entity classes
        # for the namespaces
        entity_classes_namespaces = []

        # iterates over all the namespaces
        for namespace in namespaces:
            # retrieves the list of entity classes for the namespace
            entity_classes_namespace = self.namespace_entity_classes_map.get(namespace, [])

            # extends the list of entity classes for the namespaces
            # with the entity classes for the namespace
            entity_classes_namespaces.extend(entity_classes_namespace)

        # returns the list of entity classes for the namespaces
        return entity_classes_namespaces

    def get_business_logic_classes_namespaces(self, namespaces):
        # creates the list to hold the business logic classes
        # for the namespaces
        business_logic_classes_namespaces = []

        # iterates over all the namespaces
        for namespace in namespaces:
            # retrieves the list of business logic classes for the namespace
            business_logic_classes_namespace = self.namespace_business_logic_classes_map.get(namespace, [])

            # extends the list of business logic classes for the namespaces
            # with the business logic classes for the namespace
            business_logic_classes_namespaces.extend(business_logic_classes_namespace)

        # returns the list of business logic classes for the namespaces
        return business_logic_classes_namespaces

    def entity_load(self, entity_plugin):
        # tries to retrieve the data namespaces value
        data_namespaces = entity_plugin.get_attribute("data_namespaces")

        # in case no data namespaces are found
        if not data_namespaces:
            # returns immediately
            return

        # retrieves the entity class from the entity plugin
        entity_class = entity_plugin.get_entity_class()

        # iterates over all the data namespaces
        for data_namespace in data_namespaces:
            # loads the entity class for the namespace
            self._load_entity_class_namespace(data_namespace, entity_class)

    def entity_unload(self, entity_plugin):
        # tries to retrieve the data namespaces value
        data_namespaces = entity_plugin.get_attribute("data_namespaces")

        # in case no data namespaces are found
        if not data_namespaces:
            # returns immediately
            return

        # retrieves the entity class from the entity plugin
        entity_class = entity_plugin.get_entity_class()

        # iterates over all the data namespaces
        for data_namespace in data_namespaces:
            # unloads the entity class from the namespace
            self._unload_entity_class_namespace(data_namespace, entity_class)

    def entity_bundle_load(self, entity_bundle_plugin):
        # tries to retrieve the data namespaces value
        data_namespaces = entity_bundle_plugin.get_attribute("data_namespaces")

        # in case no data namespaces are found
        if not data_namespaces:
            # returns immediately
            return

        # retrieves the entity bundle from the entity bundle plugin
        entity_bundle = entity_bundle_plugin.get_entity_bundle()

        # iterates over all the data namespaces
        for data_namespace in data_namespaces:
            # iterates over all the entity classes in the
            # entity bundle
            for entity_class in entity_bundle:
                # loads the entity class for the namespace
                self._load_entity_class_namespace(data_namespace, entity_class)

    def entity_bundle_unload(self, entity_bundle_plugin):
        # tries to retrieve the data namespaces value
        data_namespaces = entity_bundle_plugin.get_attribute("data_namespaces")

        # in case no data namespaces are found
        if not data_namespaces:
            # returns immediately
            return

        # retrieves the entity bundle from the entity bundle plugin
        entity_bundle = entity_bundle_plugin.get_entity_bundle()

        # iterates over all the data namespaces
        for data_namespace in data_namespaces:
            # iterates over all the entity classes in the
            # entity bundle
            for entity_class in entity_bundle:
                # unloads the entity class from the namespace
                self._unload_entity_class_namespace(data_namespace, entity_class)

    def business_logic_load(self, business_logic_plugin):
        # tries to retrieve the data namespaces value
        business_logic_namespaces = business_logic_plugin.get_attribute("business_logic_namespaces")

        # in case no business logic namespaces are found
        if not business_logic_namespaces:
            # returns immediately
            return

        # retrieves the business logic class from the business logic plugin
        business_logic_class = business_logic_plugin.get_business_logic_class()

        # iterates over all the business logic namespaces
        for business_logic_namespace in business_logic_namespaces:
            # loads the business logic class for the namespace
            self._load_business_logic_class_namespace(business_logic_namespace, business_logic_class)

    def business_logic_unload(self, business_logic_plugin):
        # tries to retrieve the data namespaces value
        business_logic_namespaces = business_logic_plugin.get_attribute("business_logic_namespaces")

        # in case no business logic namespaces are found
        if not business_logic_namespaces:
            # returns immediately
            return

        # retrieves the business logic class from the business logic plugin
        business_logic_class = business_logic_plugin.get_business_logic_class()

        # iterates over all the business logic namespaces
        for business_logic_namespace in business_logic_namespaces:
            # unloads the business logic class from the namespace
            self._unload_business_logic_class_namespace(business_logic_namespace, business_logic_class)

    def business_logic_bundle_load(self, business_logic_bundle_plugin):
        # tries to retrieve the business logic namespaces value
        business_logic_namespaces = business_logic_bundle_plugin.get_attribute("business_logic_namespaces")

        # in case no business logic namespaces are found
        if not business_logic_namespaces:
            # returns immediately
            return

        # retrieves the business logic bundle from the business logic bundle plugin
        business_logic_bundle = business_logic_bundle_plugin.get_business_logic_bundle()

        # iterates over all the business logic namespaces
        for business_logic_namespace in business_logic_namespaces:
            # iterates over all the business logic classes in the
            # business logic bundle
            for business_logic_class in business_logic_bundle:
                # loads the business logic class for the namespace
                self._load_business_logic_class_namespace(business_logic_namespace, business_logic_class)

    def business_logic_bundle_unload(self, business_logic_bundle_plugin):
        # tries to retrieve the business logic namespaces value
        business_logic_namespaces = business_logic_bundle_plugin.get_attribute("business_logic_namespaces")

        # in case no business logic namespaces are found
        if not business_logic_namespaces:
            # returns immediately
            return

        # retrieves the business logic bundle from the business logic bundle plugin
        business_logic_bundle = business_logic_bundle_plugin.get_business_logic_bundle()

        # iterates over all the business logic namespaces
        for business_logic_namespace in business_logic_namespaces:
            # iterates over all the business logic classes in the
            # business logic bundle
            for business_logic_class in business_logic_bundle:
                # unloads the business logic class from the namespace
                self._unload_business_logic_class_namespace(business_logic_namespace, business_logic_class)

    def _load_entity_class_namespace(self, namespace, entity_class):
        # in case the namespace does not exist in the namespace
        # entity classes map
        if not namespace in self.namespace_entity_classes_map:
            # creates a new list for the namespace entity classes map
            self.namespace_entity_classes_map[namespace] = []

        # retrieves the entity classes list
        entity_classes_list = self.namespace_entity_classes_map[namespace]

        # adds the entity class to the entity classes list
        entity_classes_list.append(entity_class)

    def _unload_entity_class_namespace(self, namespace, entity_class):
        # in case the namespace does not exist in the namespace
        # entity classes map
        if not namespace in self.namespace_entity_classes_map:
            # returns immediately
            return

        # retrieves the entity classes list
        entity_classes_list = self.namespace_entity_classes_map[namespace]

        # in case the entity class does not
        # exist in the entity classes list
        if not entity_class in entity_classes_list:
            # returns immediately
            return

        # removes the entity class from the entity classes list
        entity_classes_list.remove(entity_class)

    def _load_business_logic_class_namespace(self, namespace, business_logic_class):
        # in case the namespace does not exist in the namespace
        # business logic classes map
        if not namespace in self.namespace_business_logic_classes_map:
            # creates a new list for the namespace business logic classes map
            self.namespace_business_logic_classes_map[namespace] = []

        # retrieves the business logic classes list
        business_logic_classes_list = self.namespace_business_logic_classes_map[namespace]

        # adds the business logic class to the business logic classes list
        business_logic_classes_list.append(business_logic_class)

    def _unload_business_logic_class_namespace(self, namespace, business_logic_class):
        # in case the namespace does not exist in the namespace
        # business logic classes map
        if not namespace in self.namespace_business_logic_classes_map:
            # returns immediately
            return

        # retrieves the business logic classes list
        business_logic_classes_list = self.namespace_business_logic_classes_map[namespace]

        # in case the business logic class does not
        # exist in the business logic classes list
        if not business_logic_class in business_logic_classes_list:
            # returns immediately
            return

        # removes the business logic class from the business logic classes list
        business_logic_classes_list.remove(business_logic_class)

    def _get_target_module(self, target_module_name, globals):
        # tries to retrieve the target module
        target_module = globals.get(target_module_name, None)

        # in case the target module is not defined
        if not target_module:
            # creates the target module
            target_module = imp.new_module(target_module_name)

            # adds the target module to the globals map
            globals[target_module_name] = target_module

        # returns the target model
        return target_module

class EntityClass(object):
    """
    The base entity class used
    for the entity manager.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass
