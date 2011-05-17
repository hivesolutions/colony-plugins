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

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def handle_create(self, rest_request, parameters = {}):
        # processes the form data and retrieves the description
        form_data_map = self.process_form_data(rest_request, "utf-8")
        root_entity_description = form_data_map["root_entity"]["description"]

        # creates and stores a root entity
        ${out value=scaffold_attributes.variable_name /}_entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models
        root_entity = ${out value=scaffold_attributes.variable_name /}_entity_models.RootEntity()
        root_entity.description = root_entity_description
        root_entity.save()

        # processes the template and sets it as the response
        template_file = self.retrieve_template_file("${out value=scaffold_attributes.variable_name /}_list_contents.html.tpl")
        self.process_set_contents(rest_request, template_file)

        # returns true to indicate that the operation was successful
        return True

    def handle_list(self, rest_request, parameters = {}):
        # processes the template and sets it as the response
        template_file = self.retrieve_template_file("${out value=scaffold_attributes.variable_name /}_list_contents.html.tpl")
        self.process_set_contents(rest_request, template_file)

        # returns true to indicate that the operation was successful
        return True

    def handle_partial_list(self, rest_request, parameters = {}):
        # processes the form data and retrieves the search query
        form_data_map = self.process_form_data(rest_request, "utf-8")
        search_query = form_data_map["search_query"]
        start_record = form_data_map["start_record"]
        number_records = form_data_map["number_records"]
        start_record = int(start_record)
        number_records = int(number_records)

        # retrieves all root_entity entities and filters them
        ${out value=scaffold_attributes.variable_name /}_entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models
        entity_manager = ${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager
        root_entities = entity_manager._find_all_options(${out value=scaffold_attributes.variable_name /}_entity_models.RootEntity, {})
        filtered_root_entitys = [root_entity for root_entity in root_entities if not root_entity.description.find(search_query) == -1]

        # retrieves the specified page of root_entitys
        search_helper = parameters["search_helper"]
        results_tuple = search_helper.partial_filter(rest_request, filtered_root_entitys, start_record, number_records)
        partial_filtered_root_entitys, start_record, number_records, total_number_records = results_tuple

        # retrieves the template and assigns its values
        template_file = self.retrieve_template_file("${out value=scaffold_attributes.variable_name /}_partial_list_contents.html.tpl")
        template_file.assign("root_entitys", partial_filtered_root_entitys)
        template_file.assign("start_record", start_record)
        template_file.assign("number_records", number_records)
        template_file.assign("total_number_records", total_number_records)

        # processes the template and sets it as the response
        self.process_set_contents(rest_request, template_file)

        # returns true to indicate that the operation was successful
        return True

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def handle_delete(self, rest_request, parameters = {}):
        # retrieves the root_entity object id from the parameters
        pattern_names = parameters["pattern_names"]
        root_entity_object_id = pattern_names["root_entity_object_id"]
        root_entity_object_id = int(root_entity_object_id)

        # removes the root entity
        ${out value=scaffold_attributes.variable_name /}_entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models
        root_entity = ${out value=scaffold_attributes.variable_name /}_entity_models.RootEntity()
        root_entity.object_id = root_entity_object_id
        root_entity.remove()

        # processes the template and sets it as the response
        template_file = self.retrieve_template_file("${out value=scaffold_attributes.variable_name /}_list_contents.html.tpl")
        self.process_set_contents(rest_request, template_file)

        # returns true to indicate that the operation was successful
        return True
