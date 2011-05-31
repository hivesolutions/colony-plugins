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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.string_util

ATTRIBUTES_VALUE = "attributes"
""" The attributes value """

CLASS_NAME_VALUE = "class_name"
""" The class name value """

DATA_TYPE_VALUE = "data_type"
""" The data type value """

DESTINATION_PATH_VALUE = "destination_path"
""" The destination path value """

MODEL_VALUE = "model"
""" The model value """

NAME_VALUE = "name"
""" The name value """

NAME_LOWERCASE_VALUE = "name_lowercase"
""" The name lowercase value """

NAME_PLURAL_LOWERCASE_VALUE = "name_plural_lowercase"
""" The name plural lowercase value """

TEMPLATE_PATH_VALUE = "template_path"
""" The template path value """

VARIABLE_NAME_VALUE = "variable_name"
""" The variable name """

VARIABLE_NAME_PLURAL_VALUE = "variable_name_plural"
""" The variable name plural """

UNIX_DIRECTORY_SEPARATOR = "/"
""" The unix directory separator """

SCAFFOLDER_TYPE = "minimal_mvc"
""" The scaffolder type """

TEMPLATES_PATH = "minimal_mvc_scaffolder/scaffolder/resources/templates/"
""" The templates path """

TEMPLATES_BACKEND_PATH = TEMPLATES_PATH + "backend/"
""" The templates backend path """

TEMPLATES_BACKEND_RESOURCES_TEMPLATES_PATH = TEMPLATES_BACKEND_PATH + "resources/templates/"
""" The templates backend resources templates path """

TEMPLATES_BACKEND_RESOURCES_EXTRAS_JS_PATH = TEMPLATES_BACKEND_PATH + "resources/extras/js/"
""" The templates backend resources extras js path """

TEMPLATES = (
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_BACKEND_RESOURCES_EXTRAS_JS_PATH + "main.js.tpl",
        DESTINATION_PATH_VALUE : "${relative_backend_path}/resources/extras/js/main.js"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_BACKEND_RESOURCES_TEMPLATES_PATH + "edit.html.tpl",
        DESTINATION_PATH_VALUE : "${relative_backend_path}/resources/templates/edit.html.tpl"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_BACKEND_RESOURCES_TEMPLATES_PATH + "list.html.tpl",
        DESTINATION_PATH_VALUE : "${relative_backend_path}/resources/templates/list.html.tpl"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_BACKEND_RESOURCES_TEMPLATES_PATH + "new.html.tpl",
        DESTINATION_PATH_VALUE : "${relative_backend_path}/resources/templates/new.html.tpl"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_BACKEND_RESOURCES_TEMPLATES_PATH + "show.html.tpl",
        DESTINATION_PATH_VALUE : "${relative_backend_path}/resources/templates/show.html.tpl"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_BACKEND_PATH + "__init__.py.tpl",
        DESTINATION_PATH_VALUE : "${relative_backend_path}/__init__.py"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_BACKEND_PATH + "controllers.py.tpl",
        DESTINATION_PATH_VALUE : "${relative_backend_path}/${variable_name}_controllers.py"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_BACKEND_PATH + "entity_models.py.tpl",
        DESTINATION_PATH_VALUE : "${relative_backend_path}/${variable_name}_entity_models.py"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_BACKEND_PATH + "system.py.tpl",
        DESTINATION_PATH_VALUE : "${relative_backend_path}/${variable_name}_system.py"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_BACKEND_PATH + "__init__.py.tpl",
        DESTINATION_PATH_VALUE : "${relative_backend_root_path}/__init__.py"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_PATH + "plugin.py.tpl",
        DESTINATION_PATH_VALUE : "${variable_name}_plugin.py"
    }
)
""" The templates """

DEFAULT_MODEL_MAP = {
    NAME_VALUE : "DefaultModel",
    ATTRIBUTES_VALUE : (
        {
            NAME_VALUE : "value",
            DATA_TYPE_VALUE : "text"
        },
    )
}
""" The default model map """

class MinimalMvcScaffolder:
    """
    The minimal mvc scaffolder.
    """

    minimal_mvc_scaffolder_plugin = None
    """ The minimal mvc scaffolder plugin """

    def __init__(self, minimal_mvc_scaffolder_plugin):
        """
        Constructor of the class.

        @type minimal_mvc_scaffolder_plugin: MinimalMvcScaffolderPlugin
        @param minimal_mvc_scaffolder_plugin: The minimal mvc scaffolder plugin.
        """

        self.minimal_mvc_scaffolder_plugin = minimal_mvc_scaffolder_plugin

    def get_scaffolder_type(self):
        return SCAFFOLDER_TYPE

    def get_templates(self, scaffold_attributes_map):
        return TEMPLATES

    def process_scaffold_attributes(self, scaffold_attributes_map):
        # retrieves the model map
        model_map = scaffold_attributes_map.get(MODEL_VALUE, DEFAULT_MODEL_MAP)

        # creates a copy of the model map
        # to avoid manipulating the constant
        model_map = dict(model_map)

        # retrieves the model attributes
        class_name = model_map[NAME_VALUE]
        attributes = model_map[ATTRIBUTES_VALUE]

        # creates the variable name
        variable_name = colony.libs.string_util.convert_underscore(class_name)

        # creates the variable name plural
        variable_name_plural = colony.libs.string_util.pluralize(variable_name)

        # creates the lowercase version of the name
        name_lowercase = variable_name.replace("_", " ")
        name_plural_lowercase = variable_name_plural.replace("_", " ")

        # creates the name
        name = colony.libs.string_util.capitalize_all(name_lowercase)

        # sets the attributes in the model map
        model_map[VARIABLE_NAME_VALUE] = variable_name
        model_map[VARIABLE_NAME_PLURAL_VALUE] = variable_name_plural
        model_map[NAME_LOWERCASE_VALUE] = name_lowercase
        model_map[NAME_PLURAL_LOWERCASE_VALUE] = name_plural_lowercase
        model_map[CLASS_NAME_VALUE] = class_name
        model_map[NAME_VALUE] = name

        # sets the model in the scaffold attributes map
        scaffold_attributes_map[MODEL_VALUE] = model_map

        # for each model attribute
        for attribute_map in attributes:
            # retrieves the attribute name
            attribute_name = attribute_map[NAME_VALUE]

            # defines the lowercase version of the name
            name_lowercase = attribute_name.replace("_", " ")

            # sets the lowercase version of the name in the attribute map
            attribute_map[NAME_LOWERCASE_VALUE] = name_lowercase

    def process_template(self, template_path, template, scaffold_attributes_map):
        return template

    def generate_scaffold(self, scaffold_path, scaffold_attributes_map):
        pass
