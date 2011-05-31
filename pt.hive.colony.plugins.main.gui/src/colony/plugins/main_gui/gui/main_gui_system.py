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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys

import wx.aui
import wx._core

import colony.base.util

COLONY_VALUE = "colony"
""" The colony value """

DARWIN_VALUE = "darwin"
""" The darwin value """

FILE_VALUE = "file"
""" The file value """

NODE_VALUE = "node"
""" The node value """

PLUGIN_FOLDER_CLOSED_VALUE = "plugin-folder-closed"
""" The plugin folder closed value """

PLUGIN_FOLDER_OPEN_VALUE = "plugin-folder-open"
""" The plugin folder open value """

TAB_VALUE = "tab"
""" The tab value """

EVENT_EXIT = "exit"
""" The exit event """

UNIX_DIRECTORY_SEPARATOR = "/"
""" The unix directory separator """

GUI_PATH = "main_gui/gui"
""" The gui path """

GUI_RESOURCES_PATH = GUI_PATH + UNIX_DIRECTORY_SEPARATOR + "resources"
""" The gui resources path """

ICONS_PATH = GUI_RESOURCES_PATH + UNIX_DIRECTORY_SEPARATOR + "icons"
""" The icons path """

IMAGES_PATH = GUI_RESOURCES_PATH + UNIX_DIRECTORY_SEPARATOR + "images"
""" The images path """

ICONS_16X16_PATH = ICONS_PATH + UNIX_DIRECTORY_SEPARATOR + "16x16"
""" The icons 16x16 path """

ICONS_32X32_PATH = ICONS_PATH + UNIX_DIRECTORY_SEPARATOR + "32x32"
""" The icons 32x32 path """

NODE_ICON_HEIGHT = 16
""" The icon height """

NODE_ICON_WIDTH = 16
""" The icon width """

SPLASH_IMAGE_FILE_NAME = "colony_splash.png"
""" The splash image file name """

MAIN_WINDOW_WIDTH = 1024
""" The main window width """

MAIN_WINDOW_HEIGHT = 768
""" The main window height """

MAIN_WINDOW_MINIMUM_HEIGHT = 300
""" The main window minimum height """

MAIN_WINDOW_MINIMUM_WIDTH = 400
""" The main window minimum width """

PLUGIN_TREE_HEIGHT = 250
""" The plugin tree's height """

PLUGIN_TREE_WIDTH = 160
""" The plugin tree's width """

PLUGIN_TREE_BEST_HEIGHT = 100
""" The plugin tree's best height """

PLUGIN_TREE_BEST_WIDTH = 250
""" The plugin tree's best width """

PLUGIN_TREE_MINIMUM_WIDTH = 200
""" The plugin tree's minimum width """

PLUGIN_TREE_MINIMUM_HEIGHT = 100
""" The plugin tree's minimum height """

ROOT_NAME = "Colony Plugins"
""" The root name """

TAB_ICON_HEIGHT = 10
""" The tab icon height """

TAB_ICON_WIDTH = 10
""" The tab icon width """

WINDOW_TITLE = "Colony Manager"
""" The window title """

NODE_ICON_SIZE = (
    16, 16
)
""" The icon size """

PANEL_SIZE = (
    970, 720
)
""" The panel's size """

