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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

MESSAGING_SERVICE_ID = "stdout"
""" The messaging service id """

class StdoutMessagingExtension:
    """
    The stdout messaging extension class.
    """

    stdout_messaging_extension_plugin = None
    """ The stdout messaging extension plugin """

    def __init__(self, stdout_messaging_extension_plugin):
        """
        Constructor of the class.

        @type stdout_messaging_extension_plugin: StdoutMessagingExtensionPlugin
        @param stdout_messaging_extension_plugin: The stdout messaging extension plugin.
        """

        self.stdout_messaging_extension_plugin = stdout_messaging_extension_plugin

    def get_messaging_service_id(self):
        """
        Retrieves the messaging service id.

        @rtype: String
        @return: The messaging service id.
        """

        return MESSAGING_SERVICE_ID

    def send_message(self, message_attributes):
        """
        Retrieves the messaging service id.

        @rtype: String
        @return: The messaging service id.
        """

        # retrieves the text part of the message
        message_text = message_attributes["text"]

        # prints the message text to the stdout
        print message_text
