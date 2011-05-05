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
import re
import wx.lib.customtreectrl

class TreeVisualizerPanel(wx.Panel):
    """
    The tree visualizer panel class.
    """

    parent_plugin = None
    """ The parent plugin """

    filter_mode = False
    regex_mode = False
    node_list = []
    match_list = []
    non_match_list = []
    parent_match_list = []
    delete_list = []

    def __init__(self, parent, parent_plugin):
        """
        Constructor of the class.

        @type parent: Object
        @param parent: The parent component.
        @type parent_plugin: Plugin
        @param parent_plugin: The parent plugin.
        """

        self.parent_plugin = parent_plugin
        self.node_list = []
        self.match_list = []
        self.non_match_list = []
        self.parent_match_list = []
        self.delete_list = []

        wx.Panel.__init__(self, parent, -1, style = wx.WANTS_CHARS)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_EXPANDING, self.on_node_expanding)
        self.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_HYPERLINK, self.on_hyperlink)

        # build tree panel
        self.tree = wx.lib.customtreectrl.CustomTreeCtrl(self, wx.ID_ANY, style = wx.BORDER_DEFAULT | wx.lib.customtreectrl.TR_HAS_BUTTONS | wx.lib.customtreectrl.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.tree.EnableSelectionVista(True)
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldridx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
        self.fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, isz))
        self.fileidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.tree.SetImageList(il)
        self.il = il
        self.set_root("Nothing to display...")

        # build search box
        self.search = wx.SearchCtrl(self, wx.ID_ANY, style = wx.TE_PROCESS_ENTER, size = (250, -1))
        self.search.ShowSearchButton(True)
        self.search.ShowCancelButton(True)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.on_cancel, self.search)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_search, self.search)

        # build tree options
        self.radio_search = wx.RadioButton(self, wx.ID_ANY, "Search", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_search_mode_change, self.radio_search)
        self.radio_filter = wx.RadioButton(self, wx.ID_ANY, "Filter", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_search_mode_change, self.radio_filter)
        self.radio_search.SetValue(True)
        self.chk_regex = wx.CheckBox(self, wx.ID_ANY, "Regex", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_CHECKBOX, self.on_regex_mode_change, self.chk_regex)
        self.chk_regex.SetValue(False)
        self.btn_expand_all = wx.Button(self, wx.ID_ANY, "Expand all", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.on_expand_all_click, self.btn_expand_all)
        self.btn_collapse_all = wx.Button(self, wx.ID_ANY, "Collapse all", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.on_collapse_all_click, self.btn_collapse_all)

        # layout components
        grid_sizer = wx.FlexGridSizer(0, 1, 0, 0)
        grid_sizer.AddGrowableCol(0)
        grid_sizer.AddGrowableRow(1)
        top_sizer = wx.FlexGridSizer(0, 2, 0, 0)
        top_sizer.AddGrowableCol(1)
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer.Add(self.search, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 5)
        search_sizer.Add(self.chk_regex, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 5)
        search_sizer.Add(self.radio_search, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 5)
        search_sizer.Add(self.radio_filter, 0, wx.GROW | wx.ALIGN_LEFT | wx.ALL, 5)
        tree_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tree_sizer.Add(self.btn_expand_all, 0, wx.GROW | wx.ALIGN_RIGHT | wx.ALL, 5)
        tree_sizer.Add(self.btn_collapse_all, 0, wx.GROW | wx.ALIGN_RIGHT | wx.ALL, 5)
        top_sizer.Add(search_sizer, 0, wx.GROW | wx.ALIGN_CENTER | wx.ALL, 5)
        top_sizer.Add(tree_sizer, 0, wx.GROW | wx.ALIGN_CENTER | wx.ALL, 5)
        grid_sizer.Add(top_sizer, 0, wx.GROW | wx.ALIGN_CENTER | wx.ALL, 5)
        grid_sizer.Add(self.tree, 0, wx.GROW | wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(grid_sizer)
        self.Layout()

    def on_hyperlink(self, evt):
        pass

    def on_node_expanding(self, evt):
        pass

    def on_expand_all_click(self, evt):
        self.Freeze()
        self.tree.ExpandAll()
        self.Thaw()

    def on_collapse_all_click(self, evt):
        for node in self.node_list:
            self.tree.Collapse(node)

    def on_regex_mode_change(self, evt):
        if self.chk_regex.GetValue():
            self.regex_mode = True
        else:
            self.regex_mode = False

    def on_search_mode_change(self, evt):
        if self.radio_search.GetValue():
            self.filter_mode = False
        elif self.radio_filter.GetValue():
            self.filter_mode = True

    def on_size(self, evt):
        self.Layout()

    def on_checked(self, evt):
        item = evt.GetItem()
        (plugin_id, plugin_version) = self.tree.GetItemPyData(item)
        if item._checked:
            self.parent_plugin.manager.load_plugin(plugin_id)
        else:
            self.parent_plugin.manager.unload_plugin(plugin_id)
        self.check_plugin_nodes()

    def on_cancel(self, evt):
        self.search.SetValue("")
        self.reset_interface()

    def on_search(self, evt):
        self.do_search(evt.GetString())

    def do_search(self, search_string):
        self.match_list = []
        self.non_match_list = []
        self.parent_match_list = []
        self.delete_list = []
        self.reset_interface()
        self.Freeze()
        if self.regex_mode:
            self.find_all_matches(search_string)
        else:
            self.find_all_matches("[\\w|\\W]*" + escape_string(search_string.lower()) + "[\\w|\\W]*")
        if self.filter_mode:
            self.delete_nodes(self.delete_list)
        self.bold_nodes(self.match_list)
        self.expand_nodes(self.parent_match_list)
        if len(self.match_list) > 0:
            self.tree.ToggleItemSelection(self.match_list[0])
        self.Thaw()

    def reset_interface(self):
        self.Freeze()
        self.refresh_tree()
        self.tree.Expand(self.tree.GetRootItem())
        self.Thaw()

    def find_all_matches(self, search_string):
        regex = re.compile(search_string)
        # fill match_list, non_match_list and parent_match_list
        self.find_all_matches_aux(self.tree.GetRootItem(), regex)
        # complete filling of parent nodes by tracing back from the ones in the parent_match_list to the root
        for parent_node in self.parent_match_list:
            node = parent_node
            while not node == self.tree.GetRootItem():
                if not node in self.parent_match_list:
                    self.parent_match_list.append(node)
                node = self.tree.GetItemParent(node)
        self.delete_list = [item for item in self.non_match_list if item not in self.parent_match_list]
        for delete_node in self.delete_list:
            if self.tree.GetItemParent(delete_node) in self.delete_list:
                self.delete_list.remove(delete_node)

    def find_all_matches_aux(self, node, regex):
        if node:
            if self.tree.ItemHasChildren(node):
                self.find_all_matches_aux(self.tree.GetFirstChild(node)[0], regex)
            self.find_all_matches_aux(self.tree.GetNextSibling(node), regex)
            item_text = self.tree.GetItemText(node)
            if not self.regex_mode:
                item_text = item_text.lower()
            if regex.match(item_text):
                self.match_list.append(node)
                parent_node = self.tree.GetItemParent(node)
                if not parent_node in self.parent_match_list:
                    self.parent_match_list.append(parent_node)
            else:
                self.non_match_list.append(node)

    def delete_nodes(self, node_list):
        for node in node_list:
            self.tree.Delete(node)

    def expand_nodes(self, node_list):
        for node in node_list:
            self.tree.Expand(node)

    def bold_nodes(self, node_list):
        for node in node_list:
            self.tree.SetItemBold(node, True)

    def add_item(self, parent_node, child_name, item_type):
        child_node = self.tree.AppendItem(parent_node, child_name, ct_type = item_type)
        self.node_list.append(child_node)
        self.tree.SetItemImage(parent_node, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(parent_node, self.fldropenidx, wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(parent_node, self.fldropenidx, wx.TreeItemIcon_Selected)
        self.tree.SetItemImage(child_node, self.fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(child_node, self.fileidx, wx.TreeItemIcon_Selected)
        return child_node

    def set_root(self, root_name):
        if self.tree.GetRootItem():
            self.tree.Delete(self.tree.GetRootItem())
        self.tree.AddRoot(root_name)
        self.tree.SetItemImage(self.tree.GetRootItem(), self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.tree.GetRootItem(), self.fldropenidx, wx.TreeItemIcon_Expanded)

    def refresh_tree(self):
        pass

def escape_string(raw_string):
    new_string = ""

    special_characters = [
        ".", "^", "$", "*", "+", "?", "{", "[", "]", "\\", "|", "(", ")"
    ]

    for character in raw_string:
        if character in special_characters:
            new_string += "\\"
        new_string += character
    return new_string