class MainGui:
    """
    The main gui class.
    """

    main_gui_plugin = None
    """ The main gui plugin """

    main_application = None
    """ The main application """

    gui_panel_plugins_map = {}
    """ The gui panel plugins map """

    gui_panel_node_bitmap_map = {}
    """ The gui panel node bitmap map """

    gui_panel_tab_bitmap_map = {}
    """ The gui panel tab bitmap map """

    def __init__(self, main_gui_plugin):
        """
        Constructor of the class.

        @type main_gui_plugin: MainGuiPlugin
        @param main_gui_plugin: The main gui plugin.
        """

        self.main_gui_plugin = main_gui_plugin

        # initializes the data structures
        self.gui_panel_plugins_map = {}
        self.gui_panel_node_bitmap_map = {}
        self.gui_panel_tab_bitmap_map = {}

    def load_main_application(self):
        # initializes the main application
        self.main_application = not self.main_application and MainApplication(self) or self.main_application

        # loads the main frame
        self.main_application.load()

        # initializes the application's main loop
        self.main_application.MainLoop()

    def unload_main_application(self):
        # unloads the main application
        self.main_application.unload()

    def show_main_application(self):
        # shows the application
        self.main_application.show()

    def refresh_main_application(self):
        # refreshes the main application
        self.main_application.refresh()

    def load_gui_panel_plugin(self, plugin):
        # retrieves the bitmap loader plugin
        main_gui_plugin = self.main_gui_plugin
        bitmap_loader_plugin = main_gui_plugin.bitmap_loader_plugin

        # retrieves the plugin id
        plugin_id = plugin.id

        # sets the gui panel plugin in the gui panel plugins map
        self.gui_panel_plugins_map[plugin_id] = plugin

        # retrieves the icon path
        icon_path = plugin.get_icon_path()

        # initializes the icon maps
        gui_panel_bitmap_map = {}

        # loads the bitmaps
        bitmap_loader_plugin.load_icons(icon_path, gui_panel_bitmap_map, {})

        # retrieves the bitmaps
        gui_panel_node_bitmap = gui_panel_bitmap_map[NODE_VALUE]
        gui_panel_tab_bitmap = gui_panel_bitmap_map[TAB_VALUE]

        # sets the bitmap in the gui panel bitmap map
        self.gui_panel_node_bitmap_map[plugin_id] = gui_panel_node_bitmap
        self.gui_panel_tab_bitmap_map[plugin_id] = gui_panel_tab_bitmap

        # refreshes the main application
        self.refresh_main_application()

    def unload_gui_panel_plugin(self, plugin):
        # retrieves the plugin id
        plugin_id = plugin.id

        # removes the gui panel plugin from the gui panel plugins map
        del self.gui_panel_plugins_map[plugin_id]

        # removes the gui panel
        self.main_application.remove_gui_panel(plugin_id)

        # removes the plugin from the bitmap map
        del self.gui_panel_node_bitmap_map[plugin_id]
        del self.gui_panel_tab_bitmap_map[plugin_id]

        # refreshes the main application
        self.refresh_main_application()

