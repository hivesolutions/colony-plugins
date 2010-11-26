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

HANDLER_NAME = "database"
""" The handler name """

class MainServiceSmtpDatabaseMessageHandler:
    """
    The main service smtp database message handler class.
    """

    main_service_smtp_database_message_handler_plugin = None
    """ The main service smtp database message handler plugin """

    def __init__(self, main_service_smtp_database_message_handler_plugin):
        """
        Constructor of the class.

        @type main_service_smtp_database_message_handler_plugin: MainServiceSmtpDatabaseMessageHandlerPlugin
        @param main_service_smtp_database_message_handler_plugin: The main service smtp database message handler plugin.
        """

        self.main_service_smtp_database_message_handler_plugin = main_service_smtp_database_message_handler_plugin

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_message(self, message, arguments):
        """
        Handles the given smtp message.

        @type message: SmtpMessage
        @param message: The smtp message to handled.
        @type arguments: Dictionary
        @param arguments: The arguments to the message handling.
        """

        # retrieves the mail storage database plugin
        mail_storage_database_plugin = self.main_service_smtp_database_message_handler_plugin.mail_storage_database_plugin

        # creates the mail storage database client
        mail_storage_database_client = mail_storage_database_plugin.create_client(arguments)

        # retrieves the contents
        contents = message.get_contents()

        # retrieves the recipients list
        recipients_list = message.get_recipients_list()

        # iterates over all recipients in the recipients list
        # to check the domain
        for recipient in recipients_list:
            # splits the recipient retrieving the
            # user and the domain
            user, _domain = recipient.split("@")

            # saves the message in the database
            mail_storage_database_client.save_message(user, contents)
