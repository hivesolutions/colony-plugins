#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import time
import code

import colony.base.system
import colony.libs.time_util

CONSOLE_EXTENSION_NAME = "base"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number arguments message """

INVALID_PLUGIN_ID_MESSAGE = "invalid plugin id"
""" The invalid plugin id message """

ERROR_IN_HCS_SCRIPT = "there is an error in the hcs script"
""" The error in hcs script message """

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

class ConsoleBase(colony.base.system.System):
    """
    The console base class.
    """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_help(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the help command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the console plugin
        console_plugin = self.plugin.console_plugin

#        if len(args) < 1:
#            output_method(HELP_TEXT)
#        else:
#            extension_name = args[0]
#
#            for console_command_plugin in console_plugin.console_command_plugins:
#                console_command_plugin_console_extension_name = console_command_plugin.get_console_extension_name()
#                if console_command_plugin_console_extension_name == extension_name:
#                    output_method(console_command_plugin.get_help())

    def process_helpall(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the help all command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the console plugin
        console_plugin = self.plugin.console_plugin

#        output_method(HELP_TEXT)
#
#        for console_command_plugin in console_plugin.console_command_plugins:
#            output_method(console_command_plugin.get_help())

    def process_extensions(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the extensions command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the console plugin
        console_plugin = self.plugin.console_plugin

        output_method(EXTENSION_TABLE_TOP_TEXT)

        for console_command_plugin in console_plugin.console_command_plugins:
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

    def process_status(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the status command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager and uses it to retrieve the
        # various attributes to be displayed to the user
        plugin_manager = self.plugin.manager
        plugin_manager_uid = plugin_manager.uid
        plugin_manager_version = plugin_manager.get_version()
        plugin_manager_release = plugin_manager.get_release()
        plugin_manager_build = plugin_manager.get_build()
        plugin_manager_release_date_time = plugin_manager.get_release_date_time()
        plugin_manager_layout_mode = plugin_manager.get_layout_mode()
        plugin_manager_run_mode = plugin_manager.get_run_mode()
        plugin_manager_environment = plugin_manager.get_environment()

        # retrieves the current time and the plugin manager (start)
        # timestamp and calculates the uptime as the difference between
        # both values (time delta)
        current_time = time.time()
        plugin_manager_timestamp = plugin_manager.plugin_manager_timestamp
        uptime = current_time - plugin_manager_timestamp

        # creates the uptime string
        uptime_string = colony.libs.time_util.format_seconds_smart(uptime, "basic", ("day", "hour", "minute", "second"))

        # retrieves the plugin manager instances
        plugin_manager_instances = plugin_manager.plugin_instances

        # retrieves the plugin strings from the plugin manager instances
        plugins_string, replicas_string, instances_string = self.get_plugin_strings(plugin_manager_instances)

        # prints the status values
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

    def process_python(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the python command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager associated with the current
        # plugin context to be able to expose it
        plugin_manager = self.plugin.manager

        # creates the map containing the various local symbols
        # to be exposed to the python console to be created and
        # then creates the python console and starts running it
        # with the interact operation, this should begin a loop
        # that will only end at the exit call
        locals = {
            "manager" : plugin_manager,
            "plugin_manager" : plugin_manager
        }
        python_console = code.InteractiveConsole(locals = locals)
        python_console.interact()

    def process_show(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the show command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the plugin id
        plugin_id = arguments_map.get("plugin_id", None)

        # in case the plugin id is defined
        if plugin_id:
            # retrieves the "real" plugin id
            plugin_id = self.get_plugin_id(plugin_id)

            # retrieves the plugin instance from the plugin manager
            # plugin instances map
            plugin_instance = plugin_manager.plugin_instances_map[plugin_id]

            # sets the plugin instances (list) with only the plugin
            # instance as the element
            plugin_instances = [plugin_instance]
        # otherwise
        else:
            # sets the plugin instances as all the plugin
            # manager instances
            plugin_instances = plugin_manager.plugin_instances

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # prints the table top text
        output_method(TABLE_TOP_TEXT)

        # iterates over all the plugin instances
        for plugin_instance in plugin_instances:
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

    def process_info(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the info command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        if len(arguments) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(arguments[0])

        if plugin_id in plugin_manager.loaded_plugins_map:
            plugin = plugin_manager.loaded_plugins_map[plugin_id]
            self.print_plugin_info(plugin, output_method)
        else:
            output_method(INVALID_PLUGIN_ID_MESSAGE)

    def process_infoall(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the info all command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        for plugin in plugin_manager.plugin_instances:
            self.print_plugin_info(plugin, output_method)

    def process_add(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the add command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        if len(arguments) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(arguments[0])

        if plugin_id in plugin_manager.plugin_instances_map:
            output_method(INVALID_PLUGIN_ID_MESSAGE)
        else:
            pass

    def process_remove(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the remove command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        if len(arguments) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(arguments[0])

        if plugin_id in plugin_manager.plugin_instances_map:
            plugin_manager.stop_plugin_complete_by_id(plugin_id)
        else:
            output_method(INVALID_PLUGIN_ID_MESSAGE)

    def process_load(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the load command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        if len(arguments) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(arguments[0])

        if plugin_id in plugin_manager.plugin_instances_map:
            plugin_manager.load_plugin(plugin_id)
        else:
            output_method(INVALID_PLUGIN_ID_MESSAGE)

    def process_unload(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the unload command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        if len(arguments) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        plugin_id = self.get_plugin_id(arguments[0])

        if plugin_id in plugin_manager.plugin_instances_map:
            plugin_manager.unload_plugin(plugin_id)
        else:
            output_method(INVALID_PLUGIN_ID_MESSAGE)

    def process_loadall(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the loadall command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # iterates over all the plugin identifies existent in the
        # plugin instances map and the loads the associated plugin
        # this action should be able to trigger the load of all
        # the plugins available in the current plugin manager
        for plugin_id in plugin_manager.plugin_instances_map:
            plugin_manager.load_plugin(plugin_id)

    def process_unloadall(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the unloadall command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # iterates over all the plugin identifies existent in the
        # plugin instances map and the loads the associated plugin
        # this action should be able to trigger the unload of all
        # the plugins available in the current plugin manager
        for plugin_id in plugin_manager.plugin_instances_map:
            plugin_manager.unload_plugin(plugin_id)

    def process_exec(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the exec command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        if len(arguments) < 1:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        file_path = arguments[0]

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

    def process_restart(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the restart command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # reloads the plugins manager system
        # (exits the process and then launches it again)
        plugin_manager.reload_system()

    def process_exit(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the exit command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # unloads the plugins manager system
        # (exits the process)
        plugin_manager.unload_system()

    def process_echo(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the echo command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the echo value
        echo_value = arguments_map["echo_value"]

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
        output_method("events fired:         " + str(plugin.events_fired))
        output_method("events handled:       " + str(plugin.events_handled))

    def get_plugin_id(self, id):
        """
        Retrieves the plugin id for the given internal id.

        @type id: String
        @param id: The internal id to retrieves the plugin id.
        @rtype: String
        @return: The plugin id for the given internal id.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

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
        # it is an id value
        if valid:
            int_value = int(id)
            if int_value in plugin_manager.id_loaded_plugins_map:
                plugin_id = plugin_manager.id_loaded_plugins_map[int_value]
        # otherwise
        else:
            # sets the plugin id as the id
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
        plugins_tuple = (
            plugins_string,
            replicas_string,
            instances_string
        )

        # returns the plugins tuple
        return plugins_tuple

    def get_extension_id_list(self, argument, console_context):
        return [
            "rabeton",
            "tobias"
        ]

    def get_plugin_id_list(self, argument, console_context):
        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the plugin id list
        plugin_id_list = plugin_manager.plugin_instances_map.keys()

        # returns the plugin id list
        return plugin_id_list

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "help" : {
                "handler" : self.process_help,
                "description" : "shows this message or the referred console extension help message",
                "arguments" : [
                    {
                        "name" : "extension_id",
                        "description" : "the id of the extension to be loaded",
                        "values" : self.get_extension_id_list,
                        "mandatory" : False
                    }
                ]
            },
            "helpall" : {
                "handler" : self.process_helpall,
                "description" : "shows the help message of all the loaded console extensions"
            },
            "extensions" : {
                "handler" : self.process_extensions,
                "description" : "shows the help message of all the loaded console extensions"
            },
            "status" : {
                "handler" : self.process_status,
                "description" : "shows the current status of the system"
            },
            "python" : {
                "handler" : self.process_python,
                "description" : "starts the python interpreter cli with the current context",
            },
            "show" : {
                "handler" : self.process_show,
                "description" : "shows the status of the plugin with the defined id",
                "arguments" : [
                    {
                        "name" : "plugin_id",
                        "description" : "the id of the plugin to be shown",
                        "values" : self.get_plugin_id_list,
                        "mandatory" : False
                    }
                ]
            },
            "info" : {
                "handler" : self.process_info,
                "help" : "shows the status about a plugin",
                "arguments" : [
                    {
                        "name" : "plugin_id",
                        "description" : "the id of the plugin to show the information",
                        "values" : self.get_plugin_id_list,
                        "mandatory" : False
                    }
                ]
            },
            "infoall" : {
                "handler" : self.process_infoall,
                "help" : "shows information about all the loaded plugins"
            },
            "add" : {
                "handler" : self.process_add,
                "help" : "adds a new plugin to the system",
                "arguments" : [
                    {
                        "name" : "plugin_path",
                        "description" : "the path of the plugin to be added",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            },
            "remove" : {
                "handler" : self.process_remove,
                "help" : "removes plugin from the system",
                "arguments" : [
                    {
                        "name" : "plugin_id",
                        "description" : "the id of the plugin to be removed",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            },
            "load" : {
                "handler" : self.process_load,
                "help" : "loads a plugin",
                "arguments" : [
                    {
                        "name" : "plugin_id",
                        "description" : "the id of the plugin to be loaded",
                        "values" : self.get_plugin_id_list,
                        "mandatory" : True
                    }
                ]
            },
            "unload" : {
                "handler" : self.process_unload,
                "help" : "unloads a plugin",
                "arguments" : [
                    {
                        "name" : "plugin_id",
                        "description" : "the id of the plugin to be unloaded",
                        "values" : self.get_plugin_id_list,
                        "mandatory" : True
                    }
                ]
            },
            "loadall" : {
                "handler" : self.process_loadall,
                "help" : "loads all the available plugins"
            },
            "unloadall" : {
                "handler" : self.process_unloadall,
                "help" : "unloads all the available plugins"
            },
            "exec" : {
                "handler" : self.process_exec,
                "help" : "executes the given hcs script",
                "arguments" : [
                    {
                        "name" : "file_path",
                        "description" : "the path of the file to be executed",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            },
            "restart" : {
                "handler" : self.process_restart,
                "help" : "restarts the system"
            },
            "exit" : {
                "handler" : self.process_exit,
                "help" : "exits the system"
            },
            "echo" : {
                "handler" : self.process_echo,
                "help" : "prints the given value",
                "arguments" : [
                    {
                        "name" : "echo_value",
                        "description" : "the value to be echoed",
                        "values" : str,
                        "mandatory" : True
                    }
                ]
            }
        }

        # returns the commands map
        return commands_map
