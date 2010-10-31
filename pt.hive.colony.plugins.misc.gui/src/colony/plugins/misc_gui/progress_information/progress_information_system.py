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

import os
import stat

import wx.lib.scrolledpanel

import progress_information_logic
import colony.base.plugin_system

BASE_PATH = "/misc_gui"
PROGRESS_INFORMATION_PATH = BASE_PATH + "/" + "progress_information"
PROGRESS_INFORMATION_RESOURCES_PATH = PROGRESS_INFORMATION_PATH + "/" + "resources"
ICONS_PATH = PROGRESS_INFORMATION_RESOURCES_PATH + "/" + "icons"
ICONS_10X10_PATH = ICONS_PATH + "/" + "10x10"
ICONS_16X16_PATH = ICONS_PATH + "/" + "16x16"

PULSE_GAUGE = 0
VALUE_GAUGE = 1

GAUGE_MAX_VALUE = 100

TIMER_TIMEOUT = 20

EVT_PANEL_CLICK_TYPE = wx.NewEventType()
EVT_PANEL_CLICK = wx.PyEventBinder(EVT_PANEL_CLICK_TYPE, 1)

STATUS_TASK_NONE = progress_information_logic.STATUS_NONE
STATUS_TASK_RESUMING = progress_information_logic.STATUS_RESUMING
STATUS_TASK_RUNNING = progress_information_logic.STATUS_RUNNING
STATUS_TASK_PAUSING = progress_information_logic.STATUS_PAUSING
STATUS_TASK_PAUSED = progress_information_logic.STATUS_PAUSED
STATUS_TASK_STOPPING = progress_information_logic.STATUS_STOPPING
STATUS_TASK_STOPPED = progress_information_logic.STATUS_STOPPED

#@todo: review and comment this file
#@TODO fazer refactor a todo a parte grafica para que fique com bom aspecto os nomes das variaveis etc.
class ProgressInformation:

    progress_information_plugin = None

    progress_information_panel = None

    icons_loaded = False

    task_id_task_progress_information_item_map = {}

    bitmaps_10x10_map = {}
    """ The bitmaps map for 10x10 bitmaps """

    bitmaps_16x16_map = {}
    """ The bitmaps map for 16x16 bitmaps """

    icons_10x10_map = {}
    """ The icons map for 10x10 icons """

    icons_16x16_map = {}
    """ The icons map for 16x16 icons """

    #@todo fazer refactor deste codigo badalhoco
    def __init__(self, progress_information_plugin):
        self.progress_information_plugin = progress_information_plugin

        self.task_id_task_progress_information_item_map = {}
        self.bitmaps_10x10_map = {}
        self.bitmaps_16x16_map = {}
        self.icons_10x10_map = {}
        self.icons_16x16_map = {}

        self.plugin_path = self.progress_information_plugin.manager.get_plugin_path_by_id(self.progress_information_plugin.id)

    def load_icons(self):
        if  self.icons_loaded:
            return

        self.progress_information_plugin.bitmap_loader_plugin.load_icons(self.plugin_path + ICONS_16X16_PATH, self.bitmaps_16x16_map, self.icons_16x16_map)
        self.icons_loaded = True

    def do_panel(self, parent):
        self.load_icons()
        self.progress_information_panel = ProgressInformationPanel(parent, self)
        return self.progress_information_panel

    def process_task_information_changed_event(self, event_name, event_args):
        # in case it's a new task event
        if colony.base.plugin_system.is_event_or_sub_event("task_information_changed.new_task", event_name):
            # retrieves the task object from the event arguments
            task = event_args[0]

            # creates the new task
            task_progress_information_item = self.progress_information_plugin.progress_information.add_task_progress_information_item(task, task.id, task.name, task.description, "statuso todo", 0, None)

            # in case the progress information panel is not shown
            if not self.progress_information_panel.GetParent().IsShown():
                # generates the show progress information panel event
                self.progress_information_plugin.generate_event("gui_progress_information_changed.show_panel", [])

            self.task_id_task_progress_information_item_map[task.id] = task_progress_information_item
        # in case it's an updated task event
        elif colony.base.plugin_system.is_event_or_sub_event("task_information_changed.updated_task", event_name):
            # retrieves the task object from the event arguments
            task = event_args[0]
            # retrieves the map object with the argument value
            args_map = event_args[1]

            task_progress_information_item = self.task_id_task_progress_information_item_map[task.id]

            for args in args_map:
                if args == "status":
                    status_value = args_map[args]

                    if status_value == "paused":
                        task_progress_information_item.set_status(progress_information_logic.STATUS_PAUSED)
                    elif status_value == "running":
                        task_progress_information_item.set_status(progress_information_logic.STATUS_RUNNING)

                elif args == "percentage_complete":
                    task_progress_information_item.set_percentage_complete(args_map[args])
        # in case it's a stopped task event
        elif colony.base.plugin_system.is_event_or_sub_event("task_information_changed.stopped_task", event_name):
            # retrieves the task object from the event arguments
            task = event_args[0]

            task_progress_information_item = self.task_id_task_progress_information_item_map[task.id]

            # sets the status of the task to stopped
            task_progress_information_item.set_status(progress_information_logic.STATUS_STOPPED)

    def add_task_progress_information_item(self, task, task_progress_information_id, task_name, task_description, current_description, percentage_complete, bitmap):
        task_progress_information_item = progress_information_logic.TaskProgressInformationItem(task, task_progress_information_id, task_name, task_description, current_description, percentage_complete)
        progress_information_panel_item = self.progress_information_panel.add_task_progress_information_item(task_progress_information_item)
        task_progress_information_item.panel = progress_information_panel_item
        return task_progress_information_item

    def run_in_background(self):
        # generates the hide progress information panel event
        self.progress_information_plugin.generate_event("gui_progress_information_changed.hide_panel", [])

