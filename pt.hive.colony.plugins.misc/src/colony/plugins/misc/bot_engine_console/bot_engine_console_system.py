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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class BotEngineConsole:
    """
    The bot engine console class.
    """

    bot_engine_console_plugin = None
    """ The bot engine console plugin """

    message_plugin = None
    """ The message plugin """

    def __init__(self, bot_engine_console_plugin):
        """
        Constructor of the class.

        @type bot_engine_console_plugin: BotEngineConsolePlugin
        @param bot_engine_console_plugin: The bot engine console plugin.
        """

        self.bot_engine_console_plugin = bot_engine_console_plugin

    def respond(self, message):
        # initializes the message buffer
        self.message_buffer = ""

        # processes the command line
        self.bot_engine_console_plugin.console_plugin.process_command_line(message, self.output_method)

        # returns the message buffer
        return self.message_buffer

    def output_method(self, text, new_line = True):
        # adds to the message buffer
        self.message_buffer += text

        # adds a new line to the message buffer
        if new_line:
            self.message_buffer += "\n"
