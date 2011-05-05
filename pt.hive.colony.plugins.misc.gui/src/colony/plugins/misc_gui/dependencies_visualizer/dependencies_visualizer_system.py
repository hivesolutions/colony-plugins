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
import copy

SQUARE_SIZE = 150
COLORS = [
    wx.RED,
    wx.GREEN,
    wx.BLUE,
    wx.BLACK
]

#@todo: review and comment this file
class DependenciesVisualizer:

    dependencies_visualizer_plugin = None

    draw_panel = None
    graph = None

    def __init__(self, dependencies_visualizer_plugin):
        self.dependencies_visualizer_plugin = dependencies_visualizer_plugin

    def get_graph(self):
        if not self.graph:
            manager = self.dependencies_visualizer_plugin.manager
            dependencies_calculator_plugin = self.dependencies_visualizer_plugin.dependencies_calculator_plugin
            plugin_instances_list = manager.get_all_plugins()
            self.graph = dependencies_calculator_plugin.generate_graph(plugin_instances_list)
        return self.graph

    def do_panel(self, parent):
        graph = self.get_graph()
        self.draw_panel = DrawPanel(parent, graph)
        return self.draw_panel

class DrawPanel(wx.Panel):

    drag_image = None
    drag_shape = None
    hilite_shape = None
    drag_shape_list = []

    def __init__(self, parent, graph = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.SetBackgroundColour(wx.WHITE)
        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.drag_shape_list = []

        # creates the shapes
        self.create_shapes(graph)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)

    def create_shapes(self, graph):
        rectangle = wx.Rect(0,0, SQUARE_SIZE, SQUARE_SIZE)

        position = [
            0, 0
        ]

        for color in COLORS:
            dc, graphic_dc, bitmap = self.create_dc_gdc_bitmap()
            pen_color = color
            brush_color = color
            graphic_dc.SetPen(wx.Pen(pen_color))
            graphic_dc.SetBrush(wx.Brush(brush_color))
            # draws the rectangle into the bpm dg
            graphic_dc.DrawRoundedRectangleRect(rectangle, 8)
            self.close_dc_gdc_bitmap(dc, graphic_dc, bitmap)

            drag_shape = DragShape(bitmap)
            self.drag_shape_list.append(drag_shape)
            drag_shape.position = copy.copy(position)

            # increments the positions
            position[0] += 50
            position[1] += 50

    def create_dc_gdc_bitmap(self):
        # creates a bitmap the same size as our text
        bitmap = wx.EmptyBitmap(SQUARE_SIZE, SQUARE_SIZE, 32)

        # creates a new memory dc
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(bitmap)
        mem_dc.Clear()

        try:
            graphic_dc = wx.GCDC(mem_dc)
        except:
            graphic_dc = mem_dc

        return (
            mem_dc,
            graphic_dc,
            bitmap
        )

    def close_dc_gdc_bitmap(self, dc, gdc, bitmap):
        dc.SelectObject(wx.NullBitmap)
        bitmap.SetMaskColour(wx.WHITE)

    def find_shape(self, position):
        for drag_shape in self.drag_shape_list:
            if drag_shape.hit_test(position):
                return drag_shape

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        for drag_shape in self.drag_shape_list:
            if drag_shape.shown:
                drag_shape.draw(dc)

    def on_left_down(self, event):
        # did the mouse go down on one of our shapes ?
        shape = self.find_shape(event.GetPosition())

        # in case a shape was "hit"
        if shape:
            self.drag_shape = shape
            self.drag_start_position = event.GetPosition()

    def on_left_up(self, event):
        if not self.drag_image or not self.drag_shape:
            self.drag_image = None
            self.drag_shape = None
            return

        # hide the image, end dragging, and clear out the drag image
        self.drag_image.Hide()
        self.drag_image.EndDrag()
        self.drag_image = None

        if self.hilite_shape:
            self.RefreshRect(self.hilite_shape.get_rectangle())
            self.hilite_shape = None

        self.drag_shape.position = (self.drag_shape.position[0] + event.GetPosition()[0] - self.drag_start_position[0],
                                    self.drag_shape.position[1] + event.GetPosition()[1] - self.drag_start_position[1])

        self.drag_shape.shown = True
        self.RefreshRect(self.drag_shape.get_rectangle())
        self.drag_shape = None

    def on_motion(self, event):
        # ignore mouse movement if we're not dragging.
        if not self.drag_shape or not event.Dragging() or not event.LeftIsDown():
            return

        # if we have a shape, but haven't started dragging yet
        if self.drag_shape and not self.drag_image:

            # only start the drag after having moved a couple pixels
            tolerance = 2
            position = event.GetPosition()
            delta_x = abs(position.x - self.drag_start_position.x)
            delta_y = abs(position.y - self.drag_start_position.y)
            if delta_x <= tolerance and delta_y <= tolerance:
                return

            # refresh the area of the window where the shape was so it
            # will get erased.
            self.drag_shape.shown = False
            self.RefreshRect(self.drag_shape.get_rectangle(), True)
            self.Update()

            if self.drag_shape.text:
                self.drag_image = wx.DragString(self.drag_shape.text, wx.StockCursor(wx.CURSOR_HAND))
            else:
                self.drag_image = wx.DragImage(self.drag_shape.bitmap, wx.StockCursor(wx.CURSOR_HAND))

            hotspot = self.drag_start_position - self.drag_shape.position
            self.drag_image.BeginDrag(hotspot, self, self.drag_shape.fullscreen)

            self.drag_image.Move(position)
            self.drag_image.Show()

        # if we have shape and image then move it, possibly highlighting another shape
        elif self.drag_shape and self.drag_image:
            on_shape = self.find_shape(event.GetPosition())
            unhilite_old = False
            hilite_new = False

            # figure out what to highlight and what to unhighlight
            if self.hilite_shape:
                if on_shape == None or not self.hilite_shape == on_shape:
                    unhilite_old = True

            if on_shape and on_shape is not self.hilite_shape and on_shape.shown:
                hilite_new = True

            # if needed, hide the drag image so we can update the window
            if unhilite_old or hilite_new:
                self.drag_image.Hide()

            if unhilite_old:
                dc = wx.ClientDC(self)
                self.hilite_shape.draw(dc)
                self.hilite_shape = None

            if hilite_new:
                dc = wx.ClientDC(self)
                self.hilite_shape = on_shape
                self.hilite_shape.draw(dc, wx.INVERT)

            # now move it and show it again if needed
            self.drag_image.Move(event.GetPosition())
            if unhilite_old or hilite_new:
                self.drag_image.Show()

class DragShape:

    bitmap = None
    position = None
    shown = True
    text = None
    fullscreen = False

    def __init__(self, bitmap):
        self.bitmap = bitmap
        self.position = (0,0)
        self.shown = True
        self.text = None
        self.fullscreen = False

    def hit_test(self, position):
        rectangle = self.get_rectangle()
        return rectangle.InsideXY(position.x, position.y)

    def get_rectangle(self):
        return wx.Rect(self.position[0], self.position[1],
                      self.bitmap.GetWidth(), self.bitmap.GetHeight())

    def draw(self, dc, operation = wx.COPY):
        if self.bitmap.Ok():
            mem_dc = wx.MemoryDC()
            mem_dc.SelectObject(self.bitmap)

            dc.Blit(self.position[0], self.position[1],
                    self.bitmap.GetWidth(), self.bitmap.GetHeight(),
                    mem_dc, 0, 0, operation, True)

            return True
        else:
            return False

class GraphNodeDragShape(DragShape):

    def __init__(self, bitmap, graph_node):
        DragShape.__init__(self, bitmap)
