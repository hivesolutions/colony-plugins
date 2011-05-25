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

import os

RELATIVE_BACKEND_PATH_VALUE = "relative_backend_path"
""" The relative backend path value """

RELATIVE_PATH_VALUE = "relative_path"
""" The relative path value """

RELATIVE_DESTINATION_FILE_PATH_FORMAT = "relative_destination_file_path_format"
""" The relative destination file path format """

UNIX_DIRECTORY_SEPARATOR = "/"
""" The unix directory separator """

SCAFFOLDER_TYPE = "mvc_manager"
""" The scaffolder type """

BACKEND_TEMPLATES_PATH = "resources/templates"
""" The backend templates path """

TEMPLATES_PATH = "mvc_manager_scaffolder/scaffolder/resources/templates"
""" The templates path """

TEMPLATES_MAP = {
    "backend/controllers.py.tpl" : {
        RELATIVE_PATH_VALUE : TEMPLATES_PATH,
        RELATIVE_DESTINATION_FILE_PATH_FORMAT : "${relative_backend_path}/${variable_name}_controllers.py"
    },
    "backend/entity_models.py.tpl" : {
        RELATIVE_PATH_VALUE : TEMPLATES_PATH,
        RELATIVE_DESTINATION_FILE_PATH_FORMAT : "${relative_backend_path}/${variable_name}_entity_models.py"
    },
    "backend/exceptions.py.tpl" : {
        RELATIVE_PATH_VALUE : TEMPLATES_PATH,
        RELATIVE_DESTINATION_FILE_PATH_FORMAT : "${relative_backend_path}/${variable_name}_exceptions.py"
    },
    "backend/system.py.tpl" : {
       RELATIVE_PATH_VALUE : TEMPLATES_PATH,
       RELATIVE_DESTINATION_FILE_PATH_FORMAT : "${relative_backend_path}/${variable_name}_system.py"
    },
    "backend/test.py.tpl" : {
        RELATIVE_PATH_VALUE : TEMPLATES_PATH,
        RELATIVE_DESTINATION_FILE_PATH_FORMAT : "${relative_backend_path}/${variable_name}_test.py"
    },
    "plugin.py.tpl" : {
        RELATIVE_PATH_VALUE : TEMPLATES_PATH,
        RELATIVE_DESTINATION_FILE_PATH_FORMAT : "${variable_name}_plugin.py"
    }
}
""" The templates map """

class MvcManagerScaffolder:
    """
    The mvc manager scaffolder.
    """

    mvc_manager_scaffolder_plugin = None
    """ The mvc scaffolder plugin """

    def __init__(self, mvc_manager_scaffolder_plugin):
        """
        Constructor of the class.

        @type mvc_manager_scaffolder_plugin: MvcManagerScaffolderPlugin
        @param mvc_manager_scaffolder_plugin: The mvc manager scaffolder plugin.
        """

        self.mvc_manager_scaffolder_plugin = mvc_manager_scaffolder_plugin

    def get_scaffolder_type(self):
        return SCAFFOLDER_TYPE

    def get_templates(self, scaffold_attributes_map):
        return TEMPLATES_MAP

    def process_scaffold_attributes(self, scaffold_attributes_map):
        pass

    def process_template(self, template_file_name, template, scaffold_attributes_map):
        return template

    def generate_scaffold(self, scaffold_path, scaffold_attributes_map):
        # retrieves the relative backend path
        relative_backend_path = scaffold_attributes_map[RELATIVE_BACKEND_PATH_VALUE]

        # defines the templates path
        templates_path = scaffold_path + UNIX_DIRECTORY_SEPARATOR + relative_backend_path + UNIX_DIRECTORY_SEPARATOR + BACKEND_TEMPLATES_PATH

        # checks if the path exists
        path_exists = os.path.exists(templates_path)

        # creates the directories for the templates path
        # in case the path does not exist
        not path_exists and os.makedirs(templates_path)
