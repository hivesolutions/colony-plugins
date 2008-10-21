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

__revision__ = "$LastChangedRevision: 2114 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 15:29:05 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import wx
import wx.lib

import misc_gui.tree_visualizer.tree_visualizer_system

#@todo: review and comment this class
class OutputConfigurationVisualizerPanel(misc_gui.tree_visualizer.tree_visualizer_system.TreeVisualizerPanel):

    output_configuration = None
    domain_entity_nodes_map = {}

    def __init__(self, parent, parent_plugin):
        misc_gui.tree_visualizer.tree_visualizer_system.TreeVisualizerPanel.__init__(self, parent, parent_plugin)
        self.domain_entity_nodes_map = {}
        self.tree.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_HYPERLINK, self.on_hyperlink)

    def set_output_configuration(self, output_configuration):
        self.output_configuration = output_configuration
        self.reset_interface()

    def on_hyperlink(self, evt):
        tree_item = evt._item
        domain_entity_name = self.tree.GetItemPyData(tree_item)
        self.select_domain_entity(domain_entity_name)

    def select_domain_entity(self, domain_entity_name):
        self.tree.ToggleItemSelection(self.domain_entity_nodes_map[domain_entity_name])
        self.tree.Expand(self.domain_entity_nodes_map[domain_entity_name])

    def add_handlers(self, node, object_with_handlers):
        for handler in object_with_handlers.handler_list:
            self.add_item(node, "handler name = \"%s\"" % handler.name, 0)

    def add_attributes(self, node, domain_entity):
        for domain_attribute_name in domain_entity.domain_attribute_map:
            attribute = domain_entity.domain_attribute_map[domain_attribute_name]
            attribute_node = self.add_item(node, "attribute = \"%s\"" % domain_attribute_name, 0)
            self.add_item(attribute_node, "name = \"%s\"" % attribute.name, 0)
            self.add_item(attribute_node, "internal attribute = \"%s\"" % str(attribute.internal_attribute), 0)
            self.add_item(attribute_node, "type = \"%s\"" % attribute.type, 0)
            self.add_item(attribute_node, "primary key = \"%s\"" % attribute.primary_key, 0)
            if attribute.referenced_domain_entity:
                referenced_domain_entity_node = self.add_item(attribute_node, "referenced domain entity = \"%s\"" % attribute.referenced_domain_entity.name, 0)
                referenced_domain_entity_name_node = self.add_item(referenced_domain_entity_node, "domain entity name = \"%s\"" % attribute.referenced_domain_entity.name, 0)
                self.tree.SetItemHyperText(referenced_domain_entity_name_node, True)
                self.tree.SetItemPyData(referenced_domain_entity_name_node, attribute.referenced_domain_entity.name)
                self.add_item(referenced_domain_entity_node, "multiplicity = \"%s\"" % attribute.referenced_domain_entity.multiplicity, 0)
            if len(attribute.handler_list) > 0:
                handlers_node = self.add_item(attribute_node, "Handlers", 0)
                self.add_handlers(handlers_node, attribute)

    def add_domain_entities(self, node):
        for domain_entity_name in self.output_configuration.domain_entity_map:
            domain_entity = self.output_configuration.domain_entity_map[domain_entity_name]
            domain_entity_node = self.add_item(node, domain_entity_name, 0)
            self.domain_entity_nodes_map[domain_entity_name] = domain_entity_node
            self.add_item(domain_entity_node, "domain entity = \"%s\"" % domain_entity.name, 0)
            self.add_item(domain_entity_node, "internal entity = \"%s\"" % domain_entity.internal_entity, 0)
            self.add_item(domain_entity_node, "parent domain entity = \"%s\"" % domain_entity.parent, 0)
            self.add_item(domain_entity_node, "children = \"%s\"" % domain_entity.children, 0)
            if len(domain_entity.domain_attribute_map) > 0:
                attributes_node = self.add_item(domain_entity_node, "Attributes", 0)
                self.add_attributes(attributes_node, domain_entity)
            if len(domain_entity.handler_list) > 0:
                handlers_node = self.add_item(domain_entity_node, "Handlers", 0)
                self.add_handlers(handlers_node, domain_entity)

    def refresh_tree(self):
        self.set_root("Output Configuration")
        self.node_list = [self.tree.GetRootItem()]
        self.add_domain_entities(self.tree.GetRootItem())
        self.tree.Expand(self.tree.GetRootItem())       
