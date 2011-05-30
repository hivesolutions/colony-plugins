import os

import colony.libs.map_util

class ${out value=scaffold_attributes.class_name /}:
    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin):
        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin

    def load_components(self):
        # retrieves the database file path
        resource_manager_plugin = self.${out value=scaffold_attributes.variable_name /}_plugin.resource_manager_plugin
        system_database_filename_resource = resource_manager_plugin.get_resource("system.database.file_name")
        system_database_filename = "${out value=scaffold_attributes.variable_name /}_" + (system_database_filename_resource and system_database_filename_resource.data or "database.db")
        database_file_path = "%configuration:" + self.${out value=scaffold_attributes.variable_name /}_plugin.id + "%/" + system_database_filename

        # creates the entity manager arguments map
        entity_manager_arguments = {
            "engine" : "sqlite",
            "connection_parameters" : {
                "autocommit" : False,
                "file_path" : database_file_path
            }
        }

        # loads the models and controllers
        current_directory_path = os.path.dirname(__file__)
        web_mvc_utils_plugin = self.${out value=scaffold_attributes.variable_name /}_plugin.web_mvc_utils_plugin
        self.${out value=scaffold_attributes.variable_name /}_entity_models = web_mvc_utils_plugin.create_entity_models_path("${out value=scaffold_attributes.variable_name /}_entity_models", entity_manager_arguments, current_directory_path)
        ${out value=scaffold_attributes.variable_name /}_controllers = web_mvc_utils_plugin.import_module_mvc_utils("${out value=scaffold_attributes.variable_name /}_controllers", "${out value=scaffold_attributes.backend_namespace /}", current_directory_path)
        self.${out value=scaffold_attributes.model.variable_name /}_controller = web_mvc_utils_plugin.create_controller(${out value=scaffold_attributes.variable_name /}_controllers.${out value=scaffold_attributes.model.class_name /}Controller, [self.${out value=scaffold_attributes.variable_name /}_plugin, self], {})

    def get_patterns(self):
        return (
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}$", self.${out value=scaffold_attributes.model.variable_name /}_controller.handle_list, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/new$", self.${out value=scaffold_attributes.model.variable_name /}_controller.handle_new, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/new$", self.${out value=scaffold_attributes.model.variable_name /}_controller.handle_create, "post"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)$", self.${out value=scaffold_attributes.model.variable_name /}_controller.handle_show, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)/edit$", self.${out value=scaffold_attributes.model.variable_name /}_controller.handle_edit, "get"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)/update$", self.${out value=scaffold_attributes.model.variable_name /}_controller.handle_update, "post"),
            (r"^${out value=scaffold_attributes.variable_name /}/${out value=scaffold_attributes.model.variable_name_plural /}/(?P<${out value=scaffold_attributes.model.variable_name /}_object_id>[0-9]+)/delete$", self.${out value=scaffold_attributes.model.variable_name /}_controller.handle_delete, "get")
        )
