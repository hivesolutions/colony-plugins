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
import os.path

import diamante_gui

TXT_APPLICATION_PATH_NAME = "txt_application_path"
LBL_APPLICATION_PATH_NAME = "lbl_application_path"
BTN_BROWSE_NAME = "btn_browse"
BTN_CONVERT_NAME = "btn_convert"
BOX_NAME = "box"
VERSION_2003 = "2003"
BROWSE = "Browse..."
DIAMANTE_APPLICATION_PATH = "Diamante application path: "
CHOOSE_DIRECTORY = "Choose a directory:"

#@todo: review and comment this file
class DiamanteGui_2004(diamante_gui.DiamanteGui):
    """
    Provides wx widgets that are required to assemble the Diamante 2004 migrator interface
    """    

    product_version = "2004"
    """ The product version of Diamante this plugin supports """

    def __init__(self, parent_plugin):
        diamante_gui.DiamanteGui.__init__(self, parent_plugin)
        self.reset_state()

    def reset_state(self):        
        """
        Resets the object's state to it's initial attributes
        """
        diamante_gui.DiamanteGui.reset_state(self)

    def do_panel(self, panel_structure):
        """
        @see: colony.plugins.diamante_gui.diamante.diamante_gui.do_panel()
        """
        diamante_gui.DiamanteGui.do_panel(self, panel_structure)

        # widget initialization
        panel = panel_structure.panel
        box = panel_structure.get_widget(self.get_plugin_from_product_version(VERSION_2003), BOX_NAME)
        btn_convert = panel_structure.get_widget(self.get_plugin_from_product_version(VERSION_2003), BTN_CONVERT_NAME)
        lbl_application_path = wx.StaticText(panel, wx.ID_ANY, DIAMANTE_APPLICATION_PATH)
        txt_application_path = wx.TextCtrl(panel, wx.ID_ANY, "")
        btn_browse = wx.Button(panel, wx.ID_ANY, BROWSE)
        self.add_widget(btn_browse, BTN_BROWSE_NAME)
        self.add_widget(lbl_application_path, LBL_APPLICATION_PATH_NAME)
        self.add_widget(txt_application_path, TXT_APPLICATION_PATH_NAME)        
        panel_structure.add_widget(self.parent_plugin, lbl_application_path, LBL_APPLICATION_PATH_NAME)
        panel_structure.add_widget(self.parent_plugin, txt_application_path, TXT_APPLICATION_PATH_NAME)
        panel_structure.add_widget(self.parent_plugin, btn_browse, BTN_BROWSE_NAME)
        panel_structure.panel.Bind(wx.EVT_BUTTON, self.btn_browse_onclick, btn_browse )                
        panel_structure.panel.Bind(wx.EVT_TEXT, self.txt_application_path_changed, txt_application_path)
        panel_structure.add_handler(VERSION_2003, BTN_CONVERT_NAME, self.WidgetHandler(self.btn_convert_onclick, False))

        # widget layout
        btn_convert.Enable(False)
        box.Remove(btn_convert)
        box.Add((10,10))
        box.Add(lbl_application_path, 0, wx.ALIGN_CENTER)
        box.Add((10,10))   
        box.Add(txt_application_path, 0, wx.ALIGN_CENTER)
        box.Add((10,10))
        box.Add(btn_browse, 0, wx.ALIGN_CENTER)
        box.Add((10,10))
        box.Add(btn_convert, 0, wx.ALIGN_CENTER)
        panel.SetSizer(box)
        panel.Layout()

    #@todo: Remove redundant code
    def btn_convert_onclick(self, event):
        """
        Event called when the convert button is clicked. Logic plugin is executed.
        
        @param event: Event object sent by the associated wxPython event handler
        """
        widget_handler_list = self.get_handlers_list_event(event)
        if widget_handler_list and not self.is_processable(widget_handler_list):
            self.process_handlers(event)
            return
        self.logic_plugin.run(self.configuration)
        self.process_handlers(event)

    #@todo: Remove redundant code    
    def btn_browse_onclick(self, event):
        """
        Event called when the browse button is clicked. Opens a directory dialog, and sets its result in the application path textbox.
        
        @param event: Event object sent by the associated wxPython event handler
        """
        widget_handler_list = self.get_handlers_list_event(event)
        if widget_handler_list and not self.is_processable(widget_handler_list):
            self.process_handlers(event)
            return
        dlg = wx.DirDialog(self.get_panel(event.GetEventObject()), CHOOSE_DIRECTORY, style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            txt_application_path = self.panel_panel_structures_map[self.get_panel(event.GetEventObject())].get_widget(self.parent_plugin,TXT_APPLICATION_PATH_NAME)
            txt_application_path.SetValue(dlg.GetPath())
        dlg.Destroy()
        self.process_handlers(event)

    #@todo: Remove redundant code
    def txt_application_path_changed(self, event):
        """
        Event called when the application path textbox content changes. If the content is a path to an existing directory, then it is set in the configuration dictionary.
        
        @param event: Event object sent by the associated wxPython event handler
        """

        widget_handler_list = self.get_handlers_list_event(event)
        if widget_handler_list and not self.is_processable(widget_handler_list):
            self.process_handlers(event)
            return
        btn_convert = self.panel_panel_structures_map[self.get_panel(event.GetEventObject())].get_widget(self.get_plugin_from_product_version(VERSION_2003),BTN_CONVERT_NAME)
        if os.path.isdir(event.GetEventObject().GetValue()):
            self.configuration["application_path"] = event.GetEventObject().GetValue()
            btn_convert.Enable(True)
        else:
            btn_convert.Enable(False)
        self.process_handlers(event)
