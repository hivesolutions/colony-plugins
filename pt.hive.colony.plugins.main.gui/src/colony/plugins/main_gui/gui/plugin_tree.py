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

__author__ = "João Magalhães <joamag@hive.pt>"
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

ROOT_NAME = "Data Conversion Plugins"
""" The root name """

class PluginTree(wx.TreeCtrl):
    """
    The plugin tree class.
    """

    tab_counter = 0
    """ The tab counter value """

    root = None
    """ The root reference """

    tree_icon_map = {}
    """ The tree icon map """

    def __init__(self, parent, id, pos, size = wx.Size, style = wx.TR_DEFAULT_STYLE | wx.NO_BORDER):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)

        self.tree_icon_map = {}

        self.create_icon_list()

    def start_draw(self):
        self.create_icon_list()

        self.AssignImageList(self.icon_list)

        self.root = self.AddRoot(ROOT_NAME)

        self.SetPyData(self.root, None)
        self.SetItemImage(self.root, self.tree_icon_map["folder"], wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, self.tree_icon_map["folder_open"], wx.TreeItemIcon_Expanded)

        self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dbl_click)

    def create_icon_list(self):
        icon_size = (16, 16)
        self.icon_list = wx.ImageList(icon_size[0], icon_size[1])

        folder_icon_index = self.icon_list.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, icon_size))
        folder_open_icon_index = self.icon_list.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, icon_size))
        file_icon_index = self.icon_list.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, icon_size))

        self.tree_icon_map["folder"] = folder_icon_index
        self.tree_icon_map["folder_open"] = folder_open_icon_index
        self.tree_icon_map["file_icon"] = file_icon_index

    def refresh(self):

        self.Freeze()
        self.DeleteAllItems()
        self.start_draw()

        # refresh gui manager plugins
        for gui_plugin in self.GetParent().gui_plugins:
            item = self.AppendItem(self.root, gui_plugin.short_name, self.tree_icon_map["folder"], data = wx.TreeItemData(gui_plugin.id))
            self.SetItemImage(item, self.tree_icon_map["folder"], wx.TreeItemIcon_Normal)
            self.SetItemImage(item, self.tree_icon_map["folder_open"], wx.TreeItemIcon_Expanded)

            versions = gui_plugin.get_available_gui_versions()

            for version in versions:
                self.AppendItem(item, version, self.tree_icon_map["file_icon"], data = wx.TreeItemData(gui_plugin.id))

        # refresh misc plugins
        for gui_plugin in self.GetParent().gui_panel_plugins:
            self.AppendItem(self.root, gui_plugin.short_name, self.tree_icon_map["file_icon"], data = wx.TreeItemData(gui_plugin.id))

        self.Thaw()
        self.ExpandAll()
        self.Refresh()

    def on_left_dbl_click(self, event):
        #@todo make some refactor if possible in the parent of all
        # event the parent may have a menu where we can close all tabs
        # remove the counter for imageId
        parent = self.GetParent()
        tab_container_panel = parent.tab_container_panel
        book = tab_container_panel.book
        plugins = parent.gui_plugins
        gui_panel_plugins = parent.gui_panel_plugins
        position = event.GetPosition()
        item, flags = self.HitTest(position)
        if item:
            for plugin in plugins:
                if plugin.id == self.GetItemData(item).GetData():
                    tab_container_panel.Freeze()
                    version = self.GetItemText(item)
                    tab_name = plugin.short_name + " " + str(self.tab_counter)
                    panel = plugin.do_panel(book, version, tab_name)
                    book.AddPage(panel, plugin.short_name, imageId = 0)
                    tab_container_panel.Thaw()
                    self.tab_counter += 1
            for plugin in gui_panel_plugins:
                if plugin.id == self.GetItemData(item).GetData():
                    tab_container_panel.Freeze()
                    panel = plugin.do_panel(book)
                    book.AddPage(panel, plugin.short_name, imageId = 0)
                    tab_container_panel.Thaw()
                    self.tab_counter += 1
