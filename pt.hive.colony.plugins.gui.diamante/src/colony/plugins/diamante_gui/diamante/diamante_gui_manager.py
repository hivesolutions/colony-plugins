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
import wx.lib.scrolledpanel

#@todo: review and comment this file    
class Event:
    """
    Stores all the properties that define an a custom event
    """

    event_type = None
    """ The type of event """
    handler = None
    """ An optional handler to a function (used when the event_type = call) """
    arguments = []
    """ An optional argument list for a function (used when the event_type = call) """

    def __init__(self, event_type, handler = None, arguments = []):
        self.event_type = event_type
        self.handler = handler
        self.arguments = arguments

class PanelStructure:
    """
    Provides all the necessary information to manipulate a certain graphical user interface
    """

    panel = None
    """ Reference to the panel that contains the widget for the gui it represents """
    plugin = None
    """ Plugin that owns this graphical user interface """
    plugin_widgets_map = {}
    """ Dictionary associating plugins that contribute components to the gui, with a list of the provided widgets themselves """
    #@todo: Rename to plugin_widgetname_map
    plugin_name_widget_map = {}
    """ Dictionary associating plugins that contribute components to the gui, with a list of names from the provided widgets themselves """
    #@todo: Rename to productversion_handler_map 
    handlers = {}
    """ Dictionary associating product version with a list of event handlers """

    def __init__(self, panel = None, plugin = None):
        self.panel = panel
        self.plugin = plugin
        self.plugin_widgets_map = {}
        self.plugin_name_widget_map = {}
        self.handlers = {}

    def add_widget(self, plugin, widget, widget_name):
        """
        Adds a widget to this panel structure
        
        @param plugin: Plugin responsible for contributing this widget
        @param widget: Instance of the widget (graphical component)
        @param widget_name: String identification of the widget
        """

        if not plugin in self.plugin_widgets_map:
            self.plugin_widgets_map[plugin] = []
        if not plugin in self.plugin_name_widget_map:
            self.plugin_name_widget_map[plugin] = {}
        if not widget_name in self.plugin_name_widget_map[plugin]:
            self.plugin_name_widget_map[plugin][widget_name] = widget
        self.plugin_widgets_map[plugin].append(widget)

    def get_widget(self, plugin, widget_name):
        """
        Gets a reference to widget instance given its name and parent plugin
        
        @param plugin: Reference to the plugin instance that provided the widget
        @param widget_name: String identification of the widget one wants to retrieve
        @return: Requested widget instance
        """

        return self.plugin_name_widget_map[plugin][widget_name]

    def add_handler(self, product_version, widget_name, handler):
        """
        Associates and event handler to a certain widget and version
        
        @param product_version: Product version of the GUI where this event should be triggered
        @param widget_name: Name of the widget one wants to have bind an event to
        @param handler: An Event object
        """

        if not product_version in self.handlers:
            self.handlers[product_version] = {}
        if not widget_name in self.handlers[product_version]:
            self.handlers[product_version][widget_name] = []
        self.handlers[product_version][widget_name].insert(0, handler)

    def get_handlers_product_version(self, product_version):
        """
        Returns a dictionary of event handlers for a given product version
        
        @param product_version: Product version of the GUI from which to take the event handlers 
        @return: Dictionary of event handlers in a widget->event format
        """

        if product_version in self.handlers:
            widget_handlers_map = self.handlers[product_version]
        else:
            widget_handlers_map = {}
        return widget_handlers_map
 
class DiamanteGuiManager:

    #@todo: Change to tabname_panel_map
    panels = {}
    """ Dictionary associating tab ids with their respective inner panels """
    event_queue = []
    """ List of events to be processed when the interface is idle """

    parent_plugin = None

    def __init__(self, parent_plugin):
        self.parent_plugin = parent_plugin

    def process_event_queue(self):
        """
        Processes the whole event queue when called
        """
        while len(self.event_queue):
            stored_event = self.event_queue.pop(0)
            if stored_event.event_type == "call":
                stored_event.handler(stored_event.arguments)

    def on_idle(self, event):
        """
        Processes the whole event queue when called
        
        @param event: Event object sent by the associated wxPython event handler
        """
        self.process_event_queue()

    def layout(self, arguments):
        """
        Does the layout for a specified product and version's interface
        
        @param arguments: List of arguments provided by a the event queue handler (should contain 1 argument, a panel structure) 
        """
        panel_structure = arguments[0]
        panel_structure.plugin.do_panel(panel_structure)

    def get_available_gui_versions(self):
        """
        Returns a list with the versions of the available GUI widget plugins 
        
        @return: A list filled with the versions of Diamante whose interfaces can be composed with the available widget plugins
        """
        list_versions = []
        for plugin in self.parent_plugin.widget_plugins:
            list_versions.append(plugin.get_product_version())
        return list_versions

#    def get_user_settings(self, logic_version):
#        """
#        Returns a map with the sum of the user settings specified by all the GUI widget 
#        plugins that compose the interface to the provided logic version
#        
#        @param logic_version: ID of the logic plugin whose settings specified by the user you want to retrieve  
#        @return: Dictionary object with the specified user settings
#        """
#        user_settings = {}
#        for widgets_plugin in self.widget_plugins:
#            for key in widgets_plugin.configuration:
#                user_settings[key] = widgets_plugin.configuration[key]
#        return user_settings       

    def get_widget_plugin(self, product_version):
        """
        Returns the widget plugin that provides the necessary graphical components for a certain product version's interface
        
        @param product_version: Product version supported by the interface one is refering to
        @return: Instance of the requested widget plugin
        """
        for widget_plugin in self.parent_plugin.widget_plugins:
            if widget_plugin.get_product_version() == product_version:
                return widget_plugin

    def do_panel(self, parent, logic_version, tab_name = "none"):
        """
        Creates a panel that will hold the interface for a certain Diamante version
        
        @param parent: Parent wxPython control to which the panel will be bound to
        @param logic_version: Version of the migration logic the created panel will be bound to
        @param tab_name: String identification of the tab that will contain the created panel
        
        @return: Returns the created panel
        """
        panel = wx.lib.scrolledpanel.ScrolledPanel(parent, wx.ID_ANY, style = wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)
        self.panels[tab_name] = panel
        plugin = self.get_widget_plugin(logic_version)
        panel_structure = PanelStructure(panel, plugin)
        panel.Bind(wx.EVT_IDLE, self.on_idle)
        self.event_queue.append(Event("call", self.layout, [panel_structure]))

        return self.panels[tab_name]

    def process_query(self, args):
        self.parent_plugin.main_logic_plugin.process_query(args)
