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
