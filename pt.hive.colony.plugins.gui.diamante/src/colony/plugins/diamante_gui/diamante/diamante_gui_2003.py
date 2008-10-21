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
import os

import diamante_gui

BTN_CONVERT_NAME = "btn_convert"
CONVERT = "Convert"
BOX = "box"

#@todo: review and comment this file
class DiamanteGui_2003(diamante_gui.DiamanteGui):

    product_version = "2003"
    """ The product version of Diamante this plugin supports """

    def __init__(self, parent_plugin):
        diamante_gui.DiamanteGui.__init__(self, parent_plugin)
        self.reset_state()

    def reset_state(self):
        """
        Resets the object's state to it's initial attributes
        """

        diamante_gui.DiamanteGui.reset_state(self)
        self.configuration = {}
        self.logic_plugin = None

    def do_panel(self, panel_structure):
        """
        @see: colony.plugins.diamante_gui.diamante.diamante_gui.do_panel()
        """

        diamante_gui.DiamanteGui.do_panel(self, panel_structure)

        # widget initialization
        panel = panel_structure.panel
        box = wx.BoxSizer(wx.HORIZONTAL)
        btn_convert = wx.Button(panel, wx.ID_ANY, CONVERT)
        self.add_widget(btn_convert, BTN_CONVERT_NAME)
        panel_structure.add_widget(self.parent_plugin, btn_convert, BTN_CONVERT_NAME)
        panel_structure.add_widget(self.parent_plugin, box, BOX)
        panel_structure.panel.Bind(wx.EVT_BUTTON, self.btn_convert_onclick, btn_convert )

        # widget layout
        box.Add((10,10))   
        box.Add(btn_convert, 0, wx.ALIGN_CENTER)
        panel.SetSizer(box)
        panel.Layout()
        panel.SetupScrolling()

    #@todo: Remove redundant code
    def btn_convert_onclick(self, event):
        """
        Event called when the convert button is clicked
        
        @param event: Event object sent by the associated wxPython event handler
        """

        widget_handler_list = self.get_handlers_list_event(event)
        if widget_handler_list and not self.is_processable(widget_handler_list):
            self.process_handlers(event)
            return
        self.configuration["diamante_path"] = "C:/reverse/DIA2002/"
        self.configuration["query_type"] = "convert"
        self.configuration["input_adapter_plugin_id"] = "pt.hive.colony.plugins.adapters.input"
        self.configuration["output_adapter_plugin_id"] = "pt.hive.colony.plugins.adapters.output"
        self.configuration["work_units"] = ["customer"]
        self.parent_plugin.gui_manager_plugin.process_query(self.configuration)
        #self.logic_plugin.run(self.configuration)
        self.process_handlers(event)
