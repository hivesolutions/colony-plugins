import colony.libs.importer_util

web_mvc_utils = colony.libs.importer_util.__importer__("web_mvc_utils")

class ${out value=scaffold_attributes.model.class_name /}Controller:
    def __init__(self, ${out value=scaffold_attributes.variable_name /}_plugin, ${out value=scaffold_attributes.variable_name /}):
        self.${out value=scaffold_attributes.variable_name /}_plugin = ${out value=scaffold_attributes.variable_name /}_plugin
        self.${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.variable_name /}

    def start(self):
        self.set_relative_resources_path("${out value=scaffold_attributes.relative_backend_path /}/resources")
        self.entity_models = self.${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models
        self.entity_manager = self.entity_models.entity_manager

    def handle_list(self, rest_request, parameters = {}):
        ${out value=scaffold_attributes.model.variable_name /}_entities = self.entity_manager.find_a(self.entity_models.${out value=scaffold_attributes.model.class_name /})
        template_file = self.retrieve_template_file("list.html.tpl")
        self.apply_base_path_template_file(rest_request, template_file)
        template_file.assign("${out value=scaffold_attributes.model.variable_name_plural /}", ${out value=scaffold_attributes.model.variable_name /}_entities)
        self.apply_base_path_template_file(rest_request, template_file)
        self.process_set_contents(rest_request, template_file)

    def handle_show(self, rest_request, parameters = {}):
        ${out value=scaffold_attributes.model.variable_name /}_object_id = int(parameters["pattern_names"]["id"])
        ${out value=scaffold_attributes.model.variable_name /}_entity = self.entity_manager.get(self.entity_models.${out value=scaffold_attributes.model.class_name /}, ${out value=scaffold_attributes.model.variable_name /}_object_id)
        template_file = self.retrieve_template_file("show.html.tpl")
        template_file.assign("${out value=scaffold_attributes.model.variable_name /}", ${out value=scaffold_attributes.model.variable_name /}_entity)
        self.apply_base_path_template_file(rest_request, template_file)
        self.process_set_contents(rest_request, template_file)

    def handle_new(self, rest_request, parameters = {}):
        template_file = self.retrieve_template_file("new.html.tpl")
        self.apply_base_path_template_file(rest_request, template_file)
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def handle_create(self, rest_request, parameters = {}):
        form_data_map = self.process_form_data(rest_request, "utf-8")
        ${out value=scaffold_attributes.model.variable_name /} = form_data_map.get("${out value=scaffold_attributes.model.variable_name /}", {})
        ${out value=scaffold_attributes.model.variable_name /}_entity = self.get_entity_model(self.entity_manager, self.entity_models.${out value=scaffold_attributes.model.class_name /}, ${out value=scaffold_attributes.model.variable_name /})
        ${out value=scaffold_attributes.model.variable_name /}_entity.save_update()
        self.redirect_base_path(rest_request, "${out value=scaffold_attributes.model.variable_name_plural /}")

    def handle_edit(self, rest_request, parameters = {}):
        ${out value=scaffold_attributes.model.variable_name /}_object_id = int(parameters["pattern_names"]["id"])
        ${out value=scaffold_attributes.model.variable_name /}_entity = self.entity_manager.get(self.entity_models.${out value=scaffold_attributes.model.class_name /}, ${out value=scaffold_attributes.model.variable_name /}_object_id)
        template_file = self.retrieve_template_file("edit.html.tpl")
        template_file.assign("${out value=scaffold_attributes.model.variable_name /}", ${out value=scaffold_attributes.model.variable_name /}_entity)
        self.apply_base_path_template_file(rest_request, template_file)
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def handle_update(self, rest_request, parameters = {}):
        form_data_map = self.process_form_data(rest_request, "utf-8")
        ${out value=scaffold_attributes.model.variable_name /} = form_data_map.get("${out value=scaffold_attributes.model.variable_name /}", {})
        ${out value=scaffold_attributes.model.variable_name /}["object_id"] = int(parameters["pattern_names"]["id"])
        ${out value=scaffold_attributes.model.variable_name /}_entity = self.get_entity_model(self.entity_manager, self.entity_models.${out value=scaffold_attributes.model.class_name /}, ${out value=scaffold_attributes.model.variable_name /})
        ${out value=scaffold_attributes.model.variable_name /}_entity.save_update()
        self.redirect_base_path(rest_request, "${out value=scaffold_attributes.model.variable_name_plural /}")

    @web_mvc_utils.transaction_method("${out value=scaffold_attributes.variable_name /}.${out value=scaffold_attributes.variable_name /}_entity_models.entity_manager")
    def handle_delete(self, rest_request, parameters = {}):
        ${out value=scaffold_attributes.model.variable_name /}_entity = self.entity_models.${out value=scaffold_attributes.model.class_name /}()
        ${out value=scaffold_attributes.model.variable_name /}_entity.object_id = int(parameters["pattern_names"]["id"])
        ${out value=scaffold_attributes.model.variable_name /}_entity.remove()
        self.redirect_base_path(rest_request, "${out value=scaffold_attributes.model.variable_name_plural /}")
