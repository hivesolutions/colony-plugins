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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 1089 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-01-22 23:19:39 +0000 (qui, 22 Jan 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class BusinessBaseEngine:
    """
    The business base engine class
    """

    business_base_engine_plugin = None
    """ The business base engine plugin """

    def __init__(self, business_base_engine_plugin):
        """
        Constructor of the class

        @type business_base_engine_plugin: BusinessBaseEnginePlugin
        @param business_base_engine_plugin: The business base engine plugin
        """

        self.business_base_engine_plugin = business_base_engine_plugin

    def get_connection_manager(self):
        return BaseConnectionManager

class BaseConnectionManager:
    """
    The base connection Manager class.
    """

    util_manager = None
    """ The util manager help class """

    next_object = None
    """ The next object value """

    def __init__(self, util_manager, next_object = None):
        self.util_manager = util_manager
        self.next_object = next_object

    def create_connection(self, connection_parameters, previous_value = None):
        self.util_manager.call_next(self, "create_connection", [connection_parameters, None])

    def commit_connection(self, connection, previous_value = None):
        pass

    def rollback_connection(self, connection, previous_value = None):
        pass

    def create_transaction(self, connection, transaction_name, previous_value = None):
        pass

    def commit_transaction(self, connection, transaction_name, previous_value = None):
        pass

    def rollback_transaction(self, connection, transaction_name, previous_value = None):
        pass

class BaseSchemaManager:

    def exists_entity_definition(self, connection, entity_class):
        pass

    def exists_table_definition(self, connection, table_name):
        pass

    def exists_table_column_definition(self, connection, table_name, column_name):
        pass

class UtilManager:
    """
    The util manager class.
    """

    def call_next(self, self_value, method_name, *args):
        current_object = self_value.next_object

        while current_object:
            if method_name in dir(current_object):
                method = getattr(current_object, method_name)
                return method(*args)

            current_object = current_object.next_object
