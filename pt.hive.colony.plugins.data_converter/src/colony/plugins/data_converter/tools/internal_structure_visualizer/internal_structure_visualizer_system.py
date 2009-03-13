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

#@todo: review and comment this class
class InternalStructureVisualizerPanel(misc_gui.tree_visualizer.tree_visualizer_system.TreeVisualizerPanel):

    internal_structure = None
    entity_nodes_map = {}

    def __init__(self, parent, parent_plugin):
        misc_gui.tree_visualizer.tree_visualizer_system.TreeVisualizerPanel.__init__(self, parent, parent_plugin)
        self.entity_nodes_map = {}
        self.tree.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_HYPERLINK, self.on_hyperlink)

    def set_internal_structure(self, internal_structure):
        self.internal_structure = internal_structure
        self.reset_interface()

    def on_hyperlink(self, evt):
        tree_item = evt._item
        entity = self.tree.GetItemPyData(evt._item)
        self.select_entity(entity)

    def select_entity(self, entity):
        self.tree.ToggleItemSelection(self.entity_nodes_map[entity])
        self.tree.Expand(self.entity_nodes_map[entity])

    def add_entity(self, node, entity):
        field_names = self.get_valid_attributes(entity)
        for field_name in field_names:
            value = getattr(entity, field_name)
            if not str(type(value)) == "<type 'instance'>":
                field_node = self.add_item(node, field_name + " = \"" + str(value) + "\"", 0)
            else:
                field_node = self.add_item(node, field_name, 0)
                #self.add_entity(field_item, value)
                self.tree.SetItemHyperText(field_node, True)
            self.tree.SetItemPyData(field_node, value)

    def add_entities(self, node, entity_names):
        list_node = self.add_item(node, entity_names, 0)
        entitys = getattr(self.internal_structure, entity_names)
        x = 0
        for entity in entitys:
            entity_node = self.add_item(list_node, entity_names + "[" + str(x) + "]", 0)
            self.entity_nodes_map[entity] = entity_node
            self.add_entity(entity_node, entity)
            x += 1

    def get_valid_attributes(self, object):
        attributes = dir(object)
        for exclusion_element in object.exclusions:
            if exclusion_element in attributes:
                attributes.remove(exclusion_element)
        return attributes

    def refresh_tree(self):
        self.set_root("Internal structure")
        self.nodes = [self.tree.GetRootItem()]
        valid_attributes = self.get_valid_attributes(self.internal_structure)
        for entity_names in valid_attributes:
            self.add_entities(self.tree.GetRootItem(), entity_names)
        self.tree.Expand(self.tree.GetRootItem())       
