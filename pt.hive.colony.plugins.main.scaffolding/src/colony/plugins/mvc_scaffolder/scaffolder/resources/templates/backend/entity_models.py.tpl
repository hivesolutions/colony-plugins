#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

import colony.libs.importer_util

BASE_ENTITY_MODULE_VALUE = "base_entity"
""" The base entity module value """

# imports the base entity classes
base_entity = colony.libs.importer_util.__importer__(BASE_ENTITY_MODULE_VALUE)

class RootEntity(base_entity.EntityClass):
    """
    The root entity class, inherited by other entities
    in order for them to have a global unique identifier.
    """

    object_id = {
        "id" : True,
        "data_type" : "integer",
        "generated" : True,
        "generator_type" : "table",
        "table_generator_field_name" : "RootEntity"
    }
    """ The root entity's object id """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.object_id = None

class ${out value=scaffold_attributes.model.class_name /}(RootEntity):
    """
    The ${out value=scaffold_attributes.model.name_lowercase /} entity class.
    """
    ${foreach item=attribute from=scaffold_attributes.model.attributes}
    ${out value=attribute.name /} = {
        "data_type" : "${out value=attribute.data_type /}"
    }
    """ The ${out value=scaffold_attributes.model.name_lowercase /}'s ${out value=attribute.name_lowercase /} """
    ${/foreach}
    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        ${foreach item=attribute from=scaffold_attributes.model.attributes}
        self.${out value=attribute.name /} = None
        ${/foreach}
