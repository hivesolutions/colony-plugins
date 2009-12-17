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

__author__ = "Lu�s Martinho <lmartinho@hive.pt>"
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

import datetime

CONSOLE_EXTENSION_NAME = "revision_control_manager"
""" The console extension name """

INVALID_NUMBER_ARGUMENTS_MESSAGE = "invalid number of arguments"
""" The invalid number of arguments message """

HELP_TEXT = "### REVISION CONTROL MANAGER HELP ###\n\
list_revision_control_adapters                                                  - lists the names of the revision control adapters available\n\
checkout <adapter_name> <source> <destination>                                  - checks out the <source> to the <destination>\n\
update <adapter_name>  <resource_identifier> <revision>                         - updates a resource to a specified revision\n\
commit <adapter_name> <resource_identifier> <commit_message>                    - commits the changes in the resource with the specified message\n\
log <adapter_name> <resource_identifier> [start_revision=HEAD] [end_revision=0] - lists the change sets for the specified resource identifier between the specified revisions\n\
log_date <adapter_name> <resource_identifier> [date]                            - lists all the change sets for the specified resource identifier matching the date specification"
""" The help text """

DATE_FORMAT = "%Y/%m/%d"
""" The format for the displayed dates """

DATE_TIME_FORMAT = "%a %b %d %H:%M:%S %Y %Z"
""" The format for the displayed date times """

class ConsoleRevisionControlManager:
    """
    The console revision control manager class.
    """

    revision_control_manager_plugin = None
    """ The revision control manager plugin """

    commands = ["list_revision_control_adapters",
                "checkout",
                "update",
                "commit",
                "log",
                "log_name"]
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

        # removes the trailing newline
        stripped_output_string = output_string.strip()

        # outputs a list of available revision control adapters
        output_method(stripped_output_string)

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
        output_method("not implemented")

    def process_update(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the resource identifier
        resource_identifier = args[1]

        if len(args) > 2:
            # retrieves the revision identifier
            revision = args[2]
        else:
            revision = None

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name, resource_identifier)

        # creates the resource identifiers list
        resource_identifiers = [resource_identifier]

        try:
            # uses the revision control manager to perform the update
            update_revision = revision_control_manager.update(resource_identifiers, revision)

            if update_revision:
                # outputs the result
                output_method("successfully updated to revision " + update_revision)
            else:
                output_method("successfully updated")
        except Exception, exception:
            # outputs the result
            output_method("problem updating resources: " + str(exception))

    def process_commit(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 3:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the resource identifier
        resource_identifier = args[1]

        # retrieves the commit message
        commit_message = args[2]

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name, resource_identifier)

        # creates the resource identifiers list
        resource_identifiers = [resource_identifier]

        try:
            # uses the revision control manager to perform the commit
            commit_revision = revision_control_manager.commit(resource_identifiers, commit_message)

            if commit_revision:
                # outputs the result
                output_method("successfully committed revision " + commit_revision)
            else:
                output_method("successfully committed")
        except Exception, exception:
            # outputs the result
            output_method("problem committing resources: " + str(exception))

    def process_log(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # determines the number of arguments
        number_arguments = len(args)

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the resource identifier
        resource_identifier = args[1]

        if number_arguments > 2:
            # retrieves the start revision
            start_revision = args[2]
        else:
            start_revision = None

        if number_arguments > 3:
            # retrieves the end revision
            end_revision = args[3]
        else:
            end_revision = None

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name, resource_identifier)

        # creates the resource identifiers list
        resource_identifiers = [resource_identifier]

        try:
            # uses the revision control manager to perform the commit
            log_entries = revision_control_manager.log(resource_identifiers, start_revision, end_revision)

            # outputs the result
            output_method("showing all change sets for \"%s\"" % resource_identifier)

            # outputs the log entries
            self.output_log_entries(log_entries, output_method)
        except Exception, exception:
            # outputs the result
            output_method("problem retrieving change set log: " + str(exception))

    def load_revision_control_manager(self, adapter_name, resource_identifier):
        # creates the revision control parameters
        revision_control_parameters = {"repository_path" : resource_identifier}

        # loads a new revision control manager for the specified adapter name
        revision_control_manager = self.revision_control_manager_plugin.load_revision_control_manager(adapter_name, revision_control_parameters)

        # returns the creates revision control manager
        return revision_control_manager

    def output_log_entries(self, log_entries, output_method):
        # for all the log results
        for log_entry in log_entries:
            # retrieves the log entry fields
            log_entry_author = log_entry["author"]
            log_entry_date = log_entry["date"]
            log_entry_message = log_entry["message"]
            log_entry_revision = log_entry["revision"]

            # creates a date time
            date_time = self.get_date_time_from_timestamp(log_entry_date)

            # gets a date time string
            date_time_string = self.get_date_time_string(date_time)

            # clears a line of input
            output_method("")

            # outputs the log entry information
            output_method("changeset:   " + log_entry_revision)
            output_method("author:      " + log_entry_author)
            output_method("date:        " + date_time_string)
            output_method("summary:     " + log_entry_message)

    def get_date_time_from_timestamp(self, timestamp):
        # creates a datetime object from the timestamp with no associated tzinfo
        date_time = datetime.datetime.fromtimestamp(timestamp)

        return date_time

    def get_date_time_string(self, date_time):
        # converts the datetime to a string representation with the date and time
        date_time_string = date_time.strftime(DATE_TIME_FORMAT)

        return date_time_string
