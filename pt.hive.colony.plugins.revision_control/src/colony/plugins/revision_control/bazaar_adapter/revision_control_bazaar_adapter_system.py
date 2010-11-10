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

import bzrlib.diff
import bzrlib.bzrdir
import bzrlib.revisionspec
import bzrlib.builtins

import colony.libs.string_buffer_util

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

        # retrieves the bazaar dir containing the specified path
        bzr_dir, _unicode_path = bzrlib.bzrdir.BzrDir.open_containing(repository_path_parameter)

        # creates the appropriate working tree
        working_tree = bzr_dir.open_workingtree()

        # returns the working tree as the revision control reference
        return working_tree

    def add(self, revision_control_reference, resource_identifiers, recurse):
        raise Exception("method not implemented")

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

    def diff(self, revision_control_reference, resource_identifiers, revision_1, revision_2):
        # the list of bazaar revision specs
        bazaar_revision_specs = []

        # retrieves the first revision spec
        if not revision_1 == None:
            # creates the first bazaar revision spec
            bazaar_revision_spec_1 = bzrlib.revisionspec.RevisionSpec.from_string(revision_1)

            # appends the spec to the list of bazaar revision specs
            bazaar_revision_specs.append(bazaar_revision_spec_1)

        # retrieves the second revision spec
        if not revision_2 == None:
            # creates the second bazaar revision spec
            bazaar_revision_spec_2 = bzrlib.revisionspec.RevisionSpec.from_string(revision_2)

            # appends the spec to the list of bazaar revision specs
            bazaar_revision_specs.append(bazaar_revision_spec_2)

        # retrieves the tree to diff
        old_tree, new_tree, specific_files, _extra_trees = bzrlib.diff._get_trees_to_diff(resource_identifiers, bazaar_revision_specs, None, None, True)

        # creates the string buffer for the diffs
        diffs_string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # retrieves the diffs
        bzrlib.diff.show_diff_trees(old_tree, new_tree, diffs_string_buffer, specific_files)

        # retrieves the diffs string
        diffs_string = diffs_string_buffer.get_value()

        # retrieves the diffs list
        # @todo: parse this properly
        diffs = diffs_string.split("\n")

        # returns the computed diffs
        return diffs

    def remove(self, revision_control_reference, resource_identifiers):
        raise Exception("method not implemented")

    def get_resources_revision(self, revision_control_reference, resource_identifiers, revision):
        # retrieves the first revision spec
        if not revision == None:
            # creates the bazaar revision spec
            bazaar_revision_spec = bzrlib.revisionspec.RevisionSpec.from_string(revision)
        else:
            # otherwise the bazaar revision spec is none
            bazaar_revision_spec = None

        # creates the resources revision list
        resources_revision = []

        # for each specified resource
        for filename in resource_identifiers:
            # opens the containing tree or branch
            tree, branch, relpath = bzrlib.bzrdir.BzrDir.open_containing_tree_or_branch(filename)

            # locks the branch for read
            branch.lock_read()

            try:
                if tree == None:
                    # retrieves the basis tree for the branch
                    tree = branch.basis_tree()

                if bazaar_revision_spec:
                    # retrieves the revision tree
                    rev_tree = bzrlib.builtins._get_one_revision_tree("cat", [bazaar_revision_spec], branch = branch)
                else:
                    rev_tree = revision_control_reference

                # retrieves the old file id
                old_file_id = rev_tree.path2id(relpath)

                # retrieves the current file id
                current_file_id = tree.path2id(relpath)
                found = False
                if current_file_id is not None:
                    # then try with the actual file id
                    try:
                        content = rev_tree.get_file_text(current_file_id)
                        found = True
                    except bzrlib.errors.NoSuchId:
                        # the actual file id didn't exist at that time
                        pass
                if not found and old_file_id is not None:
                    # finally tries with the old file id
                    content = rev_tree.get_file_text(old_file_id)
                    found = True
                if not found:
                    # can't be found anywhere
                    raise bzrlib.errors.BzrCommandError(
                        "%r is not present in revision %s" % (
                            filename, rev_tree.get_revision_id()))

                # appends the resource contents to the resources revision list
                resources_revision.append(content)
            finally:
                # always unlocks the branch
                branch.unlock()

        # returns the resources revision list
        return resources_revision

    def create_revision(self, revision_control_reference, revision_identifier):
        # creates the revision
        revision = BazaarRevision()

        # splits the revision attributes in the revision identifier
        revision_attributes = revision_identifier.split("-")

        # retrieves the attributes
        author = revision_attributes[0]
        date = revision_attributes[1]
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

class BazaarRevision:
    """
    The bazaar revision class.
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

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

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
