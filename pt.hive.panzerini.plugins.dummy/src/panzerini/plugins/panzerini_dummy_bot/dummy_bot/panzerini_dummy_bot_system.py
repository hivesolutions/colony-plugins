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

__author__ = "Jo�o Magalh�es <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

BOT_NAME = "dummy"
""" The bot name """

class PanzeriniDummyBot:
    """
    The panzerini dummy bot class.
    """

    panzerini_dummy_bot_plugin = None
    """ The panzerini dummy bot plugin """

    def __init__(self, panzerini_dummy_bot_plugin):
        """
        Constructor of the class.

        @type panzerini_dummy_bot_plugin: PanzeriniDummyBotPlugin
        @param panzerini_dummy_bot_plugin: The panzerini dummy logic plugin.
        """

        self.panzerini_dummy_bot_plugin = panzerini_dummy_bot_plugin

    def get_bot_name(self):
        return BOT_NAME

    def tick(self, panzer):
        # creates a new list for the panzer actions
        panzer_actions = []

        # adds the accelerate action
        panzer_actions.append("accelerate")
