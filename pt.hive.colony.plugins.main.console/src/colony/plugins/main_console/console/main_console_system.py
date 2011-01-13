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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import sys
import time

import colony.libs.time_util

COMMAND_EXCEPTION_MESSAGE = "there was an exception"
""" The command exception message """

INVALID_COMMAND_MESSAGE = "invalid command"
""" The invalid command message """

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

COMMAND_LINE_REGEX = "\"[^\"]*\"|[^ \s]+"
""" The regular expression to retrieve the command line arguments """

ID_REGEX = "[0-9]+"
""" The regular expression to retrieve the id of the plugin """

class MainConsole:
    """
    The main console class.
    """

    main_console_plugin = None
    """ The main console plugin """

    commands = ["help", "helpall", "extensions", "status", "show", "showall", "info", "infoall", "add", "remove", "load", "unload", "exec", "exit", "echo"]
    """ The commands list """

    manager = None
    """ The plugin manager """

    commands_map = {}
    """ The map associating a command with a plugin """

    def __init__(self, main_console_plugin):
        """
        Constructor of the class.

        @type main_console_plugin: MainConsolePlugin
        @param main_console_plugin: The main console plugin.
        """

        self.main_console_plugin = main_console_plugin
        self.manager = main_console_plugin.manager

        self.commands_map = {}

    def process_command_line(self, command_line, output_method = None):
        """
        Processes the given command line, with the given output method.

        @type command_line: String
        @param command_line: The command line to be processed.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @rtype: bool
        @return: If the processing of the command line was successful.
        """

        # in case there is no output method defined
        if not output_method:
            # uses the write function as the output method
            output_method = self.write

        # splits the command line arguments
        line_split = self.split_command_line_arguments(command_line)

        # retrieves the line split length
        line_split_length = len(line_split)

        # in case the line is not empty
        if not line_split_length == 0:
            # retrieves the command value
            command = line_split[0]

            # retrieves the arguments
            arguments = line_split[1:]

            # unsets the valid flag
            valid = False

            # in case the command is defined in the native commands
            if command in self.commands:
                # creates the command method name
                method_name = "process_" + command

                # retrieves the command attribute
                attribute = getattr(self, method_name)

                try:
                    # runs the command attribute with the arguments
                    # and the output method
                    attribute(arguments, output_method)
                except Exception, exception:
                    # prints the exception message
                    output_method(COMMAND_EXCEPTION_MESSAGE + ": " + unicode(exception))

                    # logs the stack trace value
                    self.main_console_plugin.log_stack_trace()

                    # returns false (invalid)
                    return False

                # sets the valid flag
                valid = True
            elif self.main_console_plugin.console_command_plugins:
                for console_command_plugin in self.main_console_plugin.console_command_plugins:
                    # retrieves the plugin commands
                    plugin_commands = console_command_plugin.get_all_commands()

                    # iterates over all the plugin commands
                    if command in plugin_commands:
                        # retrieves the command attribute
                        attribute = console_command_plugin.get_handler_command(command)

                        try:
                            # runs the command attribute with the arguments
                            # and the output method
                            attribute(arguments, output_method)
                        except Exception, exception:
                            # prints the exception message
                            output_method(COMMAND_EXCEPTION_MESSAGE + ": " + unicode(exception))

                            # logs the stack trace value
                            self.main_console_plugin.log_stack_trace()

                            # returns false (invalid)
                            return False

                        # sets the valid flag
                        valid = True

            # in case the command is not valid
            if not valid:
                # print the invalid command message
                output_method(INVALID_COMMAND_MESSAGE)

            # returns the valid value
            return valid

    def get_command_line_alternatives(self, command_line):
        """
        Processes the given command line, with the given output method.

        @type command_line: String
        @param command_line: The command line to be retrieve the alternatives.
        @rtype: List
        @return: If list of alternatives for the given command line.
        """

        # creates the alternatives list
        alternatives_list = []

        # iterates over all the commands in the
        # commands map
        for command in self.commands_map:
            # in case the command starts with the
            # value in the command line
            command.startswith(command_line) and alternatives_list.append(command)

        # returns the alternatives list
        return alternatives_list

    def get_default_output_method(self):
        """
        Retrieves the default output method.

        @rtype: Method
        @return: The default output method for console.
        """

        return self.write

    def console_command_extension_load(self, console_command_extension_plugin):
        # retrieves all commands from the console command extension
        all_commands = console_command_extension_plugin.get_all_commands()

        # iterates over all the commands
        for command in all_commands:
            # sets the commands in the commands map
            self.commands_map[command] = console_command_extension_plugin

    def console_command_extension_unload(self, console_command_extension_plugin):
        # retrieves all commands from the console command extension
        all_commands = console_command_extension_plugin.get_all_commands()

        # iterates over all the commands
        for command in all_commands:
            # sets the commands from the commands map
            del self.commands_map[command]

    def split_command_line_arguments(self, command_line):
        """
        Separates the various command line arguments per space or per quotes.

        @type command_line: String
        @param command_line: The command line string.
        @rtype: List
        @return: The list containing the various command line arguments.
        """

        # compiles the command line regular expression generating the pattern
        pattern = re.compile(COMMAND_LINE_REGEX)

        line_split = pattern.findall(command_line)
        line_split_length = len(line_split)

        for line_split_length_index in range(line_split_length):
            line = line_split[line_split_length_index]
            line_split[line_split_length_index] = line.replace("\"", "")

        return line_split

    def write(self, text, new_line = True):
        """
        Writes the given text to the standard output,
        may use a newline or not.

        @type text: String
        @param text: The text to be written to the standard output.
        @type new_line: bool
        @param new_line: If the text should be suffixed with a newline.
        """

        # writes the text contents
        sys.stdout.write(text)

        # in case a newline should be appended
        # writes it
        new_line and sys.stdout.write("\n")

        # flushes the standard output
        sys.stdout.flush()

        import termios

        # flushes the standard output file
        termios.tcflush(sys.stdout.fileno(), termios.TCOFLUSH)

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

        output_method(EXTENSION_TABLE_TOP_TEXT)

        for console_command_plugin in self.main_console_plugin.console_command_plugins:
            # retrieves the current id for the console command plugin
            console_command_plugin_current_id = self.manager.loaded_plugins_id_map[console_command_plugin.id]
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
        plugin_manager = self.main_console_plugin.manager

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

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in self.manager.plugin_instances_map:
            plugin_instance = self.manager.plugin_instances_map[plugin_id]
            plugin_instance_current_id = self.manager.loaded_plugins_id_map[plugin_id]
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

        output_method(TABLE_TOP_TEXT)

        for plugin_instance in self.manager.plugin_instances:
            # retrieves the current id for the current plugin instance
            plugin_instance_current_id = self.manager.loaded_plugins_id_map[plugin_instance.id]
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

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in self.manager.loaded_plugins_map:
            plugin = self.manager.loaded_plugins_map[plugin_id]
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

        for plugin in self.manager.plugin_instances:
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

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in self.manager.plugin_instances_map:
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

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in self.manager.plugin_instances_map:
            self.manager.stop_plugin_complete_by_id(plugin_id)
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

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in self.manager.plugin_instances_map:
            self.manager.load_plugin(plugin_id)
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

        if len(args) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(args[0])

        if plugin_id in self.manager.plugin_instances_map:
            self.manager.unload_plugin(plugin_id)
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

        self.manager.unload_system()

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
            if int_value in self.manager.id_loaded_plugins_map:
                plugin_id = self.manager.id_loaded_plugins_map[int_value]
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
