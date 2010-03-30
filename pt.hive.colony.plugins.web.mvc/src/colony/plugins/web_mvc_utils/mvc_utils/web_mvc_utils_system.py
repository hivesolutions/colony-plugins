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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types

import web_mvc_model
import web_mvc_controller
import web_mvc_entity_model

class WebMvcUtils:
    """
    The web mvc utils class.
    """

    web_mvc_utils_plugin = None
    """ The web mvc utils plugin """

    def __init__(self, web_mvc_utils_plugin):
        """
        Constructor of the class.

        @type web_mvc_utils_plugin: WebMvcUtilsPlugin
        @param web_mvc_utils_plugin: The web mvc utils plugin.
        """

        self.web_mvc_utils_plugin = web_mvc_utils_plugin

    def create_model(self, base_model, base_arguments_list, base_arguments_map):
        # sets the module functions in the base model class
        self._set_module_functions(web_mvc_model, base_model)

        # creates the model with the sent arguments list and the arguments map
        model = base_model(*base_arguments_list, **base_arguments_map)

        # starts the model structures
        model._start_model()

        # returns the model
        return model

    def create_controller(self, base_controller, base_arguments_list, base_arguments_map):
        # sets the module functions in the base controller class
        self._set_module_functions(web_mvc_controller, base_controller)

        # creates the controller with the sent arguments list and the arguments map
        controller = base_controller(*base_arguments_list, **base_arguments_map)

        # starts the controller structures
        controller._start_controller()

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.web_mvc_utils_plugin.template_engine_manager_plugin

        # sets the template engine manager plugin in the controller
        controller.set_template_engine_manager_plugin(template_engine_manager_plugin)

        # returns the controller
        return controller

    def create_entity_models(self, base_entity_models_module_name, entity_manager_arguments):
        # retrieves the entity manager plugin
        entity_manager_plugin = self.web_mvc_utils_plugin.entity_manager_plugin

        # retrieves the business helper plugin
        business_helper_plugin = self.web_mvc_utils_plugin.business_helper_plugin



        # retrieves the base directory name
        #base_directory_name = self.get_path_directory_name()

        # imports the base entity models module
        base_entity_models_module = business_helper_plugin.import_class_module_target(base_entity_models_module_name, globals(), locals(), [], "C:/Users/joamag/workspace/pt.hive.hive_blog.plugins.main/src/hive_blog/plugins/hive_blog_main/main", base_entity_models_module_name)





        # generates the entity bundle map from the entity bundle
        #self.entity_bundle_map = business_helper_plugin.generate_bundle_map(self.entity_bundle)



        # HARDCODED PLEASE CHANGE !!!!
        base_entity_models = [base_entity_models_module.Comment]




        # creates a new entity manager for the remote models
        entity_manager = entity_manager_plugin.load_entity_manager("sqlite")

        # sets the entity manager classes list
        entity_manager.entity_classes_list = base_entity_models

        # TENHO DE TB ACTUALIZAR A ENTITY CLASSES MAP !!!


        # sets the connection parameters for the entity manager
        entity_manager.set_connection_parameters({"file_path" : "c:/tobias.db", "autocommit" : False})

        # loads the entity manager
        entity_manager.load_entity_manager()



        # iterates over all the base entity models to update them
        # in order to allow them to become entity models
        for base_entity_model in base_entity_models:
            # sets the module functions in the base model class
            self._set_module_functions(web_mvc_model, base_entity_model)

            # sets the module functions in the base model class
            self._set_module_functions(web_mvc_entity_model, base_entity_model)

            base_entity_model.__oldinit__ = base_entity_model.__init__

            base_entity_model.__init__ = base_entity_model.__newinit__

            # sets the entity manager in the base entity model
            base_entity_model.entity_manager = entity_manager

        return base_entity_models_module

    def _set_module_functions(self, module, target_class):
        """
        Updates the target class, adding all the functions
        found in the given module as method to it.

        @type module: Module
        @param module: The module to be used to find the functions
        to be added to the target class.
        @type target_class: Class
        @param target_class: The class to be used as target of the adding
        of the methods.
        """

        # iterates over all the items in the module
        for item in dir(module):
            # retrieves the item value
            item_value = getattr(module, item)

            # retrieves the item value type
            item_value_type = type(item_value)

            # in case the item value type is function
            if item_value_type == types.FunctionType:
                # sets the item in the
                setattr(target_class, item, item_value)
