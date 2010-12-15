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
import pysvn
import types
import datetime

import colony.libs.path_util

import revision_control_subversion_adapter_exceptions

ADAPTER_NAME = "svn"
""" The name for the subversion revision control adapter """

DEFAULT_REVISION_KIND = pysvn.opt_revision_kind.number
""" The default revision kind """

USERNAME_VALUE = "username"
""" The value for the username """

DEFAULT_USERNAME = "username"
""" The default username """

PASSWORD_VALUE = "password"
""" The value for the password """

DEFAULT_PASSWORD = "password"
""" The default password """

SAVE_USERNAME_PASSWORD_VALUE = "save_username_password"
""" The save username password value """

DEFAULT_SAVE_USERNAME_PASSWORD = True
""" The default save username password value """

HEAD_REVISION_IDENTIFIER = "head_revision"
""" The head revision identifier """

WORKING_COPY_REVISION_IDENTIFIER = "working_copy_revision"
""" The working copy revision identifier """

DEFAULT_PYSVN_ENCODING = "utf-8"
""" The default encoding for the svn adapter """

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
        # creates a new subversion revision control reference
        revision_control_reference = SubversionRevisionControlReference()

        # enables support for authentication
        self._enable_authentication_support(revision_control_reference, revision_control_parameters)

        # returns the svn client as the revision control reference
        return revision_control_reference

    def add(self, revision_control_reference, resource_identifiers, recurse):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # performs the svn add
        pysvn_client.add(resource_identifiers, recurse)

    def checkout(self, revision_control_reference, source, destination):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # performs the svn checkout
        pysvn_client.checkout(source, destination)

        # creates the template for the working copy revision
        head_subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.head)

        # determines the current revision by retrieving the property list for the head revision
        checkout_subversion_revision, _prop_dict = pysvn_client.revproplist(source, head_subversion_revision)

        # creates the subversion revision resulting from the check out
        checkout_revision = self.create_revision_subversion_revision(checkout_subversion_revision)

        # returns the checked out revision
        return checkout_revision

    def update(self, revision_control_reference, resource_identifiers, revision):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # retrieves the first resource identifier
        resource_identifier = resource_identifiers[0]

        # in case a revision is not specified
        if revision == None:
            # updates to the head revision
            subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.head)
        # otherwise
        else:
            # creates the subversion revision
            subversion_revision = self.create_subversion_revision_manager_revision(revision)

        # performs the update
        update_subversion_revisions = pysvn_client.update(resource_identifier, True, subversion_revision)

        # retrieves the first of the returned revisions
        update_subversion_revision = update_subversion_revisions[0]

        # creates the subversion revision resulting from the update
        update_revision = self.create_revision_subversion_revision(update_subversion_revision)

        # returns the update revision
        return update_revision

    def commit(self, revision_control_reference, resource_identifiers, commit_message):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # retrieves the result revisions
        commit_subversion_revision = pysvn_client.checkin(resource_identifiers, commit_message)

        # in case none is returned
        if not commit_subversion_revision:
            # raise the no changes in working copy exception
            raise revision_control_subversion_adapter_exceptions.WorkingCopyCleanException("no changes in working copy")

        # creates the subversion revision resulting from the commit
        commit_revision = self.create_revision_subversion_revision(commit_subversion_revision)

        # returns the commit revision
        return commit_revision

    def log(self, revision_control_reference, resource_identifiers, start_revision, end_revision):
        # in case the start revision is not specified
        if start_revision == None:
            # starts with the head of the repository
            start_subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.head)
        else:
            # creates a subversion adapter revision from the specified start revision
            start_subversion_revision = self.create_subversion_revision_manager_revision(start_revision)

        # in case the end revision is not specified
        if end_revision == None:
            # ends on the first revision of the repository
            end_subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.number, 0)
        else:
            # creates a subversion adapter revision from the specified end revision
            end_subversion_revision = self.create_subversion_revision_manager_revision(end_revision)

        # retrieves the log messages
        log_messages = self._log(revision_control_reference, resource_identifiers, start_subversion_revision, end_subversion_revision)

        # returns the retrieved log messages
        return log_messages

    def log_time(self, revision_control_reference, resource_identifiers, start_time, end_time):
        # in case the start revision is not specified
        if start_time == None:
            # starts with the head of the repository
            start_subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.head)
        else:
            # creates a subversion adapter revision from the specified start revision
            start_subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.date, start_time)

        # in case the end revision is not specified
        if end_time == None:
            # ends on the first revision of the repository
            end_subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.number, 0)
        else:
            # creates a subversion adapter revision from the specified end revision
            end_subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.date, end_time)

        # retrieves the log messages
        log_messages = self._log(revision_control_reference, resource_identifiers, start_subversion_revision, end_subversion_revision)

        # creates the filtered log messages list
        filtered_log_messages = list(log_messages)

        # removes the log messages
        # which are before the start time
        for log_message in log_messages:
            # in case the log message is before the start time
            if log_message.time < start_time:
                # removes the log message from the list
                filtered_log_messages.remove(log_message)
            # otherwise
            else:
                # skips further check (assumes sorted by time)
                break

        # removes the log messages
        # which are after the end time
        for log_message in reversed(log_messages):
            # in case the log message is after the start time
            if log_message.time > end_time:
                # removes the log message from the list
                filtered_log_messages.remove(log_message)
            # otherwise
            else:
                # skips further check (assumes reversely sorted by time)
                break

        # returns the retrieved log messages
        return filtered_log_messages

    def _log(self, revision_control_reference, resource_identifiers, start_subversion_revision, end_subversion_revision):
        # indicates if the changed_paths dictionary should be filled with a list of changed paths
        discover_changed_paths = False

        # if strict_node_history is set, log entries will not cross copies
        strict_node_history = True

        # the maximum number of log messages: 0 means all
        limit = 0

        # peg revision indicates in which revision is the resource valid
        peg_revision = pysvn.Revision(pysvn.opt_revision_kind.unspecified)

        # not discussed in the official pysvn documentation
        include_merged_revisions = False

        # revision properties is the list of revision properties to be returned
        revision_properties = None

        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # the list of log messages to retrieve
        log_messages = []

        # for each of the specified resources
        for resource_identifier in resource_identifiers:
            # retrieves the log messages for the specified parameters
            resource_log_messages = pysvn_client.log(resource_identifier, end_subversion_revision, start_subversion_revision, discover_changed_paths, strict_node_history, limit, peg_revision, include_merged_revisions, revision_properties)

            # reverse the order of the obtained messages
            resource_log_messages.reverse()

            # extends the log messages list with the retrieved log messages
            log_messages.extend(resource_log_messages)

        # convert the log messages to the standard revision control manager format
        revisions = self.adapt_log_messages(log_messages)

        return revisions

    def diff(self, revision_control_reference, resource_identifiers, revision_1, revision_2):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # retrieves the plugin manager
        plugin_manager = self.revision_control_subversion_adapter_plugin.manager

        # retrieves the temporary path
        temporary_path = plugin_manager.get_temporary_path()

        # retrieves the urls or paths
        url_or_path_1 = resource_identifiers[0]
        url_or_path_2 = url_or_path_1

        # in case the first revision is not specified
        if revision_1 == None:
            # uses the base revision
            subversion_revision_1 = pysvn.Revision(pysvn.opt_revision_kind.base)
        # otherwise
        else:
            # creates the subversion revision
            subversion_revision_1 = self.create_subversion_revision_manager_revision(revision_1)

        # in case the second revision is not specified
        if revision_2 == None:
            # uses the working revision
            subversion_revision_2 = pysvn.Revision(pysvn.opt_revision_kind.working)
        # otherwise
        else:
            # creates the subversion revision
            subversion_revision_2 = self.create_subversion_revision_manager_revision(revision_2)

        # processes the diff
        diff_string = pysvn_client.diff(temporary_path, url_or_path_1, subversion_revision_1, url_or_path_2, subversion_revision_2)

        # splits the diffs in the single diff string
        diffs = diff_string.split("\n")

        # returns the computed diff
        return diffs

    def cleanup(self, revision_control_reference, resource_identifiers):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # iterates over all the resource identifiers
        for resource_identifier in resource_identifiers:
            # cleans up any locks at the current resource
            pysvn_client.cleanup(resource_identifier)

    def cleanup_deep(self, revision_control_reference, resource_identifiers):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # iterates over all the resource identifiers
        for resource_identifier in resource_identifiers:
            # cleans up any locks at the current (base) resource
            pysvn_client.cleanup(resource_identifier)

            # retrieves the status for the current resource
            status_list = pysvn_client.status(resource_identifier)

            # retrieves the list of resources which remain locked
            locked_resource_identifiers = [status.path for status in status_list if status.is_locked]

            # recursively calls the cleanup method over the
            # locked resource identifiers
            self.cleanup(revision_control_reference, locked_resource_identifiers)

    def remove(self, revision_control_reference, resource_identifiers):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # performs the svn remove
        pysvn_client.remove(resource_identifiers)

    def revert(self, revision_control_reference, resource_identifiers):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # reverts pending changes
        pysvn_client.revert(resource_identifiers, recurse = True)

        # removes unversioned files
        self.remove_unversioned(revision_control_reference, resource_identifiers)

    def remove_unversioned(self, revision_control_reference, resource_identifiers):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # for all the specified resources
        for resource_identifier in resource_identifiers:
            # retrieves the status for the current resource
            status_list = pysvn_client.status(resource_identifier)

            # for each status in the status list
            # looks for unversioned resources
            for status in status_list:
                # in case the resource is versioned
                if not status.is_versioned or status.text_status == pysvn.wc_status_kind.ignored:
                    # retrieves the resource path
                    unversioned_resource_path = status.path

                    # removes the unversioned resource
                    self.remove_resource_path(unversioned_resource_path)

    def get_resources_revision(self, revision_control_reference, resource_identifiers, revision):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # in case the revision is not specified
        if revision == None:
            # uses the working copy revision
            subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.working)
        else:
            # creates the subversion revision
            subversion_revision = self.create_subversion_revision_manager_revision(revision)

        # initializes the resources revision list
        resources_revision = []

        # initializes the resources revisions list
        for url_or_path in resource_identifiers:
            # retrieves the file contents
            file_text = pysvn_client.cat(url_or_path, subversion_revision)

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

        # decodes the author field into unicode
        author_decoded = author.decode(DEFAULT_PYSVN_ENCODING)

        # decodes the message field
        message_decoded = message.decode(DEFAULT_PYSVN_ENCODING)

        # creates the revision
        revision = self.create_revision_subversion_revision(subversion_revision)

        # sets the author in the revision
        revision.set_author(author_decoded)

        # sets the date in the revision
        revision.set_date_utc_timestamp(date)

        # sets the message in the revision
        revision.set_message(message_decoded)

        # returns the assembled revision
        return revision

    def create_revision_subversion_revision(self, subversion_revision):
        # creates a new subversion adapter revision
        subversion_adapter_revision = SubversionAdapterRevision()

        # sets the subversion revision in the adapter revision
        subversion_adapter_revision.set_subversion_revision(subversion_revision)

        # returns the revision object
        return subversion_adapter_revision

    def create_subversion_revision_manager_revision(self, manager_revision):
        # retrieves the manager revision number
        manager_revision_number = None

        # retrieves the manager revision date
        manager_revision_date = None

        # retrieves the manager revision identifier
        manager_revision_identifier = None

        # in case the revision is empty
        if manager_revision == None:
            # creates an unspecified subversion revision
            subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.unspecified)

            # returns the subversion revision
            return subversion_revision

        # in case the revision is specified as an integer
        if type(manager_revision) == types.IntType:
            # uses the provided revision as the manager revision
            manager_revision_number = manager_revision
        elif type(manager_revision) in types.StringTypes:
            # casts the manager revision as an integer
            manager_revision_number = int(manager_revision)
        # otherwise
        else:
            # retrieves the manager revision number
            manager_revision_number = manager_revision.get_number()

            # retrieves the manager revision date
            manager_revision_date = manager_revision.get_date()

            # retrieves the manager revision identifier
            manager_revision_identifier = manager_revision.get_identifier()

        # in case a revision number is specified
        if not manager_revision_number == None:
            # creates the subversion revision
            subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.number, manager_revision_number)
        # in case a date is specified
        elif not manager_revision_date == None:
            # creates the subversion revision
            subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.date, manager_revision_date)
        # in case the head revision is specified
        elif manager_revision_identifier == HEAD_REVISION_IDENTIFIER:
            # creates the subversion revision
            subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.head)
        # in case the working copy revision is specified
        elif manager_revision_identifier == WORKING_COPY_REVISION_IDENTIFIER:
            # creates the subversion revision
            subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.working)
        # in case the revision identifier is not null
        elif not manager_revision_identifier == None:
            # uses the identifier as revision number
            manager_revision_number = int(manager_revision_identifier)

            # creates the subversion revision
            subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.number, manager_revision_number)
        # otherwise
        else:
            # creates an unspecified subversion revision
            subversion_revision = pysvn.Revision(pysvn.opt_revision_kind.unspecified)

        # returns the created subversion revision
        return subversion_revision

    def remove_resource_path(self, resource_path):
        # in the case the current node is of directory kind
        if os.path.isdir(resource_path):
            # removes the whole directory tree
            colony.libs.path_util.remove_directory(resource_path)
        else:
            # removes the resource
            os.remove(resource_path)

    def _enable_authentication_support(self, revision_control_reference, revision_control_parameters):
        # retrieves the pysvn client from the revision control reference
        pysvn_client = revision_control_reference.pysvn_client

        # retrieves the user name from the revision control parameters
        username = revision_control_parameters.get(USERNAME_VALUE, DEFAULT_USERNAME)

        # retrieves the password from the revision control parameters
        password = revision_control_parameters.get(PASSWORD_VALUE, DEFAULT_PASSWORD)

        # retrieves the option for saving username and password
        save_username_password = revision_control_parameters.get(SAVE_USERNAME_PASSWORD_VALUE, DEFAULT_SAVE_USERNAME_PASSWORD)

        # sets the username in the revision control reference
        revision_control_reference.username = username

        # sets the password in the revision control reference
        revision_control_reference.password = password

        # sets the save username password in the revision control reference
        revision_control_reference.save_username_password = save_username_password

        # initializes the get login callback
        def get_login(realm, _username, _may_save):
            # in case this is not the login first attempt
            # and no successful logins occurred
            if revision_control_reference.first_login_attempt:
                revision_control_reference.first_login_attempt = False
            # in case this is not the first attempt
            # but no successful login ocurred
            elif not revision_control_reference.successful_login:
                # signals a wrong login credentials exception
                return False, "none", "none", False

            # in case a user name and password are defined
            # and any previous try did not fail
            if revision_control_reference.username and revision_control_reference.password:
                # indicates credentials are available
                retcode = True
            else:
                # indicates credentials are not available
                retcode = False

            # returns the pysvn login tuple
            return retcode, revision_control_reference.username, revision_control_reference.password, revision_control_reference.save_username_password

        # sets the get login callback for the client
        pysvn_client.callback_get_login = get_login

