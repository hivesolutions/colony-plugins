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

class RevisionControlManager:
    """
    The revision control manager class.
    """

    revision_control_manager_plugin = None
    """ The revision control manager plugin """

    def __init__(self, revision_control_manager_plugin):
        """
        Constructor of the class.

        @type revision_control_manager_plugin: RevisionControlManagerPlugin
        @param revision_control_manager_plugin: The revision control manager plugin.
        """

        self.revision_control_manager_plugin = revision_control_manager_plugin

    def load_revision_control_manager(self, adapter_name, revision_control_parameters):
        """
        Creates a revision control manager for the specified adapter name.

        @type adapter_name: String
        @param adapter_name: The name of the adapter to for loading the revision control manager
        @type revision_control_parameters: Dictionary
        @param revision_control_parameters: The parameters with which to load revision control manager
        """

        # retrieve the first revision control manager adapter for the specified adapter name
        revision_control_adapter_plugin  = self.get_revision_control_adapter_plugin(adapter_name)

        # creates the revision control adapter using the retrieved adapter plugin
        revision_control_adapter = RevisionControlAdapter(revision_control_adapter_plugin)

        # loads the revision control adapter with the specified revision control parameters
        revision_control_adapter.load(revision_control_parameters)

        # returns the create revision control adapter
        return revision_control_adapter

    def get_revision_control_adapter_plugin(self, adapter_name):
        # retrieve the first revision control manager adapter for the specified adapter name
        for revision_control_adapter_plugin in self.revision_control_manager_plugin.revision_control_adapter_plugins:
            # retrieves the adapter name for the current plugin
            revision_control_adapter_plugin_adapter_name = revision_control_adapter_plugin.get_adapter_name()

            # in case the adapter plugin has the specified adapter name
            if revision_control_adapter_plugin_adapter_name == adapter_name:
                # uses the adapter plugin as the relevant copy
                return revision_control_adapter_plugin

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
        """

        # sets the revision control parameters
        self.revision_control_parameters = revision_control_parameters

        # creates the revision control reference using the configured plugin
        self._revision_control_reference = self.revision_control_adapter_plugin.create_revision_control_reference(revision_control_parameters)

    def update(self, resource_identifiers, revision):
        """
        Update working directory.
        """

        return self.revision_control_adapter_plugin.update(self._revision_control_reference, resource_identifiers, revision)

    def commit(self, resource_identifiers, commit_message):
        """
        Commit the specified files or all outstanding changes.
        """

        return self.revision_control_adapter_plugin.commit(self._revision_control_reference, resource_identifiers, commit_message)

    def log(self, resource_identifiers, start_revision, end_revision):
        """
        Show revision history of entire repository or files.
        """

        return self.revision_control_adapter_plugin.log(self._revision_control_reference, resource_identifiers, start_revision, end_revision)

    def status(self, resource_identifiers):
        """
        Retrieves the status of the provided resource identifiers.
        """

        return self.revision_control_adapter_plugin.status(self._revision_control_reference, resource_identifiers)

class Revision:
    number = None
    identifier = None

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def get_identifier(self):
        return self.identifier

    def set_identifier(self, identifier):
        self.identifier = identifier
