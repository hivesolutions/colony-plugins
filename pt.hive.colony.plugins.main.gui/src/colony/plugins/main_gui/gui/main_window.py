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

import wx.aui
import wx._core
import wx.lib.wordwrap

import plugin_tree
import tab_container_panel

import colony.base.plugin_system
import colony.base.util

ID_CreateGrid = wx.NewId()
ID_CreatePerspective = wx.NewId()
ID_CopyPerspective = wx.NewId()

ID_TransparentHint = wx.NewId()
ID_VenetianBlindsHint = wx.NewId()
ID_RectangleHint = wx.NewId()
ID_NoHint = wx.NewId()
ID_HintFade = wx.NewId()
ID_AllowFloating = wx.NewId()
ID_NoVenetianFade = wx.NewId()
ID_TransparentDrag = wx.NewId()
ID_AllowActivePane = wx.NewId()
ID_NoGradient = wx.NewId()
ID_VerticalGradient = wx.NewId()
ID_HorizontalGradient = wx.NewId()

ID_Settings = wx.NewId()
ID_About = wx.NewId()
ID_FirstPerspective = ID_CreatePerspective + 1000

BASE_PATH = "/main_gui"
GUI_PATH = BASE_PATH + "/" + "gui"
GUI_RESOURCES_PATH = GUI_PATH + "/" + "resources"
ICONS_PATH = GUI_RESOURCES_PATH + "/" + "icons"
IMAGES_PATH = GUI_RESOURCES_PATH + "/" + "images"
ICONS_10X10_PATH = ICONS_PATH + "/" + "10x10"
ICONS_16X16_PATH = ICONS_PATH + "/" + "16x16"
ICONS_32X32_PATH = ICONS_PATH + "/" + "32x32"

SPLASH_IMAGE_FILE_NAME = "colony_splash.png"
""" The splash image file name """

MENU_TITLE = "Colony Framework Manager"
TREE_PANEL_TITLE = "Tree Pane"
LOG_PANEL_TITLE = "Log Pane"
H_SIZE = 1024
V_SIZE = 768

