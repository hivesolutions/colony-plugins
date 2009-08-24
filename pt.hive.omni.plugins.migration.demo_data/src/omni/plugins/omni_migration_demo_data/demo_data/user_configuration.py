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

PLAINTEXT_VALUE = "plaintext"

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

class UserConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni User entities from the demo data.
    """

    omni_migration_demo_data_plugin = None
    """ The omni migration demo data plugin """

    def __init__(self, omni_migration_demo_data_plugin):
        self.omni_migration_demo_data_plugin = omni_migration_demo_data_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines the post attribute mapping handlers that must be run after the attribute mapping step has completed
        self.post_attribute_mapping_handlers = [{FUNCTION_VALUE : self.post_attribute_mapping_handler_create_users}]

    def post_attribute_mapping_handler_create_users(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_demo_data_plugin.info("Creating default users")

        user_entity = output_intermediate_structure.create_entity("User")
        user_entity.set_attribute("username", "guest")
        user_entity.set_attribute("password_hash", "guest")
        user_entity.set_attribute("password_hash_type", PLAINTEXT_VALUE)
        user_entity.set_attribute("status", OMNI_ACTIVE_ENTITY_STATUS)

        return output_intermediate_structure
