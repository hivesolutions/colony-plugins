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

import wx
import re
import string
import wx.lib.customtreectrl

import misc_gui.tree_visualizer.tree_visualizer_system

class InternalStructureVisualizerPanel(misc_gui.tree_visualizer.tree_visualizer_system.TreeVisualizerPanel):
    """
    Visualizer tool for the data converter's internal structure.
    """
    
    internal_structure = None
    """ Data converter internal structure """
    
    entity_nodes_map = {}
    """ Dictionary relating an entity with its tree node """

    def __init__(self, parent, parent_plugin):
        """
        Class constructor.
        """
        
        misc_gui.tree_visualizer.tree_visualizer_system.TreeVisualizerPanel.__init__(self, parent, parent_plugin)
        self.entity_node_map = {}
        self.entity_name_node_map = {}

    def set_internal_structure(self, internal_structure):
        """
        Sets the internal structure for the visualizer to display.
        
        @type internal_structure: InternalStructure
        @param internal_structure: Data converter internal structure object.
        """

        self.internal_structure = internal_structure
        self.reset_interface()

    def on_node_expanding(self, evt):
        """
        Event handler for when a node is expanded in the visualizer.
        
        @type evt: Event
        @param evt: Event object.
        """
        
        node = evt._item
        
        # if the expanded node is not the root node
        node_data = self.tree.GetItemPyData(evt._item)
        if node_data:
            
            # delete the node's children
            self.tree.DeleteChildren(node)
            
            # if it is a category node then fill it with the entity instances belonging to that category
            if node_data["category_node"]:
                entity_name = node_data["entity_name"]
                self.expand_entity_category_node(node, entity_name)
            else: # otherwise add nodes for the entity's properties
                entity = node_data["entity"]
                self.expand_entity_node(node, entity)

    def on_hyperlink(self, evt):
        """
        Event handler for when a link is clicked in the visualizer.
        
        @type evt: Event
        @param evt: Event object.
        """
        
        node = evt._item
        node_data = self.tree.GetItemPyData(node)
        entity = node_data["entity"]
        entity_category_node = self.entity_name_node_map[entity._name]
        self.tree.Expand(entity_category_node)
        self.expand_entity_category_node(entity_category_node, entity._name)
        entity_node = self.entity_node_map[entity]
        self.tree.Expand(entity_node)
        self.tree.ToggleItemSelection(entity_node)

    def expand_entity_category_node(self, entity_category_node, entity_name):
        """
        Expands an entity category node.
        
        @param entity_category_node: Tree node where the entity instances will be displayed.
        @type entity_name: String
        @param entity_name: Name of the entity whose category one is expanding.
        """
        
        if self.tree.GetChildrenCount(entity_category_node) == 0:
            entities = getattr(self.internal_structure, entity_name)
            for entity in entities:
                entity_node = self.add_item(entity_category_node, entity_name + "[" + str(entity._id) + "]", 0)
                self.add_item(entity_node, "Loading..." , 0)
                self.tree.SetItemPyData(entity_node, {"category_node" : False, "entity_name" : entity._name, "entity" : entity})
                self.entity_node_map[entity] = entity_node
    
    def expand_entity_node(self, entity_node, entity):
        """
        Expands an entity node.
        
        @param entity_node: Tree node where the entity node's informations will be displayed.
        @type entity: EntityStructure
        @param entity: Entity used to fill the entity tree node with.
        """
        
        if self.tree.GetChildrenCount(entity_node) == 0:
            field_names = self.get_valid_attributes(entity)
            for field_name in field_names:
                field_value = getattr(entity, field_name)
                if not str(type(field_value)) == "<type 'instance'>":
                   if type(field_value) == list:
                       #field_node = self.add_item(entity_node, field_name + " = relation with \"" + str(len(field_value)) + "\" entities", 0)
                       field_node = self.add_item(entity_node, field_name, 0)
                       for child_fild_value in field_value:
                           child_field_node = self.add_item(field_node, child_fild_value._name + " [" + str(child_fild_value._id) + "]", 0)
                           self.tree.SetItemHyperText(child_field_node, True)
                           self.tree.SetItemPyData(child_field_node, {"category_node" : False, "entity_name" : child_fild_value._name, "entity" : child_fild_value})
                   else:
                       field_node = self.add_item(entity_node, field_name + " = \"" + str(field_value) + "\"", 0)
                else:
                   field_node = self.add_item(entity_node, field_value._name + " [" + str(field_value._id) + "]", 0)
                   self.tree.SetItemHyperText(field_node, True)
                   self.tree.SetItemPyData(field_node, {"category_node" : False, "entity_name" : field_value._name, "entity" : field_value})

    def get_valid_attributes(self, object):
        """
        Returns the object attributes that can be displayed in the visualizer.
        
        @type object: Object
        @param object: Object one wants to display in the internal structure visualizer.
        @rtype: List
        @return: List of valid object attributes.
        """
        
        attributes = dir(object)
        for exclusion_element in object.exclusions:
            if exclusion_element in attributes:
                attributes.remove(exclusion_element)
        return attributes

    def refresh_tree(self):
        """
        Refreshes the internal structure visualizer.
        """
        
        self.set_root("Internal structure")
        root_node = self.tree.GetRootItem()
        valid_attributes = self.get_valid_attributes(self.internal_structure)
        for entity_name in valid_attributes:
            category_node = self.add_item(root_node, entity_name, 0)
            self.entity_name_node_map[entity_name] = category_node
            self.add_item(category_node, "Loading..." , 0)
            self.tree.SetItemPyData(category_node, {"category_node" : True, "entity_name" : entity_name, "entity" : None})
        self.tree.Expand(root_node)       
