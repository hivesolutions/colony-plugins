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

__author__ = "Tiago Silva <tsilva@hive.pt> & João Magalhães <joamag@hive.pt>"
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
import re

import colony.libs.structures_util

import main_scaffolding_exceptions

AUTHOR_VALUE = "author"
""" The author value """

BACKEND_NAMESPACE_VALUE = "backend_namespace"
""" The backend namespace value """

CLASS_NAME_VALUE = "class_name"
""" The class name value """

DESCRIPTION_VALUE = "description"
""" The description value """

DESTINATION_PATH_VALUE = "destination_path"
""" The destination path value """

PLUGIN_ID_VALUE = "plugin_id"
""" The plugin id value """

PLUGIN_VERSION_VALUE = "plugin_version"
""" The plugin version value """

PLUGINS_VALUE = "plugins"
""" The plugins value """

PROCESS_VALUE = "process"
""" The process value """

SCAFFOLD_ATTRIBUTES_VALUE = "scaffold_attributes"
""" The scaffold attributes value """

SHORT_NAME_VALUE = "short_name"
""" The short name value """

SHORT_NAME_LOWERCASE_VALUE = "short_name_lowercase"
""" The short name lowercase value """

SHORT_NAME_UPPERCASE_VALUE = "short_name_uppercase"
""" The short name uppercase value """

RELATIVE_BACKEND_PATH_VALUE = "relative_backend_path"
""" The relative backend path """

RELATIVE_BACKEND_ROOT_PATH_VALUE = "relative_backend_root_path"
""" The relative backend root path value """

TEMPLATE_PATH_VALUE = "template_path"
""" The template path """

VARIABLE_NAME_VALUE = "variable_name"
""" The variable name value """

ATTRIBUTE_KEY_FORMAT = "${%s}"
""" The attribute key format """

ATTRIBUTE_REGEX = re.compile("\$\{([a-z_]*)\}")
""" The attribute regex """

DESCRIPTION_FORMAT = "The %s"
""" The description format """

DEFAULT_AUTHOR = "Hive Solutions Lda. <development@hive.pt>"
""" The default author """

DEFAULT_ENCODING = "Cp1252"
""" The default encoding """

PLUGIN_ID_REGEX = re.compile("[a-z][a-z0-9_]*[a-z0-9]+\.(?:[a-z][a-z0-9_]*[a-z0-9]+\.)*[a-z][a-z0-9_]*[a-z0-9]+")
""" The plugin id regex """

UNIX_DIRECTORY_SEPARATOR = "/"
""" The unix directory separator """

EXTRAS_PATH = "extras"
""" The extras path """

