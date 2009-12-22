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

import bzrlib.workingtree

ADAPTER_NAME = "bzr"
""" The name for the bazaar revision control adapter """

class RevisionControlBazaarAdapter:
    """
    The revision control bazaar adapter class.
    """

    revision_control_bazaar_adapter_plugin = None
    """ The revision control bazaar adapter plugin """

    bazaar_client = None
    """ The bazaar client object """

    def __init__(self, revision_control_bazaar_adapter_plugin):
        """
        Constructor of the class.

        @type revision_control_bazaar_adapter_plugin: RevisionControlBazaarAdapter
        @param revision_control_bazaar_adapter_plugin: The revision control mecurial adapter plugin.
        """

        # sets the bazaar adapter plugin
        self.revision_control_bazaar_adapter_plugin = revision_control_bazaar_adapter_plugin

    def create_revision_control_reference(self, revision_control_parameters):
        # retrieves the repository path parameter
        repository_path_parameter = revision_control_parameters["repository_path"]

        # creates the appropriate working tree
        working_tree = bzrlib.workingtree.WorkingTree.open(repository_path_parameter)

        # returns the working tree as the revision control reference
        return working_tree

    def update(self, revision_control_reference, resource_identifiers, revision):
        # updates the whole working tree
        revision_control_reference.update()

        # retrieves the last revision identifier
        last_revision_identifier = revision_control_reference.last_revision()

        # creates the standard revision
        update_revision = self.create_revision(revision_control_reference, last_revision_identifier)

        # returns the revision after the update
        return update_revision

    def commit(self, revision_control_reference, resource_identifiers, commit_message):
        # retrieves the delta from the basis tree
        delta = revision_control_reference.changes_from(revision_control_reference.basis_tree())

        # in case no changes exist
        if not delta.has_changed():
            return None

        # commits the whole working tree
        commit_revision_identifier = revision_control_reference.commit(commit_message)

        # creates the standard revision
        commit_revision = self.create_revision(revision_control_reference, commit_revision_identifier)

        # returns the revision after the commit
        return commit_revision

    def create_revision(self, revision_control_reference, revision_identifier):
        # creates the revision object
        revision = Revision()

        # splits the revision attributes in the revision identifier
        revision_attributes = revision_identifier.split('-')

        # retrieves the attributes
        author = revision_attributes[0]
        date  = revision_attributes[1]
        identifier = revision_attributes[2]

        # retrieves the revision number from the working tree branch
        number = revision_control_reference.branch.revision_id_to_revno(revision_identifier)

        # sets the attributes in the revision
        revision.set_identifier(identifier)
        revision.set_number(number)
        revision.set_date(date)
        revision.set_author(author)
        revision.set_message("<commit message goes here>")

        return revision

    def get_adapter_name(self):
        return ADAPTER_NAME

class Revision:
    """
    The generic revision for revision control management.
    """

    identifier = None
    """ The revision identifier """

    number = None
    """ The revision number """

    date = None
    """ The revision date """

    author = "none"
    """ The revision author """

    message = None
    """ The revision message """

    def get_identifier(self):
        return self.identifier

    def set_identifier(self, identifier):
        self.identifier = identifier

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def get_date(self, date):
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
