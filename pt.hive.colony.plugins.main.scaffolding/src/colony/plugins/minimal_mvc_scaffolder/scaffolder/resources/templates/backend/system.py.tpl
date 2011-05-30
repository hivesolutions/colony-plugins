import os

import colony.libs.map_util

class ${out value=scaffold_attributes.class_name /}:
    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin):
        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin

    def load_components(self):
        # creates the entity manager arguments map
        entity_manager_arguments = {
            "engine" : "sqlite",
            "connection_parameters" : {
                "autocommit" : False
            }
        }

        # creates the entity manager parameters
        entity_manager_parameters = {
            "default_database_prefix" : "${out value=scaffold_attributes.variable_name /}_"
        }

        # creates the models and the controllers
        web_mvc_utils_plugin = self.${out value=scaffold_attributes.variable_name /}_plugin.web_mvc_utils_plugin
        entity_manager_arguments = web_mvc_utils_plugin.generate_entity_manager_arguments(self.${out value=scaffold_attributes.variable_name /}_plugin, entity_manager_arguments, entity_manager_parameters)
        web_mvc_utils_plugin.create_models("${out value=scaffold_attributes.variable_name /}_entity_models", self, self.${out value=scaffold_attributes.variable_name /}_plugin, entity_manager_arguments)
        web_mvc_utils_plugin.create_controllers("${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_controllers", self, self.${out value=scaffold_attributes.variable_name /}_plugin, "${out value=scaffold_attributes.variable_name /}")

    def get_patterns(self):
        return (
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_list, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/new$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_new, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/new$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_create, "post"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_show, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)/edit$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_edit, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)/update$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_update, "post"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)/delete$", self.${out value=scaffold_attributes.variable_name /}_${out value=scaffold_attributes.model.variable_name /}_controller.handle_delete, "get")
        )
