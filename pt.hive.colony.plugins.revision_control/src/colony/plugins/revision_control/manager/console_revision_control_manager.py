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
revision_list_adapters                                                             - lists the names of the revision control adapters available\n\
revision_add <adapter_name> <resource_identifier> [recurse]                        - schedules <resource_identifier> to be added to the repository\n\
revision_checkout <adapter_name> <source> <destination>                            - checks out the <source> to the <destination>\n\
revision_update <adapter_name>  <resource_identifier> <revision>                   - updates a resource to a specified revision\n\
revision_commit <adapter_name> <resource_identifier> <commit_message>              - commits the changes in the resource with the specified message\n\
revision_log <adapter_name> <resource_identifier> [start_revision] [end_revision]  - lists the change sets for the specified resource identifier between the specified revisions\n\
revision_status <adapter_name> <resource_identifier>                               - lists the pending changes in the current revision\n\
revision_diff <adapter_name> <resource_identifier> [start_revision] [end_revision] - compares the contents of the specified revisions\n\
revision_cleanup <adapter_name> <resource_identifier>                              - cleans up existing locks at the specified location\n\
revision_remove <adapter_name> <resource_identifier>                               - schedules <resource_identifier> to be removed from the repository\n\
revision_revert <adapter_name> <resource_identifier>                               - restores the working copy to its original state\n\n\
revision_remove_unversioned <adapter_name> <resource_identifier>                   - removes all unversioned files from the specified location\n\
revision_get_resource_revision <adapter_name> <resource_identifier> [revision]     - retrieves the content of the resource in the specified revision\n\
revision_log_date <adapter_name> <resource_identifier> [date]                      - lists all the change sets for the specified resource identifier matching the date specification"
""" The help text """

DATE_FORMAT = "%Y/%m/%d"
""" The format for the displayed dates """

DATE_TIME_FORMAT = "%a %b %d %H:%M:%S %Y %Z"
""" The format for the displayed date times """

STATUS_STRING_LIST = ("M", "A", "R", "D", "U", "I", "C")
""" The status string list """

