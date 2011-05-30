import colony.libs.importer_util

base_entity = colony.libs.importer_util.__importer__("base_entity")

class RootEntity(base_entity.EntityClass):
    object_id = {
        "id" : True,
        "data_type" : "integer",
        "generated" : True,
        "generator_type" : "table",
        "table_generator_field_name" : "RootEntity"
    }

    def __init__(self):
        self.object_id = None

class ${out value=scaffold_attributes.model.class_name /}(RootEntity):
    ${foreach item=attribute from=scaffold_attributes.model.attributes}
    ${out value=attribute.name /} = {
        "data_type" : "${out value=attribute.data_type /}"
    }
    ${/foreach}
    def __init__(self):
        RootEntity.__init__(self)
        ${foreach item=attribute from=scaffold_attributes.model.attributes}
        self.${out value=attribute.name /} = None
        ${/foreach}
