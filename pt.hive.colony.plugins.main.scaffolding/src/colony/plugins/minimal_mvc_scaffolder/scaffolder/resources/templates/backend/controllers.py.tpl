import colony.libs.importer_util

web_mvc_utils = colony.libs.importer_util.__importer__("web_mvc_utils")

class RootEntityController:
    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin, ${out value=scaffold_attributes.variable_name /}):
        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin
        self.${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.variable_name /}

    def start(self):
        # sets the templates path
        plugin_manager = self.${out value=scaffold_attributes.variable_name /}_plugin.manager
        ${out value=scaffold_attributes.variable_name /}_plugin_path = plugin_manager.get_plugin_path_by_id(self.${out value=scaffold_attributes.variable_name /}_plugin.id)
        templates_path = ${out value=scaffold_attributes.variable_name /}_plugin_path + "/${out value=scaffold_attributes.relative_backend_path /}/resources/templates"
        self.set_templates_path(templates_path)

        # sets the entity models and the entity manager
        self.entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models
        self.entity_manager = self.entity_models.entity_manager

    def handle_index(self, rest_request, parameters = {}):
        # processes the index template and sets it as the response
        template_file = self.retrieve_template_file("index.html.tpl")
        root_entities = self.entity_manager._find_all_options(self.entity_models.RootEntity, {})
        template_file.assign("root_entities", root_entities)
        self.process_set_contents(rest_request, template_file)

        # returns true indicating that the response was valid
        return True

    def handle_list_json(self, rest_request, parameters = {}):
        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, "utf-8")
        filter = form_data_map.get("filter", {})
        root_entities = self.entity_manager._find_all_options(self.entity_models.RootEntity, filter)

        # sets the root entity as the response
        serialized_root_entities = self.${out value=scaffold_attributes.variable_name /}_plugin.json_plugin.dumps(root_entities)
        self.set_contents(rest_request, serialized_root_entities)

        # returns true indicating that the response was valid
        return True

    def handle_show_json(self, rest_request, parameters = {}):
        # retrieves the root entity
        root_entity_object_id = int(parameters["pattern_names"]["root_entity_object_id"])
        root_entity = self.entity_manager.find(self.entity_models.RootEntity, root_entity_object_id)

        # sets the root entity as the response
        serialized_root_entity = self.${out value=scaffold_attributes.variable_name /}_plugin.json_plugin.dumps(root_entity)
        self.set_contents(rest_request, serialized_root_entity)

        # returns true to indicate that the handler was successful
        return True

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def handle_create_json(self, rest_request, parameters = {}):
        # creates the root entity
        form_data_map = self.process_form_data(rest_request, "utf-8")
        root_entity = form_data_map.get("root_entity", {})
        root_entity = self.get_entity_model(self.entity_manager, self.entity_models.RootEntity, root_entity)
        root_entity.save_update()

        # sets the root entity as the response
        serialized_root_entity = self.${out value=scaffold_attributes.variable_name /}_plugin.json_plugin.dumps(root_entity)
        self.set_contents(rest_request, serialized_root_entity)

        # returns true to indicate that the handler was successful
        return True

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def handle_update_json(self, rest_request, parameters = {}):
        # updates the root entity
        form_data_map = self.process_form_data(rest_request, "utf-8")
        root_entity = form_data_map.get("root_entity", {})
        root_entity["object_id"] = int(parameters["pattern_names"]["root_entity_object_id"])
        root_entity = self.get_entity_model(self.entity_manager, self.entity_models.RootEntity, root_entity)
        root_entity.save_update()

        # sets the root entity as the response
        serialized_root_entity = self.${out value=scaffold_attributes.variable_name /}_plugin.json_plugin.dumps(root_entity)
        self.set_contents(rest_request, serialized_root_entity)

        # returns true to indicate that the handler was successful
        return True

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def handle_delete_json(self, rest_request, parameters = {}):
        # retrieves the root entity object id
        root_entity_object_id = int(parameters["pattern_names"]["root_entity_object_id"])

        # removes the root entity
        root_entity = self.entity_models.RootEntity()
        root_entity.object_id = root_entity_object_id
        root_entity.remove()

        # returns true to indicate that the handler was successful
        return True
