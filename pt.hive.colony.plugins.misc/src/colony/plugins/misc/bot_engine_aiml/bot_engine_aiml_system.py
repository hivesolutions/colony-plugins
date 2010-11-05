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

import aiml

BRAIN_FILE_PATH = "../resources/bot.brn"
""" The path to the aiml brain """

CONSOLE_EXTENSION_NAME = "bot_engine_aiml"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### AIML BOT ENGINE HELP ###\n\
bot_engine_aiml_load_brain <path>  - loads a PyAIML brain into the aiml bot engine\n\
bot_engine_aiml_teach_brain <path> - teaches an aiml file to the aiml bot engine\n\
bot_engine_aiml_send <message>     - sends a message to the aiml bot engine"
""" The help text """

class BotEngineAiml:
    """
    The bot engine aiml class.
    """

    bot_engine_aiml_plugin = None
    """ The bot engine aiml plugin """

    commands = ["bot_engine_aiml_load_brain", "bot_engine_aiml_teach_brain", "bot_engine_aiml_send"]
    """ The commands list """

    aiml_engine = None
    """ The aiml engine """

    def __init__(self, bot_engine_aiml_plugin):
        """
        Constructor of the class.

        @type bot_engine_aiml_plugin: BotEngineAimlPlugin
        @param bot_engine_aiml_plugin: The bot engine aiml plugin.
        """

        self.bot_engine_aiml_plugin = bot_engine_aiml_plugin
        self.aiml_engine = aiml.Kernel()

    def load_brain(self, brain_path):
        self.aiml_engine.loadBrain(brain_path)

    def teach_brain(self, aiml_path):
        self.aiml_engine.teachBrain(aiml_path)

    def respond(self, message):
        return self.aiml_engine.respond(message)

    def get_id(self):
        return "bot_engine_aiml"

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        # returns in case the command is not in the commands list
        if not command in self.commands:
            return

        # retrieves the method name
        method_name = "process_" + command

        # retrieves the handler
        handler = getattr(self, method_name)

        # returns the handler
        return handler

    def get_help(self):
        return HELP_TEXT

    def process_bot_engine_aiml_load_brain(self, args, output_method):
        # returns in case an invalid number of arguments was specified
        if len(args) == 0:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the brain path
        brain_path = args[0]

        # loads the brain
        self.load_brain(brain_path)

    def process_bot_engine_aiml_teach_brain(self, args, output_method):
        # returns in case an invalid number of arguments was specified
        if len(args) == 0:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the aiml path
        aiml_path = args[0]

        # teaches the brain
        self.teach_brain(aiml_path)

    def process_bot_engine_aiml_send(self, args, output_method):
        # returns in case an invalid number of arguments was specified
        if len(args) == 0:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the message
        message = args[0]

        # retrieves the brain response
        response = self.respond(message)

        # outputs the response
        output_method(response)
