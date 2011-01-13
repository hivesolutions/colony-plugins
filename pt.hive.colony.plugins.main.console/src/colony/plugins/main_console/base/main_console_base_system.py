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

__revision__ = "$LastChangedRevision: 12670 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-01-13 13:08:29 +0000 (qui, 13 Jan 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import time

import colony.libs.time_util

CONSOLE_EXTENSION_NAME = "base"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number arguments message """

INVALID_PLUGIN_ID_MESSAGE = "invalid plugin id"
""" The invalid plugin id message """

ERROR_IN_HCS_SCRIPT = "there is an error in the hcs script"
""" The error in hcs script message """

HELP_TEXT = "### PLUGIN SYSTEM HELP ###\n\
help [extension-id] - shows this message or the referred console extension help message\n\
helpall             - shows the help message of all the loaded console extensions\n\
extensions          - shows the list of loaded console extensions\n\
status              - shows the current status of the system\n\
show <plugin-id>    - shows the status of the plugin with the defined id\n\
showall             - shows the status of all the loaded plugins\n\
info <plugin-id>    - shows information about the plugin with the defined id\n\
infoall             - shows information about all the loaded plugins\n\
add <plugin-path>   - adds a new plugin\n\
remove <plugin-id>  - removes a plugin\n\
load <plugin-id>    - loads a plugin\n\
unload <plugin-id>  - unloads a plugin\n\
exec <file-path>    - executes the given hcs script\n\
exit                - exits the system"
""" The help text """

TABLE_TOP_TEXT = "ID      STATUS      PLUGIN ID"
""" The table top text """

EXTENSION_TABLE_TOP_TEXT = "ID      NAME                        PLUGIN ID"
""" The extension table top text """

COLUMN_SPACING = 8
""" The column spacing """

NAME_COLUMN_SPACING = 28
""" The name column spacing """

ID_REGEX = "[0-9]+"
""" The regular expression to retrieve the id of the plugin """

class MainConsoleBase:
    """
    The main console base class.
    """

    main_console_base_plugin = None
    """ The main console base plugin """

    commands = ["help", "helpall", "extensions", "status", "show", "showall", "info", "infoall", "add", "remove", "load", "unload", "exec", "exit", "echo"]
    """ The commands list """

    def __init__(self, main_console_base_plugin):
        """
        Constructor of the class.

        @type main_console_base_plugin: MainConsoleBasePlugin
        @param main_console_base_plugin: The main console base plugin.
        """

        self.main_console_base_plugin = main_console_base_plugin

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

    def process_help(self, args, output_method):
        """
        Processes the help command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        if len(args) < 1:
            output_method(HELP_TEXT)
        else:
            extension_name = args[0]

            for console_command_plugin in self.main_console_plugin.console_command_plugins:
                console_command_plugin_console_extension_name = console_command_plugin.get_console_extension_name()
                if console_command_plugin_console_extension_name == extension_name:
                    output_method(console_command_plugin.get_help())

    def process_helpall(self, args, output_method):
        """
        Processes the help all command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        output_method(HELP_TEXT)

        for console_command_plugin in self.main_console_plugin.console_command_plugins:
            output_method(console_command_plugin.get_help())

    def process_extensions(self, args, output_method):
        """
        Processes the extensions command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        output_method(EXTENSION_TABLE_TOP_TEXT)

        for console_command_plugin in self.main_console_plugin.console_command_plugins:
            # retrieves the current id for the console command plugin
            console_command_plugin_current_id = plugin_manager.loaded_plugins_id_map[console_command_plugin.id]
            console_command_plugin_current_id_str = str(console_command_plugin_current_id)
            console_command_plugin_console_extension_name = console_command_plugin.get_console_extension_name()

            output_method(console_command_plugin_current_id_str, False)

            for _index in range(COLUMN_SPACING - len(console_command_plugin_current_id_str)):
                output_method(" ", False)

            output_method(console_command_plugin_console_extension_name, False)

            for _index in range(NAME_COLUMN_SPACING - len(console_command_plugin_console_extension_name)):
                output_method(" ", False)

            output_method(console_command_plugin.id + "\n", False)

    def process_status(self, args, output_method):
        """
        Processes the status command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        # retrieves the plugin amnager uid
        plugin_manager_uid = plugin_manager.uid

        # retrieves the plugin manager version
        plugin_manager_version = plugin_manager.get_version()

        # retrieves the plugin manager release
        plugin_manager_release = plugin_manager.get_release()

        # retrieves the plugin manager build
        plugin_manager_build = plugin_manager.get_build()

        # retrieves the plugin manager release date time
        plugin_manager_release_date_time = plugin_manager.get_release_date_time()

        # retrieves the plugin manager layout mode
        plugin_manager_layout_mode = plugin_manager.get_layout_mode()

        # retrieves the plugin manager run mode
        plugin_manager_run_mode = plugin_manager.get_run_mode()

        # retrieves the plugin manager environment
        plugin_manager_environment = plugin_manager.get_environment()

        # retrieves the current time
        current_time = time.time()

        # retrieves the plugin manager timestamp
        plugin_manager_timestamp = plugin_manager.plugin_manager_timestamp

        # calculates the uptime
        uptime = current_time - plugin_manager_timestamp

        # creates the uptime string
        uptime_string = colony.libs.time_util.format_seconds_smart(uptime, "basic", ("day", "hour", "minute", "second"))

        # retrieves the plugin manager instances
        plugin_manager_instances = plugin_manager.plugin_instances

        # retrieves the plugin strings from the plugin manager instances
        plugins_string, replicas_string, instances_string = self.get_plugin_strings(plugin_manager_instances)

        output_method("uid:          " + plugin_manager_uid)
        output_method("version:      " + plugin_manager_version)
        output_method("release:      " + plugin_manager_release)
        output_method("build:        " + plugin_manager_build)
        output_method("release date: " + plugin_manager_release_date_time)
        output_method("environment:  " + plugin_manager_environment)
        output_method("layout mode:  " + plugin_manager_layout_mode)
        output_method("run mode:     " + plugin_manager_run_mode)
        output_method("uptime:       " + uptime_string)
        output_method("plugins:      " + plugins_string)
        output_method("replicas:     " + replicas_string)
        output_method("instances:    " + instances_string)

    def process_show(self, args, output_method):
        """
        Processes the show command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in plugin_manager.plugin_instances_map:
            plugin_instance = plugin_manager.plugin_instances_map[plugin_id]
            plugin_instance_current_id = plugin_manager.loaded_plugins_id_map[plugin_id]
            plugin_instance_current_id_str = str(plugin_instance_current_id)

            output_method(TABLE_TOP_TEXT)
            output_method(plugin_instance_current_id_str, False)
            for _index in range(COLUMN_SPACING - len(plugin_instance_current_id_str)):
                output_method(" ", False)
            if plugin_instance.is_loaded():
                output_method("ACTIVE" + "      ", False)
            else:
                output_method("INACTIVE" + "    ", False)
            output_method(plugin_instance.id + "\n", False)
        else:
            output_method(INVALID_PLUGIN_ID_MESSAGE)

    def process_showall(self, args, output_method):
        """
        Processes the show all command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        output_method(TABLE_TOP_TEXT)

        for plugin_instance in plugin_manager.plugin_instances:
            # retrieves the current id for the current plugin instance
            plugin_instance_current_id = plugin_manager.loaded_plugins_id_map[plugin_instance.id]
            plugin_instance_current_id_str = str(plugin_instance_current_id)

            output_method(plugin_instance_current_id_str, False)
            for _index in range(COLUMN_SPACING - len(plugin_instance_current_id_str)):
                output_method(" ", False)
            if plugin_instance.is_loaded():
                output_method("ACTIVE" + "      ", False)
            else:
                output_method("INACTIVE" + "    ", False)
            output_method(plugin_instance.id + "\n", False)

    def process_info(self, args, output_method):
        """
        Processes the info command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in plugin_manager.loaded_plugins_map:
            plugin = plugin_manager.loaded_plugins_map[plugin_id]
            self.print_plugin_info(plugin, output_method)
        else:
            output_method(INVALID_PLUGIN_ID_MESSAGE)

    def process_infoall(self, args, output_method):
        """
        Processes the info all command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        for plugin in plugin_manager.plugin_instances:
            self.print_plugin_info(plugin, output_method)

    def process_add(self, args, output_method):
        """
        Processes the add command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in plugin_manager.plugin_instances_map:
            output_method(INVALID_PLUGIN_ID_MESSAGE)
        else:
            pass

    def process_remove(self, args, output_method):
        """
        Processes the remove command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in plugin_manager.plugin_instances_map:
            plugin_manager.stop_plugin_complete_by_id(plugin_id)
        else:
            output_method(INVALID_PLUGIN_ID_MESSAGE)

    def process_load(self, args, output_method):
        """
        Processes the load command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in plugin_manager.plugin_instances_map:
            plugin_manager.load_plugin(plugin_id)
        else:
            output_method(INVALID_PLUGIN_ID_MESSAGE)

    def process_unload(self, args, output_method):
        """
        Processes the unload command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in plugin_manager.plugin_instances_map:
            plugin_manager.unload_plugin(plugin_id)
        else:
            output_method(INVALID_PLUGIN_ID_MESSAGE)

    def process_exec(self, args, output_method):
        """
        Processes the exec command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        file_path = args[0]

        # opens the hcs file
        file = open(file_path, "r")

        # iterates over all the lines in the file
        for line in file:
            striped_line = line.strip()
            non_commented_line = striped_line.partition("#")[0]

            # in case the line is not cleared
            if not non_commented_line == "":
                # executes the command and tests for success
                if not self.process_command_line(non_commented_line, output_method):
                    # the command was not successfully executed
                    output_method(ERROR_IN_HCS_SCRIPT + ": " + file_path)
                    break

        # closes the file
        file.close()

    def process_exit(self, args, output_method):
        """
        Processes the exit command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        plugin_manager.unload_system()

    def process_echo(self, args, output_method):
        """
        Processes the echo command, with the given
        arguments and output method.

        @type args: List
        @param args: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        """

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the echo value
        echo_value = args[0]

        # outputs the echo value
        output_method(echo_value)

    def print_plugin_info(self, plugin, output_method):
        """
        Prints the plugin information for the given plugin using
        the given output method.

        @type plugin: Plugin
        @param plugin: The plugin to have the information printed.
        @type output_method: Method
        @param output_method: The output method to be used in the information printing.
        """

        output_method("id:                   " + plugin.id)
        output_method("name:                 " + plugin.name)
        output_method("sort name:            " + plugin.description)
        output_method("version:              " + plugin.version)
        output_method("author:               " + plugin.author)
        output_method("capabilities:         " + str(plugin.capabilities))
        output_method("capabilities allowed: " + str(plugin.capabilities_allowed))
        output_method("dependencies:         " + str(plugin.dependencies))
        output_method("events handled:       " + str(plugin.events_handled))
        output_method("events registrable:   " + str(plugin.events_registrable))

    def get_plugin_id(self, id):
        """
        Retrieves the plugin id for the given internal id.

        @type id: String
        @param id: The internal id to retrieves the plugin id.
        @rtype: String
        @return: The plugin id for the given internal id.
        """

        # retrieves the plugin manager
        plugin_manager = self.main_console_base_plugin.manager

        # unsets the plugin id and the valid flag
        plugin_id = None
        valid = False

        # compiles the regular expression
        compilation = re.compile(ID_REGEX)
        result = compilation.match(id)

        # in case there is at least one match
        if result:
            valid = result.group() == id

        # in case it matches the regular expression
        if valid:
            int_value = int(id)
            if int_value in plugin_manager.id_loaded_plugins_map:
                plugin_id = plugin_manager.id_loaded_plugins_map[int_value]
        else:
            plugin_id = id

        # returns the plugin id
        return plugin_id

    def get_plugin_strings(self, plugin_manager_instances):
        """
        Constructs the various plugin strings from the
        given plugin manager instances.

        @type plugin_manager_instances: List
        @param plugin_manager_instances: The list of plugin manager instances.
        @rtype: Tuple
        @return: A tuple containing the plugin strings.
        """

        # creates the plugin counters
        plugins_loaded = 0
        plugins_total = 0
        replicas_loaded = 0
        replicas_total = 0
        instances_loaded = 0
        instances_total = 0

        # iterates over all the plugin manager instances to
        # construct the plugin values
        for plugin_manager_instance in plugin_manager_instances:
            # in case it is a replica
            if plugin_manager_instance.is_replica():
                # in case the plugin manager instance is loaded
                if plugin_manager_instance.is_loaded():
                    # increments the replicas loaded
                    replicas_loaded += 1

                # increments the replicas total
                replicas_total += 1
            else:
                # in case the plugin manager instance is loaded
                if plugin_manager_instance.is_loaded():
                    # increments the plugins loaded
                    plugins_loaded += 1

                # increments the plugins total
                plugins_total += 1

            # in case the plugin manager instance is loaded
            if plugin_manager_instance.is_loaded():
                # increments the instances loaded
                instances_loaded += 1

            # increments the instances total
            instances_total += 1

        # creates the plugins string
        plugins_string = str(plugins_loaded) + "/" + str(plugins_total)

        # creates the replicas string
        replicas_string = str(replicas_loaded) + "/" + str(replicas_total)

        # creates the instances string
        instances_string = str(instances_loaded) + "/" + str(instances_total)

        # creates the plugins tuple from the plugins string, the replicas
        # string and the instances string
        plugins_tuple = (plugins_string, replicas_string, instances_string)

        # returns the plugins tuple
        return plugins_tuple
