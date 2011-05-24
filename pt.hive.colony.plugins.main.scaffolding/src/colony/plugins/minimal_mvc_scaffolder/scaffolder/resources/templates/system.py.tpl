import os

class ${out value=scaffold_attributes.class_name /}:
    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin):
        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin

    def load_components(self):
        # retrieves the database file path
        resource_manager_plugin = self.${out value=scaffold_attributes.variable_name /}_plugin.resource_manager_plugin
        system_database_filename_resource = resource_manager_plugin.get_resource("system.database.file_name")
        system_database_filename_suffix = system_database_filename_resource and system_database_filename_resource.data or "database.db"
        system_database_filename = "${out value=scaffold_attributes.variable_name /}_" + system_database_filename_suffix
        ${out value=scaffold_attributes.variable_name /}_plugin_id = self.${out value=scaffold_attributes.variable_name /}_plugin.id
        database_file_path = "%configuration:" + ${out value=scaffold_attributes.variable_name /}_plugin_id + "%/" + system_database_filename

        # creates the entity manager arguments map
        entity_manager_arguments = {
            "engine" : "sqlite",
            "connection_parameters" : {
                "autocommit" : False,
                "file_path" : database_file_path
            }
        }

        # creates the models and controllers
        web_mvc_utils_plugin = self.${out value=scaffold_attributes.variable_name /}_plugin.web_mvc_utils_plugin
        current_directory_path = os.path.dirname(__file__)
        ${out value=scaffold_attributes.variable_name /}_controllers = web_mvc_utils_plugin.import_module_mvc_utils("${out value=scaffold_attributes.variable_name /}_controllers", "${out value=scaffold_attributes.backend_namespace /}", current_directory_path)
        self.${out value=scaffold_attributes.variable_name /}_entity_models = web_mvc_utils_plugin.create_entity_models("${out value=scaffold_attributes.variable_name /}_entity_models", entity_manager_arguments, current_directory_path)
        self.root_entity_controller = web_mvc_utils_plugin.create_controller(${out value=scaffold_attributes.variable_name /}_controllers.RootEntityController, [self.${out value=scaffold_attributes.variable_name /}_plugin, self], {})

    def get_patterns(self):
        return (
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities$", self.root_entity_controller.handle_list_json, "get", "json"),
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities$", self.root_entity_controller.handle_create_json, "post", "json"),
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities/(?P<root_entity_object_id>[0-9]+)$", self.root_entity_controller.handle_show_json, "get", "json"),
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities/(?P<root_entity_object_id>[0-9]+)/update$", self.root_entity_controller.handle_update_json, "post", "json"),
            (r"^${out value=scaffold_attributes.variable_name /}/root_entities/(?P<root_entity_object_id>[0-9]+)/delete$", self.root_entity_controller.handle_delete_json, "post", "json")
        )
