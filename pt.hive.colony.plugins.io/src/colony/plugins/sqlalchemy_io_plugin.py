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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2112 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 15:23:46 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class SqlAlchemyInputOutputPlugin(colony.plugins.plugin_system.Plugin):

    id = "pt.hive.colony.plugins.io.sqlalchemy"
    name = "SqlAlchemy input/output plugin"
    short_name = "SqlAlchemy I/O"
    description = "description here"
    version = "1.0.0"
    author = "Hive Solutions"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["io.sqlalchemy"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PackageDependency(
                    "SQL Alchemy O/R mapper", "sqlalchemy", "0.4.x", "http://www.sqlalchemy.org"),
                    colony.plugins.plugin_system.PackageDependency(
                    "MySQL-Python", "MySQLdb", "1.2.x", "http://mysql-python.sourceforge.net")]
    events_handled = []
    events_registrable = []
    valid = True

    codebase = None
    """ Base code supplied by this plugin, meant to be accessible only with the methods supplied by the plugin class"""

    def __init__(self, manager):
        colony.plugins.plugin_system.Plugin.__init__(self, manager)

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)    
        global io
        import io.sqlalchemy.sqlalchemy_io
        self.codebase = io.sqlalchemy.sqlalchemy_io.SqlAlchemyInputOutput()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)
        self.codebase.drop_connection()
        self.codebase = None

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def flush(self):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.flush()
        """
        return self.codebase.flush()

    def delete(self, object):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.delete()
        """
        return self.codebase.delete(object)

    def save(self, object):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.save()
        """
        return self.codebase.save(object)

    def update(self, object):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.update()
        """
        return self.codebase.update(object)

    def save_or_update(self, object):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.save_or_update()
        """
        return self.codebase.save_or_update(object)

    def query(self, object):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.query()
        """
        return self.codebase.query(object)

    def next_primary_key(self, primary_key_name, allocation_size):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.next_primary_key()
        """
        return self.codebase.next_primary_key(primary_key_name, allocation_size)

    def get_engine(self):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.get_engine()
        """
        return self.codebase.get_engine()

    def create_engine(self, database_server_type = None, username = None, password = None, database_name = None, hostname = "localhost", port = "3306"):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.get_engine()
        """
        return self.codebase.get_engine(database_server_type, username, password, database_name, hostname, port)

    def get_metadata(self):
        return self.codebase.get_metadata()

    def get_session(self):
        return self.codebase.get_session()

    def get_connection(self):
        return self.codebase.get_connection()

    def metadata_create_all(self):
        self.codebase.metadata_create_all()

    def begin_transaction(self):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.begin_transaction()
        """
        self.codebase.begin_transaction()

    def commit_transaction(self):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.commit_transaction()
        """
        self.codebase.commit_transaction()

    def rollback_transaction(self):
        """
        @see: colony.plugins.io_sqlalchemy.sqlalchemy.sqlalchemy_io.rollback_transaction()
        """
        self.codebase.rollback_transaction()
