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
        model._start()

        # returns the model
        return model

    def create_controller(self, base_controller, base_arguments_list, base_arguments_map):
        # sets the module functions in the base controller class
        self._set_module_functions(web_mvc_controller, base_controller)

        # creates the controller with the sent arguments list and the arguments map
        controller = base_controller(*base_arguments_list, **base_arguments_map)

        # starts the controller structures
        controller._start()

        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.web_mvc_utils_plugin.template_engine_manager_plugin

        # sets the template engine manager plugin in the controller
        controller.set_template_engine_manager_plugin(template_engine_manager_plugin)

        # returns the controller
        return controller

    def _set_module_functions(self, module, target_class):
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
