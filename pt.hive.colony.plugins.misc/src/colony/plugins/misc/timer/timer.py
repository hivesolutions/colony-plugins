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

__revision__ = "$LastChangedRevision: 2096 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 13:02:08 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time

class Timer:
    """
    Provides time monitoring functions
    """

    start_timestamp = 0
    """ Timestamp of when the start() method was invoked """

    stop_timestamp = 0
    """ Timestamp of when the stop() method was invoked """

    parent_plugin = None
    """ Reference to the plugin that owns this code """

    def __init__(self, parent_plugin):
        self.parent_plugin = parent_plugin

    def start(self):
        """
        Starts the stopwatch
        """
        self.start_timestamp = time.time()
        return self.start_timestamp

    def stop(self):
        """
        Stops the stopwatch
        """
        self.stop_timestamp = time.time()
        return self.stop_timestamp

    def get_time_elapsed(self):
        """
        Returns the time between when start() and stop() calls
        """
        return self.stop_timestamp - self.start_timestamp
