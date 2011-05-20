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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class BonjourPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Bonjour plugin.
    """

    id = "pt.hive.colony.plugins.misc.bonjour"
    name = "Bonjour Plugin"
    short_name = "Bonjour"
    description = "A plugin to manage the bonjour API"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/misc/bonjour/resources/baf.xml"
    }
    capabilities = [
        "thread",
        "bonjour",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.guid", "1.0.0"),
        colony.base.plugin_system.PackageDependency("Bonjour", "bonjour", "0.2.x", "http://www.apple.com")
    ]
    main_modules = [
        "misc.bonjour.bonjour_exceptions",
        "misc.bonjour.bonjour_system"
    ]

    bonjour = None
    """ The bonjour """

    guid_plugin = None
    """ The guid plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import misc.bonjour.bonjour_system
        self.bonjour = misc.bonjour.bonjour_system.Bonjour(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

        # starts the browsing loop
        self.bonjour.start_browsing_loop()

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

        self.bonjour.stop_browsing_loop()

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.misc.bonjour", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def add_service_for_browsing(self, registration_type, domain):
        return self.bonjour.add_service_for_browsing(registration_type, domain)

    def remove_service_for_browsing(self, registration_type, domain):
        return self.bonjour.remove_service_for_browsing(registration_type, domain)

    def register_bonjour_service(self, service_name, registration_type, domain, host, port):
        return self.bonjour.register_bonjour_service(service_name, registration_type, domain, host, port)

    def browse_bonjour_services(self, registration_type, domain, timeout):
        return self.bonjour.browse_bonjour_services(registration_type, domain, timeout)

    def browse_bonjour_services_fast(self, registration_type, domain):
        return self.bonjour.browse_bonjour_services_fast(registration_type, domain)

    def get_guid_plugin(self):
        return self.guid_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.guid")
    def set_guid_plugin(self, guid_plugin):
        self.guid_plugin = guid_plugin
