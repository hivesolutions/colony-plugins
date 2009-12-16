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

    subversion_client = None
    """ The subversion client object """

    def __init__(self, revision_control_subversion_adapter_plugin):
        """
        Constructor of the class.

        @type revision_control_subversion_adapter_plugin: RevisionControlSubversionAdapter
        @param revision_control_subversion_adapter_plugin: The revision control mecurial adapter plugin.
        """

        # sets the subversion adapter plugin
        self.revision_control_subversion_adapter_plugin = revision_control_subversion_adapter_plugin

        # initializes the subversion client
        self.subversion_client = pysvn.Client()

    def update(self, resource_identifiers, revision_identifier):
        # retrieves the first resource identifier
        resource_identifier = resource_identifiers[0]

        # in case a revision is specified
        if revision_identifier:
            # creates the subversion revision
            revision = pysvn.Revision(DEFAULT_REVISION_KIND, revision_identifier)
        else:
            # updates to the head revision
            revision = pysvn.Revision(pysvn.opt_revision_kind.head)

        # performs the update
        update_result = self.subversion_client.update(resource_identifier, True, revision)

        return update_result

    def get_adapter_name(self):
        return ADAPTER_NAME