class MainApplication(wx.App):
    """
    The main application class.
    """

    main_gui = None
    """ The main gui """

    main_frame = None
    """ The main frame """

    splash_screen = None
    """ The splash screen """

    def __init__(self, main_gui):
        # calls the super
        wx.App.__init__(self, 0)

        # stores the main gui plugin
        self.main_gui = main_gui

    def load(self):
        # retrieves the plugin manager
        main_gui_plugin = self.main_gui.main_gui_plugin
        plugin_manager = main_gui_plugin.manager

        # retrieves the main gui plugin id
        main_gui_plugin_id = main_gui_plugin.id

        # retrieves the main gui plugin path
        main_gui_plugin_path = plugin_manager.get_plugin_path_by_id(main_gui_plugin_id)

        # creates the main frame size
        main_frame_size = wx.Size(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        # creates the main frame
        self.main_frame = MainFrame(self, WINDOW_TITLE, main_frame_size)

        # creates the splash screen (in case this is the first load of the gui main plugin)
        if not self.splash_screen and not plugin_manager.init_complete:
            # retrieves the splash screen image path
            splash_screen_image_path = main_gui_plugin_path + UNIX_DIRECTORY_SEPARATOR + IMAGES_PATH + UNIX_DIRECTORY_SEPARATOR + SPLASH_IMAGE_FILE_NAME

            # creates the splash screen image
            splash_screen_image = wx.Image(name = splash_screen_image_path)

            # converts the splash screen image to a bitmap
            splash_screen_bitmap = splash_screen_image.ConvertToBitmap()

            # creates the splash screen
            self.splash_screen = SplashScreen(self, self.main_frame, splash_screen_bitmap)

        # notifies the ready semaphore
        main_gui_plugin.release_ready_semaphore()

    def unload(self):
        # checks if the main application is loaded
        main_application_loaded = self.is_loaded()

        # in case the main application is not loaded
        if not main_application_loaded:
            # returns
            return

        # creates the exit event
        event = colony.base.util.Event(EVENT_EXIT)

        # send the exit event to the queue
        self.main_frame.event_queue.append(event)

        # refreshes the main frame to process the exit event
        self.main_frame.Refresh()

    def is_loaded(self):
        # returns the application's current state
        return not isinstance(self.main_frame, wx._core._wxPyDeadObject)

    def show(self):
        # closes the splash screen in case it exists
        self.splash_screen and self.splash_screen.Close()

        # shows the main frame in case the splash screen doesn't exist
        not self.splash_screen and self.main_frame.Show(True)

        # sets the main frame as the top window in case the splash screen doesn't exist
        not self.splash_screen and self.SetTopWindow(self.main_frame)

    def refresh(self):
        # checks if the main application is loaded
        loaded = self.is_loaded()

        # refreshes the main frame in
        # case the application is loaded
        loaded and self.main_frame.refresh()

    def remove_gui_panel(self, gui_panel):
        # removes the gui panel
        self.main_frame.remove_gui_panel(gui_panel)

class MainFrame(wx.Frame):
    """
    The main frame used in the gui.
    """

    main_application = None
    """ The main main_application """

    plugin_tree = None
    """ The main plugin tree used """

    tab_container_panel = None
    """ The tab container panel """

    bitmaps_16x16_map = {}
    """ The bitmaps map for 16x16 bitmaps """

    bitmaps_32x32_map = {}
    """ The bitmaps map for 32x32 bitmaps """

    icons_16x16_map = {}
    """ The icons map for 16x16 icons """

    icons_32x32_map = {}
    """ The icons map for 32x32 icons """

    event_queue = []
    """ The queue of events to be processed """

    gui_panels_map = {}
    """ The gui panels map """

    gui_panels = []
    """ The gui panels """

    def __init__(self, main_application, title, size):
        # calls the super
        wx.Frame.__init__(self, None, wx.ID_ANY, title, wx.DefaultPosition, size, wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER | wx.CLIP_CHILDREN)

        # initializes the data structures
        self.bitmaps_16x16_map = {}
        self.bitmaps_32x32_map = {}
        self.icons_16x16_map = {}
        self.icons_32x32_map = {}
        self.event_queue = []
        self.gui_panels_map = {}
        self.gui_panels = []

        # sets the main application plugin
        self.main_application = main_application

        # draws the main frame
        self.draw()

    def draw(self):
        # retrieves the main gui plugin
        main_gui = self.main_application.main_gui
        main_gui_plugin = main_gui.main_gui_plugin

        # retrieves the bitmap loader plugin
        bitmap_loader_plugin = main_gui_plugin.bitmap_loader_plugin

        # retrieves the plugin manager
        plugin_manager = main_gui_plugin.manager

        # retrieves the main gui plugin id
        main_gui_plugin_id = main_gui_plugin.id

        # starts the plugin loading process
        self.plugin_path = plugin_manager.get_plugin_path_by_id(main_gui_plugin_id)

        # loads the icons using the bitmap loader plugin
        bitmap_loader_plugin.load_icons(self.plugin_path + UNIX_DIRECTORY_SEPARATOR + ICONS_16X16_PATH, self.bitmaps_16x16_map, self.icons_16x16_map)
        bitmap_loader_plugin.load_icons(self.plugin_path + UNIX_DIRECTORY_SEPARATOR + ICONS_32X32_PATH, self.bitmaps_32x32_map, self.icons_32x32_map)

        # freezes the frame
        self.Freeze()

        # tells the frame manager to manage this frame
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        # retrieves the colony icon
        colony_icon = self.icons_16x16_map[COLONY_VALUE]

        # sets the window's icon
        self.SetIcon(colony_icon)

        # defines the minimum size
        minimum_size = wx.Size(MAIN_WINDOW_MINIMUM_WIDTH, MAIN_WINDOW_MINIMUM_HEIGHT)

        # sets the windows minimum size
        self.SetMinSize(minimum_size)

        # creates the plugin tree
        self.create_plugin_tree()

        # creates the tab container panel
        self.create_tab_container_panel()

        # commits all changes to the frame manager
        self._mgr.Update()

        # binds the events
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_MENU, self.on_exit, id = wx.ID_EXIT)
        self.Bind(wx.EVT_IDLE, self.on_idle)

        # refreshes the main frame
        self.Refresh()

        # releases the frame
        self.Thaw()

    def create_plugin_tree(self):
        # defines the plugin tree's position
        plugin_tree_position = wx.Point(0, 0)

        # defines the plugin tree's size
        plugin_tree_size = wx.Size(PLUGIN_TREE_WIDTH, PLUGIN_TREE_HEIGHT)

        # creates the plugin tree
        plugin_tree = PluginTree(self, plugin_tree_position, plugin_tree_size)

        # draws the plugin tree
        plugin_tree.draw()

        # sets the plugin tree
        self.plugin_tree = plugin_tree

        # defines the plugin tree's best size
        plugin_tree_best_size = wx.Size(PLUGIN_TREE_BEST_WIDTH, PLUGIN_TREE_BEST_HEIGHT)

        # defines the plugin tree's minimum size
        plugin_tree_minimum_size = wx.Size(PLUGIN_TREE_MINIMUM_WIDTH, PLUGIN_TREE_MINIMUM_HEIGHT)

        # creates the plugin tree pane info
        plugin_tree_pane_info = wx.aui.AuiPaneInfo()
        plugin_tree_pane_info.Name("tree_content")
        plugin_tree_pane_info.BestSize(plugin_tree_best_size)
        plugin_tree_pane_info.MinSize(plugin_tree_minimum_size)
        plugin_tree_pane_info.Left()
        plugin_tree_pane_info.Layer(1)
        plugin_tree_pane_info.Position(1)
        plugin_tree_pane_info.CloseButton(False)
        plugin_tree_pane_info.MaximizeButton(False)
        plugin_tree_pane_info.Floatable(False)

        # adds the plugin tree
        self._mgr.AddPane(plugin_tree, plugin_tree_pane_info)

        # shows the plugin tree pane info
        plugin_tree_pane_info.Show()
        plugin_tree_pane_info.Left()
        plugin_tree_pane_info.Layer(0)
        plugin_tree_pane_info.Row(0)
        plugin_tree_pane_info.Position(0)

        # sets the plugin tree
        self.plugin_tree = plugin_tree

    def create_tab_container_panel(self):
        # creates the tab container panel
        tab_container_panel = TabContainerPanel(self)

        # creates the tab container panel pane info
        tab_container_panel_pane_info = wx.aui.AuiPaneInfo()
        tab_container_panel_pane_info.Name("tab_container_content")
        tab_container_panel_pane_info.CenterPane()

        # adds the tab container panel
        self._mgr.AddPane(tab_container_panel, tab_container_panel_pane_info)

        # shows the tab container panel pane info
        tab_container_panel_pane_info.Show()

        # sets the tab container panel
        self.tab_container_panel = tab_container_panel

    def refresh(self):
        # retrieves the main gui
        main_application = self.main_application
        main_gui = main_application.main_gui

        # retrieves the gui panel bitmap maps
        gui_panel_node_bitmap_map = main_gui.gui_panel_node_bitmap_map
        gui_panel_tab_bitmap_map = main_gui.gui_panel_tab_bitmap_map

        # creates copies of the bitmap maps to avoid manipulating these references
        tab_container_panel_bitmap_map = dict(gui_panel_tab_bitmap_map)
        plugin_tree_bitmap_map = dict(gui_panel_node_bitmap_map)

        # sets the bitmaps in the tab container panel
        self.tab_container_panel.set_bitmaps(tab_container_panel_bitmap_map)

        # sets the plugin folder icons in the plugin tree bitmap map
        plugin_tree_bitmap_map[PLUGIN_FOLDER_OPEN_VALUE] = self.bitmaps_16x16_map[PLUGIN_FOLDER_OPEN_VALUE]
        plugin_tree_bitmap_map[PLUGIN_FOLDER_CLOSED_VALUE] = self.bitmaps_16x16_map[PLUGIN_FOLDER_CLOSED_VALUE]

        # sets the bitmaps in the plugin tree
        self.plugin_tree.set_bitmaps(plugin_tree_bitmap_map)

        # refreshes the plugin tree
        self.plugin_tree.refresh()

    def create_gui_panel(self, gui_panel_plugin_id):
        # retrieves the main aplication
        main_application = self.main_application
        main_gui = main_application.main_gui

        # retrieves the gui panel plugin
        gui_panel_plugin = main_gui.gui_panel_plugins_map[gui_panel_plugin_id]

        # retrieves the gui panel plugin's short name
        gui_panel_plugin_short_name = gui_panel_plugin.short_name

        # retrieves the gui panel
        gui_panel = self.gui_panels_map.get(gui_panel_plugin_id, None)

        # in case a gui panel
        # was already created
        if gui_panel:
            # returns
            return

        # creates the gui panel
        gui_panel = self.tab_container_panel.create_gui_panel(gui_panel_plugin, gui_panel_plugin_short_name)

        # stores the gui panel in the gui panels map
        self.gui_panels_map[gui_panel_plugin_id] = gui_panel

        # adds the gui panel to the gui panels list
        self.gui_panels.append(gui_panel)

    def remove_gui_panel(self, gui_panel_id):
        # retrieves the gui panel
        gui_panel = self.gui_panels_map.get(gui_panel_id, None)

        # in case no gui panel was found
        if not gui_panel:
            # returns
            return

        # removes the gui panel from the gui panels map
        del self.gui_panels_map[gui_panel_id]

        # retrieves the gui panel's index
        gui_panel_index = self.gui_panels.index(gui_panel)

        # removes the gui panel from the gui panels list
        self.gui_panels.remove(gui_panel)

        # removes the gui panel from the tab container
        self.tab_container_panel.remove_gui_panel(gui_panel_index)

    def on_close(self, event):
        # destroys the frame manager
        self._mgr.UnInit()

        # deletes the frame manager reference
        del self._mgr

        # destroys the main frame
        self.Destroy()

    def on_exit(self, event):
        # closes the main frame
        self.Close()

    def on_idle(self, event):
        # flushes the event queue
        while self.event_queue:
            # retrieves the event
            event = self.event_queue.pop(0)

            # closes the main frame in case
            # this is an exit event
            (event.event_name == EVENT_EXIT) and self.Close()