class ProgressInformationPanel(wx.Panel):
    """
    The progress information panel class
    """

    MIN_WIDTH = 550
    """ The minimum width for the panel """

    MIN_HEIGHT = 360
    """ The minimum height for the panel """

    progress_information = None

    progress_information_items_sizer = None

    progress_information_items_list = []
    selected_progress_information_panel_item = None
    panel_shown = True
    previous_height = 0

    def __init__(self, parent, progress_information):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.progress_information = progress_information

        progress_information_items_list = []

        self.panel = wx.lib.scrolledpanel.ScrolledPanel(self, wx.ID_ANY, style = wx.DOUBLE_BORDER | wx.TAB_TRAVERSAL)
        self.bitmap_1 = wx.StaticBitmap(self, wx.ID_ANY, wx.ArtProvider_GetBitmap(wx.ART_INFORMATION))
        self.label_1 = wx.StaticText(self, wx.ID_ANY, "'None' operation description")
        self.gauge_1 = wx.Gauge(self, wx.ID_ANY, 10)
        self.label_2 = wx.StaticText(self, wx.ID_ANY, "'None' informative message")

        self.button_1 = wx.Button(self, wx.ID_ANY, "Run in Background")
        self.button_2 = wx.Button(self, wx.ID_ANY, "Cancel")
        self.button_3 = wx.Button(self, wx.ID_ANY, "<< Details")
        self.button_1.Bind(wx.EVT_BUTTON, self.on_button_run_in_background)
        self.button_2.Bind(wx.EVT_BUTTON, self.on_button_cancel)
        self.button_3.Bind(wx.EVT_BUTTON, self.on_button_details)

        self.panel_shown = True

        self.__set_properties()
        self.__do_layout()

        self.panel.SetupScrolling()

    def on_button_run_in_background(self, event):
        self.progress_information.run_in_background()

    def on_button_cancel(self, event):
        pass

    def on_button_details(self, event):
        parent = self.GetParent()
        parent_size = parent.GetSize()
        parent_width = parent_size.width
        parent_height = parent_size.height

        if self.panel_shown:
            self.panel.Show(False)
            parent.SetSize(wx.Size(parent_width, 220))
            self.button_3.SetLabel(">> Details")
            self.panel_shown = False
            self.previous_height = parent_height
        else:
            self.panel.Show(True)
            self.panel.SetFocus()
            if parent_height < self.previous_height:
                parent_height = self.previous_height
            parent.SetSize(wx.Size(parent_width, parent_height))
            self.button_3.SetLabel("<< Details")
            self.panel_shown = True
            self.Layout()

    def load_icons(self, path, bitmaps_dic, icons_dic):
        dir_list = os.listdir(path)
        for file_name in dir_list:
            full_path = path + "/" + file_name
            mode = os.stat(full_path)[stat.ST_MODE]
            if not stat.S_ISDIR(mode):
                split = os.path.splitext(file_name)
                if split[-1] == ".png":
                    bitmap = wx.Bitmap(full_path, wx.BITMAP_TYPE_PNG)
                    icon = wx.IconFromBitmap(bitmap)
                    name = split[0]
                    bitmaps_dic[name] = bitmap
                    icons_dic[name] = icon

    def __set_properties(self):
        self.panel.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.label_1.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.gauge_1.SetMinSize((-1, 20))
        self.label_2.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.button_1.SetMinSize((120, -1))
        self.button_1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.button_2.SetMinSize((90, -1))
        self.button_2.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.button_3.SetMinSize((90, -1))
        self.button_3.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.SetMinSize((ProgressInformationPanel.MIN_WIDTH, ProgressInformationPanel.MIN_HEIGHT))

    def __do_layout(self):
        # retrieves the parent panel (frame)
        parent = self.GetParent()

        # creates the sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        panel1_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)

        self.progress_information_items_sizer = sizer_8

        panel1_sizer.Add((20, 20), 0, 0, 0)
        sizer_4.Add((20, 20), 0, 0, 0)
        sizer_4.Add(self.bitmap_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add((10, 20), 0, 0, 0)
        sizer_4.Add(self.label_1, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add((20, 20), 0, 0, 0)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_1.Add((20, 10), 0, 0, 0)
        sizer_5.Add((20, 10), 0, 0, 0)
        sizer_5.Add(self.gauge_1, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_5.Add((20, 10), 0, 0, 0)
        sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_1.Add((20, 0), 0, 0, 0)
        sizer_6.Add((20, 20), 0, 0, 0)
        sizer_6.Add(self.label_2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_6.Add((20, 20), 0, 0, 0)
        sizer_1.Add(sizer_6, 1, wx.EXPAND, 0)
        panel1_sizer.Add(sizer_1, 0, wx.EXPAND, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_7.Add((20, 20), 0, 0, 0)
        self.panel.SetSizer(sizer_8)
        sizer_7.Add(self.panel, 1, wx.EXPAND, 0)
        sizer_7.Add((10, 20), 0, 0, 0)
        sizer_2.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        panel1_sizer.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_3.Add(self.button_1, 0, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, 0)
        sizer_3.Add((5, 20), 0, 0, 0)
        sizer_3.Add(self.button_2, 0, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, 0)
        sizer_3.Add((5, 20), 0, 0, 0)
        sizer_3.Add(self.button_3, 0, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, 0)
        sizer_3.Add((20, 20), 0, 0, 0)
        panel1_sizer.Add(sizer_3, 0, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, 0)
        panel1_sizer.Add((20, 20), 0, 0, 0)
        self.SetSizer(panel1_sizer)
        main_sizer.Add(self, 1, wx.EXPAND | wx.ALIGN_BOTTOM, 0)

        parent.SetSizer(main_sizer)
        main_sizer.Fit(parent)
        parent.Layout()

        # loads the scrolling bar in the panel
        self.panel.SetupScrolling()

    def add_progress_information_panel_item(self, progress_information_panel_item = None):
        self.progress_information_items_list.append(progress_information_panel_item)
        self.progress_information_items_sizer.Add(progress_information_panel_item, 0, wx.EXPAND, 0)
        progress_information_panel_item.Bind(EVT_PANEL_CLICK, self.on_progress_information_panel_click)
        self.panel.Layout()
        self.panel.SetupScrolling()

    def add_task_progress_information_item(self, task_progress_information_item):
        gauge_type = None
        percentage_complete = task_progress_information_item.percentage_complete

        if percentage_complete != -1:
            gauge_type = VALUE_GAUGE
        else:
            gauge_type = PULSE_GAUGE

        # freezes the panel
        self.panel.Freeze()

        # creates a new progress information panel item
        progress_information_panel_item = ProgressInformationPanelItem(self.panel, self.progress_information, task_progress_information_item, gauge_type)
        # adds the panel to the progress information panel
        self.add_progress_information_panel_item(progress_information_panel_item)

        # resumes the drawing in the panel
        self.panel.Thaw()

        return progress_information_panel_item

    def unselect_progress_information_panel_items(self):
        for progress_information_panel_item in self.progress_information_items_list:
            progress_information_panel_item.unselect()

    def unselect_selected_progress_information_panel_item(self):
        if self.selected_progress_information_panel_item:
            self.selected_progress_information_panel_item.unselect()

    def on_progress_information_panel_click(self, event):
        progress_information_panel_item = event.get_panel()

        # in case the element is not yet selected
        if not progress_information_panel_item.selected:
            # unselect the current selection
            self.unselect_selected_progress_information_panel_item()
            # sets the current selection
            self.selected_progress_information_panel_item = progress_information_panel_item
        else:
            self.selected_progress_information_panel_item = None

        progress_information_panel_item.change_selection_state()

class ProgressInformationPanelItem(wx.Panel):

    DEFAULT_COLOR = wx.SYS_COLOUR_3DFACE
    HIGHLIGHT_COLOR = wx.SYS_COLOUR_HIGHLIGHT

    progress_information = None
    task_progress_information_item = None
    gauge_type = PULSE_GAUGE

    selected = False

    def __init__(self, parent, progress_information, task_progress_information_item = progress_information_logic.TaskProgressInformationItem(), gauge_type = PULSE_GAUGE):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.progress_information = progress_information
        self.task_progress_information_item = task_progress_information_item
        self.gauge_type = gauge_type

        self.selected = False

        task_name = self.task_progress_information_item.task_name
        task_description = self.task_progress_information_item.task_description

        self.bitmap = wx.StaticBitmap(self, wx.ID_ANY, self.progress_information.bitmaps_16x16_map["task"])
        self.label_1 = wx.StaticText(self, wx.ID_ANY, task_name)
        self.gauge = wx.Gauge(self, wx.ID_ANY, GAUGE_MAX_VALUE)
        self.bitmap_button_1 = wx.BitmapButton(self, wx.ID_ANY, self.progress_information.bitmaps_16x16_map["pause"])
        self.bitmap_button_2 = wx.BitmapButton(self, wx.ID_ANY, self.progress_information.bitmaps_16x16_map["stop"])
        self.label_2 = wx.StaticText(self, wx.ID_ANY, task_description)

        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.bitmap.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.label_1.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.gauge.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.label_2.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)

        self.bitmap_button_1.Bind(wx.EVT_BUTTON, self.on_bitmap_button_1)
        self.bitmap_button_2.Bind(wx.EVT_BUTTON, self.on_bitmap_button_2)

        if self.gauge_type == VALUE_GAUGE:
            self.update_value_gauge_value()
        else:
            self.setup_pulse_gauge()

        self.__set_properties()
        self.__do_layout()

    def timer_handler(self, event):
        self.gauge.Pulse()

    def on_left_down(self, event):
        event_handler = self.GetEventHandler()
        custom_event = CustomEvent(EVT_PANEL_CLICK_TYPE, self.GetId())
        custom_event.set_panel(self)
        event_handler.ProcessEvent(custom_event)
        event.Skip()

    def on_bitmap_button_1(self, event):
        self.pause_resume_task()

    def on_bitmap_button_2(self, event):
        self.stop_task()

    def change_selection_state(self):
        if self.selected:
            self.unselect()
        else:
            self.select()

    def unselect(self):
        self.SetBackgroundColour(wx.SystemSettings_GetColour(ProgressInformationPanelItem.DEFAULT_COLOR))
        self.Refresh()
        self.selected = False

    def select(self):
        self.SetBackgroundColour(wx.SystemSettings_GetColour(ProgressInformationPanelItem.HIGHLIGHT_COLOR))
        self.Refresh()
        self.SetFocus()
        self.selected = True

    def setup_pulse_gauge(self):
        if self.gauge_type == PULSE_GAUGE:
            self.Bind(wx.EVT_TIMER, self.timer_handler)
            self.timer = wx.Timer(self)
            self.timer.Start(TIMER_TIMEOUT)

    def update_value_gauge_value(self):
        if self.gauge_type == VALUE_GAUGE:
            percentage_complete = self.task_progress_information_item.get_percentage_complete()
            self.gauge.SetValue(percentage_complete)

    def update_task_name(self):
        task_name = self.task_progress_information_item.task_name
        status_message = self.task_progress_information_item.status_message

        if status_message and not status_message == "" and not status_message == "none":
            message = task_name + " " + "(" + status_message + ")"
        else:
            message = task_name

        self.label_1.SetLabel(message)

    def update_task_description(self):
        task_description = self.task_progress_information_item.task_description
        self.label_2.SetLabel(task_description)

    def update_status_message(self):
        self.update_task_name()

    def update_task_status(self, status):
        if status == STATUS_TASK_NONE:
            pass
        elif status == STATUS_TASK_RESUMING:
            self.enable_bitmap_button_1(False)
        elif status == STATUS_TASK_RUNNING:
            self.change_bitmap_button_1(status)
            self.enable_bitmap_button_1(True)
        elif status == STATUS_TASK_PAUSING:
            self.enable_bitmap_button_1(False)
        elif status == STATUS_TASK_PAUSED:
            self.change_bitmap_button_1(status)
            self.enable_bitmap_button_1(True)
        elif status == STATUS_TASK_STOPPING:
            self.enable_bitmap_button_1(False)
            self.enable_bitmap_button_2(False)
        elif status == STATUS_TASK_STOPPED:
            self.remove_task()

    def pause_resume_task(self):
        if self.task_progress_information_item.status == STATUS_TASK_RUNNING:
            self.pause_task()
        elif self.task_progress_information_item.status == STATUS_TASK_PAUSED:
            self.resume_task()

    def pause_task(self):
        self.task_progress_information_item.task.pause([])
        self.task_progress_information_item.set_status(progress_information_logic.STATUS_PAUSING)

    def resume_task(self):
        self.task_progress_information_item.task.resume([])
        self.task_progress_information_item.set_status(progress_information_logic.STATUS_RESUMING)

    def stop_task(self):
        self.task_progress_information_item.task.stop([])
        self.task_progress_information_item.set_status(progress_information_logic.STATUS_STOPPING)

    def remove_task(self):
        container_panel = self.GetParent()
        parent_panel = container_panel.GetParent()
        parent_panel.progress_information_items_sizer.Show(self, False)
        parent_panel.progress_information_items_sizer.Remove(self)
        parent_panel.progress_information_items_list.remove(self)
        container_panel.SetupScrolling()

        # in case there's no tasks left we close the progress information panel
        if len(parent_panel.progress_information_items_list) == 0:
            parent_panel.progress_information.run_in_background()

    def change_bitmap_button_1(self, status):
        if status == STATUS_TASK_RUNNING:
            self.bitmap_button_1.SetBitmapLabel(self.progress_information.bitmaps_16x16_map["pause"])
        elif status == STATUS_TASK_PAUSED:
            self.bitmap_button_1.SetBitmapLabel(self.progress_information.bitmaps_16x16_map["resume"])

    def enable_bitmap_button_1(self, value = True):
        if value:
            self.bitmap_button_1.Enable()
        else:
            self.bitmap_button_1.Disable()

    def enable_bitmap_button_2(self, value = True):
        if value:
            self.bitmap_button_2.Enable()
        else:
            self.bitmap_button_2.Disable()

    def __set_properties(self):
        self.SetBackgroundColour(wx.SystemSettings_GetColour(ProgressInformationPanelItem.DEFAULT_COLOR))
        self.label_1.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.gauge.SetMinSize((-1, 15))
        self.bitmap_button_1.SetSize(self.bitmap_button_1.GetBestSize())
        self.bitmap_button_2.SetSize(self.bitmap_button_2.GetBestSize())
        self.label_2.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)

        sizer_1.Add((20, 5), 0, 0, 0)
        sizer_2.Add((5, 20), 0, 0, 0)
        sizer_3.Add(self.bitmap, 0, 0, 0)
        sizer_3.Add((5, 20), 0, 0, 0)
        sizer_4.Add(self.label_1, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add((20, 3), 0, 0, 0)
        sizer_5.Add(self.gauge, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_5.Add((10, 20), 0, 0, 0)
        sizer_6.Add(self.bitmap_button_1, 1, wx.ALIGN_CENTER_VERTICAL | wx.SHAPED, 0)
        sizer_6.Add(self.bitmap_button_2, 1, wx.ALIGN_CENTER_VERTICAL | wx.SHAPED, 0)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_4.Add((20, 3), 0, 0, 0)
        sizer_4.Add(self.label_2, 0, 0, 0)
        sizer_3.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_3.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_2.Add((10, 20), 0, 0, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add((20, 5), 0, 0, 0)

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

class CustomEvent(wx.PyCommandEvent):

    panel = None

    def __init__(self, event_type, id):
        wx.PyCommandEvent.__init__(self, event_type, id)

    def set_panel(self, panel):
        self.panel = panel

    def get_panel(self):
        return self.panel
