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

import os.path
import mercurial
import mercurial.hg
import mercurial.commands
import mercurial.merge

ADAPTER_NAME = "hg"

MERCURIAL_RESOLVED_STATE_VALUE = "r"
""" The state signaling a conflict has been resolved """

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

    def update(self, resource_identifiers, revision_identifier):
        # retrieves the first resource identifier
        resource_identifier = resource_identifiers[0]

        # retrieves the repository
        repository = self.get_repository(resource_identifier)

        if revision_identifier:
            # retrieves the change context for the specified identifier
            change_context = repository[revision_identifier]

            # retrieves the node
            node = change_context.node()
        else:
            # the node defaults to true
            node = None

        # updates the working directory to node
        mercurial.hg.update(repository, node)

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
