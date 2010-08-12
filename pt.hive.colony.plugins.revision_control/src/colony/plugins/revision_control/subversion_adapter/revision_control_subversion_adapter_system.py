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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import pysvn

ADAPTER_NAME = "svn"
""" The name for the subversion revision control adapter """

DEFAULT_REVISION_KIND = pysvn.opt_revision_kind.number
""" The default revision kind """

class RevisionControlSubversionAdapter:
    """
    The revision control subversion adapter class.
    """

    revision_control_subversion_adapter_plugin = None
    """ The revision control subversion adapter plugin """

    def __init__(self, revision_control_subversion_adapter_plugin):
        """
        Constructor of the class.

        @type revision_control_subversion_adapter_plugin: RevisionControlSubversionAdapter
        @param revision_control_subversion_adapter_plugin: The revision control mecurial adapter plugin.
        """

        # sets the subversion adapter plugin
        self.revision_control_subversion_adapter_plugin = revision_control_subversion_adapter_plugin

    def create_revision_control_reference(self, revision_control_parameters):
        # initializes the subversion client
        client = pysvn.Client()

        # returns the svn client as the revision control reference
        return client

    def checkout(self, revision_control_reference, source, destination):
        # performs the svn checkout
        print repr(revision_control_reference.checkout(source, destination))

    def update(self, revision_control_reference, resource_identifiers, revision):
        # retrieves the first resource identifier
        resource_identifier = resource_identifiers[0]

        # in case a revision is specified
        if revision:
            # creates the subversion revision
            subversion_revision = pysvn.Revision(DEFAULT_REVISION_KIND, revision)
        else:
            # updates to the head revision
            subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.head)

        # performs the update
        update_subversion_revisions = revision_control_reference.update(resource_identifier, True, subversion_revision)

        # retrieves the first of the returned revisions
        update_subversion_revision = update_subversion_revisions[0]

        # retrieves the revision identifier
        update_revision = str(update_subversion_revision.number)

        return update_revision

    def commit(self, revision_control_reference, resource_identifiers, commit_message):
        # retrieves the result revisions
        commit_subversion_revision = revision_control_reference.checkin(resource_identifiers, commit_message)

        # creates the subversion revision resulting from the commit
        commit_revision = self.create_revision(commit_subversion_revision)

        # returns the commit revision
        return commit_revision

    def log(self, revision_control_reference, resource_identifiers, start_revision, end_revision):
        # the list of log messages to retrieve
        log_messages = []

        # the revision in which to start the log
        if not start_revision == None:
            start_subversion_revision = pysvn.Revision(DEFAULT_REVISION_KIND, start_revision)
        else:
            start_subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.head)

        # the revision in which to end the log
        if not end_revision == None:
            end_subversion_revision = pysvn.Revision(DEFAULT_REVISION_KIND, end_revision)
        else:
            end_subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.number, 0)

        # indicates if the changed_paths dictionary should be filled with a list of changed paths
        discover_changed_paths = False

        # if strict_node_history is set, log entries will not cross copies
        strict_node_history = True

        # the maximum number of log messages: 0 means all
        limit = 0

        # in case url_or_path no longer exists in the repos of WC, peg_revision can be specified with a revision where it did exist
        peg_revision = pysvn.Revision(pysvn.opt_revision_kind.unspecified)

        # not documented
        include_merged_revisions = False

        # revprops is a list of strings that name the revprops to be returned.
        revprops = None

        for resource_identifier in resource_identifiers:
            # retrieves the log messages for the specified parameters
            resource_log_messages = revision_control_reference.log(resource_identifier, end_subversion_revision, start_subversion_revision, discover_changed_paths, strict_node_history, limit, peg_revision, include_merged_revisions, revprops)

            # reverse the order of the obtained messages
            resource_log_messages.reverse()

            # extends the log messages list with the retrieved log messages
            log_messages.extend(resource_log_messages)

        # convert the log messages to the standard revision control manager format
        revisions = self.adapt_log_messages(log_messages)

        return revisions

    def diff(self, revision_control_reference, resource_identifiers, revision_1, revision_2):
        tmp_path = "/tmp"
        url_or_path = resource_identifiers[0]
        url_or_path_2 = url_or_path

        # the first revision
        if not revision_1 == None:
            subversion_revision_1 = pysvn.Revision(DEFAULT_REVISION_KIND, revision_1)
        else:
            subversion_revision_1 = pysvn.Revision(pysvn.opt_revision_kind.base)

        # the revision in which to end the log
        if not revision_2 == None:
            subversion_revision_2 = pysvn.Revision(DEFAULT_REVISION_KIND, revision_2)
        else:
            subversion_revision_2 = pysvn.Revision(pysvn.opt_revision_kind.working)

        # processes the diff
        diff_string = revision_control_reference.diff(tmp_path, url_or_path, subversion_revision_1, url_or_path_2, subversion_revision_2)

        # splits the diffs in the single diff string
        # @todo: split in a smarter fashion
        diffs = diff_string.split("\n")

        # returns the computed diff
        return diffs

    def get_resources_revision(self, revision_control_reference, resource_identifiers, revision):
        # the revision in which to end the log
        if not revision == None:
            subversion_revision = pysvn.Revision(DEFAULT_REVISION_KIND, revision)
        else:
            subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.working)

        # initializes the resources revision list
        resources_revision = []

        # initializes the resources revisions list
        for url_or_path in resource_identifiers:
            # retrieves the file contents
            file_text = revision_control_reference.cat(url_or_path, subversion_revision)

            # appends the file contents to the resources revision list
            resources_revision.append(file_text)

        # returns the retrieves resources revision list
        return resources_revision

    def get_adapter_name(self):
        return ADAPTER_NAME

    def adapt_log_messages(self, log_messages):
        # adapts the subversion log messages to the standard revision control manager log entries
        revisions = [self.adapt_log_message(log_message) for log_message in log_messages]

        # returns the adapted log entries
        return revisions

    def adapt_log_message(self, log_entry):
        # retrieves the log entry fields
        author = log_entry["author"]
        date = log_entry["date"]
        message = log_entry["message"]
        subversion_revision = log_entry["revision"]

        # creates the revision
        revision = self.create_revision(subversion_revision)

        # sets the author in the revision
        revision.set_author(author)

        # sets the date in the revision
        revision.set_date(date)

        # sets the message in the revision
        revision.set_message(message)

        # returns the assembled revision
        return revision

    def create_revision(self, subversion_revision):
        # wraps the binding's revision object into the adapter's revision object
        revision = SubversionRevision(subversion_revision)

        # returns the revision object
        return revision

class SubversionRevision:
    """
    The subversion revision class.
    """

    _subversion_revision = None
    """ The adapted subversion revision """

    date = None
    """ The revision date """

    author = "none"
    """ The revision author """

    message = None
    """ The revision message """

    def __init__(self, subversion_revision):
        """
        Constructor of the class.

        @type subversion_revision: CSubversionRevision
        @param subversion_revision: The adapted subversion revision.
        """

        # sets the adapted subversion revision
        self._subversion_revision = subversion_revision

    def __repr__(self):
        # uses the subversion revision number as the string representation
        return str(self._subversion_revision.number)

    def get_identifier(self):
        # retrieves the revision identifier from the subversion revision's string representation
        revision_identifier = str(self._subversion_revision)

        # returns the retrieved revision identifier
        return revision_identifier

    def get_number(self):
        return self._subversion_revision.number

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date

    def get_author(self):
        return self.author

    def set_author(self, author):
        self.author = author

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message