class TabContainerPanel(wx.Panel):
    """
    The tab container panel class
    """

    main_frame = None
    """ The main frame """

    bitmaps_map = {}
    """ The bitmaps map """

    def __init__(self, main_frame):
        # calls the super
        wx.Panel.__init__(self, main_frame, size = PANEL_SIZE)

        # sets the main frame
        self.main_frame = main_frame

        # initializes the bitmaps map
        self.bitmaps_map = {}

        # draws the tab container panel
        self.draw()

    def set_bitmaps(self, bitmaps_map):
        # resets the bitmaps map
        self.bitmaps_map = {}

        # creates the image list
        image_list = wx.ImageList(TAB_ICON_WIDTH, TAB_ICON_HEIGHT)

        # for each of the provided bitmaps
        for bitmap_id in bitmaps_map:
            # retrieves the bitmap
            bitmap = bitmaps_map[bitmap_id]

            # adds the image to the image list
            bitmap_index = image_list.Add(bitmap)

            # sets the bitmap index in the bitmaps map
            self.bitmaps_map[bitmap_id] = bitmap_index

        # assigns the image list
        self.notebook.AssignImageList(image_list)

    def draw(self):
        # creates the main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # sets the main sizer
        self.SetSizer(main_sizer)

        # creates a new notebook
        notebook = wx.Notebook(self, wx.ID_ANY, style = wx.CLIP_CHILDREN)

        # adds the notebook to the main sizer
        main_sizer.Add(notebook, 6, wx.EXPAND)

        # sets the notebook
        self.notebook = notebook

        # performs the layout
        main_sizer.Layout()

    def refresh(self):
        # refreshes the notebook
        self.notebook.Refresh()

        # refreshes the panel
        self.Refresh()

    def create_gui_panel(self, gui_panel_plugin, gui_panel_name):
        # retrieves the gui panel plugin id
        gui_panel_plugin_id = gui_panel_plugin.id

        # retrieves the gui panel bitmap index
        gui_panel_bitmap_index = self.bitmaps_map[gui_panel_plugin_id]

        # retrieves the tab container panel's book
        notebook = self.notebook

        # creates the gui panel plugin's panel
        gui_panel = gui_panel_plugin.create_panel(notebook)

        # freezes the tab container panel
        self.Freeze()

        # adds the gui panel to the page
        notebook.AddPage(gui_panel, gui_panel_name, imageId = gui_panel_bitmap_index)

        # releases the tab container panel
        self.Thaw()

        # returns the gui panel
        return gui_panel

    def remove_gui_panel(self, gui_panel_index):
        # retrieves the book
        notebook = self.notebook

        # retrieves the platform
        platform = sys.platform

        # freezes the tab container panel
        self.Freeze()

        # removes the gui panel if supported
        (platform == DARWIN_VALUE) and notebook.DeletePage(gui_panel_index)

        # releases the tab container panel
        self.Thaw()

