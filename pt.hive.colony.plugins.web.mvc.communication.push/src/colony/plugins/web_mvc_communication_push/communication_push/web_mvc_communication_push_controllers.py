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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class WebMvcCommunicationPushController:
    """
    The web mvc communication push controller.
    """

    web_mvc_communication_push_plugin = None
    """ The web mvc communication push plugin """

    web_mvc_communication_push = None
    """ The web mvc communication push """

    def __init__(self, web_mvc_communication_push_plugin, web_mvc_communication_push):
        """
        Constructor of the class.

        @type web_mvc_communication_push_plugin: WebMvcCommunicationPushPlugin
        @param web_mvc_communication_push_plugin: The web mvc communication push plugin.
        @type web_mvc_communication_push: WebMvcCommunicationPush
        @param web_mvc_communication_push: The web mvc communication push.
        """

        self.web_mvc_communication_push_plugin = web_mvc_communication_push_plugin
        self.web_mvc_communication_push = web_mvc_communication_push

    def handle_show(self, rest_request, parameters = {}):
        return True

    def handle_register(self, rest_request, parameters = {}):
        # returns true
        return True

    def handle_unregister(self, rest_request, parameters = {}):
        # returns true
        return True

    def handle_broadcast(self, rest_request, parameters = {}):
        # returns true
        return True
