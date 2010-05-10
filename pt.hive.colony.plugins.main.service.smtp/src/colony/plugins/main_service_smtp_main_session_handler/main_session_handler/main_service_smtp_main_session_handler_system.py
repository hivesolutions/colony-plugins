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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

HANDLER_NAME = "main"
""" The handler name """

class MainServiceSmtpMainSessionHandler:
    """
    The main service smtp main session handler class.
    """

    main_service_smtp_main_session_handler_plugin = None
    """ The main service smtp main session handler plugin """

    smtp_service_message_handler_plugins_map = {}
    """ The smtp service message handler plugins map """

    def __init__(self, main_service_smtp_main_session_handler_plugin):
        """
        Constructor of the class.

        @type main_service_smtp_main_session_handler_plugin: MainServiceSmtpMainSessionHandlerPlugin
        @param main_service_smtp_main_session_handler_plugin: The main service smtp main session handler plugin.
        """

        self.main_service_smtp_main_session_handler_plugin = main_service_smtp_main_session_handler_plugin

        self.smtp_service_message_handler_plugins_map = {}

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_session(self, session, properties):
        """
        Handles the given smtp session.

        @type session: SmtpSession
        @param session: The session to be handled.
        @type properties: Dictionary
        @param properties: The properties for the session handling.
        """

        # retrieves the messages from the session
        messages = session.get_messages()

        # iterates over all the messages
        for message in messages:
            # retrieves the recipients list
            recipients_list = message.get_recipients_list()

            # unsets the relay message flag
            relay_message = False

            # iterates over all recipients in the recipients list
            # to check the domain
            for recipient in recipients_list:
                # splits the recipient retrieving the
                # user and the domain
                _user, domain = recipient.split("@")

                if not domain == "hive.pt":
                    # sets the relay message flag
                    relay_message = True

            # in case the relay message is set
            if relay_message:
                self.smtp_service_message_handler_plugins_map["relay"].handle_message(message)
            else:
                self.smtp_service_message_handler_plugins_map["database"].handle_message(message)

    def smtp_service_message_handler_load(self, smtp_service_message_handler_plugin):
        # retrieves the plugin handler name
        message_handler_name = smtp_service_message_handler_plugin.get_handler_name()

        self.smtp_service_message_handler_plugins_map[message_handler_name] = smtp_service_message_handler_plugin

    def smtp_service_message_handler_unload(self, smtp_service_message_handler_plugin):
        # retrieves the plugin handler name
        message_handler_name = smtp_service_message_handler_plugin.get_handler_name()

        del self.smtp_service_message_handler_plugins_map[message_handler_name]