class SubversionAdapterRevision:
    """
    The subversion revision class.
    """

    _subversion_revision = None
    """ The adapted subversion revision """

    date = None
    """ The revision datetime.datetime date """

    time = None
    """ The revision timestamp """

    author = "none"
    """ The revision author """

    message = None
    """ The revision message """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

    def __str__(self):
        # uses the subversion revision number as the string representation
        return str(self._subversion_revision.number)

    def get_identifier(self):
        # returns the revision number
        return self._subversion_revision.number

    def get_number(self):
        return self._subversion_revision.number

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date

    def set_date_utc_timestamp(self, date_utc_timestamp):
        # sets the timestamp
        self.time = date_utc_timestamp

        # sets the date datetime
        self.date = datetime.datetime.utcfromtimestamp(date_utc_timestamp)

    def get_author(self):
        return self.author

    def set_author(self, author):
        self.author = author

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message

    def get_subversion_revision(self):
        return self._subversion_revision

    def set_subversion_revision(self, subversion_revision):
        """
        Sets the underlying subversion revision in the adapter revision.

        @type subversion_revision: CSubversionRevision
        @param subversion_revision: The adapted subversion revision.
        """

        # sets the subversion revision
        self._subversion_revision = subversion_revision

class SubversionRevisionControlReference:
    """
    The subversion revision control reference class.
    """

    pysvn_client = None
    """ The pysvn client used to contact the repository """

    username = None
    """ The username used for authentication """

    password = None
    """ The password used for authentication """

    save_username_password = None
    """ Indicates if saving username and password data in the svn cache is allowed """

    first_login_attempt = None
    """ Indicates if a login attempt already occurred """

    successful_login = None
    """ Indicates if a login attempt already occurred """

    def __init__(self):
        # initializes the subversion client
        self.pysvn_client = pysvn.Client()

        # initializes the username
        self.username = DEFAULT_USERNAME

        # initializes the password
        self.password = DEFAULT_PASSWORD

        # initializes the save flag
        self.save_username_password = DEFAULT_SAVE_USERNAME_PASSWORD

        # initializes the status
        self.first_login_attempt = True
        self.successful_login = False
