#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Omni ERP
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Omni ERP.
#
# Hive Omni ERP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Omni ERP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Omni ERP. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import generic_configuration_handlers

CHILD_TREE_NODE_ENTITY_NAMES_VALUE = "tree_node_entity_names"

ROOT_TREE_NODE_ENTITY_NAME_VALUE = "root_tree_node_entity_name"

TREE_ENTITY_NAME_VALUE = "tree_entity"

class CustomerHierarchyTreeConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni CustomerHierarchyTree entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines the handlers that must be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : generic_configuration_handlers.post_conversion_handler_create_tree,
                                          ARGUMENTS_VALUE : {TREE_ENTITY_NAME_VALUE : "CustomerHierarchyTree",
                                                             ROOT_TREE_NODE_ENTITY_NAME_VALUE : "OrganizationalHierarchyTreeNode",
                                                             CHILD_TREE_NODE_ENTITY_NAMES_VALUE : ["CustomerPerson", "CustomerCompany"]}}]
