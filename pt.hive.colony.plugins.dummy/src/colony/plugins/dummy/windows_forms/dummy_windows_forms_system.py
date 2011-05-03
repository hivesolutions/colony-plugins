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

import clr
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")

import System.Drawing.Font
import System.Drawing.Point

import System.Windows.Forms.Form
import System.Windows.Forms.Label
import System.Windows.Forms.Application

FORM_TITLE_TEXT = "Dummy Plugin Windows Forms"

class DummyWindowsForms:

    dummy_plugin_windows_forms = None

    queue = []

    def __init__(self, dummy_plugin_windows_forms):
        self.dummy_plugin_windows_forms = dummy_plugin_windows_forms

    def start(self):
        # creates the form layout
        self.do_layout()

        # sets the idle event handler
        System.Windows.Forms.Application.Idle += self.on_idle

        # notifies the ready semaphore
        self.dummy_plugin_windows_forms.release_ready_semaphore()

        # start the main windows forms event loop and show the main form
        System.Windows.Forms.Application.Run(self.form)

    def do_layout(self):
        self.form = DummyForm()
        self.form.Text = FORM_TITLE_TEXT
        self.label_location = System.Drawing.Point(20, 20)
        self.label_font = System.Drawing.Font("Microsoft Sans Serif", 10)
        self.label = System.Windows.Forms.Label(Text = "Loaded Label Plugins List", Height = 15, Width = 250, Location = self.label_location, Font = self.label_font)

        self.form.Controls.Add(self.label)

    def on_idle(self, sender, args):
        if len(self.queue):
            event_name, args = self.queue.pop(0)
            if event_name == "add_label":
                self.form.add_label(args)
            elif event_name == "remove_label":
                self.form.remove_label(args)

    def stop(self):
        System.Windows.Forms.Application.Exit()

    def get_form(self):
        return self.form

    def add_label(self, label):
        # defines the add label tuple
        add_label_tuple = (
            "add_label",
            label
        )

        # adds the adda label tuple to the queue
        self.queue.append(add_label_tuple)

        # invalidates the form
        self.form.Invalidate()

    def remove_label(self, label):
        # defines the remove label tuple
        remove_label_tuple = (
            "remove_label",
            label
        )

        # adds the remove label tuple to the queue
        self.queue.append(remove_label_tuple)

        # invalidates the form
        self.form.Invalidate()

class DummyForm(System.Windows.Forms.Form):

    current_position = (40, 40)

    def add_label(self, label):
        current_position_x, current_position_y = self.current_position
        label_location = System.Drawing.Point(current_position_x, current_position_y)
        self.current_position = (current_position_x, current_position_y + 20)
        label.Location = label_location
        self.Controls.Add(label)

    def remove_label(self, label):
        self.Controls.Remove(label)
