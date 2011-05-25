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

import colony.libs.importer_util

PATTERN_NAMES_VALUE = "pattern_names"
""" The pattern names value """

SERIALIZER_VALUE = "serializer"
""" The serializer value """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

TEMPLATES_PATH = "${out value=scaffold_attributes.relative_backend_path /}/resources/templates"
""" The templates path """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__("web_mvc_utils")

class RootEntityController:
    """
    The root entity controller.
    """

    ${out value=scaffold_attributes.variable_name /}_plugin = None
    """ The ${out value=scaffold_attributes.short_name_lowercase /} plugin """

    ${out value=scaffold_attributes.variable_name /} = None
    """ The ${out value=scaffold_attributes.short_name_lowercase /} """

    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin, ${out value=scaffold_attributes.variable_name /}):
        """
        Constructor of the class.

        @type ${out value=scaffold_attributes.variable_name /}_plugin: ${out value=scaffold_attributes.class_name /}Plugin
        @param ${out value=scaffold_attributes.variable_name /}_plugin: The ${out value=scaffold_attributes.short_name_lowercase /} plugin.
        @type ${out value=scaffold_attributes.variable_name /}: ${out value=scaffold_attributes.class_name /}
        @param ${out value=scaffold_attributes.variable_name /}: The ${out value=scaffold_attributes.short_name_lowercase /}.
        """

        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin
        self.${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.variable_name /}

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.${out value=scaffold_attributes.variable_name /}_plugin.manager

        # retrieves the ${out value=scaffold_attributes.short_name_lowercase /} plugin path
        ${out value=scaffold_attributes.variable_name /}_plugin_path = plugin_manager.get_plugin_path_by_id(self.${out value=scaffold_attributes.variable_name /}_plugin.id)

        # creates the templates path
        templates_path = ${out value=scaffold_attributes.variable_name /}_plugin_path + "/" + TEMPLATES_PATH

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_list(self, rest_request, parameters = {}):
        # retrieves the root entities
        root_entities = self._get_root_entities(rest_request, {})

        # retrieves the template file
        template_file = self.retrieve_template_file("list.html.tpl")

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # assigns the root entities to the template file
        template_file.assign("root_entities", root_entities)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_show(self, rest_request, parameters = {}):
        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the root entity object id pattern
        root_entity_object_id = pattern_names["root_entity_object_id"]

        # converts the root entity object id to integer
        root_entity_object_id = int(root_entity_object_id)

        # retrieves the specified root entity
        root_entity = self._get_root_entity(rest_request, root_entity_object_id)

        # retrieves the template file
        template_file = self.retrieve_template_file("show.html.tpl")

        # assigns the root entity to the template file
        template_file.assign("root_entity", root_entity)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_new(self, rest_request, parameters = {}):
        # retrieves the template file
        template_file = self.retrieve_template_file("new.html.tpl")

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_create(self, rest_request, parameters = {}):
        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the root entity
        root_entity = form_data_map.get("root_entity", {})

        # saves the root entity
        self._save_root_entity(rest_request, root_entity)

        # redirects to the root entities page
        self.redirect_base_path(rest_request, "root_entities")

        # returns true
        return True

    def handle_edit(self, rest_request, parameters = {}):
        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the root entity object id pattern
        root_entity_object_id = pattern_names["root_entity_object_id"]

        # converts the root entity object id to integer
        root_entity_object_id = int(root_entity_object_id)

        # retrieves the specified root entity
        root_entity = self._get_root_entity(rest_request, root_entity_object_id)

        # retrieves the template file
        template_file = self.retrieve_template_file("edit.html.tpl")

        # assigns the root entity to the template file
        template_file.assign("root_entity", root_entity)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_update(self, rest_request, parameters = {}):
        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the root entity
        root_entity = form_data_map.get("root_entity", {})

        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the root entity object id pattern
        root_entity_object_id = pattern_names["root_entity_object_id"]

        # converts the root entity object id to integer
        root_entity_object_id = int(root_entity_object_id)

        # sets the object id in the root entity
        root_entity["object_id"] = root_entity_object_id

        # updates the root entity
        self._save_root_entity(rest_request, root_entity)

        # redirects to the root entities page
        self.redirect_base_path(rest_request, "root_entities")

        # returns true
        return True

    def handle_delete(self, rest_request, parameters = {}):
        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the root entity object id pattern
        root_entity_object_id = pattern_names["root_entity_object_id"]

        # converts the root entity object id to integer
        root_entity_object_id = int(root_entity_object_id)

        # creates the root entity
        root_entity = {
            "object_id" : root_entity_object_id
        }

        # deletes the specified root entity
        self._delete_root_entity(rest_request, root_entity)

        # redirects to the root entities page
        self.redirect_base_path(rest_request, "root_entities")

        # returns true
        return True

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def _save_root_entity(self, rest_request, root_entity):
        # retrieves the ${out value=scaffold_attributes.short_name_lowercase /} entity models
        ${out value=scaffold_attributes.variable_name /}_entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models

        # retrieves the root entity
        root_entity = self.get_entity_model(${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager, ${out value=scaffold_attributes.variable_name /}_entity_models.RootEntity, root_entity)

        # validates the root entity
        self.validate_model_exception(root_entity, "root entity validation failed")

        # saves the root entity
        root_entity.save_update()

        # returns the root entity
        return root_entity

    def _get_root_entities(self, rest_request, filter):
        # retrieves the entity models
        ${out value=scaffold_attributes.variable_name /}_entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models

        # retrieves the specified root entities
        root_entities = ${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager._find_all_options(${out value=scaffold_attributes.variable_name /}_entity_models.RootEntity, filter)

        # returns the root entities
        return root_entities

    def _get_root_entity(self, rest_request, root_entity_object_id):
        # retrieves the entity models
        ${out value=scaffold_attributes.variable_name /}_entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models

        # retrieves the specified root entity
        root_entity = ${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager.find(${out value=scaffold_attributes.variable_name /}_entity_models.RootEntity, root_entity_object_id)

        # returns the root entity
        return root_entity

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def _delete_root_entity(self, rest_request, root_entity):
        # retrieves the entity models
        ${out value=scaffold_attributes.variable_name /}_entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models

        # retrieves the root entity object id
        root_entity_object_id = root_entity["object_id"]

        # creates a new root entity
        root_entity = ${out value=scaffold_attributes.variable_name /}_entity_models.RootEntity()

        # sets the object id in the root entity
        root_entity.object_id = root_entity_object_id

        # removes the root entity
        root_entity.remove()
