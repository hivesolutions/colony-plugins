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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainServiceAbeculaCommunicationPushHandlerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Abecula Service Main Communication Push Handler plugin.
    """

    id = "pt.hive.colony.plugins.main.service.abecula.communication_push_handler"
    name = "Abecula Service Main Communication Push Handler Plugin"
    short_name = "Abecula Service Main Communication Push Handler"
    description = "The plugin that offers the abecula service communication push handler"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_service_abecula_communication_push_handler/communication_push_handler/resources/baf.xml"
    }
    capabilities = [
        "abecula_service_handler",
        "diagnostics",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.communication.push", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.authentication", "1.0.0"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.misc.json", "1.0.0")
    ]
    main_modules = [
        "main_service_abecula_communication_push_handler.communication_push_handler.main_service_abecula_communication_push_handler_exceptions",
        "main_service_abecula_communication_push_handler.communication_push_handler.main_service_abecula_communication_push_handler_system"
    ]

    main_service_abecula_communication_push_handler = None
    """ The main service abecula communication push handler """

    communication_push_plugin = None
    """ The communication push plugin """

    main_authentication_plugin = None
    """ The main authentication plugin """

    json_plugin = None
    """ The json plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_service_abecula_communication_push_handler.communication_push_handler.main_service_abecula_communication_push_handler_system
        self.main_service_abecula_communication_push_handler = main_service_abecula_communication_push_handler.communication_push_handler.main_service_abecula_communication_push_handler_system.MainServiceAbeculaCommunicationPushHandler(self)

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

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.plugin_system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.plugin_system.Plugin.unset_configuration_property(self, property_name)

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.main_service_abecula_communication_push_handler.get_handler_name()

    def handle_request(self, request):
        """
        Handles the given abecula request.

        @type request: AbeculaRequest
        @param request: The abecula request to be handled.
        """

        return self.main_service_abecula_communication_push_handler.handle_request(request)

    def print_diagnostics(self):
        """
        Prints diagnostic information about the plugin instance.
        """

        return self.main_service_abecula_communication_push_handler.print_diagnostics()

    def get_communication_push_plugin(self):
        return self.communication_push_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.communication.push")
    def set_communication_push_plugin(self, communication_push_plugin):
        self.communication_push_plugin = communication_push_plugin

    def get_main_authentication_plugin(self):
        return self.main_authentication_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.authentication")
    def set_main_authentication_plugin(self, main_authentication_plugin):
        self.main_authentication_plugin = main_authentication_plugin

    def get_json_plugin(self):
        return self.json_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.json")
    def set_json_plugin(self, json_plugin):
        self.json_plugin = json_plugin

    @colony.base.decorators.set_configuration_property_method("handler_configuration")
    def handler_configuration_set_configuration_property(self, property_name, property):
        self.main_service_abecula_communication_push_handler.set_handler_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("handler_configuration")
    def handler_configuration_unset_configuration_property(self, property_name):
        self.main_service_abecula_communication_push_handler.unset_handler_configuration_property()
