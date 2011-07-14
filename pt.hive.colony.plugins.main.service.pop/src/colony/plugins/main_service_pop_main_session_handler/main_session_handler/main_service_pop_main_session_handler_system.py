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

import main_service_pop_main_session_handler_exceptions

HANDLER_NAME = "main"
""" The handler name """

MESSAGE_PROVIDER_VALUE = "message_provider"
""" The message provider value """

ARGUMENTS_VALUE = "arguments"
""" The arguments value """

class MainServicePopMainSessionHandler:
    """
    The main service pop main session handler class.
    """

    main_service_pop_main_session_handler_plugin = None
    """ The main service pop main session handler plugin """

    pop_service_message_provider_plugins_map = {}
    """ The pop service message provider plugins map """

    def __init__(self, main_service_pop_main_session_handler_plugin):
        """
        Constructor of the class.

        @type main_service_pop_main_session_handler_plugin: MainServicePopMainSessionHandlerPlugin
        @param main_service_pop_main_session_handler_plugin: The main service pop main session handler plugin.
        """

        self.main_service_pop_main_session_handler_plugin = main_service_pop_main_session_handler_plugin

        self.pop_service_message_provider_plugins_map = {}

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_session(self, session, properties):
        """
        Handles the given pop session.

        @type session: PopSession
        @param session: The session to be handled.
        @type properties: Dictionary
        @param properties: The properties for the session handling.
        """

        # in case the message provider property is not defined
        if not MESSAGE_PROVIDER_VALUE in properties:
            # raises the missing property exception
            raise main_service_pop_main_session_handler_exceptions.MissingProperty(MESSAGE_PROVIDER_VALUE)

        # in case the arguments property is not defined
        if not ARGUMENTS_VALUE in properties:
            # raises the missing property exception
            raise main_service_pop_main_session_handler_exceptions.MissingProperty(ARGUMENTS_VALUE)

        # retrieves the message provider
        message_provider = properties[MESSAGE_PROVIDER_VALUE]

        # retrieves the arguments
        arguments = properties[ARGUMENTS_VALUE]

        # retrieves the message provider plugin
        message_provider_plugin = self.pop_service_message_provider_plugins_map[message_provider]

        # creates a message client for the given arguments
        message_client = message_provider_plugin.provide_message_client(arguments)

        # sets the message client in the session
        session.set_message_client(message_client)

    def pop_service_message_provider_load(self, pop_service_message_provider_plugin):
        # retrieves the plugin provider name
        message_provider_name = pop_service_message_provider_plugin.get_provider_name()

        self.pop_service_message_provider_plugins_map[message_provider_name] = pop_service_message_provider_plugin

    def pop_service_message_provider_unload(self, pop_service_message_provider_plugin):
        # retrieves the plugin provider name
        message_provider_name = pop_service_message_provider_plugin.get_provider_name()

        del self.pop_service_message_provider_plugins_map[message_provider_name]
