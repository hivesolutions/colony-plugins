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

__revision__ = "$LastChangedRevision: 2107 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 15:06:41 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import wx

#@todo: review and comment this file
class DiamanteGui:
    """
    Class inherited by the base code of all widget plugins
    """

    product_version = None
    """ The product version of Diamante this plugin supports """
    configuration = {}
    """ User specified settings (filled by widget events) """
    panel_panel_structures_map = {}
    """ Dictionary associating panels with their respective panel structure objects """
    own_panel_structures = []
    """ A list of the panel structures that belong to this plugin """
    name_widget_map = {}
    """ Dictionary associating the name of a widget with its instance """
    widget_name_map = {}
    """ Dictionary associating an widget instance with the widget name """
    parent_plugin = None
    """ Reference to the plugin that is invoking this base code """ 
    
    class WidgetHandler:
        """
        Encodes custom event handling information for a widget
        """
        handler = None
        """ Reference to a function """
        propagate = True
        """ Boolean indicating if the next widget handler should also be called """

        def __init__(self, handler, propagate = True):
            self.handler = handler
            self.propagate = propagate

    def __init__(self, parent_plugin):
        self.reset_state()
        self.parent_plugin = parent_plugin

    def reset_state(self):
        """
        Resets the object's state to it's initial attributes
        """

        for panel_structure in self.own_panel_structures:
            for plugin, widgets_list in panel_structure.plugin_widgets_map.iteritems():
                for widget in widgets_list:
                    if isinstance(widget,wx.Control):
                        widget.Hide()
                        widget.Destroy()
        self.configuration = {}
        self.panel_panel_structures_map = {}
        self.own_panel_structures = []
        self.name_widget_map = {}
        self.widget_name_map = {}

    def add_widget(self, widget, widget_name):
        """
        Adds information about the widget to the plugins dictionaries
        
        @param widget: A widget instance
        @param widget_name: The string identification of the provided widget instance
        """

        self.widget_name_map[widget] = widget_name
        self.name_widget_map[widget_name] = widget

    def process_handlers(self, event):
        """
        Processes the event handlers linked to a certain event
        
        @param event: The event for which the linked event handlers should be processed
        """

        widget_handler_list = self.get_handlers_list_event(event)
        
        if not widget_handler_list:
            return

        for widget_handler in widget_handler_list:
            if self.is_processable(widget_handler_list, widget_handler):
                widget_handler.handler(event)

    def get_plugin_from_product_version(self, product_version):
        """
        Retrieves a widget plugin by the product version it supports
        
        @param product_version: Product version supported by the required plugin
        @return: The requested plugin instance
        """

        for plugin in self.parent_plugin.widget_plugins:
            if plugin.get_product_version() == product_version:
                return plugin

    def do_panel(self, panel_structure):
        """
        Contributes widgets and events to the provided panel structure
        
        @param panel_structure: PanelStructure object containing all the necessary information for 
                                this plugin to be able to contribute its widgets and events
        """

        panel = panel_structure.panel
        
        self.panel_panel_structures_map[panel] = panel_structure

        if panel_structure.plugin == self.parent_plugin:
            self.own_panel_structures.append(panel_structure)

        for widget_plugin in self.parent_plugin.widget_plugins:
            widget_plugin.do_panel(panel_structure)

    # @todo: Document this function better
    def is_processable(self, widget_handler_list, widget_handler = None):
        """
        Indicates if the event handler list should continue being processed
        
        @param widget_handler_list: List of event handlers  
        @param widget_handler: A widget event handler
        @return: Returns true if an widget event handler is in the list
        """

        widget_handler_list.reverse()
        for widget_handler_element in widget_handler_list:
            if widget_handler_element == widget_handler:
                return True
            if not widget_handler_element.propagate:
                return False
        return True

    def get_panel(self, widget):
        """
        Retrieves the panel that is parent to a certain widget
        
        @param widget: A widget instance
        @return: Instance of the panel that is parent to the provided widget
        """

        current_widget = widget
        while not isinstance(current_widget, wx.Panel) and current_widget:
            current_widget = current_widget.GetParent()
        return current_widget

    #@todo: Document better
    def get_handlers_list_event(self, event):
        """
        Returns a list of event handlers that follow a certain event
        
        @param event: Event object
        @return: List of event handlers that follow the given event
        """

        panel = self.get_panel(event.GetEventObject())
        panel_structure = self.panel_panel_structures_map[panel]
        widget_handlers_map = panel_structure.get_handlers_product_version(self.product_version)      
        widget = event.GetEventObject()
        if not widget in self.widget_name_map:
            return
        widget_name = self.widget_name_map[widget]
        if not widget_name in widget_handlers_map:
            return
        widget_handler_list = widget_handlers_map[widget_name]  
        return widget_handler_list

    def run(self):
        return
