#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 1089 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-01-22 23:19:39 +0000 (qui, 22 Jan 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import javax.swing

class DummySwing:
    """
    The dummy swing class.
    """

    dummmy_swing_plugin = None
    """ The dummy swing plugin """

    main_frame = None
    """ The main frame """

    def __init__(self, dummmy_swing_plugin):
        """
        Constructor of the class

        @type dummmy_swing_plugin: DummySwingPlugin
        @param dummmy_swing_plugin: The dummy swing plugin.
        """

        self.dummmy_swing_plugin = dummmy_swing_plugin

    def start(self):
        self.main_frame = javax.swing.JFrame("Dummy Swing")
        label = javax.swing.JLabel("Hello Colony!", javax.swing.JLabel.CENTER)
        self.main_frame.add(label)
        self.main_frame.setDefaultCloseOperation(javax.swing.JFrame.EXIT_ON_CLOSE)
        self.main_frame.setSize(300, 300)
        self.main_frame.show()

    def stop(self):
        self.main_frame.dispose()