class MainScaffolding:
    """
    The main scaffolding.
    """

    main_scaffolding_plugin = None
    """ The main scaffolding plugin """

    scaffolder_plugins_map = None
    """ The scaffolder plugins map """

    def __init__(self, main_scaffolding_plugin):
        """
        Constructor of the class.

        @type main_scaffolding_plugin: MainScaffoldingPlugin
        @param main_scaffolding_plugin: The main scaffolding plugin.
        """

        self.main_scaffolding_plugin = main_scaffolding_plugin

        # initializes the structures
        self.scaffolder_plugins_map = colony.libs.structures_util.MultipleValueMap()

    def load_scaffolder_plugin(self, scaffolder_plugin):
        # retrieves the scaffolder type
        scaffolder_type = scaffolder_plugin.get_scaffolder_type()

        # sets the scaffolder plugin in the map
        self.scaffolder_plugins_map[scaffolder_type] = scaffolder_plugin

    def unload_scaffolder_plugin(self, scaffolder_plugin):
        # retrieves the scaffolder type
        scaffolder_type = scaffolder_plugin.get_scaffolder_type()

        # unsets the scaffolder plugin from the map
        self.scaffolder_plugins_map.unset(scaffolder_type, scaffolder_plugin)

    def get_scaffolder_types(self):
        # retrieves the scaffolder types
        scaffolder_types = self.scaffolder_plugins_map.keys()

        # returns the scaffolder types
        return scaffolder_types

    def generate_scaffolds(self, scaffolder_types, plugin_id, plugin_version, scaffold_path, specification_file_path):
        # for each scaffolder type
        for scaffolder_type in scaffolder_types:
            # generates the scaffold for that type
            self.generate_scaffold(scaffolder_type, plugin_id, plugin_version, scaffold_path, specification_file_path)

    def generate_scaffold(self, scaffolder_type, plugin_id, plugin_version, scaffold_path, specification_file_path):
        # retrieves the plugin manager
        plugin_manager = self.main_scaffolding_plugin.manager

        # retrieves the scaffolder plugin
        scaffolder_plugin = self._get_scaffolder_plugin(scaffolder_type)

        # validates the plugin id
        self._validate_plugin_id(plugin_id)

        # checks id the scaffold path exists
        scaffold_path_exists = os.path.exists(scaffold_path)

        # makes the directories for the scaffold path
        # (in case it's necessary)
        not scaffold_path_exists and os.makedirs(scaffold_path)

        # initializes the scaffold attributes map
        scaffold_attributes_map = {}

        # loads the specification in case one was specified
        scaffold_attributes_map = specification_file_path and self._get_json_data(specification_file_path) or scaffold_attributes_map

        # sets the plugin id in the scaffold attributes map
        scaffold_attributes_map[PLUGIN_ID_VALUE] = plugin_id

        # sets the plugin version in the scaffold attributes map
        scaffold_attributes_map[PLUGIN_VERSION_VALUE] = plugin_version

        # processes the scaffold attributes map
        self.process_scaffold_attributes(scaffold_attributes_map)

        # processes the scaffold attributes map with the scaffolder plugin
        scaffolder_plugin.process_scaffold_attributes(scaffold_attributes_map)

        # retrieves the scaffolder's templates
        templates = scaffolder_plugin.get_templates(scaffold_attributes_map)

        # retrieves the scaffolder plugin path
        scaffolder_plugin_path = plugin_manager.get_plugin_path_by_id(scaffolder_plugin.id)

        # for each template in the templates map
        for template_map in templates:
            # retrieves the mandatory template attributes
            relative_template_file_path = template_map[TEMPLATE_PATH_VALUE]
            relative_destination_file_path_format = template_map[DESTINATION_PATH_VALUE]

            # retrieves the optional template attributes
            process_template = template_map.get(PROCESS_VALUE, True)

            # defines the template file path
            template_file_path = scaffolder_plugin_path + UNIX_DIRECTORY_SEPARATOR + relative_template_file_path

            # applies the attributes to the relative destination file path format
            relative_destination_file_path = self._apply_attributes(relative_destination_file_path_format, scaffold_attributes_map)

            # defines the destination file path
            destination_file_path = scaffold_path + UNIX_DIRECTORY_SEPARATOR + relative_destination_file_path

            # processes the template
            processed_template = process_template and self.process_template(template_file_path, scaffold_attributes_map) or self._get_file_data(template_file_path)

            # processes the template with the scaffolder
            processed_template = process_template and scaffolder_plugin.process_template(relative_template_file_path, processed_template, scaffold_attributes_map) or processed_template

            # creates the destination file
            self._create_file(destination_file_path, processed_template)

        # generates the scaffolder's part of the scaffold
        scaffolder_plugin.generate_scaffold(scaffold_path, scaffold_attributes_map)

        # adds the scaffold path to the plugin paths (and persists it)
        plugin_manager.add_plugin_path(scaffold_path, True)

    def process_scaffold_attributes(self, scaffold_attributes_map):
        # retrieves the mandatory scaffold attributes
        plugin_id = scaffold_attributes_map[PLUGIN_ID_VALUE]

        # retrieves the optional attributes
        short_name = scaffold_attributes_map.get(SHORT_NAME_VALUE)
        description = scaffold_attributes_map.get(DESCRIPTION_VALUE)
        author = scaffold_attributes_map.get(AUTHOR_VALUE, DEFAULT_AUTHOR)
        variable_name = scaffold_attributes_map.get(VARIABLE_NAME_VALUE)
        relative_backend_path = scaffold_attributes_map.get(RELATIVE_BACKEND_PATH_VALUE)

        # retrieves the plugins index
        plugins_index = plugin_id.find(PLUGINS_VALUE)

        # calculates the plugins length
        plugins_length = len(PLUGINS_VALUE)

        # calculates the short name index
        short_name_index = plugins_index + plugins_length

        # sets the short name index to zero in case plugins was not found
        short_name_index = plugins_index > -1 and short_name_index or 0

        # creates the short name out of the id suffix in case none is defined
        short_name = short_name or plugin_id[short_name_index:]

        # replaces id separation characters with spaces
        short_name = short_name.replace(".", " ")
        short_name = short_name.replace("_", " ")

        # capitalizes the short name words
        short_name = colony.libs.string_util.capitalize_all(short_name)

        # defines the lowercase version of the short name
        short_name_lowercase = short_name.lower()

        # defines the uppercase version of the short name
        short_name_uppercase = short_name.upper()

        # defines the variable name
        variable_name = variable_name or short_name_lowercase.replace(" ", "_")

        # retrieves the variable name tokens
        variable_name_tokens = variable_name.split("_")

        # retrieves the number of variable name tokens
        number_variable_name_tokens = len(variable_name_tokens)

        # defines the root folder name
        root_folder_name = variable_name

        # defines the sub folder name
        sub_folder_name = number_variable_name_tokens > 1 and variable_name_tokens[-1] or variable_name

        # defines the relative backend path
        relative_backend_path = root_folder_name + UNIX_DIRECTORY_SEPARATOR + sub_folder_name

        # defines the class name
        class_name = colony.libs.string_util.convert_camelcase(variable_name)

        # defines the description
        description = description or DESCRIPTION_FORMAT % short_name_lowercase

        # defines the backend namespace
        backend_namespace = relative_backend_path.replace(UNIX_DIRECTORY_SEPARATOR, ".")

        # sets the attributes in the scaffold attributes map
        scaffold_attributes_map[RELATIVE_BACKEND_ROOT_PATH_VALUE] = root_folder_name
        scaffold_attributes_map[RELATIVE_BACKEND_PATH_VALUE] = relative_backend_path
        scaffold_attributes_map[SHORT_NAME_VALUE] = short_name
        scaffold_attributes_map[SHORT_NAME_LOWERCASE_VALUE] = short_name_lowercase
        scaffold_attributes_map[SHORT_NAME_UPPERCASE_VALUE] = short_name_uppercase
        scaffold_attributes_map[AUTHOR_VALUE] = author
        scaffold_attributes_map[VARIABLE_NAME_VALUE] = variable_name
        scaffold_attributes_map[CLASS_NAME_VALUE] = class_name
        scaffold_attributes_map[DESCRIPTION_VALUE] = description
        scaffold_attributes_map[BACKEND_NAMESPACE_VALUE] = backend_namespace

    def process_template(self, template_file_path, scaffold_attributes_map):
        # retrieves the template engine manager plugin
        template_engine_manager_plugin = self.main_scaffolding_plugin.template_engine_manager_plugin

        # parses the template file path
        template_file = template_engine_manager_plugin.parse_file_path_encoding(template_file_path, DEFAULT_ENCODING)

        # assigns the scaffold attributes to the template
        template_file.assign(SCAFFOLD_ATTRIBUTES_VALUE, scaffold_attributes_map)

        # processes the template
        processed_template = template_file.process()

        # returns the processed template
        return processed_template

    def _validate_plugin_id(self, plugin_id):
        # matches the plugin id against the regular expression
        plugin_id_matches = PLUGIN_ID_REGEX.findall(plugin_id)

        # retrieves the plugin id match
        plugin_id_match = plugin_id_matches and plugin_id_matches[0] or None

        # in case the plugin id match isn't the plugin id
        if not plugin_id_match == plugin_id:
            # raises an invalid plugin identifier exception
            raise main_scaffolding_exceptions.InvalidPluginIdentifier("plugin identifier is invalid")

    def _get_scaffolder_plugin(self, scaffolder_type):
        # retrieves the scaffolder for the specified type
        scaffolder_plugin = self.scaffolder_plugins_map[scaffolder_type]

        # in case no scaffolder plugin was found
        if not scaffolder_plugin:
            # raises a scaffolder type not supported exception
            raise main_scaffolding_exceptions.ScaffolderTypeNotSupported("the specified scaffolder type is not supported")

        # returns the scaffolder plugin
        return scaffolder_plugin

    def _apply_attributes(self, data, attributes_map):
        # retrieves the attribute names
        attribute_names = ATTRIBUTE_REGEX.findall(data)

        # replaces the attributes in the data
        for attribute_name in attribute_names:
            # retrieves the attribute value
            attribute_value = attributes_map[attribute_name]

            # defines the attribute key
            attribute_key = ATTRIBUTE_KEY_FORMAT % attribute_name

            # replaces the attribute
            data = data.replace(attribute_key, attribute_value)

        # returns the data
        return data

    def _create_file(self, file_path, contents = ""):
        # splits the file path
        directory_path, file_name = os.path.split(file_path)

        # creates the directories in case they don't exist
        not os.path.exists(directory_path) and os.makedirs(directory_path)

        # opens the file
        file = open(file_path, "wb")

        # encodes the contents
        contents = contents.encode(DEFAULT_ENCODING)

        try:
            # writes the contents
            file.write(contents)
        finally:
            # closes the file
            file.close()

    def _get_json_data(self, json_file_path):
        # retrieves the json plugin
        json_plugin = self.main_scaffolding_plugin.json_plugin

        # reads the json file
        json_file_data = self._get_file_data(json_file_path)

        # loads the json data from the json file
        json_data = json_plugin.loads(json_file_data)

        # returns the json data
        return json_data

    def _get_file_data(self, file_path):
        # opens the file
        file = open(file_path, "rb")

        try:
            # reads the data from the file
            data = file.read()
        finally:
            # closes the file
            file.close()

        # decodes the data
        data = data.decode(DEFAULT_ENCODING)

        # returns the data
        return data

    def _get_scaffold_path(self, plugin_id):
        # retrieves the plugin manager
        plugin_manager = self.main_scaffolding_plugin.manager

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # creates the extras path from the variable path
        extras_path = os.path.join(variable_path, EXTRAS_PATH)

        # creates the scaffold path by joining the plugin id to
        # the extras path
        scaffold_path = os.path.join(extras_path, plugin_id)

        # returns the scaffold path (for the plugin id)
        return scaffold_path
