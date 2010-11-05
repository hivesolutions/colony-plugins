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

CONSOLE_EXTENSION_NAME = "bot_manager"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### BOT MANAGER HELP ###\n\
bot_manager_list_bots                                                 - lists the currently running bots\n\
bot_manager_start_bot <bot_id> <bot_engine_id> <input_id> <output_id> - starts a new bot\n\
bot_manager_stop_bot <bot_id>                                         - stops a running bot\n\
bot_manager_list_inputs                                               - lists the available input plugins for the bots\n\
bot_manager_list_engines                                              - lists the available bot engines\n\
bot_manager_list_outputs                                              - lists the available output plugins for the bots"
""" The help text """

class BotManager:
    """
    The bot manager class.
    """

    bot_manager_plugin = None
    """ The bot manager plugin """

    commands = ["bot_manager_list_bots", "bot_manager_start_bot", "bot_manager_stop_bot", "bot_manager_list_inputs", "bot_manager_list_outputs", "bot_manager_list_engines"]
    """ The commands list """

    bots_map = {}
    """ The bots map """

    bot_input_map = {}
    """ The bot input map """

    bot_output_map = {}
    """ The bot output map """

    bot_engine_map = {}
    """ The bot engine map """

    def __init__(self, bot_manager_plugin):
        """
        Constructor of the class.

        @type bot_manager_plugin: BotManagerPlugin
        @param bot_manager_plugin: The bot manager plugin.
        """

        self.bot_manager_plugin = bot_manager_plugin
        self.bots_map = {}
        self.bot_input_map = {}
        self.bot_output_map = {}
        self.bot_engine_map = {}

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        # returns in case the command was not found
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

    def process_bot_manager_start_bot(self, args, output_method):
        # returns in case a invalid number of arguments was specified
        if len(args) < 4:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the bot id
        bot_id = args[0]

        # returns in case the bot id is not in the bot map
        if not bot_id in self.bots_map:
            return

        # retrieves the bot engine id
        bot_engine_id = args[1]

        # returns in case the bot engine id is not in the bot engine map
        if not bot_engine_id in self.bot_engine_map:
            return

        # retrieves the bot engine plugin
        bot_engine_plugin = self.bot_engine_map[bot_engine_id]

        # retrieves the bot input id
        bot_input_id = args[2]

        # returns in case the bot input id is not in the bot input map
        if not bot_input_id in self.bot_input_map:
            return

        # retrieves the bot input plugin
        bot_input_plugin = self.bot_input_map[bot_input_id]

        # retrieves the bot output id
        bot_output_id = args[3]

        # returns in case the bot output id is not in the bot output map
        if not bot_output_id in self.bot_output_map:
            return

        # retrieves the bot output plugin
        bot_output_plugin = self.bot_manager_map[bot_output_id]

        # sets the bot in the bot map
        self.bots_map[bot_id] = Bot(bot_id, bot_engine_plugin, bot_input_plugin, bot_output_plugin)

    def process_bot_manager_stop_bot(self, args, output_method):
        # returns in case an invalid number of arguments was specified
        if len(args) == 0:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the bot id
        bot_id = args[0]

        # returns in case the bot id is not in the bot map
        if not bot_id in self.bots_map:
            return

        # retrieves the bot
        bot = self.bots_map[bot_id]

        # stops the bot
        bot.stop()

        # removes the bot from the bot map
        del self.bots_map[bot_id]

    def process_bot_manager_list_bots(self, args, output_method):
        output_method("List of running bots:")

        # outpus the bot ids
        for bot_id in self.bots_map:
            output_method("* " + bot_id)

    def process_bot_manager_list_inputs(self, args, output_method):
        for bot_input_plugin in self.bot_input_map:
            output_method(bot_input_plugin)

    def process_bot_manager_list_engines(self, args, output_method):
        for bot_engine_plugin in self.bot_engine_map:
            output_method(bot_engine_plugin)

    def process_bot_manager_list_outputs(self, args, output_method):
        for bot_output_plugin in self.bot_output_map:
            output_method(bot_output_plugin)

    def load_bot_input_plugin(self, bot_input_plugin):
        self.bot_input_map[bot_input_plugin.id] = bot_input_plugin

    def unload_bot_input_plugin(self, bot_input_plugin):
        del self.bot_input_map[bot_input_plugin.id]

    def load_bot_output_plugin(self, bot_output_plugin):
        self.bot_output_map[bot_output_plugin.id] = bot_output_plugin

    def unload_bot_output_plugin(self, bot_output_plugin):
        del self.bot_output_map[bot_output_plugin.id]

    def load_bot_engine_plugin(self, bot_engine_plugin):
        self.bot_engine_map[bot_engine_plugin.id] = bot_engine_plugin

    def unload_bot_engine_plugin(self, bot_engine_plugin):
        del self.bot_engine_map[bot_engine_plugin.id]

class Bot:
    """
    The bot class.
    """

    bot_id = None
    """ The bot id """

    bot_engine_plugin = None
    """ The bot engine plugin """

    bot_input_plugin = None
    """ The bot input plugin """

    bot_output_plugin = None
    """ The bot output plugin """

    def __init__(self, bot_id, bot_engine_plugin, bot_input_plugin, bot_output_plugin):
        """
        Constructor fo the class.

        @type bot_id: int
        @param bot_id: The bot id.
        @type bot_engine_plugin: BotEnginePlugin
        @param bot_engine_plugin: The bot engine plugin.
        @type bot_input_plugin: BotInputPlugin
        @param bot_input_plugin: The bot input plugin.
        @type bot_output_plugin: BotOuputPlugin
        @param bot_output_plugin: The bot output plugin.
        """

        self.bot_id = bot_id
        self.bot_engine_plugin = bot_engine_plugin
        self.bot_input_plugin = bot_input_plugin
        self.bot_output_plugin = bot_output_plugin
        self.start()

    def start(self):
        self.bot_input_plugin.register_message_handler(self.bot_id, self.handle_incoming_message)

    def stop(self):
        self.bot_input_plugin.register_message_handler(self.bot_id, None)

    def handle_incoming_message(self, sender_id, message):
        # retrieves the bot engine response
        response_message = self.bot_engine_plugin.respond(message)

        # outputs the bot engine response
        self.bot_output_plugin.send(self.bot_id, sender_id, response_message)
