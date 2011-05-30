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

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

RESOURCES_PATH = "${out value=scaffold_attributes.relative_backend_path /}/resources"
""" The resources path """

TEMPLATES_PATH = RESOURCES_PATH + "/templates"
""" The templates path """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__("web_mvc_utils")

class ${out value=scaffold_attributes.model.class_name /}Controller:
    """
    The ${out value=scaffold_attributes.model.name_lowercase /} controller.
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

        # sets the relative resources path
        self.set_relative_resources_path(RESOURCES_PATH)

    def handle_list(self, rest_request, parameters = {}):
        # retrieves the ${out value=scaffold_attributes.model.name_lowercase /} entities
        ${out value=scaffold_attributes.model.variable_name /}_entities = self._get_${out value=scaffold_attributes.model.variable_name_plural /}(rest_request, {})

        # retrieves the template file
        template_file = self.retrieve_template_file("list.html.tpl")

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # assigns the ${out value=scaffold_attributes.model.name_lowercase /} entities to the template file
        template_file.assign("${out value=scaffold_attributes.model.variable_name_plural /}", ${out value=scaffold_attributes.model.variable_name /}_entities)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    def handle_show(self, rest_request, parameters = {}):
        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the ${out value=scaffold_attributes.model.name_lowercase /} object id pattern
        ${out value=scaffold_attributes.model.variable_name /}_object_id = pattern_names["${out value=scaffold_attributes.model.variable_name /}_object_id"]

        # converts the ${out value=scaffold_attributes.model.name_lowercase /} object id to integer
        ${out value=scaffold_attributes.model.variable_name /}_object_id = int(${out value=scaffold_attributes.model.variable_name /}_object_id)

        # retrieves the specified ${out value=scaffold_attributes.model.name_lowercase /}
        ${out value=scaffold_attributes.model.variable_name /}_entity = self._get_${out value=scaffold_attributes.model.variable_name /}(rest_request, ${out value=scaffold_attributes.model.variable_name /}_object_id)

        # retrieves the template file
        template_file = self.retrieve_template_file("show.html.tpl")

        # assigns the ${out value=scaffold_attributes.model.name_lowercase /} entity to the template file
        template_file.assign("${out value=scaffold_attributes.model.variable_name /}", ${out value=scaffold_attributes.model.variable_name /}_entity)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    def handle_new(self, rest_request, parameters = {}):
        # retrieves the template file
        template_file = self.retrieve_template_file("new.html.tpl")

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    def handle_create(self, rest_request, parameters = {}):
        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the ${out value=scaffold_attributes.model.name_lowercase /}
        ${out value=scaffold_attributes.model.variable_name /} = form_data_map.get("${out value=scaffold_attributes.model.variable_name /}", {})

        # saves the ${out value=scaffold_attributes.model.name_lowercase /}
        self._save_${out value=scaffold_attributes.model.variable_name /}(rest_request, ${out value=scaffold_attributes.model.variable_name /})

        # redirects to the ${out value=scaffold_attributes.model.name_lowercase /} entities page
        self.redirect_base_path(rest_request, "${out value=scaffold_attributes.model.variable_name_plural /}")

    def handle_edit(self, rest_request, parameters = {}):
        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the ${out value=scaffold_attributes.model.name_lowercase /} object id pattern
        ${out value=scaffold_attributes.model.variable_name /}_object_id = pattern_names["${out value=scaffold_attributes.model.variable_name /}_object_id"]

        # converts the ${out value=scaffold_attributes.model.name_lowercase /} object id to integer
        ${out value=scaffold_attributes.model.variable_name /}_object_id = int(${out value=scaffold_attributes.model.variable_name /}_object_id)

        # retrieves the specified ${out value=scaffold_attributes.model.name_lowercase /}
        ${out value=scaffold_attributes.model.variable_name /}_entity = self._get_${out value=scaffold_attributes.model.variable_name /}(rest_request, ${out value=scaffold_attributes.model.variable_name /}_object_id)

        # retrieves the template file
        template_file = self.retrieve_template_file("edit.html.tpl")

        # assigns the ${out value=scaffold_attributes.model.name_lowercase /} to the template file
        template_file.assign("${out value=scaffold_attributes.model.variable_name /}", ${out value=scaffold_attributes.model.variable_name /}_entity)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    def handle_update(self, rest_request, parameters = {}):
        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the ${out value=scaffold_attributes.model.name_lowercase /}
        ${out value=scaffold_attributes.model.variable_name /} = form_data_map.get("${out value=scaffold_attributes.model.variable_name /}", {})

        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the ${out value=scaffold_attributes.model.name_lowercase /} object id pattern
        ${out value=scaffold_attributes.model.variable_name /}_object_id = pattern_names["${out value=scaffold_attributes.model.variable_name /}_object_id"]

        # converts the ${out value=scaffold_attributes.model.name_lowercase /} object id to integer
        ${out value=scaffold_attributes.model.variable_name /}_object_id = int(${out value=scaffold_attributes.model.variable_name /}_object_id)

        # sets the object id in the ${out value=scaffold_attributes.model.name_lowercase /}
        ${out value=scaffold_attributes.model.variable_name /}["object_id"] = ${out value=scaffold_attributes.model.variable_name /}_object_id

        # updates the ${out value=scaffold_attributes.model.name_lowercase /}
        self._save_${out value=scaffold_attributes.model.variable_name /}(rest_request, ${out value=scaffold_attributes.model.variable_name /})

        # redirects to the ${out value=scaffold_attributes.model.name_plural_lowercase /} entities page
        self.redirect_base_path(rest_request, "${out value=scaffold_attributes.model.variable_name_plural /}")

    def handle_delete(self, rest_request, parameters = {}):
        # retrieves the pattern names from the parameters
        pattern_names = parameters[PATTERN_NAMES_VALUE]

        # retrieves the ${out value=scaffold_attributes.model.name_lowercase /} object id pattern
        ${out value=scaffold_attributes.model.variable_name /}_object_id = pattern_names["${out value=scaffold_attributes.model.variable_name /}_object_id"]

        # converts the ${out value=scaffold_attributes.model.name_lowercase /} object id to integer
        ${out value=scaffold_attributes.model.variable_name /}_object_id = int(${out value=scaffold_attributes.model.variable_name /}_object_id)

        # creates the ${out value=scaffold_attributes.model.name_lowercase /}
        ${out value=scaffold_attributes.model.variable_name /} = {
            "object_id" : ${out value=scaffold_attributes.model.variable_name /}_object_id
        }

        # deletes the specified ${out value=scaffold_attributes.model.name_lowercase /}
        self._delete_${out value=scaffold_attributes.model.variable_name /}(rest_request, ${out value=scaffold_attributes.model.variable_name /})

        # redirects to the ${out value=scaffold_attributes.model.name_plural_lowercase /} page
        self.redirect_base_path(rest_request, "${out value=scaffold_attributes.model.variable_name_plural /}")

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def _save_${out value=scaffold_attributes.model.variable_name /}(self, rest_request, ${out value=scaffold_attributes.model.variable_name /}):
        # retrieves the ${out value=scaffold_attributes.short_name_lowercase /} entity models
        ${out value=scaffold_attributes.variable_name /}_entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models

        # creates the ${out value=scaffold_attributes.model.name_lowercase /} entity
        ${out value=scaffold_attributes.model.variable_name /}_entity = self.get_entity_model(${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager, ${out value=scaffold_attributes.variable_name /}_entity_models.${out value=scaffold_attributes.model.class_name /}, ${out value=scaffold_attributes.model.variable_name /})

        # validates the ${out value=scaffold_attributes.model.name_lowercase /} entity
        self.validate_model_exception(${out value=scaffold_attributes.model.variable_name /}_entity, "${out value=scaffold_attributes.model.name_lowercase /} validation failed")

        # saves the ${out value=scaffold_attributes.model.name_lowercase /} entity
        ${out value=scaffold_attributes.model.variable_name /}_entity.save_update()

        # returns the ${out value=scaffold_attributes.model.name_lowercase /} entity
        return ${out value=scaffold_attributes.model.variable_name /}_entity

    def _get_${out value=scaffold_attributes.model.variable_name_plural /}(self, rest_request, filter):
        # retrieves the entity models
        ${out value=scaffold_attributes.variable_name /}_entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models

        # retrieves the specified ${out value=scaffold_attributes.model.name_lowercase /} entities
        ${out value=scaffold_attributes.model.variable_name /}_entities = ${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager._find_all_options(${out value=scaffold_attributes.variable_name /}_entity_models.${out value=scaffold_attributes.model.class_name /}, filter)

        # returns the ${out value=scaffold_attributes.model.name_lowercase /} entities
        return ${out value=scaffold_attributes.model.variable_name /}_entities

    def _get_${out value=scaffold_attributes.model.variable_name /}(self, rest_request, ${out value=scaffold_attributes.model.variable_name /}_object_id):
        # retrieves the entity models
        ${out value=scaffold_attributes.variable_name /}_entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models

        # retrieves the specified ${out value=scaffold_attributes.model.name_lowercase /} entity
        ${out value=scaffold_attributes.model.variable_name /}_entity = ${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager.find(${out value=scaffold_attributes.variable_name /}_entity_models.${out value=scaffold_attributes.model.class_name /}, ${out value=scaffold_attributes.model.variable_name /}_object_id)

        # returns the ${out value=scaffold_attributes.model.name_lowercase /} entity
        return ${out value=scaffold_attributes.model.variable_name /}_entity

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def _delete_${out value=scaffold_attributes.model.variable_name /}(self, rest_request, ${out value=scaffold_attributes.model.variable_name /}):
        # retrieves the entity models
        ${out value=scaffold_attributes.variable_name /}_entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models

        # retrieves the ${out value=scaffold_attributes.model.name_lowercase /} object id
        ${out value=scaffold_attributes.model.variable_name /}_object_id = ${out value=scaffold_attributes.model.variable_name /}["object_id"]

        # creates a new ${out value=scaffold_attributes.model.name_lowercase /} entity
        ${out value=scaffold_attributes.model.variable_name /}_entity = ${out value=scaffold_attributes.variable_name /}_entity_models.${out value=scaffold_attributes.model.class_name /}()

        # sets the object id in the ${out value=scaffold_attributes.model.name_lowercase /} entity
        ${out value=scaffold_attributes.model.variable_name /}_entity.object_id = ${out value=scaffold_attributes.model.variable_name /}_object_id

        # removes the ${out value=scaffold_attributes.model.name_lowercase /} entity
        ${out value=scaffold_attributes.model.variable_name /}_entity.remove()
