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

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
HELP_TEXT = "### BOT MANAGER HELP ###\n\
bot_manager_list_bots - lists the currently running bots\n\
bot_manager_start_bot <bot_id> <bot_engine_id> <input_id> <output_id> - starts a new bot\n\
bot_manager_stop_bot <bot_id> - stops a running bot\n\
bot_manager_list_inputs - lists the available input plugins for the bots\n\
bot_manager_list_engines - lists the available bot engines\n\
bot_manager_list_outputs - lists the available output plugins for the bots"

class Bot:
    bot_id = None
    bot_engine_plugin = None
    bot_input_plugin = None
    bot_output_plugin = None
    
    def __init__(self, bot_id, bot_engine_plugin, bot_input_plugin, bot_output_plugin):
        self.bot_id = bot_id
        self.bot_engine_plugin = bot_engine_plugin
        self.bot_input_plugin = bot_input_plugin
        self.bot_output_plugin = bot_output_plugin
        self.start()
        
    def start(self):
        self.bot_input_plugin.register_message_handler(self.bot_id, self.handle_incoming_message)
    
    def stop(self):
        print "Stop called for " + self.bot_id
        self.bot_input_plugin.register_message_handler(self.bot_id, None)
        
    def handle_incoming_message(self, sender_id, message):
        response_message = self.bot_engine_plugin.respond(message)
        print response_message
        self.bot_output_plugin.send(self.bot_id, sender_id, response_message)
    
#@todo: comment this class
class BotManager:
    
    commands = ["bot_manager_list_bots", "bot_manager_start_bot", "bot_manager_stop_bot", "bot_manager_list_inputs", "bot_manager_list_outputs", "bot_manager_list_engines"]

    bots_map = {}
    
    def __init__(self, parent_plugin):
        self.parent_plugin = parent_plugin
        self.bots_map = {}
        
    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT
    
    def process_bot_manager_start_bot(self, args, output_method):
        if len(args) >= 4:
            bot_id = args[0]
            bot_engine_id = args[1]
            bot_input_id = args[2]
            bot_output_id = args[3]
            condition = bot_engine_id in self.parent_plugin.bot_engine_plugins
            condition = condition and bot_input_id in self.parent_plugin.bot_input_plugins
            condition = condition and bot_output_id in self.parent_plugin.bot_output_plugins
            condition = condition and not bot_id in self.bots_map
            if condition:
                bot_engine_plugin = self.parent_plugin.bot_engine_plugins[bot_engine_id]
                bot_input_plugin = self.parent_plugin.bot_input_plugins[bot_input_id]
                bot_output_plugin = self.parent_plugin.bot_output_plugins[bot_output_id]
                self.bots_map[bot_id] = Bot(bot_id, bot_engine_plugin, bot_input_plugin, bot_output_plugin)
        else:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
    
    def process_bot_manager_stop_bot(self, args, output_method):
        if len(args) >= 1:
            bot_id = args[0]
            if bot_id in self.bots_map:
                self.bots_map[bot_id].stop()
                del self.bots_map[bot_id]
        else:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
    
    def process_bot_manager_list_bots(self, args, output_method):
        output_method("List of running bots:")
        for bot_id in self.bots_map:
            output_method("* " + bot_id)
                
    def process_bot_manager_list_inputs(self, args, output_method):
        for bot_input_plugin in self.parent_plugin.bot_input_plugins:
            output_method(bot_input_plugin)

    def process_bot_manager_list_engines(self, args, output_method):
        for bot_engine_plugin in self.parent_plugin.bot_engine_plugins:
            output_method(bot_engine_plugin)
            
    def process_bot_manager_list_outputs(self, args, output_method):
        for bot_output_plugin in self.parent_plugin.bot_output_plugins:
            output_method(bot_output_plugin)  
