# This script intends to detect duplicate object ids, and may be used to compare to different data sources

from omni.tools import *

entity_manager = get_entity_manager(plugin_manager)
entities = get_all_entities(entity_manager)

# should keep the same value
# original: 250409
# fixed: #250409 ok
len(entities)

# get all the existing object_ids (including duplicates)
object_ids = [entity.object_id for entity in entities]

# compare the number of entities with the number of distinct object ids
# should keep
# original: 250409
# fixed: #250409 ok
len(object_ids)

# should match the number of entities (one unique object id for each entity)
# original: 245721
# fixed: #250409 ok
len(set(object_ids))

# RUN ON FIXED
len(entities)
#250435
object_ids = [entity.object_id for entity in entities]
len(object_ids)
#250435
len(set(object_ids))
#250435

# RUN ON REAL
len(entities)
#250435
object_ids = [entity.object_id for entity in entities]
len(object_ids)
#250435
len(set(object_ids))
#245747
