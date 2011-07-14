#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import revision_control_manager_exceptions

NUMBER_VALUE = "number"
""" The number value """

IDENTIFIER_VALUE = "identifier"
""" The identifier value """

DATE_VALUE = "date"
""" The date value """

AUTHOR_VALUE = "author"
""" The author value """

MESSAGE_VALUE = "message"
""" The message value """

class RevisionControlManager:
    """
    The revision control manager class.
    """

    revision_control_manager_plugin = None
    """ The revision control manager plugin """

    revision_control_adapter_plugins_map = {}
    """ The revision control adapter plugins map """

    def __init__(self, revision_control_manager_plugin):
        """
        Constructor of the class.

        @type revision_control_manager_plugin: RevisionControlManagerPlugin
        @param revision_control_manager_plugin: The revision control manager plugin.
        """

        self.revision_control_manager_plugin = revision_control_manager_plugin

        self.revision_control_adapter_plugins_map = {}

    def load_revision_control_manager(self, adapter_name, revision_control_parameters):
        """
        Creates a revision control manager for the specified adapter name.

        @type adapter_name: String
        @param adapter_name: The name of the adapter for loading the revision control manager
        @type revision_control_parameters: Dictionary
        @param revision_control_parameters: The parameters with which to load revision control manager
        """

        # retrieves the first revision control manager adapter for the specified adapter name
        revision_control_adapter_plugin = self.get_revision_control_adapter_plugin(adapter_name)

        # creates the revision control adapter using the retrieved adapter plugin
        revision_control_adapter = RevisionControlAdapter(revision_control_adapter_plugin)

        # loads the revision control adapter with the specified revision control parameters
        revision_control_adapter.load(revision_control_parameters)

        # returns the create revision control adapter
        return revision_control_adapter

    def revision_control_adapter_load(self, revision_control_adapter_plugin):
        # retrieves the plugin adapter name
        adapter_name = revision_control_adapter_plugin.get_adapter_name()

        self.revision_control_adapter_plugins_map[adapter_name] = revision_control_adapter_plugin

    def revision_control_adapter_unload(self, revision_control_adapter_plugin):
        # retrieves the plugin adapter name
        adapter_name = revision_control_adapter_plugin.get_adapter_name()

        del self.revision_control_adapter_plugins_map[adapter_name]

    def get_revision_control_adapter_plugin(self, adapter_name):
        # tries to retrieve the adapter plugin
        adapter_plugin = self.revision_control_adapter_plugins_map.get(adapter_name, None)

        # in case the adapter name is not found in the revision control adapter
        # plugins map
        if not adapter_plugin:
            # raises the revision control adapter not found exception
            raise revision_control_manager_exceptions.RevisionControlAdapterNotFoundException("no revision control adapter for adapter name: " + adapter_name)

        # returns the adapter plugin
        return adapter_plugin

