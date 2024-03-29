#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import sys

import colony


class BusinessHelper(colony.System):
    """
    The business helper class.
    """

    namespace_entity_classes_map = {}
    """ The map associating the namespace with the entity classes """

    namespace_business_logic_classes_map = {}
    """ The map associating the namespace with the business logic classes """

    def import_class_module(
        self,
        class_module_name,
        globals,
        locals,
        global_values,
        base_directory_path,
        target_module_name="helper_module",
        extra_symbols_map={},
        extra_globals_map={},
    ):
        """
        Imports the class module using the globals and locals from the current target,
        it imports the symbols in the module to the current globals environment.

        :type class_module_name: String
        :param class_module_name: The name of the module containing the classes to be imported.
        :type globals: Dictionary
        :param globals: The global variables map.
        :type locals: Dictionary
        :param locals: The local variables map.
        :type global_values: List
        :param global_values: A list containing the global values to be converted from locals.
        :type base_directory_path: String
        :param base_directory_path: The base directory path to be used.
        :type target_module_name: String
        :param target_module_name: The name of the module to import the classes.
        :type extra_symbols_map: Dictionary
        :param extra_symbols_map: A map containing a set of (extra) symbols to be set in
        the imported module under the base entity module.
        :type extra_globals_map: Dictionary
        :param extra_globals_map: A map containing a set of (extra) global symbols to be set in
        the imported module under as global variables.
        :rtype: module
        :return: The created target module.
        """

        # checks if the target module already exists, to later
        # avoid module reloading
        exists_target_module = self._exists_target_module(target_module_name, globals)

        # tries to retrieve the target module, from the existing context
        target_module = self._get_target_module(target_module_name, globals)

        # in case the target module already existed
        # no need to reload it, returns the reference immediately
        if exists_target_module:
            return target_module

        # sets the target module dictionary as the target map
        target_map = target_module.__dict__

        # retrieves the base entity module
        base_entity_module = self._get_target_module("base_entity", globals)

        # retrieves the entity class and sets it in the base
        # entity module (for latter reference)
        entity_class = self.get_entity_class()
        base_entity_module.__dict__[entity_class.__name__] = entity_class

        # iterates over all the extra symbols (in map)
        # to set then "under" the base entity
        for extra_symbol_name, extra_symbol_value in colony.legacy.items(
            extra_symbols_map
        ):
            # sets the extra symbol in the base entity module (for the class name)
            base_entity_module.__dict__[extra_symbol_name] = extra_symbol_value

        # iterates over all the extra globals (in map)
        # to set them as global symbols of the module
        for extra_global_name, extra_global_value in colony.legacy.items(
            extra_globals_map
        ):
            # sets the extra global value (symbol) in the globals
            # map for the module
            globals[extra_global_name] = extra_global_value

        # sets the base entity module in the globals
        globals["base_entity"] = base_entity_module

        # sets the globals and locals reference attributes
        target_map["_globals"] = globals
        target_map["_locals"] = locals

        # creates the the (complete) path to the module file
        # for file execution
        module_file_path = os.path.join(base_directory_path, class_module_name + ".py")

        # executes the file in the given environment
        # to import the symbols
        colony.legacy.execfile(module_file_path, target_map, target_map)

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
        bundle_module = colony.legacy.new_module(bundle_module_name)

        for bundle_key, bundle_value in colony.legacy.items(bundle_map):
            bundle_module.__dict__[bundle_key] = bundle_value

        # returns the bundle module
        return bundle_module

    def get_entity_class(self):
        # retrieves the entity manager plugin to use it to
        # retrieve the (base) entity class
        entity_manager_plugin = self.plugin.entity_manager_plugin
        entity_class = entity_manager_plugin.get_entity_class()

        # returns the retrieved (base) entity class,
        # every entity model must inherit from this class
        return entity_class

    def get_entity_classes_namespaces(self, namespaces):
        # creates the list to hold the entity classes
        # for the namespaces
        entity_classes_namespaces = []

        # iterates over all the namespaces
        for namespace in namespaces:
            # retrieves the list of entity classes for the namespace
            entity_classes_namespace = self.namespace_entity_classes_map.get(
                namespace, []
            )

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
            business_logic_classes_namespace = (
                self.namespace_business_logic_classes_map.get(namespace, [])
            )

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

        # in case no data namespaces are found, must return
        # immediately as there's nothing to be done
        if not data_namespaces:
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
        business_logic_namespaces = business_logic_plugin.get_attribute(
            "business_logic_namespaces"
        )

        # in case no business logic namespaces are found
        if not business_logic_namespaces:
            # returns immediately
            return

        # retrieves the business logic class from the business logic plugin
        business_logic_class = business_logic_plugin.get_business_logic_class()

        # iterates over all the business logic namespaces
        for business_logic_namespace in business_logic_namespaces:
            # loads the business logic class for the namespace
            self._load_business_logic_class_namespace(
                business_logic_namespace, business_logic_class
            )

    def business_logic_unload(self, business_logic_plugin):
        # tries to retrieve the data namespaces value
        business_logic_namespaces = business_logic_plugin.get_attribute(
            "business_logic_namespaces"
        )

        # in case no business logic namespaces are found
        if not business_logic_namespaces:
            # returns immediately
            return

        # retrieves the business logic class from the business logic plugin
        business_logic_class = business_logic_plugin.get_business_logic_class()

        # iterates over all the business logic namespaces
        for business_logic_namespace in business_logic_namespaces:
            # unloads the business logic class from the namespace
            self._unload_business_logic_class_namespace(
                business_logic_namespace, business_logic_class
            )

    def business_logic_bundle_load(self, business_logic_bundle_plugin):
        # tries to retrieve the business logic namespaces value
        business_logic_namespaces = business_logic_bundle_plugin.get_attribute(
            "business_logic_namespaces"
        )

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
                self._load_business_logic_class_namespace(
                    business_logic_namespace, business_logic_class
                )

    def business_logic_bundle_unload(self, business_logic_bundle_plugin):
        # tries to retrieve the business logic namespaces value
        business_logic_namespaces = business_logic_bundle_plugin.get_attribute(
            "business_logic_namespaces"
        )

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
                self._unload_business_logic_class_namespace(
                    business_logic_namespace, business_logic_class
                )

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
        business_logic_classes_list = self.namespace_business_logic_classes_map[
            namespace
        ]

        # adds the business logic class to the business logic classes list
        business_logic_classes_list.append(business_logic_class)

    def _unload_business_logic_class_namespace(self, namespace, business_logic_class):
        # in case the namespace does not exist in the namespace
        # business logic classes map
        if not namespace in self.namespace_business_logic_classes_map:
            # returns immediately
            return

        # retrieves the business logic classes list
        business_logic_classes_list = self.namespace_business_logic_classes_map[
            namespace
        ]

        # in case the business logic class does not
        # exist in the business logic classes list
        if not business_logic_class in business_logic_classes_list:
            # returns immediately
            return

        # removes the business logic class from the business logic classes list
        business_logic_classes_list.remove(business_logic_class)

    def _exists_target_module(self, target_module_name, globals):
        # checks if the target target module already exists
        # in the globals or in the  "system modules"
        exists_target_module = (
            target_module_name in globals or target_module_name in sys.modules
        )

        # returns the result of the existence test
        return exists_target_module

    def _get_target_module(self, target_module_name, globals):
        # tries to retrieve the target module from the
        # globals or from the "system modules"
        target_module = globals.get(target_module_name, None) or sys.modules.get(
            target_module_name, None
        )

        # in case the target module is not defined,
        # need to create a new one
        if not target_module:
            # creates the target module, using the underlying
            # python facilities for it
            target_module = colony.legacy.new_module(target_module_name)

            # adds the target module to the globals map
            # and sets it in the global modules reference map
            globals[target_module_name] = target_module
            sys.modules[target_module_name] = target_module

        # returns the target model
        return target_module
