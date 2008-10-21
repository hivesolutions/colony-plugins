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

__revision__ = "$LastChangedRevision: 2114 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 15:29:05 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

STATUS_NONE = 0
STATUS_RESUMING = 1
STATUS_RUNNING = 2
STATUS_PAUSING = 3
STATUS_PAUSED = 4
STATUS_STOPPING = 5
STATUS_STOPPED = 6

#@todo: review and comment this file

class TaskProgressInformationItem:

    task = None
    task_id = 0
    task_name = "none"
    status_message = "none"
    task_description = "none"
    current_description = "none"

    percentage_complete = 0
    status = STATUS_RUNNING

    status_changed_handlers_list = []
    panel = None

    def __init__(self, task = None, task_progress_information_id = 0, task_name = "none", task_description = "none", current_description = "none", percentage_complete = 0, status = STATUS_RUNNING, panel = None):
        self.task = task
        self.task_progress_information_id = task_progress_information_id
        self.task_name = task_name
        self.task_description = task_description
        self.current_description = current_description
        self.percentage_complete = percentage_complete
        self.status = status
        self.panel = panel
        
        self.status_changed_handlers_list = []

    def set_task_name(self, task_name):
        self.task_name = task_name
        self.panel.update_task_name()

    def get_task_name(self):
        return self.task_name

    def set_status_message(self, status_message):
        self.status_message = status_message
        self.panel.update_status_message()

    def get_status_message(self):
        return self.status_message

    def set_task_description(self, task_description):
        self.task_description = task_description
        self.panel.update_task_description()

    def get_task_description(self):
        return self.task_description

    def get_percentage_complete(self):
        return self.percentage_complete

    def set_percentage_complete(self, value):
        self.percentage_complete = value
        self.panel.update_value_gauge_value()

    def get_percentage_complete(self):
        return self.percentage_complete

    def set_status(self, status):
        if self.status == status:
            return

        if status == STATUS_NONE:
            pass
        elif status == STATUS_RESUMING:
            self.set_status_message("Resuming...")
        elif status == STATUS_RUNNING:
            self.set_status_message("Running")
        elif status == STATUS_PAUSING:
            self.set_status_message("Pausing...")
        elif status == STATUS_PAUSED:
            self.set_status_message("Paused")
        elif status == STATUS_STOPPING:
            self.set_status_message("Stopping...")
        elif status == STATUS_STOPPED:
            self.set_status_message("Stopped")

        self.panel.update_task_status(status)    
        self.status = status

    def get_status(self):
        return self.status

    def add_status_changed_handler(self, status_changed_handler):
        self.status_changed_handlers_list.append(status_changed_handler)

    def remove_status_changed_handler(self, status_changed_handler):
        self.status_changed_handlers_list.remove(status_changed_handler)

    def notify_all_status_changed_handlers(self, event, args):
        for status_changed_handler in self.status_changed_handlers_list:
            status_changed_handler(event, args)
