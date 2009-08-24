#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Omni ERP
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Omni ERP.
#
# Hive Omni ERP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Omni ERP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Omni ERP. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CHILD_TREE_NODE_ENTITY_NAMES_VALUE = "tree_node_entity_names"

ROOT_TREE_NODE_ENTITY_NAME_VALUE = "root_tree_node_entity_name"

TREE_ENTITY_NAME_VALUE = "tree_entity"

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

def post_conversion_handler_create_tree(data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
    tree_entity_name = arguments[TREE_ENTITY_NAME_VALUE]
    root_tree_node_entity_name = arguments[ROOT_TREE_NODE_ENTITY_NAME_VALUE]
    child_tree_node_entity_names = arguments[CHILD_TREE_NODE_ENTITY_NAMES_VALUE]

    # creates the tree and its root node
    tree_entity = output_intermediate_structure.create_entity(tree_entity_name)
    tree_entity.set_attribute("status", OMNI_ACTIVE_ENTITY_STATUS)
    root_tree_node_entity = output_intermediate_structure.create_entity(root_tree_node_entity_name)
    root_tree_node_entity.set_attribute("status", OMNI_ACTIVE_ENTITY_STATUS)
    tree_entity.set_attribute("root_node", root_tree_node_entity)

    # joins all tree nodes that belong to the tree
    tree_node_entities = []
    for child_tree_node_entity_name in child_tree_node_entity_names:
        tree_node_entities.extend(output_intermediate_structure.get_entities_by_name(child_tree_node_entity_name))

    # adds all orfan tree node entities to the tree's root node
    root_node_child_nodes = []
    for tree_node_entity in tree_node_entities:
        if not tree_node_entity.get_attribute("parent_nodes"):
            tree_node_entity.set_attribute("parent_nodes", [root_tree_node_entity])
            root_node_child_nodes.append(tree_node_entity)
    root_tree_node_entity.set_attribute("child_nodes", root_node_child_nodes)

    return output_intermediate_structure
