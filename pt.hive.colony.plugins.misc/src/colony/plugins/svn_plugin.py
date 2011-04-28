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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class SvnPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Svn plugin.
    """

    id = "pt.hive.colony.plugins.misc.svn"
    name = "Svn Plugin"
    short_name = "Svn"
    description = "A plugin to manage svn repositories"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/misc/svn/resources/baf.xml"
    }
    capabilities = [
        "svn",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PackageDependency("PySvn", "pysvn", "1.6.2.x", "http://pysvn.tigris.org")
    ]
    main_modules = [
        "misc.svn.svn_system"
    ]

    svn = None
    """ The svn """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.svn.svn_system
        self.svn = misc.svn.svn_system.Svn(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def create_svn_client(self, svn_client_path):
        return self.svn.create_svn_client(svn_client_path)

    def svn_set_default_username(self, username):
        return self.svn.svn_set_default_username(username)

    def svn_add_login(self, realm, username, password):
        return self.svn.svn_add_login(realm, username, password)

    def svn_checkin(self, checkin_path, message):
        return self.svn.svn_checkin(checkin_path, message)

    def svn_checkout(self, repository_url, checkout_directory, revision):
        return self.svn.svn_checkout(repository_url, checkout_directory, revision)
