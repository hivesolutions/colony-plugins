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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
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

CONSOLE_EXTENSION_NAME = "revision_control_manager"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### REVISION CONTROL MANAGER HELP ###\n\
list_adapters - list the revision control adapters available\n\
checkout <adapter_name> <source> <destination>\n\
update <adapter_name>  <resource_identifier> <revision_identifier>\n\
commit <adapter_name> <resource_identifier>\n"
""" The help text """

COLUMN_SPACING = 4
""" The column spacing """

ACTIVE_VALUE = "ACTIVE"
""" The active value """

INACTIVE_VALUE = "INACTIVE"
""" The inactive value """

ID_COLUMN_HEADER = "ID"
""" The id column header """

ENABLED_COLUMN_HEADER = "ENABLED"
""" The enabled column header """

TYPE_COLUMN_HEADER = "TYPE"
""" The type column header """

DESCRIPTION_COLUMN_HEADER = "DESCRIPTION"
""" The description column header """

class ConsoleRevisionControlManager:
    """
    The console revision control manager class.
    """

    revision_control_manager_plugin = None
    """ The revision control manager plugin """

    commands = ["list_revision_control_adapters",
                "checkout",
                "update",
                "commit"]
    """ The commands list """

    def __init__(self, revision_control_manager_plugin):
        """
        Constructor of the class.

        @type revision_control_manager_plugin: RevisionControlManagerPlugin
        @param revision_control_manager_plugin: The revision control manager plugin.
        """

        self.revision_control_manager_plugin = revision_control_manager_plugin

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

    def process_list_revision_control_adapters(self, args, output_method):
        # retrieves the list of adapter names
        adapter_names = [revision_control_adapter_plugin.get_adapter_name() for revision_control_adapter_plugin in self.revision_control_manager_plugin.revision_control_adapter_plugins]

        # builds a string with all the adapter names
        output_string = "".join([adapter_name + "\n" for adapter_name in adapter_names])

        # outputs a list of available revision control adapters
        output_method(output_string)

    def process_checkout(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 3:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the source
        source = args[1]

        # retrieves the destination
        destination = args[2]

        # @todo: use the revision control manager plugin to checkout

        # outputs the retrieved configurations
        output_method()

    def process_update(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the resource identifiers
        resource_identifiers = [args[1]]

        if len(args) > 2:
            # retrieves the revision identifier
            revision_identifier = args[2]
        else:
            revision_identifier = None

        # uses the revision control manager plugin to perform the update
        update_result = self.revision_control_manager_plugin.update(adapter_name, resource_identifiers, revision_identifier)

        # outputs the result
        output_method(update_result)

    def process_commit(self, args, output_method):
        pass
