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

MESSAGING_SERVICE_ID = "email"
""" The messaging service id """

class EmailMessagingExtension:
    """
    The email messaging extension class.
    """

    email_messaging_extension_plugin = None
    """ The email messaging extension plugin """

    def __init__(self, email_messaging_extension_plugin):
        """
        Constructor of the class.

        @type email_messaging_extension_plugin: EmailMessagingExtensionPlugin
        @param email_messaging_extension_plugin: The email messaging extension plugin.
        """

        self.email_messaging_extension_plugin = email_messaging_extension_plugin

    def get_messaging_service_id(self):
        """
        Retrieves the messaging service id.

        @rtype: String
        @return: The messaging service id.
        """

        return MESSAGING_SERVICE_ID

    def send_message(self, message_attributes):
        """
        Sends a message using the given message attributes.

        @type message_attributes: Dictionary
        @param message_attributes: The attributes of the message to
        be sent.
        """

        # retrieves the email plugin
        email_plugin = self.email_messaging_extension_plugin.email_plugin

        # retrieves the email of the message sender
        email_sender = message_attributes["email_sender"]

        # retrieves the email of the message receiver
        email_receiver = message_attributes["email_receiver"]

        # retrieves the name of the message sender
        name_sender = message_attributes["name_sender"]

        # retrieves the name of the message receiver
        name_receiver = message_attributes["name_receiver"]

        # retrieves the subject part of the message
        subject = message_attributes["subject"]

        # retrieves the text part of the message
        contents = message_attributes["text"]

        # sends the email message
        email_plugin.send_email(email_sender, email_receiver, name_sender, name_receiver, subject, contents, "hive.pt", "joamag", "cdnosap0zg6t")
