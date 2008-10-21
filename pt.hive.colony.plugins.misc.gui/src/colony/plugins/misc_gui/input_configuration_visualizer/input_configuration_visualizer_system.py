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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import wx
import wx.lib

import misc_gui.tree_visualizer.tree_visualizer_system

#@todo: review and comment this class
class InputConfigurationVisualizerPanel(misc_gui.tree_visualizer.tree_visualizer_system.TreeVisualizerPanel):

    input_configuration = None
    table_nodes_map = {}

    def __init__(self, parent, parent_plugin):
        misc_gui.tree_visualizer.tree_visualizer_system.TreeVisualizerPanel.__init__(self, parent, parent_plugin)
        self.table_nodes_map = {}
        self.tree.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_HYPERLINK, self.on_hyperlink)

    def set_input_configuration(self, input_configuration):
        self.input_configuration = input_configuration
        self.reset_interface()

    def on_hyperlink(self, evt):
        tree_item = evt._item
        table_name = self.tree.GetItemPyData(tree_item)
        self.select_table(table_name)

    def select_table(self, table_name):
        self.tree.ToggleItemSelection(self.table_nodes_map[table_name])
        self.tree.Expand(self.table_nodes_map[table_name])

    def add_handlers(self, node, object_with_handlers):
        for handler in object_with_handlers.handler_list:
            self.add_item(node, "handler name = \"%s\"" % handler.name, 0)

    def add_columns(self, node, table):
        for column_name in table.column_map:
            column = table.column_map[column_name]
            column_node = self.add_item(node, "column = \"%s\"" % column_name, 0)
            self.add_item(column_node, "name = \"%s\"" % column.name, 0)
            self.add_item(column_node, "primary_key = \"%s\"" % str(column.primary_key), 0)
            self.add_item(column_node, "internal entity = \"%s\"" % column.internal_entity, 0)
            self.add_item(column_node, "internal entity id = \"%s\"" % column.internal_entity_id, 0)
            self.add_item(column_node, "internal attribute = \"%s\"" % column.internal_attribute, 0)
            if column.referenced_table:
                referenced_table_node = self.add_item(column_node, "referenced table = \"%s\"" % column.referenced_table, 0)
                self.tree.SetItemHyperText(referenced_table_node, True)
                self.tree.SetItemPyData(referenced_table_node, column.referenced_table)
            if len(column.handler_list) > 0:
                handlers_node = self.add_item(column_node, "Handlers", 0)
                self.add_handlers(handlers_node, column)

    def add_tables(self, node):
        for table_name in self.input_configuration.table_map:
            table = self.input_configuration.table_map[table_name]
            table_node = self.add_item(node, table_name, 0)
            self.table_nodes_map[table_name] = table_node
            self.add_item(table_node, "table name = \"%s\"" % table.name, 0)
            self.add_item(table_node, "internal entity = \"%s\"" % table.internal_entity, 0)
            if len(table.column_map) > 0:
                columns_node = self.add_item(table_node, "Columns", 0)
                self.add_columns(columns_node, table)
            if len(table.handler_list) > 0:
                handlers_node = self.add_item(table_node, "Handlers", 0)
                self.add_handlers(handlers_node, table)

    def refresh_tree(self):
        self.set_root("Input Configuration")
        self.node_list = [self.tree.GetRootItem()]
        self.add_tables(self.tree.GetRootItem())
        self.tree.Expand(self.tree.GetRootItem())       