class ConsoleRevisionControlManager:
    """
    The console revision control manager class.
    """

    revision_control_manager_plugin = None
    """ The revision control manager plugin """

    commands = ["revision_list_adapters",
                "revision_add",
                "revision_checkout",
                "revision_update",
                "revision_commit",
                "revision_log",
                "revision_log_name",
                "revision_status",
                "revision_diff",
                "revision_cleanup",
                "revision_remove",
                "revision_revert",
                "revision_remove_unversioned",
                "revision_get_resource_revision"]
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

    def process_revision_list_adapters(self, args, output_method):
        # retrieves the list of adapter names
        adapter_names = [revision_control_adapter_plugin.get_adapter_name() for revision_control_adapter_plugin in self.revision_control_manager_plugin.revision_control_adapter_plugins]

        # builds a string with all the adapter names
        output_string = "".join([adapter_name + "\n" for adapter_name in adapter_names])

        # removes the trailing newline
        stripped_output_string = output_string.strip()

        # outputs a list of available revision control adapters
        output_method(stripped_output_string)

    def process_revision_add(self, args, output_method):
        # retrieves the argument count
        argument_count = len(args)

        # returns in case an invalid number of arguments was provided
        if argument_count < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the source
        resource_identifier = args[1]

        # retrieves the recurse flag representation
        if(argument_count > 2):
            recurse_string = args[2]

            # retrieves the recurse flag
            recurse = recurse_string == "true"
        else:
            # recurse default to true
            recurse = True

        # builds the resource identifier list
        resource_identifiers = [resource_identifier]

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name)

        try:
            # uses the revision control manager to perform the checkout
            revision_control_manager.add(resource_identifiers, recurse)

            # outputs the result
            output_method("successfully added " + unicode(resource_identifier))
        except Exception, exception:
            # outputs the result
            output_method("problem adding " + unicode(resource_identifier) + ": " + unicode(exception))

    def process_revision_checkout(self, args, output_method):
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

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name)

        # uses the revision control manager to perform the checkout
        revision_control_manager.checkout(source, destination)

    def process_revision_update(self, args, output_method):
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
        revision_control_manager = self.load_revision_control_manager(adapter_name)

        # creates the resource identifiers list
        resource_identifiers = [resource_identifier]

        try:
            # uses the revision control manager to perform the update
            update_revision = revision_control_manager.update(resource_identifiers, revision)

            if update_revision:
                # outputs the result
                output_method("successfully updated to revision " + str(update_revision))
            else:
                output_method("successfully updated")
        except Exception, exception:
            # outputs the result
            output_method("problem updating resources: " + unicode(exception))

    def process_revision_commit(self, args, output_method):
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

            # in case a valid revision was created
            if commit_revision:
                # outputs the result
                output_method("successfully committed revision " + str(commit_revision))
            else:
                # otherwise indicates nothing is available to commit
                output_method("nothing to commit")
        except Exception, exception:
            # outputs the result
            output_method("problem committing resources: " + unicode(exception))

    def process_revision_log(self, args, output_method):
        # determines the number of arguments
        number_arguments = len(args)

        # returns in case an invalid number of arguments was provided
        if number_arguments < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

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

            # outputs the log entries
            self.output_log_entries(log_entries, output_method)
        except Exception, exception:
            # outputs the result
            output_method("problem retrieving change set log: " + unicode(exception))

    def process_revision_status(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the resource identifier
        resource_identifier = args[1]

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name, resource_identifier)

        # creates the resource identifiers list
        resource_identifiers = [resource_identifier]

        try:
            # uses the revision control manager to check the status
            status = revision_control_manager.status(resource_identifiers)

            # outputs the result
            self.output_status(status, output_method)
        except Exception, exception:
            # outputs the result
            output_method("problem retrieving status: " + unicode(exception))

    def process_revision_diff(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the resource identifier
        resource_identifier = args[1]

        # number of arguments
        number_arguments = len(args)

        # retrieves the first revision
        if number_arguments > 2:
            revision_1 = args[2]
        else:
            revision_1 = None

        # retrieves the second revision
        if number_arguments > 3:
            revision_2 = args[3]
        else:
            revision_2 = None

        # creates the resource identifiers list
        resource_identifiers = [resource_identifier]

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name, resource_identifier)

        try:
            # uses the revision control manager to perform the diff
            diffs = revision_control_manager.diff(resource_identifiers, revision_1, revision_2)

            # outputs the result
            self.output_diffs(diffs, output_method)
        except Exception, exception:
            # outputs the result
            output_method("problem computing diff: " + unicode(exception))

    def process_revision_cleanup(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the resource identifier
        resource_identifier = args[1]

        # creates the resource identifiers list
        resource_identifiers = [resource_identifier]

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name, resource_identifier)

        # invokes the cleanup command
        revision_control_manager.cleanup(resource_identifiers)

    def process_revision_remove(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the source
        resource_identifier = args[1]

        # builds the resource identifier list
        resource_identifiers = [resource_identifier]

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name)

        try:
            # uses the revision control manager to perform the checkout
            revision_control_manager.remove(resource_identifiers)

            # outputs the result
            output_method("successfully removed " + unicode(resource_identifier))
        except Exception, exception:
            # outputs the result
            output_method("problem removing " + unicode(resource_identifier) + ": " + unicode(exception))

    def process_revision_revert(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the resource identifier
        resource_identifier = args[1]

        # creates the resource identifiers list
        resource_identifiers = [resource_identifier]

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name, resource_identifier)

        # invokes the revert command
        revision_control_manager.revert(resource_identifiers)

    def process_revision_remove_unversioned(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the resource identifier
        resource_identifier = args[1]

        # creates the resource identifiers list
        resource_identifiers = [resource_identifier]

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name, resource_identifier)

        # invokes the remove unversioned command
        revision_control_manager.revision_remove_unversioned(resource_identifiers)

    def process_revision_get_resource_revision(self, args, output_method):
        # returns in case an invalid number of arguments was provided
        if len(args) < 2:
            output_method(INVALID_NUMBER_ARGUMENTS_MESSAGE)
            return

        # retrieves the adapter name
        adapter_name = args[0]

        # retrieves the resource identifier
        resource_identifier = args[1]

        # number of arguments
        number_arguments = len(args)

        # retrieves the first revision
        if number_arguments > 2:
            revision = args[2]
        else:
            revision = None

        # creates the resource identifiers list
        resource_identifiers = [resource_identifier]

        # creates a revision control manager to use on the resource
        revision_control_manager = self.load_revision_control_manager(adapter_name, resource_identifier)

        try:
            # uses the revision control manager to perform the cat
            resources_revision = revision_control_manager.get_resources_revision(resource_identifiers, revision)

            # outputs the result
            for resource_revision in resources_revision:
                output_method(resource_revision)
        except Exception, exception:
            if not revision:
                # outputs the result
                output_method("problem retrieving the resource's content: " + unicode(exception))
            else:
                # outputs the result
                output_method("problem retrieving the resource's content for revision " + revision + ": " + unicode(exception))

    def load_revision_control_manager(self, adapter_name, resource_identifier = None):
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
            log_entry_author = log_entry.get_author()
            log_entry_date = log_entry.get_date()
            log_entry_message = log_entry.get_message()
            log_entry_revision = str(log_entry)

            # gets a date time string
            date_time_string = self.get_date_time_string(log_entry_date)

            # clears a line of input
            output_method("")

            # outputs the log entry information
            output_method("changeset: " + log_entry_revision)
            output_method("author:    " + log_entry_author)
            output_method("date:      " + date_time_string)
            output_method("summary:   " + log_entry_message)

    def output_status(self, status, output_method):
        # retrieves the status length
        status_length = len(status)

        # iterates over the status length range
        for status_type_index in range(status_length):
            # retrieves the resources for the current status type
            status_type_resource_identifiers = status[status_type_index]

            # retrieves the string for the current status type
            status_string = STATUS_STRING_LIST[status_type_index]

            # for all the resources of the current status type
            for resource_identifier in status_type_resource_identifiers:
                output_method(status_string + "        " + resource_identifier)

    def output_diffs(self, diffs, output_method):
        for diff in diffs:
            output_method(diff)

    def get_date_time_string(self, date_time):
        # converts the datetime to a string representation with the date and time
        date_time_string = date_time.strftime(DATE_TIME_FORMAT)

        return date_time_string