class RevisionControlAdapter:

    revision_control_adapter_plugin = None
    """ The revision control manager adapter plugin to use """

    revision_control_parameters = {}
    """ The revision control parameters used to configure the interaction with the adapter plugins """

    _revision_control_reference = None
    """ The internal revision control reference, used by the revision control manager adapter plugin """

    def __init__(self, revision_control_adapter_plugin):
        """
        The constructor of the class.

        @type revision_control_adapter_plugin: RevisionControlAdapterPlugin
        @param revision_control_adapter_plugin: The revision control
        adapter plugin.
        """

        # stores the revision control manager adapter plugin
        self.revision_control_adapter_plugin = revision_control_adapter_plugin

        # initializes the revision control parameters
        self.revision_control_parameters = {}

        # initializes the revision control reference
        self._revision_control_reference = None

    def load(self, revision_control_parameters):
        """
        Loads the revision control adapter.

        @type revision_control_parameters: Dictionary
        @param revision_control_parameters: The parameters used
        in the initialization of the adapter.
        """

        # sets the revision control parameters
        self.revision_control_parameters = revision_control_parameters

        # creates the revision control reference using the configured plugin
        self._revision_control_reference = self.revision_control_adapter_plugin.create_revision_control_reference(revision_control_parameters)

    def add(self, resource_identifiers, recurse):
        """
        Schedules a set of resources for addition to the repository.

        @type resource_identifiers: List
        @param resource_identifiers: The list of resource identifiers.
        @type recurse: Boolean
        @param recurse: Indicates if a directory's children are to be recursively added.
        """

        return self.revision_control_adapter_plugin.add(self._revision_control_reference, resource_identifiers, recurse)

    def checkout(self, source, destination):
        """
        Performs a checkout from the given source into
        the defined destination

        @type source: String
        @param source: The source path to be used.
        @type destination: String
        @param destination: The destination of the checkout.
        """

        return self.revision_control_adapter_plugin.checkout(self._revision_control_reference, source, destination)

    def update(self, resource_identifiers, revision):
        """
        Update working directory.

        @type resource_identifiers: List
        @param resource_identifiers: The list of resource identifiers.
        @type revision: Revision
        @param revision: The revision to update to.
        @rtype: Revision
        @return: The updated revision.
        """

        return self.revision_control_adapter_plugin.update(self._revision_control_reference, resource_identifiers, revision)

    def commit(self, resource_identifiers, commit_message):
        """
        Commit the specified files or all outstanding changes.

        @type resource_identifiers: List
        @param resource_identifiers: The list of resource identifiers.
        @type commit_message: String
        @param commit_message: The message describing the commit.
        @rtype: Revision
        @return: The updated revision.
        """

        return self.revision_control_adapter_plugin.commit(self._revision_control_reference, resource_identifiers, commit_message)

    def log(self, resource_identifiers, start_revision, end_revision):
        """
        Show revision history of entire repository or files.
        """

        return self.revision_control_adapter_plugin.log(self._revision_control_reference, resource_identifiers, start_revision, end_revision)

    def log_time(self, resource_identifiers, start_time, end_time):
        """
        Show revision history inside a time interval.

        @type resource_identifiers: List
        @param resource_identifiers: The list of resource identifiers.
        @type start_time: int
        @param start_time: The timestamp for the start date for the time interval.
        @type end_time: int
        @param end_time: The timestamp for the end date for the time interval.
        """

        return self.revision_control_adapter_plugin.log_time(self._revision_control_reference, resource_identifiers, start_time, end_time)

    def status(self, resource_identifiers):
        """
        Retrieves the status of the provided resource identifiers.
        """

        return self.revision_control_adapter_plugin.status(self._revision_control_reference, resource_identifiers)

    def diff(self, resource_identifiers, revision_1, revision_2):
        """
        Retrieves the diff between the specified revisions for the specified resources.
        """

        return self.revision_control_adapter_plugin.diff(self._revision_control_reference, resource_identifiers, revision_1, revision_2)

    def diff_summary(self, resource_identifiers, revision_1, revision_2):
        """
        Retrieves the diff summary between the specified revisions for the specified resources.
        """

        return self.revision_control_adapter_plugin.diff_summary(self._revision_control_reference, resource_identifiers, revision_1, revision_2)

    def cleanup(self, resource_identifiers):
        """
        Cleans up any locks in the working copy at path.
        Typically these locks result from a failed or interrupted operation.

        @type resource_identifiers: List
        @param resource_identifiers: The list of resource identifiers.
        """

        return self.revision_control_adapter_plugin.cleanup(self._revision_control_reference, resource_identifiers)

    def cleanup_deep(self, resource_identifiers):
        """
        Cleans up any locks in the working copy at path.
        Typically these locks result from a failed or interrupted operation.
        Recursively double checks for resource which remain locked.
        Useful for dealing with locked external resources.

        @type resource_identifiers: List
        @param resource_identifiers: The list of resource identifiers.
        """

        return self.revision_control_adapter_plugin.cleanup_deep(self._revision_control_reference, resource_identifiers)

    def remove(self, resource_identifiers):
        """
        Schedules a set of resources for removal from the repository.

        @type resource_identifiers: List
        @param resource_identifiers: The list of resource identifiers.
        """

        return self.revision_control_adapter_plugin.remove(self._revision_control_reference, resource_identifiers)

    def revert(self, resource_identifiers):
        """
        Cleans up any locks in the working copy at path.
        Typically these locks result from a failed or interrupted operation.


        @type resource_identifiers: List
        @param resource_identifiers: The list of resource identifiers.
        """

        return self.revision_control_adapter_plugin.revert(self._revision_control_reference, resource_identifiers)

    def remove_unversioned(self, resource_identifiers):
        """
        Removes unversioned files from the specified resources.
        """

        return self.revision_control_adapter_plugin.remove_unversioned(self._revision_control_reference, resource_identifiers)

    def get_resources_revision(self, resource_identifiers, revision):
        """
        Retrieves the content of the specified resources in the specified revision.
        """

        return self.revision_control_adapter_plugin.get_resources_revision(self._revision_control_reference, resource_identifiers, revision)

    def create_revision(self):
        """
        Creates a new revision object.

        @rtype: Revision
        @return: A new revision.
        """

        return Revision()

