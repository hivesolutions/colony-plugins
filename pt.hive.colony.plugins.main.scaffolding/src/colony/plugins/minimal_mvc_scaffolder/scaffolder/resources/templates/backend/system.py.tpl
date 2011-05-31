import os

import colony.libs.map_util

class ${out value=scaffold_attributes.class_name /}:
    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin):
        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin
        self.patterns = []

    def load_components(self):
        web_mvc_utils_plugin = self.${out value=scaffold_attributes.variable_name /}_plugin.web_mvc_utils_plugin
        entity_manager_arguments = {"engine" : "sqlite", "connection_parameters" : {"autocommit" : False}}
        entity_manager_parameters = {"default_database_prefix" : "${out value=scaffold_attributes.variable_name /}_"}
        entity_manager_arguments = web_mvc_utils_plugin.generate_entity_manager_arguments(self.${out value=scaffold_attributes.variable_name /}_plugin, entity_manager_arguments, entity_manager_parameters)
        web_mvc_utils_plugin.create_models("${out value=scaffold_attributes.variable_name /}_entity_models", self, self.${out value=scaffold_attributes.variable_name /}_plugin, entity_manager_arguments)
        web_mvc_utils_plugin.create_controllers("${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_controllers", self, self.${out value=scaffold_attributes.variable_name /}_plugin, "${out value=scaffold_attributes.variable_name /}")
        web_mvc_utils_plugin.generate_patterns(self.patterns, self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller, "${out value=scaffold_attributes.variable_name /}")

    def get_patterns(self):
        return self.patterns

    def get_resource_patterns(self):
        ${out value=scaffold_attributes.variable_name /}_plugin_path = self.${out value=scaffold_attributes.variable_name /}_plugin.manager.get_plugin_path_by_id(self.${out value=scaffold_attributes.variable_name /}_plugin.id)
        return ((r"^${out value=scaffold_attributes.variable_name /}/resources/.+$", (${out value=scaffold_attributes.variable_name /}_plugin_path + "/${out value=scaffold_attributes.relative_backend_path /}/resources/extras", "${out value=scaffold_attributes.variable_name /}/resources")),)
