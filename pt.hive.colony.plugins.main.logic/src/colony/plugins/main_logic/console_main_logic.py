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

__revision__ = "$LastChangedRevision: 888 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-28 16:39:52 +0000 (Sun, 28 Dec 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

CONSOLE_EXTENSION_NAME = "migrator"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

INVALID_ADDRESS_MESSAGE = "invalid address"
""" The invalid address message """

HELP_TEXT = "### MIGRATOR HELP ###\n\
migrate - migrates diamante"
""" The help text """

#@todo: review and comment this file
class ConsoleMainLogic:

    commands = ["migrate"]

    main_logic_plugin = None

    def __init__(self, main_logic_plugin = None):
        self.main_logic_plugin = main_logic_plugin

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_all_commands(self):
        return self.commands

    def get_handler_command(self, command):
        if command in self.commands:
            method_name = "process_" + command
            attribute = getattr(self, method_name)
            return attribute

    def get_help(self):
        return HELP_TEXT

    def process_migrate(self, args, output_method):
        self.main_logic_plugin.process_query({"work_units" : ["customer"], 
                                         "diamante_path" : "c:/DIA2002", 
                                         "query_type" : "convert" , 
                                         "input_adapter_plugin_id" : "pt.hive.colony.plugins.adapters.input", 
                                         "output_adapter_plugin_id" : "pt.hive.colony.plugins.adapters.output"})
        return
        
