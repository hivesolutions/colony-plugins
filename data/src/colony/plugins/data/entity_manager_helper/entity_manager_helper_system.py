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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 7750 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-29 14:32:40 +0100 (seg, 29 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types

ENGINE_VALUE = "engine"
""" The engine value """

CONNECTION_PARAMETERS_VALUE = "connection_parameters"
""" The connection parameters value """

ENTITY_CLASSES_LIST_VALUE = "entity_classes_list"
""" The entity classes list value """

ENTITY_CLASSES_MAP_VALUE = "entity_classes_map"
""" The entity classes map value """

FILE_PATH_VALUE = "file_path"
""" The file path value """

DEFAULT_ENGINE = "sqlite"
""" The default engine """

DEFAULT_CONNECTION_PARAMETERS = {
    "file_path" : "system.db",
    "autocommit" : False
}
""" The default connection parameters """

class EntityManagerHelper:
    """
    The entity manager helper class.
    """

    entity_manager_helper_plugin = None
    """ The entity manager helper plugin """

    def __init__(self, entity_manager_helper_plugin):
        """
        Constructor of the class

        @type entity_manager_helper_plugin: EntityManagerHelperPlugin
        @param entity_manager_helper_plugin: The entity manager helper plugin.
        """

        self.entity_manager_helper_plugin = entity_manager_helper_plugin

    def load_entity_manager(self, entities_module_name, entities_module_path, entity_manager_arguments):
        """
        Loads the entity manager object, used to access
        the database.
        The entity manager is loaded for the entities in the module
        located in the entities module path and in the module with the given
        entities module name.
        The given entity manager arguments are used in the connection establishment.

        @type entities_module_name: String
        @param entities_module_name: The name of the entities module.
        @type entities_module_path: String
        @param entities_module_path: The path to the entities module.
        @type entity_manager_arguments: Dictionary
        @param entity_manager_arguments: The arguments for the entity manager
        loading.
        @rtype: EntityManager
        @return: The loaded entity manager.
        """

        # retrieves the entity manager plugin
        entity_manager_plugin = self.entity_manager_helper_plugin.entity_manager_plugin

        # retrieves the business helper plugin
        business_helper_plugin = self.entity_manager_helper_plugin.business_helper_plugin

        # imports the entities module
        entities_module = business_helper_plugin.import_class_module_target(entities_module_name, globals(), locals(), [], entities_module_path, entities_module_name)

        # retrieves the entity class
        entity_class = business_helper_plugin.get_entity_class()

        # retrieves all the entity classes from the entities module
        base_entity_models = self._get_entity_classes(entities_module, entity_class)

        # generates the entity models map from the base entity models list
        # creating the map associating the class names with the classes
        base_entity_models_map = business_helper_plugin.generate_bundle_map(base_entity_models)

        # retrieves the engine from the entity manager arguments or uses
        # the default engine
        engine = entity_manager_arguments.get(ENGINE_VALUE, DEFAULT_ENGINE)

        # retrieves the connection parameters from the entity manager arguments or uses
        # the default connection parameters
        connection_parameters = entity_manager_arguments.get(CONNECTION_PARAMETERS_VALUE, DEFAULT_CONNECTION_PARAMETERS)

        # resolves the connection parameters
        self._resolve_connection_parameters(connection_parameters)

        # creates the entity manager properties
        entity_manager_properties = {ENTITY_CLASSES_LIST_VALUE : base_entity_models, ENTITY_CLASSES_MAP_VALUE : base_entity_models_map}

        # creates a new entity manager for the remote models with the given properties
        entity_manager = entity_manager_plugin.load_entity_manager_properties(engine, entity_manager_properties)

        # sets the connection parameters for the entity manager
        entity_manager.set_connection_parameters(connection_parameters)

        # loads the entity manager
        entity_manager.load_entity_manager()

        # returns the entity manager
        return entity_manager

    def _resolve_connection_parameters(self, connection_parameters):
        """
        Resolves the given connection parameters map, substituting
        the values with the resolved ones.

        @type connection_parameters: Dictionary
        @param connection_parameters: The connection parameters to be resolved.
        """

        # retrieves the plugin manager
        plugin_manager = self.entity_manager_helper_plugin.manager

        # resolves the file path
        connection_parameters[FILE_PATH_VALUE] = plugin_manager.resolve_file_path(connection_parameters[FILE_PATH_VALUE], True, True)

    def _get_entity_classes(self, module, entity_class):
        """
        Retrieves all the entity classes from the given module
        using the given entity class as the reference to get the entity classes.

        @type module: Module
        @param module: The module to be used to retrieve the entity classes.
        @type entity_class: Class
        @param entity_class: The entity class to be used as reference
        to retrieve the entity classes.
        @rtype: List
        @return: The list of entity classes in the module.
        """

        # creates the entity classes list
        entity_classes = []

        # retrieves the base entity models module map
        module_map = module.__dict__

        # iterates over all the module item names
        for module_item_name in module_map:
            # retrieves the module item from  module
            module_item = getattr(module, module_item_name)

            # retrieves the module item type
            module_item_type = type(module_item)

            # in case the module item type is type and
            # the module item is subclass of the entity class
            if module_item_type == types.TypeType and issubclass(module_item, entity_class):
                # adds the module item to the entity classes
                entity_classes.append(module_item)

        # returns the entity classes
        return entity_classes
