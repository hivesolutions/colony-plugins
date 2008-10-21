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

__revision__ = "$LastChangedRevision: 2096 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 13:02:08 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import aiml

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
HELP_TEXT = "### AIML BOT ENGINE HELP ###\n\
bot_engine_aiml_load_brain <path> - loads a PyAIML brain into the AIML bot engine\n\
bot_engine_aiml_teach_brain <path> - teaches an AIML file to the AIML bot engine\n\
bot_engine_aiml_send <message> - sends a message to the AIML bot engine"
    
#@todo: comment this file
class BotEngineAIML:

    parent_plugin = None

    commands = ["bot_engine_aiml_load_brain", "bot_engine_aiml_teach_brain", "bot_engine_aiml_send"]
    
    aiml_engine = None
    
    def __init__(self, parent_plugin):
        self.parent_plugin = parent_plugin
        self.aiml_engine = aiml.Kernel()
    
    def load_brain(self, brain_path):
        self.aiml_engine.loadBrain(brain_path)
    
    def teach_brain(self, aiml_path):
        self.aiml_engine.teachBrain(aiml_path)
        
    def respond(self, message):
        return self.aiml_engine.respond(message)
    
    def get_id(self):
        return "bot_engine_aiml"
    
    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT
    
    def process_bot_engine_aiml_load_brain(self, args, output_method):
        if len(args) >= 1:
            brain_path = args[0]
            self.load_brain(brain_path)
        else:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
    
    def process_bot_engine_aiml_teach_brain(self, args, output_method):
        if len(args) >= 1:
            aiml_path = args[0]
            self.teach_brain(aiml_path)
        else:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE) 

    def process_bot_engine_aiml_send(self, args, output_method):
        if len(args) >= 1:
            message = args[0]
            output_method(self.respond(message))
        else:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