class PluginTree(wx.TreeCtrl):
    """
    The plugin tree class.
    """

    main_frame = None
    """ The main frame """

    root_node_item = None
    """ The root node item """

    bitmaps_map = {}
    """ The bitmaps map """

    def __init__(self, main_frame, position, size):
        # calls the super
        wx.TreeCtrl.__init__(self, main_frame, wx.ID_ANY, position, size, wx.TR_DEFAULT_STYLE | wx.NO_BORDER)

        # sets the main frame in the plugin tree
        self.main_frame = main_frame

        # initializes the bitmaps map
        self.bitmaps_map = {}

    def set_bitmaps(self, bitmaps_map):
        # resets the bitmaps map
        self.bitmaps_map = {}

        # creates the image list
        image_list = wx.ImageList(NODE_ICON_WIDTH, NODE_ICON_HEIGHT)

        # for each of the provided bitmaps
        for bitmap_id in bitmaps_map:
            # retrieves the bitmap
            bitmap = bitmaps_map[bitmap_id]

            # adds the image to the image list
            bitmap_index = image_list.Add(bitmap)

            # sets the bitmap in the bitmaps map
            self.bitmaps_map[bitmap_id] = bitmap_index

        # assigns the image list
        self.AssignImageList(image_list)

    def draw(self):
        # creates the root node item
        self.root_node_item = self.AddRoot(ROOT_NAME)

        # binds the left double click event
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_double_click)

        # in case the tree icon map is not defined
        if not self.bitmaps_map:
            # returns
            return

        # retrieves the icons
        folder_icon_index = self.bitmaps_map["plugin-folder-closed"]
        folder_open_icon_index = self.bitmaps_map["plugin-folder-open"]

        # assigns the images to the root node item
        self.SetItemImage(self.root_node_item, folder_icon_index, wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root_node_item, folder_open_icon_index, wx.TreeItemIcon_Expanded)

    def refresh(self):
        # retrieves the main gui plugin
        main_application = self.main_frame.main_application
        main_gui = main_application.main_gui
        main_gui_plugin = main_gui.main_gui_plugin

        # retrieves the gui panel plugins
        gui_panel_plugins = main_gui_plugin.gui_panel_plugins

        # freezes the plugin tree
        self.Freeze()

        # deletes all items
        self.DeleteAllItems()

        # draws the plugin tree
        self.draw()

        # adds the node item for each plugin
        for gui_panel_plugin in gui_panel_plugins:
            # retrieves the gui panel plugin's id
            gui_panel_plugin_id = gui_panel_plugin.id

            # defines the plugin node name
            plugin_node_name = gui_panel_plugin.short_name

            # retrieves the plugin node bitmap index
            plugin_node_bitmap_index = self.bitmaps_map[gui_panel_plugin_id]

            # creates the plugin node data
            plugin_node_data = wx.TreeItemData(gui_panel_plugin_id)

            # creates the node item for the plugin
            self.AppendItem(self.root_node_item, plugin_node_name, plugin_node_bitmap_index, data = plugin_node_data)

        # expands all items
        self.ExpandAll()

        # refreshes the interface
        self.Refresh()

        # releases the plugin tree
        self.Thaw()

    def on_left_double_click(self, event):
        # retrieves the main gui
        main_frame = self.main_frame

        # retrieves the event's position
        position = event.GetPosition()

        # retrieves the selected item
        node_item, _flags = self.HitTest(position)

        # in case no item was selected
        if not node_item:
            # returns
            return

        # retrieves the clicked node item's data
        node_item_data = self.GetItemData(node_item)

        # retrieves the gui panel plugin id
        gui_panel_plugin_id = node_item_data.GetData()

        # in case the id is none
        if not gui_panel_plugin_id:
            # returns
            return

        # creates the gui panel
        main_frame.create_gui_panel(gui_panel_plugin_id)

class SplashScreen(wx.SplashScreen):

    main_application = None
    """ The main application """

    main_frame = None
    """ The main frame """

    def __init__(self, main_application, main_frame, bitmap):
        # calls the super
        wx.SplashScreen.__init__(self, bitmap, wx.SPLASH_CENTRE_ON_SCREEN, 0, main_frame, style = wx.NO_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)

        # stores the main application and the parent
        self.main_application = main_application
        self.main_frame = main_frame

        # binds the splash screen close event
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        # hides the splash screen
        self.Show(False)

        # shows the parent
        wx.CallAfter(self.main_frame.Show, True)

        # set the main application as the top window
        wx.CallAfter(self.main_application.SetTopWindow, self.main_frame)
