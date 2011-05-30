import colony.libs.importer_util

web_mvc_utils = colony.libs.importer_util.__importer__("web_mvc_utils")

class ${out value=scaffold_attributes.model.class_name /}Controller:
    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin, ${out value=scaffold_attributes.variable_name /}):
        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin
        self.${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.variable_name /}

    def start(self):
        # sets the relative resources path
        self.set_relative_resources_path("${out value=scaffold_attributes.relative_backend_path /}/resources")

        # sets the entity models and the entity manager
        self.entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models
        self.entity_manager = self.entity_models.entity_manager

    def handle_list(self, rest_request, parameters = {}):
        # retrieves the ${out value=scaffold_attributes.model.name_lowercase /} entities
        ${out value=scaffold_attributes.model.variable_name /}_entities = self.entity_manager._find_all(self.entity_models.${out value=scaffold_attributes.model.class_name /})

        # processes the template and sets it as the response
        template_file = self.retrieve_template_file("list.html.tpl")
        self.apply_base_path_template_file(rest_request, template_file)
        template_file.assign("${out value=scaffold_attributes.model.variable_name_plural /}", ${out value=scaffold_attributes.model.variable_name /}_entities)
        self.process_set_contents(rest_request, template_file)

    def handle_show(self, rest_request, parameters = {}):
        # retrieves the specified ${out value=scaffold_attributes.model.name_lowercase /} entity
        ${out value=scaffold_attributes.model.variable_name /}_object_id = int(parameters["pattern_names"]["${out value=scaffold_attributes.model.variable_name /}_object_id"])
        ${out value=scaffold_attributes.model.variable_name /}_entity = self.entity_manager.find(self.entity_models.${out value=scaffold_attributes.model.class_name /}, ${out value=scaffold_attributes.model.variable_name /}_object_id)

        # processes the template and sets it as the response
        template_file = self.retrieve_template_file("show.html.tpl")
        template_file.assign("${out value=scaffold_attributes.model.variable_name /}", ${out value=scaffold_attributes.model.variable_name /}_entity)
        self.process_set_contents(rest_request, template_file)

    def handle_new(self, rest_request, parameters = {}):
        # retrieves the template and sets it as the response
        template_file = self.retrieve_template_file("new.html.tpl")
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def handle_create(self, rest_request, parameters = {}):
        # creates the ${out value=scaffold_attributes.model.name_lowercase /} entity
        form_data_map = self.process_form_data(rest_request, "utf-8")
        ${out value=scaffold_attributes.model.variable_name /} = form_data_map.get("${out value=scaffold_attributes.model.variable_name /}", {})
        ${out value=scaffold_attributes.model.variable_name /}_entity = self.get_entity_model(self.entity_manager, self.entity_models.${out value=scaffold_attributes.model.class_name /}, ${out value=scaffold_attributes.model.variable_name /})
        ${out value=scaffold_attributes.model.variable_name /}_entity.save_update()

        # redirects to the ${out value=scaffold_attributes.model.name_lowercase /} entities page
        self.redirect_base_path(rest_request, "${out value=scaffold_attributes.model.variable_name_plural /}")

    def handle_edit(self, rest_request, parameters = {}):
        # retrieves the specified ${out value=scaffold_attributes.model.name_lowercase /} entity
        ${out value=scaffold_attributes.model.variable_name /}_object_id = int(parameters["pattern_names"]["${out value=scaffold_attributes.model.variable_name /}_object_id"])
        ${out value=scaffold_attributes.model.variable_name /}_entity = self.entity_manager.find(self.entity_models.${out value=scaffold_attributes.model.class_name /}, ${out value=scaffold_attributes.model.variable_name /}_object_id)

        # processes the template and sets it as the response
        template_file = self.retrieve_template_file("edit.html.tpl")
        template_file.assign("${out value=scaffold_attributes.model.variable_name /}", ${out value=scaffold_attributes.model.variable_name /}_entity)
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def handle_update(self, rest_request, parameters = {}):
        # updates the specified ${out value=scaffold_attributes.model.name_lowercase /} entity
        form_data_map = self.process_form_data(rest_request, "utf-8")
        ${out value=scaffold_attributes.model.variable_name /} = form_data_map.get("${out value=scaffold_attributes.model.variable_name /}", {})
        ${out value=scaffold_attributes.model.variable_name /}["object_id"] = int(parameters["pattern_names"]["${out value=scaffold_attributes.model.variable_name /}_object_id"])
        ${out value=scaffold_attributes.model.variable_name /}_entity = self.get_entity_model(self.entity_manager, self.entity_models.${out value=scaffold_attributes.model.class_name /}, ${out value=scaffold_attributes.model.variable_name /})
        ${out value=scaffold_attributes.model.variable_name /}_entity.save_update()

        # redirects to the ${out value=scaffold_attributes.model.name_plural_lowercase /} entities page
        self.redirect_base_path(rest_request, "${out value=scaffold_attributes.model.variable_name_plural /}")

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def handle_delete(self, rest_request, parameters = {}):
        # removes the specified ${out value=scaffold_attributes.model.name_lowercase /} entity
        ${out value=scaffold_attributes.model.variable_name /}_entity = self.entity_models.${out value=scaffold_attributes.model.class_name /}()
        ${out value=scaffold_attributes.model.variable_name /}_entity.object_id = int(parameters["pattern_names"]["${out value=scaffold_attributes.model.variable_name /}_object_id"])
        ${out value=scaffold_attributes.model.variable_name /}_entity.remove()

        # redirects to the ${out value=scaffold_attributes.model.name_plural_lowercase /} page
        self.redirect_base_path(rest_request, "${out value=scaffold_attributes.model.variable_name_plural /}")