class MainFrame(wx.Frame):
    """
    The main frame used in the gui.
    """

    plugin_tree = None
    """ The main plugin tree used """

    tab_container_panel = None
    """ The tab container panel """

    text_control = None
    """ The text control """

    progress_information_frame = None
    """ The progress information frame """

    bitmaps_10x10_map = {}
    """ The bitmaps map for 10x10 bitmaps """

    bitmaps_16x16_map = {}
    """ The bitmaps map for 16x16 bitmaps """

    bitmaps_32x32_map = {}
    """ The bitmaps map for 32x32 bitmaps """

    icons_10x10_map = {}
    """ The icons map for 10x10 icons """

    icons_16x16_map = {}
    """ The icons map for 16x16 icons """

    icons_32x32_map = {}
    """ The icons map for 32x32 icons """

    main_gui_plugin = None
    """ the main gui plugin """

    gui_plugins = []
    """ The list of gui plugins loaded """

    gui_panel_plugins = []
    """ The list of gui panel plugins loaded """

    progress_information_plugin = None
    """ The progress information plugin """

    event_queue = []
    """ The queue of events to be processed """

    def __init__(self, main_gui_plugin, parent, id = wx.ID_ANY, title = MENU_TITLE, position = wx.DefaultPosition,
                 size = wx.Size(H_SIZE, V_SIZE), style = wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER | wx.CLIP_CHILDREN):

        wx.Frame.__init__(self, parent, id, title, position, size, style)

        self.main_gui_plugin = main_gui_plugin

        # starts the plugin loading process
        self.gui_plugins = []
        self.gui_panel_plugins = []
        self.plugin_path = self.main_gui_plugin.manager.get_plugin_path_by_id(self.main_gui_plugin.id)

        # loads the icons using the bitmap loader plugin
        self.main_gui_plugin.bitmap_loader_plugin.load_icons(self.plugin_path + ICONS_10X10_PATH, self.bitmaps_10x10_map, self.icons_10x10_map)
        self.main_gui_plugin.bitmap_loader_plugin.load_icons(self.plugin_path + ICONS_16X16_PATH, self.bitmaps_16x16_map, self.icons_16x16_map)
        self.main_gui_plugin.bitmap_loader_plugin.load_icons(self.plugin_path + ICONS_32X32_PATH, self.bitmaps_32x32_map, self.icons_32x32_map)

        # tell FrameManager to manage this frame
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        # start the event queue
        self.event_queue = []

        self._perspectives = []
        self.n = 0
        self.x = 0

        self.SetIcon(self.icons_16x16_map["omni"])

        # create menu
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, "Exit")

        view_menu = wx.Menu()
        options_menu = wx.Menu()
        options_menu.AppendRadioItem(ID_TransparentHint, "Transparent Hint")
        options_menu.AppendRadioItem(ID_VenetianBlindsHint, "Venetian Blinds Hint")
        options_menu.AppendRadioItem(ID_RectangleHint, "Rectangle Hint")
        options_menu.AppendRadioItem(ID_NoHint, "No Hint")
        options_menu.AppendSeparator()
        options_menu.AppendCheckItem(ID_HintFade, "Hint Fade-in")
        options_menu.AppendCheckItem(ID_AllowFloating, "Allow Floating")
        options_menu.AppendCheckItem(ID_NoVenetianFade, "Disable Venetian Blinds Hint Fade-in")
        options_menu.AppendCheckItem(ID_TransparentDrag, "Transparent Drag")
        options_menu.AppendCheckItem(ID_AllowActivePane, "Allow Active Pane")
        options_menu.AppendSeparator()
        options_menu.AppendRadioItem(ID_NoGradient, "No Caption Gradient")
        options_menu.AppendRadioItem(ID_VerticalGradient, "Vertical Caption Gradient")
        options_menu.AppendRadioItem(ID_HorizontalGradient, "Horizontal Caption Gradient")
        options_menu.AppendSeparator()
        options_menu.Append(ID_Settings, "Settings Pane")

        self._perspectives_menu = wx.Menu()
        self._perspectives_menu.Append(ID_CreatePerspective, "Create Perspective")
        self._perspectives_menu.Append(ID_CopyPerspective, "Copy Perspective Data To Clipboard")
        self._perspectives_menu.AppendSeparator()
        self._perspectives_menu.Append(ID_FirstPerspective + 0, "Default Startup")
        self._perspectives_menu.Append(ID_FirstPerspective + 1, "All Panes")
        self._perspectives_menu.Append(ID_FirstPerspective + 2, "Vertical Toolbar")

        help_menu = wx.Menu()
        help_menu.Append(ID_About, "About...")

        mb.Append(file_menu, "File")
        mb.Append(view_menu, "View")
        mb.Append(self._perspectives_menu, "Perspectives")
        mb.Append(options_menu, "Options")
        mb.Append(help_menu, "Help")

        self.SetMenuBar(mb)

        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Ready", 0)
        self.statusbar.SetStatusText(MENU_TITLE, 1)

        # min size for the frame itself isnt completely done.
        # see the end up FrameManager::Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))

        # create a tool bar
        tool_bar = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tool_bar.SetToolBitmapSize(wx.Size(16, 16))
        tool_bar.AddLabelTool(ID_CreateGrid, "New", self.bitmaps_16x16_map["doc"])
        tool_bar.AddLabelTool(ID_CreateGrid, "Save", self.bitmaps_16x16_map["disk"])
        tool_bar.AddSeparator()
        tool_bar.AddLabelTool(ID_CreateGrid, "Play", self.bitmaps_16x16_map["play"])
        tool_bar.AddLabelTool(ID_CreateGrid, "Pause", self.bitmaps_16x16_map["pause"])
        tool_bar.AddLabelTool(ID_CreateGrid, "Record", self.bitmaps_16x16_map["record"])
        tool_bar.AddLabelTool(ID_CreateGrid, "Statistics", self.bitmaps_16x16_map["chart_bar"])

        tool_bar.Realize()

        # create some normal panels
        self._mgr.AddPane(self.create_plugin_tree(), wx.aui.AuiPaneInfo().
                          Name("tree_content").Caption(TREE_PANEL_TITLE).
                          BestSize(wx.Size(250, 100)).MinSize(wx.Size(200, 100)).
                          Left().Layer(1).Position(1).CloseButton(False).MaximizeButton(False))

        self._mgr.AddPane(self.create_text_control(), wx.aui.AuiPaneInfo().
                          Name("log_content").Caption(LOG_PANEL_TITLE).
                          Bottom().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))

        # create the tab container panel
        self._mgr.AddPane(self.create_tab_container_panel(), wx.aui.AuiPaneInfo().Name("tab_container_content").
                          CenterPane())

        # add the toolbars to the manager
        self._mgr.AddPane(tool_bar, wx.aui.AuiPaneInfo().
                          Name("tool_bar").Caption("Toolbar").
                          ToolbarPane().Top().Row(1).
                          LeftDockable(False).RightDockable(False))

        # make some default perspectives
        perspective_all = self._mgr.SavePerspective()

        # retrieves all the current panes
        all_panes = self._mgr.GetAllPanes()

        # creates vertical perspective
        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()

        self._mgr.GetPane("tree_content").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("log_content").Show().Left().Layer(0).Row(0).Position(1)
        self._mgr.GetPane("tab_container_content").Show()

        # saves perspective
        perspective_vert = self._mgr.SavePerspective()

        # creates default perspective
        for ii in xrange(len(all_panes)):
            if not all_panes[ii].IsToolbar():
                all_panes[ii].Hide()

        self._mgr.GetPane("tree_content").Show().Left().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("log_content").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("tab_container_content").Show()

        # saves perspective
        perspective_default = self._mgr.SavePerspective()

        # saves perspectives in the same order as in the menu bar
        self._perspectives.append(perspective_default)
        self._perspectives.append(perspective_all)
        self._perspectives.append(perspective_vert)

        # "commit" all changes made to FrameManager
        self._mgr.Update()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.on_pane_close)

        self.Bind(wx.EVT_MENU, self.on_create_perspective, id=ID_CreatePerspective)
        self.Bind(wx.EVT_MENU, self.on_copy_perspective, id=ID_CopyPerspective)

        self.Bind(wx.EVT_MENU, self.on_manager_flag, id=ID_AllowFloating)
        self.Bind(wx.EVT_MENU, self.on_manager_flag, id=ID_TransparentHint)
        self.Bind(wx.EVT_MENU, self.on_manager_flag, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_MENU, self.on_manager_flag, id=ID_RectangleHint)
        self.Bind(wx.EVT_MENU, self.on_manager_flag, id=ID_NoHint)
        self.Bind(wx.EVT_MENU, self.on_manager_flag, id=ID_HintFade)
        self.Bind(wx.EVT_MENU, self.on_manager_flag, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_MENU, self.on_manager_flag, id=ID_TransparentDrag)
        self.Bind(wx.EVT_MENU, self.on_manager_flag, id=ID_AllowActivePane)

        self.Bind(wx.EVT_MENU, self.on_gradient, id=ID_NoGradient)
        self.Bind(wx.EVT_MENU, self.on_gradient, id=ID_VerticalGradient)
        self.Bind(wx.EVT_MENU, self.on_gradient, id=ID_HorizontalGradient)
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_about, id=ID_About)

        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_TransparentHint)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_RectangleHint)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_NoHint)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_HintFade)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_AllowFloating)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_TransparentDrag)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_AllowActivePane)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_NoGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_VerticalGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_ui, id=ID_HorizontalGradient)

        self.Bind(wx.EVT_MENU_RANGE, self.on_restore_perspective, id=ID_FirstPerspective,
                  id2=ID_FirstPerspective + 1000)

        self.Bind(wx.EVT_IDLE, self.on_idle)

        self.Refresh()

    def process_gui_progress_information_changed_event(self, event_name, event_args):
        if colony.base.plugin_system.is_event_or_sub_event("gui_progress_information_changed.show_panel", event_name):
            self.show_progress_information_frame()
        elif colony.base.plugin_system.is_event_or_sub_event("gui_progress_information_changed.hide_panel", event_name):
            self.hide_progress_information_frame()

    def on_idle(self, event):
        while len(self.event_queue):
            event = self.event_queue.pop(0)
            if event.event_name == "exit":
                self.Close()
            elif event.event_name == "refresh_panel_tabs":
                self.Freeze()
                book = self.tab_container_panel.book
                for gui_panel_plugin in self.gui_panel_plugins:
                    panel = gui_panel_plugin.do_panel(book)
                    book.AddPage(panel, gui_panel_plugin.short_name, imageId = 0)
                self.Thaw()
            elif event.event_name == "create_progress_information_frame":
                self.progress_information_frame = ProgressInformationFrame(self, wx.ID_ANY, "Progress information", self.progress_information_plugin)
                self.progress_information_frame.do_panel()
            elif event.event_name == "show_progress_information_frame":
                self.progress_information_frame.Show(True)
            elif event.event_name == "hide_progress_information_frame":
                self.progress_information_frame.Show(False)

    def on_pane_close(self, event):
        caption = event.GetPane().caption

        if caption in ["Tree Pane", "Dock Manager Settings", "Fixed Pane"]:
            msg = "Are You Sure You Want To Close This Pane?"
            dlg = wx.MessageDialog(self, msg, "AUI Question",
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

            if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
                event.Veto()
            dlg.Destroy()

    def on_close(self, event):
        self._mgr.UnInit()
        del self._mgr
        self.Destroy()

    def on_exit(self, event):
        self.Close()

    def on_about(self, event):
        info = wx.AboutDialogInfo()

        # about dialog information
        info.Name = MENU_TITLE
        info.Version = "1.0.0"
        info.Copyright = "(C) 2008 Hive Solutions Lda."
        info.Description = wx.lib.wordwrap.wordwrap(
            "Just another framework administrator from Hive Solutions.\n"
            "This one is targeted to everyone.\n",
            350, wx.ClientDC(self))
        info.WebSite = ("http://www.hive.pt", "Hive Solutions Lda. <development@hive.pt>")
        info.Developers = ["Joao Magalhaes <joamag@hive.pt>", "Tiago Silva <tsilva@hive.pt>", "Luís Martinho <lmartinho@hive.pt>"]
        info.License = wx.lib.wordwrap.wordwrap("GNU General Public License (GPL), Version 3", 500, wx.ClientDC(self))
        info.SetIcon(self.icons_32x32_map["omni"])

        # creates the about box with the information
        wx.AboutBox(info)

    def get_dock_art(self):
        return self._mgr.GetArtProvider()

    def do_update(self):
        self._mgr.Update()

    def on_erase_background(self, event):
        event.Skip()

    def on_size(self, event):
        event.Skip()

    def on_gradient(self, event):
        gradient = 0

        if event.GetId() == ID_NoGradient:
            gradient = wx.aui.AUI_GRADIENT_NONE
        elif event.GetId() == ID_VerticalGradient:
            gradient = wx.aui.AUI_GRADIENT_VERTICAL
        elif event.GetId() == ID_HorizontalGradient:
            gradient = wx.aui.AUI_GRADIENT_HORIZONTAL

        self._mgr.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE, gradient)
        self._mgr.Update()

    def on_manager_flag(self, event):

        flag = 0
        eid = event.GetId()

        if eid in [ ID_TransparentHint, ID_VenetianBlindsHint, ID_RectangleHint, ID_NoHint ]:
            flags = self._mgr.GetFlags()
            flags &= ~wx.aui.AUI_MGR_TRANSPARENT_HINT
            flags &= ~wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
            flags &= ~wx.aui.AUI_MGR_RECTANGLE_HINT
            self._mgr.SetFlags(flags)

        if eid == ID_AllowFloating:
            flag = wx.aui.AUI_MGR_ALLOW_FLOATING
        elif eid == ID_TransparentDrag:
            flag = wx.aui.AUI_MGR_TRANSPARENT_DRAG
        elif eid == ID_HintFade:
            flag = wx.aui.AUI_MGR_HINT_FADE
        elif eid == ID_NoVenetianFade:
            flag = wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
        elif eid == ID_AllowActivePane:
            flag = wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE
        elif eid == ID_TransparentHint:
            flag = wx.aui.AUI_MGR_TRANSPARENT_HINT
        elif eid == ID_VenetianBlindsHint:
            flag = wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
        elif eid == ID_RectangleHint:
            flag = wx.aui.AUI_MGR_RECTANGLE_HINT

        self._mgr.SetFlags(self._mgr.GetFlags() ^ flag)


    def on_update_ui(self, event):

        flags = self._mgr.GetFlags()
        eid = event.GetId()

        if eid == ID_NoGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_NONE)

        elif eid == ID_VerticalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_VERTICAL)

        elif eid == ID_HorizontalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_HORIZONTAL)

        elif eid == ID_AllowFloating:
            event.Check((flags & wx.aui.AUI_MGR_ALLOW_FLOATING) != 0)

        elif eid == ID_TransparentDrag:
            event.Check((flags & wx.aui.AUI_MGR_TRANSPARENT_DRAG) != 0)

        elif eid == ID_TransparentHint:
            event.Check((flags & wx.aui.AUI_MGR_TRANSPARENT_HINT) != 0)

        elif eid == ID_VenetianBlindsHint:
            event.Check((flags & wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT) != 0)

        elif eid == ID_RectangleHint:
            event.Check((flags & wx.aui.AUI_MGR_RECTANGLE_HINT) != 0)

        elif eid == ID_NoHint:
            event.Check(((wx.aui.AUI_MGR_TRANSPARENT_HINT |
                          wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT |
                          wx.aui.AUI_MGR_RECTANGLE_HINT) & flags) == 0)

        elif eid == ID_HintFade:
            event.Check((flags & wx.aui.AUI_MGR_HINT_FADE) != 0)

        elif eid == ID_NoVenetianFade:
            event.Check((flags & wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE) != 0)

    def on_create_perspective(self, event):
        dlg = wx.TextEntryDialog(self, "Enter a name for the new perspective:", "AUI Test")

        dlg.SetValue(("Perspective %d")%(len(self._perspectives)+1))
        if dlg.ShowModal() != wx.ID_OK:
            return

        if len(self._perspectives) == 0:
            self._perspectives_menu.AppendSeparator()

        self._perspectives_menu.Append(ID_FirstPerspective + len(self._perspectives), dlg.GetValue())
        self._perspectives.append(self._mgr.SavePerspective())

    def on_copy_perspective(self, event):
        s = self._mgr.SavePerspective()

        if wx.TheClipboard.Open():

            wx.TheClipboard.SetData(wx.TextDataObject(s))
            wx.TheClipboard.Close()

    def on_restore_perspective(self, event):
        self._mgr.LoadPerspective(self._perspectives[event.GetId() - ID_FirstPerspective])

    def get_start_position(self):
        self.x = self.x + 20
        x = self.x
        pt = self.ClientToScreen(wx.Point(0, 0))

        return wx.Point(pt.x + x, pt.y + x)

    def create_text_control(self):
        self.text_control = wx.TextCtrl(self, wx.ID_ANY, "", wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE)

        # @todo fazer refactor deste codigo
        logger = self.main_gui_plugin.manager.get_plugin_by_id("pt.hive.colony.plugins.main.log")
        logger_log = logger.get_logger("main")
        composite_handler = logger.get_composite_handler()
        composite_handler.set_handler_def(self.add_text_to_text_control)
        logger_log.set_handler(composite_handler)

        return self.text_control

    def add_text_to_text_control(self, text):
        self.text_control.AppendText(text)

    def refresh_tree(self):
        # @todo fazer refactor deste codigo
        logger = self.main_gui_plugin.manager.get_plugin_by_id("pt.hive.colony.plugins.main.log")
        logger_log = logger.get_logger("main")
        #  @todo this is a fix for mac osx change it to work in all os
        #logger_log.get_logger().warn("refreshing tree\n")
        self.plugin_tree.refresh()

    def refresh_panel_tabs(self):
        event = colony.base.util.Event("refresh_panel_tabs")
        self.event_queue.append(event)
        self.Refresh()

    def create_progress_information_frame(self):
        event = colony.base.util.Event("create_progress_information_frame")
        self.event_queue.append(event)
        self.Refresh()

    def show_progress_information_frame(self):
        # in case the progress information frame is already shown
        if self.progress_information_frame.IsShown():
            return

        event = colony.base.util.Event("show_progress_information_frame")
        self.event_queue.append(event)
        self.Refresh()

    def hide_progress_information_frame(self):
        # in case the progress information frame is already hidden
        if not self.progress_information_frame.IsShown():
            return

        event = colony.base.util.Event("hide_progress_information_frame")
        self.event_queue.append(event)
        self.Refresh()

    def refresh_progress_information_frame(self):
        pass

    def create_plugin_tree(self):
        self.plugin_tree = plugin_tree.PluginTree(self, wx.ID_ANY,
                                             wx.Point(0, 0), wx.Size(160, 250),
                                             wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        self.plugin_tree.gui_plugins = self.gui_plugins
        self.plugin_tree.start_draw()

        return self.plugin_tree

    def create_tab_container_panel(self):
        self.tab_container_panel = tab_container_panel.TabContainerPanel(self, [self.bitmaps_10x10_map["scroll"], self.bitmaps_10x10_map["tab_aux"]])

        return self.tab_container_panel

class ProgressInformationFrame(wx.Frame):
    """
    The progress information frame class.
    """

    FRAME_STYLE = wx.CAPTION | wx.FRAME_FLOAT_ON_PARENT | wx.RESIZE_BORDER | wx.PD_AUTO_HIDE | wx.PD_APP_MODAL
    """ The frame style """

    MIN_WIDTH = 480
    """ The frame minimum width """

    MIN_HEIGHT = 240
    """ The frame minimum height """

    progress_information_plugin = None
    """ The progress information plugin """

    panel_loaded = False
    """ The panel loaded flag """

    def __init__(self, parent, id, title, progress_information_plugin):
        wx.Frame.__init__(self, parent, id, title, style = ProgressInformationFrame.FRAME_STYLE)

        # sets the minimum size for the window
        self.SetMinSize((ProgressInformationFrame.MIN_WIDTH, ProgressInformationFrame.MIN_HEIGHT))

        self.progress_information_plugin = progress_information_plugin

    def Show(self, value = True, modal = False):
        # in case the show value of the window is already the same
        if self.IsShown() == value:
            return
        self.do_panel()
        if modal:
            self.MakeModal(True)
        if value:
            self.center_on_parent()
        wx.Frame.Show(self, value)

    def do_panel(self, force = False):
        if self.panel_loaded and not force:
            return
        self.progress_information_plugin.do_panel(self)
        self.panel_loaded = True

    def center_on_parent(self):
        parent = self.GetParent()

        parent_point = parent.GetPosition()
        parent_x = parent_point.x
        parent_y = parent_point.y

        parent_size = parent.GetSize()
        parent_width = parent_size.width
        parent_height = parent_size.height

        size = self.GetSize()
        width = size.width
        height = size.height

        center_x = parent_x + (parent_width / 2)
        center_y = parent_y + (parent_height / 2)

        x = center_x - (width / 2)
        y = center_y - (height / 2)

        point = wx.Point(x, y)

        self.SetPosition(point)

    def is_ready(self):
        if self.progress_information_plugin:
            return True
        else:
            return False

class SplashScreen(wx.SplashScreen):

    application = None
    parent = None

    def __init__(self, application = None, parent = None, bitmap = None, splash_style = wx.SPLASH_CENTRE_ON_SCREEN, splash_screen_style = wx.NO_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP):
        wx.SplashScreen.__init__(self, bitmap, splash_style, 0, parent, style = splash_screen_style)

        self.application = application
        self.parent = parent

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.Show(False)
        wx.CallAfter(self.parent.Show, True)
        wx.CallAfter(self.application.SetTopWindow, self.parent)

class MainApplication(wx.App):
    """
    The main application class.
    """

    main_gui_plugin = None
    """ The main gui plugin """

    main_frame = None
    """ The main frame """

    splash_screen = None
    """ The splash screen """

    def __init__(self, number, main_gui_plugin):
        self.main_gui_plugin = main_gui_plugin
        wx.App.__init__(self, number)

    def load_main_frame(self):
        # creates the main frame
        self.main_frame = MainFrame(self.main_gui_plugin, None, wx.ID_ANY, MENU_TITLE, size = wx.Size(H_SIZE, V_SIZE))

        # creates the splash screen (in case this is the first load of the gui main plugin)
        if self.splash_screen == None and not self.main_gui_plugin.manager.init_complete:
            plugin_path = self.main_gui_plugin.manager.get_plugin_path_by_id(self.main_gui_plugin.id)
            splash_screen_image_path = plugin_path + "/" + IMAGES_PATH + "/" + SPLASH_IMAGE_FILE_NAME
            splash_screen_bitmap = wx.Image(name = splash_screen_image_path).ConvertToBitmap()
            self.splash_screen = SplashScreen(self, self.main_frame, splash_screen_bitmap)

        # notifies the ready semaphore
        self.main_gui_plugin.release_ready_semaphore()

    def show_main_frame(self):
        if self.splash_screen:
            self.splash_screen.Close()
        else:
            self.main_frame.Show(True)
            self.SetTopWindow(self.main_frame)

    def is_loaded(self):
        """
        Returns the current state of the application.
        """

        return not isinstance(self.main_frame, wx._core._wxPyDeadObject)

    def unload(self):
        """
        Unloads the application from memory.
        """

        logger = self.main_gui_plugin.manager.get_plugin_by_id("pt.hive.colony.plugins.main.log")
        logger_log = logger.get_logger("main")
        logger_log.unset_handler()

        # in case the application is loaded
        if self.is_loaded():
            # creates the exit event
            event = colony.base.util.Event("exit")

            # send the exit event to the queue
            self.main_frame.event_queue.append(event)

            # refreshes the main frame to process the exit event
            self.main_frame.Refresh()