class Revision:
    """
    The abstract revision class.
    """

    number = None
    """ The revision number """

    identifier = None
    """ The identifier of the revision """

    date = None
    """ The revision datetime.datetime date """

    timestamp = None
    """ The revision utc timestamp """

    author = "none"
    """ The revision author """

    message = None
    """ The revision message """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def get_number(self):
        """
        Retrieves the number.

        @rtype: int
        @return: The number.
        """

        return self.number

    def set_number(self, number):
        """
        Sets the number.

        @type number: int
        @param number: The number.
        """

        self.number = number

    def get_identifier(self):
        """
        Retrieves the identifier.

        @rtype: String
        @return: The identifier.
        """

        return self.identifier

    def set_identifier(self, identifier):
        """
        Sets the identifier.

        @type identifier: String
        @param identifier: The identifier.
        """

        self.identifier = identifier

    def get_date(self):
        """
        Retrieves the date.

        @rtype: datetime
        @return: The revision date.
        """

        return self.date

    def set_date(self, date):
        """
        Sets the date.

        @type date: datetime
        @param date: The date.
        """

        self.date = date

    def get_timestamp(self):
        """
        Retrieves the timestamp.

        @rtype: int
        @return: The date as an utc timestamp.
        """

        return self.timestamp

    def set_timestamp(self, timestamp):
        """
        Sets the timestamp.

        @type timestamp: int
        @param timestamp: The utc timestamp for the revision.
        """

        # sets the timestamp
        self.timestamp = timestamp

    def get_author(self):
        """
        Retrieves the author.

        @rtype: String
        @return: The author.
        """

        return self.author

    def set_author(self, author):
        """
        Sets the author.

        @type author: String
        @param author: The author.
        """

        self.author = author

    def get_message(self):
        """
        Retrieves the message.

        @rtype: String
        @return: The message.
        """

        return self.message

    def set_message(self, message):
        """
        Sets the message.

        @type message: String
        @param message: The message.
        """

        self.message = message

    def get_revision_map(self):
        """
        Retrieves the revision map for the current revision.

        @rtype: Dictionary
        @return: The revision map.
        """

        # retrieves the number
        number = self.get_number()

        # retrieves the identifier
        identifier = self.get_identifier()

        # retrieves the date
        date = self.get_date()

        # retrieves the author
        author = self.get_author()

        # retrieves the message
        message = self.get_message()

        # creates the revision map
        revision_map = {
            NUMBER_VALUE : number,
            IDENTIFIER_VALUE : identifier,
            DATE_VALUE : date,
            AUTHOR_VALUE : author,
            MESSAGE_VALUE : message
        }

        # returns the created revision map
        return revision_map
