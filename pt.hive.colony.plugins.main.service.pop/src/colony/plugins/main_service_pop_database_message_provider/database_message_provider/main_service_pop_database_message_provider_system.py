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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

PROVIDER_NAME = "database"
""" The provider name """

class MainServicePopDatabaseMessageProvider:
    """
    The main service pop database message provider class.
    """

    main_service_pop_database_message_provider_plugin = None
    """ The main service pop database message provider plugin """

    def __init__(self, main_service_pop_database_message_provider_plugin):
        """
        Constructor of the class.

        @type main_service_pop_database_message_provider_plugin: MainServicePopDatabaseMessageProviderPlugin
        @param main_service_pop_database_message_provider_plugin: The main service pop database message provider plugin.
        """

        self.main_service_pop_database_message_provider_plugin = main_service_pop_database_message_provider_plugin

    def get_provider_name(self):
        """
        Retrieves the provider name.

        @rtype: String
        @return: The provider name.
        """

        return PROVIDER_NAME

    def provide_message_client(self, arguments):
        """
        Provides the message client.

        @type arguments: Dictionary
        @param arguments: The arguments to the message client.
        @rtype: MessageClient
        @return: The message client.
        """

        # retrieves the mail storage database plugin
        mail_storage_database_plugin = self.main_service_pop_database_message_provider_plugin.mail_storage_database_plugin

        # creates the mail storage database client
        mail_storage_database_client = mail_storage_database_plugin.create_client(arguments)

        # returns the mail storage database client
        return mail_storage_database_client
