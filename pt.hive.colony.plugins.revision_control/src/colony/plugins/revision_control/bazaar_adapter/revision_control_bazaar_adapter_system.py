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

import bzrlib
import bzrlib.builtins

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
        pass

    def update(self, revision_control_reference, resource_identifiers, revision_identifier):
        # retrieves the first resource identifier
        resource_identifier = resource_identifiers[0]

        # creates the update command
        update_command = bzrlib.builtins.cmd_update()

        # runs the update command
        return_revision_identifier = update_command.run(resource_identifier)

        return return_revision_identifier

    def get_adapter_name(self):
        return ADAPTER_NAME
