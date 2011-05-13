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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

import mercurial.hg
import mercurial.ui
import mercurial.patch
import mercurial.cmdutil

ADAPTER_NAME = "hg"
""" The name for the revision control adapter """

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

MERCURIAL_RESOLVED_STATE_VALUE = "r"
""" The state signaling a conflict has been resolved """

REVISION_RANGE_SEPARATOR = ":"
""" The separator for revisions in revision ranges """

class RevisionControlMercurialAdapter:
    """
    The revision control mercurial adapter class.
    """

    revision_control_mercurial_adapter_plugin = None
    """ The revision control mercurial adapter plugin """

    mercurial_user_interface = None
    """ The mercurial user interface object """

    def __init__(self, revision_control_mercurial_adapter_plugin):
        """
        Constructor of the class.

        @type revision_control_mercurial_adapter_plugin: RevisionControlMercurialAdapter
        @param revision_control_mercurial_adapter_plugin: The revision control mecurial adapter plugin.
        """

        # sets the mercurial adapter plugin
        self.revision_control_mercurial_adapter_plugin = revision_control_mercurial_adapter_plugin

        # initializes the mercurial user interface
        self.mercurial_user_interface = mercurial.ui.ui()

    def create_revision_control_reference(self, revision_control_parameters):
        # retrieves the repository path parameter
        repository_path_parameter = revision_control_parameters["repository_path"]

        # retrieves the repository
        repository = self.get_repository(repository_path_parameter)

        # returns the repository as the revision control reference
        return repository

    def add(self, revision_control_reference, resource_identifiers, recurse):
        raise Exception("method not implemented")

    def update(self, revision_control_reference, resource_identifiers, revision):
        if revision:
            # retrieves the change context for the specified identifier
            change_context = revision_control_reference[revision]

            # retrieves the node
            node = change_context.node()
        else:
            # the node defaults to true
            node = None

        # updates the working directory to node
        mercurial.hg.update(revision_control_reference, node)

        # retrieves the change context for the working directory
        update_change_context = revision_control_reference[None]

        # retrieves the revision node
        update_node = update_change_context.node()

        return update_node

    def commit(self, revision_control_reference, resource_identifiers, commit_message):
        # retrieves the match for the resource identifier in the file system
        match = mercurial.cmdutil.match(revision_control_reference, resource_identifiers)

        # commits the retrieved match
        commit_change_context_node = revision_control_reference.commit(commit_message, None, None, match, None, None)

        # retrieves the change context for the working directory
        commit_change_context = revision_control_reference[commit_change_context_node]

        # creates the mercuial revision resulting from the commit
        commit_revision = self.create_revision(commit_change_context)

        return commit_revision

    def log(self, revision_control_reference, resource_identifiers, start_revision, end_revision):
        # an omitted first index defaults to zero
        if start_revision == None:
            start_revision = 0
        else:
            # @todo: find a better way to test for int compatible string
            try:
                start_revision = int(start_revision)
            except ValueError:
                start_revision = revision_control_reference[start_revision].rev()

        # an omitted second index defaults to the size of the repository being sliced.
        if end_revision == None:
            end_revision = len(revision_control_reference)
        else:
            # @todo: find a better way to test for int compatible string
            try:
                end_revision = int(end_revision)
            except ValueError:
                end_revision = revision_control_reference[end_revision].rev()

        # initializes the change context list
        change_contexts = []

        for revision_number in range(start_revision, end_revision + 1):
            # retrieves the change context for the current revision number
            change_context = revision_control_reference[revision_number]

            # appends the the current change context
            change_contexts.append(change_context)

        # adapts the change context to revisions
        revisions = [self.create_revision(change_context) for change_context in change_contexts]

        return revisions

    def log_time(self, revision_control_reference, resource_identifiers, start_time, end_time):
        raise Exception("not implemented in mercurial adapter")

    def status(self, revision_control_reference, resource_identifiers):
        # retrieves the working directory status
        status = revision_control_reference.status()

        return status

    def diff(self, revision_control_reference, resource_identifiers, revision_1, revision_2):
        # initializes the options map
        options = {}

        # creates a match object for the specified resource if any
        match = mercurial.cmdutil.match(revision_control_reference, resource_identifiers, options)

        # diffs the specified revisions
        diff_iterator = mercurial.patch.diff(revision_control_reference, revision_1, revision_2, match, None)

        # retrieves the list of diffs from the iterator
        diffs = list(diff_iterator)

        # retrieves the computed diffs
        return diffs

    def remove(self, revision_control_reference, resource_identifiers):
        raise Exception("method not implemented")

    def get_resources_revision(self, revision_control_reference, resource_identifier, revision):
        # an omitted second index defaults to the size of the repository being sliced.
        if not revision == None:
            # @todo: find a better way to test for int compatible string
            try:
                revision = int(revision)
            except ValueError:
                revision = revision_control_reference[revision].rev()


        # retrieves the change context for the specified revision
        change_context = revision_control_reference[revision]

        # initializes the options map
        options = {}

        # creates a match object for the specified resource if any
        match = mercurial.cmdutil.match(revision_control_reference, resource_identifier, options)

        # initializes the return list
        resources_revision = []

        # for each path in the change context within match
        for absolute_path in change_context.walk(match):
            # retrieves the file context for the current match
            file_context = change_context[absolute_path]

            # retrieves the data contents of the file context
            data = file_context.data()

            # appends the file data to the resources revision list
            resources_revision.append(data)

        # returns the list of resource contents for the specified revision
        return resources_revision

    def get_repository(self, path):
        # finds the repository path
        repository_path = self.find_repository_path(path)

        # creates a repository object for the retrieved path
        repository = mercurial.hg.repository(self.mercurial_user_interface, repository_path)

        # returns the repository
        return repository

    def find_repository_path(self, path):
        """
        Finds a repository in or above the specified path.
        """
        while not os.path.isdir(os.path.join(path, ".hg")):
            old_path, path = path, os.path.dirname(path)
            if path == old_path:
                return None

        return path

    def get_adapter_name(self):
        return ADAPTER_NAME

    def create_revision(self, change_context):
        # creates the revision object from the change context
        revision = MercurialRevision(change_context)

        # returns the revision objects
        return revision

class MercurialRevision:
    """
    The mercurial revision class.
    """

    _mercurial_change_context = None
    """ The adapted mercurial change context """

    def __init__(self, mercurial_change_context):
        # sets the adapted mercurial change context
        self._mercurial_change_context = mercurial_change_context

    def __str__(self):
        # retrieves the revision number
        revision_number = self.get_number()

        # retrieves the revision identifier
        revision_identifier = self.get_identifier()

        # builds the revision_string
        if revision_number:
            revision_string = "%d:%s" % (revision_number, revision_identifier)
        else:
            revision_string = revision_identifier

        # returns the revision string
        return revision_string

    def get_identifier(self):
        # retrieves the revision identifier
        identifier = str(self._mercurial_change_context)

        # returns the retrieved identifier
        return identifier

    def get_number(self):
        # retrieves the revision number from the change context
        number = self._mercurial_change_context.rev()

        # returns the retrieved number
        return number

    def get_date(self):
        # retrieves the mercurial change context date tuple
        mercurial_change_context_date_tuple = self._mercurial_change_context.date()

        # retrieves the timestamp from the tuple
        date = mercurial_change_context_date_tuple[0]

        # returns the date
        return date

    def get_author(self):
        # retrieves the author from the change context
        author = self._mercurial_change_context.user()

        # returns the author
        return author

    def get_message(self):
        # retrieves the message from the change context
        message = self._mercurial_change_context.description()

        # returns the message
        return message

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
